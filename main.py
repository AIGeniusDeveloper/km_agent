from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.config import get_settings
from app.agents.core import AgentCore
from app.agents.orchestrator import SectorRouter
from app.agents.translator import ContextualTranslator
from app.rag.retriever import LocalKnowledgeRetriever
from app.tools.simulator import TaskSimulator
from app.core.exceptions import SectorRoutingError, RAGRetrievalError, LLMError
from app.api.voice import router as voice_router
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include voice router
app.include_router(voice_router)

# Dependency Injection: Create dependencies explicitly
sector_router = SectorRouter()
knowledge_retriever = LocalKnowledgeRetriever()
task_simulator = TaskSimulator()
translator = ContextualTranslator()

# Inject dependencies into AgentCore
agent_core = AgentCore(
    router=sector_router,
    retriever=knowledge_retriever,
    simulator=task_simulator,
    translator=translator
)

class ChatRequest(BaseModel):
    query: str
    sector_hint: str = None
    session_id: str = "default"
    image_base64: str = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

@app.get("/")
async def root():
    return {"message": "Welcome to KM-Agent FP Multi-Secteurs API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await agent_core.process_query(
            query=request.query, 
            session_id=request.session_id, 
            sector_hint=request.sector_hint,
            image_base64=request.image_base64
        )
        return result
    except SectorRoutingError as e:
        raise HTTPException(status_code=422, detail={"error": "routing_failed", "message": str(e)})
    except RAGRetrievalError as e:
        raise HTTPException(status_code=503, detail={"error": "retrieval_failed", "message": str(e)})
    except LLMError as e:
        raise HTTPException(status_code=503, detail={"error": "llm_failed", "message": str(e)})
    except Exception as e:
        logger.error(f"Unexpected error in /chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "internal_error", "message": "An unexpected error occurred"})

class SimulationStartRequest(BaseModel):
    sector: str

class SimulationStepRequest(BaseModel):
    scenario_id: str
    step_index: int
    user_action: str

@app.post("/simulate/start")
async def start_simulation(request: SimulationStartRequest):
    return agent_core.start_simulation(request.sector)

@app.post("/simulate/step")
async def evaluate_simulation_step(request: SimulationStepRequest):
    return agent_core.evaluate_simulation_step(request.scenario_id, request.step_index, request.user_action)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
