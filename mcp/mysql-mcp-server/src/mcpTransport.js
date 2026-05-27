'use strict';

function encodeMessage(message) {
  const body = JSON.stringify(message);
  return `Content-Length: ${Buffer.byteLength(body, 'utf8')}\r\n\r\n${body}`;
}

function writeMessage(message, output) {
  const stream = output || process.stdout;
  stream.write(encodeMessage(message));
}

function createContentLengthParser(onMessage) {
  let buffer = Buffer.alloc(0);

  return function parse(chunk) {
    buffer = Buffer.concat([buffer, chunk]);

    while (buffer.length > 0) {
      const headerEnd = buffer.indexOf('\r\n\r\n');
      if (headerEnd === -1) return;

      const header = buffer.slice(0, headerEnd).toString('utf8');
      const lengthMatch = header.match(/Content-Length:\s*(\d+)/i);
      if (!lengthMatch) {
        throw new Error('Invalid MCP frame: missing Content-Length');
      }

      const bodyLength = Number(lengthMatch[1]);
      const bodyStart = headerEnd + 4;
      const bodyEnd = bodyStart + bodyLength;
      if (buffer.length < bodyEnd) return;

      const body = buffer.slice(bodyStart, bodyEnd).toString('utf8');
      buffer = buffer.slice(bodyEnd);
      onMessage(JSON.parse(body));
    }
  };
}

module.exports = {
  createContentLengthParser,
  encodeMessage,
  writeMessage,
};

