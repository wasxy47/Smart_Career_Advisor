from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from src.config import Config  # <--- NEW IMPORT
import json
import os

class CareerVectorStore:
    def __init__(self):
        # Use the model name from Config
        print(f"Loading embedding model: {Config.EMBEDDING_MODEL}...")
        self.embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        self.vector_db = None

    def ingest_data(self, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        documents = []
        for role in data['roles']:
            content = f"Role: {role['title']}. Description: {role['description']}. Skills: {', '.join(role['skills'])}."
            doc = Document(page_content=content, metadata={"title": role['title'], "type": "role"})
            documents.append(doc)

        # Use the Persistent Path from Config (optional, but good practice)
        self.vector_db = Chroma.from_documents(documents, self.embeddings)
        print("Vector Store Created Successfully.")

    def search(self, query, k=2):
        if not self.vector_db:
            return [] 
        return self.vector_db.similarity_search(query, k=k)