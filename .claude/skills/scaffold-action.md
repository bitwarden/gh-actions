---
name: scaffold-action
description: "Generate boilerplate directory structure, action.yml, README.md, test workflow, and type-specific files for a new GitHub Action from its SPEC.md."
argument-hint: "<action-name>"
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(ls:*)
  - Bash(mkdir:*)
---

# Scaffold Action - Boilerplate Generation

Generate the complete file structure for a new GitHub Action in the Bitwarden `gh-actions` repository. Read the SPEC.md produced by the define-action skill and create all skeleton files with TODO placeholders -- no implementation logic.

## Input

This skill accepts a single required argument: the action directory name (e.g., `my-new-action`).

The action directory must already contain a `SPEC.md` file produced by the `define-action` skill.

**Examples:**
- `scaffold-action my-new-action`
- `scaffold-action report-deployment-status-to-slack`

## Procedure

### Step 1: Validate Prerequisites

1. Confirm `{action-name}/SPEC.md` exists using `ls`.
2. If SPEC.md does not exist, stop and report: "No SPEC.md found in {action-name}/. Run the define-action skill first to generate a specification."
3. Read `{action-name}/SPEC.md` to understand the action's type, inputs, outputs, and integrations.

### Step 2: Read Reference Files

Read the appropriate reference files from the repository to ensure generated code matches current conventions.

**For ALL action types, read:**
- `check-permission/action.yml` -- reference for action.yml structure, input validation, output setting
- `.github/workflows/test-check-permission.yml` -- reference for test workflow structure

**For TypeScript actions, also read:**
- `get-keyvault-secrets/action.yml` -- node24 action.yml pattern
- `get-keyvault-secrets/package.json` -- dependency and build script pattern
- `get-keyvault-secrets/tsconfig.json` -- TypeScript configuration
- `get-keyvault-secrets/src/main.ts` -- implementation skeleton pattern

**For Docker actions, also read:**
- `version-bump/action.yml` -- Docker action.yml pattern
- `version-bump/Dockerfile` -- multi-stage build pattern
- `version-bump/main.py` -- Python entry point pattern

### Step 3: Create Directory

Run `mkdir -p {action-name}` to ensure the action directory exists (it should already exist from define-action, but ensure it).

### Step 4: Generate action.yml

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

### Step 5: Generate Type-Specific Files

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

### Step 6: Generate Test Workflow

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

**Important**: Use the exact checkout action SHA and version comment from the reference file. Read an existing test workflow to get the currently pinned version.

### Step 7: Generate README.md

Create `{action-name}/README.md` with section headings and TODO placeholders. The scaffold defines the structure; `implement-action` populates it later.

**Required sections** (always include):

```markdown
# {Action Name}

{description from SPEC.md}

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
<!-- TODO: Populate from action.yml inputs -->

## Outputs

| Name | Description |
|------|-------------|
<!-- TODO: Populate from action.yml outputs -->

## Usage

<!-- TODO: Add basic usage example -->
<!-- TODO: Add additional examples for different configurations if applicable -->
```

**Conditional sections** (include based on SPEC.md):

```markdown
## Features
<!-- Include if action has 2+ distinct capabilities. TODO: List key features as bullet points -->

## Prerequisites
<!-- Include if action requires external setup (Azure credentials, installed tools, etc.). TODO: Document setup requirements -->

## Permissions
<!-- Include if action requires specific GitHub token permissions. TODO: Document required permissions -->

## Development
<!-- Include for TypeScript actions only. TODO: Document build and test instructions -->
```

**Section ordering**: Title → Description → Features (if applicable) → Inputs → Outputs → Prerequisites (if applicable) → Usage → Permissions (if applicable) → Development (if applicable)

Only include conditional sections whose TODO markers will be fulfillable based on SPEC.md. Do not include empty conditional sections.

### Step 8: Report Results

List all files created with their paths. Example:

```
Scaffolded files for {action-name}:
  - {action-name}/action.yml
  - {action-name}/src/main.ts
  - {action-name}/package.json
  - {action-name}/tsconfig.json
  - {action-name}/.gitignore
  - {action-name}/README.md
  - .github/workflows/test-{action-name}.yml

Next step: Run the implement-action skill to replace TODO placeholders with working code:
  implement-action {action-name}
```

## Important Rules

- Do NOT implement any logic. Only generate skeletons with TODO comments.
- Always read the reference files first to match current conventions exactly.
- For the test workflow, use the exact pinned SHA for `actions/checkout` from an existing test workflow.
- All input references in composite `run:` blocks MUST go through `env:` -- never use `${{ inputs.* }}` directly in shell commands.
- Output names must use underscores, not hyphens.
- Runner must be pinned to `ubuntu-24.04` (not `ubuntu-latest`).
- This skill only creates files. It never runs `npm install`, `npm run build`, or any build commands.

## Related Skills

- **define-action**: Run first to produce the SPEC.md this skill consumes. Example: `define-action {action-name}`
- **implement-action**: Run after scaffolding to replace TODO placeholders with working code. Example: `implement-action {action-name}`
- **evaluate-action**: Reviews implementation completeness against SPEC.md. Example: `evaluate-action {action-name}`
- **validate-action**: Run after implementation to check formatting, structure, and linter compliance. Example: `validate-action {action-name}`
