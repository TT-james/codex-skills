---
name: understand-anything-project-knowledge
description: Build, inspect, and reuse project knowledge graphs with Understand-Anything before coding. Use when entering a new repository, onboarding Codex or subagents to an unfamiliar codebase, creating a visual or chat-based project map, reducing repeated repository scans, planning multi-agent work, reviewing change impact, or needing a durable `.understand-anything/knowledge-graph.json` context.
---

# Understand Anything Project Knowledge

Use Understand-Anything as a project-orientation layer when a repository needs a durable knowledge graph, visual dashboard, or chat/explain/diff workflow before development. Prefer it for architecture maps, module relationships, onboarding, review context, and multi-agent handoffs; still read target files directly before editing.

## Workflow

1. Confirm the project root with `pwd` / `Get-Location`, then run `scripts/probe_understand_anything_project.py --root <project-root>` from this skill.
2. If Understand-Anything is not installed, read `references/understand-anything-setup.md` and install it from the official source. Check the current README before running setup commands.
3. Initialize or refresh the knowledge graph from the project root. The expected local artifact is `.understand-anything/knowledge-graph.json`.
4. Use `/understand` for full project analysis, `/understand-dashboard` for visual exploration, `/understand-chat` for questions, `/understand-explain` for code explanation, and `/understand-diff` for change review when available.
5. Summarize only task-relevant findings for Codex: modules, entry points, dependencies, risk areas, candidate files, and validation paths.
6. Share the summary with subagents instead of asking each one to rediscover the repository.
7. Refresh or mark the graph stale after major edits, refactors, dependency layout changes, or large generated-file changes.

## Quick Commands

```powershell
python C:\Users\lenovo\.codex\skills\understand-anything-project-knowledge\scripts\probe_understand_anything_project.py --root .

# Inside a supported AI coding assistant after installation:
/understand
/understand-dashboard
/understand-chat
/understand-explain <file-or-symbol>
/understand-diff
```

If slash commands are unavailable in the current environment, use the official CLI/MCP instructions from the repository and record the fallback.

## Query Pattern

Start with these project questions:

```text
1. What are the main modules, entry points, and data flows for this task?
2. Which files or symbols are central to the requested behavior?
3. Which dependencies, callers, tests, jobs, configs, SQL scripts, or views may be affected?
4. What should each subagent open directly before editing or reviewing?
5. Is `.understand-anything/knowledge-graph.json` fresh enough to trust?
```

For Matrix Cloud / CodeIgniter projects, orient around controller -> model -> view -> helper/library -> queue -> SQL paths.

## Multi-Agent Use

Run one shared Understand-Anything orientation pass before multi-agent execution. Pass this compact context to subagents:

```markdown
Understand-Anything context:
- Project root:
- Graph artifact:
- Graph freshness:
- Relevant modules:
- Entry points:
- Candidate files:
- Dependency/impact paths:
- Dashboard/chat findings:
- Exclusions/blind spots:
- Required verification:
```

Recommended role usage:

- Planner: convert graph findings into module boundaries, dependencies, unknowns, and task order.
- Developer: open candidate files directly and implement against the graph-derived path.
- Tester: derive smoke and regression coverage from entry points, data flows, and impacted files.
- Reviewer: compare the diff against graph impact and dependency paths.
- Release writer: record graph freshness, generated artifacts, and any fallback analysis.

## Context Cache

When useful, keep one short project-local context note:

```markdown
# Understand-Anything Project Map

- Generated:
- Graph status:
- Graph artifact:
- Index exclusions:
- Main modules:
- Entry points:
- Cross-cutting services:
- Risk areas:
- Common validation commands:
- Refresh rule:
```

Prefer existing project memory locations such as `.codex/memories/`, `.specstory/history/`, or documented agent notes. Do not paste the full JSON graph into prompts; store the graph locally and pass summaries.

## Guardrails

- Do not treat the graph as the sole source of truth. Read changed files directly before editing.
- Do not index secrets, `.git/`, logs, caches, dependency folders, generated assets, private dumps, or production-only data unless explicitly required.
- Do not commit `.understand-anything/` artifacts unless the repository intentionally tracks them.
- Prefer project-local rules for team behavior and user-level setup for personal Codex workflow.
- If Understand-Anything is unavailable, record the command/error and fall back to `rg --files`, `rg`, and direct file reads.
- Refresh cached summaries after major refactors or stale graph status.

## References

- Read `references/understand-anything-setup.md` when installing, configuring, troubleshooting, or writing project-specific Understand-Anything rules.
- Run `scripts/probe_understand_anything_project.py` when entering a new repository or preparing a subagent handoff.
