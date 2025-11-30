from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core.config import get_settings
from app.agents.core import AgentCore

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

agent_core = AgentCore()

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
