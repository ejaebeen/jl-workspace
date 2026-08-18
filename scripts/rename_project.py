#!/usr/bin/env python3
"""Project Renaming Script.

Customizes template placeholders (project name, description, author)
across pyproject.toml, settings, Makefile, and documentation.

Usage:
    python scripts/rename_project.py --name "my-awesome-agent" --description "Production agent workflow"
"""

import argparse
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def sanitize_name(name: str) -> str:
    """Sanitizes project name to kebab-case valid package identifier."""
    name = re.sub(r"[^\w\-_]", "-", name.lower())
    return re.sub(r"-+", "-", name).strip("-_")


def update_pyproject_toml(project_name: str, description: str) -> None:
    path = ROOT_DIR / "pyproject.toml"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    content = re.sub(r'name = "[^"]+"', f'name = "{project_name}"', content, count=1)
    if description:
        content = re.sub(
            r'description = "[^"]+"', f'description = "{description}"', content, count=1
        )
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Updated {path.relative_to(ROOT_DIR)}")


def update_settings(project_name: str) -> None:
    path = ROOT_DIR / "src" / "config" / "settings.py"
    if not path.exists():
        return
    human_title = project_name.replace("-", " ").replace("_", " ").title()
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        r'app_name:\s*str\s*=\s*"[^"]+"',
        f'app_name: str = "{human_title}"',
        content,
    )
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Updated {path.relative_to(ROOT_DIR)}")


def update_makefile(project_name: str) -> None:
    path = ROOT_DIR / "Makefile"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        r"jl-workspace",
        project_name,
        content,
    )
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Updated {path.relative_to(ROOT_DIR)}")


def update_readme(project_name: str, description: str) -> None:
    path = ROOT_DIR / "README.md"
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    human_title = project_name.replace("-", " ").replace("_", " ").title()
    content = re.sub(
        r"# [^\n]+",
        f"# {human_title}",
        content,
        count=1,
    )
    if description:
        # replace first paragraph after heading
        content = re.sub(
            r"\n\nA production-ready[^\n]+",
            f"\n\n{description}",
            content,
            count=1,
        )
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ Updated {path.relative_to(ROOT_DIR)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rename project template and update metadata."
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="New project name (e.g., 'customer-support-agent')",
    )
    parser.add_argument(
        "--description",
        type=str,
        default="",
        help="Short project description",
    )

    args = parser.parse_args()
    project_name = sanitize_name(args.name)

    if not project_name:
        print("❌ Error: Invalid project name.", file=sys.stderr)
        sys.exit(1)

    print(f"\n🔄 Renaming project template to '{project_name}'...")
    update_pyproject_toml(project_name, args.description)
    update_settings(project_name)
    update_makefile(project_name)
    update_readme(project_name, args.description)

    print(f"\n✅ Project successfully renamed to '{project_name}'!\n")


if __name__ == "__main__":
    main()
