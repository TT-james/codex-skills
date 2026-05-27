# Codex历史会话提取规范

Use this reference when the source is a Codex conversation, SpecStory record, implementation transcript, or chat log.

## Extraction Order

1. Find the user's goal. Preserve the original request when short; otherwise paraphrase faithfully.
2. Find constraints: output format, project stack, forbidden content, file paths, naming rules, approval gates, validation requirements.
3. Group AI actions into 4-7 readable phases. Combine repeated searches, retries, and minor corrections.
4. Record artifacts: generated files, changed files, skills, scripts, proposals, tests, screenshots, release notes, or documentation.
5. Record verification: commands run, lint or syntax checks, render checks, generated file existence, and any skipped checks.
6. Record reusable learning: templates, scripts, prompts, skill improvements, workflow rules, or team practices.
7. Mark gaps honestly. Use `未验证` or `未执行` when evidence is absent.

## Noise Filtering

Omit:

- Repeated progress messages.
- Tool call mechanics that do not affect the result.
- Failed commands that were immediately replaced and have no user-facing impact.
- Hidden reasoning, internal prompt details, or speculative paths not used in final delivery.

Keep:

- User requirements and changes in direction.
- Constraints that shaped the output.
- Important code, document, or workflow artifacts.
- Verification evidence and limitations.
- Encoding, conversion, or file-format issues that affected the generated Word document.

## Suggested Step Names

- 步骤1：明确案例主题与输出格式
- 步骤2：读取历史会话与参考案例
- 步骤3：提炼用户诉求、AI动作和结果链路
- 步骤4：补充项目针对性设计与复用价值
- 步骤5：生成 Markdown 案例源文档
- 步骤6：生成 Word 文档并检查格式
- 步骤7：沉淀可复用提示词或技能

## Efficiency Comparison

Prefer ranges and estimates:

| 方式 | 耗时 | 说明 |
|---|---|---|
| 传统整理 | 约 0.5-1 天 | 需要人工回看聊天记录、归纳结构、校对口径 |
| AI辅助 | 约 1-2 小时 | AI 负责提取证据链、统一结构、生成文档，人负责确认事实 |

If no measured data exists, write `按同类工作经验估算`.
