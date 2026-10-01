const { spawn } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { parseHeaders } = require('./headers');

function input(name) {
  return (process.env[`INPUT_${name.toUpperCase()}`] || '').trim();
}

function saveState(key, value) {
  fs.appendFileSync(process.env.GITHUB_STATE, `${key}=${value}\n`);
}

function fail(message) {
  console.log(`::error::live-log-tap: ${message}`);
  process.exit(1);
}

if (!input('command') && !input('file') && !input('url')) {
  fail('set at least one of `command`, `file`, or `url`');
}

if (input('url')) {
  let url;
  try {
    url = new URL(input('url'));
  } catch {
    fail('`url` is not a valid URL');
  }
  if (url.protocol !== 'https:' && url.protocol !== 'http:') {
    fail('`url` must be http or https');
  }
  try {
    parseHeaders(process.env.INPUT_HEADERS || '');
  } catch (err) {
    fail(err.message);
  }
  const interval = Number(input('batch-interval') || 1);
  if (!(interval > 0)) {
    fail('`batch-interval` must be a positive number of seconds');
  }
}

// JS actions run on <runner root>/externals/nodeXX/bin/node.
const runnerRoot = path.resolve(process.execPath, '..', '..', '..', '..');
const pagesDir = path.join(runnerRoot, '_diag', 'pages');
if (!fs.existsSync(pagesDir)) {
  console.log(
    `::error::live-log-tap: runner log pages not found at ${pagesDir}`,
  );
  process.exit(1);
}

const workDir = path.join(
  process.env.RUNNER_TEMP,
  `live-log-tap-${crypto.randomBytes(4).toString('hex')}`,
);
fs.mkdirSync(workDir, { recursive: true });
const tapLog = fs.openSync(path.join(workDir, 'tap.log'), 'a');

// List existing pages here rather than in tap.js: the next step can start (and
// create its page) before the background process gets going.
fs.writeFileSync(
  path.join(workDir, 'preexisting'),
  fs.readdirSync(pagesDir).join('\n'),
);

const child = spawn(process.execPath, [path.join(__dirname, 'tap.js')], {
  detached: true,
  stdio: ['ignore', tapLog, tapLog],
  env: {
    ...process.env,
    LIVE_LOG_TAP_PAGES: pagesDir,
    LIVE_LOG_TAP_WORKDIR: workDir,
    LIVE_LOG_TAP_START: new Date().toISOString(),
  },
});
child.unref();

saveState('workdir', workDir);
saveState('pid', child.pid);
console.log(`live-log-tap: following ${pagesDir} (pid ${child.pid})`);
