.DEFAULT_GOAL := help

# ==============================================================================
# Configuration & Variables
# ==============================================================================
PYTHON      ?= python3
UV          ?= uv
HOST        ?= 0.0.0.0
PORT        ?= 8000
WORKERS     ?= 4
APP_MODULE  ?= src.api.app:create_app
MCP_MODULE  ?= src.mcp.server

# Colors for terminal output
COLOR_RESET   = \033[0m
COLOR_CYAN    = \033[36m
COLOR_GREEN   = \033[32m
COLOR_YELLOW  = \033[33m
COLOR_BLUE    = \033[34m
COLOR_BOLD    = \033[1m

# ==============================================================================
# Help Target
# ==============================================================================
.PHONY: help
help: ## Show this help message with available commands
	@echo ""
	@echo "$(COLOR_BOLD)jl-workspace Makefile$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)Usage:$(COLOR_RESET)"
	@echo "  make $(COLOR_CYAN)<target>$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)Available targets:$(COLOR_RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "  $(COLOR_CYAN)%-22s$(COLOR_RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

# ==============================================================================
# Dependencies & Environment
# ==============================================================================
.PHONY: install
install: ## Install base project dependencies
	@echo "$(COLOR_GREEN)Installing dependencies with uv...$(COLOR_RESET)"
	$(UV) sync

.PHONY: install-all
install-all: ## Install all dependency groups (dev, api, mcp, observability)
	@echo "$(COLOR_GREEN)Installing all dependency groups with uv...$(COLOR_RESET)"
	$(UV) sync --all-groups

.PHONY: install-dev
install-dev: ## Install development dependency group
	@echo "$(COLOR_GREEN)Installing dev dependencies...$(COLOR_RESET)"
	$(UV) sync --group dev

.PHONY: lock
lock: ## Update dependency lockfile (uv.lock)
	@echo "$(COLOR_GREEN)Locking dependencies...$(COLOR_RESET)"
	$(UV) lock

# ==============================================================================
# Application & Development Servers
# ==============================================================================
.PHONY: dev
dev: ## Run FastAPI development server with hot-reloading
	@echo "$(COLOR_GREEN)Starting FastAPI development server on http://$(HOST):$(PORT)...$(COLOR_RESET)"
	$(UV) run uvicorn $(APP_MODULE) --factory --reload --host $(HOST) --port $(PORT)

.PHONY: run-prod
run-prod: ## Run FastAPI application in production mode
	@echo "$(COLOR_GREEN)Starting production server on http://$(HOST):$(PORT)...$(COLOR_RESET)"
	$(UV) run uvicorn $(APP_MODULE) --factory --host $(HOST) --port $(PORT) --workers $(WORKERS)

.PHONY: run-mcp
run-mcp: ## Run MCP server module
	@echo "$(COLOR_GREEN)Starting MCP server...$(COLOR_RESET)"
	$(UV) run python -m $(MCP_MODULE)

# ==============================================================================
# Testing
# ==============================================================================
.PHONY: test
test: ## Run test suite with pytest
	@echo "$(COLOR_GREEN)Running pytest test suite...$(COLOR_RESET)"
	$(UV) run pytest

.PHONY: test-unit
test-unit: ## Run unit tests
	@echo "$(COLOR_GREEN)Running unit tests...$(COLOR_RESET)"
	$(UV) run pytest tests/unit

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "$(COLOR_GREEN)Running integration tests...$(COLOR_RESET)"
	$(UV) run pytest tests/integration

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	@echo "$(COLOR_GREEN)Running e2e tests...$(COLOR_RESET)"
	$(UV) run pytest tests/e2e

.PHONY: test-cov
test-cov: ## Run tests with code coverage report
	@echo "$(COLOR_GREEN)Running pytest with code coverage...$(COLOR_RESET)"
	$(UV) run pytest --cov=src --cov-report=term-missing --cov-report=html

# ==============================================================================
# Code Quality, Linting & Formatting
# ==============================================================================
.PHONY: lint
lint: ## Run ruff linter checks
	@echo "$(COLOR_GREEN)Running ruff check...$(COLOR_RESET)"
	$(UV) run ruff check .

.PHONY: lint-fix
lint-fix: ## Auto-fix linting issues with ruff
	@echo "$(COLOR_GREEN)Auto-fixing lint issues with ruff...$(COLOR_RESET)"
	$(UV) run ruff check . --fix

.PHONY: format
format: ## Format source code with ruff
	@echo "$(COLOR_GREEN)Formatting code with ruff...$(COLOR_RESET)"
	$(UV) run ruff format .

.PHONY: format-check
format-check: ## Check code formatting without modifying files
	@echo "$(COLOR_GREEN)Checking code format with ruff...$(COLOR_RESET)"
	$(UV) run ruff format --check .

.PHONY: typecheck
typecheck: ## Run static type checking with mypy
	@echo "$(COLOR_GREEN)Running static type checking with mypy...$(COLOR_RESET)"
	$(UV) run mypy src

.PHONY: check
check: lint format-check typecheck ## Run all code quality checks (lint, format-check, typecheck)
	@echo "$(COLOR_GREEN)All quality checks passed!$(COLOR_RESET)"

.PHONY: fix
fix: format lint-fix ## Auto-format and fix all fixable lint issues
	@echo "$(COLOR_GREEN)All formatting and lint fixes applied!$(COLOR_RESET)"

# ==============================================================================
# Docker
# ==============================================================================
.PHONY: docker-build-api
docker-build-api: ## Build Docker container for the API service
	@echo "$(COLOR_GREEN)Building Docker image for API (jl-workspace-api:latest)...$(COLOR_RESET)"
	docker build -f Dockerfile.api -t jl-workspace-api:latest .

.PHONY: docker-build-mcp
docker-build-mcp: ## Build Docker container for the MCP service
	@echo "$(COLOR_GREEN)Building Docker image for MCP (jl-workspace-mcp:latest)...$(COLOR_RESET)"
	docker build -f Dockerfile.mcp -t jl-workspace-mcp:latest .

.PHONY: docker-build
docker-build: docker-build-api docker-build-mcp ## Build all Docker containers

# ==============================================================================
# Cleanup
# ==============================================================================
.PHONY: clean
clean: ## Remove temporary cache files, build artifacts, and test outputs
	@echo "$(COLOR_YELLOW)Cleaning build and cache artifacts...$(COLOR_RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ dist/ build/
	@echo "$(COLOR_GREEN)Cleanup complete.$(COLOR_RESET)"

.PHONY: clean-all
clean-all: clean ## Deep clean including virtual environment (.venv)
	@echo "$(COLOR_YELLOW)Removing virtual environment (.venv)...$(COLOR_RESET)"
	rm -rf .venv
	@echo "$(COLOR_GREEN)Deep cleanup complete.$(COLOR_RESET)"
