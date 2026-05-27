---
name: sync-skills-to-github
description: Synchronize locally generated Codex skills to the user's GitHub skills repository, defaulting to TT-james/codex-skills.git. Use when the user asks to upload, publish, back up, mirror, or sync local Codex skills to GitHub, and when they need bilingual Chinese/English documentation describing what each skill does, how to use it, and how to apply or install it in Codex.
---

# Sync Skills to GitHub

## Workflow

Use this skill to publish local Codex skills into a GitHub repository with generated bilingual documentation.

1. Inspect the local skills directory before syncing. Default to `%CODEX_HOME%\skills` when `CODEX_HOME` is set, otherwise use `~/.codex/skills`.
2. Use `scripts/sync_skills_to_github.py` for the actual sync. Prefer a dry run first when the user has not explicitly asked to push immediately.
3. Confirm the generated repository layout:
   - `skills/<skill-name>/` contains copied skill folders.
   - `README.en.md` documents the skills in English.
   - `README.zh-CN.md` documents the skills in Chinese.
   - `README.md` points readers to both language versions.
4. Run a real sync only after checking the dry-run output or when the user explicitly asks to upload/push now.
5. Report the changed skills, documentation files, commit status, and whether the push succeeded.

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

Read `references/documentation-format.md` when changing the generated README structure or wording. Keep generated documentation concise and operational: what the skill does, when to use it, how to invoke it in Codex, and where it lives in the repository.

## Safety

- Preserve the Git repository history. Do not delete the repository checkout unless the user asks.
- The script replaces only the repository `skills/` directory and generated README files.
- If authentication or push fails, leave the local commit/checkouts intact and tell the user the exact next command to retry.
- If the user has uncommitted changes in the target repository, stop and ask before overwriting unless those changes are only generated skill sync outputs from the same script.
