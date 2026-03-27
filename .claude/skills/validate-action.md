---
name: validate-action
description: "Run formatting, structural, and Bitwarden workflow linter compliance checks on a GitHub Action. Fixes issues directly and reports results."
argument-hint: "<action-name>"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(ls:*)
  - Bash(npx prettier:*)
---

# Validate Action - Correctness and Compliance Checks

Run formatting, structural, and Bitwarden workflow linter compliance checks on a GitHub Action in the Bitwarden `gh-actions` repository. The deliverable is a clean action with all fixable issues resolved and a validation summary reported directly to the user.

## Input

This skill accepts a single required argument: the action directory name.

The directory must contain `action.yml` and implementation files. A test workflow at `.github/workflows/test-{action-name}.yml` should also exist.

**Examples:**
- `validate-action report-deployment-status-to-slack`
- `validate-action check-permission`

## Procedure

### Step 1: Validate Prerequisites

1. Run `ls /Users/tyler/dev/gh-actions/{action-name}/` to confirm the directory exists.
2. If the directory does not exist, stop and report: "Directory {action-name}/ not found."
3. Read `{action-name}/action.yml`. If it does not exist, stop and report: "No action.yml found in {action-name}/. Run scaffold-action first."
4. Determine the action type from the `runs.using` field in action.yml (composite, node24, docker).
5. Check for the test workflow at `.github/workflows/test-{action-name}.yml`. If missing, record a Critical finding: "Missing test workflow."

### Step 2: Prettier Formatting

Run Prettier to check all action files and the test workflow:
```bash
npx prettier --check "/Users/tyler/dev/gh-actions/{action-name}/**"
npx prettier --check "/Users/tyler/dev/gh-actions/.github/workflows/test-{action-name}.yml"
```

If any files fail the check, fix them:
```bash
npx prettier --write "/Users/tyler/dev/gh-actions/{action-name}/**"
npx prettier --write "/Users/tyler/dev/gh-actions/.github/workflows/test-{action-name}.yml"
```

Record each file that required formatting as a Low finding.

### Step 3: action.yml Structure Validation

Read `{action-name}/action.yml` and verify all required fields. Use `Grep` to search for specific keys if needed.

- [ ] `name` -- present and descriptive
- [ ] `description` -- present and descriptive
- [ ] `author` -- set to `"Bitwarden"`
- [ ] `branding` -- has both `icon` and `color` properties
- [ ] `inputs` -- each input has `description` and `required` fields
- [ ] `outputs` -- each output has `description`; for composite actions, each also has `value`
- [ ] `runs` -- has correct `using` value for the action type (`composite`, `node24`, or `docker`)

**Severity for missing fields:**
- Missing `name`, `description`, or `runs`: **Critical**
- Missing `author` or `branding`: **Medium**
- Input/output missing `description` or `required`: **High**
- Composite output missing `value` reference: **Critical**

### Step 4: Bitwarden Workflow Linter Compliance

Read `.github/workflows/test-{action-name}.yml` and check it against each linter rule. Use `Grep` to search for specific patterns. Also read one existing test workflow (e.g., `.github/workflows/test-check-permission.yml`) as a reference for expected conventions and pinned SHAs.

**name_exists** -- every workflow and job must have a `name` field.
- [ ] Workflow has top-level `name:`
- [ ] Every job has a `name:` field
- Missing name: **High**

**name_capitalized** -- names must begin with a capital letter.
- [ ] Workflow name starts with uppercase
- [ ] All job names start with uppercase
- [ ] All step names start with uppercase
- Lowercase name: **Medium**

**permissions_exist** -- `permissions` key must be explicitly set.
- [ ] Workflow-level `permissions:` is present, OR every job has a `permissions:` key
- Missing permissions: **High**

**pinned_job_runner** -- runners must be pinned to specific versions.
- [ ] All `runs-on` values use pinned versions (e.g., `ubuntu-24.04`, NOT `ubuntu-latest`)
- Unpinned runner: **High**

**step_pinned** -- external actions must be pinned to commit SHA.
- [ ] All `uses:` references to external actions use `owner/repo@SHA # vX.Y.Z` format
- [ ] Local actions (`./action-name`) are exempt from pinning
- Use `Grep` with pattern `uses:` in the test workflow to find all action references
- Unpinned external action: **High**

