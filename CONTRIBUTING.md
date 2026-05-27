# Contributing

**Language:** English | 简体中文

## English

Use this flow when adding or updating a skill:

1. Add or update the skill under `skills/<skill-name>/`.
2. Keep `SKILL.md` at the skill root.
3. Put reusable scripts under `scripts/`.
4. Put long-form references under `references/`.
5. Keep root README files concise. Skill-specific detail belongs inside the skill folder.
6. Validate the skill before publishing.

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

## 简体中文

新增或更新技能时，建议遵守这个流程：

1. 在 `skills/<skill-name>/` 下新增或更新技能。
2. 技能根目录必须包含 `SKILL.md`。
3. 可复用脚本放到 `scripts/`。
4. 较长的说明、背景资料和模板放到 `references/`。
5. 根目录 README 保持简洁，技能专属细节放回技能目录。
6. 发布前运行技能校验。

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```
