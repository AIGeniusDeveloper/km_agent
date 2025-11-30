import os
from typing import List, Dict
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import get_settings

settings = get_settings()

class LocalKnowledgeRetriever:
    def __init__(self):
        # Using Google Embeddings for now, can switch to others
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        
        # Initialize ChromaDB client
        # We will have separate collections for each sector or use metadata filtering
        # For MVP, let's use a single DB with metadata filtering
        self.vector_db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="km_agent_knowledge"
        )

    async def retrieve(self, query: str, sector: str, k: int = 3) -> List[Dict]:
        """
        Retrieve documents relevant to the query and sector.
        """
        # Filter by sector metadata
        results = self.vector_db.similarity_search(
            query,
            k=k,
            filter={"sector": sector}
        )
        
        return [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]

    def add_documents(self, documents: List[str], metadatas: List[Dict]):
        """
        Add documents to the vector DB.
        """
        self.vector_db.add_texts(texts=documents, metadatas=metadatas)
