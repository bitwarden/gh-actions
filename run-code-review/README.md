# Run Code Review

Runs an AI-powered code review using Claude Code with Bitwarden plugins.

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
    - Description: Pull request number to review.
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
  - github_token
    - Description: GitHub token for API access.
    - Example:
      ```
      github_token: ${{ secrets.GITHUB_TOKEN }}
      ```
- Optional
  - mode
    - Description: Review mode. See [Modes](#modes) for details.
    - Default: `current`
    - Example:
      ```
      mode: vnext
      ```

## Required Permissions

This action requires the `id-token: write` permission to obtain an OIDC token for Azure authentication.

## Examples

### Job Snippet

```
      - name: Review Code
        uses: bitwarden/gh-actions/run-code-review@main
        with:
          azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}
          checkout_ref: ${{ github.event.pull_request.head.sha }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Modes

Both modes retrieve existing PR review threads before invoking Claude and load the same Bitwarden plugin set.

### `current` (default)

Uses the built-in `claude-code-action` features `use_sticky_comment` and `track_progress` for comment management.

### `vnext`

Creates a placeholder PR comment via `update-pr-comment`, then passes the comment ID to Claude. Claude writes its final summary to `/tmp/review-summary.md`. A post-step updates the PR comment from that file. Grants the `Write` tool so Claude can produce the summary file.

## Development Lifecycle

1. **Understand** -- Read `action.yml` and this README. Steps are gated by `if: inputs.mode == 'current'` or `if: inputs.mode == 'vnext'`. The caller workflow (`_review-code.yml`) maps PR labels to the `mode` input; this action only sees the mode value.
2. **Plan** -- Define what you want to change and why. Know which mode you are targeting before editing.
3. **Modify** -- Add or edit vnext-gated steps in `action.yml`. Do not change current-mode steps.
4. **Test** -- Apply the `ai-review-vnext` label to PRs in downstream repos and compare against current-mode reviews.
5. **Iterate** -- Repeat steps 3-4 until satisfied.
6. **Promote** -- In a separate PR, update current-mode steps to match vnext, remove the vnext-specific steps, and merge.
7. **Document** -- Update the Modes section of this README to describe the new current and vnext behaviors.
