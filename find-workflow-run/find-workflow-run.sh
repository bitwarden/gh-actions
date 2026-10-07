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
#   WORKFLOW, RUN_ID, COMMIT, BRANCH, REQUIRE_BRANCH_HEAD, WORKFLOW_CONCLUSION, PULL_REQUESTS,
#   ARTIFACTS, NAME_IS_REGEXP, SEARCH_ARTIFACTS, ALLOW_FORKS, MAX_RUNS_CHECKED, RETRY_ATTEMPTS,
#   RETRY_DELAYS
#
# Fails closed: if any lookup cannot be completed or confirmed, the step fails rather than return a
# run that might not be the newest match.

REPO="${REPO:-}"
WORKFLOW="${WORKFLOW:-}"
RUN_ID="${RUN_ID:-}"
COMMIT="${COMMIT:-}"
BRANCH="${BRANCH:-}"
WORKFLOW_CONCLUSION="${WORKFLOW_CONCLUSION:-}"
PULL_REQUESTS="${PULL_REQUESTS:-exclude}"
ARTIFACTS="${ARTIFACTS:-}"
MAX_RUNS_CHECKED="${MAX_RUNS_CHECKED:-2000}"
RETRY_ATTEMPTS="${RETRY_ATTEMPTS:-3}"
RETRY_DELAYS="${RETRY_DELAYS:-2,5}"

# The lookup runs inside $(...), where its stdout is captured, so its workflow commands go to fd 3.
exec 3>&1

# Newest pull_request run IDs that matched everything but pull_requests: exclude, for the log.
EXCLUDED_PRS_FILE=$(mktemp "${RUNNER_TEMP:-/tmp}/excluded-prs.XXXXXX")
trap 'rm -f "$EXCLUDED_PRS_FILE"' EXIT

fail() {
  echo "::error::$1"
  exit 1
}

is_true() {
  [[ "${1:-false}" == "true" ]]
}

# GET from the GitHub API, retrying server errors, rate limits and network failures per
# RETRY_ATTEMPTS and RETRY_DELAYS. Other 4xx responses won't change on retry, so they fail at once.
# Output is printed only from a successful attempt, so a retried --paginate call never emits partial
# results.
api() {
  local attempt out delay err_file
  local -a delays
  IFS=, read -ra delays <<<"$RETRY_DELAYS"
  err_file=$(mktemp "${RUNNER_TEMP:-/tmp}/gh-api-error.XXXXXX")
  for ((attempt = 1; ; attempt++)); do
    if out=$(gh api --method GET -H "X-GitHub-Api-Version: 2022-11-28" "$@" 2>"$err_file"); then
      rm -f "$err_file"
      printf '%s\n' "$out"
      return 0
    fi
    cat "$err_file" >&2
    if ((attempt >= RETRY_ATTEMPTS)) \
      || { grep -qE 'HTTP 4[0-9]{2}' "$err_file" && ! grep -qiE 'HTTP 429|rate limit' "$err_file"; }; then
      rm -f "$err_file"
      return 1
    fi
    # Past the end of the list, keep using the last delay.
    delay="${delays[attempt - 1]:-${delays[${#delays[@]} - 1]}}"
    echo "==> GitHub API call failed (attempt $attempt of $RETRY_ATTEMPTS); retrying in ${delay}s" >&2
    sleep "$delay"
  done
}

# =============================================================
# Input validation
# =============================================================

[[ "$REPO" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]] || fail "repo must be in owner/repo format, got '$REPO'"
[[ -z "$RUN_ID" || "$RUN_ID" =~ ^[0-9]+$ ]] || fail "run_id must be numeric, got '$RUN_ID'"
[[ -n "$RUN_ID" || -n "$WORKFLOW" ]] || fail "workflow is required unless run_id is set"
[[ -z "$COMMIT" || -z "$BRANCH" ]] || fail "commit and branch cannot be used together"
[[ "$PULL_REQUESTS" =~ ^(exclude|include|only)$ ]] || fail "pull_requests must be exclude, include or only, got '$PULL_REQUESTS'"
if is_true "${REQUIRE_BRANCH_HEAD:-}"; then
  [[ -n "$BRANCH" ]] || fail "require_branch_head needs branch to be set"
  # A branch HEAD request wants a build of the branch itself, which a pull_request run is not.
  [[ "$PULL_REQUESTS" == "exclude" ]] || fail "require_branch_head cannot be used with pull_requests: $PULL_REQUESTS"
