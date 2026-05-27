#!/usr/bin/env python3
"""Probe project knowledge graph readiness across CodeGraph and Understand-Anything."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path


DEFAULT_EXCLUDES = [
    ".git",
    ".codegraph",
    ".understand-anything",
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


def graph_json_summary(path: Path) -> str:
    if not path.exists():
        return "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return "present, unreadable JSON: {0}".format(exc)
    if isinstance(data, dict):
        keys = ", ".join(sorted(data.keys())[:8])
        return "present, top-level keys: {0}".format(keys or "none")
    return "present, JSON type: {0}".format(type(data).__name__)


def choose_path(codegraph_ready: bool, ua_ready: bool) -> str:
    if codegraph_ready and ua_ready:
        return "Hybrid"
    if codegraph_ready:
        return "CodeGraph"
    if ua_ready:
        return "Understand-Anything"
    return "Fallback"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check CodeGraph and Understand-Anything readiness for a repository."
    )
    parser.add_argument("--root", default=os.getcwd(), help="Project root to inspect.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    codegraph_dir = root / ".codegraph"
    ua_graph = root / ".understand-anything" / "knowledge-graph.json"
    codegraph_cmd = shutil.which("codegraph")
    ua_commands = [c for c in [shutil.which("understand-anything"), shutil.which("ua"), shutil.which("npx")] if c]
    excludes = existing_dirs(root, DEFAULT_EXCLUDES)
    priority = existing_dirs(root, PRIORITY_DIRS)

    codegraph_ready = codegraph_dir.exists()
    ua_ready = ua_graph.exists()
    tool_path = choose_path(codegraph_ready, ua_ready)

    print("# Project Knowledge Graph Probe")
    print()
    print("- Project root: `{0}`".format(root))
    print("- Recommended tool path: `{0}`".format(tool_path))
    print("- CodeGraph command: `{0}`".format(codegraph_cmd or "not found"))
    print("- CodeGraph artifact: `{0}`".format("present" if codegraph_ready else "missing"))
    print("- Understand-Anything commands: {0}".format(", ".join(ua_commands) if ua_commands else "none found"))
    print("- Understand-Anything graph: `{0}`".format(graph_json_summary(ua_graph)))
    print("- Suggested excludes present: {0}".format(", ".join(excludes) if excludes else "none detected"))
    print("- Priority source areas present: {0}".format(", ".join(priority) if priority else "none detected"))

    print()
    print("## Next Steps")
    print()
    if tool_path == "Hybrid":
        print("- Use Understand-Anything for broad module map and dashboard/chat findings.")
        print("- Use CodeGraph for symbols, candidate files, callers, and impact.")
    elif tool_path == "CodeGraph":
        print("- Use CodeGraph for targeted code context and impact.")
        print("- Consider adding Understand-Anything if visual onboarding or chat exploration is needed.")
    elif tool_path == "Understand-Anything":
        print("- Use Understand-Anything for broad project map and explain/diff workflows.")
        print("- Consider adding CodeGraph if precise symbol or impact queries are needed.")
    else:
        print("- Install or initialize a graph tool from official sources, or fall back to `rg` and direct reads.")
    print("- Always open target files directly before editing.")

    print()
    print("## Agent Handoff Template")
    print()
    print("```markdown")
    print("Project knowledge graph context:")
    print("- Project root: {0}".format(root))
    print("- Tool path: {0}".format(tool_path))
    print("- Graph status: CodeGraph={0}; Understand-Anything={1}".format(
        "present" if codegraph_ready else "missing",
        "present" if ua_ready else "missing",
    ))
    print("- Relevant modules:")
    print("- Entry points:")
    print("- Candidate files:")
    print("- Symbol/caller/impact findings:")
    print("- Visual/chat/dashboard findings:")
    print("- Exclusions/blind spots: {0}".format(", ".join(excludes) if excludes else "none"))
    print("- Staleness:")
    print("- Required verification:")
    print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
