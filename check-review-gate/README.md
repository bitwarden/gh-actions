# Check Review Gate

Determines whether a Claude Code AI review should run on a pull request, routing through a label-triggered path or an automatic safety net.

## How It Works

The gate evaluates two paths in order:

**Label path** (checked first): If the PR carries `ai-review-vnext` or `ai-review`, the review proceeds immediately. Draft status is ignored — a reviewer explicitly asked for a review.

**Safety net** (when no label matched): Fires on `opened`, `ready_for_review`, and `reopened` events for non-draft PRs that do not already have a review comment. Prevents duplicate reviews on push-triggered re-runs.

## Inputs

- Required
  - `token`
    - Description: GitHub token for API access.
    - Example:
      ```
      token: ${{ github.token }}
      ```
  - `pr_number`
    - Description: Pull request number.
    - Example:
      ```
      pr_number: ${{ github.event.pull_request.number }}
      ```
  - `repository`
    - Description: Repository in `owner/repo` format.
    - Example:
      ```
      repository: ${{ github.repository }}
      ```
  - `event_name`
    - Description: The triggering event name from the calling workflow.
    - Example:
      ```
      event_name: ${{ github.event_name }}
      ```
- Optional
  - `marker_id`
    - Description: HTML comment marker ID used to detect an existing review comment (idempotency guard). Must match the `marker_id` passed to `update-pr-comment`.
    - Default: `bitwarden-code-review`
    - Example:
      ```
      marker_id: my-review-marker
      ```

## Outputs

| Output           | Description                                                            |
| ---------------- | ---------------------------------------------------------------------- |
| `should_review`  | `true` if a review should execute, `false` otherwise                   |
| `review_variant` | `current` or `vnext` when `should_review=true`; empty string otherwise |
| `skip_reason`    | Human-readable explanation when `should_review=false`                  |

## Required Permissions

| Permission      | Access | Reason                          |
| --------------- | ------ | ------------------------------- |
| `pull-requests` | `read` | Fetch PR labels and comments    |
| `contents`      | `read` | Check out the action definition |

## Example

```yaml
- name: Check review gate
  id: gate
  uses: bitwarden/gh-actions/check-review-gate@main
  with:
    token: ${{ github.token }}
    pr_number: ${{ github.event.pull_request.number }}
    repository: ${{ github.repository }}
    event_name: ${{ github.event_name }}

- name: Run review
  if: steps.gate.outputs.should_review == 'true'
  run: echo "Running ${{ steps.gate.outputs.review_variant }} review"
```
