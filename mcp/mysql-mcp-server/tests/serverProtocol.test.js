const assert = require('assert');
const { createServer } = require('../src/server');
const { createContentLengthParser, encodeMessage } = require('../src/mcpTransport');
const { TOOLS, createToolCaller } = require('../src/tools');

async function test(name, fn) {
  try {
    await fn();
    console.log(`ok - ${name}`);
  } catch (error) {
    console.error(`not ok - ${name}`);
    console.error(error.stack || error.message);
    process.exitCode = 1;
  }
}

function withCapturedStdout(fn) {
  const chunks = [];
  const originalWrite = process.stdout.write;
  process.stdout.write = (chunk) => {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(String(chunk)));
    return true;
  };

  try {
    fn();
  } finally {
    process.stdout.write = originalWrite;
  }

  return Buffer.concat(chunks).toString('utf8');
}

function parseFrame(frame) {
  const parts = frame.split('\r\n\r\n');
  assert.strictEqual(parts.length, 2);
  return JSON.parse(parts[1]);
}

test('declares expected MCP tools', () => {
  assert.deepStrictEqual(
    TOOLS.map((tool) => tool.name),
    ['list_databases', 'list_tables', 'describe_table', 'search_tables', 'sample_rows', 'run_select', 'explain_query']
  );
});

test('responds to initialize with tools capability', () => {
  const server = createServer({});
  const output = withCapturedStdout(() => {
    server.handle({ jsonrpc: '2.0', id: 1, method: 'initialize', params: {} });
  });
  const response = parseFrame(output);
  assert.strictEqual(response.result.serverInfo.name, 'mysql-mcp-server');
  assert.deepStrictEqual(response.result.capabilities, { tools: {} });
  assert.match(response.result.instructions, /read-only MySQL/i);
});

test('content-length parser accepts one complete frame', () => {
  const messages = [];
  const parse = createContentLengthParser((message) => messages.push(message));
  const body = JSON.stringify({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
  parse(Buffer.from(`Content-Length: ${Buffer.byteLength(body)}\r\n\r\n${body}`));
  assert.deepStrictEqual(messages, [{ jsonrpc: '2.0', id: 2, method: 'tools/list' }]);
});

test('encodes one MCP frame with content length', () => {
  const frame = encodeMessage({ jsonrpc: '2.0', id: 3, result: { ok: true } });
  const parsed = parseFrame(frame);
  assert.deepStrictEqual(parsed, { jsonrpc: '2.0', id: 3, result: { ok: true } });
});

test('tool caller dispatches database methods', async () => {
  const calls = [];
  const db = {
    listDatabases: async (args) => {
      calls.push(['listDatabases', args]);
      return ['demo'];
    },
  };
  const callTool = createToolCaller(db);
  assert.deepStrictEqual(await callTool('list_databases', { ok: true }), ['demo']);
  assert.deepStrictEqual(calls, [['listDatabases', { ok: true }]]);
  assert.throws(() => callTool('missing_tool', {}), /Unknown tool/);
});
