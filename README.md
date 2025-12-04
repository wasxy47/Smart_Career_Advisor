# 🤖 Smart GraphRAG Career Advisor

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange)
![Tech Stack](https://img.shields.io/badge/Stack-LangGraph%20|%20NetworkX%20|%20ChromaDB-purple)

## 📖 Overview

The **Smart GraphRAG Career Advisor** is an advanced AI system designed to provide accurate, structured career guidance. Unlike standard chatbots that may hallucinate job requirements, this system uses **Graph Retrieval-Augmented Generation (GraphRAG)**.

It grounds the Large Language Model (LLM) in a strict **Knowledge Graph** of skills, roles, and prerequisites, ensuring that advice is not just textually similar, but logically connected.

### 🌟 Key Features
* **Hybrid Search Engine:** Combines **Vector Search** (semantic understanding of user queries) with **Graph Traversal** (structured dependency mapping).
* **Interactive Visualization:** A dynamic 3D network graph (using PyVis) that allows users to explore career paths visually.
* **Focus Mode:** An "Ego Graph" algorithm filters the massive network to show only the relevant prerequisites and next steps for a specific role.
* **Stateful Agent:** Uses **LangGraph** to manage conversation state and retrieval workflows.
* **Local Privacy:** Uses local embeddings (`all-MiniLM-L6-v2`) via HuggingFace, keeping vector data on your machine.
* **Multi-Interface:** Includes both a Modern Web UI (Streamlit) and a Developer CLI.

---

## 🏗️ Technical Architecture

The system is composed of four distinct layers:

1.  **The Knowledge Layer (Data):**
    * **NetworkX:** Manages the graph structure (Nodes = Roles/Skills, Edges = Relationships).
    * **ChromaDB:** Stores vector embeddings of job descriptions for fuzzy matching.

2.  **The Logic Layer (Controller):**
    * **Hybrid Retriever:** Merges results from Vector Search (Similarity) and Graph Search (Neighborhoods).
    * **LangGraph:** Orchestrates the flow: `User Query -> Retrieve Context -> Generate Answer`.

3.  **The Intelligence Layer (AI):**
    * **Google Gemini 2.0 Flash:** Synthesizes the retrieved facts into human-readable advice.
    * **HuggingFace:** Provides local embedding models to convert text to vectors.

4.  **The Presentation Layer (UI):**
    * **Streamlit:** Renders the chat interface and HTML graph widgets.
    * **PyVis:** Generates the physics-based network visualization.

---

## 📂 Project Structure

```text
SMART_CAREER_ADVISOR/
├── data/
│   └── career_data.json       # The Database: Contains all roles, skills, and graph edges
├── lib/                       # PyVis Javascript dependencies (auto-generated)
├── src/                       # Source Code
│   ├── __init__.py            # Package marker
│   ├── agent.py               # LangGraph Agent workflow definition
│   ├── config.py              # Central configuration (API Keys, Model names)
│   ├── graph_builder.py       # Graph logic, Ego-graph filtering, Visualization
│   ├── retriever.py           # Hybrid search logic (Vector + Graph combination)
│   └── vector_store.py        # Vector Database management (ChromaDB)
├── .gitignore                 # Security (Prevents uploading API keys)
├── .env                       # Environment Variables (API Keys)
├── app.py                     # Main Web Application entry point
├── check_models.py            # Diagnostic script for Google Gemini models
├── graph.html                 # Temporary output for visualization
├── main.py                    # Command Line Interface (CLI) entry point
└── requirements.txt           # Python dependencies list
```
---

## 🚀 Installation & Setup

### 1. Prerequisites

* Python **3.10+**
* Google AI Studio **API Key**

### 2. Clone the Repository

```bash
git clone https://github.com/wasxy47/Smart_Career_Advisor.git
cd Smart_Career_Advisor
```

### 3. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file:

```ini
GOOGLE_API_KEY=your_actual_api_key_here

# Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT="Smart Career Advisor"
```

---

## 🎮 Usage Guide

### **Option A — Web App (Recommended)**

```bash
streamlit run app.py
```

**Chat Tab:** Ask job direction questions
**Graph Tab:**

* Full network view
* Focus view for specific roles

### **Option B — Command Line Interface**

```bash
python main.py
```

---

## 🧠 Customizing the Database

Modify the file: `data/career_data.json`

Example structure:

```json
{
  "roles": [
    {
      "id": "new_role_id",
      "title": "New Job Title",
      "salary_range": "$100k - $150k",
      "description": "Short description of the role.",
      "skills": ["Skill 1", "Skill 2"],
      "tools": ["Tool A", "Tool B"],
      "prerequisites": ["previous_role_id"]
    }
  ],
  "skills_relations": [
    {
      "source": "previous_role_id",
      "relation": "prerequisite_of",
      "target": "new_role_id"
    }
  ]
}
```

Restart the app after making changes.

---

## 🛠️ Troubleshooting

### **1. ModuleNotFoundError**

Activate the virtual environment and reinstall dependencies:

```bash
pip install -r requirements.txt
```

### **2. TypeError: Failed to fetch dynamically imported module**

This happens when Streamlit reloads but browser cache is stale.
Hard refresh your browser (`Ctrl+F5` or `Cmd+Shift+R`).

### **3. 404: Model Not Found**

Google retires old model names.
Check your available models:

```bash
python check_models.py
```

Update `LLM_MODEL` in `src/config.py`.

---

## 📜 License

Open-source under the **MIT License**.


