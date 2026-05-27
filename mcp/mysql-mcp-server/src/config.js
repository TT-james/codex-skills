'use strict';

require('dotenv').config();

const { parseCsv } = require('./queryGuard');

function numberFromEnv(name, fallback) {
  const value = Number(process.env[name]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function loadConfig() {
  return {
    host: process.env.MYSQL_HOST || '127.0.0.1',
    port: numberFromEnv('MYSQL_PORT', 3306),
    database: process.env.MYSQL_DATABASE || '',
    user: process.env.MYSQL_USER || '',
    password: process.env.MYSQL_PASSWORD || '',
    maxRows: numberFromEnv('MYSQL_MAX_ROWS', 50),
    connectTimeout: numberFromEnv('MYSQL_CONNECT_TIMEOUT_MS', 10000),
    allowDatabases: parseCsv(process.env.MYSQL_ALLOW_DATABASES),
    allowTables: parseCsv(process.env.MYSQL_ALLOW_TABLES),
    denyTables: parseCsv(process.env.MYSQL_DENY_TABLES),
    extraSensitiveFields: process.env.MYSQL_EXTRA_SENSITIVE_FIELDS || '',
  };
}

function assertConfig(config) {
  const missing = [];
  if (!config.database) missing.push('MYSQL_DATABASE');
  if (!config.user) missing.push('MYSQL_USER');
  if (!config.password) missing.push('MYSQL_PASSWORD');
  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
}

module.exports = {
  loadConfig,
  assertConfig,
};

