from typing import Literal, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import get_settings
from app.core.llm_factory import get_llm
from app.core.exceptions import SectorRoutingError
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class SectorRoute(BaseModel):
    """Route the user query to the most appropriate sector."""
    sector: Literal["solar", "mechanics", "agritech", "construction", "general"] = Field(
        ...,
        description="The sector that best matches the user query. Use 'general' if it doesn't fit any specific sector."
    )
    confidence: float = Field(..., description="Confidence score between 0 and 1.")
    reasoning: str = Field(..., description="Brief explanation of why this sector was chosen.")



class SectorRouter:
    def __init__(self):
        # Using Gemini Flash (or Pro if configured) for routing with low temp
        self.llm = get_llm(temperature=0, model_name="gemini-1.5-flash-001")
        self.parser = PydanticOutputParser(pydantic_object=SectorRoute)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert router for a technical assistant. "
                       "Your job is to classify user queries into one of the following sectors: "
                       "Solar Energy (solar), Mechanics/Maintenance (mechanics), "
                       "AgriTech (agritech), or ConstructionTech (construction). "
                       "If the query is not related to these, or is a general greeting, use 'general'.\n"
                       "{format_instructions}"),
            ("user", "{query}")
        ]).partial(format_instructions=self.parser.get_format_instructions())

        self.chain = self.prompt | self.llm | self.parser

    async def route_query(self, query: str) -> SectorRoute:
        try:
            logger.info(f"Routing query: {query[:50]}...")
            result = await self.chain.ainvoke({"query": query})
            logger.info(f"Routed to sector: {result.sector} (confidence: {result.confidence})")
            return result
        except Exception as e:
            logger.error(f"Routing failed: {str(e)}", exc_info=True)
            raise SectorRoutingError(f"Failed to route query: {str(e)}") from e
