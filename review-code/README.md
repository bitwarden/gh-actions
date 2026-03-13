# Claude review code

## Summary

Enables on-demand Claude Code review on Pull Request in GitHub by adding `ai-review` label.

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
- Only users with **write** permission on the repository can trigger a Claude response. Mentions from users without write access are silently skipped.

### GitHub Permissions

The calling workflow must grant the following GitHub permissions to the `_respond.yml` action:

| Permission | Access | Reason |
|---|---|---|
| `actions` | `read` | Read workflow run status for progress tracking |
| `contents` | `read` | Check out repo and commit changes if requested |
| `id-token` | `write` | Authenticate with Azure via OIDC |
| `pull-requests` | `write` | Post and update comments on pull requests |

## Features

- Triggers automatically when the `ai-review` label is added to a pull request
- Uses a sticky comment — Claude updates a single comment rather than posting new ones
- Loads Bitwarden's internal plugins: `bitwarden-code-review`, `bitwarden-software-engineer`, `bitwarden-security-engineer`
- Claude's tool access includes file reading (`Read`, `Grep`, `Glob`), git history (`git diff`, `git log`, `git show`), and PR interaction (`gh pr view/diff/checks`, inline comments)

## Special Considerations

- Claude runs with the **Opus** model
- The Claude step has a **10-minute timeout**; the overall review job has a **15-minute timeout**

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| No review after adding `ai-review` label | Actor lacks write permission, or the calling workflow does not trigger on `labeled` events |
| Workflow fails at secret retrieval | Azure credentials are missing or the calling workflow did not pass the required secrets |
| Claude response stops mid-way | 10-minute step timeout was hit; consider breaking the request into smaller tasks |
