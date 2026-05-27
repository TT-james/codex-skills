# Codex Skills 中文说明

这个仓库用于集中管理和分发可复用的 Codex skills。当前主要收录项目知识图谱相关技能，方便 Codex 在进入新项目、分析代码影响面、编排多 Agent 开发前，先复用已有的项目结构和语义上下文，减少反复全仓检索带来的 token 消耗。

仓库地址:

```text
https://github.com/TT-james/codex-skills
```

## 已包含技能

| 技能名称 | 作用 | 适用场景 |
|---|---|---|
| `project-knowledge-graph` | 融合版项目知识图谱技能，会根据环境选择 CodeGraph、Understand-Anything、双工具混合模式或 `rg` 降级模式。 | 推荐优先安装。适合新项目接入、多 Agent 上下文准备、影响面分析、减少重复检索。 |
| `codegraph-project-knowledge` | 基于 CodeGraph 构建、刷新和查询本地项目代码图谱。 | 适合语义代码搜索、符号定位、调用关系、候选文件筛选、入口点分析。 |
| `understand-anything-project-knowledge` | 基于 Understand-Anything 构建和复用项目知识图谱上下文。 | 适合可视化项目地图、聊天式项目理解、差异解释、团队共享项目认知。 |

## 推荐安装

大多数情况下，优先安装融合版技能:

```text
project-knowledge-graph
```

它会在使用时自动判断当前项目更适合使用 CodeGraph、Understand-Anything、两个工具混合，还是在工具不可用时降级到 `rg --files`、`rg` 和直接读取文件。

## 通过 skill-installer 安装

如果你的 Codex 环境中已有官方 `skill-installer` 技能，可以使用其中的安装脚本从 GitHub 仓库拉取技能。

安装融合版技能:

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

一次安装全部三个技能:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph \
  --path skills/codegraph-project-knowledge \
  --path skills/understand-anything-project-knowledge
```

安装完成后，重启 Codex，让新技能被重新扫描并加载。

## Windows 手动安装

也可以直接克隆仓库，然后复制需要的技能目录到 Codex skills 目录。

```powershell
git clone https://github.com/TT-james/codex-skills.git
Copy-Item -Recurse .\codex-skills\skills\project-knowledge-graph C:\Users\<你的用户名>\.codex\skills\
```

常见 Codex skills 目录:

```text
C:\Users\<你的用户名>\.codex\skills\
```

复制完成后，同样需要重启 Codex。

## macOS / Linux 手动安装

```bash
git clone https://github.com/TT-james/codex-skills.git
cp -r codex-skills/skills/project-knowledge-graph ~/.codex/skills/
```

## 插件包结构

仓库中也提供了一个插件包:

```text
plugins/knowledge-graph-skills/
```

这个插件包一次性包含三个知识图谱技能，并通过根目录的 `marketplace.json` 暴露给支持仓库型插件市场的 Codex 环境。

目录结构:

```text
plugins/
  knowledge-graph-skills/
    .codex-plugin/plugin.json
    skills/
      project-knowledge-graph/
      codegraph-project-knowledge/
      understand-anything-project-knowledge/
```

如果你的 Codex 支持通过插件市场或仓库链接安装插件，可以优先使用这个插件包；如果只是想快速使用某个技能，直接安装 `skills/` 下的单个技能即可。

## 使用方式

在新项目中优先使用融合版技能:

```text
使用 $project-knowledge-graph 检索当前项目，生成可供 Codex 多 Agent 使用的项目知识图谱上下文。
```

需要更精确的代码语义检索和影响面分析时:

```text
使用 $codegraph-project-knowledge 找出这个功能的入口文件、调用链和可能受影响的代码。
```

需要项目地图、解释型上下文或团队共享理解时:

```text
使用 $understand-anything-project-knowledge 为这个仓库生成可视化/聊天式项目知识图谱。
```

## 三个技能如何选择

优先选择 `project-knowledge-graph`。它是融合版，适合作为团队默认技能。

当你只需要语义代码搜索、符号级定位、调用关系和候选文件时，可以单独使用 `codegraph-project-knowledge`。

当你更需要可视化项目结构、自然语言解释、团队分享和非开发同事也能理解的项目地图时，可以单独使用 `understand-anything-project-knowledge`。

## 外部工具说明

这些 skills 不会把 CodeGraph 或 Understand-Anything 工具源码打包进仓库。它们的作用是告诉 Codex 如何发现、调用、复用和降级处理这些工具。

- CodeGraph: https://github.com/colbymchenry/codegraph
- Understand-Anything: https://github.com/Lum1104/Understand-Anything

如果当前机器没有安装对应工具，技能会要求 Codex 记录失败原因，并降级使用 `rg --files`、`rg` 和目标文件直接读取，避免任务中断。

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

marketplace.json
README.md
README.zh-CN.md
```

## 发布前校验

校验单个 skill:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/project-knowledge-graph
```

校验插件包:

```bash
python <plugin-creator-dir>/scripts/validate_plugin.py plugins/knowledge-graph-skills
```

## 后续新增技能的建议流程

1. 在 `skills/<skill-name>/` 下新增标准技能目录，至少包含 `SKILL.md`。
2. 如果希望通过插件包统一分发，同步复制到 `plugins/<plugin-name>/skills/<skill-name>/`。
3. 更新 `README.md` 和 `README.zh-CN.md`，说明技能用途、安装命令和使用示例。
4. 更新 `marketplace.json` 或插件 manifest 中的描述信息。
5. 运行 skill 和 plugin 校验脚本。
6. 提交并推送到 GitHub，其他人即可通过仓库链接安装。
