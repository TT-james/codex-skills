---
name: codegraph-project-knowledge
description: Build, refresh, and query a project-local CodeGraph knowledge graph before coding. Use when entering a new repository, onboarding Codex or subagents to an unfamiliar codebase, reducing repeated repository-wide searches, planning multi-agent work from code structure, investigating impact of changes, or needing semantic context from CodeGraph CLI/MCP.
---

# CodeGraph Project Knowledge

Use CodeGraph as the first project-orientation layer before broad `rg` sweeps. Prefer it for structure, dependency, symbol, call-path, and impact questions; fall back to direct file reads and `rg` for exact text, generated files, or when CodeGraph is unavailable.

## Workflow

1. Confirm the current project root with `pwd` / `Get-Location`, then run `scripts/probe_codegraph_project.py --root <project-root>` from this skill to inspect readiness.
2. If CodeGraph is not installed, read `references/codegraph-setup.md` and install it using the current official method. Avoid guessing global config paths.
3. Initialize or refresh the project index from the repository root. Exclude dependency, cache, build, log, and history directories unless the task specifically needs them.
4. Run `codegraph status` or the closest available health command. If the index is stale or empty, refresh before relying on results.
5. Query CodeGraph for high-level context before opening many files. Ask for affected files, symbols, ownership boundaries, call paths, and implementation entry points.
6. Share a compact knowledge summary with any subagent or multi-agent prompt: task goal, relevant CodeGraph findings, candidate files, known exclusions, and validation commands.
7. After edits that change important relationships, refresh the index or note that CodeGraph results may be stale.

## Quick Commands

```powershell
python C:\Users\lenovo\.codex\skills\codegraph-project-knowledge\scripts\probe_codegraph_project.py --root .
codegraph status
codegraph context "<task or feature>"
codegraph search "<symbol, class, route, or table>"
codegraph impact "<file or symbol>"
```

Use `--run-status` with the probe script only when running `codegraph status` is acceptable for the current repository.

## Query Pattern

Start each new-project task with this sequence when useful:

```text
1. What are the main modules and entry points for this request?
2. Which controllers, models, views, jobs, config files, and tests are linked?
3. What symbols or files are most likely impacted by this change?
4. Which exact files should be opened next for verification?
```

For Matrix Cloud / CodeIgniter style projects, ask for controller -> model -> view -> helper/library -> SQL/queue paths before editing.

## Multi-Agent Use

When dispatching subagents, provide the CodeGraph summary instead of asking every subagent to rediscover the repository. Include only task-relevant facts:

```markdown
CodeGraph context:
- Project root:
- Index time/status:
- Relevant modules:
- Candidate files:
- Impact paths:
- Exclusions/staleness:
- Required verification:
```

If a subagent needs deeper context, ask it to query CodeGraph for the narrow module or symbol rather than repeating a full project scan.

For multi-agent planning, use one shared CodeGraph orientation pass first, then split work:

- Planner: convert CodeGraph findings into module boundaries, task dependencies, and unknowns.
- Developer: open candidate files directly, then edit with the CodeGraph impact list nearby.
- Tester: derive smoke and regression paths from impacted entry points.
- Reviewer: compare the diff against the CodeGraph impact list and flag missed callers or data paths.
- Release writer: mention whether CodeGraph was fresh, stale, or unavailable in release notes when relevant.

## Context Cache

For a new repository or long-running effort, create or update one small project-local context note only when the user or project workflow allows it. Keep it short enough to paste into subagent prompts:

```markdown
# CodeGraph Project Map

- Generated:
- CodeGraph status:
- Index exclusions:
- Main modules:
- Entry points:
- Cross-cutting services:
- Risk areas:
- Common validation commands:
- Refresh rule:
```

Prefer existing project memory locations such as `.codex/memories/`, `.specstory/history/`, or the repository's documented agent notes. Do not store the full graph dump in prompt context; store the database locally through CodeGraph and pass only summaries.

## Guardrails

- Do not treat CodeGraph as the sole source of truth. Read changed files directly before editing.
- Do not index secrets, `.git/`, logs, caches, dependency folders, generated assets, or private data dumps unless explicitly required.
- Do not commit `.codegraph/` database files unless the repository intentionally tracks them.
- Prefer project-local configuration for shared team behavior and user-level configuration for personal Codex workflow.
- Record command failures and fallback searches in task notes so future agents understand whether CodeGraph was unavailable or only partially useful.
- Keep cached summaries factual and dated. Refresh them after major refactors, dependency layout changes, or stale CodeGraph status.

## References

- Read `references/codegraph-setup.md` when installing, configuring, troubleshooting, or writing project-specific CodeGraph rules.
- Run `scripts/probe_codegraph_project.py` when entering a new repository or preparing a subagent handoff.
