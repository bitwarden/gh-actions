# Test Workflow — Structural Template

Distilled from: `test-check-permission.yml`

---

## Single-Job Test Workflow

```yaml
name: Test {Action Name}

on:
  pull_request:
    paths:
      - "{action-name}/**"
      - ".github/workflows/test-{action-name}.yml"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    name: Test {Action Name}
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          persist-credentials: false

      - name: Run {action-name}
        id: test
        uses: ./{action-name}
        with:
          # TODO: Provide test inputs

      - name: Verify outputs
        env:
          # TODO: Map outputs to env vars
          OUTPUT_NAME: ${{ steps.test.outputs.output_name }}
        run: |
          echo "Output: $OUTPUT_NAME"
          # TODO: Add assertions
```

---

## Multi-Job Test Workflow

For actions with distinct modes or configurations, use separate jobs:

```yaml
name: Test {Action Name}

on:
  pull_request:
    paths:
      - "{action-name}/**"
      - ".github/workflows/test-{action-name}.yml"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test-default-mode:
    name: Test default mode
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          persist-credentials: false

      - name: Run with default configuration
        id: test-default
        uses: ./{action-name}
        with:
          # TODO: Provide default mode inputs

      - name: Verify outputs
        env:
          OUTPUT: ${{ steps.test-default.outputs.output_name }}
        run: |
          echo "Output: $OUTPUT"

  test-alternate-mode:
    name: Test alternate mode
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          persist-credentials: false

      - name: Run with alternate configuration
        id: test-alt
        uses: ./{action-name}
        with:
          # TODO: Provide alternate mode inputs

      - name: Verify outputs
        env:
          OUTPUT: ${{ steps.test-alt.outputs.output_name }}
        run: |
          echo "Output: $OUTPUT"
```

---

## Structural Rules

### Triggers

- Always include `pull_request` with `paths` scoped to the action directory and the test workflow itself
- Always include `workflow_dispatch` for manual testing

### Permissions

- Set `permissions` at the workflow level (not per-job) unless jobs need different scopes
- Use `contents: read` as the baseline — only escalate if the action requires more

### Runners

- Always pin to `ubuntu-24.04` — never use `ubuntu-latest`

### External Actions

- Pin to commit SHA with version comment: `uses: actions/checkout@{sha} # v{version}`
- Always include `persist-credentials: false` on checkout

### Output Verification

- Map step outputs to `env:` variables — never inline `${{ steps.*.outputs.* }}` in `run:` blocks
- Use descriptive env var names that match the output names

### Job Naming

- Workflow `name` starts with a capital letter
- Job `name` starts with a capital letter
- Step `name` starts with a capital letter

### When to Use Multiple Jobs

- The action has distinct modes (e.g., fail/skip/continue)
- The action has mutually exclusive input combinations
- Different test scenarios need different permissions
- A failure in one scenario should not block testing other scenarios
