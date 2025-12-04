import sys
from src.graph_builder import CareerGraph
from src.vector_store import CareerVectorStore
from src.retriever import HybridRetriever
from src.agent import CareerAgent
from src.config import Config

def main():
    print("\n🚀 Initializing Smart Career Advisor (CLI Mode)...")
    print(f"🔹 Model: {Config.LLM_MODEL}")
    print(f"🔹 Data: {Config.DATA_PATH}")
    
    try:
        # 1. Initialize Components using Config
        graph = CareerGraph()
        graph.load_data(Config.DATA_PATH)
        
        vector = CareerVectorStore()
        vector.ingest_data(Config.DATA_PATH)
        
        retriever = HybridRetriever(graph, vector)
        agent = CareerAgent(retriever)
        
        print("\n✅ System Ready! Type 'exit', 'quit', or 'q' to stop.\n")
        print("-" * 50)

        # 2. Start the Chat Loop
        while True:
            query = input("\n👤 You: ")
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query.strip():
                continue
                
            print("🤖 Advisor is thinking...")
            response = agent.run(query)
            print(f"\n💡 Advisor:\n{response}")
            print("-" * 50)

    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        print("Tip: Check your .env file and API keys.")

if __name__ == "__main__":
    main()