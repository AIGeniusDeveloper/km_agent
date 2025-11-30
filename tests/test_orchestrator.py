"""
Unit tests for SectorRouter.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.orchestrator import SectorRouter, SectorRoute
from app.core.exceptions import SectorRoutingError

@pytest.mark.asyncio
class TestSectorRouter:
    
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
    
    async def test_sector_route_invalid_sector(self):
        """Test that invalid sectors are rejected."""
        with pytest.raises(Exception):  # Pydantic validation error
            SectorRoute(
                sector="invalid_sector",
                confidence=0.5,
                reasoning="Test"
            )
