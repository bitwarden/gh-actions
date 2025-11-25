# Examples

## Basic Usage

### Fail Mode (default)

Workflow stops if permission missing.

```yaml
steps:
  - uses: bitwarden/gh-actions/check-permission@main
    with:
      require: admin
      username: ${{ github.triggering_actor }}
      token: ${{ secrets.GITHUB_TOKEN }}
```

### Skip Mode

Workflow continues, skip protected steps.

```yaml
steps:
  - id: check
    uses: bitwarden/gh-actions/check-permission@main
    with:
      require: write
      username: ${{ github.triggering_actor }}
      token: ${{ secrets.GITHUB_TOKEN }}
      failure_mode: skip

  - if: steps.check.outputs.should_skip != 'true'
    run: ./deploy.sh
```

### Continue Mode

Branch on actual permission level.

```yaml
steps:
  - id: check
    uses: bitwarden/gh-actions/check-permission@main
    with:
      require: write
      username: ${{ github.triggering_actor }}
      token: ${{ secrets.GITHUB_TOKEN }}
      failure_mode: continue

  - if: steps.check.outputs.user_permission == 'admin'
    run: ./admin-deploy.sh

  - if: steps.check.outputs.user_permission == 'write'
    run: ./standard-deploy.sh

  - if: steps.check.outputs.user_permission == 'read'
    run: ./read-only.sh
```

## Advanced Patterns

### Multi-Environment Deploy

```yaml
jobs:
  check:
    outputs:
      permission: ${{ steps.check.outputs.user_permission }}
    steps:
      - uses: actions/checkout@v4
      - id: check
        uses: ./check-permission
        with:
          require: read
          username: ${{ github.triggering_actor }}
          token: ${{ secrets.GITHUB_TOKEN }}
          failure_mode: continue

  prod:
    needs: check
    if: needs.check.outputs.permission == 'admin'
    steps:
      - run: ./deploy-prod.sh

  staging:
    needs: check
    if: needs.check.outputs.permission == 'write'
    steps:
      - run: ./deploy-staging.sh

  dev:
    needs: check
    if: needs.check.outputs.permission == 'read'
    steps:
      - run: ./deploy-dev.sh
```

### Permission Gate

```yaml
jobs:
  gate:
    outputs:
      should_skip: ${{ steps.check.outputs.should_skip }}
    steps:
      - uses: actions/checkout@v4
      - id: check
        uses: ./check-permission
        with:
          require: write
          username: ${{ github.triggering_actor }}
          token: ${{ secrets.GITHUB_TOKEN }}
          failure_mode: skip

  deploy:
    needs: gate
    if: needs.gate.outputs.should_skip != 'true'
    steps:
      - run: ./deploy.sh
```

### Fallback Strategy

```yaml
steps:
  - id: admin
    uses: ./check-permission
    with:
      require: admin
      username: ${{ github.triggering_actor }}
      token: ${{ secrets.GITHUB_TOKEN }}
      failure_mode: skip

  - if: steps.admin.outputs.should_skip == 'true'
    id: write
    uses: ./check-permission
    with:
      require: write
      username: ${{ github.triggering_actor }}
      token: ${{ secrets.GITHUB_TOKEN }}
      failure_mode: fail

  - if: steps.admin.outputs.has_permission == 'true'
    run: ./full-deploy.sh

  - if: steps.admin.outputs.should_skip == 'true'
    run: ./standard-deploy.sh
```

## Reusable Workflows

### Flexible Consumer Control

```yaml
# reusable-deploy.yml
on:
  workflow_call:
    inputs:
      failure_mode:
        type: string
        default: 'fail'

jobs:
  check:
    outputs:
      should_skip: ${{ steps.check.outputs.should_skip }}
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
    if: needs.check.outputs.should_skip != 'true'
    steps:
      - run: ./deploy.sh
```

### Job-Level Outputs

```yaml
on:
  workflow_call:
    outputs:
      deployed:
        value: ${{ jobs.check.outputs.has_permission }}

jobs:
  check:
    outputs:
      has_permission: ${{ steps.check.outputs.has_permission }}
    steps:
      - uses: actions/checkout@v4
      - id: check
        uses: ./check-permission
        with:
          require: write
          username: ${{ github.triggering_actor }}
          token: ${{ secrets.GITHUB_TOKEN }}
          failure_mode: skip

  deploy:
    needs: check
    if: needs.check.outputs.has_permission == 'true'
    steps:
      - run: ./deploy.sh
```

## Best Practices

- Use `fail` for critical operations
- Use `skip` for optional features
- Use `continue` for tiered functionality
- Specify `failure_mode` explicitly
- Test with different permission levels
- Handle bot accounts separately
- Use outputs for conditional logic
- Document permission requirements
