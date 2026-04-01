# Composite Action — Structural Template

Distilled from: `check-permission`, `get-pull-request-threads`, `update-pr-comment`, `container-tag`

---

## Files

A composite action directory contains:

```
{action-name}/
├── action.yml
├── README.md
└── SPEC.md        (internal, deleted after pipeline completes)
```

No additional files are needed — all logic lives in `action.yml`.

---

## action.yml Structure

```yaml
name: "{Action Name}"
description: "{One-line description}"
author: "Bitwarden"

inputs:
  required_input:
    description: "What this input controls"
    required: true
  optional_input:
    description: "What this optional input controls"
    required: false
    default: "default_value"

outputs:
  output_name:
    description: "What this output contains"
    value: ${{ steps.step-id.outputs.output_name }}

runs:
  using: "composite"
  steps:
    - name: Descriptive step name
      id: step-id
      shell: bash
      env:
        REQUIRED_INPUT: ${{ inputs.required_input }}
        OPTIONAL_INPUT: ${{ inputs.optional_input }}
      run: |
        set -e
        # TODO: Implementation
```

### Field ordering

1. `name`
2. `description`
3. `author`
4. `inputs` (required first, then optional)
5. `outputs` (each with `description` and `value`)
6. `runs`

### Output value references

Every output `value` must reference a step by its `id`:

```yaml
outputs:
  result:
    description: "The result"
    value: ${{ steps.my-step.outputs.result }}
```

The step `id` and output name must match exactly.

### Step conventions

- Every step has `shell: bash`
- Every step has an `env:` block mapping all inputs it uses
- Never use `${{ inputs.* }}` directly in `run:` blocks
- Steps that set outputs must have an `id:`

### Multi-step actions

For actions with multiple logical phases (e.g., authenticate → fetch → process), use separate steps:

```yaml
steps:
  - name: Authenticate
    id: auth
    shell: bash
    env:
      CLIENT_ID: ${{ inputs.client_id }}
    run: |
      set -e
      # TODO: Authentication logic

  - name: Process data
    id: process
    shell: bash
    env:
      AUTH_TOKEN: ${{ steps.auth.outputs.token }}
    run: |
      set -e
      # TODO: Processing logic
```

### Calling other actions from composite steps

When wrapping Bitwarden actions:

```yaml
steps:
  - name: Azure login
    uses: bitwarden/gh-actions/azure-login@main
    with:
      tenant_id: ${{ inputs.azure_tenant_id }}
      client_id: ${{ inputs.azure_client_id }}
      subscription_id: ${{ inputs.azure_subscription_id }}
```
