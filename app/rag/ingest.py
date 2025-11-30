import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from app.rag.retriever import LocalKnowledgeRetriever

def ingest_data():
    retriever = LocalKnowledgeRetriever()
    
    # Get the directory where this script is located (app/rag)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to get to km_agent root, then into data
    data_dir = os.path.join(current_dir, "../../data")
    files = {
        "solar": "solar_data.md",
        "mechanics": "mechanics_data.md",
        "agritech": "agritech_data.md",
        "construction": "construction_data.md"
    }

    documents = []
    metadatas = []

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    for sector, filename in files.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            loader = TextLoader(file_path)
            docs = loader.load()
            chunks = text_splitter.split_documents(docs)
            
            for chunk in chunks:
                documents.append(chunk.page_content)
                metadatas.append({"sector": sector, "source": filename})
            
            print(f"Loaded {len(chunks)} chunks for {sector}")
        else:
            print(f"File not found: {file_path}")

    if documents:
        retriever.add_documents(documents, metadatas)
        print("Ingestion complete.")
    else:
        print("No documents to ingest.")

if __name__ == "__main__":
    ingest_data()
