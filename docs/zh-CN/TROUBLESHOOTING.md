# 排障指南

**语言:** [English](../TROUBLESHOOTING.md) | 简体中文

## Codex 没有识别到技能

检查:

- 技能目录是否位于 `~/.codex/skills/` 或 `C:\Users\<你的用户名>\.codex\skills\`。
- 技能目录根部是否存在 `SKILL.md`。
- 安装后是否重启了 Codex。
- 是否误装成了类似 `skills/project-knowledge-graph/project-knowledge-graph` 的嵌套目录。

## 出现重复技能

通常是同一个技能通过多个路径重复安装。

处理方式:

- 只保留一份。
- GitHub 安装版和插件安装版二选一。
- 清理后重启 Codex。

## CodeGraph 不可用

技能会记录工具缺失，并降级使用 `rg` 和目标文件直接读取。

安装方式请参考上游仓库:

```text
https://github.com/colbymchenry/codegraph
```

## Understand-Anything 不可用

技能会记录工具缺失，并继续使用 CodeGraph 或 fallback 模式。

上游仓库:

```text
https://github.com/Lum1104/Understand-Anything
```

## 图谱上下文过期

以下情况应刷新图谱或标记为 stale:

- 大规模重构。
- 依赖目录移动。
- 路由、命令、入口文件变化。
- 新增核心模块。

真正编辑代码前，仍然必须直接打开目标文件阅读。知识图谱是定位和影响面辅助，不替代源代码事实。
