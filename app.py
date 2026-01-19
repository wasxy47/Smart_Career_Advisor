import streamlit as st
import streamlit.components.v1 as components
import os
from src.config import Config
from src.graph_builder import CareerGraph
from src.vector_store import CareerVectorStore
from src.retriever import HybridRetriever
from src.agent import CareerAgent

st.set_page_config(page_title="Smart Career Advisor", layout="wide")
st.title("🤖 Smart GraphRAG Career Advisor")
st.markdown("Ask about job roles, skills, or career paths.")

@st.cache_resource
def setup_system():
    # Use Config paths instead of hardcoded strings
    graph = CareerGraph()
    graph.load_data(Config.DATA_PATH)
    
    vector = CareerVectorStore()
    vector.ingest_data(Config.DATA_PATH)
    
    retriever = HybridRetriever(graph, vector)
    agent = CareerAgent(retriever)
    return agent, graph

try:
    agent, graph_system = setup_system()
    
    tab1, tab2 = st.tabs(["💬 AI Advisor", "🕸️ Knowledge Graph"])

    with tab1:
        user_query = st.text_input("Enter your career question:", "How do I become an AI Engineer?")
        if st.button("Get Advice"):
            if user_query:
                with st.spinner("Analyzing Knowledge Graph..."):
                    # Run the agent
                    result = agent.run(user_query)
                    
                    st.markdown("### 💡 AI Advice:")
                    
                    # --- NEW RESPONSE PARSING LOGIC ---
                    final_text = ""
                    
                    # Check if result is a dictionary (The LangGraph State)
                    if isinstance(result, dict) and "response" in result:
                        content = result["response"]
                        
                        # Case 1: Standard LangChain Message Object
                        if hasattr(content, "content"):
                            final_text = content.content
                        
                        # Case 2: List of dictionaries (The Google/Gemini JSON format you saw)
                        elif isinstance(content, list) and len(content) > 0:
                            first_item = content[0]
                            if isinstance(first_item, dict):
                                final_text = first_item.get("text", str(content))
                            else:
                                final_text = str(content)
                                
                        # Case 3: It is just a string
                        elif isinstance(content, str):
                            final_text = content
                        else:
                            final_text = str(content)
                            
                    # Fallback if result isn't a dict
                    else:
                        final_text = str(result)

                    # Display the cleaned text
                    st.markdown(final_text)
            else:
                st.warning("Please enter a question.")

    # TAB 2: The Visual Graph
    with tab2:
        st.header("Visualizing the Career Network")
        
        # Two columns for controls
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Dropdown to pick a role (sorted alphabetically)
            if graph_system and graph_system.graph:
                all_nodes = sorted(list(graph_system.graph.nodes))
                selected_node = st.selectbox("Focus on a specific Role or Skill:", ["Full Network"] + all_nodes)
            else:
                selected_node = "Full Network"

        with col2:
            st.write("") # Spacer
            st.write("") # Spacer
            generate_btn = st.button("Generate View")

        if generate_btn:
            output_file = "graph.html"
            
            if selected_node == "Full Network":
                st.info("Generating full network map... (This might look crowded!)")
                path = graph_system.visualize(output_file)
            else:
                st.success(f"Generating focused path for: **{selected_node}**")
                # Call our visualizer method
                path = graph_system.visualize_path(selected_node, output_file)

            # Display the result
            if path and os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                components.html(source_code, height=650, scrolling=True)
            else:
                st.error("Could not generate graph. Please check if the node exists.")

except Exception as e:
    st.error(f"Error initializing system: {e}")