#!/usr/bin/env python3
"""Probe a repository for CodeGraph readiness and emit Codex agent context."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


DEFAULT_EXCLUDES = [
    ".git",
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
]


def run_status(root: Path) -> str:
    try:
        result = subprocess.run(
            ["codegraph", "status"],
            cwd=str(root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
    except Exception as exc:
        return "status command failed: {0}".format(exc)
    return result.stdout.strip() or "status command returned no output"


def existing_dirs(root: Path, dirs: list[str]) -> list[str]:
    found = []
    for rel in dirs:
        if (root / rel).exists():
            found.append(rel)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check CodeGraph readiness for a repository and print an agent handoff."
    )
    parser.add_argument("--root", default=os.getcwd(), help="Project root to inspect.")
    parser.add_argument(
        "--run-status",
        action="store_true",
        help="Run `codegraph status` if the codegraph command is available.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    codegraph_bin = shutil.which("codegraph")
    codegraph_dir = root / ".codegraph"
    excludes = existing_dirs(root, DEFAULT_EXCLUDES)
    priority = existing_dirs(root, PRIORITY_DIRS)

    print("# CodeGraph Project Probe")
    print()
    print("- Project root: `{0}`".format(root))
    print("- CodeGraph command: `{0}`".format(codegraph_bin or "not found"))
    print("- Local index directory: `{0}`".format("present" if codegraph_dir.exists() else "missing"))
    print("- Suggested excludes present: {0}".format(", ".join(excludes) if excludes else "none detected"))
    print("- Priority source areas present: {0}".format(", ".join(priority) if priority else "none detected"))

    if args.run_status and codegraph_bin:
        print()
        print("## `codegraph status`")
        print()
        print("```text")
        print(run_status(root))
        print("```")

    print()
    print("## Next Commands")
    print()
    if not codegraph_bin:
        print("- Read `references/codegraph-setup.md`, then install CodeGraph from the official source.")
    if not codegraph_dir.exists():
        print("- Initialize the index from the project root, for example: `codegraph init -i`.")
    else:
        print("- Refresh the existing index if files changed, for example: `codegraph sync`.")
    print("- Verify health: `codegraph status`.")
    print("- Query task context: `codegraph context \"<task>\"`.")
    print("- Query impact: `codegraph impact \"<file-or-symbol>\"`.")

    print()
    print("## Agent Handoff Template")
    print()
    print("```markdown")
    print("CodeGraph context:")
    print("- Project root: {0}".format(root))
    print("- Index status: {0}".format("present" if codegraph_dir.exists() else "missing"))
    print("- Relevant modules:")
    print("- Candidate files:")
    print("- Impact paths:")
    print("- Exclusions/staleness: {0}".format(", ".join(excludes) if excludes else "none"))
    print("- Required verification:")
    print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
