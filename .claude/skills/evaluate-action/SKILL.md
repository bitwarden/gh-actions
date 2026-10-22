---
name: evaluate-action
description: "Review a GitHub Action implementation for completeness. Audits input/output coverage, error handling, edge cases, and test scenarios against its SPEC.md."
argument-hint: "<action-name>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(ls:./*)
---

# Evaluate Action - Completeness Review

Review a fully implemented GitHub Action in the Bitwarden `gh-actions` repository for completeness and correctness. The action must have been defined (SPEC.md), scaffolded, and implemented. The deliverable is a findings report appended to SPEC.md, with Critical and High issues fixed directly.

## Input

This skill accepts a single required argument: the action directory name.

The directory must contain `SPEC.md`, `action.yml`, implementation files, and a test workflow.

**Examples:**
- `evaluate-action report-deployment-status-to-slack`
- `evaluate-action check-permission`

## Procedure

### Step 1: Validate Prerequisites

1. Run `ls {action-name}/` to confirm the directory exists.
2. If the directory does not exist, stop and report: "Directory {action-name}/ not found. Run define-action and scaffold-action first."
3. Read `{action-name}/SPEC.md` for the full requirements specification.
4. If SPEC.md does not exist, stop and report: "No SPEC.md found in {action-name}/. Run define-action first."
5. Read `{action-name}/action.yml` for declared inputs and outputs.
6. If action.yml does not exist, stop and report: "No action.yml found in {action-name}/. Run scaffold-action first."
7. Determine the action type from the `runs.using` field in action.yml.
8. Read the implementation file(s):
   - Composite: the `run:` blocks are inline in `action.yml` (already read).
   - TypeScript: Read `{action-name}/src/main.ts`.
   - Docker: Read `{action-name}/main.py`.
9. Read `.github/workflows/test-{action-name}.yml`. If it does not exist, record a Critical finding: "Missing test workflow."
10. Use `Grep` to search for remaining `TODO` comments across all files in `{action-name}/`. If any TODOs remain, record them as findings (severity depends on context).

### Step 2: Input Coverage Audit

For every input declared in `action.yml`, use `Grep` to search for its name in the implementation files. Verify:

- [ ] The input is read by the implementation (grep for the input name in implementation files).
- [ ] A missing required input is handled with a clear error message (check for validation logic near where the input is read).
- [ ] The default value declared in action.yml is consistent with any defaults in the implementation.
- [ ] Sensitive input data (per SPEC.md) is never logged, echoed, or printed (grep for `echo`, `console.log`, `print` near the input name).

**Flag as findings:**
- Input declared in action.yml but never read by implementation: **High** severity.
- Input read by implementation but not declared in action.yml: **Critical** severity.
- Required input with no validation for empty/missing value: **High** severity.
- Sensitive input appearing in log/echo/print statements: **Critical** severity.

### Step 3: Output Coverage Audit

For every output declared in `action.yml`, use `Grep` to search for where it is set in the implementation. Verify:

- [ ] The output is set by the implementation (grep for the output name in implementation files).
- [ ] The output is set in all code paths (check conditional branches).
- [ ] For composite actions: the `value` field in action.yml correctly references the step ID that sets it.
- [ ] Sensitive output data (per SPEC.md) is masked before being set.

**Flag as findings:**
- Output declared but never set: **Critical** severity.
- Output set in some code paths but not others: **High** severity.
- Output value reference in action.yml does not match step ID: **Critical** severity.
- Sensitive output not masked: **High** severity.

### Step 4: Error Handling Audit

Read through the implementation and verify error handling at each external interaction:

- [ ] Every external call (API, file I/O, subprocess) has error handling. Use `Grep` to find calls like `fetch`, `exec`, `subprocess`, `curl`, `az`, `gh`, then verify each has a surrounding try/catch, `|| exit 1`, or equivalent.
- [ ] Error messages are actionable (explain what went wrong and suggest a fix).
- [ ] The action fails explicitly on unrecoverable errors (not silently succeeding).
- [ ] For composite actions: every bash `run:` block starts with `set -e`.
- [ ] For TypeScript: the `run()` function is wrapped in try/catch with `core.setFailed()`.
- [ ] For Python: there is a top-level exception handler that calls `sys.exit(1)`.

**Flag as findings:**
- External call with no error handling: **High** severity.
- Silent failure (error caught but action reports success): **Critical** severity.
- Missing `set -e` in composite bash blocks: **Medium** severity.
- Generic error messages ("An error occurred"): **Medium** severity.

### Step 5: Edge Case Review

Check the implementation for handling of these common edge cases:

