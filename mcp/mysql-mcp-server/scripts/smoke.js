#!/usr/bin/env node
'use strict';

const { loadConfig, assertConfig } = require('../src/config');
const { createDatabase } = require('../src/db');

async function main() {
  const config = loadConfig();
  assertConfig(config);
  const db = createDatabase(config);

  try {
    const databases = await db.listDatabases();
    const tables = await db.listTables({ database: config.database });
    console.log(JSON.stringify({
      ok: true,
      databases,
      tableCount: tables.length,
      firstTables: tables.slice(0, 5).map((table) => table.table_name),
    }, null, 2));
  } finally {
    await db.close();
  }
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});

