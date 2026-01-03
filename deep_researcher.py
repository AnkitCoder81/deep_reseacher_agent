import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")

import asyncio
from dotenv import load_dotenv
from typing import Annotated, TypedDict

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# =========================
# Config
# =========================
MAX_ITERATIONS = 3
load_dotenv()

# =========================
# State
# =========================
class ResearchTask(TypedDict):
    messages: Annotated[list, add_messages]
    iteration_count: int

# =========================
# LLM + Tools
# =========================
tools = [TavilySearch(k=5)]

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)

# =========================
# Nodes
# =========================
async def researcher_node(state: ResearchTask) -> ResearchTask:
    messages = state["messages"]
    iteration_count = state.get("iteration_count", 0)

    if iteration_count >= MAX_ITERATIONS:
        return state

    prompt = SystemMessage(
        content=(
            "You are a Deep Researcher. Use tools to find detailed technical data. "
            "When necessary, call tools. Produce structured research notes with sources."
        )
    )

    response = await llm_with_tools.ainvoke([prompt] + messages)

    return {
        "messages": messages + [response],
        "iteration_count": iteration_count + 1
    }

async def writer_node(state: ResearchTask) -> ResearchTask:
    messages = state["messages"]

    prompt = SystemMessage(
        content=(
            "You are a Best Technical Writer. Convert the research notes into a "
            "clear, well-structured technical article with headings, examples, and takeaways."
        )
    )

    response = await llm.ainvoke([prompt] + messages)

    return {
        "messages": messages + [response],
        "iteration_count": state.get("iteration_count", 0)
    }

# =========================
# Graph Builder
# =========================
def build_graph():
    graph = StateGraph(ResearchTask)

    graph.add_node("researcher", researcher_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("writer", writer_node)

    graph.add_edge(START, "researcher")
    graph.add_conditional_edges("researcher", tools_condition)
    graph.add_edge("tools", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()

# =========================
# Async Runner
# =========================
async def _run_async(query: str) -> str:
    app = build_graph()

    inputs = {
        "messages": [HumanMessage(content=query)],
        "iteration_count": 0
    }

    final_state = None
    async for output in app.astream(inputs):
        final_state = output

    for key in ("writer", "researcher"):
        msgs = final_state.get(key, {}).get("messages", [])
        if msgs:
            return msgs[-1].content

    return "No output generated."

# =========================
# Public Sync API (for Streamlit)
# =========================
def run_deep_research(query: str) -> str:
    """
    Safe synchronous wrapper for Streamlit / FastAPI / CLI
    """
    try:
        return asyncio.run(_run_async(query))
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_run_async(query))

# =========================
# Standalone Execution
# =========================
if __name__ == "__main__":
    result = run_deep_research(
        "Analyze how the Model Context Protocol (MCP) improves modularity in AI agents."
    )
    print("\n===== FINAL OUTPUT =====\n")
    print(result)
