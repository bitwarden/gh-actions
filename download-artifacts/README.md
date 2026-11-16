# Download workflow artifact

Downloads the artifacts of another workflow run, found by workflow and branch, commit, pull request or run ID.

A composite of two steps:

1. [`find-workflow-run`](../find-workflow-run) finds the run. GitHub's filtered run search can silently drop runs, so it
   checks the search result against the unfiltered run list rather than trust it.
2. [`actions/download-artifact`](https://github.com/actions/download-artifact) downloads the run's matching artifacts.

Earlier versions were a node action forked from
[dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact). The inputs and outputs are
unchanged, apart from the two noted below.

## Usage

```yaml
- name: Download build
  id: download
  uses: bitwarden/gh-actions/download-artifacts@main
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    repo: bitwarden/clients
    workflow: build-cli.yml
    commit: ${{ steps.client_info.outputs.sha }}
    artifacts: 'bw-linux-*.zip, bw-macos-*.zip'
    path: artifacts
```

To download several times from one build, resolve the run once (for example with `dry_run: true`) and pass its
`run_id` output to the later steps.

## Inputs

| Input                  | Default                    | Description                                                                                                  |
| ---------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `github_token`         | `${{ github.token }}`      | Token with `actions:read` on `repo`.                                                                         |
| `repo`                 | `${{ github.repository }}` | Repository the workflow belongs to.                                                                          |
| `workflow`             | current workflow           | Workflow file name or ID. Not needed with `run_id`.                                                          |
| `workflow_conclusion`  | `success`                  | Conclusion or status the run must have. Empty matches any run.                                               |
| `branch`               |                            | Newest matching run on this branch (or tag). `refs/heads/` is stripped.                                      |
| `commit`               |                            | Newest matching run built from this commit.                                                                  |
| `pr`                   |                            | Newest matching run of this pull request's head commit.                                                      |
| `run_id`               |                            | Use this run as is, without searching.                                                                       |
| `require_branch_head`  | `false`                    | Fail unless the run was built from `branch`'s HEAD commit. Pull request runs are skipped.                    |
| `allow_forks`          | `false`                    | Accept runs from forks.                                                                                      |
| `check_artifacts`      | `false`                    | Skip runs without any artifacts when searching.                                                              |
| `search_artifacts`     | `false`                    | Skip runs that lack `artifacts` when searching.                                                              |
| `name_is_regexp`       | `false`                    | With `search_artifacts`, treat `artifacts` as one regular expression for the search.                         |
| `artifacts`            | all                        | Comma-separated names with `*` wildcards. Artifacts matching any name are downloaded.                        |
| `path`                 | `./`                       | Where to put the artifacts. Every artifact is extracted into `path` directly.                                |
| `skip_unpack`          | `false`                    | Save each artifact as `<path>/<name>.zip` instead of extracting it.                                          |
| `dry_run`              |                            | Find the run and its artifacts without downloading.                                                          |
| `if_no_artifact_found` | `fail`                     | `fail`, `warn` or `ignore` when no run or no matching artifact is found, or a matching artifact has expired. |

`pr`, `commit`, `branch` and `run_id` can't be combined. Without any of them, the newest matching run of the workflow is
used. Pull request runs count as matches, except with `require_branch_head`.

## Outputs

| Output                  | Description                                                                   |
| ----------------------- | ----------------------------------------------------------------------------- |
| `run_id`                | The run the artifacts come from.                                              |
| `artifact-build-commit` | Commit the artifacts were built from. Set when at least one artifact matched. |
| `artifact-build-branch` | Branch the artifacts were built from. Set when at least one artifact matched. |
| `artifacts`             | JSON array of the matching artifacts, as returned by the GitHub API.          |
| `found_artifact`        | `true` if matching artifacts were found.                                      |
| `dry_run`               | With `dry_run`, `true` if matching artifacts were found.                      |
| `error_message`         | Set when the run lookup fails.                                                |

## Changes from the node action

- **`event` and `run_number` are no longer supported**, and fail the step if set.
- **The run search fails if it can't be confirmed.** `find-workflow-run` checks up to 2,000 of the workflow's newest
  runs against the search result. The node action warned and used the search result when it reached that limit; this
  version fails, rather than risk an old build.
- `dry_run: false` no longer means a dry run.
