FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Install uv using Astral's official installer into /usr/local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Switch to the default non-root user provided by Microsoft's image
USER vscode
