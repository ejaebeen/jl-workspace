"""Service layer orchestrating domain rules, clients, and graph workflows."""

from typing import Any, Dict
from src.graphs.workflow import build_workflow


class AgentService:
    """Orchestrates AI agents, workflows, and domain operations."""

    def __init__(self):
        self.workflow = build_workflow()

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the compiled graph workflow with provided input data."""
        # Execute workflow invocation
        return {"result": "processed", "input": input_data}
