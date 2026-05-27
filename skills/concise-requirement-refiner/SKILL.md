---
name: concise-requirement-refiner
description: >-
  Extract key information from fuzzy Chinese business requirements, screenshots, chat notes, or rough module ideas, then rewrite them into a concise field-focused requirement draft using the Matrix Cloud style: numbered modules, inline field notes in parentheses, approval flow, management list, filters, operations, and print/export notes. Use when the user asks to 整理需求, 完善需求, 提炼详细需求, 按刚才模板整理, or turn vague requirement text into a clear implementation-ready requirement.
---

# Concise Requirement Refiner

## Goal

Turn vague requirement material into a concise final requirement draft that resembles the project's business-demand notes, not a heavy PRD.

Prefer this shape:

```text
部门/角色 - 功能需求
1、模块名称
字段：字段A（必填，类型/控件，关键规则）、字段B（非必填，类型/控件，关键规则）

审批流/处理流程：发起人提交 -> 节点A审批（规则）-> 节点B审批（人员/角色）

2、模块管理（列表、详情、打印/导出）
筛选：字段A（模糊）、字段B（下拉）、日期字段（起止）
字段：列表展示字段1、字段2、字段3
操作：新增、编辑（状态限制）、删除（状态限制）、查看、提交审批、打印/导出（条件）
```

## Workflow

1. Extract only business-critical facts from the user's fuzzy input:
   - 功能模块
   - 字段名称
   - 必填/非必填
   - 输入方式：文本、日期、下拉、字典、多选、附件、系统生成、系统带出
   - 关键校验：不得早于当前日期、若无填“无”、金额大小写、编号规则、状态限制
   - 流程节点、审批人、部门/角色规则
   - 管理页筛选项、列表字段、操作项
   - 打印、导出、归档、附件等输出要求

2. Put important notes inside field parentheses instead of separate long explanations.

3. Keep output short and implementation-oriented:
   - Use numbered sections.
   - Use inline lists separated by Chinese commas.
   - Avoid tables unless the user explicitly asks for tables.
   - Avoid long background,目标、权限矩阵、验收标准 unless required.

4. Preserve uncertain information as concise assumptions:
   - If the fuzzy input implies a value, write it directly.
   - If a required detail is absent but can be safely defaulted, add a short default in parentheses.
   - If the missing detail affects implementation heavily, add `待确认：...` at the end, limited to 3 items.

## Field Annotation Rules

Use this order inside parentheses:

```text
字段名称（必填/非必填，类型或控件，选项/规则/来源）
```

Common examples:

- `申请单编号（系统自动生成，开头BHSQ-）`
- `保函介质（必填，下拉选择，电子保函/纸质保函）`
- `受益人（必填，文本输入）`
- `保函金额（必填，金额输入，大小写，可根据小写自动生成大写）`
- `到期日期（必填，日期选择，不得早于当前日期）`
- `附件（非必填，支持上传合同/标书/相关材料）`
- `审批状态（系统带出，草稿/审批中/已通过/已驳回/已撤回）`

## Output Rules

- Match the user's language. For Matrix Cloud business requests, output Chinese.
- Keep the final result directly copyable into a requirement document.
- Do not mention the skill or internal analysis in the final requirement draft.
- Do not over-design database tables, APIs, tests, or permission matrices unless the user asks.
- If the user says “最终版”, output only the polished requirement content plus at most a short note about unresolved confirmations.

## Quality Check

Before finalizing, verify:

- Every module has fields or operations.
- Every field with business impact has parentheses for type/rule/source.
- Approval or workflow is written as arrows when present.
- Management requirements include at least filters, list fields, and operations when applicable.
- Print/export requirements state trigger condition and data source when applicable.
