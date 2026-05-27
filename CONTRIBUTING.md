# Contributing

**Language:** English | 简体中文

## English

Use this flow when adding or updating a skill:

1. Add the skill under `skills/<skill-name>/`.
2. Keep `SKILL.md` at the skill root.
3. Put reusable commands or probes under `scripts/`.
4. Put long setup notes under `references/`.
5. If the skill should be distributed through the plugin package, mirror it under `plugins/knowledge-graph-skills/skills/<skill-name>/`.
6. Update `README.md`, `README.zh-CN.md`, and the relevant docs under `docs/`.
7. Validate the skill and plugin package before publishing.

Skill validation:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

Plugin validation:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```

## 简体中文

新增或更新技能时，建议遵守这个流程:

1. 在 `skills/<skill-name>/` 下新增技能目录。
2. 技能根目录必须包含 `SKILL.md`。
3. 可复用命令或探测脚本放到 `scripts/`。
4. 较长的安装说明、工具说明、背景资料放到 `references/`。
5. 如果希望通过插件包分发，同步复制到 `plugins/knowledge-graph-skills/skills/<skill-name>/`。
6. 更新 `README.md`、`README.zh-CN.md` 和 `docs/` 下的相关文档。
7. 发布前运行 skill 和 plugin 校验。

校验 skill:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

校验 plugin:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```
