#!/usr/bin/env python3
"""MCP Server & Tool Verification Script.

Tests the MCP server module and lists registered tools.

Usage:
    python scripts/test_mcp.py
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


def main() -> None:
    print("\n🔍 Checking MCP Server setup...")
    try:
        import mcp

        print(
            f"  ✓ MCP SDK imported successfully (version: {mcp.__version__ if hasattr(mcp, '__version__') else 'installed'})"
        )
    except ImportError:
        print(
            "  ❌ 'mcp' package is not installed. Run 'uv sync --group mcp' to install."
        )
        sys.exit(1)

    try:
        from src.mcp import server

        print(f"  ✓ Found MCP server module ({server.__file__})")
        print("\n✨ MCP environment is ready.")
    except Exception as exc:  # noqa: BLE001
        print(f"  ❌ Error loading MCP server module: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
