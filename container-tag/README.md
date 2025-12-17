# Generate Container Image Tag

A reusable GitHub Action that generates standardized, sanitized container image tags for Docker images across Bitwarden repositories.

## Features

- **Simple interface**: Single input parameter using GitHub's context
- **Consistent sanitization**: Converts to lowercase, replaces invalid characters, removes leading/trailing special characters
- **Length limiting**: Truncates to 128 characters (Docker's maximum tag length)
- **Branch mapping**: Automatically converts `main` branch to `dev` tag
- **Handles all event types**: Works with pull requests, pushes, and tag events

## Usage

### Basic Example

```yaml
- name: Generate Docker image tag
  id: tag
  uses: bitwarden/gh-actions/container-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}

- name: Use the generated tag
  run: |
    echo "Tag: ${{ steps.tag.outputs.tag }}"
```

### Complete Docker Build Example

```yaml
- name: Generate Docker image tag
  id: tag
  uses: bitwarden/gh-actions/container-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}

- name: Build and push image
  uses: docker/build-push-action@v6
  with:
    push: true
    tags: ghcr.io/bitwarden/myimage:${{ steps.tag.outputs.tag }}
```

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| `ref` | Branch or tag reference. Use `github.head_ref \|\| github.ref` | Yes |

## Outputs

| Output | Description |
|--------|-------------|
| `tag` | The generated container image tag |

## Tag Generation Rules

1. **Pull Requests**: Uses the head branch name (e.g., `feature/add-login` → `feature-add-login`)
2. **Branch Pushes**: Uses the branch name (e.g., `refs/heads/rc` → `rc`)
3. **Tag Pushes**: Uses the tag name (e.g., `refs/tags/v1.0.0` → `v1-0-0`)
4. **Sanitization**:
   - Converts to lowercase
   - Replaces non-alphanumeric characters (except `.`, `_`, `-`) with `-`
   - Collapses multiple consecutive `-` into one
   - Removes leading/trailing `-` or `.`
   - Truncates to 128 characters
5. **Main branch**: Converts `main` → `dev`

## Examples

| Input | Output |
|-------|--------|
| `main` | `dev` |
| `rc` | `rc` |
| `hotfix-rc` | `hotfix-rc` |
| `Feature/Add-Login` | `feature-add-login` |
| `feature/PM-1234_update` | `feature-pm-1234_update` |
| `v2024.12.0` | `v2024-12-0` |

## Migration from Inline Script

**Before:**
```yaml
- name: Generate Docker image tag
  id: tag
  run: |
    if [[ "${GITHUB_EVENT_NAME}" == "pull_request" || "${GITHUB_EVENT_NAME}" == "pull_request_target" ]]; then
      IMAGE_TAG=$(echo "${GITHUB_HEAD_REF}" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/-+/-/g; s/^-+|-+$//g' | cut -c1-128 | sed -E 's/[.-]$//')
    else
      BRANCH_NAME=$(echo "${GITHUB_REF}" | sed 's|^refs/heads/||; s|^refs/tags/||')
      IMAGE_TAG=$(echo "${BRANCH_NAME}" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/-+/-/g; s/^-+|-+$//g' | cut -c1-128 | sed -E 's/[.-]$//')
    fi
    if [[ "$IMAGE_TAG" == "main" ]]; then
      IMAGE_TAG=dev
    fi
    echo "image_tag=$IMAGE_TAG" >> "$GITHUB_OUTPUT"
```

**After:**
```yaml
- name: Generate Docker image tag
  id: tag
  uses: bitwarden/gh-actions/container-tag@main
  with:
    ref: ${{ github.head_ref || github.ref }}
```

Then reference as `${{ steps.tag.outputs.tag }}`.
