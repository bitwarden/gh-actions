# SDLC / Auto Label PR Composite Action

## Description

The `auto-label-pr-sdlc` composite action labels pull requests based on changed file paths and PR title patterns (conventional commit format). Each repository provides its own `label-pr.json` config defining which labels to apply for which file paths or title prefixes.

## Key Features

- **Title-based labeling**: Matches conventional commit prefixes (e.g. `feat:`, `fix(scope):`) to `t:*` labels
- **Path-based labeling**: Matches changed file paths against configurable prefix patterns
- **Negation patterns**: Supports `.gitignore`-style `!` exclusion patterns within path rules
- **Add or replace mode**: Either appends labels or does a full replace (preserving non-`t:`/`app:` labels like `hold`, `needs-qa`)
- **Dry-run support**: Preview what labels would be applied without mutating the PR

## How to use it

### 1. Add a config file to your repository

Create `.github/label-pr.json` in your repository:

```json
{
  "title_patterns": {
    "t:feature": ["feat", "feature"],
    "t:bugfix": ["fix", "bug"],
    "t:tech-debt": ["refactor", "chore", "cleanup"],
    "t:docs": ["docs"],
    "t:ci": ["ci", "build"],
    "t:deps": ["deps"]
  },
  "path_patterns": {
    "t:ci": [".github/", "scripts/"],
    "t:docs": ["docs/", "README.md"]
  }
}
```

Both `title_patterns` and `path_patterns` keys are required.

**Title matching**: checks for `<pattern>:` or `<pattern>(` anywhere in the lowercased PR title (conventional commit format).

**Path matching**: checks if any changed file path starts with the pattern string. Prefix a pattern with `!` to exclude previously matched files (last match wins, like `.gitignore`).

### 2. Add a workflow to your repository

```yaml
name: Label PR
run-name: Label PR #${{ github.event.pull_request.number }}

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions: {}

jobs:
  label:
    name: Label PR
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      pull-requests: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Label PR
        uses: bitwarden/gh-actions/auto-label-pr-sdlc@main
        with:
          pr-number: ${{ github.event.pull_request.number }}
          pr-labels: ${{ toJSON(github.event.pull_request.labels) }}
          mode: replace
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `pr-number` | Yes | — | The pull request number |
| `pr-labels` | No | `[]` | Current PR labels as JSON array (e.g. `toJSON(github.event.pull_request.labels)`) |
| `mode` | No | `add` | `add` appends labels; `replace` rewrites `t:`/`app:` labels while preserving others |
| `dry-run` | No | `false` | Set to `true` to preview without applying |
| `config-path` | No | `.github/label-pr.json` | Path to config JSON, relative to workspace root |
| `github-token` | Yes | — | GitHub token with `pull-requests: write` permission |

## Mode behavior

- **`add`**: Calls `gh pr edit --add-label`. Existing labels are never removed.
- **`replace`**: Calls `PATCH /issues/:number` to set the exact label list. Labels that don't start with `t:` or `app:` (e.g. `hold`, `needs-qa`, `DB-migrations-changed`) are preserved automatically.

## Requirements

- The repository must have the relevant labels created (e.g. `t:feature`, `t:bugfix`).
- The runner must have Python 3.9+ and the `gh` CLI available (both are present on all GitHub-hosted runners).

## Troubleshooting

### No labels applied

- Check that `label-pr.json` has both `title_patterns` and `path_patterns` keys.
- Verify the labels referenced in the config exist in the repository.
- Run with `dry-run: 'true'` to see what would be matched without applying.

### Config file not found

- Ensure `actions/checkout` runs before this action so the workspace is populated.
- The `config-path` is relative to the workspace root; the default is `.github/label-pr.json`.
