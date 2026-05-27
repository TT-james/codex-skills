# Project Patterns For Skill Library Management

Use this reference when comparing skill-management projects or designing a local/team workflow.

## Pattern Table

| Project | Strong pattern to reuse | Watch out for |
|---|---|---|
| `openai/skills` | Treat as the official source for Codex skill layout, system skills, curated/experimental separation, and validation style. | It is a catalog and standard reference, not a full local package manager. |
| `vercel-labs/skills` | CLI ergonomics: add/list/find/update/remove, global vs project scope, multi-agent targeting, symlink vs copy choices. | Check current CLI commands before use because npm tools evolve quickly. |
| `ComposioHQ/awesome-codex-skills` | Discovery taxonomy and practical examples across development, productivity, communication, data, and meta utilities. | Catalog entries need independent quality and safety review before global install. |
| `yeasy/ask` | Package-manager governance: lockfiles, security scanner, source whitelists, offline/private repo support, Web UI, and multi-agent sync. | More moving parts than simple Codex-only setups; verify installation and platform support. |
| `Tyuts/xiaobai-skills` | Beginner-friendly starter defaults, backup instead of delete, one active default per need, generated inventory. | Curation is mostly hard-coded and Windows/PowerShell oriented. |
| `jscraik/Agent-Skills` | Team control-plane ideas: command handles, audits, evals, proof, runtime projections, closeout gates. | Powerful but heavy; use only the parts that match the team's maturity. |
| `akillness/oh-my-skills` | Broad skill coverage and cross-agent orchestration patterns. | Large catalogs increase trigger overlap; curate before enabling globally. |

## Recommended Hybrid Model

Use a layered approach:

1. **Standard**: use `openai/skills` for layout, metadata, and validation expectations.
2. **Discovery**: use curated catalogs such as `awesome-codex-skills` to find candidates.
3. **Install**: use `vercel-labs/skills` or `skill-installer` for simple installs; use `ask` when lockfiles, security scans, private repos, or multi-agent sync matter.
4. **Curate**: apply the `xiaobai-skills` principle of one active default per need and backup-first conflict handling.
5. **Govern**: borrow `Agent-Skills` concepts for team audits, eval evidence, and closeout proof only when the workflow needs that rigor.
6. **Publish**: sync selected local skills to a GitHub repository with bilingual or operational docs.

## Decision Checklist

Ask these before installing or activating a skill globally:

- Does it solve a need not already covered by an active skill?
- Is the trigger description narrow enough to avoid surprise activation?
- Is the source reputable and maintained enough for the user's risk tolerance?
- Does it require external CLIs, secrets, browsers, paid APIs, or broad shell access?
- Can it be restored or removed cleanly?
- Is this better as a project-local skill instead of global?
- Do we need a lockfile, audit report, or team review before use?

## Suggested Inventory Columns

Use these columns for user-facing reports:

| Skill | Path | Source | Category | Keep/Backup/Remove | Reason | Risk |
|---|---|---|---|---|---|---|

Keep reasons short and operational, such as:

- official system skill
- narrow trigger and useful globally
- duplicate of stronger active skill
- broad workflow framework; keep as fallback
- deprecated or personal scope
- requires unverified external command

## Backup Layout

Use a dated backup root:

```text
skills-backup/
  YYYY-MM-DD-skill-library-manager/
    README.md
    disabled-global-entries/
    disabled-subskills/
    packages/
```

The backup `README.md` should list original path, new path, reason, restore command, and restart reminder.
