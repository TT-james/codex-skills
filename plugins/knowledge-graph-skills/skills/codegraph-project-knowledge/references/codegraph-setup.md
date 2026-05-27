# CodeGraph Setup And Usage Notes

Use this reference only when the task requires installing, configuring, or troubleshooting CodeGraph.

## Official Source

- Repository and docs entry: https://github.com/colbymchenry/codegraph

Check the official README or docs before changing installation commands. CodeGraph is an external dependency and command names may change.

## Current Integration Shape

CodeGraph is intended to provide a local semantic knowledge graph for a repository. Its common workflow is:

```powershell
# From project root
codegraph status
codegraph init -i
codegraph sync
codegraph search "<module, symbol, or feature>"
codegraph context "<task or symbol>"
codegraph impact "<file or symbol>"
```

If a command is unavailable, run:

```powershell
codegraph --help
codegraph <command> --help
```

Then adapt the workflow to the installed version.

## Suggested Ignore Policy

Exclude:

- `.git/`, `.codegraph/`, `.idea/`, `.vscode/`
- `vendor/`, `node_modules/`, generated dependency folders
- caches, build outputs, logs, coverage, temporary exports
- large binary files, dumps, and private data snapshots
- conversation histories unless the task explicitly needs process memory

For PHP / CodeIgniter projects, prioritize:

- `application/controllers/`
- `application/models/`
- `application/views/`
- `application/helpers/`
- `application/libraries/`
- `application/queue/`
- `theme/`
- `scripts/`
- selected `sql/` files when the request touches database behavior

## Codex / Agent Prompt Template

Before coding in a new repository, run a narrow CodeGraph orientation and pass this to agents:

```markdown
Use CodeGraph first. Do not rescan the whole repository unless CodeGraph is missing required context.

Task:

CodeGraph findings:
- Index status:
- Relevant modules:
- Entry points:
- Impacted symbols/files:
- Unknowns:

Open these files directly before editing:

Validation expected:
```

## Project Cache Placement

When a repository benefits from durable CodeGraph context, prefer a small summary file over repeated broad analysis. Use the project's existing convention first:

- `.codex/memories/codegraph-project-map.md` for Codex-local project memory
- `.specstory/history/<task>.md` for task-scoped history
- `docs/` or `references/` only if the team intentionally tracks development-process notes

Recommended cache rules:

- Include generation time and CodeGraph status.
- Include exclusions so agents understand blind spots.
- Include entry points and risk areas, not every symbol.
- Update after major refactors or when `codegraph status` reports stale data.
- Never paste full graph dumps into agent prompts.

## Failure Fallback

If CodeGraph cannot be installed or indexed:

1. Capture the command and error.
2. Continue with `rg --files`, `rg`, and direct file reads.
3. Avoid pretending CodeGraph context exists.
4. Add a task note describing the fallback so future agents do not repeat the same failed setup blindly.
