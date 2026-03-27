---
name: validate-action
description: "Phase 5: Run correctness and compliance checks on a GitHub Action. Validates formatting, structure, build, and Bitwarden workflow linter rules."
---

# Validate Action - Phase 5: Correctness and Compliance Checks

You are validating a GitHub Action in the Bitwarden `gh-actions` repository for formatting, structural correctness, and compliance with Bitwarden's workflow linter rules.

## Procedure

### Step 1: Prettier Formatting

Run Prettier on all generated files:
```bash
npx prettier --check "{action-name}/**"
npx prettier --check ".github/workflows/test-{action-name}.yml"
```

If any files fail, fix them:
```bash
npx prettier --write "{action-name}/**"
npx prettier --write ".github/workflows/test-{action-name}.yml"
```

### Step 2: action.yml Structure Validation

Verify the `action.yml` file contains all required fields:
- [ ] `name` — present and descriptive
- [ ] `description` — present and descriptive
- [ ] `author` — set to `"Bitwarden"`
- [ ] `branding` — has `icon` and `color`
- [ ] `inputs` — each has `description` and `required`
- [ ] `outputs` — each has `description` and `value` (for composite)
- [ ] `runs` — has correct `using` value for the action type

### Step 3: TypeScript Build Validation (if applicable)

For TypeScript actions:
1. Run `cd {action-name} && npm install && npm run build`
2. Verify `dist/index.js` exists and is non-empty
3. Verify `action.yml` `main` field points to the correct compiled file

### Step 4: Bitwarden Workflow Linter Compliance

Check the test workflow `.github/workflows/test-{action-name}.yml` against all linter rules:

**name_exists**: Every workflow and job has a `name` field.
- [ ] Workflow has top-level `name:`
- [ ] Every job has a `name:` field

**name_capitalized**: Names begin with a capital letter.
- [ ] Workflow name starts with uppercase
- [ ] All job names start with uppercase
- [ ] All step names start with uppercase

**permissions_exist**: `permissions` key is explicitly set.
- [ ] Workflow-level `permissions:` is present, OR
- [ ] Every job has a `permissions:` key

**pinned_job_runner**: Runners are pinned to specific versions.
- [ ] All `runs-on` values use pinned versions (e.g., `ubuntu-24.04`, NOT `ubuntu-latest`)

**step_pinned**: External actions are pinned to commit SHA.
- [ ] All `uses:` references to external actions use `owner/repo@SHA # vX.Y.Z` format
- [ ] Local actions (`./action-name`) are exempt from pinning

**step_approved**: Only approved actions are used.
- [ ] Check all external `uses:` references against Bitwarden's approved actions list
- [ ] Common approved actions: `actions/checkout`, `actions/upload-artifact`, `actions/download-artifact`
- [ ] If an unapproved action is used, flag it and suggest alternatives

**underscore_outputs**: Outputs use underscores.
- [ ] All output names in `action.yml` use underscores (not hyphens) for multi-word names
- [ ] All output references in workflow files use underscore format

**job_environment_prefix**: Environment variable naming conventions.
- [ ] Job-level environment variables follow Bitwarden naming conventions

**check_pr_target**: If `pull_request_target` trigger is used, it only runs on default branch.

### Step 5: File Naming Convention

- [ ] Action directory is kebab-case
- [ ] Test workflow is named `test-{action-name}.yml`
- [ ] Source files follow language conventions (camelCase for TS, snake_case for Python)

### Step 6: Report Results

Append a summary to SPEC.md under a `## Phase 5: Validation Results` section listing:
- All checks passed
- Any issues found and how they were resolved
- Any remaining issues that need manual attention

## Important Rules

- Fix all formatting and structural issues directly. Do not just report them.
- For linter compliance issues, fix them if possible. If the fix requires using an unapproved action, flag it to the user.
- Always run Prettier AFTER making any fixes to ensure final files are formatted.
- The pinned SHA for `actions/checkout` should match what other test workflows in the repo use. Read an existing test workflow to get the current SHA.
