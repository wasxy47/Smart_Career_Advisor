from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from src.config import Config
import json
import os
import shutil

class CareerVectorStore:
    def __init__(self):
        # 1. FORCE Local Embeddings (Free & Unlimited)
        print(f"Loading local embedding model: {Config.EMBEDDING_MODEL}...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None

    def ingest_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        documents = []
        for role in data['roles']:
            # Create rich context from ALL JSON fields
            content_parts = []
            for key, value in role.items():
                if key == 'id': continue
                
                if isinstance(value, list):
                    value_str = ", ".join(value)
                else:
                    value_str = str(value)
                
                content_parts.append(f"{key.capitalize()}: {value_str}")
            
            full_content = ". ".join(content_parts)
            doc = Document(page_content=full_content, metadata={"title": role['title'], "type": "role"})
            documents.append(doc)

        # 2. Save to Disk so we don't have to rebuild every time
        # This creates the 'chroma_db' folder you were looking for
        if os.path.exists(Config.VECTOR_DB_PATH):
    # 'ignore_errors=True' tells Windows: "If it's locked, just skip it and move on."
            shutil.rmtree(Config.VECTOR_DB_PATH, ignore_errors=True)
            
        self.vector_db = Chroma.from_documents(
            documents, 
            self.embeddings, 
            persist_directory=Config.VECTOR_DB_PATH
        )
        print("Vector Store Created & Saved Successfully.")

    def search(self, query, k=2):
        # 3. Load from Disk if available
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=Config.VECTOR_DB_PATH, 
                embedding_function=self.embeddings
            )
            
        return self.vector_db.similarity_search(query, k=k)