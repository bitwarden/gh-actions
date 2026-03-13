# Version Calculation Reusable Workflow

## Description

The `_version.yml` workflow calculates version numbers for release and non-release builds based on PR labels and git tags.

## Key Features

- **Release builds**: Calculates next semantic version (major, minor, patch) based on PR version labels
- **Non-release builds**: Generates temporary versions with PR identifiers
- **Version label enforcement**: Validates exactly one version label per release PR

## How to use it

### Setup

1. Copy the `version.yml` workflow template into your repository's `.github/workflows/` directory
2. Ensure your repository uses semantic versioning with git tags (format: `vX.Y.Z`)
3. Create these labels in your repository:
   - `version:major` - For breaking changes
   - `version:minor` - For new features
   - `version:patch` - For bug fixes

### Usage

Call this workflow from other workflows using `workflow_call`:

```yaml
jobs:
  calculate-version:
    uses: bitwarden/gh-actions/.github/workflows/_version.yml@main
    with:
      is-release: true # or false for non-release builds
    permissions:
      contents: read
      pull-requests: read
      issues: read
```

The workflow will:

1. Extract the PR number from the commit message
2. For release builds:
   - Get the version label from the PR
   - Fetch the latest git tag
   - Calculate the next version based on the label type
3. For non-release builds:
   - Fetch the latest git tag
   - Append the PR ID (e.g., `1.2.3+456`)

## Inputs

| Input        | Type    | Required | Description                     |
| ------------ | ------- | -------- | ------------------------------- |
| `is-release` | boolean | Yes      | Whether this is a release build |

## Outputs

| Output    | Description                   |
| --------- | ----------------------------- |
| `version` | The calculated version number |

## Requirements

- Repository must use semantic versioning with git tags in format `vX.Y.Z`
- PRs must be squash merged (commit message contains PR number in format `(#123)`)
- For release builds, PR must have exactly one version label
- Repository must have at least one existing git tag

## Troubleshooting

### "Multiple version labels found!" error

- The PR has more than one version label
- Remove all but one version label from the PR

### Version calculation produces unexpected result

- Verify the latest git tag is in format `vX.Y.Z`
- Check that the PR was squash merged with PR number in commit message
- Ensure the correct version label is applied to the PR

### "No merge commit" error

- The commit was not from a squash-merged PR
- Commit messages must contain `(#PR_NUMBER)` format

## Testing

The workflow includes a test workflow at `.github/workflows/test-version.yml` that validates both release and non-release scenarios and cleans up test resources automatically.
