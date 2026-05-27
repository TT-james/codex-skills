# Understand-Anything Setup And Usage Notes

Use this reference only when installing, configuring, or troubleshooting Understand-Anything.

## Official Source

- Repository: https://github.com/Lum1104/Understand-Anything

Check the official README before changing installation commands. Understand-Anything is an external dependency and command names may change.

## Current Integration Shape

The official project describes Understand-Anything as an AI-native codebase and knowledge-base visualization tool. It can generate a knowledge graph for a repository and supports AI coding assistant integrations including Codex.

Common workflow after installation:

```text
/understand
/understand-dashboard
/understand-chat
/understand-explain <file-or-symbol>
/understand-diff
```

The expected local project artifact is:

```text
.understand-anything/knowledge-graph.json
```

If slash commands are not available, inspect the installed package help, MCP configuration, or official docs and adapt the workflow.

## Suggested Ignore Policy

Exclude:

- `.git/`, `.understand-anything/`, `.codegraph/`, `.idea/`, `.vscode/`
- `vendor/`, `node_modules/`, generated dependency folders
- caches, build outputs, logs, coverage, temporary exports
- large binary files, database dumps, and private data snapshots
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

Before coding in a new repository:

```markdown
Use Understand-Anything first. Do not rescan the whole repository unless the knowledge graph is missing required context.

Task:

Understand-Anything findings:
- Graph artifact:
- Graph freshness:
- Relevant modules:
- Entry points:
- Dependency/impact paths:
- Unknowns:

Open these files directly before editing:

Validation expected:
```

## Project Cache Placement

When durable graph context is useful, prefer a small summary file over repeated broad analysis:

- `.codex/memories/understand-anything-project-map.md` for Codex-local project memory
- `.specstory/history/<task>.md` for task-scoped history
- `docs/` or `references/` only if the team intentionally tracks process notes

Recommended cache rules:

- Include generation time and graph status.
- Include exclusions and blind spots.
- Include entry points and risk areas, not every node.
- Update after major refactors or stale graph status.
- Never paste full graph dumps into agent prompts.

## Failure Fallback

If Understand-Anything cannot be installed or indexed:

1. Capture the command and error.
2. Continue with `rg --files`, `rg`, and direct file reads.
3. Avoid pretending graph context exists.
4. Add a task note describing the fallback so future agents do not repeat the same failed setup blindly.
