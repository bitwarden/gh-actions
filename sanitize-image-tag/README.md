# Sanitize Image Tag

A reusable GitHub Action that generates standardized container image tags from a Git ref, with optional prefix and fork-repo prepending. Centralizes the tag-derivation logic that was previously duplicated across `bitwarden/server`, `bitwarden/clients`, and `bitwarden/self-host`.

## Usage

### Basic

```yaml
- name: Generate Docker image tag
  id: tag
  uses: bitwarden/gh-actions/sanitize-image-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}

- name: Build and push
  run: docker push ghcr.io/bitwarden/myimage:${{ steps.tag.outputs.tag }}
```

### With prefix (e.g., dispatching Bitwarden Lite from server/clients)

```yaml
- name: Generate override tag
  id: tag
  uses: bitwarden/gh-actions/sanitize-image-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}
    prefix: "server-"
```

### With fork-PR handling

```yaml
- name: Generate tag
  id: tag
  uses: bitwarden/gh-actions/sanitize-image-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}
    fork_repo: ${{ github.event.pull_request.head.repo.fork == true && github.event.pull_request.head.repo.full_name || '' }}
```

## Inputs

| Input       | Description                                                                                                            | Required | Default |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | -------- | ------- |
| `ref`       | Branch or tag reference. Accepts both `refs/heads/<name>` / `refs/tags/<name>` form and bare branch names.             | Yes      |         |
| `prefix`    | Prepended verbatim to the final tag (include trailing dash, e.g., `server-`).                                          | No       | `""`    |
| `fork_repo` | Sanitized fork repo full name (e.g., `forkuser/repo`) prepended to distinguish fork-PR builds. Empty for non-fork events. | No       | `""`    |

## Outputs

| Output | Description                       |
| ------ | --------------------------------- |
| `tag`  | The generated container image tag |

## Tag generation rules

1. **Ref extraction**: strips `refs/heads/` or `refs/tags/` prefix if present.
2. **Sanitization**:
   - Lowercases the entire string.
   - Strips a single leading `v` (so `v1.2.3` → `1.2.3`).
   - Replaces any run of characters outside `[a-z0-9._-]` with a single `-`.
   - Collapses repeated dashes.
   - Strips leading/trailing `.` or `-`.
3. **Fork prepending** (if `fork_repo` is set): sanitized fork name + `-` is prepended.
4. **Main-to-dev mapping**: a final value of exactly `main` becomes `dev`. Runs after fork prepending so `fork-main` is unaffected.
5. **Prefix**: `prefix` is prepended verbatim.
6. **Length cap**: truncated to 128 characters; trailing `.` or `-` after truncation is stripped.

## Examples

| `ref`                       | `prefix`  | `fork_repo`        | Output                          |
| --------------------------- | --------- | ------------------ | ------------------------------- |
| `main`                      | `""`      | `""`               | `dev`                           |
| `main`                      | `server-` | `""`               | `server-dev`                    |
| `rc`                        | `""`      | `""`               | `rc`                            |
| `hotfix-rc`                 | `web-`    | `""`               | `web-hotfix-rc`                 |
| `feature/PM-1234_update`    | `""`      | `""`               | `feature-pm-1234_update`        |
| `Feature/Add-Login`         | `server-` | `""`               | `server-feature-add-login`      |
| `refs/tags/v2024.12.0`      | `""`      | `""`               | `2024.12.0`                     |
| `feature/foo`               | `""`      | `bobuser/server`   | `bobuser-server-feature-foo`    |
| `main`                      | `""`      | `bobuser/server`   | `bobuser-server-main`           |
