'use strict';

const DEFAULT_SENSITIVE_PATTERNS = [
  /password/i,
  /passwd/i,
  /pwd/i,
  /secret/i,
  /token/i,
  /salt/i,
  /mobile/i,
  /phone/i,
  /tel/i,
  /email/i,
  /id_?card/i,
  /bank/i,
  /account/i,
  /address/i,
];

const FORBIDDEN_SQL_PATTERNS = [
  /\binsert\b/i,
  /\bupdate\b/i,
  /\bdelete\b/i,
  /\bdrop\b/i,
  /\balter\b/i,
  /\bcreate\b/i,
  /\btruncate\b/i,
  /\breplace\b/i,
  /\bgrant\b/i,
  /\brevoke\b/i,
  /\bcall\b/i,
  /\bload\b/i,
  /\bhandler\b/i,
  /\block\b/i,
  /\bunlock\b/i,
  /\bset\b/i,
  /\binto\s+out(?:file|dumpfile)\b/i,
  /\binfile\b/i,
];

function parseCsv(value) {
  if (!value) return [];
  return String(value)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function stripTrailingSemicolons(sql) {
  return sql.replace(/;\s*$/g, '').trim();
}

function rejectComments(sql) {
  if (/--|\/\*|\*\/|(^|\s)#/.test(sql)) {
    throw new Error('SQL comments are not allowed');
  }
}

function rejectMultipleStatements(sql) {
  if (stripTrailingSemicolons(sql).indexOf(';') !== -1) {
    throw new Error('Multiple SQL statements are not allowed');
  }
}

function rejectForbiddenTokens(sql) {
  for (const pattern of FORBIDDEN_SQL_PATTERNS) {
    if (pattern.test(sql)) {
      throw new Error(`Forbidden SQL token matched: ${pattern}`);
    }
  }
}

function normalizeLimit(sql, maxRows) {
  const max = Number(maxRows) > 0 ? Number(maxRows) : 50;
  const limitPattern = /\blimit\s+(\d+)(\s*,\s*(\d+))?\s*$/i;
  const match = sql.match(limitPattern);

  if (!match) {
    return `${sql} LIMIT ${max}`;
  }

  if (match[3] !== undefined) {
    const offset = Number(match[1]);
    const count = Number(match[3]);
    if (count <= max) return sql;
    return sql.replace(limitPattern, `LIMIT ${offset}, ${max}`);
  }

  const count = Number(match[1]);
  if (count <= max) return sql;
  return sql.replace(limitPattern, `LIMIT ${max}`);
}

function enforceSelectQuery(sql, options) {
  const opts = options || {};
  if (typeof sql !== 'string' || !sql.trim()) {
    throw new Error('SQL query is required');
  }

  const normalized = stripTrailingSemicolons(sql);
  rejectComments(normalized);
  rejectMultipleStatements(normalized);

  if (!/^\s*select\b/i.test(normalized)) {
    throw new Error('Only SELECT statements are allowed');
  }

  rejectForbiddenTokens(normalized);

  return normalizeLimit(normalized, opts.maxRows);
}

function assertSafeIdentifier(value, label) {
  const name = String(value || '').trim();
  const kind = label || 'identifier';
  if (!/^[A-Za-z0-9_]+$/.test(name)) {
    throw new Error(`Invalid ${kind}: ${value}`);
  }
  return name;
}

function buildSensitivePatterns(extraNames) {
  const patterns = DEFAULT_SENSITIVE_PATTERNS.slice();
  for (const name of parseCsv(extraNames)) {
    patterns.push(new RegExp(name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'));
  }
  return patterns;
}

function shouldRedactField(field, patterns) {
  return patterns.some((pattern) => pattern.test(field));
}

function redactRows(rows, extraSensitiveFields) {
  const patterns = buildSensitivePatterns(extraSensitiveFields);
  return rows.map((row) => {
    const redacted = {};
    for (const key of Object.keys(row)) {
      redacted[key] = shouldRedactField(key, patterns) ? '[REDACTED]' : row[key];
    }
    return redacted;
  });
}

function extractReferencedTables(sql) {
  const tables = [];
  const pattern = /\b(?:from|join)\s+`?([A-Za-z0-9_]+)`?(?:\.`?([A-Za-z0-9_]+)`?)?/gi;
  let match;
  while ((match = pattern.exec(sql))) {
    tables.push(match[2] || match[1]);
  }
  return tables;
}

function assertTableAccess(tableName, options) {
  const table = assertSafeIdentifier(tableName, 'table');
  const opts = options || {};
  const allowTables = parseCsv(opts.allowTables);
  const denyTables = parseCsv(opts.denyTables);

  if (denyTables.includes(table)) {
    throw new Error(`Table is denied by policy: ${table}`);
  }

  if (allowTables.length > 0 && !allowTables.includes(table)) {
    throw new Error(`Table is not allowed by policy: ${table}`);
  }

  return table;
}

function assertQueryTableAccess(sql, options) {
  const tables = extractReferencedTables(sql);
  for (const table of tables) {
    assertTableAccess(table, options);
  }
  return tables;
}

module.exports = {
  enforceSelectQuery,
  normalizeLimit,
  redactRows,
  parseCsv,
  assertSafeIdentifier,
  assertTableAccess,
  assertQueryTableAccess,
  extractReferencedTables,
};
