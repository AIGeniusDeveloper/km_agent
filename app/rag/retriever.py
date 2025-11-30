import os
from typing import List, Dict
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import get_settings
from app.core.exceptions import RAGRetrievalError
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class LocalKnowledgeRetriever:
    def __init__(self):
        try:
            # Using Google Embeddings for now, can switch to others
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GOOGLE_API_KEY
            )
            self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
            
            # Initialize ChromaDB client
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name="km_agent_knowledge"
            )
            logger.info("LocalKnowledgeRetriever initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize retriever: {str(e)}", exc_info=True)
            raise RAGRetrievalError(f"Failed to initialize knowledge retriever: {str(e)}") from e

    async def retrieve(self, query: str, sector: str, k: int = 3) -> List[Dict]:
        """
        Retrieve documents relevant to the query and sector.
        """
        try:
            logger.info(f"Retrieving documents for sector '{sector}', query: {query[:50]}...")
            results = self.vector_db.similarity_search(
                query,
                k=k,
                filter={"sector": sector}
            )
            logger.info(f"Retrieved {len(results)} documents")
            return [
                {"content": doc.page_content, "metadata": doc.metadata}
                for doc in results
            ]
        except Exception as e:
            logger.error(f"Retrieval failed: {str(e)}", exc_info=True)
            raise RAGRetrievalError(f"Failed to retrieve documents: {str(e)}") from e

    def add_documents(self, documents: List[str], metadatas: List[Dict]):
        """
        Add documents to the vector DB.
        """
        try:
            self.vector_db.add_texts(texts=documents, metadatas=metadatas)
            logger.info(f"Added {len(documents)} documents to vector DB")
        except Exception as e:
            logger.error(f"Failed to add documents: {str(e)}", exc_info=True)
            raise RAGRetrievalError(f"Failed to add documents: {str(e)}") from e
