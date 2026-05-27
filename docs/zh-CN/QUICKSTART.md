# 快速开始

**语言:** [English](../QUICKSTART.md) | 简体中文

## 1. 选择一种安装方式

三种方式选一种即可:

- 推荐：从 GitHub 安装 `skills/project-knowledge-graph`。
- 手动：复制某个技能目录到本地 Codex skills 目录。
- 插件：如果 Codex 环境支持仓库型插件，安装 `plugins/knowledge-graph-skills`。

不要重复叠加安装同一个技能，避免 Codex 扫描到多个重复副本。

## 2. 安装推荐技能

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/project-knowledge-graph
```

安装后重启 Codex。

## 3. 在项目中使用

对 Codex 说:

```text
使用 $project-knowledge-graph 检索当前项目，生成可供 Codex 多 Agent 使用的项目知识图谱上下文。
```

技能会执行这些动作:

- 探测 CodeGraph 或 Understand-Anything 是否可用。
- 如果已有图谱产物，优先复用。
- 工具不可用时，降级到 `rg` 和目标文件直接读取。
- 输出一份精简项目上下文，供规划、开发、测试、评审和发布说明复用。

## 4. 保持图谱新鲜

以下情况需要刷新或标记图谱上下文过期:

- 大规模重构。
- 依赖目录变化。
- 入口文件、路由、命令、数据流变化。
- 新增或删除核心模块。
