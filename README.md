# Codex Skills

**Language:** English | [简体中文](README.zh-CN.md)

[![Codex Skills](https://img.shields.io/badge/Codex-Skills-2563EB)](https://github.com/TT-james/codex-skills)
[![Knowledge Graph](https://img.shields.io/badge/Focus-Knowledge%20Graph-16A34A)](skills/project-knowledge-graph)
[![Plugin Ready](https://img.shields.io/badge/Plugin-Ready-7C3AED)](plugins/knowledge-graph-skills)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Reusable Codex skills for project knowledge graph workflows.

This repository is designed as a small, shareable Codex skill catalog. Its first package helps Codex understand a repository before coding by using CodeGraph, Understand-Anything, or a low-friction fallback path. The goal is to reduce repeated whole-repo scans, prepare better multi-agent context, and make project onboarding more consistent.

---

## Start Here

Most users should install only the integrated skill:

```text
project-knowledge-graph
```

It decides whether to use CodeGraph, Understand-Anything, both tools, or plain `rg` fallback based on the current environment and task.

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

Restart Codex after installing new skills.

> Important: pick one install path. Use either the GitHub skill installer, manual copy, or plugin package. Do not install the same skill through multiple paths unless you intentionally want duplicate local copies.

---

## Included Skills

| Skill | Purpose | Best For |
|---|---|---|
| [`project-knowledge-graph`](skills/project-knowledge-graph) | Unified project knowledge graph orchestrator that chooses CodeGraph, Understand-Anything, hybrid mode, or fallback. | New repository onboarding, multi-agent planning, impact analysis, reducing repeated scans. |
| [`codegraph-project-knowledge`](skills/codegraph-project-knowledge) | Builds, refreshes, and queries a CodeGraph-backed local project code graph. | Semantic code search, symbols, callers, candidate files, implementation entry points, impact analysis. |
| [`understand-anything-project-knowledge`](skills/understand-anything-project-knowledge) | Builds and reuses Understand-Anything project knowledge graph context. | Visual project maps, dashboard/chat/explain/diff workflows, shared project understanding. |
| [`concise-requirement-refiner`](skills/concise-requirement-refiner) | Rewrites fuzzy Chinese business notes into concise field-focused requirement drafts. | Requirement整理, field notes, approval flow drafts, management list/filter/operation notes. |

---

## Install Options

### Option 1: Install One Skill From GitHub

Integrated skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

CodeGraph-only skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/codegraph-project-knowledge
```

Understand-Anything-only skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/understand-anything-project-knowledge
```

Concise requirement refiner:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/concise-requirement-refiner
```

### Option 2: Manual Copy

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/project-knowledge-graph ~/.codex/skills/
```

Windows target:

```text
C:\Users\<you>\.codex\skills\
```

### Option 3: Plugin Package

This repository also includes a plugin package:

```text
plugins/knowledge-graph-skills/
```

It bundles all three knowledge graph skills and is listed in:

```text
marketplace.json
```

Use this path when your Codex environment supports repository-backed plugin marketplace entries.

---

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

Use the concise requirement refiner when you need a short implementation-ready business requirement:

```text
Use $concise-requirement-refiner to整理下面这段需求，输出简洁字段化版本：...
```

---

## Codex Multi-Agent Pattern

Run the graph skill once before dispatching agents, then pass the same compact context to every role.

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

Suggested role usage:

| Role | How it uses the graph |
|---|---|
| Planner | Converts graph findings into task boundaries, dependency order, and unknowns. |
| Developer | Opens the graph-derived candidate files directly before editing. |
| Tester | Builds smoke and regression paths from entry points and impacted files. |
| Reviewer | Compares the diff against semantic impact and dependency paths. |
| Release writer | Records graph freshness, fallback analysis, and validation evidence. |

---

## External Tool Notes

These skills do not vendor CodeGraph or Understand-Anything. They orchestrate and document how Codex should use those tools when available.

- CodeGraph: https://github.com/colbymchenry/codegraph
- Understand-Anything: https://github.com/Lum1104/Understand-Anything

If a tool is not installed, the skills instruct Codex to record the failure and fall back to `rg --files`, `rg`, and direct file reads.

---

## Docs

| Document | Description |
|---|---|
| [Chinese README](README.zh-CN.md) | Full Chinese overview, installation, and usage guide. |
| [Quick Start](docs/QUICKSTART.md) | Short install and first-use guide. |
| [中文快速开始](docs/zh-CN/QUICKSTART.md) | 中文安装和首次使用说明。 |
| [Skill Catalog](docs/SKILL_CATALOG.md) | Detailed skill comparison and selection guide. |
| [中文技能目录](docs/zh-CN/SKILL_CATALOG.md) | 中文技能能力矩阵和选择建议。 |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common install, loading, and graph-tool issues. |
| [中文排障指南](docs/zh-CN/TROUBLESHOOTING.md) | 中文常见问题处理。 |
| [Concise Requirement Refiner](docs/CONCISE_REQUIREMENT_REFINER.md) | English guide for the concise requirement整理 skill. |
| [简洁需求整理技能](docs/zh-CN/CONCISE_REQUIREMENT_REFINER.md) | 中文说明：技能用途、安装方式、Codex 调用方式和输出格式。 |
| [Contributing](CONTRIBUTING.md) | How to add or update skills in this repository. |

---

## Repository Layout

```text
skills/
  project-knowledge-graph/
  codegraph-project-knowledge/
  understand-anything-project-knowledge/
  concise-requirement-refiner/

plugins/
  knowledge-graph-skills/
    .codex-plugin/plugin.json
    skills/

docs/
  QUICKSTART.md
  SKILL_CATALOG.md
  TROUBLESHOOTING.md
  zh-CN/

marketplace.json
README.md
README.zh-CN.md
```

---

## Validation

Validate a skill:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/project-knowledge-graph
```

Validate the plugin package:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```

---

## License

MIT. Use freely, adapt for your team, and keep useful skills shareable.
