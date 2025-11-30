"""
Integration tests for FastAPI endpoints.
"""
import pytest
import httpx
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.orchestrator import SectorRoute
from main import app

@pytest.mark.asyncio
class TestAPIEndpoints:
    
    @pytest.fixture
    async def client(self):
        """Create an async test client."""
        async with AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as ac:
            yield ac
    
    async def test_health_check(self, client):
        """Test the health check endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    async def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        assert "KM-Agent" in response.json()["message"]
    
    async def test_chat_endpoint_success(self, client):
        """Test successful chat interaction."""
        # Mock the agent_core.process_query method
        with patch('main.agent_core.process_query', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = {
                "response": "Test response",
                "sector": "solar",
                "confidence": 0.95,
                "reasoning": "Test",
                "context": []
            }
            
            response = await client.post("/chat", json={
                "query": "How do I clean solar panels?",
                "session_id": "test123"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["sector"] == "solar"
            assert "response" in data
    
    async def test_chat_endpoint_with_sector_hint(self, client):
        """Test chat with sector hint."""
        with patch('main.agent_core.process_query', new_callable=AsyncMock) as mock_process:
            mock_process.return_value = {
                "response": "Mechanics response",
                "sector": "mechanics",
                "confidence": 1.0,
                "reasoning": "User hint",
                "context": []
            }
            
            response = await client.post("/chat", json={
                "query": "Engine problem",
                "sector_hint": "mechanics"
            })
            
            assert response.status_code == 200
            assert response.json()["sector"] == "mechanics"
    
    async def test_simulation_start(self, client):
        """Test starting a simulation."""
        with patch('main.agent_core.start_simulation') as mock_start:
            mock_start.return_value = {
                "scenario_id": "solar_001",
                "title": "Test Scenario",
                "description": "Test",
                "first_step": "Step 1"
            }
            
            response = await client.post("/simulate/start", json={
                "sector": "solar"
            })
            
            assert response.status_code == 200
            assert "scenario_id" in response.json()