fi
if is_true "${NAME_IS_REGEXP:-}" || is_true "${SEARCH_ARTIFACTS:-}"; then
  [[ -n "$ARTIFACTS" ]] || fail "name_is_regexp and search_artifacts need artifacts to be set"
fi
[[ "$MAX_RUNS_CHECKED" =~ ^[1-9][0-9]*$ ]] || fail "max_runs_checked must be a positive whole number, got '$MAX_RUNS_CHECKED'"
[[ "$RETRY_ATTEMPTS" =~ ^[1-9][0-9]*$ ]] || fail "retry_attempts must be a positive whole number, got '$RETRY_ATTEMPTS'"
[[ "$RETRY_DELAYS" =~ ^[0-9]+(,[0-9]+)*$ ]] || fail "retry_delays must be comma-separated whole seconds, got '$RETRY_DELAYS'"

# Runs are listed up to 100 per page; a smaller max_runs_checked uses smaller pages so the limit is exact.
PER_PAGE=$((MAX_RUNS_CHECKED < 100 ? MAX_RUNS_CHECKED : 100))
PAGE_LIMIT=$(((MAX_RUNS_CHECKED + PER_PAGE - 1) / PER_PAGE))
readonly PER_PAGE PAGE_LIMIT

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
# Returns 1 when artifacts are missing and 2 when they could not be listed.
has_artifacts() {
  local matched missing
  matched=$(match_artifacts "$1") || return 2
  missing=$(jq '.missing | length' <<<"$matched") || return 2
  [[ "$missing" == "0" ]]
}

# =============================================================
# Run selection
# =============================================================

