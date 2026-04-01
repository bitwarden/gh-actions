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

### Step 2: Read Structural Templates

Read the structural templates from `references/` (co-located with this skill). These are the primary baseline for file structure, field ordering, and skeleton content.

**For ALL action types, read:**
- `references/test-workflow-structure.md` — test workflow triggers, permissions, pinning, job structure
- `references/readme-specification.md` — README section definitions and formatting rules

**Per action type, also read:**
- **Composite**: `references/composite-structure.md`
- **TypeScript**: `references/typescript-structure.md`
- **Docker/Python**: `references/docker-structure.md`

Use these templates as the authoritative source for generating skeleton files. The inline examples in Steps 4-7 below are summaries — the templates have the full detail.

**Discovery fallback**: If the SPEC.md describes integrations or structural needs not covered by the templates (e.g., wrapping an unfamiliar external action, unusual multi-file layout), propose specific actions from the repository to use as additional references. Present them to the user before reading:

```
The structural templates do not cover {specific need}.
Proposed additional references from the repository:
  - {action-name}/{file} — {why this is relevant}

Proceed with these references?
```

Only read repository files after the user approves. Do not scan the repository speculatively.

### Step 3: Create Directory

Run `mkdir -p {action-name}` to ensure the action directory exists (it should already exist from define-action, but ensure it).

### Step 4: Generate action.yml

Create `{action-name}/action.yml` with:

```yaml
name: "{Action Name}"
description: "{description from SPEC.md}"
author: "Bitwarden"

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
  "type": "module",
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

**Important**: Use the exact checkout action SHA from `references/test-workflow-structure.md`. That template is kept current — do not scan the repository for a different SHA.

### Step 7: Generate README.md

Create `{action-name}/README.md` with section headings and TODO placeholders. The scaffold defines the structure; `implement-action` populates it later.

Read `references/readme-specification.md` (already loaded in Step 2) for the canonical section definitions, table formats, ordering rules, and formatting constraints.

**Scaffolding rules:**
- Include all sections from the specification that apply based on SPEC.md (Title, Description, Features, Inputs, Outputs, Usage, and any relevant supplementary sections).
- Use `<!-- TODO: ... -->` comments as placeholders for content that implement-action will fill in.
- Only include conditional/supplementary sections whose TODOs will be fulfillable based on SPEC.md. Do not include empty sections.
- Pre-fill table headers and column structure exactly as the specification defines (column order, backtick formatting).
- Pre-fill the title and description from SPEC.md — these are known at scaffold time.

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
- Always read the structural templates in `references/` first. They are the primary baseline.
- For the test workflow, use the exact pinned SHA for `actions/checkout` from `references/test-workflow-structure.md`.
- Do not scan the repository for patterns unless the templates are insufficient for the SPEC.md requirements. If discovery is needed, propose references to the user first.
- All input references in composite `run:` blocks MUST go through `env:` -- never use `${{ inputs.* }}` directly in shell commands.
- Output names must use underscores, not hyphens.
- Runner must be pinned to `ubuntu-24.04` (not `ubuntu-latest`).
- This skill only creates files. It never runs `npm install`, `npm run build`, or any build commands.

## Related Skills

- **define-action**: Run first to produce the SPEC.md this skill consumes. Example: `define-action {action-name}`
- **implement-action**: Run after scaffolding to replace TODO placeholders with working code. Example: `implement-action {action-name}`
- **evaluate-action**: Reviews implementation completeness against SPEC.md. Example: `evaluate-action {action-name}`
- **validate-action**: Run after implementation to check formatting, structure, and linter compliance. Example: `validate-action {action-name}`
