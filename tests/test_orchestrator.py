"""
Unit tests for SectorRouter.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.orchestrator import SectorRouter, SectorRoute
from app.core.exceptions import SectorRoutingError

@pytest.mark.asyncio
class TestSectorRouter:
    
    async def test_routing_error_handling(self):
        """Test that routing errors are properly raised."""
        router = SectorRouter()
        
        # Mock the chain's ainvoke to raise an exception
        async def mock_ainvoke(*args, **kwargs):
            raise Exception("LLM API error")
        
        router.chain.ainvoke = mock_ainvoke
        
        with pytest.raises(SectorRoutingError) as exc_info:
            await router.route_query("Test query")
        
        assert "Failed to route query" in str(exc_info.value)
    
    async def test_sector_route_model(self):
        """Test SectorRoute model validation."""
        route = SectorRoute(
            sector="solar",
            confidence=0.95,
            reasoning="Test reasoning"
        )
        
        assert route.sector == "solar"
        assert route.confidence == 0.95
        assert route.reasoning == "Test reasoning"
