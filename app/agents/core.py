from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.core.config import get_settings
from app.agents.orchestrator import SectorRouter
from app.agents.translator import ContextualTranslator
from app.rag.retriever import LocalKnowledgeRetriever
from app.tools.simulator import TaskSimulator
from app.core.llm_factory import get_llm

settings = get_settings()

# Global store for in-memory chat history (Use Redis in production)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

class AgentCore:
    def __init__(
        self,
        router: SectorRouter,
        retriever: LocalKnowledgeRetriever,
        simulator: TaskSimulator,
        translator: ContextualTranslator = None
    ):
        """
        Initialize AgentCore with injected dependencies.
        
        Args:
            router: SectorRouter instance for query classification
            retriever: LocalKnowledgeRetriever for RAG
            simulator: TaskSimulator for training scenarios
            translator: Optional ContextualTranslator for multilingual support
        """
        self.router = router
        self.translator = translator or ContextualTranslator()
        self.retriever = retriever
        self.simulator = simulator
        
        # Initialize LLM for response generation (higher temp for creativity)
        self.llm = get_llm(temperature=0.3, model_name="gemini-2.5-pro")
        
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical assistant for the {sector} sector. "
                       "Answer the user's question based ONLY on the provided context. "
                       "If the context doesn't contain the answer, say so politely. "
                       "IMPORTANT: Answer in the same language as the user's question."),
            MessagesPlaceholder(variable_name="history"),
            ("user", "Context:\n{context}\n\nQuestion: {query}")
        ])
        
        chain = self.response_prompt | self.llm
        
        self.response_chain = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="query",
            history_messages_key="history"
        )

    async def process_query(self, query: str, session_id: str = "default", sector_hint: str = None, image_base64: str = None) -> Dict[str, Any]:
        """
        Process a user query with memory and optional image:
        1. Translate input (if needed)
        2. Route to sector (if hint not provided)
        3. Retrieve info
        4. Generate response using LLM with History and Image
        5. Translate output (if needed)
        """
        
        # 1. Routing
        if sector_hint:
            sector = sector_hint
            confidence = 1.0
            reasoning = "User provided hint"
        else:
            route = await self.router.route_query(query)
            sector = route.sector
            confidence = route.confidence
            reasoning = route.reasoning

        # 2. Retrieval
        retrieved_docs = []
        if sector != "general":
            retrieved_docs = await self.retriever.retrieve(query, sector)
        
        context_text = "\n\n".join([doc["content"] for doc in retrieved_docs])

        # 3. Response Generation with Memory & Image
        from langchain_core.messages import HumanMessage
        
        input_message_content = [
            {"type": "text", "text": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
        
        if image_base64:
            input_message_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })
            
        # We need to manually invoke the chain with the constructed message if image is present
        # Or update the prompt to handle it. 
        # For simplicity with RunnableWithMessageHistory, we'll pass the complex input to 'query'
        # But standard prompt templates expect string for 'query'.
        # Let's adjust the prompt strategy slightly for images.
        
        if image_base64:
             # Direct invocation for image cases (bypassing the standard prompt template for the input part)
             # We still want history though.
             # LangChain's history wrapper works best with text inputs.
             # For this MVP, we will append the image to the message sent to the model.
             
             # Create a specific message for this turn
             message = HumanMessage(content=input_message_content)
             
             # We invoke the LLM directly with history + new message
             # This bypasses the prompt template which is text-only
             history = get_session_history(session_id)
             messages = history.messages + [message]
             
             # Add system prompt manually
             system_prompt = f"You are an expert technical assistant for the {sector} sector. Answer based on context and image."
             from langchain_core.messages import SystemMessage
             full_messages = [SystemMessage(content=system_prompt)] + messages
             
             response_msg = await self.llm.ainvoke(full_messages)
             
             # Update history manually
             history.add_user_message(message)
             history.add_ai_message(response_msg)
             
             response_text = response_msg.content
             
        else:
            response_msg = await self.response_chain.ainvoke(
                {
                    "sector": sector,
                    "context": context_text,
                    "query": query
                },
                config={"configurable": {"session_id": session_id}}
            )
            response_text = response_msg.content
        
        return {
            "response": response_text,
            "sector": sector,
            "confidence": confidence,
            "reasoning": reasoning,
            "context": retrieved_docs
        }

    def start_simulation(self, sector: str) -> Dict[str, Any]:
        scenario = self.simulator.get_scenario(sector)
        if not scenario:
            return {"error": f"No scenario found for sector {sector}"}
        return {
            "scenario_id": scenario.id,
            "title": scenario.title,
            "description": scenario.description,
            "first_step": scenario.steps[0]["instruction"]
        }

    def evaluate_simulation_step(self, scenario_id: str, step_index: int, user_action: str) -> Dict[str, Any]:
        return self.simulator.evaluate_step(scenario_id, step_index, user_action)
