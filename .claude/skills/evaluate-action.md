---
name: evaluate-action
description: "Phase 4: Review completeness of a GitHub Action implementation. Checks inputs/outputs coverage, error handling, edge cases, and test scenarios."
---

# Evaluate Action - Phase 4: Completeness Review

You are evaluating a newly implemented GitHub Action in the Bitwarden `gh-actions` repository for completeness and correctness. The action has been defined, scaffolded, and implemented. Your job is to find gaps and fix them.

## Procedure

### Step 1: Read All Files

1. Read `{action-name}/SPEC.md` for requirements
2. Read `{action-name}/action.yml` for declared inputs/outputs
3. Read the implementation file(s):
   - Composite: the `run:` blocks in `action.yml`
   - TypeScript: `{action-name}/src/main.ts`
   - Docker: `{action-name}/main.py`
4. Read `.github/workflows/test-{action-name}.yml`

### Step 2: Input Coverage Audit

For every input declared in `action.yml`:
- [ ] Is it read by the implementation?
- [ ] Is a missing required input handled with a clear error?
- [ ] Is the default value applied when the input is optional and not provided?
- [ ] Is sensitive input data never logged or echoed?

Flag any input that is declared but unused, or used but undeclared.

### Step 3: Output Coverage Audit

For every output declared in `action.yml`:
- [ ] Is it set by the implementation in all code paths?
- [ ] Is the output value reference in `action.yml` correct (matches step ID)?
- [ ] Is sensitive output data masked before being set?

Flag any output that is declared but never set, or set inconsistently across code paths.

### Step 4: Error Handling Audit

- [ ] Does every external call (API, file I/O, subprocess) have error handling?
- [ ] Are error messages actionable (explain what went wrong and how to fix)?
- [ ] Does the action fail explicitly on unrecoverable errors (not silently succeed)?
- [ ] For composite actions: does the script use `set -e`?
- [ ] For TypeScript: is everything in a try/catch with `core.setFailed()`?
- [ ] For Python: is there a top-level exception handler?

### Step 5: Edge Case Review

Check for:
- [ ] Empty string inputs where non-empty is expected
- [ ] Whitespace-only inputs
- [ ] Inputs with special characters (spaces, quotes, newlines)
- [ ] Missing environment variables that are assumed to exist
- [ ] Actions that depend on runner state (installed tools, file system)
- [ ] Race conditions or ordering issues in multi-step composite actions

### Step 6: Test Workflow Review

- [ ] Does the test workflow exercise all required inputs?
- [ ] Does it test both success and failure paths?
- [ ] Does it verify outputs (not just "run and hope")?
- [ ] Are test inputs realistic, not just "test" or "foo"?
- [ ] Does each test job have a descriptive name (capitalized per linter rules)?
- [ ] Are there enough test jobs to cover different configurations/modes?

### Step 7: Report and Fix

For each finding:
1. Classify severity: **Critical** (action won't work), **High** (may fail in some cases), **Medium** (quality issue), **Low** (minor improvement)
2. Fix Critical and High issues directly
3. Fix Medium issues directly unless they require a design decision
4. Report Low issues to the user for consideration

Append a summary to SPEC.md under a `## Phase 4: Evaluation Results` section.

## Important Rules

- Read ALL files before making any judgments.
- Do NOT add new features. Only fix gaps in the existing specification.
- Do NOT refactor working code for style preferences.
- Fix issues directly rather than just reporting them, unless the fix requires a user decision.
- Focus on functional correctness, not code aesthetics.
