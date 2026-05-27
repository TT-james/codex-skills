---
name: skill-library-manager
description: Manage Codex and agent skill libraries by combining the best ideas from open skill ecosystems. Use when the user asks to audit installed skills, discover better skills on GitHub, choose active vs backup skills, deduplicate broad workflow skills, compare skill managers such as openai/skills, vercel-labs/skills, ComposioHQ/awesome-codex-skills, yeasy/ask, Agent-Skills, oh-my-skills, xiaobai-skills, install or update skill sets, create a skills inventory, publish skills to a GitHub skills repository, or design a team-ready skill governance workflow.
---

# Skill Library Manager

Manage skills as a small governed library, not a loose folder dump. Favor official sources for standards, package managers for installation and updates, curated catalogs for discovery, backup-first curation for safety, and repository sync for sharing.

## First Move

Classify the request before acting:

- **Discover**: find candidate skills, compare repositories, or recommend a starter stack.
- **Inventory**: inspect installed skills and summarize names, paths, descriptions, source packages, and likely overlaps.
- **Curate**: choose active defaults, move alternatives to backup, or plan restore points.
- **Install/update/remove**: use a package manager or repo-specific installer.
- **Validate**: check metadata, trigger breadth, dangerous instructions, duplicate responsibilities, and broken references.
- **Publish**: sync local skills to a GitHub skills repository with useful docs.

If the user did not request writes, stay read-only and produce a recommendation. If writes are requested, prefer dry-run or backup-first operations before changing active skill folders.

## Source Strategy

Use the strongest project for the job:

- `openai/skills`: official standard, system skills, examples, and validation expectations.
- `vercel-labs/skills`: practical CLI-style install, list, find, update, remove, multi-agent targeting, and symlink/copy decisions.
- `ComposioHQ/awesome-codex-skills`: discovery catalog for candidate skills and categories.
- `yeasy/ask`: package-manager ideas such as lockfiles, security scanning, offline/private repo support, Web UI, and multi-agent sync.
- `Tyuts/xiaobai-skills`: beginner-safe defaults, one active default per need, inventory writing, and backup instead of deletion.
- `jscraik/Agent-Skills`: team governance, command handles, audits, eval evidence, runtime projections, and closeout proof.
- `akillness/oh-my-skills` or similar large catalogs: broad coverage, but require stricter trigger and overlap review before global install.

For current facts about external repositories, search GitHub or the web before making claims about stars, maintenance, latest commands, or active branches.

For a compact comparison table and decision checklist, read `references/project-patterns.md`.

## Inventory Workflow

Inspect likely skill roots, adapting paths to the user environment:

```powershell
$roots = @(
  "$env:USERPROFILE\.codex\skills",
  "$env:USERPROFILE\.agents\skills",
  "$env:USERPROFILE\.claude\skills"
)
foreach ($root in $roots) {
  if (Test-Path -LiteralPath $root) {
    Get-ChildItem -LiteralPath $root -Recurse -Filter SKILL.md -File
  }
}
```

For each `SKILL.md`, capture:

- `name`, path, and first-line purpose from frontmatter.
- likely source repository or package root.
- category: discovery, creation, frontend, image/media, docs/content, engineering workflow, planning, debugging, review, release, security, browser automation, project-specific, or broad framework.
- risk flags: overbroad trigger, destructive shell guidance, secret handling, external service dependency, deprecated/in-progress/personal scope, duplicate responsibility, missing license, or stale references.

Summarize with a small table first, then details only where they affect action.

## Curation Rules

Keep the active library small:

1. Prefer official/system skills when they fully cover the need.
2. Prefer narrow, concrete skills over broad workflow frameworks for global activation.
3. Keep only one broad engineering/process framework globally unless the user explicitly wants more.
4. Keep high-risk, experimental, deprecated, personal, or overlapping skills in backup.
5. Back up before moving or replacing. Do not delete by default.
6. Preserve restore notes, including original path, backup path, reason, and restart reminder.

Recommended minimum global stack:

- official system skills for image generation, OpenAI docs, plugin creation, skill creation, and skill installation.
- one discovery mechanism: `skill-installer`, `vercel-labs/skills`, `find-skills`, or a catalog-backed equivalent.
- one frontend/design lane if the user builds UI often.
- one engineering workflow lane, chosen by preference: official/project-specific workflow, Matt Pocock-style engineering skills, Superpowers-style strict methodology, or team-specific lifecycle skills.
- one publish/sync lane when the user maintains a shared skills repository.

## Install And Update

Prefer mature package-manager flows when available:

```powershell
# Discover/list from a repository
npx skills add owner/repo --list

# Install selected skills globally for Codex
npx skills add owner/repo --skill skill-name -g -a codex -y

# List or update installed skills
npx skills list -g
npx skills update -g -y
```

Use repo-provided scripts only after reading them enough to understand:

- target directories
- overwrite behavior
- network downloads
- backup/restore behavior
- dependency assumptions
- whether dry-run exists

If `ask` is installed and appropriate, consider it for version locking, security checks, offline/private repo support, and multi-agent sync. If it is not installed, do not require it for simple Codex-only tasks.

## Validation

For each skill being added or kept active, check:

- frontmatter has only valid `name` and `description` unless the local standard allows more.
- `description` clearly says what the skill does and when to use it.
- trigger scope is not so broad that it fires on most coding tasks.
- `SKILL.md` stays concise and links optional details through `references/`.
- scripts are deterministic enough to justify being bundled and have been test-run when changed.
- dangerous operations require explicit user intent and backups.
- external tools, API keys, or MCP dependencies are disclosed.

When creating or updating a skill, use `$skill-creator` conventions and run the available validation script, for example:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "path\to\skill"
```

## Publish Workflow

When the user asks to publish, back up, upload, or sync skills to GitHub:

1. Inspect the local skill folder and target repository status.
2. Exclude `.system` skills unless the user explicitly asks for them.
3. Prefer the existing sync skill or script if present.
4. Dry-run first unless the user explicitly asked to push now.
5. Confirm generated layout includes `skills/<skill-name>/` and useful README files.
6. Commit with a clear message and push.
7. Report changed skills, validation result, commit hash, push result, and any retry command if auth fails.

If the target repository has unrelated uncommitted changes, stop and ask before overwriting generated outputs.

## Output Shape

For analysis tasks, return:

- verdict: use, avoid, backup, or investigate
- comparison table
- recommended active stack
- backup candidates
- exact next commands, if action is requested

For write tasks, return:

- files changed
- validation commands and results
- git commit/push status
- restart reminder if skills were installed, moved, or updated
