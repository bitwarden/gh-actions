# Claude respond action

## Summary

Enables on-demand Claude Code responses in issues and pull requests. When a user with write permission mentions `@claude` in a comment, review, or issue body, this workflow retrieves a Bitwarden-managed Anthropic API key and runs Claude Code with the message as its prompt.

## Usage

See [`respond.yml`](./respond.yml) for a calling workflow template.

The calling workflow must pass the following secrets:

```yaml
jobs:
  respond:
    uses: bitwarden/gh-actions/.github/workflows/_respond.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
```

## Inputs

Secrets:

- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`

## Outputs

None

## Requirements

- The calling repository must have access to the `gh-org-bitwarden` Azure Key Vault, which contains the `ANTHROPIC-RESPONSE-API-KEY` secret used to authenticate with the Anthropic API.
- Only users with **write** permission on the repository can trigger a Claude response. Mentions from users without write access are silently skipped.

### GitHub Permissions

The calling workflow must grant the following GitHub permissions to the `_respond.yml` action:

| Permission | Access | Reason |
|---|---|---|
| `actions` | `read` | Read workflow run status for progress tracking |
| `contents` | `write` | Check out repo and commit changes if requested |
| `id-token` | `write` | Authenticate with Azure via OIDC |
| `issues` | `write` | Post and update comments on issues |
| `pull-requests` | `write` | Post and update comments on pull requests |

## Features

- Supports `@claude` mentions in issue comments, PR review comments, PR reviews, and issue bodies
- Uses a sticky comment — Claude updates a single comment rather than posting new ones
- Loads Bitwarden's internal plugins: `bitwarden-code-review`, `bitwarden-software-engineer`, `bitwarden-security-engineer`
- Claude's tool access is restricted to GitHub comment and PR diff tools only

## Special Considerations

- Claude runs with the **Opus** model and has a 10-minute timeout

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| No response after mentioning `@claude` | Actor lacks write permission, or `@claude` was not in the top-level comment/review body |
| Workflow fails at secret retrieval | Azure credentials are missing or the calling workflow did not pass the required secrets |
| Claude response stops mid-way | 10-minute job timeout was hit; consider breaking the request into smaller tasks |
