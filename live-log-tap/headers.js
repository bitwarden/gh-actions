// Parses the `headers` input: one `Name: value` per line, blank lines ignored.
// Errors name the line number only, since values often hold secrets.
function parseHeaders(text) {
  const headers = {};
  text.split('\n').forEach((line, index) => {
    if (!line.trim()) {
      return;
    }
    const colon = line.indexOf(':');
    const name = colon > 0 ? line.slice(0, colon).trim() : '';
    if (!/^[!#$%&'*+.^_`|~0-9A-Za-z-]+$/.test(name)) {
      throw new Error(`headers line ${index + 1} is not in "Name: value" form`);
    }
    headers[name] = line.slice(colon + 1).trim();
  });
  return headers;
}

module.exports = { parseHeaders };
