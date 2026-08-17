"""Tool definitions for LLM function calling."""

from langchain_core.tools import tool


@tool
def example_tool(query: str) -> str:
    """An example tool that can be bound to LLMs."""
    return f"Processed query: {query}"
