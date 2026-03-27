---
name: scaffold-action
description: "Phase 2: Generate boilerplate directory structure, action.yml, README.md, test workflow, and type-specific files based on SPEC.md."
---

# Scaffold Action - Phase 2: Boilerplate Generation

You are generating the boilerplate file structure for a new GitHub Action in the Bitwarden `gh-actions` repository. You will read the SPEC.md produced by Phase 1 and create all skeleton files.

## Procedure

### Step 1: Read the Specification

Read `{action-name}/SPEC.md` to understand the action's type, inputs, outputs, and integrations.

### Step 2: Read Reference Files

Read the appropriate reference files from the repository to ensure generated code matches current conventions:

**For ALL action types, read:**
- `check-permission/action.yml` — reference for action.yml structure, input validation, output setting
- `.github/workflows/test-check-permission.yml` — reference for test workflow structure

**For TypeScript actions, also read:**
- `get-keyvault-secrets/action.yml` — node24 action.yml pattern
- `get-keyvault-secrets/package.json` — dependency and build script pattern
- `get-keyvault-secrets/tsconfig.json` — TypeScript configuration
- `get-keyvault-secrets/src/main.ts` — implementation skeleton pattern

**For Docker actions, also read:**
- `version-bump/action.yml` — Docker action.yml pattern
- `version-bump/Dockerfile` — multi-stage build pattern
- `version-bump/main.py` — Python entry point pattern

### Step 3: Generate action.yml

Create `{action-name}/action.yml` with:

```yaml
name: "{Action Name}"
description: "{description from SPEC.md}"
author: "Bitwarden"
branding:
  icon: shield
  color: blue

inputs:
  # From SPEC.md - each input with description, required, and default

outputs:
  # From SPEC.md - each output with description and value reference

runs:
  # Type-specific runs configuration
```

**Composite**: `using: "composite"` with placeholder steps including `shell: bash` and `env:` blocks for inputs (never inline `${{ inputs.* }}` in `run:` commands).

**TypeScript**: `using: "node24"`, `main: "dist/index.js"`

**Docker**: `using: "docker"`, `image: "Dockerfile"`

### Step 4: Generate Type-Specific Files

**For TypeScript actions:**

Create `{action-name}/package.json`:
```json
{
  "name": "@bitwarden/{action-name}",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "build": "ncc build src/main.ts -o dist --license licenses.txt",
    "postbuild": "node -e \"const fs=require('fs'); const f='dist/index.js'; fs.writeFileSync(f, fs.readFileSync(f,'utf8').replace(/\\r\\n/g,'\\n'))\""
  },
  "dependencies": {
    "@actions/core": "^1.11.1"
  },
  "devDependencies": {
    "@vercel/ncc": "^0.38.4",
    "typescript": "^5.9.3"
  }
}
```

Add any additional dependencies based on SPEC.md integrations (e.g., `@azure/identity`, `@azure/keyvault-secrets`, `@actions/github`).

Create `{action-name}/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

Create `{action-name}/src/main.ts` skeleton:
```typescript
import * as core from '@actions/core';

async function run(): Promise<void> {
  try {
    // TODO: Read inputs
    // const inputName = core.getInput('input_name', { required: true });

    // TODO: Implementation

    // TODO: Set outputs
    // core.setOutput('output_name', value);
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

run();
```

Create `{action-name}/.gitignore`:
```
node_modules/
```

**For Docker actions:**

Create `{action-name}/Dockerfile`:
```dockerfile
FROM python:3-slim AS builder

WORKDIR /app

# Install dependencies if needed
# RUN pip3 install --no-cache-dir package-name --target=.

ADD ./main.py .

FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /app /app
ENV PYTHONPATH=/app

ENTRYPOINT ["/usr/bin/python3", "-u", "/app/main.py"]
```

Create `{action-name}/main.py` skeleton:
```python
import os
import sys


def main():
    # TODO: Read inputs from environment variables
    # input_name = os.getenv("INPUT_INPUT_NAME", "")

    # TODO: Implementation

    # TODO: Set outputs
    # with open(os.getenv("GITHUB_OUTPUT", ""), "a") as f:
    #     f.write(f"output_name={value}\n")


if __name__ == "__main__":
    main()
```

### Step 5: Generate Test Workflow

Create `.github/workflows/test-{action-name}.yml` following the exact pattern from the reference:

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
          # TODO: Map outputs to env vars for safe use
        run: |
          echo "TODO: Verify action outputs"
```

**Important**: Use the exact checkout action SHA and version comment from the reference file. Check the current pinned version in an existing test workflow.

### Step 6: Generate README.md

Create `{action-name}/README.md`:

```markdown
# {Action Name}

{description from SPEC.md}

## Usage

\`\`\`yaml
- name: {Action Name}
  uses: bitwarden/gh-actions/{action-name}@main
  with:
    # Required inputs
    input_name: "value"
\`\`\`

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| ... | ... | ... | ... |

## Outputs

| Name | Description |
|------|-------------|
| ... | ... |
```

## Important Rules

- Do NOT implement any logic. Only generate skeletons with TODO comments.
- Always read the reference files first to match current conventions exactly.
- For the test workflow, use the exact pinned SHA for `actions/checkout` from an existing test workflow.
- All input references in composite `run:` blocks MUST go through `env:` — never use `${{ inputs.* }}` directly in shell commands.
- Output names must use underscores, not hyphens.
- Runner must be pinned to `ubuntu-24.04` (not `ubuntu-latest`).
