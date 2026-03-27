---
name: implement-action
description: "Replace TODO placeholders in a scaffolded GitHub Action with working implementation code, input validation, error handling, and test scenarios."
argument-hint: "<action-name>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(ls:*)
  - Bash(cd * && npm install)
  - Bash(cd * && npm run build)
---

# Implement Action - Core Logic Development

Replace TODO placeholders in a scaffolded GitHub Action with working code. The action must already have a `SPEC.md` (from define-action) and scaffolded skeleton files (from scaffold-action). The deliverable is a fully functional action with no remaining TODOs.

## Input

This skill accepts a single required argument: the action directory name.

The directory must already contain `SPEC.md` and scaffolded files with TODO placeholders.

**Examples:**
- `implement-action report-deployment-status-to-slack`
- `implement-action check-permission`

## Procedure

### Step 1: Validate Prerequisites

1. Run `ls /Users/tyler/dev/gh-actions/{action-name}/` to confirm the directory exists.
2. If the directory does not exist, stop and report: "Directory {action-name}/ not found. Run define-action and scaffold-action first."
3. Read `{action-name}/SPEC.md` for the full requirements specification.
4. If SPEC.md does not exist, stop and report: "No SPEC.md found in {action-name}/. Run define-action first."
5. Read all scaffolded files in the `{action-name}/` directory to understand what was generated.
6. If scaffolded files contain no TODO placeholders, stop and report: "Scaffolded files appear to already be implemented. Run evaluate-action to review completeness instead."

### Step 2: Read Reference Implementations

Use `Glob` with pattern `*/action.yml` to list existing actions. Identify 1-2 similar actions based on the SPEC.md requirements (same type, similar integrations). Read their implementation files to learn current patterns.

**Minimum required references by type:**

- **Composite**: Read `check-permission/action.yml` for input validation, env block usage, and output setting.
- **TypeScript**: Read `get-keyvault-secrets/src/main.ts` for input reading, secret masking, error handling, and output setting.
- **Docker/Python**: Read `version-bump/main.py` for environment variable input reading, output writing, and error handling.

### Step 3: Implement Core Logic

**For Composite actions** -- edit `{action-name}/action.yml`:
1. Replace placeholder steps with real implementation.
2. Use `env:` blocks to pass all inputs to shell scripts (never inline `${{ inputs.* }}` in `run:` -- this is a command injection vector).
3. Use `set -e` at the top of every bash `run:` block.
4. Write outputs using `echo "name=value" >> "$GITHUB_OUTPUT"`.
5. Use `::error::`, `::warning::`, `::notice::` annotations for user-facing messages.
6. Always quote shell variables: `"$VAR"` not `$VAR`.

**For TypeScript actions** -- edit `{action-name}/src/main.ts`:
1. Import `@actions/core` and any packages needed per SPEC.md integrations.
2. Read inputs with `core.getInput('name', { required: true/false })`.
3. Mask sensitive values with `core.setSecret(value)` before any logging.
4. Set outputs with `core.setOutput('name', value)`.
5. Wrap the entire `run()` body in try/catch with `core.setFailed()` in the catch block.

**For Docker/Python actions** -- edit `{action-name}/main.py`:
1. Read inputs from environment: `os.getenv("INPUT_NAME")` (GitHub uppercases and prefixes with `INPUT_`).
2. Write outputs by appending to the file at `os.getenv("GITHUB_OUTPUT")`.
3. Exit with non-zero status on failure: `sys.exit(1)`.
4. Use `subprocess.run()` with argument lists, never `shell=True` with untrusted input.

### Step 4: Implement Input Validation

At the entry point of every action, validate all inputs before any business logic runs:
- Check required inputs are non-empty.
- Validate format constraints (e.g., regex for version strings, allowed enum values).
- Validate file path inputs against directory traversal (`../`, absolute paths where relative expected).
- Provide clear error messages: what was wrong, what format is expected.

