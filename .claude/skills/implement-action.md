---
name: implement-action
description: "Phase 3: Implement the core logic of a GitHub Action based on SPEC.md and scaffolded files. Writes working code, not skeletons."
---

# Implement Action - Phase 3: Core Logic Development

You are implementing the core logic for a new GitHub Action in the Bitwarden `gh-actions` repository. The action has already been defined (Phase 1) and scaffolded (Phase 2). Your job is to replace TODO placeholders with working code.

## Procedure

### Step 1: Understand Requirements

1. Read `{action-name}/SPEC.md` for the full requirements specification
2. Read all scaffolded files in the `{action-name}/` directory
3. Identify similar existing actions in the repo that solve related problems — read their implementations for patterns

### Step 2: Implement Core Logic

**For Composite actions** — edit `{action-name}/action.yml`:
1. Replace placeholder steps with real implementation
2. Use `env:` blocks to pass all inputs to shell scripts (never inline `${{ inputs.* }}` in `run:`)
3. Use `set -e` at the top of bash scripts
4. Write outputs to `$GITHUB_OUTPUT` using `echo "name=value" >> "$GITHUB_OUTPUT"`
5. Use `::error::`, `::warning::`, `::notice::` annotations for user-facing messages
6. Validate all required inputs at the start of the script
7. Reference pattern: read `check-permission/action.yml` for input validation and output setting

**For TypeScript actions** — edit `{action-name}/src/main.ts`:
1. Import `@actions/core` and any needed packages
2. Read inputs with `core.getInput('name', { required: true/false })`
3. Mask sensitive values with `core.setSecret(value)`
4. Set outputs with `core.setOutput('name', value)`
5. Wrap everything in try/catch with `core.setFailed()` in the catch block
6. Reference pattern: read `get-keyvault-secrets/src/main.ts`

**For Docker/Python actions** — edit `{action-name}/main.py`:
1. Read inputs from environment: `os.getenv("INPUT_NAME")` (GitHub uppercases and prefixes with `INPUT_`)
2. Write outputs: append to `os.getenv("GITHUB_OUTPUT")` file
3. Exit with non-zero status on failure: `sys.exit(1)`
4. Reference pattern: read `version-bump/main.py`

### Step 3: Implement Input Validation

For every action type, validate inputs at the entry point:
- Check required inputs are non-empty
- Validate format constraints (e.g., regex for version strings, allowed enum values)
- Provide clear error messages indicating what was wrong and what's expected
- For composite actions, use pattern from `check-permission/action.yml`:
  ```bash
  if [[ ! "$INPUT" =~ ^(allowed|values)$ ]]; then
    echo "::error::Invalid input; must be 'allowed' or 'values'"
    exit 1
  fi
  ```

### Step 4: Implement Error Handling

- Handle all expected failure modes described in SPEC.md
- Provide actionable error messages (not just "failed" — explain what went wrong and how to fix)
- For API calls, handle network errors, auth failures, and unexpected responses
- For file operations, handle missing files and permission errors

### Step 5: Update Test Workflow

Edit `.github/workflows/test-{action-name}.yml`:
1. Replace TODO comments with actual test scenarios
2. Provide realistic test inputs
3. Add output verification steps that check expected values
4. Add multiple test jobs if the action has different modes or configurations
5. Follow the multi-job pattern from `test-check-permission.yml` for actions with multiple modes

### Step 6: Build (TypeScript only)

For TypeScript actions:
1. Run `cd {action-name} && npm install`
2. Run `npm run build`
3. Verify `dist/index.js` was created
4. These files must be committed alongside the source

## Important Rules

- Write real, working code. No stubs, no TODOs, no placeholder comments in the final output.
- Follow the existing code style in the repository (Prettier will enforce formatting).
- Do NOT add unnecessary dependencies. Use the standard library where possible.
- Do NOT add features beyond what SPEC.md describes.
- For bash: always quote variables, use `set -e`, prefer `[[ ]]` over `[ ]`.
- For TypeScript: use strict types, handle undefined/null explicitly.
- For Python: use type hints where helpful, handle exceptions explicitly.
- Pass inputs through environment variables in composite actions, never inline in shell.
