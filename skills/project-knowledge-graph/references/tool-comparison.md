# CodeGraph vs Understand-Anything

## Summary

| Dimension | CodeGraph | Understand-Anything | Hybrid Recommendation |
|---|---|---|---|
| Best at | Code-level semantic search, symbols, impact, callers | Visual project map, chat/explain/diff, onboarding | Use CodeGraph for precision, Understand-Anything for shared map |
| Main artifact | `.codegraph/` local index/database | `.understand-anything/knowledge-graph.json` | Keep both local, pass only summaries |
| Interaction | CLI/MCP-style commands such as status/context/search/impact | Slash commands such as `/understand`, dashboard, chat, explain, diff | One shared orientation, then narrow follow-up queries |
| Token value | Reduces broad file scans with targeted context | Reduces repeated architecture rediscovery | Main agent summarizes once for subagents |
| Strength | Precise implementation entry points and change impact | Human/agent-friendly overview and visual exploration | Combine for Standard/Strict tasks |
| Risk | May be less useful for high-level visual onboarding if only CLI output is available | May be less precise than direct semantic symbol/impact queries | Confirm with direct file reads before editing |

## Use CodeGraph First

Use CodeGraph when the request asks:

- Where is this feature implemented?
- Which symbol/class/method/table is involved?
- What files are impacted by this change?
- Which callers or dependencies should be reviewed?
- Which exact files should a developer open before editing?

## Use Understand-Anything First

Use Understand-Anything when the request asks:

- Explain this unfamiliar repository.
- Generate or inspect a project knowledge graph.
- Show a visual architecture map or dashboard.
- Let agents chat with the codebase or explain a module.
- Review changed code through graph-aware diff workflow.

## Use Hybrid Mode

Use both tools when:

- The repository is unfamiliar and the task is multi-file or cross-module.
- Planning, development, testing, and review are split across agents.
- The change touches finance, permissions, queues, SQL, external interfaces, performance, or security.
- Architecture-level understanding and precise code impact are both needed.

Hybrid sequence:

1. Probe current graph readiness.
2. Use Understand-Anything for broad module map and dashboard/chat findings.
3. Use CodeGraph for candidate files, symbols, callers, and impact.
4. Merge findings into one handoff.
5. Ask subagents to use narrow graph queries only when the shared handoff is insufficient.

## Fallback Mode

If either tool is unavailable:

1. Record missing command/artifact and any error.
2. Use the available graph tool if one exists.
3. If neither exists, use `rg --files`, `rg`, and direct file reads.
4. State that graph context is unavailable or partial.