**Composite pattern** (from `check-permission/action.yml`):
```bash
if [[ -z "$INPUT_NAME" ]]; then
  echo "::error::Input 'input_name' is required but was empty."
  exit 1
fi
if [[ ! "$INPUT_VALUE" =~ ^(allowed|values)$ ]]; then
  echo "::error::Input 'input_value' must be 'allowed' or 'values', got '$INPUT_VALUE'"
  exit 1
fi
```

**TypeScript pattern**: Validate after `core.getInput()`, throw descriptive errors.

**Python pattern**: Validate after `os.getenv()`, call `sys.exit(1)` with a printed error.

### Step 5: Implement Error Handling

- Handle all expected failure modes described in SPEC.md.
- For API calls: handle network errors, auth failures, rate limits, and unexpected response shapes.
- For file operations: handle missing files, permission errors, and malformed content.
- Provide actionable error messages (not just "failed" -- explain what went wrong and suggest a fix).
- Never expose sensitive data in error messages (tokens, secrets, internal URLs).

### Step 6: Update Test Workflow

Read `.github/workflows/test-{action-name}.yml`, then edit it:
1. Replace TODO comments with actual test scenarios from SPEC.md.
2. Provide realistic test inputs (not "test" or "foo").
3. Add output verification steps that assert expected values using `env:` blocks.
4. Add multiple test jobs if the action has distinct modes or configurations.
5. Ensure each test job has a descriptive, capitalized name (workflow linter requirement).
6. Reference the multi-job pattern from `.github/workflows/test-check-permission.yml` if needed.

### Step 7: Build (TypeScript Only)

For TypeScript actions only:
1. Run `cd {action-name} && npm install` to install dependencies.
2. Run `cd {action-name} && npm run build` to compile.
3. Verify `dist/index.js` was created with `ls {action-name}/dist/index.js`.
4. The compiled `dist/` files must be committed alongside the source.

Skip this step for Composite and Docker actions.

### Step 8: Report Results

List all files modified and summarize what was implemented:

```
Implementation complete for {action-name}:

Modified files:
  - {action-name}/action.yml -- core logic, input validation, output setting
  - {action-name}/src/main.ts -- (TypeScript only) full implementation
  - {action-name}/main.py -- (Docker only) full implementation
  - .github/workflows/test-{action-name}.yml -- test scenarios and assertions

Remaining TODOs: {count, should be 0}

Next step: Run evaluate-action to review completeness:
  evaluate-action {action-name}
```

If any TODOs remain that could not be resolved (e.g., require external credentials or infrastructure not available locally), list them explicitly with the reason.

## Important Rules

- Write real, working code. No stubs, no TODOs, no placeholder comments in the final output.
- Do NOT add features beyond what SPEC.md describes. Implement exactly the specification.
- Do NOT add unnecessary dependencies. Use the standard library where possible.
- Follow the existing code style in the repository (Prettier will enforce formatting on commit).
- Pass inputs through `env:` blocks in composite actions -- never inline `${{ inputs.* }}` in `run:` commands.
- For bash: always quote variables, use `set -e`, prefer `[[ ]]` over `[ ]`.
- For TypeScript: use strict types, handle undefined/null explicitly.
- For Python: use type hints where helpful, handle exceptions explicitly.
- Never log, echo, or print sensitive values. Mask them before any output.
- Output names must use underscores, not hyphens (workflow linter requirement).

## Related Skills

- **define-action**: Produces the SPEC.md this skill consumes. Run it first if no SPEC.md exists. Example: `define-action {action-name}`
- **scaffold-action**: Generates the skeleton files this skill fills in. Run it after define-action. Example: `scaffold-action {action-name}`
- **evaluate-action**: Reviews completeness of the implementation. Run after this skill. Example: `evaluate-action {action-name}`
- **validate-action**: Checks formatting, structure, and linter compliance. Example: `validate-action {action-name}`
