import os
from dotenv import load_dotenv

# Load the .env file immediately when this module is imported
load_dotenv()

class Config:
    # 1. API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # 2. Model Settings (Change these here to update the whole app!)
    LLM_MODEL = "gemini-flash-latest" 
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # 3. File Paths
    # We use os.path.join to make sure it works on Windows and Mac
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "career_data.json")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "chroma_db")