# Reads runs as a JSON array, prints matching runs newest first (one compact object per line).
# Ordered by run ID: IDs follow creation order, and a re-run keeps its ID, so a re-run of an old
# build correctly ranks as old. The optional argument overrides PULL_REQUESTS.
#
# workflow_conclusion accepts a run status (e.g. completed) as well as a conclusion.
# A pull_request run's head_branch is the pull request's source branch, so `branch` matches it by that.
filter_runs() {
  jq -c \
    --arg repo "$REPO" \
    --arg branch "$BRANCH" \
    --arg commit "$COMMIT" \
    --arg conclusion "$WORKFLOW_CONCLUSION" \
    --arg pull_requests "${1:-$PULL_REQUESTS}" \
    --argjson allow_forks "$(is_true "${ALLOW_FORKS:-}" && echo true || echo false)" '
    def is_status: IN("requested", "queued", "pending", "waiting", "in_progress", "completed");
    map(select(
      ($conclusion == ""
        or (if ($conclusion | is_status) then .status == $conclusion else .conclusion == $conclusion end))
      and ($allow_forks or (.head_repository.full_name // "") == $repo)
      and ($branch == "" or .head_branch == $branch)
      and ($commit == "" or .head_sha == $commit)
      and (if $pull_requests == "exclude" then .event != "pull_request"
           elif $pull_requests == "only" then .event == "pull_request"
           else true end)
    ))
    | sort_by(.id) | reverse | .[]'
}

# Records pull_request runs from the branch that only pull_requests: exclude kept out.
note_excluded_prs() {
  [[ "$PULL_REQUESTS" == "exclude" && -n "$BRANCH" ]] || return 0
  filter_runs only | jq -rs '.[0].id // empty' >>"$EXCLUDED_PRS_FILE"
}

# Prints the first run (newest first) from stdin that is wanted, or nothing. Fails if a run's
# artifacts cannot be listed, rather than skip it and fall back to an older run.
first_wanted() {
  local run id rc
  while IFS= read -r run; do
    if is_true "${SEARCH_ARTIFACTS:-}"; then
      id=$(jq -r .id <<<"$run")
      rc=0
      has_artifacts "$id" || rc=$?
      if [[ $rc -eq 2 ]]; then
        echo "::error::Could not list the artifacts of run $id" >&3
        cat >/dev/null
        return 1
      fi
      if [[ $rc -ne 0 ]]; then
        echo "==> Skipping run $id: missing artifacts" >&2
        continue
      fi
    fi
    echo "$run"
    # Read the rest so the producer isn't killed by SIGPIPE, which pipefail would report as a failure.
    cat >/dev/null
    return 0
  done
}

find_run() {
  local runs_path="repos/$REPO/actions/workflows/$WORKFLOW/runs"
  local search_args=()
  [[ -n "$BRANCH" ]] && search_args+=(-f "branch=$BRANCH")
  [[ -n "$COMMIT" ]] && search_args+=(-f "head_sha=$COMMIT")

  # Filtered search: may drop runs, so its answer is only a lower bound.
  local search_run="" page runs count
  if [[ ${#search_args[@]} -gt 0 ]]; then
    for ((page = 1; page <= PAGE_LIMIT; page++)); do
      runs=$(api "$runs_path" "${search_args[@]}" -f per_page=$PER_PAGE -f page=$page --jq '.workflow_runs') \
        || { echo "::error::Could not search the runs of $WORKFLOW (page $page)" >&3; return 1; }
      note_excluded_prs <<<"$runs" || return 1
      search_run=$(filter_runs <<<"$runs" | first_wanted) || return 1
      count=$(jq length <<<"$runs") || return 1
      [[ -n "$search_run" || $count -lt $PER_PAGE ]] && break
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
    runs=$(api "$runs_path" -f per_page=$PER_PAGE -f page=$page --jq '.workflow_runs') \
      || { echo "::error::Could not list the runs of $WORKFLOW (page $page)" >&3; return 1; }
    note_excluded_prs <<<"$runs" || return 1
    newer=$(jq --argjson after "$search_id" 'map(select(.id > $after))' <<<"$runs" | filter_runs | first_wanted) \
      || return 1
    if [[ -n "$newer" ]]; then
      if [[ "$search_id" != "0" ]]; then
        echo "::warning::Run search returned $search_id but missed newer run $(jq -r .id <<<"$newer"); using the newer run" >&3
      fi
      echo "$newer"
      return 0
    fi
    min_id=$(jq '(map(.id) | min) // 0' <<<"$runs") || return 1
    count=$(jq length <<<"$runs") || return 1
    if [[ $count -lt $PER_PAGE || "$min_id" -le "$search_id" ]]; then
      echo "$search_run"
      return 0
    fi
  done

  # The walk ran out before reaching the search result (or the end of the list), so a newer match
  # may exist beyond it. Fail rather than return a run that isn't confirmed as the newest.
  echo "::error::Checked the newest $MAX_RUNS_CHECKED runs of $WORKFLOW without confirming the newest match. Raise max_runs_checked to check further." >&3
  return 1
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
  echo "==> Pull request runs: $PULL_REQUESTS"
  if is_true "${REQUIRE_BRANCH_HEAD:-}"; then
    # Look up by the HEAD commit itself, so an older green build can never stand in for HEAD.
    COMMIT=$(api "repos/$REPO/branches/$BRANCH" --jq .commit.sha) || fail "Branch $BRANCH not found in $REPO"
    echo "==> Branch: $BRANCH (HEAD $COMMIT)"
  else
    [[ -n "$BRANCH" ]] && echo "==> Branch: $BRANCH"
    [[ -n "$COMMIT" ]] && echo "==> Commit: $COMMIT"
  fi
  run=$(find_run) || fail "Could not complete the run lookup for $WORKFLOW; no run was selected"
  if [[ -z "$run" ]]; then
    if [[ -s "$EXCLUDED_PRS_FILE" ]]; then
      echo "::notice::pull_request runs from $BRANCH exist but were excluded (pull_requests: exclude), e.g. run $(sort -rn "$EXCLUDED_PRS_FILE" | head -n 1)"
    fi
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
  matched=$(match_artifacts "$run_id") || fail "Could not list the artifacts of run $run_id"
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
