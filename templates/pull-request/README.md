# Pull Request and Pull Request Target Workflow Templates

Templates for safely handling internal and external fork pull requests in GitHub Actions workflows that require secrets, following Bitwarden security patterns.

## Overview

Different strategies are needed for internal vs. fork PRs when workflows require secrets:

- **Internal PRs**: Use `pull_request` trigger (runs with limited permissions, no secrets needed)
- **Fork PRs**: Use `pull_request_target` (runs in target repo context with approval gate for secret access)

## The Two-Workflow Pattern

### `example-workflow.yml` - Main Workflow

Contains actual job logic (build, test, deploy, etc.). Triggered by `pull_request` for internal PRs and `workflow_call` for reuse. Skips fork PRs via condition: `if: github.event.pull_request.head.repo.full_name == github.repository`

### `example-workflow-target.yml` - Fork Handler

Safely handles fork PRs needing secrets. Triggered by `pull_request_target` (targets default branch only). Runs `check-run` security gate first, then calls main workflow with `secrets: inherit`. Only executes for forks via condition: `if: github.event.pull_request.head.repo.full_name != github.repository`

## Security Model

**The Problem**: Fork PRs can't access secrets with `pull_request`, but `pull_request_target` runs untrusted code in your repo's context with secret access.

**The Solution**: Two-phase approval process:
1. `pull_request_target` workflow runs immediately for fork PRs
2. `check-run` job fails (fork user lacks write permissions)
3. Maintainer reviews code for malicious behavior
4. Maintainer re-runs workflow (passes check-run with maintainer identity, grants secret access)

**Protection Layers**:
- Permission check validates write access
- Conditional execution separates internal/fork paths
- Mandatory code review before secret access
- Workflow linter enforces `pull_request_target` targets default branch only and workflows include `check-run`

## ⚠️ Critical Security Warning

**ALWAYS review fork PR code BEFORE re-running failed workflows.** Once re-run, workflows access repository secrets and can exfiltrate data.

**Check for**:
- Uploads to external services
- Unexpected network requests
- Base64 encoding/obfuscation
- Secrets exposed in artifacts or logs

## Approval Process

**For `pull_request` (no secrets)**: Click "Approve and run" to unblock workflow execution.

**For `pull_request_target` (with secrets)**:
1. Workflow runs immediately, `check-run` fails (expected)
2. Review PR code thoroughly
3. Click "Re-run failed jobs" (grants secret access via maintainer identity)

## Usage Instructions

1. **Copy templates** to `.github/workflows/` and rename appropriately
2. **Customize main workflow**: Update name, paths, jobs, secrets, and inputs
3. **Customize target workflow**: Update name, workflow reference in `uses:`, paths, permissions, and inputs
4. **Test both scenarios**: Create internal PR (should trigger main workflow) and fork PR (should trigger target workflow with failed check-run)

## Best Practices

**DO**:
- Use `check-run` job first in `pull_request_target` workflows
- Review fork code before approving
- Set minimal permissions per job
- Pin actions to commit hashes
- Use conditions to separate internal/fork execution

**DON'T**:
- Skip `check-run` security gate
- Use `pull_request_target` unless secrets are required
- Grant unnecessary permissions
- Expose secrets in logs/outputs
- Run both workflows for same PR

## Troubleshooting

**Both workflows running for internal PR**: Check conditional expressions match template patterns.

**"Check PR run" failed (EXPECTED)**: This is the security gate working. Review code, then re-run to grant secret access.

**Secrets unavailable in fork PR**: Ensure using `pull_request_target` pattern with `secrets: inherit`.

**Workflow linter failing**: Verify `pull_request_target` targets default branch only.

**Compliance**: Templates comply with all Bitwarden workflow-linter rules (pinned runners/actions, explicit permissions, proper naming, `pull_request_target` restrictions).

## References

- [GitHub Actions: pull_request vs pull_request_target](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request_target)
- [Bitwarden Workflow Linter Rules](https://github.com/bitwarden/workflow-linter/tree/main/src/bitwarden_workflow_linter/rules)
- [Bitwarden Clients Example](https://github.com/bitwarden/clients/blob/main/.github/workflows/build-web-target.yml)
- [Keeping your GitHub Actions secure](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
