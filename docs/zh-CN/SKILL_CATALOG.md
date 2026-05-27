# 技能目录

**语言:** [English](../SKILL_CATALOG.md) | 简体中文

## 选择建议

| 需求 | 推荐技能 |
|---|---|
| 新项目快速理解 | `project-knowledge-graph` |
| 多 Agent 共享上下文 | `project-knowledge-graph` |
| 语义代码搜索和调用关系 | `codegraph-project-knowledge` |
| 从文件或符号分析影响面 | `codegraph-project-knowledge` |
| 可视化项目地图或仪表盘 | `understand-anything-project-knowledge` |
| 聊天式解释、差异解释、团队共享理解 | `understand-anything-project-knowledge` |
| 高风险跨模块任务 | `project-knowledge-graph` 混合模式 |

## 技能说明

### project-knowledge-graph

统一入口技能。它会判断使用 CodeGraph、Understand-Anything、两个工具混合，还是降级到普通仓库检索。

适合:

- 进入陌生仓库。
- 分派子 Agent 前先生成一份共享上下文。
- 同时需要代码语义影响面和架构层理解。
- 希望减少反复全仓扫描。

### codegraph-project-knowledge

CodeGraph 专用流程，用于本地代码图谱探测、语义搜索、符号/调用关系查询和影响面分析。

适合:

- 实现类任务。
- 需要入口点、调用方、候选文件或符号级上下文。
- 希望先得到低 token 的聚焦上下文，再打开文件。

### understand-anything-project-knowledge

Understand-Anything 专用流程，用于可视化/聊天式项目地图和持久化仓库理解。

适合:

- 宽范围项目导览。
- 仪表盘、聊天、解释、diff 工作流。
- 团队共享项目结构理解。

## 团队默认策略

建议团队默认使用 `project-knowledge-graph`。另外两个单工具技能作为精确工具入口保留，方便在需要时直接调用。