**step_approved** -- only approved actions are used.
- [ ] Check all external `uses:` references against commonly approved actions: `actions/checkout`, `actions/upload-artifact`, `actions/download-artifact`
- [ ] If an unapproved action is found, record it as **High** and suggest alternatives
- Use `Grep` across existing test workflows to see which actions are commonly used in this repo

**underscore_outputs** -- multi-word output names must use underscores.
- [ ] All output names in `action.yml` use underscores (not hyphens)
- [ ] All output references in the test workflow use underscore format
- Hyphenated output name: **High**

**job_environment_prefix** -- environment variable naming conventions.
- [ ] Job-level environment variables follow Bitwarden naming conventions
- Non-conforming env var: **Medium**

**check_pr_target** -- if `pull_request_target` trigger is used, it must only run on the default branch.
- [ ] If present, verify it targets `main`
- Unrestricted pull_request_target: **Critical**

### Step 5: File Naming Conventions

- [ ] Action directory name is kebab-case (lowercase letters, numbers, hyphens only)
- [ ] Test workflow is named `test-{action-name}.yml`
- [ ] Source files follow language conventions (camelCase for TS, snake_case for Python)
- Non-conforming name: **Medium**

### Step 6: Fix Issues

Process all findings from Steps 2-5:

1. **Critical** and **High** issues: Fix directly using `Edit` or `Write`. After fixing, update the finding status to "Fixed."
2. **Medium** issues: Fix directly unless the fix requires a design decision. If so, set status to "Flagged" with an explanation.
3. **Low** issues: Do not fix. Set status to "Noted."
4. After all fixes, re-run Prettier to ensure fixed files are properly formatted:
   ```bash
   npx prettier --write "/Users/tyler/dev/gh-actions/{action-name}/**"
   npx prettier --write "/Users/tyler/dev/gh-actions/.github/workflows/test-{action-name}.yml"
   ```

### Step 7: Report Results

Print a validation summary directly to the user. Do NOT append results to SPEC.md — validation findings are mechanical and transient, not useful to downstream phases.

Use this format:

```
Validation complete for {action-name}: {PASS / PASS WITH NOTES / FAIL}

Findings:
| # | Severity | Category | Description | Status |
|---|----------|----------|-------------|--------|
| 1 | High | Linter Compliance | {description} | Fixed |
| 2 | Medium | Structure | {description} | Flagged |
| 3 | Low | Formatting | {description} | Noted |

Summary:
- Critical/High fixed: {count}
- Medium flagged: {count}
- Low noted: {count}
- Files modified: {list}
```

**Status criteria:**
- **PASS**: Zero findings, or all findings were Low/Noted.
- **PASS WITH NOTES**: All Critical/High fixed, some Medium flagged for user review.
- **FAIL**: Any Critical/High issue could not be fixed (e.g., unapproved action with no alternative).

**Zero-findings case:**

```
Validation complete for {action-name}: PASS

All formatting, structural, and linter compliance checks passed.
```

## Important Rules

- Fix all formatting and structural issues directly. Do not just report them.
- For linter compliance issues, fix them if possible. If a fix requires using an unapproved action, flag it to the user rather than removing the action.
- Always run Prettier AFTER making any fixes to ensure final files are formatted correctly.
- The pinned SHA for `actions/checkout` must match what other test workflows in the repo use. Read an existing test workflow (e.g., `test-check-permission.yml`) to get the current SHA.
- Do NOT change implementation logic. This skill only validates and fixes formatting, structure, and compliance.
- Do NOT add new features or refactor code. Focus strictly on correctness and compliance.
- Output names must use underscores, not hyphens (workflow linter requirement).
- Runners must be pinned to `ubuntu-24.04` (not `ubuntu-latest`).

## Related Skills

- **define-action**: Produces the SPEC.md that defines the action's requirements. Example: `define-action {action-name}`
- **scaffold-action**: Generates skeleton files from SPEC.md. Example: `scaffold-action {action-name}`
- **implement-action**: Replaces TODO placeholders with working code. Run before this skill. Example: `implement-action {action-name}`
- **evaluate-action**: Reviews implementation completeness against SPEC.md. Example: `evaluate-action {action-name}`
- **secure-action**: Security assessment and final quality gate. Run after this skill. Example: `secure-action {action-name}`
