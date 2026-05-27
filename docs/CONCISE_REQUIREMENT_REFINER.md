# Concise Requirement Refiner

`concise-requirement-refiner` turns fuzzy Chinese business requirements, screenshots, chat notes, or rough module ideas into a concise implementation-ready requirement draft.

## What It Does

- Extracts business-critical modules, fields, required flags, input controls, validation rules, approval flows, list filters, operations, and print/export notes.
- Rewrites requirements in the Matrix Cloud concise style: numbered modules, inline field annotations, compact workflow arrows, and directly copyable output.
- Keeps uncertain items as short `待确认` notes instead of expanding them into a heavy PRD.

## How to Use in Codex

Install the skill into your local Codex skills directory:

```bash
python <skill-installer-dir>/scripts/install-skill-from-github.py \
  --repo TT-james/codex-skills \
  --path skills/concise-requirement-refiner
```

Or manually copy:

```text
skills/concise-requirement-refiner -> ~/.codex/skills/concise-requirement-refiner
```

Then invoke it explicitly:

```text
Use $concise-requirement-refiner to整理下面这段需求，输出简洁字段化版本：...
```

Codex can also invoke it implicitly when the user asks to `整理需求`, `完善需求`, `提炼详细需求`, or convert rough Chinese business notes into an implementation-ready requirement.

## Output Style

The skill produces Chinese requirement drafts with this shape:

```text
1、模块名称
字段：字段A（必填，类型/控件，关键规则）、字段B（非必填，类型/控件，关键规则）
审批流：发起人提交 -> 节点A审批 -> 节点B审批

2、模块管理
筛选：字段A（模糊）、字段B（下拉）
字段：列表展示字段1、字段2、字段3
操作：新增、编辑、删除、查看、提交审批、打印/导出
```

## Validation

Validate after installation:

```bash
python <skill-creator-dir>/scripts/quick_validate.py skills/concise-requirement-refiner
```
