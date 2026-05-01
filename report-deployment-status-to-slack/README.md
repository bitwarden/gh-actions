# Report Deployment Status to Slack Action

Post a deployment status message to a Slack channel via an incoming webhook.

## Features

- Sends formatted Slack messages for deployment events: `start`, `success`, `failure`, `cancelled`, `no-changes`
- Links the tag/branch and commit SHA back to the source repository
- Optionally appends a database-migration warning when `db_migration_detected` is `true` on a feature branch
- Works across repositories — caller passes the project owner, name, ref, and SHA explicitly

## Inputs

| Input                   | Description                                                                                     | Required | Default     |
| ----------------------- | ----------------------------------------------------------------------------------------------- | -------- | ----------- |
| `project`               | The name of the project (repository name).                                                      | Yes      | -           |
| `project_owner`         | The owner/org of the project.                                                                   | No       | `bitwarden` |
| `tag`                   | The name of the branch or tag being deployed.                                                   | Yes      | -           |
| `commit_sha`            | The full SHA of the branch or tag. Shortened to 7 characters in the message.                    | Yes      | -           |
| `environment`           | The name of the environment (e.g. `US-QA Cloud`).                                               | Yes      | -           |
| `event`                 | Deployment event type. One of: `start`, `success`, `failure`, `cancelled`, `no-changes`.        | Yes      | -           |
| `url`                   | URL of the deployment action run, included in the message body.                                 | No       | -           |
| `db_migration_detected` | When `true`, appends a database-migration warning unless `tag` is `main`, `rc`, or `hotfix-rc`. | No       | `false`     |
| `slack_webhook_url`     | Slack incoming webhook URL to post the message to.                                              | Yes      | -           |

## Usage

### Basic Usage

```yaml
- name: Report deploy start
  uses: bitwarden/gh-actions/report-deployment-status-to-slack@main
  with:
    project: server
    tag: ${{ github.ref_name }}
    commit_sha: ${{ github.sha }}
    environment: US-QA Cloud
    event: start
    url: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Reporting Multiple Deployment Phases

```yaml
- name: Notify deploy started
  uses: bitwarden/gh-actions/report-deployment-status-to-slack@main
  with:
    project: server
    tag: ${{ github.ref_name }}
    commit_sha: ${{ github.sha }}
    environment: US-QA Cloud
    event: start
    url: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}

- name: Run deployment
  id: deploy
  run: ./scripts/deploy.sh

- name: Notify deploy result
  if: always()
  uses: bitwarden/gh-actions/report-deployment-status-to-slack@main
  with:
    project: server
    tag: ${{ github.ref_name }}
    commit_sha: ${{ github.sha }}
    environment: US-QA Cloud
    event: ${{ steps.deploy.outcome == 'success' && 'success' || 'failure' }}
    url: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### With a Database Migration Warning

When the deployment includes schema changes on a feature branch, set `db_migration_detected: true` to append a `:red_siren:` line to the message. The warning is suppressed on `main`, `rc`, and `hotfix-rc` since migrations on those branches are expected.

```yaml
- name: Report deploy with migration warning
  uses: bitwarden/gh-actions/report-deployment-status-to-slack@main
  with:
    project: server
    tag: ${{ github.ref_name }}
    commit_sha: ${{ github.sha }}
    environment: US-QA Cloud
    event: success
    db_migration_detected: ${{ steps.detect-migration.outputs.detected }}
    url: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Cross-Repository Reporting

The action uses `project` and `project_owner` (not `github.repository`) when building commit/tree links, so a workflow in one repo can report on a deployment of another repo:

```yaml
- name: Report cross-repo deploy
  uses: bitwarden/gh-actions/report-deployment-status-to-slack@main
  with:
    project: clients
    project_owner: bitwarden
    tag: web-v2026.4.0
    commit_sha: 50f7fa03dbc0f18a641206ab1a92fb11a1131572
    environment: US-Prod Cloud
    event: success
    url: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
    slack_webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Requirements

- A Slack incoming webhook URL must be provisioned for the destination channel and stored as a secret.
- The custom emoji `:loading:` must exist in the destination Slack workspace; the `start` event renders it as literal text otherwise.
- `jq` is preinstalled on GitHub-hosted runners; self-hosted runners must provide it.
