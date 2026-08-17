# AI Agent & GenAI Project Template

A production-ready, modular template for building scalable Generative AI applications, LangGraph agentic workflows, Model Context Protocol (MCP) integrations, and LLM-powered microservices.

---

## 🌟 Key Features

- **🏛️ Clean Architecture**: Strict separation of concerns (Domain, Services, Graphs, Schemas, API) with zero-dependency domain entities.
- **🧠 LangGraph Workflows**: Declarative state machines, cyclic multi-agent graphs, typed channels, and memory checkpointing.
- **🔌 Model Context Protocol (MCP)**: First-class support for MCP servers and client protocol handling.
- **⚡ FastAPI & Async-First**: High-throughput asynchronous REST endpoints with Pydantic v2 validation.
- **🔍 Observability & Telemetry**: Built-in OpenTelemetry distributed tracing and MLflow experiment tracking.
- **🤖 AI Agent-Native**: Pre-configured with [`AGENTS.md`](file:///Users/ejaebeen/Documents/github/jl-workspace/AGENTS.md) and [`docs/architecture.md`](file:///Users/ejaebeen/Documents/github/jl-workspace/docs/architecture.md) for seamless pair-programming with AI coding assistants (Antigravity, Cursor, Copilot, Claude).

---

## 📁 Repository Structure

```
.
├── src/
│   ├── api/             # FastAPI routers, endpoints, and HTTP middleware
│   ├── mcp/             # MCP server/client implementations & protocol handling
│   ├── graphs/          # LangGraph nodes, edges, and compiled workflows
│   ├── tools/           # Native Python tools bound to LLMs
│   ├── prompts/         # Standardised .md files, Jinja templates, system instructions
│   ├── state/           # LangGraph State definitions and checkpointing logic
│   ├── services/        # Logic orchestrating domain rules, clients, and graphs
│   ├── domain/          # Core business entities and rules (zero external dependencies)
│   ├── schemas/         # Pydantic models for API requests/responses and validation
│   ├── clients/         # External integrations (HTTP clients, DB connectors, LLMs)
│   ├── observability/   # MLflow tracking and OpenTelemetry trace/span configurations
│   └── config/          # Pydantic-settings, env var loading, and global constants
├── docs/
│   └── architecture.md  # Detailed architecture rules and layer constraints
├── AGENTS.md            # Operational rules and checklist for AI coding agents
└── pyproject.toml       # Project configuration and dependency definitions
```

---

## 🚀 Quickstart

### 1. Prerequisites

- Python 3.12+
- Package manager: `uv`, `pip`, or `poetry`

### 2. Installation

Clone the repository and install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e ".[dev]"
```

### 3. Configure Environment

Create your `.env` configuration file:

```bash
cp .env.example .env  # If available, or create a .env file
```

Example environment variables:

```env
APP_NAME="AI Project Template"
APP_ENV="development"
DEBUG=true
API_PREFIX="/api/v1"
```

### 4. Run the Application

Start the local FastAPI development server:

```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Development & Quality Assurance

Run the test suite, linter, and type checker with the following commands:

| Action | Command |
| :--- | :--- |
| **Run Tests** | `pytest` |
| **Lint & Format Check** | `ruff check .` |
| **Auto-fix Lint Issues** | `ruff check . --fix` |
| **Format Code** | `ruff format .` |
| **Type Check** | `mypy src` |

---

## 🏗️ Architecture & Extension Guide

For in-depth architectural patterns, dependency boundaries, and request flow lifecycles, refer to [docs/architecture.md](file:///Users/ejaebeen/Documents/github/jl-workspace/docs/architecture.md).

### How to Build New Features:

1. **New Agent Workflow**:
   - Define state schema in `src/state/`.
   - Store system prompts in `src/prompts/`.
   - Implement functions/tools in `src/tools/`.
   - Compose graph in `src/graphs/`.
   - Orchestrate in `src/services/`.

2. **New API Route**:
   - Define Pydantic request/response in `src/schemas/`.
   - Implement logic in `src/services/`.
   - Expose endpoint in `src/api/routes.py`.

3. **New Tool**:
   - Implement with `@tool` in `src/tools/`.
   - Bind to graphs or register with `src/mcp/`.

---

## 🤖 Working with AI Agents

When utilizing AI assistants (such as Antigravity, Cursor, Copilot, or Claude) to develop within this repository, reference [`AGENTS.md`](file:///Users/ejaebeen/Documents/github/jl-workspace/AGENTS.md). It enforces layer boundaries, dependency rules, and standard coding conventions automatically.

---

## 📄 License

MIT License. See `LICENSE` for details.
