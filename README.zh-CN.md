# Codex 技能整合库

**语言:** [English](README.md) | 简体中文

[![Codex Skills](https://img.shields.io/badge/Codex-Custom%20Skills-2563EB)](https://github.com/TT-james/codex-skills)
[![Skill Hub](https://img.shields.io/badge/Hub-Skills%20%2B%20Docs-16A34A)](skills)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

这是一个 Codex 自定义技能整合库，用于集中沉淀、管理和分发本地生成的可复用技能及说明文档。

仓库只保留清晰的技能主目录：`skills/`。每个技能都自带 `SKILL.md`、参考资料和脚本，避免在根目录堆叠重复的插件包、旧快速开始和过期说明。

## 工作说明

- 每个技能都独立放在 `skills/<skill-name>/`。
- `SKILL.md` 是 Codex 触发技能后读取的入口说明。
- 技能专属长文档放在该技能的 `references/` 目录。
- 可复用脚本放在该技能的 `scripts/` 目录。
- 本地使用时只安装当前任务需要的技能，避免重复扫描和重复触发。

## 快速选择

| 使用场景 | 推荐技能 |
|---|---|
| 进入新项目、理解代码结构、给多 Agent 准备上下文 | `project-knowledge-graph` |
| 基于 Codex 历史会话生成中文 AI 推广案例 Word 文档 | `ai-promotion-case-doc` |
| 审计、整理、去重、发布本地技能库 | `skill-library-manager` |
| 将本地自定义技能同步到 GitHub 仓库 | `sync-skills-to-github` |

## 已包含技能

<!-- sync-skills:skills:start -->
| 技能 | 用途 | 最适合 |
|---|---|---|
| [`project-knowledge-graph`](skills/project-knowledge-graph) | 统一的项目知识图谱编排器，可选择 CodeGraph、Understand-Anything、混合模式或回退。 | 新仓库入职、多智能体规划、影响分析、减少重复扫描。 |
| [`codegraph-project-knowledge`](skills/codegraph-project-knowledge) | 构建、刷新和查询基于 CodeGraph 的本地项目代码图。 | 语义代码搜索、符号、调用者、候选文件、实现入口点、影响分析。 |
| [`understand-anything-project-knowledge`](skills/understand-anything-project-knowledge) | 构建并复用 Understand-Anything 项目知识图谱上下文。 | 可视化项目地图、仪表板/聊天/解释/差异工作流、共享项目理解。 |
| [`skill-library-manager`](skills/skill-library-manager) | 审计、整理、去重、安装、验证和发布 Codex 技能库。 | 技能发现、启用/备份决策、更安全的全局技能栈和团队技能治理。 |
| [`sync-skills-to-github`](skills/sync-skills-to-github) | 将本地 Codex 技能同步到 GitHub，同时保留既定仓库模板格式。 | 发布本地技能到 GitHub，且不破坏 README 排版或手写文档。 |
| [`ai-promotion-case-doc`](skills/ai-promotion-case-doc) | 基于 Codex 工作证据和历史记录生成可复用的中文 AI 推广案例文档。 | AI 应用案例、团队推广材料、交付复盘和面向管理层的 Word 汇报文档。 |
<!-- sync-skills:skills:end -->

## 安装方式

通过 GitHub 安装单个技能：

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/<skill-name>
```

也可以手动复制：

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/<skill-name> ~/.codex/skills/
```

Windows 目标目录通常是：

```text
C:\Users\<你的用户名>\.codex\skills\
```

安装后请重启 Codex，让新技能被重新扫描并加载。

## 使用示例

```text
使用 $project-knowledge-graph 检索当前项目，生成可供 Codex 多 Agent 使用的项目知识图谱上下文。
```

```text
使用 $ai-promotion-case-doc 将这段 Codex 历史会话整理成 AI推广案例 Word 文档。
```

```text
使用 $sync-skills-to-github 将本地 Codex skills 同步到 TT-james/codex-skills。
```

## 仓库结构

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
    references/
    scripts/

CONTRIBUTING.md
LICENSE
README.md
README.zh-CN.md
```

## 发布前校验

校验单个 skill：

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/<skill-name>
```

## 许可证

MIT。可以自由使用、修改和按团队习惯扩展。
