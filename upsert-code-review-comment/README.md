# Upsert Code Review Comment

Creates or updates a sticky PR comment identified by a hidden HTML marker.

## Inputs

| Input        | Description                                                                | Required | Default                    |
| ------------ | -------------------------------------------------------------------------- | -------- | -------------------------- |
| `token`      | GitHub token for API access                                                | Yes      | -                          |
| `pr_number`  | Pull request number                                                        | Yes      | -                          |
| `repository` | Repository in `owner/repo` format                                          | Yes      | -                          |
| `marker_id`  | HTML comment marker ID for identifying the sticky comment                  | No       | `bitwarden-review-comment` |
| `body`       | Custom comment body string. Mutually exclusive with `body_file`            | No       | -                          |
| `body_file`  | Path to a file containing the comment body. Mutually exclusive with `body` | No       | -                          |
| `job_url`    | Override URL for the running job (auto-detected if not provided)           | No       | -                          |

## Outputs

| Output            | Description                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| `comment_id`      | Numeric ID of the created or updated comment                                    |
| `comment_url`     | HTML URL of the comment                                                         |
| `comment_created` | Whether a new comment was created (`true`) or an existing one updated (`false`) |
