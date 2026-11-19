# Workflow Summary

A composite GitHub Action that standardizes job summary output using `$GITHUB_STEP_SUMMARY`. Provides a consistent, Bitwarden-styled summary displayed at the end of workflow runs.

## Features

- Status header with emoji indicators
- Run metadata (run ID, actor, ref, SHA)
- Job results table with pass/fail status and duration
- Custom markdown content (inline or file-based)
- Collapsible details sections for verbose output

## Inputs

| Name                   | Required | Default       | Description                                                   |
| ---------------------- | -------- | ------------- | ------------------------------------------------------------- |
| `status`               | Yes      | —             | Overall workflow status: `success`, `failure`, or `cancelled` |
| `title`                | No       | Workflow name | Custom title for the summary header                           |
| `description`          | No       | `""`          | Brief description displayed under the title                   |
| `job-results`          | No       | `""`          | JSON string of job results (see format below)                 |
| `custom-markdown`      | No       | `""`          | Arbitrary markdown content to append                          |
| `custom-markdown-file` | No       | `""`          | Path to a file containing markdown to append                  |
| `details-label`        | No       | `"Details"`   | Label for the collapsible details section                     |
| `details-content`      | No       | `""`          | Content for the collapsible details section                   |
| `details-content-file` | No       | `""`          | Path to a file containing details content                     |
| `include-run-metadata` | No       | `"true"`      | Include run ID, actor, ref, SHA in the header                 |

## Outputs

| Name           | Description                        |
| -------------- | ---------------------------------- |
| `summary-path` | Path to the generated summary file |

## Job Results JSON Format

```json
[
  { "name": "Build", "status": "success", "duration": "2m 30s" },
  { "name": "Test", "status": "failure", "duration": "5m 12s" },
  { "name": "Deploy", "status": "skipped", "duration": "-" }
]
```

Supported status values: `success`, `failure`, `cancelled`, `skipped`

## Usage

### Minimal

```yaml
- uses: bitwarden/gh-actions/workflow-summary@main
  with:
    status: success
```

### With Job Results

```yaml
- uses: bitwarden/gh-actions/workflow-summary@main
  with:
    status: failure
    title: 'Release Pipeline'
    description: 'Nightly release build for v2024.1.0'
    job-results: |
      [
        {"name": "Build", "status": "success", "duration": "2m 30s"},
        {"name": "Test", "status": "failure", "duration": "5m 12s"},
        {"name": "Deploy", "status": "skipped", "duration": "-"}
      ]
```

### With Custom Markdown and Details

```yaml
- uses: bitwarden/gh-actions/workflow-summary@main
  with:
    status: success
    custom-markdown: |
      ## Release Notes
      - Added new feature X
      - Fixed bug Y
    details-label: 'Build Logs'
    details-content-file: build-output.log
```

### File-based Content

```yaml
- uses: bitwarden/gh-actions/workflow-summary@main
  with:
    status: success
    custom-markdown-file: build-notes.md
    details-label: 'Test Results'
    details-content-file: test-results.txt
```

### With GitHub Context Variables

GitHub evaluates `${{ }}` expressions before passing values into the action, so any
workflow context variable can be used in the inputs.

```yaml
- uses: bitwarden/gh-actions/workflow-summary@main
  with:
    status: ${{ job.status }}
    description: 'Triggered by ${{ github.event_name }} on ${{ github.ref_name }}'
    custom-markdown: |
      **PR:** #${{ github.event.pull_request.number }}
      **Head SHA:** `${{ github.event.pull_request.head.sha }}`
```
