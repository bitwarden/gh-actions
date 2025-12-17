# Container Tag

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

| Input | Description                                                    | Required |
| ----- | -------------------------------------------------------------- | -------- |
| `ref` | Branch or tag reference. Use `github.head_ref \|\| github.ref` | Yes      |

## Outputs

| Output | Description                       |
| ------ | --------------------------------- |
| `tag`  | The generated container image tag |

## Tag Generation Rules

1. **Pull Requests**: Uses the head branch name (e.g., `feature/add-login` → `feature-add-login`)
2. **Branch Pushes**: Uses the branch name (e.g., `refs/heads/rc` → `rc`)
3. **Tag Pushes**: Uses the tag name (e.g., `refs/tags/v1.0.0` → `1.0.0`)
4. **Sanitization**:
   - Converts to lowercase
   - Strips leading `v` prefix (common in version tags)
   - Replaces non-alphanumeric characters (except `.`, `_`, `-`) with `-`
   - Collapses multiple consecutive `-` into one
   - Removes leading/trailing `-` or `.`
   - Truncates to 128 characters
5. **Main branch**: Converts `main` → `dev`

## Examples

| Input                    | Output                   |
| ------------------------ | ------------------------ |
| `main`                   | `dev`                    |
| `rc`                     | `rc`                     |
| `hotfix-rc`              | `hotfix-rc`              |
| `Feature/Add-Login`      | `feature-add-login`      |
| `feature/PM-1234_update` | `feature-pm-1234_update` |
| `v2024.12.0`             | `2024.12.0`              |
| `v1.2.3`                 | `1.2.3`                  |
