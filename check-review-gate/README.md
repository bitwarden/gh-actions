# Check Review Gate

Determines whether an AI-powered code review should run on a pull request. The `ai-review-vnext` or `ai-review` labels are the primary opt-in signal that an engineer desires an AI code review. The at-least-one AI-powered code review rule states that if a PR is being opened, reopening, or publishing from a draft state then we must validate. The way we validate is by using a sticky comment with a hidden HTML marker.

## How It Works

The gate evaluates two paths in order:

**Label path**: If the PR carries `ai-review-vnext` or `ai-review`, the review proceeds immediately without validating the at-least-one rule.

**At-least-one rules**: Validates that a non-draft PR has at least one AI-powered code review when the event trigger is `opened`, `ready_for_review`, and `reopened`.

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
  - `marker_id`
    - Description: HTML comment marker ID used to detect an existing review comment (idempotency guard). Must match the `marker_id` passed to `update-pr-comment`.
    - Example:
      ```
      marker_id: bitwarden-code-review
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
    event_name: ${{ github.event_name }}
    marker_id: bitwarden-code-review
    pr_number: ${{ github.event.pull_request.number }}
    repository: ${{ github.repository }}
    token: ${{ github.token }}

- name: Run review
  if: steps.gate.outputs.should_review == 'true'
  run: echo "Running ${{ steps.gate.outputs.review_variant }} review"
```
