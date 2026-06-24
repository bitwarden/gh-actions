# Claude review code

## Summary

Runs an automated Claude Code review on pull requests. Reviews fire automatically when a PR is opened, converted from draft, or reopened (safety net), and can be triggered on demand by adding the `ai-review` label.

## Usage

See [`review-code.yml`](./review-code.yml) for a calling workflow template.

The calling workflow must pass the following secrets:

```yaml
jobs:
  respond:
    uses: bitwarden/gh-actions/.github/workflows/_review-code.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
    permissions:
      actions: read
      contents: read
      pull-requests: write
      id-token: write
```

## Inputs

Secrets:

- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`

## Outputs

None

## Requirements

- The calling repository must have access to the `gh-org-bitwarden` Azure Key Vault, which contains the `ANTHROPIC-CODE-REVIEW-API-KEY` secret used to authenticate with the Anthropic API.
- Only users with **write** permission on the repository can trigger a review. Requests from users without write access are silently skipped.
- The `ai-review` and `ai-review-vnext` labels must exist in the calling repository.

### GitHub Permissions

The calling workflow must grant the following GitHub permissions to the `_review-code.yml` action:

| Permission      | Access  | Reason                                         |
| --------------- | ------- | ---------------------------------------------- |
| `actions`       | `read`  | Read workflow run status for progress tracking |
| `contents`      | `read`  | Check out repo to read code for review         |
| `id-token`      | `write` | Authenticate with Azure via OIDC               |
| `pull-requests` | `write` | Post and update comments on pull requests      |

## Features

- **Safety net**: Runs automatically when a PR is opened, converted from draft, or reopened — no label required. Skips if a review comment already exists (idempotency guard).
- **On-demand label triggers**: Adding `ai-review` runs the current review variant; `ai-review-vnext` runs the next-generation variant. Label triggers bypass draft status and the idempotency guard.
- Uses a sticky comment — Claude updates a single comment rather than posting new ones
- Loads Bitwarden's internal plugins: `bitwarden-code-review`, `bitwarden-software-engineer`, `bitwarden-security-engineer`, and `claude-config-validator`
- Claude's tool access includes file reading (`Read`, `Grep`, `Glob`), git history (`git diff`, `git log`, `git show`), and PR interaction (`gh pr view/diff/checks`, inline comments)

## Special Considerations

- Claude runs with the **Opus** model
- The Claude step has a **10-minute timeout**; the overall review job has a **15-minute timeout**

## Troubleshooting

| Symptom                                  | Likely cause                                                                                                                              |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| No review when PR is opened              | The calling workflow does not trigger on `opened`, `ready_for_review`, and `reopened` events — copy the latest `review-code.yml` template |
| No review after adding `ai-review` label | Actor lacks write permission, or the calling workflow does not trigger on `labeled` events                                                |
| Safety net ran but review was skipped    | A sticky comment with the review marker already exists from a prior run (idempotency guard)                                               |
| Review skipped on a draft PR             | Expected — the safety net does not run on drafts. Add the `ai-review` label to force a review on a draft.                                 |
| Workflow fails at secret retrieval       | Azure credentials are missing or the calling workflow did not pass the required secrets                                                   |
| Claude response stops mid-way            | 10-minute step timeout was hit; consider breaking the request into smaller tasks                                                          |
