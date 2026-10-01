const fs = require('fs');
const path = require('path');

function input(name) {
  return (process.env[`INPUT_${name.toUpperCase()}`] || '').trim();
}

function isAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const workDir = process.env.STATE_workdir;
  const pid = Number(process.env.STATE_pid);
  if (!workDir || !pid) {
    console.log(
      'live-log-tap: main step did not start the tap; nothing to drain',
    );
    return;
  }

  fs.writeFileSync(path.join(workDir, 'stop'), '');

  const deadline = Date.now() + Number(input('drain-timeout') || 30) * 1000;
  while (isAlive(pid) && Date.now() < deadline) {
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  if (isAlive(pid)) {
    console.log(
      '::warning::live-log-tap: drain timed out; the last lines may not have been forwarded',
    );
    process.kill(pid);
  }

  const statusFile = path.join(workDir, 'sink-status.json');
  if (fs.existsSync(statusFile)) {
    const { code, signal, early, linesDropped } = JSON.parse(
      fs.readFileSync(statusFile, 'utf8'),
    );
    const exit = signal ? `signal ${signal}` : `code ${code}`;
    if (early) {
      console.log(
        `::warning::live-log-tap: the command exited (${exit}) before the job ended; ${linesDropped} line(s) after that were not sent to it`,
      );
    } else if (code !== 0) {
      console.log(`::warning::live-log-tap: the command exited with ${exit}`);
    }
  }

  console.log('::group::live-log-tap diagnostics');
  console.log(fs.readFileSync(path.join(workDir, 'tap.log'), 'utf8'));
  console.log('::endgroup::');
}

main();
