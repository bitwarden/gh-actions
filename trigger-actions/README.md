# Trigger Actions

A composite action that creates a GitHub deployment event on a target repository to trigger downstream workflow automation.

## Purpose

This action provides a standardized way to signal that a deployment-related workflow should run in another repository. Rather than calling workflows directly, it creates a GitHub deployment event against the `trigger-actions` environment using a named `task`. Receiving repositories listen for these events via a `deployment` trigger and route to the appropriate workflow based on the `task` value.

This decouples the caller from knowledge of what workflow runs downstream — the caller only needs to know the task name. The target repository is resolved automatically based on the task.

## How It Works

1. Authenticates to Azure via OIDC and retrieves the GitHub App credentials (`GH-TRIGGER-APP-ID`, `GH-TRIGGER-APP-KEY`) from the `gh-org-bitwarden` Key Vault
2. Mints a short-lived GitHub App token scoped to the target repository with `deployments: write`
3. Creates a deployment event on `main` of the target repository with `environment: trigger-actions` and the provided `task`

Receiving repositories should have a workflow triggered on `deployment` that filters on both `github.event.deployment.environment == 'trigger-actions'` and `github.event.deployment.task == '<task-name>'`.

## Inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `azure_subscription_id` | Yes | | Azure Subscription ID for OIDC login |
| `azure_tenant_id` | Yes | | Azure Tenant ID for OIDC login |
| `azure_client_id` | Yes | | Azure Client ID for OIDC login |
| `task` | Yes | | Task name used for routing. Also determines the target repository (`deploy-server-dev` → `devops`, all others → `deploy`) |
| `description` | No | *(task value)* | Human-readable description of the trigger. Defaults to the `task` value if not provided |
| `test` | No | `false` | Skip App token generation and use the calling workflow's token instead. For testing only |

## Usage

```yaml
- name: Trigger deployment
  uses: bitwarden/gh-actions/trigger-actions@main
  with:
    azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
    azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
    azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
    task: deploy-my-service-dev
    description: "Triggered by build on main"
```

## Prerequisites

- The calling workflow must have `id-token: write` permission for Azure OIDC authentication
- `GH-TRIGGER-APP-ID` and `GH-TRIGGER-APP-KEY` must be present in the `gh-org-bitwarden` Key Vault
- The GitHub App must be installed on the target repository with `deployments: write`
- The target repository must have a workflow listening on the `deployment` event that handles the `trigger-actions` environment and the relevant `task` value
