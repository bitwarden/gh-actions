# Validate AI

Reviews Claude Code material that changed in a pull request using Claude Code with Bitwarden plugins. It works for any repository that carries Claude config, not only plugin marketplaces. A repo with its own `.claude/` directory (skills, agents, commands, hooks, settings) and `CLAUDE.md` gets the same review as a marketplace of plugins.

It detects changed Claude-related files (`.claude/` config, `CLAUDE.md`, agents, skills, commands, hooks, and plugin directories), runs the `plugin-dev` and `claude-config-validator` plugins against them, and posts the results to a sticky PR comment. In a plugin marketplace repository (one with a `.claude-plugin/marketplace.json`), a pull request that touches a `plugins/` directory also runs the bundled structure, marketplace, and version-bump scripts against the checkout. Repositories without that manifest skip those steps and just get the AI-driven review.

The validation scripts live in [`scripts/`](scripts/) and are bundled with the action — this action directory is their sole source of truth, so callers do not need to vendor anything.

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
    - Description: Pull request number to validate.
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

This action requires the `id-token: write` permission to obtain an OIDC token for Azure authentication, and `pull-requests: write` to manage the sticky validation comment.

## Usage

Most repositories should call the reusable workflow rather than the action directly. See [Reusable Workflow](#reusable-workflow) below.

### Job Snippet

```
      - name: Validate AI
        uses: bitwarden/gh-actions/run-ai-validation@main
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

`bitwarden/gh-actions/.github/workflows/_validate-ai.yml` wraps this action with a permission gate. Add a caller workflow to any repository:

```yaml
name: Validate AI

on:
  pull_request:

permissions: {}

jobs:
  validate:
    name: Validate AI
    uses: bitwarden/gh-actions/.github/workflows/_validate-ai.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
```

The action no-ops when a pull request changes no Claude-related files, so it is safe to run on every PR.

## Validation Steps

| Step                             | Runs when                                                                           | Fails the job |
| -------------------------------- | ----------------------------------------------------------------------------------- | ------------- |
| Plugin structure                 | A `plugins/` directory changed and the repo has a `.claude-plugin/marketplace.json` | Yes           |
| Marketplace                      | A `plugins/` directory changed and the repo has a `.claude-plugin/marketplace.json` | Yes           |
| Version bump                     | Component files changed inside `plugins/` and the repo has a `marketplace.json`     | Yes           |
| Component & security (AI-driven) | Any agent, skill, command, hook, `CLAUDE.md`, or `.claude/` file changed            | Yes           |

The structure, marketplace, and version-bump steps run the bundled scripts against the caller's checkout (via `REPO_ROOT`). They only trigger in a plugin marketplace repository, which the action detects by the presence of a `.claude-plugin/marketplace.json`. A repo that has an unrelated top-level `plugins/` directory but no marketplace manifest never runs them, so it won't hit spurious failures. The AI-driven validation runs in any repository.

## Bundled Scripts

[`scripts/`](scripts/) is the sole source for the marketplace validation logic:

- `validate-plugin-structure.sh` — plugin directory layout and required files
- `validate-marketplace.sh` — `.claude-plugin/marketplace.json` consistency
- `validate-version-bump.sh` — enforces a version bump + changelog entry when components change
- `bump-plugin-version.sh` — developer helper to bump a plugin version across all files
- `lib/path-sanitization.sh` — shared path-sanitization helpers
- `README.md` — full script documentation

Each script derives `REPO_ROOT` from its own location for standalone use but honors a `REPO_ROOT` environment override, which is how the action points them at the checkout being validated.
