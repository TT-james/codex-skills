# Codex Skills

This repository collects reusable Codex skills created for project knowledge graph workflows.

## Included Skills

| Skill | Purpose | Best For |
|---|---|---|
| `project-knowledge-graph` | Unified project knowledge graph orchestrator that chooses CodeGraph, Understand-Anything, hybrid mode, or fallback. | New repository onboarding, multi-agent planning, impact analysis, reducing repeated scans. |
| `codegraph-project-knowledge` | Builds, refreshes, and queries a CodeGraph-backed local project code graph. | Semantic code search, symbols, callers, candidate files, implementation entry points, impact analysis. |
| `understand-anything-project-knowledge` | Builds and reuses Understand-Anything project knowledge graph context. | Visual project maps, dashboard/chat/explain/diff workflows, shared project understanding. |

## Recommended Skill

Most users should install:

```text
project-knowledge-graph
```

It is the integrated skill that decides whether to use CodeGraph, Understand-Anything, both, or a plain `rg` fallback.

## Install A Skill Into Codex

Use Codex's `skill-installer` workflow to install from this GitHub repository.

Install the integrated skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

Install the CodeGraph-only skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/codegraph-project-knowledge
```

Install the Understand-Anything-only skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/understand-anything-project-knowledge
```

Install all three:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph \
  --path skills/codegraph-project-knowledge \
  --path skills/understand-anything-project-knowledge
```

Restart Codex after installing new skills.

## Manual Install

Clone this repository and copy a skill folder into your Codex skills directory:

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/project-knowledge-graph ~/.codex/skills/
```

On Windows, copy to:

```text
C:\Users\<you>\.codex\skills\
```

Restart Codex after copying.

## Plugin Package

This repository also includes a plugin package:

```text
plugins/knowledge-graph-skills/
```

It bundles all three knowledge graph skills and is listed in:

```text
marketplace.json
```

Use this package if your Codex environment supports installing plugins from a repository marketplace source.

## Usage Examples

Use the integrated skill before working in an unfamiliar repository:

```text
Use $project-knowledge-graph to inspect this repository and prepare a concise multi-agent context.
```

Use CodeGraph directly when you need precise code impact:

```text
Use $codegraph-project-knowledge to find the entry points and impacted files for this feature.
```

Use Understand-Anything directly when you need a project map:

```text
Use $understand-anything-project-knowledge to build a visual/chat-oriented project map.
```

## External Tool Notes

These skills do not vendor CodeGraph or Understand-Anything. They orchestrate and document how Codex should use those tools when available.

- CodeGraph: https://github.com/colbymchenry/codegraph
- Understand-Anything: https://github.com/Lum1104/Understand-Anything

If a tool is not installed, the skills instruct Codex to record the failure and fall back to `rg --files`, `rg`, and direct file reads.

## Repository Layout

```text
skills/
  project-knowledge-graph/
  codegraph-project-knowledge/
  understand-anything-project-knowledge/

plugins/
  knowledge-graph-skills/
    .codex-plugin/plugin.json
    skills/

marketplace.json
```

## Validation

Before publishing a skill, validate it with:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/project-knowledge-graph
```

Validate the plugin package with:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```
