# Codex Skills 中文说明

**语言:** [English](README.md) | 简体中文

[![Codex Skills](https://img.shields.io/badge/Codex-Skills-2563EB)](https://github.com/TT-james/codex-skills)
[![Knowledge Graph](https://img.shields.io/badge/Focus-Knowledge%20Graph-16A34A)](skills/project-knowledge-graph)
[![Plugin Ready](https://img.shields.io/badge/Plugin-Ready-7C3AED)](plugins/knowledge-graph-skills)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

这个仓库用于集中管理和分发可复用的 Codex skills。当前重点是项目知识图谱技能：让 Codex 在进入新项目、分析代码影响面、编排多 Agent 开发前，先复用已有项目结构和语义上下文，减少反复全仓检索带来的 token 消耗。

---

## 快速选择

大多数人只需要安装融合版技能:

```text
project-knowledge-graph
```

它会根据当前环境和任务自动选择 CodeGraph、Understand-Anything、双工具混合模式，或在工具不可用时降级到 `rg --files`、`rg` 和目标文件直接读取。

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

安装后请重启 Codex，让新技能被重新扫描并加载。

> 重要提醒：只选择一种安装方式。通过 GitHub skill-installer、手动复制、插件包三者选其一即可。不要重复叠加安装同一个技能，避免 Codex 扫描到重复副本。

---

## 已包含技能

| 技能名称 | 作用 | 适用场景 |
|---|---|---|
| [`project-knowledge-graph`](skills/project-knowledge-graph) | 融合版项目知识图谱技能，会根据环境选择 CodeGraph、Understand-Anything、双工具混合模式或 `rg` 降级模式。 | 推荐优先安装。适合新项目接入、多 Agent 上下文准备、影响面分析、减少重复检索。 |
| [`codegraph-project-knowledge`](skills/codegraph-project-knowledge) | 基于 CodeGraph 构建、刷新和查询本地项目代码图谱。 | 适合语义代码搜索、符号定位、调用关系、候选文件筛选、入口点分析。 |
| [`understand-anything-project-knowledge`](skills/understand-anything-project-knowledge) | 基于 Understand-Anything 构建和复用项目知识图谱上下文。 | 适合可视化项目地图、聊天式项目理解、差异解释、团队共享项目认知。 |

---

## 安装方式

### 方式一：通过 GitHub 安装单个技能

安装融合版:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

安装 CodeGraph 单工具版:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/codegraph-project-knowledge
```

安装 Understand-Anything 单工具版:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/understand-anything-project-knowledge
```

### 方式二：Windows 手动复制

```powershell
git clone https://github.com/TT-james/codex-skills.git
Copy-Item -Recurse .\codex-skills\skills\project-knowledge-graph C:\Users\<你的用户名>\.codex\skills\
```

常见 Codex skills 目录:

```text
C:\Users\<你的用户名>\.codex\skills\
```

### 方式三：macOS / Linux 手动复制

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/project-knowledge-graph ~/.codex/skills/
```

### 方式四：插件包

仓库中提供了一个插件包:

```text
plugins/knowledge-graph-skills/
```

它一次性包含三个知识图谱技能，并通过根目录的 `marketplace.json` 暴露给支持仓库型插件市场的 Codex 环境。

---

## 使用示例

新项目优先使用融合版:

```text
使用 $project-knowledge-graph 检索当前项目，生成可供 Codex 多 Agent 使用的项目知识图谱上下文。
```

需要更精确的代码语义检索和影响面分析:

```text
使用 $codegraph-project-knowledge 找出这个功能的入口文件、调用链和可能受影响的代码。
```

需要项目地图、解释型上下文或团队共享理解:

```text
使用 $understand-anything-project-knowledge 为这个仓库生成可视化/聊天式项目知识图谱。
```

---

## Codex 多 Agent 接入方式

建议主 Agent 在分派子 Agent 前先运行一次知识图谱技能，然后把同一份精简上下文传给规划、开发、测试、评审和发布文档角色。

```markdown
Project knowledge graph context:
- Project root:
- Tool path: CodeGraph / Understand-Anything / Hybrid / Fallback
- Graph status:
- Relevant modules:
- Entry points:
- Candidate files:
- Symbol/caller/impact findings:
- Visual/chat/dashboard findings:
- Exclusions/blind spots:
- Staleness:
- Required verification:
```

| 角色 | 如何使用知识图谱 |
|---|---|
| Planner | 把图谱结果转成模块边界、任务依赖、执行顺序和待确认问题。 |
| Developer | 先打开图谱给出的候选文件，再进行代码修改。 |
| Tester | 根据入口点、数据流和影响文件设计冒烟和回归验证。 |
| Reviewer | 用语义影响面和依赖路径复核 diff 是否遗漏风险。 |
| Release writer | 记录图谱新鲜度、降级分析、验证证据和残余风险。 |

---

## 三个技能如何选择

优先选择 `project-knowledge-graph`。它是融合版，适合作为团队默认技能。

当你只需要语义代码搜索、符号级定位、调用关系和候选文件时，可以单独使用 `codegraph-project-knowledge`。

当你更需要可视化项目结构、自然语言解释、团队分享和非开发同事也能理解的项目地图时，可以单独使用 `understand-anything-project-knowledge`。

---

## 外部工具说明

这些 skills 不会把 CodeGraph 或 Understand-Anything 工具源码打包进仓库。它们的作用是告诉 Codex 如何发现、调用、复用和降级处理这些工具。

- CodeGraph: https://github.com/colbymchenry/codegraph
- Understand-Anything: https://github.com/Lum1104/Understand-Anything

如果当前机器没有安装对应工具，技能会要求 Codex 记录失败原因，并降级使用 `rg --files`、`rg` 和目标文件直接读取，避免任务中断。

---

## 文档导航

| 文档 | 说明 |
|---|---|
| [中文快速开始](docs/zh-CN/QUICKSTART.md) | 安装、重启、首次使用。 |
| [中文技能目录](docs/zh-CN/SKILL_CATALOG.md) | 三个技能的能力对比和选择建议。 |
| [中文排障指南](docs/zh-CN/TROUBLESHOOTING.md) | 常见安装、加载、工具不可用问题。 |
| [英文 Quick Start](docs/QUICKSTART.md) | 英文快速开始。 |
| [英文 Skill Catalog](docs/SKILL_CATALOG.md) | 英文技能目录。 |
| [贡献说明](CONTRIBUTING.md) | 后续新增或更新技能的标准流程。 |

---

## 仓库结构

```text
skills/
  project-knowledge-graph/
  codegraph-project-knowledge/
  understand-anything-project-knowledge/

plugins/
  knowledge-graph-skills/
    .codex-plugin/plugin.json
    skills/

docs/
  QUICKSTART.md
  SKILL_CATALOG.md
  TROUBLESHOOTING.md
  zh-CN/

marketplace.json
README.md
README.zh-CN.md
```

---

## 发布前校验

校验单个 skill:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/project-knowledge-graph
```

校验插件包:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```

---

## 许可证

MIT。可以自由使用、修改和按团队习惯扩展。
