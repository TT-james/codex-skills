# mysql-mcp-server

Generic read-only MySQL MCP server for Codex App, Codex CLI, and other MCP clients.

It lets an MCP client inspect database structure and small, capped samples without giving it write access.

This package is only the MCP server. Put project-specific prompting rules in your Codex skills or project instructions, not in this server package.

## What It Exposes

- `list_databases`
- `list_tables`
- `describe_table`
- `search_tables`
- `sample_rows`
- `run_select`
- `explain_query`

## Safety Model

- Use a dedicated MySQL user with `SELECT` and `SHOW VIEW` only.
- `run_select` accepts only one `SELECT` statement.
- Multi-statements, SQL comments, write keywords, DDL keywords, `INTO OUTFILE`, and similar risky tokens are rejected.
- Queries are capped by `MYSQL_MAX_ROWS`.
- Sensitive-looking fields are redacted in row output.
- Access can be narrowed with `MYSQL_ALLOW_DATABASES`, `MYSQL_ALLOW_TABLES`, and `MYSQL_DENY_TABLES`.

## Install

```powershell
cd D:\path\to\mysql-mcp-server
npm install
npm test
```

The package is Node 14 compatible. Newer Node versions are also fine.

To verify a real database connection with environment variables configured:

```powershell
npm run smoke
```

## Create A Read-Only MySQL User

Replace `your_database` and password values:

```sql
CREATE USER 'codex_reader'@'127.0.0.1' IDENTIFIED BY 'your-strong-password';
GRANT SELECT, SHOW VIEW ON your_database.* TO 'codex_reader'@'127.0.0.1';
FLUSH PRIVILEGES;
```

## Connect To Codex App

Codex reads MCP configuration from `~/.codex/config.toml`. Project-level `.codex/config.toml` can also be used for trusted workspaces, but user-level config is better for a reusable local service.

On Windows, user-level config is usually:

```text
C:\Users\<you>\.codex\config.toml
```

Add:

```toml
[mcp_servers.mysql_mcp_server]
command = "node"
args = ["D:/path/to/mysql-mcp-server/src/server.js"]
enabled = true
startup_timeout_sec = 20
tool_timeout_sec = 60
default_tools_approval_mode = "prompt"

[mcp_servers.mysql_mcp_server.env]
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "your_database"
MYSQL_USER = "codex_reader"
MYSQL_PASSWORD = "replace-with-local-readonly-password"
MYSQL_MAX_ROWS = "50"
MYSQL_DENY_TABLES = "users,admins,salaries"
```

Restart Codex App after editing the config. In Codex CLI/TUI, use `/mcp` to inspect connected MCP servers when available.

If the package is later published to npm, users can configure it like this instead of using a local path:

```toml
[mcp_servers.mysql_mcp_server]
command = "npx"
args = ["-y", "mysql-mcp-server"]
enabled = true
startup_timeout_sec = 20
tool_timeout_sec = 60
default_tools_approval_mode = "prompt"

[mcp_servers.mysql_mcp_server.env]
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "your_database"
MYSQL_USER = "codex_reader"
MYSQL_PASSWORD = "replace-with-local-readonly-password"
MYSQL_MAX_ROWS = "50"
```

## Share With Other People

Share this folder as a Git repository, ZIP package, or internal tools bundle. Each user should:

1. Install Node.js.
2. Run `npm install`.
3. Create their own read-only MySQL account.
4. Copy `codex-config.example.toml` into their own `~/.codex/config.toml`.
5. Replace path, database, username, password, and table policy values.
6. Restart Codex App.

Do not share real `.env` files or database passwords.

## Package Contents

- `src/server.js` - MCP request handling and process startup.
- `src/tools.js` - tool definitions and tool-to-database dispatch.
- `src/mcpTransport.js` - STDIO Content-Length frame encoding and parsing.
- `src/db.js` - MySQL read-only operations.
- `src/queryGuard.js` - SQL guardrails, table policy, limit capping, and redaction.
- `src/config.js` - environment-based configuration.
- `tests/` - protocol and SQL guard tests.

## Optional Local `.env`

You can also copy `.env.example` to `.env` for local command-line testing. `.env` is ignored by git.
