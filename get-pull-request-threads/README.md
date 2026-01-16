# Get Pull Request Threads Action

Retrieve pull request review threads (including resolved) via GraphQL API.

## Features

- Retrieves all inline review threads (including resolved)
- Retrieves general PR comments
- Outputs structured JSON for downstream processing
- Works with any repository

## Inputs

| Input         | Description                                 | Required | Default                    |
| ------------- | ------------------------------------------- | -------- | -------------------------- |
| `token`       | GitHub token with pull-requests: read       | Yes      | -                          |
| `pr_number`   | Pull request number to retrieve threads for | Yes      | -                          |
| `repository`  | Repository in owner/repo format             | No       | `${{ github.repository }}` |
| `output_path` | Path to write the JSON output               | No       | `/tmp/pr-threads.json`     |
| `max_threads` | Maximum number of threads to retrieve       | No       | `100`                      |

## Outputs

| Output             | Description                     |
| ------------------ | ------------------------------- |
| `threads_file`     | Path to the generated JSON file |
| `total_threads`    | Total number of threads found   |
| `unresolved_count` | Number of unresolved threads    |
| `resolved_count`   | Number of resolved threads      |

## Usage Examples

### Basic Usage

```yaml
- uses: bitwarden/gh-actions/get-pull-request-threads@main
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    pr_number: ${{ github.event.pull_request.number }}
```

### Custom Output Path

```yaml
- id: threads
  uses: bitwarden/gh-actions/get-pull-request-threads@main
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    pr_number: ${{ github.event.pull_request.number }}
    output_path: /tmp/review-context.json

- run: cat ${{ steps.threads.outputs.threads_file }}
```

## Output JSON Schema

```json
{
  "pr_number": 123,
  "repository": "owner/repo",
  "retrieved_at": "2025-01-15T10:30:00Z",
  "total_threads": 5,
  "unresolved_count": 2,
  "resolved_count": 3,
  "threads": [
    {
      "id": "PRRT_abc123",
      "path": "src/auth.ts",
      "line": 45,
      "start_line": 40,
      "diff_side": "RIGHT",
      "is_resolved": false,
      "is_outdated": false,
      "comments": [
        {
          "id": "PRRC_xyz789",
          "author": "reviewer",
          "body": "Consider adding error handling here",
          "created_at": "2025-01-14T09:00:00Z"
        }
      ]
    }
  ],
  "general_comments": [
    {
      "author": "reviewer",
      "body": "Overall looks good!",
      "created_at": "2025-01-14T08:00:00Z"
    }
  ]
}
```

## Permissions

Requires `pull-requests: read` permission. The default `GITHUB_TOKEN` works.

```yaml
permissions:
  pull-requests: read
```
