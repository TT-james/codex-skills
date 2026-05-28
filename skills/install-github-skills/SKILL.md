---
name: install-github-skills
description: Install, list, update, or remove Codex skills from a GitHub skills repository, especially TT-james/codex-skills, using vercel-labs/skills (`npx skills`) as the preferred installer and the built-in OpenAI skill-installer as a fallback. Use when the user asks to download, install, sync, refresh, update, uninstall, or verify skills from a GitHub repo into Codex local or project skill directories.
---

# Install GitHub Skills

## Overview

Use this workflow to manage reusable Codex skills from a GitHub repository. Default to `TT-james/codex-skills` when the user does not provide another repository.

Prefer `npx skills` from `vercel-labs/skills` because it can list repository skills, install selected skills, target Codex, and update/remove previously installed skills. Use the built-in `$skill-installer` script only when `npx` or Node.js is unavailable.

## Preflight

Check the runtime before using `npx skills`:

```bash
node -v
npm view skills version engines --json
```

Use `npx skills` only when Node.js is `>=18`. If the current shell uses an older Node.js, tell the user and switch to the fallback installer or ask them to switch Node versions with their normal version manager.

## Decision

- **List available skills**: inspect the repository before installing.
- **Install for this user**: use global install into `~/.codex/skills` so the skill works across projects.
- **Install for this project**: omit `-g` so the skill lands in `./.agents/skills/` and can be committed with the project.
- **Update installed skills**: use `npx skills update`.
- **Remove installed skills**: use `npx skills remove`.
- **Private repository**: prefer an SSH URL such as `git@github.com:OWNER/REPO.git`, and make sure local SSH or GitHub auth is configured.

## Commands

Set these defaults unless the user provides alternatives:

```bash
REPO="TT-james/codex-skills"
AGENT="codex"
```

List repository skills:

```bash
npx skills add TT-james/codex-skills --list
```

If `npx skills ...` prints `command not found: add`, the shell is probably using an old npm/npx runtime or a broken cached shim. Verify `node -v`, clear the npx cache if appropriate, or use the fallback installer.

Install one skill globally for Codex:

```bash
npx skills add TT-james/codex-skills --skill skill-name -a codex -g -y
```

Install all repository skills globally for Codex:

```bash
npx skills add TT-james/codex-skills --skill '*' -a codex -g -y
```

Install one skill into the current project:

```bash
npx skills add TT-james/codex-skills --skill skill-name -a codex -y
```

Update global skills:

```bash
npx skills update -g -y
```

Remove a global Codex skill:

```bash
npx skills remove skill-name -g -a codex -y
```

Use SSH for private repos:

```bash
npx skills add git@github.com:TT-james/codex-skills.git --skill skill-name -a codex -g -y
```

## Repository Layout

Expect a repository layout like:

```text
skills/
  skill-name/
    SKILL.md
    agents/
    references/
    scripts/
```

Each `SKILL.md` must have YAML frontmatter with string `name` and `description` fields.

## Fallback

If `npx skills` cannot run because Node.js is too old, npm is unavailable, or the command shim fails, use the built-in installer script:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/skill-name
```

On Windows, use:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo TT-james/codex-skills `
  --path skills/skill-name
```

## Verification

After installation:

1. Confirm the target directory exists, usually `~/.codex/skills/<skill-name>` for global installs or `.agents/skills/<skill-name>` for project installs.
2. Read the installed `SKILL.md` frontmatter and confirm `name` and `description` are present.
3. Tell the user to restart Codex after installing or updating skills so new metadata is loaded.
