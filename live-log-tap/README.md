# Live Log Tap

Streams a job's masked log output to a command and/or file while the job is still running, on
GitHub-hosted or self-hosted runners. Lines are forwarded after GitHub masks secrets, so the
destination receives the same text as the GitHub UI.

## Usage

```yaml
steps:
  - name: Stream job logs
    uses: bitwarden/gh-actions/live-log-tap@main
    with:
      command: curl -sS --data-binary @- https://logs.example.com/ingest
      file: ${{ runner.temp }}/job.log
  # ...the rest of the job
```

Put it first. Lines are forwarded exactly as they appear in the downloaded logs: the runner's
timestamp, then the masked line.

## Inputs

| Input           | Required | Description                                                                                                                  |
| --------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `command`       | No       | Shell command that receives lines on stdin for the rest of the job. Its stdout/stderr appear in the post step's diagnostics. |
| `file`          | No       | Path to append lines to.                                                                                                     |
| `drain-timeout` | No       | Seconds the post step waits for the last lines. Default `30`.                                                                |

At least one of `command` or `file` is required.

## How it works

The runner masks each output line and writes it to page files under `<runner>/_diag/pages`, one
set per step plus one for the whole job, before uploading and deleting them. The main step records
which pages already exist and starts a background process that follows every new per-step page,
holding each file open so the runner's delete after upload loses nothing. The post step tells it to
forward what's left and waits up to `drain-timeout` seconds.

## Behavior to know about

- **Latency.** The runner flushes pages in ~4 KB chunks and when a step ends, so chatty steps
  arrive within about a second and quiet steps arrive when they finish. The GitHub UI updates every
  250–500 ms.
- **Masking.** The same as the GitHub UI, gaps included: a value registered with `::add-mask::` is
  only masked from that point on.
- **Earlier steps.** Lines written before the tap started ("Set up job", or steps placed before it)
  come from the job-level page, which is flushed lazily. Anything still unflushed there when the
  job ends is not forwarded.
- **Its own output.** The tap step's header (the `Run ...` group listing its inputs) is forwarded
  with the earlier lines; its own output and its post step are not.
- **Internals.** This relies on the runner's on-disk page layout, which is not a public contract
  and could change in any runner release. Tested on `ubuntu-24.04` with runner 2.337.0.
