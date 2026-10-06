#!/usr/bin/env bash
set -euo pipefail

# Find a workflow run, and optionally its artifacts, without trusting GitHub's filtered run search.
#
# When the runs API is filtered by branch, event, head_sha or status, GitHub answers from a search
# index that intermittently drops runs (dawidd6/action-download-artifact#428). The result is still
# sorted newest first and looks complete, so a dropped newest run silently selects an older build.
# The filtered search is used here only to bound the work: the unfiltered run list, which is
# reliable, is then walked newest first back to the search result, and any newer matching run wins.
#
# Required environment:
#   GH_TOKEN      - token with actions:read on REPO.
#   REPO          - owner/repo the workflow belongs to.
#   GITHUB_OUTPUT - set by GitHub Actions; receives run_id, head_sha, head_branch and artifact_ids.
# Optional environment (see action.yml for details):
#   WORKFLOW, RUN_ID, COMMIT, BRANCH, REQUIRE_BRANCH_HEAD, WORKFLOW_CONCLUSION, ARTIFACTS,
#   NAME_IS_REGEXP, SEARCH_ARTIFACTS, ALLOW_FORKS

# Pages of the unfiltered run list to walk before keeping the search result unconfirmed.
readonly PAGE_LIMIT="${PAGE_LIMIT:-20}"
readonly PER_PAGE=100

WORKFLOW="${WORKFLOW:-}"
RUN_ID="${RUN_ID:-}"
COMMIT="${COMMIT:-}"
BRANCH="${BRANCH:-}"
WORKFLOW_CONCLUSION="${WORKFLOW_CONCLUSION:-}"
ARTIFACTS="${ARTIFACTS:-}"

fail() {
  echo "::error::$1"
  exit 1
}

is_true() {
  [[ "${1:-false}" == "true" ]]
}

api() {
  gh api --method GET -H "X-GitHub-Api-Version: 2022-11-28" "$@"
}

# =============================================================
# Input validation
# =============================================================

[[ "$REPO" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]] || fail "repo must be in owner/repo format, got '$REPO'"
[[ -z "$RUN_ID" || "$RUN_ID" =~ ^[0-9]+$ ]] || fail "run_id must be numeric, got '$RUN_ID'"
[[ -n "$RUN_ID" || -n "$WORKFLOW" ]] || fail "workflow is required unless run_id is set"
[[ -z "$COMMIT" || -z "$BRANCH" ]] || fail "commit and branch cannot be used together"
if is_true "${REQUIRE_BRANCH_HEAD:-}" && [[ -z "$BRANCH" ]]; then
  fail "require_branch_head needs branch to be set"
fi
if is_true "${NAME_IS_REGEXP:-}" || is_true "${SEARCH_ARTIFACTS:-}"; then
  [[ -n "$ARTIFACTS" ]] || fail "name_is_regexp and search_artifacts need artifacts to be set"
fi

echo "==> Repository: $REPO"
[[ -n "$ARTIFACTS" ]] && echo "==> Artifacts: $ARTIFACTS (regexp: ${NAME_IS_REGEXP:-false})"

# =============================================================
# Artifact matching
# =============================================================

# Prints {"ids": [...], "missing": [...]} for the run's unexpired artifacts. Glob patterns are
# comma-separated, with `*` as the only wildcard, and match whole names. A regexp is a single
# pattern (it may contain commas) and matches anywhere in the name unless anchored.
match_artifacts() {
  local run_id="$1"
  api --paginate "repos/$REPO/actions/runs/$run_id/artifacts" -f per_page=100 --jq '.artifacts[]' \
    | jq -s -c \
      --arg patterns "$ARTIFACTS" \
      --argjson regexp "$(is_true "${NAME_IS_REGEXP:-}" && echo true || echo false)" '
      def glob_to_regex:
        "^" + (split("*") | map(gsub("(?<c>[.+?^${}()|\\[\\]\\\\/])"; "\\\(.c)")) | join(".*")) + "$";
      map(select(.expired | not)) as $artifacts
      | (if $regexp then [{text: $patterns, re: $patterns}]
         else $patterns | split(",") | map(sub("^\\s+"; "") | sub("\\s+$"; ""))
           | map(select(. != "")) | map({text: ., re: glob_to_regex})
         end)
      | map(.re as $re | {text, ids: [$artifacts[] | select(.name | test($re)) | .id]})
      | {ids: (map(.ids[]) | unique), missing: map(select(.ids == []) | .text)}'
}

# In search_artifacts mode a run only counts if it has every requested artifact.
has_artifacts() {
  local missing
  missing=$(match_artifacts "$1" | jq '.missing | length')
  [[ "$missing" == "0" ]]
}

# =============================================================
# Run selection
# =============================================================

