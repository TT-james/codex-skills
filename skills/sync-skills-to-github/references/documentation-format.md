# Generated Documentation Format

The sync script generates three root-level documentation files in the target repository:

- `README.md`: bilingual entry point linking to English and Chinese documentation.
- `README.en.md`: English usage guide.
- `README.zh-CN.md`: Chinese usage guide.

Each language file must include:

1. Repository purpose: this repository stores reusable Codex skills.
2. Skill index: skill name, description, and repository path.
3. How to use in Codex: copy or install the skill folder into `~/.codex/skills`, then invoke it by `$skill-name` or by asking for a matching task.
4. How to update: run the sync skill from the local Codex environment.
5. Notes: generated documentation should be reviewed when skills contain private or project-specific information.

Keep wording direct and concise. The generated files are for humans browsing GitHub, not for Codex runtime behavior.
