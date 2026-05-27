#!/usr/bin/env python3
"""Probe a repository for Understand-Anything readiness and emit Codex agent context."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


DEFAULT_EXCLUDES = [
    ".git",
    ".understand-anything",
    ".codegraph",
    ".idea",
    ".vscode",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    "logs",
    "log",
    "tmp",
    "cache",
    ".specstory",
    "datalog",
]

PRIORITY_DIRS = [
    "application/controllers",
    "application/models",
    "application/views",
    "application/helpers",
    "application/libraries",
    "application/queue",
    "src",
    "app",
    "lib",
    "theme",
    "scripts",
    "sql",
    "tests",
    "docs",
]


def existing_dirs(root: Path, dirs: list[str]) -> list[str]:
    return [rel for rel in dirs if (root / rel).exists()]


def graph_summary(graph_path: Path) -> str:
    if not graph_path.exists():
        return "missing"
    try:
        data = json.loads(graph_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return "present, unreadable JSON: {0}".format(exc)
    if isinstance(data, dict):
        keys = ", ".join(sorted(data.keys())[:8])
        return "present, top-level keys: {0}".format(keys or "none")
    return "present, JSON type: {0}".format(type(data).__name__)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Understand-Anything readiness for a repository and print an agent handoff."
    )
    parser.add_argument("--root", default=os.getcwd(), help="Project root to inspect.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    ua_dir = root / ".understand-anything"
    graph_path = ua_dir / "knowledge-graph.json"
    excludes = existing_dirs(root, DEFAULT_EXCLUDES)
    priority = existing_dirs(root, PRIORITY_DIRS)
    candidates = [
        shutil.which("understand-anything"),
        shutil.which("ua"),
        shutil.which("npx"),
    ]
    commands = [c for c in candidates if c]

    print("# Understand-Anything Project Probe")
    print()
    print("- Project root: `{0}`".format(root))
    print("- Candidate commands: {0}".format(", ".join(commands) if commands else "none found"))
    print("- Local graph directory: `{0}`".format("present" if ua_dir.exists() else "missing"))
    print("- Knowledge graph: `{0}`".format(graph_summary(graph_path)))
    print("- Suggested excludes present: {0}".format(", ".join(excludes) if excludes else "none detected"))
    print("- Priority source areas present: {0}".format(", ".join(priority) if priority else "none detected"))

    print()
    print("## Next Commands")
    print()
    if not ua_dir.exists() or not graph_path.exists():
        print("- Read `references/understand-anything-setup.md`, then initialize the graph from the official workflow.")
        print("- In a supported assistant, run: `/understand`.")
    else:
        print("- Refresh the graph if files changed, using the official Understand-Anything workflow.")
    print("- Explore visually: `/understand-dashboard`.")
    print("- Ask graph questions: `/understand-chat`.")
    print("- Explain target code: `/understand-explain <file-or-symbol>`.")
    print("- Review changed code: `/understand-diff`.")

    print()
    print("## Agent Handoff Template")
    print()
    print("```markdown")
    print("Understand-Anything context:")
    print("- Project root: {0}".format(root))
    print("- Graph artifact: {0}".format(graph_path))
    print("- Graph freshness: {0}".format("present" if graph_path.exists() else "missing"))
    print("- Relevant modules:")
    print("- Entry points:")
    print("- Candidate files:")
    print("- Dependency/impact paths:")
    print("- Dashboard/chat findings:")
    print("- Exclusions/blind spots: {0}".format(", ".join(excludes) if excludes else "none"))
    print("- Required verification:")
    print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
