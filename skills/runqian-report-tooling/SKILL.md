---
name: runqian-report-tooling
description: Work with Runqian/Raqsoft `.rpx` report templates in this Matrix Cloud workspace. Use when Codex needs to open or inspect a Runqian report, extract every dataset SQL, print SQL with runtime parameters substituted, change dataset SQL or data source names, migrate report SQL from the internal system source to `matrix_cloud`, fix report SQL Chinese mojibake, validate SQL against the Runqian data source, or create a new report by copying and adapting an existing `.rpx`.
---

# Runqian Report Tooling

## 中文说明

本技能用于处理 Matrix Cloud 项目中的润乾 / Raqsoft `.rpx` 报表模板，适用于打开和检查报表、抽取所有数据集 SQL、按运行参数打印可对比 SQL、替换数据源和表字段、修复中文乱码、校验报表 SQL，以及通过复制旧报表生成新报表。

处理润乾报表时优先使用本技能内的脚本和润乾 Java API。不要直接编辑 RPX 二进制文件；修改前必须备份，修改后必须回读检查数据集、数据源、参数数量、分组字段和中文显示。

## Scope

Use this skill for Runqian/Raqsoft report files such as:

- `*.rpx` report templates under `D:/Users/lenovo/Desktop/JZ/润乾报表/...`
- matrix_cloud report templates under `report/`
- exported report comparison files when the task is to trace dataset SQL or grouping differences

For SQL/data checks, also use `matrix-sql-data-change` and `matrix-mysql-readonly`.

## Golden Rules

- Never edit RPX binaries directly. Use the Runqian Java API.
- Always back up the target `.rpx` before writing changes.
- Keep report SQL structure as close as possible to the source report unless the user explicitly approves logic changes.
- When migrating internal-system reports to Matrix Cloud, replace table and field names first; do not silently remove joins, change grouping, or rewrite subtotal logic.
- For monthly expense reports, preserve `GROUP BY t.stype` when the internal-system SQL uses that grouping.
- Avoid Chinese literals in RPX SQL when prior saves produced mojibake. Prefer MySQL UTF-8 hex constants such as `CONVERT(0xE58685E983A8 USING utf8mb4)`.
- Do not print database passwords or Runqian datasource credentials.

## Core Workflow

1. Read required project context:
   - `.codex/agent_improvement/from_conversation.md`
   - relevant project SQL/report skills and rules
2. Inspect both the source and target report:
   - dataset names
   - data source names
   - raw SQL
3. Compare before changing:
   - dataset count and names
   - table references
   - grouping keys
   - subtotal outer queries
   - parameter count/order
4. Generate SQL files per dataset when changing SQL.
5. Validate generated SQL with prepared parameters against the intended Runqian datasource.
6. Back up the RPX.
7. Write the SQL/data source through the Runqian API.
8. Read the RPX back and verify:
   - all intended datasets changed
   - data source names are correct
   - no unexpected old tables remain
   - no mojibake markers such as `??`, `�`, or known garbled text remain
   - required grouping such as `GROUP BY t.stype` remains when required
9. Update `.specstory/history/` for the task.

## Reusable Script

Use `scripts/runqian_dataset.ps1` for repeated RPX operations.

Inspect a report:

```powershell
powershell -ExecutionPolicy Bypass -File .codex\skills\runqian-report-tooling\scripts\runqian_dataset.ps1 `
  -Mode inspect `
  -ReportPath "D:\path\to\report.rpx" `
  -OutPath "outputs\report_sql\report.inspect.txt"
```

Update a report from one SQL file per dataset:

```powershell
powershell -ExecutionPolicy Bypass -File .codex\skills\runqian-report-tooling\scripts\runqian_dataset.ps1 `
  -Mode update `
  -ReportPath "D:\path\to\report.rpx" `
  -SqlDir "runtime\report-sql"
```

Print parameter-expanded SQL:

```powershell
powershell -ExecutionPolicy Bypass -File .codex\skills\runqian-report-tooling\scripts\runqian_dataset.ps1 `
  -Mode expand `
  -ReportPath "D:\path\to\report.rpx" `
  -OutPath "outputs\report_sql\report_202604_sql_expanded.md" `
  -StartDate "2026-04-01 00:00:00" `
  -EndDate "2026-04-30 23:59:59" `
  -StartYear "2026-01-01 00:00:00" `
  -EndYear "2026-04-30 23:59:59" `
  -MineCode ""
```

The script assumes the standard local Runqian install paths used in this workspace:

- `D:/Program Files/raqsoft/report/classes`
- `D:/Program Files/raqsoft/report/lib/*`
- `D:/Program Files/raqsoft/report/web/webapps/demo/WEB-INF/lib/*`
- `D:/Program Files/raqsoft/common/jdbc/*`

## Monthly Expense Report Mapping Notes

When migrating `jzypaymentExpensesReport.rpx` to `matrixPaymentExpensesReport.rpx`, keep internal-system SQL shape and apply these approved mappings:

- `bxd` -> `ci_bxd`
- `bxditem` -> `ci_bxd_item`
- `sys_office` and `ci_ding_dept_office_rel` -> `ci_department`
- `b.office_id` -> `ci_bxd.user_dept_id`
- `sys_office.management_center_id` -> `ci_department.management_center_id`
- `management_center_department` -> `ci_management_center_department`
- `sys_user` -> `ci_user`
- `sys_user.dinguserid` -> `ci_user.ding_user_id`
- `jzy_travel_allowance_info` -> `ci_travel_allowance_info`
- `project` / `project_extend` -> `ci_project`
- `ci_project.project_no = ci_travel_allowance_info.project_no`
- `before_sale_project` -> `ci_before_sale_project`
- `ci_fbt_corporate_payments_order` -> `ci_fbt_corporate_payments`

Important domain fact:

- In the internal system, `sys_office` is the department table and `ci_ding_dept_office_rel` maps DingTalk `dept_id`.
- In Matrix Cloud, `ci_department` is the department table and `ci_department.id` is the DingTalk department id.

## Chinese Literal Safety

Use hex constants for Chinese literals that must survive RPX save/load:

- `内部`: `CONVERT(0xE58685E983A8 USING utf8mb4)`
- `公司内部`: `CONVERT(0xE585ACE58FB8E58685E983A8 USING utf8mb4)`
- `山东矩阵软件工程股份有限公司`: `CONVERT(0xE5B1B1E4B89CE79FA9E998B5E8BDAFE4BBB6E5B7A5E7A88BE882A1E4BBBDE69C89E99990E585ACE58FB8 USING utf8mb4)`
- `山东人机协和智能科技有限公司`: `CONVERT(0xE5B1B1E4B89CE4BABAE69CBAE58D8FE5928CE699BAE883BDE7A791E68A80E69C89E99990E585ACE58FB8 USING utf8mb4)`

When printing SQL for human comparison, create a readable Markdown copy that replaces known mojibake text with the intended Chinese, without changing RPX files unless the user asks.

## Validation Checklist

- RPX readback works after save.
- Dataset count and names match the source report.
- Parameter counts match expected report runtime parameters.
- SQL executes as prepared SELECT with representative parameters.
- Report-specific grouping is preserved.
- No secrets are printed.
- A backup path is reported in the final response when the RPX is changed.
