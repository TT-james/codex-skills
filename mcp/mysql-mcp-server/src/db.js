'use strict';

const mysql = require('mysql2/promise');
const {
  assertSafeIdentifier,
  assertTableAccess,
  assertQueryTableAccess,
  enforceSelectQuery,
  redactRows,
} = require('./queryGuard');

function quoteIdentifier(identifier) {
  return `\`${assertSafeIdentifier(identifier, 'identifier')}\``;
}

function createDatabase(config) {
  let pool;

  function databaseName(input) {
    const db = input || config.database;
    const allowed = config.allowDatabases.length > 0 ? config.allowDatabases : [config.database];
    if (!allowed.includes(db)) {
      throw new Error(`Database is not allowed by policy: ${db}`);
    }
    return assertSafeIdentifier(db, 'database');
  }

  async function getPool() {
    if (!pool) {
      pool = mysql.createPool({
        host: config.host,
        port: config.port,
        user: config.user,
        password: config.password,
        database: config.database,
        waitForConnections: true,
        connectionLimit: 4,
        namedPlaceholders: true,
        connectTimeout: config.connectTimeout,
        multipleStatements: false,
      });
    }
    return pool;
  }

  async function query(sql, params) {
    const activePool = await getPool();
    const [rows] = await activePool.execute(sql, params || []);
    return rows;
  }

  async function listDatabases() {
    const rows = await query('SHOW DATABASES');
    const allowed = config.allowDatabases.length > 0 ? config.allowDatabases : [config.database];
    return rows
      .map((row) => row.Database || row.Database || Object.values(row)[0])
      .filter((db) => allowed.includes(db));
  }

  async function listTables(args) {
    const db = databaseName(args && args.database);
    const rows = await query(
      'SELECT TABLE_NAME AS table_name, TABLE_COMMENT AS table_comment, TABLE_ROWS AS table_rows, ENGINE AS engine FROM information_schema.TABLES WHERE TABLE_SCHEMA = ? ORDER BY TABLE_NAME',
      [db]
    );

    return rows.filter((row) => {
      try {
        assertTableAccess(row.table_name, config);
        return true;
      } catch (error) {
        return false;
      }
    });
  }

  async function describeTable(args) {
    const db = databaseName(args && args.database);
    const table = assertTableAccess(args && args.table, config);
    const columns = await query(
      'SELECT COLUMN_NAME AS column_name, COLUMN_TYPE AS column_type, IS_NULLABLE AS is_nullable, COLUMN_DEFAULT AS column_default, COLUMN_KEY AS column_key, EXTRA AS extra, COLUMN_COMMENT AS column_comment FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? ORDER BY ORDINAL_POSITION',
      [db, table]
    );
    const indexes = await query(
      'SELECT INDEX_NAME AS index_name, NON_UNIQUE AS non_unique, SEQ_IN_INDEX AS seq_in_index, COLUMN_NAME AS column_name, INDEX_TYPE AS index_type FROM information_schema.STATISTICS WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? ORDER BY INDEX_NAME, SEQ_IN_INDEX',
      [db, table]
    );
    return { table, columns, indexes };
  }

  async function searchTables(args) {
    const db = databaseName(args && args.database);
    const keyword = String((args && args.keyword) || '').trim();
    if (!keyword) throw new Error('keyword is required');
    const like = `%${keyword}%`;
    const rows = await query(
      'SELECT TABLE_NAME AS table_name, COLUMN_NAME AS column_name, COLUMN_TYPE AS column_type, COLUMN_COMMENT AS column_comment FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = ? AND (TABLE_NAME LIKE ? OR COLUMN_NAME LIKE ? OR COLUMN_COMMENT LIKE ?) ORDER BY TABLE_NAME, ORDINAL_POSITION LIMIT 200',
      [db, like, like, like]
    );
    return rows.filter((row) => {
      try {
        assertTableAccess(row.table_name, config);
        return true;
      } catch (error) {
        return false;
      }
    });
  }

  async function sampleRows(args) {
    const table = assertTableAccess(args && args.table, config);
    const limit = Math.min(Number((args && args.limit) || config.maxRows), config.maxRows);
    const sql = `SELECT * FROM ${quoteIdentifier(table)} LIMIT ${limit > 0 ? limit : config.maxRows}`;
    const rows = await query(sql);
    return redactRows(rows, config.extraSensitiveFields);
  }

  async function runSelect(args) {
    const guarded = enforceSelectQuery(args && args.sql, { maxRows: config.maxRows });
    assertQueryTableAccess(guarded, config);
    const rows = await query(guarded);
    return {
      sql: guarded,
      rows: redactRows(rows, config.extraSensitiveFields),
    };
  }

  async function explainQuery(args) {
    const guarded = enforceSelectQuery(args && args.sql, { maxRows: config.maxRows });
    assertQueryTableAccess(guarded, config);
    return {
      sql: guarded,
      plan: await query(`EXPLAIN ${guarded}`),
    };
  }

  async function close() {
    if (pool) {
      await pool.end();
      pool = null;
    }
  }

  return {
    listDatabases,
    listTables,
    describeTable,
    searchTables,
    sampleRows,
    runSelect,
    explainQuery,
    close,
  };
}

module.exports = {
  createDatabase,
};

