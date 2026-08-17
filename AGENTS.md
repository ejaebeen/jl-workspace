# AI Agent Playbook & Repository Guidelines (`AGENTS.md`)

Welcome to the project! This document serves as the operational guide and rulebook for AI coding assistants (e.g., Antigravity, Cursor, Copilot, Claude) working in this repository.

---

## 1. Project Overview

This repository is a production-ready template for building scalable, observable, and modular AI agent systems.

- **Frameworks & Core Tech**: Python 3.12+, FastAPI, LangGraph, LangChain Core, Model Context Protocol (MCP), Pydantic v2.
- **Observability**: OpenTelemetry, MLflow.
- **Architecture Style**: Clean Architecture / Ports & Adapters with strict inward dependency rules.
- **Detailed Reference**: See [docs/architecture.md](file:///Users/ejaebeen/Documents/github/jl-workspace/docs/architecture.md).

---

## 2. Directory Architecture & Layer Rules

```
src/
├── api/             # FastAPI routers, endpoints, and HTTP middleware
├── mcp/             # MCP server/client implementations & protocol handling
├── graphs/          # LangGraph nodes, edges, and compiled workflows
├── tools/           # Native Python tools bound to LLMs
├── prompts/         # Standardised .md files, Jinja templates, system instructions
├── state/           # LangGraph State definitions and checkpointing logic
├── services/        # Logic that orchestrates domain rules, clients, and graphs
├── domain/          # Core business entities and rules (zero external dependencies)
├── schemas/         # Pydantic models for API requests/responses and validation
├── clients/         # External integrations (HTTP clients, DB connectors, LLMs)
├── observability/   # MLflow tracking and OpenTelemetry trace/span configurations
└── config/          # Pydantic-settings, env var loading, and global constants
```

### Strict Layer Constraints for AI Agents

1. **`src/domain/` is pure Python**:
   - ZERO external framework dependencies. No FastAPI, no LangChain, no Pydantic. Use standard dataclasses or pure Python classes.
2. **`src/api/` contains NO business logic**:
   - Routes only validate requests via `src/schemas/`, call `src/services/`, and return response schemas.
3. **`src/graphs/` contains workflow definitions**:
   - All state must be typed using schemas from `src/state/`.
   - Node functions must not directly import API routes or external infrastructure.
4. **`src/prompts/` isolates all prompt text**:
   - Do not hardcode multi-line prompt strings inside graph nodes or service files.
5. **`src/config/` is the single source for settings**:
   - Use `get_settings()` from `src/config/settings.py`. Never call `os.getenv` directly in feature files.

---

## 3. Development Commands

| Action | Command |
| :--- | :--- |
| **Run Dev Server** | `python main.py` or `uvicorn main:app --reload` |
| **Run Tests** | `pytest` |
| **Lint Check** | `ruff check .` |
| **Format Code** | `ruff format .` |
| **Type Check** | `mypy src` |

---

## 4. Coding Standards & Conventions

- **Type Annotations**: All functions, methods, and schemas must include explicit type hints (`typing.Optional`, `typing.Sequence`, `typing.Annotated`, etc.).
- **Async by Default**: I/O operations (API routes, services, external client calls, MCP handlers) must be asynchronous (`async def`).
- **Error Handling**: Use custom domain exceptions in `src/domain/` or `src/services/`, and translate them to HTTP status codes in `src/api/`.
- **Telemetry**: Add OpenTelemetry spans and structured logging via `src/observability/setup.py` on key workflows and external LLM calls.

---

## 5. Agent Task Execution Checklist

When implementing new features or resolving issues, adhere to the following workflow:

### Adding a New API Endpoint
1. Define request and response schemas in `src/schemas/`.
2. Implement business logic / orchestration in `src/services/`.
3. Expose route in `src/api/routes.py` (or a dedicated submodule).
4. Write unit and integration tests under `tests/`.

### Adding a New Agent Workflow / Graph
1. Define the workflow state schema in `src/state/agent_state.py`.
2. Add system instructions or prompt templates in `src/prompts/`.
3. Create necessary tools in `src/tools/`.
4. Compose nodes, conditional edges, and compile the graph in `src/graphs/`.
5. Expose graph execution through `src/services/agent_service.py`.

### Adding an LLM Tool
1. Define tool input models if complex arguments are required.
2. Implement the tool using the `@tool` decorator in `src/tools/`.
3. Ensure comprehensive docstrings with argument descriptions for LLM function calling.
4. Bind tool to graph workflows (`src/graphs/`) or expose via MCP (`src/mcp/`).
