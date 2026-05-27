#!/usr/bin/env node
'use strict';

const { loadConfig, assertConfig } = require('./config');
const { createDatabase } = require('./db');
const { createContentLengthParser, writeMessage } = require('./mcpTransport');
const { TOOLS, createToolCaller } = require('./tools');

function makeTextResult(value) {
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(value, null, 2),
      },
    ],
  };
}

function makeErrorResult(error) {
  return {
    isError: true,
    content: [
      {
        type: 'text',
        text: error && error.message ? error.message : String(error),
      },
    ],
  };
}

function createServer(db) {
  const callTool = createToolCaller(db);

  async function handle(request) {
    if (!request || typeof request !== 'object') return;
    if (request.method && request.method.startsWith('notifications/')) return;

    try {
      if (request.method === 'initialize') {
        writeMessage({
          jsonrpc: '2.0',
          id: request.id,
          result: {
            protocolVersion: '2024-11-05',
            capabilities: { tools: {} },
            serverInfo: { name: 'mysql-mcp-server', version: '0.1.0' },
            instructions:
              'Use this server for read-only MySQL inspection only. Prefer schema tools before sample data, keep queries narrow, and never request write or DDL operations.',
          },
        });
        return;
      }

      if (request.method === 'tools/list') {
        writeMessage({ jsonrpc: '2.0', id: request.id, result: { tools: TOOLS } });
        return;
      }

      if (request.method === 'tools/call') {
        const params = request.params || {};
        const result = await callTool(params.name, params.arguments || {});
        writeMessage({ jsonrpc: '2.0', id: request.id, result: makeTextResult(result) });
        return;
      }

      writeMessage({
        jsonrpc: '2.0',
        id: request.id,
        error: { code: -32601, message: `Method not found: ${request.method}` },
      });
    } catch (error) {
      writeMessage({ jsonrpc: '2.0', id: request.id, result: makeErrorResult(error) });
    }
  }

  return { handle };
}

async function main() {
  const config = loadConfig();
  assertConfig(config);
  const db = createDatabase(config);
  const server = createServer(db);
  const parse = createContentLengthParser((message) => {
    server.handle(message).catch((error) => {
      console.error(error.stack || error.message);
    });
  });

  process.stdin.on('data', parse);
  process.on('SIGINT', async () => {
    await db.close();
    process.exit(0);
  });
  process.on('SIGTERM', async () => {
    await db.close();
    process.exit(0);
  });
}

if (require.main === module) {
  main().catch((error) => {
    console.error(error.stack || error.message);
    process.exit(1);
  });
}

module.exports = {
  createServer,
};
