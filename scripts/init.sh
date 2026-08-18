#!/usr/bin/env bash
# ==============================================================================
# AI Project Initialization Script
# ==============================================================================
set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[32m"
CYAN="\033[36m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"

echo -e "\n${BOLD}${CYAN}===============================================${RESET}"
echo -e "${BOLD}${CYAN}   🚀 Initializing AI Project Workspace        ${RESET}"
echo -e "${BOLD}${CYAN}===============================================${RESET}\n"

# 1. Check Python version
echo -e "${CYAN}🔍 Checking Python installation...${RESET}"
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo -e "   Found Python ${GREEN}${PYTHON_VERSION}${RESET}"
else
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.12 or newer.${RESET}"
    exit 1
fi

# 2. Check / Install uv
echo -e "\n${CYAN}🔍 Checking uv package manager...${RESET}"
if ! command -v uv >/dev/null 2>&1; then
    echo -e "   ${YELLOW}uv not found. Installing uv...${RESET}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

if command -v uv >/dev/null 2>&1; then
    UV_VERSION=$(uv --version)
    echo -e "   Using ${GREEN}${UV_VERSION}${RESET}"
else
    echo -e "${RED}❌ Failed to locate uv after installation attempt.${RESET}"
    exit 1
fi

# 3. Setup environment configuration (.env)
echo -e "\n${CYAN}⚙️  Configuring environment variables...${RESET}"
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "   ${GREEN}Created .env from .env.example${RESET}"
    else
        touch .env
        echo -e "   ${YELLOW}Created empty .env file${RESET}"
    fi
else
    echo -e "   ${YELLOW}.env already exists. Skipping copy.${RESET}"
fi

# 4. Install dependencies using uv sync
echo -e "\n${CYAN}📦 Installing project dependencies (all groups)...${RESET}"
uv sync --all-groups
echo -e "   ${GREEN}Dependencies installed successfully.${RESET}"

# 5. Optional git hooks setup
if [ -d .git ]; then
    echo -e "\n${CYAN}⚓ Setting up Git pre-commit hooks...${RESET}"
    mkdir -p .git/hooks
    cat << 'HOOK' > .git/hooks/pre-commit
#!/usr/bin/env bash
# Run ruff format and lint check before commit
if command -v uv >/dev/null 2>&1; then
    echo "Running pre-commit ruff checks..."
    uv run ruff check .
    uv run ruff format --check .
fi
HOOK
    chmod +x .git/hooks/pre-commit
    echo -e "   ${GREEN}Pre-commit hook installed (.git/hooks/pre-commit).${RESET}"
fi

echo -e "\n${BOLD}${GREEN}===============================================${RESET}"
echo -e "${BOLD}${GREEN}   ✨ Project Initialized Successfully!        ${RESET}"
echo -e "${BOLD}${GREEN}===============================================${RESET}\n"

echo -e "${BOLD}Next steps:${RESET}"
echo -e "  1. Edit ${CYAN}.env${RESET} to configure your API keys (OpenAI, Anthropic, Ollama, etc.)"
echo -e "  2. Start the FastAPI development server: ${CYAN}make dev${RESET}"
echo -e "  3. Run the test suite:                  ${CYAN}make test${RESET}"
echo -e "  4. Scaffold a new agent workflow:       ${CYAN}python scripts/scaffold_agent.py --name <agent_name>${RESET}"
echo -e "  5. Rename project template:             ${CYAN}python scripts/rename_project.py --name <new_name>${RESET}\n"
