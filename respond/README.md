# Claude respond action

## Summary

Enables on-demand Claude Code responses in issues and pull requests. When a user with write permission mentions `@claude` in a comment, review, or issue body, this workflow retrieves a Bitwarden-managed Anthropic API key and runs Claude Code with the message as its prompt.

## When to use it

Mention `@claude` to ask a question or make a request about a pull request or issue. Claude answers in a comment.

Do not ask Claude to write or commit code. This workflow is meant for answers only.

## How it works

The workflow runs three jobs in order. Each job runs only if the one before it passes.

1. **Check permission** confirms that the user who triggered the run has write permission on the repository. It uses [`check-permission`](../check-permission/README.md).
2. **Validation** confirms that the comment, review, or issue body mentions `@claude`.
3. **Claude comment** checks out the repo, retrieves the Anthropic API key, and runs Claude Code. Claude posts its answer in a comment.

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

| Permission      | Access  | Reason                                                               |
| --------------- | ------- | -------------------------------------------------------------------- |
| `actions`       | `read`  | Read workflow run status for progress tracking                       |
| `contents`      | `write` | Check out the repo and see the note below                            |
| `id-token`      | `write` | Authenticate with Azure and get the Claude GitHub App token via OIDC |
| `issues`        | `write` | Post and update comments on issues                                   |
| `pull-requests` | `write` | Post and update comments on pull requests                            |

`contents: write` may be more than the workflow needs. Checkout needs only `read`, and Claude's commits and pushes use the Claude GitHub App token. This is noted as a potential defect and will be investigated and resolved soon.

## Features

- Supports `@claude` mentions in issue comments, PR review comments, PR reviews, and issue bodies
- Uses a sticky comment — Claude updates a single comment rather than posting new ones
- Loads plugins from the [Bitwarden marketplace](https://github.com/bitwarden/ai-plugins): `bitwarden-code-review`, `bitwarden-software-engineer`, `bitwarden-security-engineer`, and `claude-config-validator`
- The workflow allows GitHub comment and PR diff tools. `claude-code-action` adds file reading, file edits in the checked-out repo, and git commit and push tools.

## Special Considerations

- Claude runs with the **Opus** model and has a 10-minute timeout

## Troubleshooting

| Symptom                                | Likely cause                                                                            |
| -------------------------------------- | --------------------------------------------------------------------------------------- |
| No response after mentioning `@claude` | Actor lacks write permission, or `@claude` was not in the top-level comment/review body |
| Workflow fails at secret retrieval     | Azure credentials are missing or the calling workflow did not pass the required secrets |
| Claude response stops mid-way          | 10-minute step timeout was hit; consider breaking the request into smaller tasks        |
