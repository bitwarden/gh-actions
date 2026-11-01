# Classify Owning Team

Runs the `owning-team-classifier` agent from the [`bitwarden-owning-team-review`](https://github.com/bitwarden/ai-plugins/tree/main/plugins/bitwarden-owning-team-review) plugin on a pull request, and posts the result as a sticky PR comment. The comment shows which owning teams the change needs and why, with feedback checkboxes for each team.

This action runs in evaluation mode. It sets no status and requests no reviewers, so CODEOWNERS still decides who must approve. Team handles appear in code spans, so the comment notifies no team.

The action also checks whether the `BW-GHAPP` GitHub App could request each owning team as a reviewer, without requesting anyone. It mints an App token with organization Members read access, resolves each team, and reads the team's permission on the repository. When the App lacks Members read access, the token cannot be minted, and the comment says so.

## Inputs

- Required
  - azure_subscription_id
    - Description: Azure Subscription ID for OIDC authentication.
  - azure_tenant_id
    - Description: Azure Tenant ID for OIDC authentication.
  - azure_client_id
    - Description: Azure Client ID for OIDC authentication.
  - pr_number
    - Description: Pull request number to classify.
  - repository
    - Description: Repository in `owner/repo` format.
  - github_token
    - Description: GitHub token for reading the pull request and posting the comment.
- Optional
  - plugin_ref
    - Description: Ref of `bitwarden/ai-plugins` to run the plugin from.
    - Default: `main`
  - claude_code_version
    - Description: Exact version of `@anthropic-ai/claude-code` to run the classifier with.
    - Default: `2.1.308`

## Required Permissions

```yaml
permissions:
  contents: read
  id-token: write
  pull-requests: write
```

## Security

- The agent has only `Read`, `Grep`, and `Glob`, scoped to the prepared context and the plugin. Every `gh` and `git` call runs in a step before the agent starts, and no token is in the checkout.
- The agent runs from an empty directory, so no `CLAUDE.md` or `.claude/` settings from the pull request load.
- The App token is used only for read requests, in a step that runs after the agent finishes.
- The comment is rendered by the plugin's `render-comment.sh`, which escapes the agent's text. A missing, unparseable, or stale result renders as no verdict.

## Usage

Call the reusable workflow from a repository, triggered by the `owner-classification` label:

```yaml
name: Owning-Team Classification

on:
  pull_request:
    types: [labeled]

permissions: {}

jobs:
  classify:
    name: Classify
    if: github.event.label.name == 'owner-classification'
    uses: bitwarden/gh-actions/.github/workflows/_classify-owning-team.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
    permissions:
      contents: read
      id-token: write
      pull-requests: write
```

Remove and re-add the label to classify a new head commit. Each run uploads `result.json` and `teams.json` as an artifact for 90 days, for scoring the evaluation.
