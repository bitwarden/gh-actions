# Examples

## Basic Usage

### Retrieve All Threads

```yaml
steps:
  - uses: bitwarden/gh-actions/get-pull-request-threads@main
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      pr_number: ${{ github.event.pull_request.number }}
      repository: ${{ github.repository }}
```

### Conditional on Thread Count

```yaml
steps:
  - id: threads
    uses: bitwarden/gh-actions/get-pull-request-threads@main
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      pr_number: ${{ github.event.pull_request.number }}
      repository: ${{ github.repository }}

  - if: steps.threads.outputs.unresolved_count != '0'
    run: echo "There are ${{ steps.threads.outputs.unresolved_count }} unresolved threads"
```

## Advanced Patterns

### Pre-Review Context for AI Code Review

Retrieve threads before running an AI code review to provide context about existing discussions.

```yaml
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Retrieve existing review threads
        id: threads
        uses: bitwarden/gh-actions/get-pull-request-threads@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}
          output_path: /tmp/existing-threads.json

      - name: Run AI code review
        uses: anthropics/claude-code-action@main
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # The AI can read /tmp/existing-threads.json to avoid duplicate comments
```

### Cross-Repository Thread Retrieving

Retrieve threads from a different repository (requires appropriate token permissions).

```yaml
steps:
  - uses: bitwarden/gh-actions/get-pull-request-threads@main
    with:
      token: ${{ secrets.PAT_TOKEN }}
      pr_number: '123'
      repository: 'other-org/other-repo'
```

## Reusable Workflows

### Thread-Aware Review Workflow

```yaml
# .github/workflows/review-with-context.yml
name: Review with Context
on:
  workflow_call:
    inputs:
      pr_number:
        type: number
        required: true
    secrets:
      ANTHROPIC_API_KEY:
        required: true

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: read
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Get thread context
        id: threads
        uses: bitwarden/gh-actions/get-pull-request-threads@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ inputs.pr_number }}
          repository: ${{ github.repository }}

      - name: Review
        if: steps.threads.outputs.unresolved_count != '0'
        run: |
          echo "Reviewing PR with ${{ steps.threads.outputs.unresolved_count }} unresolved threads"
          # Add your review logic here
```

### Job Outputs for Downstream Jobs

```yaml
jobs:
  fetch-context:
    runs-on: ubuntu-latest
    outputs:
      has_unresolved: ${{ steps.threads.outputs.unresolved_count != '0' }}
    steps:
      - id: threads
        uses: bitwarden/gh-actions/get-pull-request-threads@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}

  process-threads:
    needs: fetch-context
    if: needs.fetch-context.outputs.has_unresolved == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Processing unresolved threads..."
```

## Best Practices

- All threads (resolved and unresolved) are always retrieved to provide full context
- Store output in `/tmp/` to avoid cluttering the workspace
- Use outputs for conditional logic in subsequent steps
- Consider token permissions when retrieving from other repositories
- Use `unresolved_count` output to check for active discussions
