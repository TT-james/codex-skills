'use strict';

const TOOLS = [
  {
    name: 'list_databases',
    description: 'List MySQL databases allowed by the local read-only policy.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'list_tables',
    description: 'List tables in the allowed database with comments and approximate row counts.',
    inputSchema: {
      type: 'object',
      properties: { database: { type: 'string' } },
      additionalProperties: false,
    },
  },
  {
    name: 'describe_table',
    description: 'Describe columns and indexes for a single allowed table.',
    inputSchema: {
      type: 'object',
      properties: {
        database: { type: 'string' },
        table: { type: 'string' },
      },
      required: ['table'],
      additionalProperties: false,
    },
  },
  {
    name: 'search_tables',
    description: 'Search allowed table names, column names, and column comments.',
    inputSchema: {
      type: 'object',
      properties: {
        database: { type: 'string' },
        keyword: { type: 'string' },
      },
      required: ['keyword'],
      additionalProperties: false,
    },
  },
  {
    name: 'sample_rows',
    description: 'Read a limited sample from one allowed table with sensitive fields redacted.',
    inputSchema: {
      type: 'object',
      properties: {
        table: { type: 'string' },
        limit: { type: 'number' },
      },
      required: ['table'],
      additionalProperties: false,
    },
  },
  {
    name: 'run_select',
    description: 'Run one guarded SELECT query. The server rejects writes, comments, multi-statements, dangerous tokens, and caps LIMIT.',
    inputSchema: {
      type: 'object',
      properties: { sql: { type: 'string' } },
      required: ['sql'],
      additionalProperties: false,
    },
  },
  {
    name: 'explain_query',
    description: 'Run EXPLAIN for one guarded SELECT query.',
    inputSchema: {
      type: 'object',
      properties: { sql: { type: 'string' } },
      required: ['sql'],
      additionalProperties: false,
    },
  },
];

function createToolCaller(db) {
  const handlers = {
    list_databases: (args) => db.listDatabases(args || {}),
    list_tables: (args) => db.listTables(args || {}),
    describe_table: (args) => db.describeTable(args || {}),
    search_tables: (args) => db.searchTables(args || {}),
    sample_rows: (args) => db.sampleRows(args || {}),
    run_select: (args) => db.runSelect(args || {}),
    explain_query: (args) => db.explainQuery(args || {}),
  };

  return function callTool(name, args) {
    if (!handlers[name]) {
      throw new Error(`Unknown tool: ${name}`);
    }
    return handlers[name](args || {});
  };
}

module.exports = {
  TOOLS,
  createToolCaller,
};

