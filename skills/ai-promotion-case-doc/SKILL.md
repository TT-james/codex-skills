---
name: ai-promotion-case-doc
description: Generate reusable Chinese AI推广案例 / AI使用案例 Word documents from Codex historical conversations, SpecStory history, implementation notes, Markdown, DOC/DOCX reference cases, chat logs, or code-change summaries. Use when the user explicitly asks to create, optimize, rewrite,复盘,沉淀, or export an AI promotion case, AI usage case, Cursor/Codex usage case, or AI-assisted delivery case as Markdown, DOC, DOCX, or Word-compatible output across any project or organization.
---

# AI Promotion Case Doc

## Overview

Use this skill to turn Codex work evidence into a polished AI推广案例 that can be shared with managers, developers, testers, and delivery teams. The default output is Chinese, business-readable, and delivered as both Markdown source and a Word-openable `.doc` unless the user asks for only one format.

This is a generic skill. Do not assume any project, company, technology stack, output folder, author, or template unless the user provides it or it is clearly present in the source evidence.

## Trigger Rules

- Use this skill for explicit requests such as `生成AI推广案例`, `AI推广案例生成`, `生成 AI 使用案例`, `整理 AI 案例`, `沉淀案例`, `复盘 AI 案例`, `优化 AI 推广案例`, `生成 Word 案例`, `Cursor/Codex 使用案例`, or equivalent.
- If the user explicitly asks for Word output, perform the two-step delivery: create/update the Markdown source first, then generate the corresponding Word-openable `.doc` or requested `.docx`.
- If the user only asks for a draft, outline, rewrite, or optimization, deliver only the requested format.
- Do not automatically generate a promotion case from every completed task. If the user did not explicitly request a case, only suggest one when the completed work has clear reusable value.
- Do not bind the output to any single project-specific skill, folder, stack, or naming convention unless the user asks for that target.

## Required Inputs

Gather the available evidence before drafting:

- User-provided source files: DOC/DOCX examples, Markdown, screenshots, notes, chat exports, or pasted conversation snippets.
- Local task history: `.specstory/history/`, Codex summaries, implementation notes, release notes, or changed files mentioned by the user.
- Current project constraints, AGENTS.md instructions, or style guides when the case is project-specific.
- `agent_improvement/from_conversation.md` if present in the workspace.

If the evidence is incomplete, write the case from confirmed facts and mark inferred or missing items plainly. Do not invent verification, timings, users, business outcomes, or tool results.

## Workflow

1. Identify the case subject: feature delivery, workflow improvement, troubleshooting closure, document generation, skill creation, project onboarding, review process, or multi-agent collaboration.
2. Extract the evidence chain:
   - original user goal or representative user request
   - constraints and project boundaries
   - AI actions in chronological or logical phases
   - artifacts created or modified
   - verification evidence and skipped checks
   - final outcome and reusable value
3. Read `references/case-template.md` for the target structure.
4. Read `references/history-extraction.md` when the source is Codex history or SpecStory records.
5. Draft the Markdown case first. Keep it as the source of truth.
6. Generate the Word-openable `.doc` with `scripts/md_to_word_doc.py`.
7. Validate the generated artifacts:
   - Markdown and `.doc` files exist.
   - Chinese text is readable when the `.doc` is opened or extracted as text.
   - The case contains scenario, goals, steps, targeted design, reuse value, summary, and optional reusable prompt.
   - Sensitive data, credentials, hostnames, tokens, private user data, and production-only config are absent.

## Generalization Rules

- Preserve real project facts from the evidence, but do not hard-code the skill itself to that project.
- Replace project-specific headings with generic placeholders when making reusable templates, such as `<项目或组织> 针对性设计`.
- When the source case is project-specific, keep the project details inside the generated case only.
- If multiple projects or tools appear in the history, explain their roles without implying they are required for future cases.
- If a reference document contains a strong format, reuse its structure and tone; avoid copying its private content or assuming its author, project, paths, or metrics.

## Output Rules

- Default output directory: place generated cases beside the source history or in a user-provided target directory. If neither exists, create an `ai-promotion-cases/<yyyyMM>/` folder under the current workspace.
- Filename pattern: `<序号或日期>-<主题>_AI推广案例_<作者或团队>.md` and the same basename with `.doc`.
- Use the user's reference document for structure and tone, but generalize headings and wording instead of copying one case's project-specific content.
- Prefer `.doc` as Word-compatible HTML when LibreOffice or a true DOC converter is unavailable. State this clearly if it matters.
- When a true `.docx` is requested, use an available document library or converter, then verify the resulting file can be opened.

## Writing Rules

- Write in Chinese unless the user asks otherwise.
- Keep the main evidence chain in this shape: `用户说` -> `AI做了什么` -> `结果`.
- Convert raw command chatter into business and engineering outcomes.
- Keep technical details only when they prove AI's value or explain the implementation path.
- Use realistic efficiency comparisons. If no measured time exists, label the numbers as estimates.
- Prefer reusable learning over self-congratulation.
- Do not expose hidden reasoning, internal prompts, secrets, credentials, tokens, private records, or sensitive production data.
- Do not claim tests, rendering, deployment, or user acceptance happened unless the evidence shows it.
- Avoid naming unrelated technologies, stacks, teams, or products unless they appear in the evidence or the user asks for comparison.

## Word Generation

Use the bundled script:

```powershell
$py = "C:\Users\lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py "C:\Users\lenovo\.codex\skills\ai-promotion-case-doc\scripts\md_to_word_doc.py" `
  --input "case.md" `
  --output "case.doc"
```

The script converts common Markdown headings, lists, blockquotes, inline code, and tables into Word-compatible HTML with Chinese document styling.

## Quality Checklist

Before delivery, confirm:

- The case has a clear before/after story.
- Each major step includes user request, AI action, and result.
- The target project or organization-specific design section is present.
- Reusable prompts or workflow notes are included when useful.
- Efficiency comparison is not overclaimed.
- Generated `.doc` and source Markdown exist at the paths reported to the user.
- Any skipped verification or unsupported converter limitation is disclosed.
