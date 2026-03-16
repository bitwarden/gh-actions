# Update PR Comment

Creates or updates a sticky PR comment identified by a hidden HTML marker.

## Inputs

- Required
  - token
    - Description: GitHub token for API access.
    - Example:
      ```
      token: ${{ secrets.GITHUB_TOKEN }}
      ```
  - pr_number
    - Description: Pull request number.
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
- Optional
  - marker_id
    - Description: HTML comment marker ID used to find and update the sticky comment.
    - Default: `bitwarden-pr-comment`
    - Example:
      ```
      marker_id: my-action-comment
      ```
  - body
    - Description: Comment body string. Mutually exclusive with `body_file`. One of `body` or `body_file` must be provided.
    - Example:
      ```
      body: "Working..."
      ```
  - body_file
    - Description: Path to a file containing the comment body. Mutually exclusive with `body`. Skips with a warning if the file does not exist.
    - Example:
      ```
      body_file: /tmp/results.md
      ```
  - comment_id
    - Description: Known comment ID to update directly, skipping the marker search. Use the `comment_id` output from a prior step.
    - Example:
      ```
      comment_id: ${{ steps.create-comment.outputs.comment_id }}
      ```

## Outputs

| Output            | Description                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| `comment_id`      | Numeric ID of the created or updated comment                                    |
| `comment_url`     | HTML URL of the comment                                                         |
| `comment_created` | Whether a new comment was created (`true`) or an existing one updated (`false`) |

## Required Permissions

This action requires the `pull-requests: write` permission to create and update PR comments.

## Examples

### Create a placeholder, then update with results

```
jobs:
  example:
    name: Example Job
    runs-on: ubuntu-24.04
    permissions:
      pull-requests: write
    steps:
      - name: Create PR comment placeholder
        id: create-comment
        uses: bitwarden/gh-actions/update-pr-comment@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}
          body: "Working..."

      - name: Do work
        shell: bash
        run: echo "results" > /tmp/results.md

      - name: Update PR comment with results
        uses: bitwarden/gh-actions/update-pr-comment@main
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
          repository: ${{ github.repository }}
          comment_id: ${{ steps.create-comment.outputs.comment_id }}
          body_file: /tmp/results.md
```
