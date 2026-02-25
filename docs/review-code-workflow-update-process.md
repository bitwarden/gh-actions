# Review Code Workflow

## Overview

Bitwarden uses Claude Code for AI-assisted code reviews on pull requests. Reviews are triggered by PR labels and executed through a reusable GitHub Actions workflow (`_review-code.yml`).

The system uses a **dual-track model** with two composite actions:

- **`review-code/`** (current/stable) -- the default review path, triggered by the `ai-review` label.
- **`review-code-vnext/`** (experimental) -- the next-version path, triggered by the `ai-review-vnext` label.

This lets engineers beta test review changes (prompt updates, plugin changes, model switches) on individual PRs before rolling them out to all repos.

## Architecture

```
_review-code.yml (reusable workflow)
  |
  +-- check-permission job
  |     Verifies the PR author has write permission to the repo.
  |
  +-- validation job
  |     Reads PR labels. Outputs review_variant:
  |       - "vnext"   if ai-review-vnext label is present
  |       - "current" if ai-review label is present
  |       - skips     if neither label is present
  |
  +-- review job
        Step-level routing based on review_variant:
          - "current" -> review-code/action.yml
          - "vnext"   -> review-code-vnext/action.yml
```

**Label precedence:** If both labels are present, `ai-review-vnext` wins. It represents a deliberate manual choice and overrides the default.

**At rest:** Both composite actions are byte-for-byte identical. They only diverge during active vnext development.

## Composite Action Reference

### Inputs

| Name                    | Required | Description                                     |
| ----------------------- | -------- | ----------------------------------------------- |
| `azure_subscription_id` | Yes      | Azure Subscription ID for OIDC authentication   |
| `azure_tenant_id`       | Yes      | Azure Tenant ID for OIDC authentication         |
| `azure_client_id`       | Yes      | Azure Client ID for OIDC authentication         |
| `pr_number`             | Yes      | Pull request number to review                   |
| `repository`            | Yes      | Repository in `owner/repo` format               |
| `checkout_ref`          | Yes      | Git ref to checkout (typically the PR head SHA) |
| `github_token`          | Yes      | GitHub token for API access                     |

### Required Job Permissions

The calling job must declare these permissions:

```yaml
permissions:
  actions: read
  contents: read
  id-token: write
  pull-requests: write
```

### Notes

- The Key Vault name and secret name are hardcoded inside the composite actions, not configurable via inputs.
- `timeout-minutes` cannot be set inside composite actions. The calling workflow sets a 15-minute job-level timeout as the safety net.

## Development Lifecycle

Process for changing the AI code review behavior.

### 1. Starting state

Both `review-code/action.yml` and `review-code-vnext/action.yml` are byte-for-byte identical.

### 2. Identify a change

An engineer identifies a needed change -- switching from tag mode to agent mode, updating plugins, changing the prompt, etc.

### 3. Branch and modify vnext

Create a branch. Modify **only** `review-code-vnext/action.yml`. Never touch `review-code/action.yml` during this phase.

### 4. PR and merge to main

Open a PR with the vnext changes, get it reviewed, and merge. At this point the two files differ on `main`.

### 5. Beta testing

On any PR in any downstream repo, swap the `ai-review` label for `ai-review-vnext`. The workflow routes to the vnext composite action. Compare review quality against the current track. Swap back anytime -- zero risk to production reviews.

### 6. Iterate

If vnext needs tweaks, repeat steps 3-5. Each iteration is a clean diff against the vnext action only.

### 7. Approval

After sufficient testing across multiple PRs and repos, the team agrees vnext is ready for promotion.

### 8. Promote

Copy `review-code-vnext/action.yml` to `review-code/action.yml`:

```bash
cp review-code-vnext/action.yml review-code/action.yml
```

A literal copy -- no edits needed since the files have no differentiating metadata. Open a PR for this change.

### 9. Merge the promotion PR

Both actions are identical again on `main`.

### 10. At rest

Cycle complete. Both actions are byte-for-byte identical, ready for the next change.

## Important Notes

- Both composite actions **must** remain byte-for-byte identical when the system is at rest (between development cycles).
- Never modify `review-code/action.yml` directly -- always go through the vnext cycle.
- The two files should only differ during active vnext development and testing.
