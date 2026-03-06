# Upsert Code Review Comment

Creates or updates a sticky PR comment identified by a hidden HTML marker.

## Inputs

| Input        | Description                                                      | Required | Default                    |
| ------------ | ---------------------------------------------------------------- | -------- | -------------------------- |
| `token`      | GitHub token for API access                                      | Yes      | -                          |
| `pr_number`  | Pull request number                                              | Yes      | -                          |
| `repository` | Repository in `owner/repo` format                                | Yes      | -                          |
| `marker_id`  | HTML comment marker ID for identifying the sticky comment        | No       | `bitwarden-review-comment` |
| `job_url`    | Override URL for the running job (auto-detected if not provided) | No       | -                          |

## Outputs

| Output            | Description                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| `comment_id`      | Numeric ID of the created or updated comment                                    |
| `comment_url`     | HTML URL of the comment                                                         |
| `comment_created` | Whether a new comment was created (`true`) or an existing one updated (`false`) |

## Usage

```yaml
steps:
  - id: comment
    uses: bitwarden/gh-actions/upsert-code-review-comment@main
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      pr_number: ${{ github.event.pull_request.number }}
      repository: ${{ github.repository }}

  - name: Update comment with results
    env:
      GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      COMMENT_ID: ${{ steps.comment.outputs.comment_id }}
      REPOSITORY: ${{ github.repository }}
    run: |
      gh api "repos/${REPOSITORY}/issues/comments/${COMMENT_ID}" \
        --method PATCH \
        --field body="## Review Results"$'\n\n'"Your content here"$'\n\n'"<!-- bitwarden-review-comment -->"
```

## Permissions

```yaml
permissions:
  pull-requests: write
```
