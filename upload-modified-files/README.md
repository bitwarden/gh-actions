# Upload Modified Files Action

## Description

The `upload-modified-files` action detects files that have been modified in the working tree of a checked-out repository and uploads them to the current workflow run as an artifact. It is designed for the pattern where one repository (for example, a build repo) produces changes to tracked files — such as version bumps — and a downstream repository (for example, a deploy repo) downloads those changes and commits them back using a bot with direct push access.

The action runs in two steps:

1. **Detect modified files.** Inspects `git status` and collects modifications to existing tracked files. It **fails if any files are added (new/untracked) or deleted**, because the downstream consumer commits the files over an existing checkout and cannot safely reconcile additions or removals.
2. **Upload to the workflow run.** Archives the modified files into a `tar.gz` that preserves their exact repo-relative paths, then uploads it as an artifact.

## Key Features

- **Modification-only safety check**: Fails fast on added or deleted files so only in-place edits are propagated.
- **Exact path preservation**: Files are archived with their full repo-relative paths, so they restore to the same structure when extracted in another repo — even when the changes span subdirectories.
- **Simple, self-contained**: Pure `git` and `tar`, no external dependencies beyond what GitHub-hosted runners provide.

## How to Use It

Add this step after a step that modifies tracked files (e.g. a version bump). The repository must already be checked out.

```yaml
- name: Checkout
  uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    persist-credentials: false

# ... step(s) that modify tracked files, e.g. a version bump ...

- name: Upload modified files
  id: upload
  uses: bitwarden/gh-actions/upload-modified-files@main
  with:
    artifact_name: modified-files
    retention_days: '7'
```

### Inputs

| Input            | Required | Default          | Description                                              |
| ---------------- | -------- | ---------------- | -------------------------------------------------------- |
| `artifact_name`  | No       | `modified-files` | Name of the artifact to upload the modified files under. |
| `retention_days` | No       | `1`              | Number of days to retain the uploaded artifact.          |

### Outputs

| Output           | Description                                     |
| ---------------- | ----------------------------------------------- |
| `count`          | Number of modified files detected and uploaded. |
| `modified_files` | Newline-separated list of modified file paths.  |

## Consuming the Artifact

The artifact contains a single file, `modified-files.tar.gz`, holding the modified files at their original repo-relative paths. In a downstream repository, download it, extract it over the checkout, and commit:

```yaml
- name: Checkout target repo
  uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

- name: Download modified files
  uses: actions/download-artifact@37930b1c2abaa49bbe596cd826c3c89aef350131 # v7.0.0
  with:
    name: modified-files
    path: modified-files-tmp
    github-token: ${{ steps.app-token.outputs.token }}
    run-id: ${{ github.event.workflow_run.id }}
    repository: bitwarden/source-repo

- name: Apply and commit
  run: |
    tar -xzf modified-files-tmp/modified-files.tar.gz
    git add --update
    git commit -m "Apply modified files from upstream run"
    git push
```

> For cross-repo downloads, generate a GitHub App token scoped to the source repository and pass it to `actions/download-artifact` via `github-token`, along with the upstream `run-id` and `repository`.

## Requirements

- The repository must be checked out before this action runs (`actions/checkout`), with the modifications present in the working tree.
- `git` and `tar` must be available on the runner (present by default on GitHub-hosted runners).

## Troubleshooting

### "Detected added/untracked files, which are not supported"

- The working tree contains new files that are not tracked by git. This action only uploads modifications to existing tracked files. Remove the new files or handle them separately.

### "Detected deleted files, which are not supported"

- A tracked file was removed from the working tree. The downstream consumer cannot safely apply deletions; revert the deletion or handle it separately.

### "No modified files detected. Nothing to upload."

- The working tree is clean. Confirm the step that is supposed to modify files ran before this action and actually changed something.

### Nested paths are missing after download

- Ensure you extract `modified-files.tar.gz` from the repository root in the downstream job so the preserved repo-relative paths land in the right place.
