# Repository Documentation Format

The sync script preserves existing repository documentation by default.

## Hard Rule

Do not rewrite established repository templates. Preserve hand-written README structure, ECC-inspired presentation, badges, language switchers, install sections, docs navigation, screenshots, hero blocks, and wording unless the user explicitly asks to edit those files.

## Missing Files

When root documentation files are missing, the script may create fallback files:

- `README.md`: bilingual entry point linking to English and Chinese documentation.
- `README.en.md`: English usage guide.
- `README.zh-CN.md`: Chinese usage guide.

Fallback files should include:

1. Repository purpose: this repository stores reusable Codex skills.
2. Skill index: skill name, description, and repository path.
3. How to use in Codex: copy or install the skill folder into `~/.codex/skills`, then invoke it by `$skill-name` or by asking for a matching task.
4. How to update: run the sync skill from the local Codex environment.

## Bilingual Skill Documentation

Every published skill must provide both English and Chinese documentation.

- English is required for frontmatter `description` and repository-wide skill tables.
- Chinese is required in the skill body, usually as a Chinese summary, usage notes, or bilingual section.
- If a source skill has only Chinese notes, add an English summary before syncing.
- If a source skill has only English notes, add a Chinese summary before syncing.
- Do not remove project-specific Chinese business terms when adding English; keep both versions side by side when the context matters.

## Marker Blocks

Existing docs are updated only inside this explicit marker pair:

```markdown
<!-- sync-skills:skills:start -->
<!-- sync-skills:skills:end -->
```

The marker block may be placed under an existing heading such as `Included Skills`, `Skill Index`, or `技能索引`. The script replaces only the content from the start marker through the end marker. Everything outside the markers must remain byte-for-byte unchanged.

If no marker block exists, the script must print that the file was preserved and must not edit it.
