// Background process: follows the runner's per-step log pages and forwards
// each masked line to the configured sinks until the post step asks it to stop.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const { parseHeaders } = require('./headers');

const pagesDir = process.env.LIVE_LOG_TAP_PAGES;
const workDir = process.env.LIVE_LOG_TAP_WORKDIR;
const startIso = process.env.LIVE_LOG_TAP_START;
const stopFile = path.join(workDir, 'stop');
const command = (process.env.INPUT_COMMAND || '').trim();
const outFile = (process.env.INPUT_FILE || '').trim();
const url = (process.env.INPUT_URL || '').trim();
const batchIntervalMs =
  Number((process.env['INPUT_BATCH-INTERVAL'] || '').trim() || 1) * 1000;

// Page files are named <timelineId>_<recordId>_<page>.log.
const PAGE_RE = /^([0-9a-f-]{36})_([0-9a-f-]{36})_(\d+)\.log$/;
// Runner lines start with an ISO timestamp with 7 fractional digits.
const TS_RE = /^\uFEFF?(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})\d*Z /;

function log(message) {
  console.log(`${new Date().toISOString()} ${message}`);
}

// --- Sinks -----------------------------------------------------------------

const writers = [];
let stopping = false;

// Read by the post step to warn when a sink fails.
const status = { command: null, url: null };

function writeStatus() {
  fs.writeFileSync(path.join(workDir, 'status.json'), JSON.stringify(status));
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

if (outFile) {
  const fd = fs.openSync(outFile, 'a');
  writers.push((lines, text) => fs.writeSync(fd, text));
}

let sinkProc = null;
let sinkExited = false;

if (command) {
  status.command = { linesDropped: 0 };
  sinkProc = spawn(command, {
    shell: true,
    stdio: ['pipe', 'inherit', 'inherit'],
  });
  sinkProc.stdin.on('error', (err) => log(`sink stdin error: ${err.message}`));
  sinkProc.on('exit', (code, signal) => {
    sinkExited = true;
    Object.assign(status.command, { code, signal, early: !stopping });
    log(`sink command exited (code ${code}, signal ${signal})`);
    writeStatus();
  });
  writers.push((lines, text) => {
    if (sinkExited) {
      status.command.linesDropped += lines.length;
    } else {
      sinkProc.stdin.write(text);
    }
  });
}

// --- URL sink: POSTs queued lines in batches, one request at a time ---------

const MAX_BATCH_LINES = 5000;
const POST_ATTEMPTS = 3;
const POST_TIMEOUT_MS = 30 * 1000;
const urlQueue = [];
let urlSending = false;
let urlHeaders = {};

if (url) {
  urlHeaders = parseHeaders(process.env.INPUT_HEADERS || '');
  status.url = { linesSent: 0, linesFailed: 0, lastError: null };
  writers.push((lines) => {
    for (const line of lines) {
      urlQueue.push(line);
    }
  });
  setInterval(sendBatches, batchIntervalMs);
}

async function postBatch(lines) {
  let error = null;
  for (let attempt = 1; attempt <= POST_ATTEMPTS; attempt++) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain; charset=utf-8', ...urlHeaders },
        body: lines.join('\n') + '\n',
        signal: AbortSignal.timeout(POST_TIMEOUT_MS),
      });
      await response.arrayBuffer();
      if (response.ok) {
        status.url.linesSent += lines.length;
        return;
      }
      error = `HTTP ${response.status}`;
      // Other 4xx responses won't succeed on retry.
      if (response.status < 500 && response.status !== 429) {
        break;
      }
    } catch (err) {
      error = err.cause ? `${err.message}: ${err.cause.message}` : err.message;
    }
    if (attempt < POST_ATTEMPTS) {
      await sleep(attempt * 1000);
    }
  }
  status.url.linesFailed += lines.length;
  status.url.lastError = error;
  log(`url: batch of ${lines.length} line(s) failed: ${error}`);
  writeStatus();
}

async function sendBatches() {
  if (urlSending) {
    return;
  }
  urlSending = true;
  try {
    while (urlQueue.length > 0) {
      await postBatch(urlQueue.splice(0, MAX_BATCH_LINES));
    }
  } finally {
    urlSending = false;
  }
}

async function drainUrl() {
  while (urlSending) {
    await sleep(50);
  }
  await sendBatches();
}

let linesForwarded = 0;

function emit(lines) {
  if (lines.length === 0) {
    return;
  }
  const text = lines.join('\n') + '\n';
  for (const write of writers) {
    try {
      write(lines, text);
    } catch (err) {
      log(`sink write error: ${err.message}`);
    }
  }
  linesForwarded += lines.length;
}

// --- Page tracking ---------------------------------------------------------

