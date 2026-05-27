---
name: project-knowledge-graph
description: Orchestrate CodeGraph and Understand-Anything for project knowledge graphs before coding. Use when entering a new repository, onboarding Codex or subagents, choosing between semantic code search and visual/chat project maps, reducing repeated repository scans, preparing multi-agent context, analyzing impact, or reusing durable project graph summaries.
---

# Project Knowledge Graph

Use this skill as the unified entry point for project knowledge graphs. It decides when to use CodeGraph, Understand-Anything, or both, then turns graph output into a compact context handoff for Codex and subagents.

## Decision

- Use **CodeGraph first** when the task needs code-level semantic search, symbols, callers, impact analysis, implementation entry points, or low-token targeted context.
- Use **Understand-Anything first** when the task needs visual architecture maps, project onboarding, chat/explain/diff workflows, durable project maps, or broad module relationship understanding.
- Use **both** for Standard/Strict work, unfamiliar repositories, cross-module changes, architecture review, performance/security review, or multi-agent planning.
- Fall back to `rg --files`, `rg`, and direct file reads when either graph tool is unavailable. Record the failure and do not pretend graph context exists.

## Workflow

1. Confirm the project root with `pwd` / `Get-Location`.
2. Run `scripts/probe_project_knowledge_graph.py --root <project-root>` from this skill.
3. Check existing artifacts:
   - CodeGraph: `.codegraph/`
   - Understand-Anything: `.understand-anything/knowledge-graph.json`
4. Choose the tool path:
   - CodeGraph-only for narrow implementation or impact questions.
   - Understand-Anything-only for project map, dashboard, onboarding, or chat-style exploration.
   - Hybrid for multi-agent work or high-risk changes.
5. Query graph tools before broad repository scans, then open exact files directly before editing.
6. Produce one concise handoff summary for all agents.
7. Refresh or mark graph context stale after major edits, refactors, or dependency layout changes.

## Quick Commands

```powershell
# From this skill folder, or replace <skill-dir> with the installed skill path.
python <skill-dir>\scripts\probe_project_knowledge_graph.py --root .

# CodeGraph when installed
codegraph status
codegraph context "<task or feature>"
codegraph search "<symbol, class, route, or table>"
codegraph impact "<file or symbol>"

# Understand-Anything in supported assistants
/understand
/understand-dashboard
/understand-chat
/understand-explain <file-or-symbol>
/understand-diff
```

## Multi-Agent Handoff

Run one shared graph orientation before dispatching subagents. Pass this template:

```markdown
Project knowledge graph context:
- Project root:
- Tool path: CodeGraph / Understand-Anything / Hybrid / Fallback
- Graph status:
- Relevant modules:
- Entry points:
- Candidate files:
- Symbol/caller/impact findings:
- Visual/chat/dashboard findings:
- Exclusions/blind spots:
- Staleness:
- Required verification:
```

Role usage:

- Planner: convert graph findings into module boundaries, dependencies, task order, and unknowns.
- Developer: open candidate files directly and implement from the graph-derived path.
- Tester: derive smoke/regression paths from entry points, data flows, and impacted files.
- Reviewer: compare the diff against semantic impact and dependency paths.
- Release writer: record graph freshness, generated artifacts, fallback analysis, and validation evidence.

## Matrix Cloud Pattern

For PHP / CodeIgniter projects, orient graph queries around:

```text
controller -> model -> view -> helper/library -> queue/cron -> SQL/config -> validation path
```

Prioritize:

- `application/controllers/`
- `application/models/`
- `application/views/`
- `application/helpers/`
- `application/libraries/`
- `application/queue/`
- `theme/`
- `scripts/`
- selected `sql/` files when database behavior is involved

Exclude dependency, cache, log, generated, private dump, and graph output directories unless explicitly required.

## Context Cache

When a repository benefits from durable context, create one small project-local summary:

```markdown
# Project Knowledge Graph Map

- Generated:
- Tool path:
- Graph artifacts:
- Exclusions:
- Main modules:
- Entry points:
- Cross-cutting services:
- Risk areas:
- Common validation commands:
- Refresh rule:
```

Prefer `.codex/memories/`, `.specstory/history/`, or the repository's documented agent notes. Do not paste full graph databases or JSON dumps into prompts.

## Guardrails

- Graphs guide orientation; direct file reads remain mandatory before edits.
- Do not index secrets, `.git/`, logs, caches, dependency folders, private dumps, or production-only data unless explicitly required.
- Do not commit `.codegraph/` or `.understand-anything/` artifacts unless the team intentionally tracks them.
- Keep graph summaries factual, dated, and scoped to the task.
- If graph tools disagree, prefer direct code facts and note the discrepancy.

## References

- Read `references/tool-comparison.md` to choose between CodeGraph, Understand-Anything, or hybrid mode.
- Read `references/setup-notes.md` when installing, configuring, or troubleshooting either tool.
- Run `scripts/probe_project_knowledge_graph.py` when entering a new repository or preparing multi-agent handoff.
