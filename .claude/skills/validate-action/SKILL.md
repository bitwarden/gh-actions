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
  - Bash(bwwl lint:*)
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

1. Run `ls {action-name}/` to confirm the directory exists.
2. If the directory does not exist, stop and report: "Directory {action-name}/ not found."
3. Read `{action-name}/action.yml`. If it does not exist, stop and report: "No action.yml found in {action-name}/. Run scaffold-action first."
4. Determine the action type from the `runs.using` field in action.yml (composite, node24, docker).
5. Check for the test workflow at `.github/workflows/test-{action-name}.yml`. If missing, record a Critical finding: "Missing test workflow."

### Step 2: Prettier Formatting

Run Prettier to check all action files and the test workflow:
```bash
npx prettier --check "{action-name}/**"
npx prettier --check ".github/workflows/test-{action-name}.yml"
```

If any files fail the check, fix them:
```bash
npx prettier --write "{action-name}/**"
npx prettier --write ".github/workflows/test-{action-name}.yml"
```

Record each file that required formatting as a Low finding.

### Step 3: action.yml Structure Validation

Read `{action-name}/action.yml` and verify all required fields. Use `Grep` to search for specific keys if needed.

- [ ] `name` -- present, descriptive, and starts with a capital letter
- [ ] `description` -- present and descriptive
- [ ] `author` -- set to `"Bitwarden"`
- [ ] `inputs` -- each input has `description` and `required` fields; multi-word names use underscores (not hyphens)
- [ ] `outputs` -- each output has `description`; for composite actions, each also has `value`; multi-word names use underscores (not hyphens)
- [ ] `runs` -- has correct `using` value for the action type (`composite`, `node24`, or `docker`)

**Severity for missing fields:**
- Missing `name`, `description`, or `runs`: **Critical**
- Missing `author`: **Medium**
- Input/output missing `description` or `required`: **High**
- Composite output missing `value` reference: **Critical**
- `name` does not start with a capital letter: **Medium**
- Input or output name uses hyphens instead of underscores: **High**

### Step 4: Bitwarden Workflow Linter Compliance

Run the Bitwarden Workflow Linter (`bwwl`) against the test workflow. This is the authoritative source for linting rules — do not reimplement its checks manually.

```bash
bwwl lint -f .github/workflows/test-{action-name}.yml
```

If `bwwl` is available:
1. Run it and capture the output.
2. Record each reported violation as a finding. Map severity from the linter output:
   - Violations that would block PR merge: **High**
   - Warnings: **Medium**
3. Fix each violation directly using `Edit`, then re-run `bwwl lint` to confirm the fix.

If `bwwl` is not available (command not found):
1. Report to the user: "`bwwl` is not installed. Install with `pip install bitwarden_workflow_linter`. Falling back to manual checks."
2. Read `.github/workflows/test-{action-name}.yml` and manually check the following rules. Also read one existing test workflow (e.g., `.github/workflows/test-check-permission.yml`) as a reference for expected conventions and pinned SHAs.

   - **name_exists**: Workflow and every job must have a `name` field. Missing: **High**
   - **name_capitalized**: Workflow, job, and step names must start with a capital letter. Lowercase: **Medium**
   - **permissions_exist**: `permissions` key must be set at workflow level or on every job. Missing: **High**
   - **pinned_job_runner**: `runs-on` must use pinned versions (e.g., `ubuntu-24.04`, not `ubuntu-latest`). Unpinned: **High**
   - **step_pinned**: External `uses:` must be pinned to SHA with version comment (`owner/repo@SHA # vX.Y.Z`). Local actions exempt. Unpinned: **High**
   - **step_approved**: Only approved external actions are used. Unapproved: **High**
   - **underscore_outputs**: Multi-word output names must use underscores, not hyphens. Hyphenated: **High**
   - **job_environment_prefix**: Job-level env vars follow Bitwarden naming conventions. Non-conforming: **Medium**
   - **check_pr_target**: `pull_request_target` trigger must only run on default branch. Unrestricted: **Critical**

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
   npx prettier --write "{action-name}/**"
   npx prettier --write ".github/workflows/test-{action-name}.yml"
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
