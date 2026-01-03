# 🔍 Deep Research Agent (Streamlit + LangGraph)

An AI-powered **deep research application** built using **LangGraph**, **LangChain**, **Groq LLM**, and **Tavily Search**, with a **Streamlit UI** for interactive research queries.

This app performs **iterative web research**, summarizes findings, and provides structured answers to complex questions.

---

## 🚀 Features

- 🔁 Iterative research using LangGraph
- 🌐 Web search via Tavily API
- 🧠 LLM powered by Groq (LLaMA models)
- 🖥️ Clean Streamlit UI
- 📄 Well-structured research responses
- ⚙️ Environment-based configuration

---

## 📂 Project Structure

deep-research/
│
├── app.py
│   Streamlit application entry point (UI for research queries)
│
├── deep_researcher.py
│   Core research engine built with LangGraph and LangChain
│
├── main.py
│   Local testing / CLI execution script (optional)
│
├── requirements.txt
│   Python dependencies required to run the project
│
├── pyproject.toml
│   Project metadata and tool configuration
│
├── uv.lock
│   Dependency lock file for reproducible installs
│
├── .gitignore
│   Files and folders excluded from GitHub
│
└── README.md
    Project documentation
Environment variables are loaded using python-dotenv.

Required variables:
- GROQ_API_KEY   → Used for Groq LLM access
- TAVILY_API_KEY → Used for web search queries

Create a `.env` file in the project root and add:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
