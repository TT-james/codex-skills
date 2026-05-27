# Quick Start

**Language:** English | [简体中文](zh-CN/QUICKSTART.md)

## 1. Pick One Install Path

Use one of these paths:

- Recommended: install `skills/project-knowledge-graph` from GitHub.
- Manual: copy one skill folder into your local Codex skills directory.
- Plugin: install `plugins/knowledge-graph-skills` if your Codex environment supports repository-backed plugins.

Avoid stacking install paths for the same skill.

## 2. Install The Recommended Skill

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

Restart Codex after installation.

## 3. Use It In A Repository

Ask Codex:

```text
Use $project-knowledge-graph to inspect this repository and prepare a concise multi-agent context.
```

The skill will:

- Probe whether CodeGraph or Understand-Anything is available.
- Reuse existing graph artifacts when present.
- Fall back to `rg` and direct file reads when graph tools are unavailable.
- Produce a compact project context for planning, development, testing, review, and release notes.

## 4. Keep Graph Context Fresh

Refresh or mark graph context stale after:

- Large refactors.
- Dependency layout changes.
- Major module additions or removals.
- Changes that invalidate entry points, routes, or data flows.
