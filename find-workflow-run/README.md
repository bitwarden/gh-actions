# Find Workflow Run

Finds a workflow run, and optionally checks its artifacts, then outputs the run ID for a download step to pin to.

GitHub's run search can't be trusted on its own. When the workflow runs API is filtered by `branch`, `event`, `head_sha` or `status`, it answers from a search index that intermittently returns a random subset of the matching runs ([dawidd6/action-download-artifact#428](https://github.com/dawidd6/action-download-artifact/issues/428)). The subset is still sorted newest first and nothing shows that runs are missing, so a lookup can silently pick an old build. `gh run list --branch` and `--commit` go through the same search.

## Usage

```yaml
- name: Find build run
  id: find
  uses: bitwarden/gh-actions/find-workflow-run@main
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    repo: bitwarden/clients
    workflow: build-cli.yml
    branch: main
    artifacts: '^bw-linux-\d{4}\.\d+\.\d+\.zip$'
    name_is_regexp: true

- name: Download build
  uses: dawidd6/action-download-artifact@b6e2e70617bc3265edd6dab6c906732b2f1ae151 # v21
  with:
    github_token: ${{ steps.app-token.outputs.token }}
    repo: bitwarden/clients
    run_id: ${{ steps.find.outputs.run_id }}
    name: '^bw-linux-\d{4}\.\d+\.\d+\.zip$'
    name_is_regexp: true
```

Pass the run ID to the download step and drop its `branch`, `commit` and `workflow_conclusion` inputs. With a run ID, download actions skip their own run search.

## Inputs

| Input                 | Default                    | Description                                                                                                                                                                                           |
| --------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `github_token`        | `${{ github.token }}`      | Token with `actions:read` on `repo`.                                                                                                                                                                  |
| `repo`                | `${{ github.repository }}` | Repository the workflow belongs to.                                                                                                                                                                   |
| `workflow`            |                            | Workflow file name or ID. Required unless `run_id` is set.                                                                                                                                            |
| `run_id`              |                            | Use this run as is. Overrides `branch` and `commit`, and ignores `workflow_conclusion`. Artifacts are still checked.                                                                                  |
| `commit`              |                            | Newest matching run built from this SHA. Cannot be used with `branch`.                                                                                                                                |
| `branch`              |                            | Newest matching run on this branch. Cannot be used with `commit`.                                                                                                                                     |
| `require_branch_head` | `false`                    | Only accept a run of the branch's HEAD commit. Fails rather than fall back to an older run. Cannot be combined with `pull_requests: include` or `only`.                                               |
| `workflow_conclusion` | `success`                  | Conclusion (e.g. `success`) or status (e.g. `completed`) the run must have. Empty matches any run.                                                                                                    |
| `pull_requests`       | `exclude`                  | `exclude`, `include` or `only` `pull_request` runs. A pull request run matches `branch` by its source branch.                                                                                         |
| `artifacts`           |                            | Artifacts the run must have: comma-separated names with `*` wildcards, matching whole names.                                                                                                          |
| `name_is_regexp`      | `false`                    | Treat `artifacts` as one regular expression (commas included), matched anywhere in the name unless anchored with `^` and `$`.                                                                         |
| `search_artifacts`    | `false`                    | Skip runs that lack the artifacts and keep looking at older ones. Otherwise the newest matching run must have them, or the step fails.                                                                |
| `allow_forks`         | `false`                    | Accept runs from forks.                                                                                                                                                                               |
| `max_runs_checked`    | `2000`                     | How many of the workflow's newest runs to check against the filtered search. The step fails if the newest match can't be confirmed within them. Raise it for rarely built branches in busy workflows. |
| `retry_attempts`      | `3`                        | Attempts per GitHub API call, including the first. Server errors, rate limits and network failures are retried; other 4xx responses are not.                                                          |
| `retry_delays`        | `2,5`                      | Comma-separated seconds to wait before each retry. The last value repeats if there are more retries than values.                                                                                      |

With neither `branch` nor `commit`, the newest matching run of the workflow is used.

## Outputs

| Output         | Description                                                                         |
| -------------- | ----------------------------------------------------------------------------------- |
| `run_id`       | ID of the run found. Never empty: the step fails if no run matches.                 |
| `head_sha`     | Commit the run was built from.                                                      |
| `head_branch`  | Branch the run was built from.                                                      |
| `artifact_ids` | Comma-separated IDs of the unexpired matching artifacts. Empty without `artifacts`. |

## How the run is selected

1. The filtered search (`branch` or `head_sha`) finds a candidate. Its answer is only a lower bound.
2. The unfiltered run list, which isn't affected, is walked newest first back to that candidate. Any newer matching run wins, with a warning in the log.
3. The walk checks at most `max_runs_checked` runs (2,000 by default). If it hasn't reached the candidate by then, the step fails, because a newer match could lie beyond it. The right limit depends on how busy the workflow is and how rarely the branch is built.
4. Runs are ordered by run ID. A re-run keeps its ID, so a re-run of an old build ranks as old.
5. Runs from forks are skipped unless `allow_forks` is set.
6. `pull_request` runs are skipped unless `pull_requests` is `include` or `only`. When that leaves no run on the branch but pull request runs exist, the log notes it.
7. With `require_branch_head`, the lookup is by the branch's HEAD commit, so no older build can stand in for it.
8. The lookup fails closed. If any GitHub API call still fails after `retry_attempts`, or a run's artifacts can't be listed, the step fails rather than fall back to an older run.
