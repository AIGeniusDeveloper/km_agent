"""
Custom exceptions for KM-Agent.
"""

class KMAgentError(Exception):
    """Base exception for all KM-Agent errors."""
    pass

class SectorRoutingError(KMAgentError):
    """Raised when sector routing fails."""
    pass

class RAGRetrievalError(KMAgentError):
    """Raised when RAG retrieval fails."""
    pass

class LLMError(KMAgentError):
    """Raised when LLM invocation fails."""
    pass

class SimulationError(KMAgentError):
    """Raised when simulation operations fail."""
    pass

class ConfigurationError(KMAgentError):
    """Raised when configuration is invalid."""
    pass
