# Check Permission Reusable Workflow

Reusable workflow that checks if a user has the required permission level in a repository with configurable failure handling. Enables conditional workflow logic based on user permissions.

## Key Features

- **Permission validation**: Check if users have admin, write, read, or none permission levels
- **Configurable failure modes**: Choose how to handle permission failures (fail, skip, or continue)
- **Output-based branching**: Use permission check outputs to conditionally run workflow steps
- **Flexible integration**: Works seamlessly in reusable workflows and composite actions

## How To Use It

### Setup

1. Copy the `check-permission.yml` workflow template into your repository's `.github/workflows/` directory
2. No special labels or secrets required beyond `GITHUB_TOKEN`

### Usage

See [check-permission.yml](./check-permission.yml) template for a calling workflow.

```yaml
jobs:
  permission-check:
    uses: bitwarden/gh-actions/.github/workflows/_check-permission.yml@main
    with:
      require_permission: write # admin, write, read, or none
      failure_mode: fail # fail, skip, or continue
    permissions:
      contents: read
```

### Workflow Behavior

#### Failure Mode: `fail` (default)

When user lacks required permission:

1. Workflow fails with exit code 1
2. Outputs: `has_permission=false`, `should_proceed=false`
3. Stops entire workflow execution

When user has required permission:

1. Workflow succeeds
2. Outputs: `has_permission=true`, `should_proceed=true`

#### Failure Mode: `skip`

When user lacks required permission:

1. Workflow succeeds (exit code 0)
2. Outputs: `has_permission=false`, `should_proceed=false`
3. Use `should_proceed` output to skip protected steps

When user has required permission:

1. Workflow succeeds
2. Outputs: `has_permission=true`, `should_proceed=true`

#### Failure Mode: `continue`

When user lacks required permission:

1. Workflow succeeds (exit code 0)
2. Outputs: `has_permission=false`, `should_proceed=true`
3. Use `user_permission` output for granular branching

When user has required permission:

1. Workflow succeeds
2. Outputs: `has_permission=true`, `should_proceed=true`

## Inputs

| Name                 | Type   | Default | Description                                                   |
| -------------------- | ------ | ------- | ------------------------------------------------------------- |
| `failure_mode`       | string | `fail`  | How to handle permission failures: `fail`, `skip`, `continue` |
| `require_permission` | string | `write` | Required permission level: `admin`, `write`, `read`, `none`   |

## Outputs

| Name              | Description                                                            |
| ----------------- | ---------------------------------------------------------------------- |
| `has_permission`  | Whether the user has the required permission (`true` or `false`)       |
| `user_permission` | Actual permission level of the user (`admin`, `write`, `read`, `none`) |
| `should_proceed`  | Whether subsequent jobs should proceed (`true` or `false`)             |

## Requirements

- `GITHUB_TOKEN` with `contents: read` permission (default token works)
- No additional secrets or labels required

### GitHub Permissions

| Permission | Access | Reason                                |
| ---------- | ------ | ------------------------------------- |
| `contents` | read   | Check user permissions via GitHub API |

## Use Cases

### Restrict Sensitive Deployments

Only allow users with admin permissions to deploy to production:

```yaml
jobs:
  check:
    uses: bitwarden/gh-actions/.github/workflows/_check-permission.yml@main
    with:
      require_permission: admin
      failure_mode: fail

  deploy-prod:
    needs: check
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy-production.sh
```

### Conditional Workflow Paths

Different actions based on permission level:

```yaml
jobs:
  check:
    uses: bitwarden/gh-actions/.github/workflows/_check-permission.yml@main
    with:
      require_permission: write
      failure_mode: continue
    outputs:
      user_permission: ${{ jobs.check-permission.outputs.user_permission }}

  admin-deploy:
    needs: check
    if: needs.check.outputs.user_permission == 'admin'
    runs-on: ubuntu-latest
    steps:
      - run: ./admin-deploy.sh

  standard-deploy:
    needs: check
    if: needs.check.outputs.user_permission == 'write'
    runs-on: ubuntu-latest
    steps:
      - run: ./standard-deploy.sh
```

### Skip Steps Without Failing

Allow workflow to continue but skip protected operations:

```yaml
jobs:
  check:
    uses: bitwarden/gh-actions/.github/workflows/_check-permission.yml@main
    with:
      require_permission: write
      failure_mode: skip

  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  deploy:
    needs: [check, build]
    if: needs.check.outputs.should_proceed == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

## Troubleshooting

### Permission check fails with API error

- Verify `GITHUB_TOKEN` has `contents: read` permission
- Check that the triggering actor exists and has valid username format
- If using `failure_mode: skip` or `continue`, API failures are treated as "none" permission

### Workflow always shows user has no permission

- Confirm the user is a collaborator on the repository
- Check that required permission level is spelled correctly: `admin`, `write`, `read`, or `none`
- External contributors may only have `read` or `none` permissions

### Wrong user being checked

- The workflow checks `github.triggering_actor` (the user who triggered the workflow)
- For `pull_request_target` events, this is the PR author, not the committer
- For manual `workflow_dispatch`, this is the user who clicked "Run workflow"

### Outputs not available in subsequent jobs

- Ensure the permission check job has `outputs:` defined that map to the workflow outputs
- Use `needs.<job-id>.outputs.<output-name>` syntax in dependent jobs
- Verify output names match exactly (case-sensitive)

## Testing

The workflow includes a test workflow at `.github/workflows/test-check-permission.yml` that validates:

1. User with sufficient permission passes check
2. User without permission fails correctly in `fail` mode
3. User without permission sets correct outputs in `skip` mode
4. User without permission continues correctly in `continue` mode
5. All output values are accurate

The test workflow uses `test_mode` to simulate permission levels without requiring actual GitHub API calls or multiple user accounts.

## Permission Levels Hierarchy

Permission levels are hierarchical:

- `admin` >= `write` >= `read` >= `none`
- If you require `write`, users with `admin` also pass
- If you require `read`, users with `write` or `admin` also pass
