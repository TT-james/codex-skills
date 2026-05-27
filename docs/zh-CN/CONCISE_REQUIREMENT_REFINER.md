# 简洁需求整理技能

`concise-requirement-refiner` 用于把模糊中文业务需求、截图内容、聊天记录、粗略模块想法整理成可开发的简洁字段化需求稿。

## 技能用途

- 提取功能模块、字段、必填规则、控件类型、校验规则、审批流程、列表筛选、操作项、打印/导出等关键信息。
- 按 Matrix Cloud 常用需求风格输出：编号模块、字段括号内说明、审批流箭头、管理列表、筛选项、操作项。
- 对缺失但影响实现的信息，用简短 `待确认` 记录，不展开成冗长 PRD。

## 如何应用到 Codex

通过 GitHub skill installer 安装：

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/concise-requirement-refiner
```

也可以手动复制：

```text
skills/concise-requirement-refiner -> ~/.codex/skills/concise-requirement-refiner
```

安装后可显式调用：

```text
使用 $concise-requirement-refiner 整理下面这段需求，输出简洁字段化版本：...
```

当用户提出“整理需求”“完善需求”“提炼详细需求”“按刚才模板整理”等请求时，Codex 也可以按技能描述自动触发。

## 输出格式

典型输出如下：

```text
1、模块名称
字段：字段A（必填，类型/控件，关键规则）、字段B（非必填，类型/控件，关键规则）
审批流：发起人提交 -> 节点A审批 -> 节点B审批

2、模块管理
筛选：字段A（模糊）、字段B（下拉）
字段：列表展示字段1、字段2、字段3
操作：新增、编辑、删除、查看、提交审批、打印/导出
```

## 校验方式

安装后可执行：

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/concise-requirement-refiner
```
