# Enforce PR Labels

Reusable workflow that blocks PRs with specific labels from being merged. Currently configured to prevent merging PRs marked with the `hold` label, providing a simple mechanism to pause merges when needed.

## Key Features

- **Automatic blocking**: PRs with the `hold` label cannot be merged
- **Clear feedback**: Displays error message in GitHub Actions step summary
- **Zero configuration**: No inputs or secrets required for basic usage
- **Fail-safe behavior**: Workflow fails explicitly (exit 1) to prevent accidental merges

## How To Use It

### Setup

1. Ensure the `hold` label exists in your repository
2. Copy the `enforce-labels.yml` workflow template into your repository's `.github/workflows/` directory

### Usage

See [enforce-labels.yml](./enforce-labels.yml) template for a calling workflow.

```yaml
jobs:
  enforce-labels:
    uses: bitwarden/gh-actions/.github/workflows/_enforce-labels.yml@main
    permissions: {}
```

### Workflow Behavior

When a PR has the `hold` label:

1. The workflow job runs
2. Fails with exit code 1
3. Displays error message: "PRs with the hold label cannot be merged"
4. Adds error to GitHub step summary

When a PR does not have the `hold` label:

1. The workflow job is skipped (due to conditional check)
2. No action taken

## Requirements

- The `hold` label must exist in your repository
- No secrets or special permissions required

### GitHub Permissions

This workflow requires no special permissions. It can run with:

| Permission | Access | Reason                           |
| ---------- | ------ | -------------------------------- |
| None       | None   | Only checks GitHub event context |

## Use Cases

- **Hold for review**: Block merging while awaiting additional review or approval
- **Hold for dependencies**: Prevent merging until dependent PRs are merged first
- **Hold for testing**: Keep PR open for extended testing before merge
- **Hold for coordination**: Synchronize merges across multiple repositories

## Troubleshooting

### Workflow doesn't block PR with hold label

- Verify the label is spelled exactly as `hold` (case-sensitive)
- Check that the workflow is properly configured to run on PR events
- Ensure the workflow file is on the default branch (usually `main`)

### Workflow blocks PR without hold label

- Check PR labels - GitHub may show labels from linked issues
- Verify no label named `hold` is present (including temporary labels that were added/removed)
- Review workflow run logs for the actual label check condition

### Hold label was removed but workflow still fails

- Re-run the workflow after removing the label
- GitHub's event context is captured at workflow start
- Removing the label mid-run won't update the running workflow

## Testing

The workflow includes a test workflow at `.github/workflows/test-enforce-labels.yml` that validates:

1. Workflow correctly fails when hold label is present (simulated)
2. Workflow correctly passes when hold label is absent (simulated)

The test workflow uses `test_mode` to simulate label conditions without requiring actual PRs or labels.
