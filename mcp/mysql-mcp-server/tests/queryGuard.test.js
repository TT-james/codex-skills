const assert = require('assert');
const {
  enforceSelectQuery,
  normalizeLimit,
  redactRows,
  parseCsv,
  assertSafeIdentifier,
} = require('../src/queryGuard');

function test(name, fn) {
  try {
    fn();
    console.log(`ok - ${name}`);
  } catch (error) {
    console.error(`not ok - ${name}`);
    console.error(error.stack || error.message);
    process.exitCode = 1;
  }
}

test('allows simple select and appends max limit', () => {
  assert.strictEqual(
    enforceSelectQuery('select id, name from ci_customer', { maxRows: 50 }),
    'select id, name from ci_customer LIMIT 50'
  );
});

test('caps large limit', () => {
  assert.strictEqual(
    enforceSelectQuery('SELECT * FROM ci_customer LIMIT 5000', { maxRows: 100 }),
    'SELECT * FROM ci_customer LIMIT 100'
  );
});

test('caps mysql offset count limit form', () => {
  assert.strictEqual(
    enforceSelectQuery('SELECT * FROM ci_customer LIMIT 20, 500', { maxRows: 100 }),
    'SELECT * FROM ci_customer LIMIT 20, 100'
  );
});

test('rejects non-select statements', () => {
  assert.throws(
    () => enforceSelectQuery('update ci_customer set name = "x"', { maxRows: 50 }),
    /Only SELECT/i
  );
});

test('rejects multi statements', () => {
  assert.throws(
    () => enforceSelectQuery('select * from ci_customer; select * from ci_admin', { maxRows: 50 }),
    /Multiple SQL statements/i
  );
});

test('rejects dangerous keywords and comments', () => {
  assert.throws(
    () => enforceSelectQuery('select * from ci_customer into outfile "/tmp/a"', { maxRows: 50 }),
    /Forbidden SQL token/i
  );
  assert.throws(
    () => enforceSelectQuery('select * from ci_customer -- hide', { maxRows: 50 }),
    /SQL comments/i
  );
});

test('normalizes explicit limit with no change when inside max', () => {
  assert.strictEqual(normalizeLimit('select * from ci_customer limit 20', 50), 'select * from ci_customer limit 20');
});

test('redacts sensitive fields in returned rows', () => {
  const rows = redactRows([
    {
      id: 1,
      name: 'Alice',
      password: 'secret',
      mobile: '13800000000',
      id_card: '123456789012345678',
      amount: '88.00',
    },
  ]);

  assert.deepStrictEqual(rows, [
    {
      id: 1,
      name: 'Alice',
      password: '[REDACTED]',
      mobile: '[REDACTED]',
      id_card: '[REDACTED]',
      amount: '88.00',
    },
  ]);
});

test('parses comma separated env values', () => {
  assert.deepStrictEqual(parseCsv('a, b,,c'), ['a', 'b', 'c']);
});

test('validates mysql identifiers', () => {
  assert.strictEqual(assertSafeIdentifier('ci_customer', 'table'), 'ci_customer');
  assert.throws(() => assertSafeIdentifier('ci_customer;drop table x', 'table'), /Invalid table/i);
});

