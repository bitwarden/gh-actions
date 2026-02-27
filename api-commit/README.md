# API Commit Action

Create a verified commit via the GitHub API without requiring `git` credentials on the runner.

## Features

- Creates commits via the GitHub REST API (Git Data API)
- Supports GitHub App tokens for commits verified as a GitHub App identity
- Commits multiple files atomically in a single commit
- Exposes the resulting commit SHA as an output

## Inputs

| Input     | Description                                                                    | Required | Default                  |
| --------- | ------------------------------------------------------------------------------ | -------- | ------------------------ |
| `files`   | Newline-delimited list of files to commit. If omitted, all files modified relative to HEAD are committed. | No | -  |
| `message` | Commit message                                                                 | Yes      | -                        |
| `branch`  | Branch to commit to                                                            | No       | `${{ github.ref_name }}` |
| `token`   | GitHub token for API access. Use a GitHub App token for verified commits.     | Yes      | -                        |

## Outputs

| Output       | Description                   |
| ------------ | ----------------------------- |
| `commit_sha` | SHA of the created commit     |

## Usage

### Auto-detect Changed Files

Omit `files` to automatically commit all files modified relative to HEAD:

```yaml
- name: Commit all changed files
  uses: bitwarden/gh-actions/api-commit@main
  with:
    message: "chore: update generated files"
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Explicit File List

```yaml
- name: Commit changed files
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: |
      package.json
      package-lock.json
    message: "chore: bump version to ${{ inputs.version }}"
    token: ${{ secrets.GITHUB_TOKEN }}
```

### With a GitHub App Token

Pass a GitHub App token to create commits verified as a GitHub App identity:

```yaml
- name: Generate GitHub App token
  id: app-token
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.APP_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}

- name: Commit changed files
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: version.txt
    message: "chore: update version"
    token: ${{ steps.app-token.outputs.token }}
```

### Specifying a Branch

```yaml
- name: Commit to a specific branch
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: CHANGELOG.md
    message: "docs: update changelog"
    branch: release/2024.1
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Using the Commit SHA Output

```yaml
- name: Commit changed files
  id: api-commit
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: version.txt
    message: "chore: bump version"
    token: ${{ secrets.GITHUB_TOKEN }}

- name: Print commit SHA
  run: echo "Created commit ${{ steps.api-commit.outputs.commit_sha }}"
```

## Permissions

Requires `contents: write` permission on the calling job:

```yaml
permissions:
  contents: write
```