- [ ] Empty string inputs where non-empty is expected.
- [ ] Whitespace-only inputs (check if validation trims before checking).
- [ ] Inputs with special characters (spaces, quotes, newlines) -- especially in bash variable expansions.
- [ ] Missing environment variables that are assumed to exist (e.g., `GITHUB_OUTPUT`, `GITHUB_TOKEN`).
- [ ] Actions that depend on runner state (installed tools, file system paths).
- [ ] Race conditions or ordering issues in multi-step composite actions.

**Flag as findings:**
- Unquoted variable expansion in bash (`$VAR` instead of `"$VAR"`): **High** severity.
- Missing check for required environment variable: **Medium** severity.
- Assumption about runner tool availability without checking: **Low** severity.

### Step 6: Test Workflow Review

Read `.github/workflows/test-{action-name}.yml` and verify test coverage:

- [ ] The test workflow exercises all required inputs.
- [ ] Both success and failure paths are tested (at least one job that expects success and one that expects failure where applicable).
- [ ] Output verification steps assert expected values (not just "run and hope").
- [ ] Test inputs are realistic, not placeholder values like "test" or "foo".
- [ ] Each test job has a descriptive name that starts with a capital letter (workflow linter requirement).
- [ ] There are enough test jobs to cover different configurations or modes described in SPEC.md.

**Flag as findings:**
- No output verification in any test job: **High** severity.
- Required input not covered by any test: **Medium** severity.
- Only success path tested, no failure path: **Medium** severity.
- Placeholder test inputs: **Low** severity.

### Step 7: README Completeness Review

Read `{action-name}/README.md` and verify it is a complete, accurate artifact:

- [ ] README exists and is not empty.
- [ ] Every input declared in `action.yml` appears in the Inputs table.
- [ ] Every output declared in `action.yml` appears in the Outputs table.
- [ ] At least one usage example exists with realistic values (not placeholders).
- [ ] No TODO comments or placeholder text remains.
- [ ] Section ordering follows the structure established by scaffold-action (Title, Description, Features, Inputs, Outputs, Usage, supplementary sections).

**Flag as findings:**
- Missing README or empty file: **Critical** severity.
- Input or output in action.yml but missing from README table: **High** severity.
- No usage examples: **High** severity.
- Remaining TODO or placeholder text: **Medium** severity.
- Section ordering does not match scaffold structure: **Low** severity.

### Step 8: Fix Issues

Process all findings collected in Steps 2-7:

1. **Critical** and **High** issues: Fix directly using `Edit` or `Write`. After fixing, update the finding status to "Fixed."
2. **Medium** issues: Fix directly unless the fix requires a design decision that should be made by the user. If so, set status to "Flagged" with an explanation.
3. **Low** issues: Do not fix. Report to the user for consideration. Set status to "Noted."

### Step 9: Report Results

Append a summary to `{action-name}/SPEC.md` under a `## Phase 4: Evaluation Results` heading using this exact format:

```markdown
## Phase 4: Evaluation Results

### Status: PASS / PASS WITH NOTES / FAIL

### Findings
| # | Severity | Category | Description | Status |
|---|----------|----------|-------------|--------|
| 1 | Critical | Input Coverage | {description} | Fixed |
| 2 | High | Error Handling | {description} | Fixed |
| 3 | Medium | Test Coverage | {description} | Flagged |
| 4 | Low | Edge Cases | {description} | Noted |

### Summary
- **Critical/High fixed**: {count}
- **Medium flagged**: {count}
- **Low noted**: {count}
- **Overall**: {brief assessment}
```

**Zero-findings case:** If all checks pass with no findings:

```markdown
## Phase 4: Evaluation Results

### Status: PASS

### Findings
No issues found.

### Summary
All inputs, outputs, error handling, edge cases, and test scenarios verified against SPEC.md. Implementation is complete.
```

After appending the report, print a summary to the user listing files modified and the finding counts.

## Important Rules

- Read ALL files before making any judgments. Do not flag issues based on partial information.
- Do NOT add new features. Only fix gaps relative to the existing SPEC.md specification.
- Do NOT refactor working code for style preferences. Focus on functional correctness.
- Fix Critical and High issues directly rather than just reporting them.
- Never introduce security regressions when fixing issues (e.g., do not inline `${{ inputs.* }}` in `run:` blocks).
- If a fix would change the action's external interface (inputs, outputs, behavior), flag it to the user instead of fixing silently.

## Related Skills

- **define-action**: Produces the SPEC.md this skill evaluates against. Example: `define-action {action-name}`
- **scaffold-action**: Generates skeleton files from SPEC.md. Example: `scaffold-action {action-name}`
- **implement-action**: Replaces TODO placeholders with working code. Run before this skill. Example: `implement-action {action-name}`
- **validate-action**: Checks formatting, structure, and linter compliance. Run after this skill. Example: `validate-action {action-name}`