# Reads runs as a JSON array, prints matching runs newest first (one compact object per line).
# Ordered by run ID: IDs follow creation order, and a re-run keeps its ID, so a re-run of an old
# build correctly ranks as old.
filter_runs() {
  jq -c \
    --arg repo "$REPO" \
    --arg branch "$BRANCH" \
    --arg commit "$COMMIT" \
    --arg conclusion "$WORKFLOW_CONCLUSION" \
    --argjson allow_forks "$(is_true "${ALLOW_FORKS:-}" && echo true || echo false)" \
    --argjson skip_pr "$(is_true "${REQUIRE_BRANCH_HEAD:-}" && echo true || echo false)" '
    map(select(
      ($conclusion == "" or .conclusion == $conclusion)
      and ($allow_forks or (.head_repository.full_name // "") == $repo)
      and ($branch == "" or .head_branch == $branch)
      and ($commit == "" or .head_sha == $commit)
      and (($skip_pr | not) or .event != "pull_request")
    ))
    | sort_by(.id) | reverse | .[]'
}

# Prints the first run (newest first) from stdin that is wanted, or nothing.
first_wanted() {
  local run
  while IFS= read -r run; do
    if ! is_true "${SEARCH_ARTIFACTS:-}" || has_artifacts "$(jq -r .id <<<"$run")"; then
      echo "$run"
      return
    fi
    echo "==> Skipping run $(jq -r .id <<<"$run"): missing artifacts" >&2
  done
}

find_run() {
  local runs_path="repos/$REPO/actions/workflows/$WORKFLOW/runs"
  local search_args=()
  [[ -n "$BRANCH" ]] && search_args+=(-f "branch=$BRANCH")
  [[ -n "$COMMIT" ]] && search_args+=(-f "head_sha=$COMMIT")

  # Filtered search: may drop runs, so its answer is only a lower bound.
  local search_run="" page runs
  if [[ ${#search_args[@]} -gt 0 ]]; then
    for ((page = 1; page <= PAGE_LIMIT; page++)); do
      runs=$(api "$runs_path" "${search_args[@]}" -f per_page=$PER_PAGE -f page=$page --jq '.workflow_runs')
      search_run=$(filter_runs <<<"$runs" | first_wanted)
      [[ -n "$search_run" || $(jq length <<<"$runs") -lt $PER_PAGE ]] && break
    done
    if [[ -n "$search_run" ]]; then
      echo "==> Search result: run $(jq -r .id <<<"$search_run")" >&2
    else
      echo "==> Search result: none" >&2
    fi
  fi
  local search_id=0
  [[ -z "$search_run" ]] || search_id=$(jq -r .id <<<"$search_run")

  # Unfiltered walk, newest first, back to the search result.
  local newer min_id
  for ((page = 1; page <= PAGE_LIMIT; page++)); do
    runs=$(api "$runs_path" -f per_page=$PER_PAGE -f page=$page --jq '.workflow_runs')
    newer=$(jq --argjson after "$search_id" 'map(select(.id > $after))' <<<"$runs" | filter_runs | first_wanted)
    if [[ -n "$newer" ]]; then
      if [[ "$search_id" != "0" ]]; then
        echo "::warning::Run search returned $search_id but missed newer run $(jq -r .id <<<"$newer"); using the newer run" >&2
      fi
      echo "$newer"
      return
    fi
    min_id=$(jq '(map(.id) | min) // 0' <<<"$runs")
    if [[ $(jq length <<<"$runs") -lt $PER_PAGE || "$min_id" -le "$search_id" ]]; then
      echo "$search_run"
      return
    fi
  done

  if [[ -n "$search_run" ]]; then
    echo "::warning::Checked the newest $((PAGE_LIMIT * PER_PAGE)) runs without reaching run $search_id; using it unconfirmed" >&2
    echo "$search_run"
  fi
}

# =============================================================
# Main
# =============================================================

if [[ -n "$RUN_ID" ]]; then
  [[ -n "$BRANCH$COMMIT" ]] && echo "==> run_id is set; ignoring branch and commit"
  run=$(api "repos/$REPO/actions/runs/$RUN_ID") || fail "Run $RUN_ID not found in $REPO"
else
  echo "==> Workflow: $WORKFLOW"
  echo "==> Conclusion: ${WORKFLOW_CONCLUSION:-any}"
  if is_true "${REQUIRE_BRANCH_HEAD:-}"; then
    # Look up by the HEAD commit itself, so an older green build can never stand in for HEAD.
    COMMIT=$(api "repos/$REPO/branches/$BRANCH" --jq .commit.sha) || fail "Branch $BRANCH not found in $REPO"
    echo "==> Branch: $BRANCH (HEAD $COMMIT)"
  else
    [[ -n "$BRANCH" ]] && echo "==> Branch: $BRANCH"
    [[ -n "$COMMIT" ]] && echo "==> Commit: $COMMIT"
  fi
  run=$(find_run)
  if [[ -z "$run" ]]; then
    if is_true "${REQUIRE_BRANCH_HEAD:-}"; then
      fail "No matching run of $WORKFLOW at $BRANCH HEAD ($COMMIT). Build the branch HEAD and try again."
    fi
    fail "No matching run of $WORKFLOW found"
  fi
fi

run_id=$(jq -r .id <<<"$run")
head_sha=$(jq -r .head_sha <<<"$run")
head_branch=$(jq -r '.head_branch // ""' <<<"$run")
echo "==> (found) Run ID: $run_id"
echo "==> (found) Run date: $(jq -r .created_at <<<"$run")"
echo "==> (found) Commit: $head_sha ($head_branch)"
echo "==> (found) URL: $(jq -r .html_url <<<"$run")"

artifact_ids=""
if [[ -n "$ARTIFACTS" ]]; then
  matched=$(match_artifacts "$run_id")
  missing=$(jq -r '.missing | join(", ")' <<<"$matched")
  [[ -z "$missing" ]] || fail "Run $run_id has no unexpired artifact matching: $missing"
  artifact_ids=$(jq -r '.ids | join(",")' <<<"$matched")
  echo "==> (found) Artifact IDs: $artifact_ids"
fi

{
  echo "run_id=$run_id"
  echo "head_sha=$head_sha"
  echo "head_branch=$head_branch"
  echo "artifact_ids=$artifact_ids"
} >>"$GITHUB_OUTPUT"
