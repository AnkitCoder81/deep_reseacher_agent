# app.py
import streamlit as st
from deep_researcher import run_deep_research

st.set_page_config(
    page_title="MCP Deep Research Agent",
    layout="wide"
)

st.title("🧠 MCP Deep Research Agent")
st.caption("LangGraph · Tool Calling · Modular AI Agents")

query = st.text_area(
    "Enter your research topic",
    height=180,
    placeholder=(
        "Conduct a deep technical investigation into how the Model Context Protocol "
        "(MCP) influences modularity in AI agents..."
    )
)

if st.button("🚀 Run Research"):
    if not query.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Running deep research..."):
            output = run_deep_research(query)

        st.success("Research Complete")
        st.markdown("---")
        st.markdown(output)
