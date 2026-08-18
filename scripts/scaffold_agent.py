#!/usr/bin/env python3
"""Agent Scaffolding Script.

Generates boilerplate for a new agent workflow following Clean Architecture
and layer constraints defined in AGENTS.md and docs/architecture.md.

Generated artifacts:
  - src/state/<name>_state.py
  - src/prompts/<name>_prompt.md
  - src/tools/<name>_tools.py
  - src/graphs/<name>_graph.py
  - tests/unit/test_<name>_graph.py

Usage:
    python scripts/scaffold_agent.py --name researcher
"""

import argparse
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def to_snake_case(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "_", s).strip("_")


def to_pascal_case(name: str) -> str:
    return "".join(word.capitalize() for word in to_snake_case(name).split("_"))


def generate_state(name_snake: str, name_pascal: str) -> str:
    return f'''"""State definition for {name_pascal} agent workflow."""

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class {name_pascal}State(TypedDict):
    """Workflow state schema for {name_pascal}."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: dict[str, str]
    current_step: str
    is_complete: bool
'''


def generate_prompt(name_snake: str, name_pascal: str) -> str:
    return f"""# {name_pascal} Agent System Prompt

You are the **{name_pascal} Agent**, a specialized autonomous sub-system.

## Role & Responsibilities
- Execute domain workflows specific to {name_snake} tasks.
- Use bound tools when additional context or actions are required.
- Maintain structured, verifiable outputs.

## Constraints & Guardrails
- Always validate inputs prior to tool execution.
- If information is missing, request clarification.
- Return final results in a structured format.
"""


def generate_tools(name_snake: str, name_pascal: str) -> str:
    return f'''"""Native tools for {name_pascal} agent workflow."""

from langchain_core.tools import tool


@tool
def {name_snake}_lookup(query: str) -> str:
    """Performs a domain-specific lookup for {name_pascal}.

    Args:
        query: The search query or subject to look up.

    Returns:
        A formatted string with the lookup result.
    """
    # Placeholder implementation: replace with real logic or client calls
    return f"Lookup result for query: {{query}}"
'''


def generate_graph(name_snake: str, name_pascal: str) -> str:
    return f'''"""Compiled LangGraph workflow for {name_pascal} agent."""

from pathlib import Path
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph

from src.state.{name_snake}_state import {name_pascal}State
from src.tools.{name_snake}_tools import {name_snake}_lookup


def _load_system_prompt() -> str:
    """Loads system instructions from prompts directory."""
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "{name_snake}_prompt.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "You are a helpful assistant."


async def {name_snake}_node(state: {name_pascal}State) -> dict:
    """Primary execution node for {name_pascal}."""
    # System prompt is available via _load_system_prompt()
    # Tool execution can be invoked or bound to LLM client
    return {{
        "messages": [AIMessage(content="{name_pascal} step processed successfully.")],
        "current_step": "completed",
        "is_complete": True,
    }}


def build_{name_snake}_graph() -> StateGraph:
    """Constructs and compiles the {name_pascal} LangGraph workflow."""
    workflow = StateGraph({name_pascal}State)

    workflow.add_node("{name_snake}_node", {name_snake}_node)
    workflow.add_edge(START, "{name_snake}_node")
    workflow.add_edge("{name_snake}_node", END)

    return workflow.compile()
'''


def generate_test(name_snake: str, name_pascal: str) -> str:
    return f'''"""Unit tests for {name_pascal} agent workflow."""

import pytest
from langchain_core.messages import HumanMessage
from src.graphs.{name_snake}_graph import build_{name_snake}_graph


@pytest.mark.asyncio
async def test_{name_snake}_graph_execution():
    """Verifies that {name_pascal} graph compiles and processes state."""
    app = build_{name_snake}_graph()

    initial_state = {{
        "messages": [HumanMessage(content="Test trigger")],
        "context": {{}},
        "current_step": "init",
        "is_complete": False,
    }}

    result = await app.ainvoke(initial_state)

    assert result["is_complete"] is True
    assert len(result["messages"]) > 1
'''


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a new agent workflow across state, prompt, tool, graph, and test layers."
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the agent workflow (e.g. 'researcher', 'summarizer')",
    )

    args = parser.parse_args()
    name_snake = to_snake_case(args.name)
    name_pascal = to_pascal_case(args.name)

    if not name_snake:
        print("❌ Error: Invalid agent name.", file=sys.stderr)
        sys.exit(1)

    print(f"\n🛠️  Scaffolding '{name_pascal}' Agent ({name_snake})...\n")

    files_to_create = [
        (
            ROOT_DIR / "src" / "state" / f"{name_snake}_state.py",
            generate_state(name_snake, name_pascal),
        ),
        (
            ROOT_DIR / "src" / "prompts" / f"{name_snake}_prompt.md",
            generate_prompt(name_snake, name_pascal),
        ),
        (
            ROOT_DIR / "src" / "tools" / f"{name_snake}_tools.py",
            generate_tools(name_snake, name_pascal),
        ),
        (
            ROOT_DIR / "src" / "graphs" / f"{name_snake}_graph.py",
            generate_graph(name_snake, name_pascal),
        ),
        (
            ROOT_DIR / "tests" / "unit" / f"test_{name_snake}_graph.py",
            generate_test(name_snake, name_pascal),
        ),
    ]

    for path, content in files_to_create:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            print(f"  ⚠️  Skipped (already exists): {path.relative_to(ROOT_DIR)}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"  ✓ Created {path.relative_to(ROOT_DIR)}")

    print(f"\n✨ Successfully scaffolded {name_pascal} agent!")
    print(f"Run tests with: uv run pytest tests/unit/test_{name_snake}_graph.py\n")


if __name__ == "__main__":
    main()
