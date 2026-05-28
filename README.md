# Codex Skill Hub

**Language:** English | [简体中文](README.zh-CN.md)

[![Codex Skills](https://img.shields.io/badge/Codex-Custom%20Skills-2563EB)](https://github.com/TT-james/codex-skills)
[![Skill Hub](https://img.shields.io/badge/Hub-Skills%20%2B%20Docs-16A34A)](skills)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An integration repository for reusable Codex custom skills and their documentation.

This repository collects self-built Codex skills, references, and helper scripts under `skills/`. It is meant to be a clean shared source for custom Codex capabilities, not a single-purpose package or a duplicate plugin bundle.

## Working Notes

- Each skill is self-contained under `skills/<skill-name>/`.
- `SKILL.md` is the runtime entry point Codex reads when the skill triggers.
- Skill-specific long-form docs should live inside that skill's `references/` directory.
- Reusable automation should live inside that skill's `scripts/` directory.
- Install only the skills you need into your local Codex skills directory.

## Choose What You Need

| Need | Recommended skill |
|---|---|
| Understand a repository before coding or dispatching agents | `project-knowledge-graph` |
| Generate Chinese AI promotion / AI usage case Word documents | `ai-promotion-case-doc` |
| Audit, curate, or publish a local skill library | `skill-library-manager` |
| Sync local custom skills to this GitHub repository | `sync-skills-to-github` |

## Included Skills

<!-- sync-skills:skills:start -->
| Skill | Purpose | Best For |
|---|---|---|
| [`project-knowledge-graph`](skills/project-knowledge-graph) | Unified project knowledge graph orchestrator that chooses CodeGraph, Understand-Anything, hybrid mode, or fallback. | New repository onboarding, multi-agent planning, impact analysis, reducing repeated scans. |
| [`codegraph-project-knowledge`](skills/codegraph-project-knowledge) | Builds, refreshes, and queries a CodeGraph-backed local project code graph. | Semantic code search, symbols, callers, candidate files, implementation entry points, impact analysis. |
| [`understand-anything-project-knowledge`](skills/understand-anything-project-knowledge) | Builds and reuses Understand-Anything project knowledge graph context. | Visual project maps, dashboard/chat/explain/diff workflows, shared project understanding. |
| [`skill-library-manager`](skills/skill-library-manager) | Audits, curates, deduplicates, installs, validates, and publishes Codex skill libraries. | Skill discovery, active-vs-backup decisions, safer global stacks, and team skill governance. |
| [`sync-skills-to-github`](skills/sync-skills-to-github) | Synchronizes local Codex skills to GitHub while preserving established repository templates. | Publishing local skills to GitHub without disturbing README layout or hand-written docs. |
| [`install-github-skills`](skills/install-github-skills) | Installs, lists, updates, and removes Codex skills from a GitHub skills repository. | Team skill distribution from TT-james/codex-skills or another GitHub skill hub. |
| [`ai-promotion-case-doc`](skills/ai-promotion-case-doc) | Generates reusable Chinese AI promotion case documents from Codex work evidence and history. | AI adoption stories, team enablement cases, delivery retrospectives, and management-facing Word reports. |
<!-- sync-skills:skills:end -->

## Install

Bootstrap the installer skill first, then use `$install-github-skills` to install other skills from this repository:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/install-github-skills
```

Windows example:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo TT-james/codex-skills `
  --path skills/install-github-skills
```

You can also download the packaged ZIP:

```text
https://github.com/TT-james/codex-skills/raw/main/packages/install-github-skills.zip
```

Unzip it into `~/.codex/skills/` or `C:\Users\<you>\.codex\skills\`, then restart Codex.

Install one skill from GitHub:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/<skill-name>
```

Or copy manually:

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/<skill-name> ~/.codex/skills/
```

Windows target:

```text
C:\Users\<you>\.codex\skills\
```

Restart Codex after installing new skills.

## Examples

```text
Use $project-knowledge-graph to inspect this repository and prepare a concise multi-agent context.
```

```text
Use $ai-promotion-case-doc to turn this Codex historical session into an AI推广案例 Word document.
```

```text
Use $sync-skills-to-github to sync my local Codex skills to TT-james/codex-skills.
```

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
    references/
    scripts/

packages/
  install-github-skills.zip

CONTRIBUTING.md
LICENSE
README.md
README.zh-CN.md
```

## Validation

Validate a skill:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

## License

MIT. Use freely, adapt for your team, and keep useful skills shareable.
