from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.config import Config  # <--- NEW IMPORT

# Define State
class AgentState(TypedDict):
    query: str
    context: str
    response: str

class CareerAgent:
    def __init__(self, retriever):
        self.retriever = retriever
        # Use the Model Name from Config
        self.llm = ChatGoogleGenerativeAI(model=Config.LLM_MODEL, temperature=0)
        self.workflow = self._build_workflow()

    def retrieve_node(self, state: AgentState):
        query = state['query']
        print(f"--- Retrieving info for: {query} ---")
        context = self.retriever.retrieve(query)
        return {"context": context}

    def generate_node(self, state: AgentState):
        query = state['query']
        context = state['context']
        print("--- Generating Response ---")

        prompt = f"""
        You are a Smart Career Advisor. Use the retrieved context below to answer the user's career question.
        
        Context from Knowledge Graph & Database:
        {context}

        User Question: {query}

        If the context has salary, mention it. If it has prerequisites, list them clearly.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return {"response": response.content}

    def _build_workflow(self):
        builder = StateGraph(AgentState)
        builder.add_node("retrieve", self.retrieve_node)
        builder.add_node("generate", self.generate_node)
        builder.set_entry_point("retrieve")
        builder.add_edge("retrieve", "generate")
        builder.add_edge("generate", END)
        return builder.compile()

    def run(self, query: str):
        result = self.workflow.invoke({"query": query})
        return result["response"]