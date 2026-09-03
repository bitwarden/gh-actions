# Audit External Plugin

Audits a new or updated external Claude Code plugin pin in a repository's `.claude-plugin/marketplace.json`, using the `bitwarden-security-engineer` plugin's `auditing-external-claude-plugins` skill, and posts the report to a sticky PR comment.

It diffs the pull request's base and head `marketplace.json` for plugin entries with `"category": "external"` whose `source.sha` is new or has changed, then runs the audit skill once per changed entry (`Skill(bitwarden-security-engineer:auditing-external-claude-plugins)`) and combines the reports into one comment. A repository with no `.claude-plugin/marketplace.json`, or a pull request that doesn't change one, no-ops.

## Inputs

- Required
  - azure_subscription_id
    - Description: Azure Subscription ID for OIDC authentication.
    - Example:
      ```
      azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      ```
  - azure_tenant_id
    - Description: Azure Tenant ID for OIDC authentication.
    - Example:
      ```
      azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
      ```
  - azure_client_id
    - Description: Azure Client ID for OIDC authentication.
    - Example:
      ```
      azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
      ```
  - pr_number
    - Description: Pull request number to audit.
    - Example:
      ```
      pr_number: ${{ github.event.pull_request.number }}
      ```
  - repository
    - Description: Repository in `owner/repo` format.
    - Example:
      ```
      repository: ${{ github.repository }}
      ```
  - checkout_ref
    - Description: Git ref to check out (typically the PR head SHA).
    - Example:
      ```
      checkout_ref: ${{ github.event.pull_request.head.sha }}
      ```
  - base_ref
    - Description: Base branch to diff against for change detection (typically the PR base ref).
    - Example:
      ```
      base_ref: ${{ github.base_ref }}
      ```
  - github_token
    - Description: GitHub token for API access.
    - Example:
      ```
      github_token: ${{ secrets.GITHUB_TOKEN }}
      ```

## Required Permissions

This action requires the `id-token: write` permission to obtain an OIDC token for Azure authentication, and `pull-requests: write` to manage the sticky audit comment.

## Usage

Most repositories should call the reusable workflow rather than the action directly. See [Reusable Workflow](#reusable-workflow) below.

### Job Snippet

```
      - name: Audit external plugin pins
        uses: bitwarden/gh-actions/audit-external-plugin@main
        with:
          azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}
          checkout_ref: ${{ github.event.pull_request.head.sha }}
          base_ref: ${{ github.base_ref }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Reusable Workflow

`bitwarden/gh-actions/.github/workflows/_audit-external-plugin.yml` wraps this action with a permission gate. Add a caller workflow to any repository with a `.claude-plugin/marketplace.json`:

```yaml
name: Audit External Plugin

on:
  pull_request:
    paths:
      - ".claude-plugin/marketplace.json"

permissions: {}

jobs:
  audit:
    name: Audit External Plugin
    uses: bitwarden/gh-actions/.github/workflows/_audit-external-plugin.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
```

The action no-ops when a pull request changes no external plugin pin, so it is safe to run on every PR that touches `marketplace.json`.

## What Counts as a Changed Pin

An entry qualifies when `"category": "external"` and its `source.sha` differs between the PR's base and head `marketplace.json` — this covers both a brand-new external entry and an existing one moved to a new commit. A removed entry, or any change to a non-external plugin, is ignored.

## Why `Skill(bitwarden-security-engineer:auditing-external-claude-plugins)` and Not a Slash Command

The skill runs as an isolated forked subagent (`context: fork`) pinned to the `bitwarden-security-engineer` agent and the `fable` model, with its own scoped `allowed-tools` — it clones the *audited* plugin's repository, which this action treats as untrusted, adversarial input by design. The top-level `claude-code-action` invocation in this action only orchestrates: it invokes the skill once per changed entry and combines the resulting report files, and is granted nothing beyond `Skill`, `Read`, and `Write`.