// Every line is written to both its step's page and the job-level page. Step
// pages are flushed when the step ends, the job page only when the job ends,
// so step pages are forwarded and the job page is used only for lines written
// before the tap started ("Set up job" etc.).
function findJobId() {
  const diagDir = path.dirname(pagesDir);
  const workerLogs = fs
    .readdirSync(diagDir)
    .filter((name) => /^Worker_.*\.log$/.test(name))
    .map((name) => path.join(diagDir, name))
    .sort((a, b) => fs.statSync(b).mtimeMs - fs.statSync(a).mtimeMs);
  if (workerLogs.length === 0) {
    return null;
  }
  const match = /Job ID ([0-9a-f-]{36})/.exec(
    fs.readFileSync(workerLogs[0], 'utf8'),
  );
  return match ? match[1] : null;
}

const seen = new Set();
const ignoredRecords = new Set();
const tracked = new Map();
let filesFollowed = 0;

function track(name, preStartOnly) {
  try {
    const fd = fs.openSync(path.join(pagesDir, name), 'r');
    tracked.set(name, {
      fd,
      pos: 0,
      rest: '',
      preStartOnly,
      preStartDone: false,
      keep: true,
      first: true,
    });
    filesFollowed++;
  } catch (err) {
    log(`could not open ${name}: ${err.message}`);
  }
}

function filterPreStart(page, lines) {
  const kept = [];
  for (const line of lines) {
    const ts = TS_RE.exec(line);
    if (ts) {
      page.keep = `${ts[1]}Z` < startIso;
    }
    if (!page.keep) {
      page.preStartDone = true;
      break;
    }
    kept.push(line);
  }
  return kept;
}

const buffer = Buffer.alloc(64 * 1024);

function readPage(name, page, final) {
  let text = '';
  for (;;) {
    const bytes = fs.readSync(page.fd, buffer, 0, buffer.length, page.pos);
    if (bytes === 0) {
      break;
    }
    page.pos += bytes;
    text += buffer.toString('utf8', 0, bytes);
  }
  if (page.first && text) {
    page.first = false;
    if (text.startsWith('\uFEFF')) {
      text = text.slice(1);
    }
  }
  const lines = (page.rest + text).split('\n');
  page.rest = lines.pop();
  if (final && page.rest) {
    lines.push(page.rest);
    page.rest = '';
  }
  emit(page.preStartOnly ? filterPreStart(page, lines) : lines);
}

function close(name, page) {
  fs.closeSync(page.fd);
  tracked.delete(name);
}

function poll(final) {
  for (const name of fs.readdirSync(pagesDir)) {
    if (seen.has(name)) {
      continue;
    }
    seen.add(name);
    const match = PAGE_RE.exec(name);
    // Rollover pages (_2.log, ...) of the job page or of pre-existing steps.
    if (match && !ignoredRecords.has(match[2])) {
      track(name, false);
    }
  }

  for (const [name, page] of tracked) {
    // Check before reading: the runner flushes and closes a page before
    // deleting it, so a read after a missing check sees everything.
    const gone = !fs.existsSync(path.join(pagesDir, name));
    readPage(name, page, gone || final);
    if (gone || final || page.preStartDone) {
      close(name, page);
    }
  }
}

// --- Main loop -------------------------------------------------------------

const jobId = findJobId();
if (!jobId) {
  log(
    'job ID not found in worker log; lines written before the tap started will be skipped',
  );
}

// Pages that exist now belong to the job, "Set up job", earlier steps, or this
// tap's own step. None are forwarded live; the job page supplies earlier lines.
const preexisting = fs
  .readFileSync(path.join(workDir, 'preexisting'), 'utf8')
  .split('\n')
  .filter(Boolean);
for (const name of preexisting) {
  seen.add(name);
  const match = PAGE_RE.exec(name);
  if (!match) {
    continue;
  }
  ignoredRecords.add(match[2]);
  if (match[2] === jobId && match[3] === '1') {
    track(name, true);
  }
}
log(
  `started; job ID ${jobId || 'unknown'}; ignoring ${ignoredRecords.size} pre-existing record(s)`,
);

const timer = setInterval(() => {
  try {
    if (fs.existsSync(stopFile)) {
      clearInterval(timer);
      poll(true);
      shutdown();
      return;
    }
    poll(false);
  } catch (err) {
    log(`poll error: ${err.stack}`);
  }
}, 100);

async function shutdown() {
  stopping = true;
  if (url) {
    await drainUrl();
  }
  log(
    `stopping; forwarded ${linesForwarded} line(s) from ${filesFollowed} page file(s)`,
  );
  if (status.command) {
    log(`command: ${status.command.linesDropped} line(s) after it exited`);
  }
  if (status.url) {
    log(
      `url: ${status.url.linesSent} line(s) sent, ${status.url.linesFailed} failed`,
    );
  }
  writeStatus();
  if (!sinkProc || sinkExited) {
    process.exit(0);
  }
  sinkProc.on('exit', () => process.exit(0));
  sinkProc.stdin.end();
}
