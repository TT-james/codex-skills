# Troubleshooting

**Language:** English | [简体中文](zh-CN/TROUBLESHOOTING.md)

## Codex Does Not See The Skill

Check:

- The skill folder is under `~/.codex/skills/` or `C:\Users\<you>\.codex\skills\`.
- The folder contains `SKILL.md` at its root.
- Codex was restarted after installation.
- You did not install nested paths such as `skills/project-knowledge-graph/project-knowledge-graph`.

## Duplicate Skills Appear

This usually means the same skill was installed through multiple paths.

Fix:

- Keep one copy only.
- Prefer the GitHub-installed copy or the plugin-installed copy, not both.
- Restart Codex after cleanup.

## CodeGraph Is Not Available

The skill should record the missing tool and fall back to `rg` and direct file reads.

Check the upstream project for installation:

```text
https://github.com/colbymchenry/codegraph
```

## Understand-Anything Is Not Available

The skill should record the missing tool and continue with CodeGraph or fallback mode.

Check the upstream project:

```text
https://github.com/Lum1104/Understand-Anything
```

## Graph Context Looks Stale

Refresh or rebuild graph context after:

- Large refactors.
- Dependency moves.
- Route, command, or entry point changes.
- New modules added to the repository.

Always open target files directly before editing. Graph context is an orientation aid, not a replacement for source reads.
