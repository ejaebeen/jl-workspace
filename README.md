# AI Agent & GenAI Project Template

A production-ready, modular template for building scalable Generative AI applications, LangGraph agentic workflows, Model Context Protocol (MCP) integrations, and LLM-powered microservices.

---

## 🌟 Key Features

- **🏛️ Clean Architecture**: Strict separation of concerns (Domain, Services, Graphs, Schemas, API) with zero-dependency domain entities.
- **🧠 LangGraph Workflows**: Declarative state machines, cyclic multi-agent graphs, typed channels, and memory checkpointing.
- **🔌 Model Context Protocol (MCP)**: First-class support for MCP servers and client protocol handling.
- **⚡ FastAPI & Async-First**: High-throughput asynchronous REST endpoints with Pydantic v2 validation.
- **🔍 Observability & Telemetry**: Built-in OpenTelemetry distributed tracing and MLflow experiment tracking.
- **🛠️ Developer Automation & Scaffolding**: 1-command project initialization, template renaming, and agent scaffolding scripts.
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
├── scripts/
│   ├── init.sh          # 1-command bootstrap (dependencies, .env, git hooks)
│   ├── rename_project.py# Renames template placeholders to your project name
│   ├── scaffold_agent.py# Generates complete agent workflow boilerplate
│   └── test_mcp.py      # Verifies local MCP server and environment
├── tests/
│   ├── unit/            # Isolated unit tests
│   ├── integration/     # Service and workflow integration tests
│   └── e2e/             # End-to-end API and system tests
├── docs/
│   ├── architecture.md  # Detailed architecture rules and layer constraints
│   └── decisions/       # Architectural Decision Records (ADRs)
├── .env.example         # Template for environment variables and API keys
├── Dockerfile.api       # Container definition for FastAPI application
├── Dockerfile.mcp       # Container definition for MCP server
├── Makefile             # Development, testing, and lifecycle commands
├── AGENTS.md            # Operational rules and checklist for AI coding agents
└── pyproject.toml       # Project configuration and dependency definitions
```

---

## 🚀 Quickstart

### 1. Prerequisites

- Python 3.12+
- Package manager: [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

### 2. 1-Command Initialization

Run the automated initialization script (checks Python/uv, creates `.env`, installs all dependencies, and sets up git hooks):

```bash
make init
# or directly:
./scripts/init.sh
```

### 3. Customize Project Name (Optional)

If you are using this repository as a template for a new project, rename the package, metadata, and container configurations with:

```bash
make rename NAME="my-agent-service"
# or
python scripts/rename_project.py --name "my-agent-service" --description "Production agent service"
```

### 4. Configure Environment Variables

Edit the generated `.env` file to configure your LLM provider keys and tracking endpoints:

```env
# Application Settings
APP_NAME="AI Project Template"
APP_ENV="development"
DEBUG=true
API_PREFIX="/api/v1"

# LLM Providers
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="AIza..."
OLLAMA_BASE_URL="http://localhost:11434"

# Observability
MLFLOW_TRACKING_URI="http://localhost:5000"
OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
```

### 5. Run the Application

Start the local FastAPI development server with hot reload:

```bash
make dev
```

The API and documentation will be available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Scaffolding New Agent Workflows

Use the built-in scaffolding script to generate architectural boilerplate for new LangGraph agents:

```bash
make scaffold-agent NAME=researcher
# or
python scripts/scaffold_agent.py --name researcher
```

This automatically generates files adhering to strict Clean Architecture rules:
1. `src/state/researcher_state.py` — TypedDict state definition with message reducers.
2. `src/prompts/researcher_prompt.md` — Isolated Markdown system instructions.
3. `src/tools/researcher_tools.py` — Native Python tool functions with `@tool`.
4. `src/graphs/researcher_graph.py` — StateGraph workflow definition and compilation.
5. `tests/unit/test_researcher_graph.py` — Unit test suite verifying workflow execution.

---

## 📋 Makefile Commands Reference

| Category | Command | Description |
| :--- | :--- | :--- |
| **Setup** | `make help` | Show all available targets and descriptions |
| | `make init` | 1-command bootstrap (dependencies, `.env`, git hooks) |
| | `make install` | Sync base dependencies with `uv` |
| | `make install-all` | Sync all dependency groups (`dev`, `api`, `mcp`, `observability`) |
| | `make lock` | Update `uv.lock` |
| **Scaffolding** | `make rename NAME=<name>` | Rename template metadata across the repository |
| | `make scaffold-agent NAME=<name>` | Scaffold a complete new LangGraph agent workflow |
| **Development** | `make dev` | Run FastAPI development server with auto-reload |
| | `make run-prod` | Run FastAPI server in production mode with workers |
| | `make run-mcp` | Run MCP server module |
| | `make test-mcp` | Verify MCP server environment and tools |
| **Testing** | `make test` | Run complete pytest test suite |
| | `make test-unit` | Run unit tests only (`tests/unit`) |
| | `make test-integration` | Run integration tests only (`tests/integration`) |
| | `make test-e2e` | Run end-to-end tests only (`tests/e2e`) |
| | `make test-cov` | Run tests with terminal & HTML coverage report |
| **Code Quality** | `make lint` | Run ruff linter |
| | `make lint-fix` | Auto-fix linting errors with ruff |
| | `make format` | Format code with ruff |
| | `make format-check` | Check code formatting without applying edits |
| | `make typecheck` | Run static type checking with mypy |
| | `make check` | Run `lint`, `format-check`, and `typecheck` |
| | `make fix` | Run `format` and `lint-fix` |
| **Docker** | `make docker-build-api` | Build FastAPI Docker image |
| | `make docker-build-mcp` | Build MCP server Docker image |
| | `make docker-build` | Build all Docker containers |
| **Cleanup** | `make clean` | Remove cache directories, `.pytest_cache`, and build artifacts |
| | `make clean-all` | Deep clean including `.venv` virtual environment |

---

## 🏗️ Architecture & Extension Guide

For in-depth architectural patterns, layer boundaries, and request flow lifecycles, refer to [docs/architecture.md](file:///Users/ejaebeen/Documents/github/jl-workspace/docs/architecture.md).

### Layer Guidelines Summary:
- **`src/domain/`**: Pure Python entities and business rules (zero external dependencies).
- **`src/prompts/`**: Multi-line system prompts stored exclusively in Markdown / Jinja files.
- **`src/graphs/` & `src/state/`**: LangGraph workflows and TypedDict schemas.
- **`src/api/`**: Thin FastAPI routers for HTTP validation and status dispatch.
- **`src/mcp/`**: Model Context Protocol handlers for AI tooling integration.
- **`src/services/`**: Orchestration between domain models, graph workflows, and clients.
- **`src/config/`**: Centralized Pydantic settings (`get_settings()`).

---

## 🤖 Working with AI Agents

When using AI coding assistants (such as Antigravity, Cursor, Copilot, or Claude) in this repository, reference [`AGENTS.md`](file:///Users/ejaebeen/Documents/github/jl-workspace/AGENTS.md). It outlines strict coding rules, layer constraints, and verification workflows.

---

## 📄 License

MIT License. See `LICENSE` for details.
