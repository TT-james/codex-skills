# Codex Skill Hub

**Language:** English | [简体中文](README.zh-CN.md)

[![Codex Skills](https://img.shields.io/badge/Codex-Custom%20Skills-2563EB)](https://github.com/TT-james/codex-skills)
[![Skill Hub](https://img.shields.io/badge/Hub-Skills%20%2B%20Docs-16A34A)](skills)
[![Plugin Optional](https://img.shields.io/badge/Plugin-Optional-7C3AED)](plugins/knowledge-graph-skills)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An integration repository for reusable Codex custom skills and their documentation.

This repository is not a single-purpose skill package. It collects self-built Codex skills, reference docs, helper scripts, and optional plugin packaging so the same capabilities can be reused across local Codex environments. Current skills cover project knowledge graphs, AI promotion case document generation, skill-library governance, and GitHub synchronization.

---

## Choose What You Need

Install only the skill you need. Each skill lives under `skills/<skill-name>/` with its own `SKILL.md`, references, scripts, and UI metadata when available.

| Need | Recommended skill |
|---|---|
| Understand a repository before coding or dispatching agents | `project-knowledge-graph` |
| Generate Chinese AI promotion / AI usage case Word documents | `ai-promotion-case-doc` |
| Audit, curate, or publish a local skill library | `skill-library-manager` |
| Sync local custom skills to this GitHub repository | `sync-skills-to-github` |

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/<skill-name>
```

Restart Codex after installing new skills.

> Important: pick one install path. Use either the GitHub skill installer, manual copy, or plugin package. Do not install the same skill through multiple paths unless you intentionally want duplicate local copies.

---

## Included Skills

<!-- sync-skills:skills:start -->
| Skill | Purpose | Best For |
|---|---|---|
| [`project-knowledge-graph`](skills/project-knowledge-graph) | Unified project knowledge graph orchestrator that chooses CodeGraph, Understand-Anything, hybrid mode, or fallback. | New repository onboarding, multi-agent planning, impact analysis, reducing repeated scans. |
| [`codegraph-project-knowledge`](skills/codegraph-project-knowledge) | Builds, refreshes, and queries a CodeGraph-backed local project code graph. | Semantic code search, symbols, callers, candidate files, implementation entry points, impact analysis. |
| [`understand-anything-project-knowledge`](skills/understand-anything-project-knowledge) | Builds and reuses Understand-Anything project knowledge graph context. | Visual project maps, dashboard/chat/explain/diff workflows, shared project understanding. |
| [`skill-library-manager`](skills/skill-library-manager) | Audits, curates, deduplicates, installs, validates, and publishes Codex skill libraries. | Skill discovery, active-vs-backup decisions, safer global stacks, and team skill governance. |
| [`sync-skills-to-github`](skills/sync-skills-to-github) | Synchronizes local Codex skills to GitHub while preserving established repository templates. | Publishing local skills to GitHub without disturbing README layout or hand-written docs. |
| [`ai-promotion-case-doc`](skills/ai-promotion-case-doc) | Generates reusable Chinese AI promotion case documents from Codex work evidence and history. | AI adoption stories, team enablement cases, delivery retrospectives, and management-facing Word reports. |
<!-- sync-skills:skills:end -->

---

## Install Options

### Option 1: Install One Skill From GitHub

Example: install the AI promotion case document skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/ai-promotion-case-doc
```

Example: install the integrated project knowledge graph skill:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

Example: install the skill sync helper:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/sync-skills-to-github
```

### Option 2: Manual Copy

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/<skill-name> ~/.codex/skills/
```

Windows target:

```text
C:\Users\<you>\.codex\skills\
```

### Option 3: Plugin Package

This repository also includes an optional plugin package for the knowledge graph skills:

```text
plugins/knowledge-graph-skills/
```

It bundles the three knowledge graph skills and is listed in:

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

Generate an AI promotion case document from Codex history or implementation notes:

```text
Use $ai-promotion-case-doc to turn this Codex historical session into an AI推广案例 Word document.
```

Publish local custom skills to this repository:

```text
Use $sync-skills-to-github to sync my local Codex skills to TT-james/codex-skills.
```

---

## Project Knowledge Graph Pattern

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

## Knowledge Graph Tool Notes

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
| [Contributing](CONTRIBUTING.md) | How to add or update skills in this repository. |

---

## Repository Layout

```text
skills/
  ai-promotion-case-doc/
  project-knowledge-graph/
  codegraph-project-knowledge/
  understand-anything-project-knowledge/
  skill-library-manager/
  sync-skills-to-github/

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
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

Validate the plugin package:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```

---

## License

MIT. Use freely, adapt for your team, and keep useful skills shareable.
