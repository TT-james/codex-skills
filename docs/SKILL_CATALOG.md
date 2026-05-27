# Skill Catalog

**Language:** English | [简体中文](zh-CN/SKILL_CATALOG.md)

## Selection Guide

| Need | Recommended Skill |
|---|---|
| Default repository onboarding | `project-knowledge-graph` |
| Multi-agent planning context | `project-knowledge-graph` |
| Semantic code search and callers | `codegraph-project-knowledge` |
| Impact analysis from files or symbols | `codegraph-project-knowledge` |
| Visual project map or dashboard | `understand-anything-project-knowledge` |
| Chat/explain/diff project understanding | `understand-anything-project-knowledge` |
| High-risk cross-module work | `project-knowledge-graph` in hybrid mode |

## Skills

### project-knowledge-graph

Unified entry point. It decides when to use CodeGraph, Understand-Anything, both tools, or fallback repository search.

Use it when:

- You are entering an unfamiliar repository.
- You want one shared context before dispatching subagents.
- You need both semantic code impact and architecture-level understanding.
- You want to reduce repeated whole-repository scans.

### codegraph-project-knowledge

CodeGraph-specific workflow for local code graph probing, semantic search, symbol/caller lookup, and impact analysis.

Use it when:

- The task is implementation-heavy.
- You need entry points, callers, candidate files, or symbol-level context.
- You want focused, low-token context before opening files.

### understand-anything-project-knowledge

Understand-Anything-specific workflow for visual/chat-oriented project maps and durable repository understanding.

Use it when:

- You need broad project orientation.
- You want dashboard, chat, explain, or diff workflows.
- You need a team-friendly project map.

## Team Default

Use `project-knowledge-graph` as the team default. Keep the two single-tool skills available for explicit tool-specific work.
