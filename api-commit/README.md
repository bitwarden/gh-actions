# API Commit Action

Create a verified commit via the GitHub API without requiring `git` credentials on the runner.

## Features

- Creates commits via the GitHub REST API (Git Data API)
- Supports GitHub App tokens for commits verified as a GitHub App identity
- Commits multiple files atomically in a single commit, including deletions
- Reads files and runs `git` from a configurable working directory (useful for cross-repo checkouts)
- Exposes the resulting commit SHA as an output

## Inputs

| Input               | Description                                                                                                                                                                | Required | Default                               |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------- |
| `files`             | Newline-delimited list of files to commit (paths relative to `working-directory`). If both `files` and `deletions` are omitted, additions and deletions are auto-detected via `git diff`. | No       | -                                     |
| `deletions`         | Newline-delimited list of files to remove (paths relative to `working-directory`). If both `files` and `deletions` are omitted, additions and deletions are auto-detected via `git diff`. | No       | -                                     |
| `message`           | Commit message                                                                                                                                                            | Yes      | -                                     |
| `branch`            | Branch to commit to                                                                                                                                                       | No       | `${{ github.ref }}`                   |
| `token`             | GitHub token for API access. Use a GitHub App token for verified commits.                                                                                                 | Yes      | -                                     |
| `tag_name`          | Tag to create pointing at the commit. If omitted, no tag is created. If no commit is made, the tag is skipped.                                                            | No       | -                                     |
| `owner`             | Repository owner (org or user). Defaults to the current workflow repository owner.                                                                                        | No       | `${{ github.repository_owner }}`      |
| `repo`              | Repository name. Defaults to the current workflow repository.                                                                                                             | No       | `${{ github.event.repository.name }}` |
| `working-directory` | Directory to read files from and run `git` in. Paths in `files`/`deletions` and the local `origin` remote checked by auto-detect are interpreted relative to this directory. | No       | `GITHUB_WORKSPACE`                    |

## Outputs

| Output       | Description                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------- |
| `commit_sha` | SHA of the created commit, or empty if no changes were detected and no commit was made.      |

## Usage

### Auto-detect Changes

Omit both `files` and `deletions` to commit every change in the working tree relative to `HEAD` — modifications, staged additions, and deletions:

```yaml
- name: Commit all changed files
  uses: bitwarden/gh-actions/api-commit@main
  with:
    message: "chore: update generated files"
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Explicit File List

```yaml
- name: Commit specific files
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: |
      package.json
      package-lock.json
    message: "chore: bump version to ${{ inputs.version }}"
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Removing Files

Use `deletions` to remove files from the branch. Mix with `files` to perform additions and deletions in a single atomic commit:

```yaml
- name: Replace generated artifacts
  uses: bitwarden/gh-actions/api-commit@main
  with:
    files: |
      generated/new-schema.json
    deletions: |
      generated/old-schema.json
    message: "chore: rotate generated schemas"
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Cross-repo / Subdirectory Checkout

When `actions/checkout` puts the target repository at a subdirectory (e.g., `path: sdk-go`), use `working-directory` so file paths and auto-detect resolve there:

```yaml
- name: Checkout target repo
  uses: actions/checkout@v6
  with:
    repository: bitwarden/sdk-go
    path: sdk-go

# ... steps that modify files under sdk-go/ ...

- name: Commit changes
  uses: bitwarden/gh-actions/api-commit@main
  with:
    working-directory: sdk-go
    owner: bitwarden
    repo: sdk-go
    branch: main
    message: "chore: sync from upstream"
    token: ${{ steps.app-token.outputs.token }}
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

## Behaviour Notes

- **Auto-detect vs. explicit.** Auto-detect runs only when *both* `files` and `deletions` are empty. Setting either input disables auto-detect entirely — the action operates only on the paths listed. This avoids accidental partial commits when callers think they're listing files explicitly.
- **Deletion of a path not on the branch.** If a deletion path doesn't exist in the target branch's tree, the commit may end up tree-identical and is skipped. The action reports this with an empty `commit_sha` output and a "Tree unchanged" log line.
- **Symlinks.** Symbolic links are committed with mode `120000` and the link target as content, matching how git stores them.
- **Executable bit.** Files with the user-executable bit set are committed with mode `100755`; everything else uses `100644`.

## Requirements

- The target `branch` must already exist. The action looks up the branch HEAD via the API as its first step and will fail with a 404 if the branch does not exist.
- Auto-detect mode requires a local git repository with a `HEAD` commit (i.e., `actions/checkout` must have run inside `working-directory`). Explicit `files` / `deletions` modes have no git dependency — additions are read directly from disk; deletions are validated as path shape only.
- When auto-detect targets a repository other than the workflow's own, the `working-directory` must be a checkout of that repository (the action verifies via `git remote get-url origin`).

## Permissions

Requires `contents: write` permission on the calling job:

```yaml
permissions:
  contents: write
```
