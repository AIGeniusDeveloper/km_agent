"""
Unit tests for LocalKnowledgeRetriever.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.rag.retriever import LocalKnowledgeRetriever
from app.core.exceptions import RAGRetrievalError

@pytest.mark.asyncio
class TestLocalKnowledgeRetriever:
    
    @pytest.fixture
    def mock_chroma(self):
        """Create a mock ChromaDB instance."""
        with patch('app.rag.retriever.Chroma') as mock:
            yield mock
    
    @pytest.fixture
    def retriever(self, mock_chroma):
        """Create a LocalKnowledgeRetriever with mocked ChromaDB."""
        return LocalKnowledgeRetriever()
    
    async def test_retrieve_documents(self, retriever):
        """Test successful document retrieval."""
        # Mock document
        mock_doc = MagicMock()
        mock_doc.page_content = "Solar panels should be cleaned every 6 months."
        mock_doc.metadata = {"sector": "solar", "source": "manual.pdf"}
        
        retriever.vector_db.similarity_search = MagicMock(return_value=[mock_doc])
        
        results = await retriever.retrieve("cleaning solar panels", "solar", k=3)
        
        assert len(results) == 1
        assert results[0]["content"] == "Solar panels should be cleaned every 6 months."
        assert results[0]["metadata"]["sector"] == "solar"
    
    async def test_retrieve_empty_results(self, retriever):
        """Test retrieval with no matching documents."""
        retriever.vector_db.similarity_search = MagicMock(return_value=[])
        
        results = await retriever.retrieve("unknown query", "solar")
        
        assert len(results) == 0
    
    async def test_retrieve_error_handling(self, retriever):
        """Test error handling during retrieval."""
        retriever.vector_db.similarity_search = MagicMock(side_effect=Exception("DB error"))
        
        with pytest.raises(RAGRetrievalError):
            await retriever.retrieve("test query", "solar")
    
    def test_add_documents(self, retriever):
        """Test adding documents to the vector DB."""
        retriever.vector_db.add_texts = MagicMock()
        
        docs = ["Document 1", "Document 2"]
        metadata = [{"sector": "solar"}, {"sector": "solar"}]
        
        retriever.add_documents(docs, metadata)
        
        retriever.vector_db.add_texts.assert_called_once_with(texts=docs, metadatas=metadata)
