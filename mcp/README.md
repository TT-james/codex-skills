# MCP Servers

This directory contains reusable Model Context Protocol servers.

Unlike `skills/`, which contains Codex runtime instructions, `mcp/` contains executable tool servers that can be bound in `~/.codex/config.toml`.

## Included Servers

| Server | Purpose |
|---|---|
| [`mysql-mcp-server`](mysql-mcp-server) | Read-only MySQL schema and data inspection for Codex and other MCP clients. |

## Layout

```text
mcp/
  <server-name>/
    package.json
    src/
    tests/
    README.md
```

Keep credentials out of this repository. Use local environment variables, local `.env` files, or Codex user-level config for secrets.

