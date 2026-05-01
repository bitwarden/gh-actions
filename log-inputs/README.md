# Log Inputs to Job Summary

Logs workflow inputs to the GitHub Actions job summary as a collapsible JSON block.

## Usage

```yaml
- name: Log inputs
  uses: bitwarden/gh-actions/log-inputs@main
  with:
    inputs: ${{ toJson(inputs) }}
```

## Inputs

| Input    | Required | Description               |
| -------- | -------- | ------------------------- |
| `inputs` | Yes      | Workflow inputs as JSON   |

## Example

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
      version:
        description: Release version
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Log inputs
        uses: bitwarden/gh-actions/log-inputs@main
        with:
          inputs: ${{ toJson(inputs) }}
```

The action appends a collapsible `<details>` block to the job summary containing the formatted JSON inputs.
