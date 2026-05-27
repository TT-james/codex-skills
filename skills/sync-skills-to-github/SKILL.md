---
name: sync-skills-to-github
description: Synchronize locally generated Codex skills to the user's GitHub skills repository, defaulting to TT-james/codex-skills.git. Use when the user asks to upload, publish, back up, mirror, or sync local Codex skills to GitHub, preserve an existing repository README/template, update only marked skill-index blocks, or maintain bilingual Chinese/English skill documentation without disturbing established repository formatting.
---

# Sync Skills to GitHub

## Workflow

Use this skill to publish local Codex skills into a GitHub repository while preserving the repository's established README/template format.

1. Inspect the local skills directory before syncing. Default to `%CODEX_HOME%\skills` when `CODEX_HOME` is set, otherwise use `~/.codex/skills`.
2. Use `scripts/sync_skills_to_github.py` for the actual sync. Prefer a dry run first when the user has not explicitly asked to push immediately.
3. Confirm the repository layout:
   - `skills/<skill-name>/` contains copied skill folders.
   - Existing root documentation is preserved by default.
   - `README.md`, `README.en.md`, and `README.zh-CN.md` are created only when missing.
   - Existing documentation is updated only inside explicit sync marker blocks.
4. Run a real sync only after checking the dry-run output or when the user explicitly asks to upload/push now.
5. Report changed skills, preserved documentation files, updated marker blocks, commit status, and whether the push succeeded.

## Default Repository

Default repository URL:

```text
https://github.com/TT-james/codex-skills.git
```

Default local checkout:

```text
~/.codex/synced-skill-repos/codex-skills
```

Do not include `~/.codex/skills/.system` unless the user explicitly requests system skills.

## Commands

Dry run:

```powershell
python "C:\Users\lenovo\.codex\skills\sync-skills-to-github\scripts\sync_skills_to_github.py" --dry-run
```

Validate this skill against the original requirements:

```powershell
python "C:\Users\lenovo\.codex\skills\sync-skills-to-github\scripts\validate_skill_requirements.py"
```

Sync, commit, and push:

```powershell
python "C:\Users\lenovo\.codex\skills\sync-skills-to-github\scripts\sync_skills_to_github.py"
```

Sync without pushing:

```powershell
python "C:\Users\lenovo\.codex\skills\sync-skills-to-github\scripts\sync_skills_to_github.py" --no-push
```

Use a custom repository or checkout:

```powershell
python "C:\Users\lenovo\.codex\skills\sync-skills-to-github\scripts\sync_skills_to_github.py" --repo-url "https://github.com/OWNER/REPO.git" --repo-dir "D:\path\to\repo"
```

## Documentation

Read `references/documentation-format.md` when changing documentation behavior. The hard rule is template preservation: do not rewrite established repository introductions, badges, language switchers, install sections, ECC-style layout, or hand-written docs.

To let the script update a skill index inside an existing README, add this marker pair exactly where the generated table should live:

```markdown
<!-- sync-skills:skills:start -->
<!-- sync-skills:skills:end -->
```

If a README has no marker pair, the script must leave it unchanged and only sync `skills/`.

## Safety

- Preserve the Git repository history. Do not delete the repository checkout unless the user asks.
- The script replaces only the repository `skills/` directory by default.
- The script must not rewrite existing README/template files unless they contain explicit sync markers.
- If authentication or push fails, leave the local commit/checkouts intact and tell the user the exact next command to retry.
- If the user has uncommitted changes in the target repository outside `skills/`, stop before overwriting.
