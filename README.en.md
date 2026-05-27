# Codex Skills

This repository is a backup and sharing space for reusable Codex skills.

Source repository: https://github.com/TT-james/codex-skills.git

## Skill Index

| Skill | What it does | Path |
| --- | --- | --- |
| `codegraph-project-knowledge` | Build, refresh, and query a project-local CodeGraph knowledge graph before coding. Use when entering a new repository, onboarding Codex or subagents to an unfamiliar codebase, reducing repeated repository-wide searches, planning multi-agent work from code structure, investigating impact of changes, or needing semantic context from CodeGraph CLI/MCP. | `skills/codegraph-project-knowledge` |
| `project-knowledge-graph` | Orchestrate CodeGraph and Understand-Anything for project knowledge graphs before coding. Use when entering a new repository, onboarding Codex or subagents, choosing between semantic code search and visual/chat project maps, reducing repeated repository scans, preparing multi-agent context, analyzing impact, or reusing durable project graph summaries. | `skills/project-knowledge-graph` |
| `skill-library-manager` | Manage Codex and agent skill libraries by combining the best ideas from open skill ecosystems. Use when the user asks to audit installed skills, discover better skills on GitHub, choose active vs backup skills, deduplicate broad workflow skills, compare skill managers such as openai/skills, vercel-labs/skills, ComposioHQ/awesome-codex-skills, yeasy/ask, Agent-Skills, oh-my-skills, xiaobai-skills, install or update skill sets, create a skills inventory, publish skills to a GitHub skills repository, or design a team-ready skill governance workflow. | `skills/skill-library-manager` |
| `sync-skills-to-github` | Synchronize locally generated Codex skills to the user's GitHub skills repository, defaulting to TT-james/codex-skills.git. Use when the user asks to upload, publish, back up, mirror, or sync local Codex skills to GitHub, and when they need bilingual Chinese/English documentation describing what each skill does, how to use it, and how to apply or install it in Codex. | `skills/sync-skills-to-github` |
| `understand-anything-project-knowledge` | Build, inspect, and reuse project knowledge graphs with Understand-Anything before coding. Use when entering a new repository, onboarding Codex or subagents to an unfamiliar codebase, creating a visual or chat-based project map, reducing repeated repository scans, planning multi-agent work, reviewing change impact, or needing a durable `.understand-anything/knowledge-graph.json` context. | `skills/understand-anything-project-knowledge` |

## How to Use in Codex

1. Copy the skill folder you need from `skills/<skill-name>` into your local `~/.codex/skills/<skill-name>` directory.
2. Restart or refresh Codex if your environment does not auto-discover new skills.
3. Invoke the skill explicitly with `$skill-name`, or ask for a task that matches the skill description.
4. Open the skill's `SKILL.md` to see its workflow, scripts, references, and usage constraints.

## How to Update This Repository

Run the local Codex skill `$sync-skills-to-github` and ask Codex to sync local skills to GitHub. The sync process copies local skill folders, regenerates these docs, commits the changes, and pushes them to the repository when authentication is available.

## Notes

Review generated changes before publishing if a skill may contain private project paths, internal business rules, credentials, or customer data.
