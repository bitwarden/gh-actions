# Check Permission Action

Check user permissions with configurable failure handling.

## Features

- Check permissions: admin, write, read, none
- Three modes: fail, skip, or continue
- Control workflow execution based on permission level
- Works in reusable workflows

## Inputs

| Input          | Description                                                  | Required | Default |
| -------------- | ------------------------------------------------------------ | -------- | ------- |
| `require`      | Required permission level (`admin`, `write`, `read`, `none`) | Yes      | -       |
| `username`     | Username to check permissions for                            | Yes      | -       |
| `token`        | GitHub token for API access                                  | Yes      | -       |
| `failure_mode` | How to handle failures: `fail`, `skip`, or `continue`        | No       | `fail`  |

### Failure Modes

- **`fail`**: Exit 1 when permission missing - workflow stops
- **`skip`**: Exit 0, set `should_proceed=false` - skip protected steps
- **`continue`**: Exit 0 always - branch on `has_permission` output

## Outputs

| Output            | Description                                                             |
| ----------------- | ----------------------------------------------------------------------- |
| `has_permission`  | `true` if user has required permission, `false` otherwise               |
| `user_permission` | Actual permission level of the user (`admin`, `write`, `read`, `none`)  |
| `should_proceed`  | `true` when permission check passes, `false` when `skip` mode and fails |

## Usage Examples

### Hard Fail (default)

```yaml
- uses: bitwarden/gh-actions/check-permission@main
  with:
    require: write
    username: ${{ github.triggering_actor }}
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Skip Mode

```yaml
- id: permission
  uses: bitwarden/gh-actions/check-permission@main
  with:
    require: write
    username: ${{ github.triggering_actor }}
    token: ${{ secrets.GITHUB_TOKEN }}
    failure_mode: skip

- if: steps.permission.outputs.should_proceed == 'true'
  run: ./deploy.sh
```

### Continue Mode

```yaml
- id: permission
  uses: bitwarden/gh-actions/check-permission@main
  with:
    require: write
    username: ${{ github.triggering_actor }}
    token: ${{ secrets.GITHUB_TOKEN }}
    failure_mode: continue

- if: steps.permission.outputs.user_permission == 'admin'
  run: ./admin-deploy.sh

- if: steps.permission.outputs.user_permission == 'write'
  run: ./standard-deploy.sh
```

### Reusable Workflow

```yaml
on:
  workflow_call:
    inputs:
      failure_mode:
        type: string
        default: 'fail'

jobs:
  check:
    outputs:
      should_proceed: ${{ steps.check.outputs.should_proceed }}
    steps:
      - uses: actions/checkout@v4
      - id: check
        uses: ./check-permission
        with:
          require: write
          username: ${{ github.triggering_actor }}
          token: ${{ secrets.GITHUB_TOKEN }}
          failure_mode: ${{ inputs.failure_mode }}

  deploy:
    needs: check
    if: needs.check.outputs.should_proceed == 'true'
    steps:
      - run: ./deploy.sh
```

## Permissions

Requires `contents: read` permission. The default `GITHUB_TOKEN` works.

```yaml
permissions:
  contents: read
```
