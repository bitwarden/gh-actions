#!/usr/bin/env bash
set -euo pipefail

# Check download-artifacts' inputs and turn them into find-workflow-run inputs.
#
# Keeps the behaviour of the earlier node action, which callers rely on:
#   - pr, commit, branch and run_id can't be combined.
#   - pr selects the run of the pull request's head commit.
#   - branch may be given as refs/heads/<branch>.
#   - Pull request runs count as matches unless require_branch_head is set.
#   - Without workflow or run_id, the current workflow is searched.
#   - check_artifacts skips runs without any artifacts.
#
# Required environment:
#   GH_TOKEN      - token with read access to REPO.
#   REPO          - owner/repo the workflow belongs to.
#   GITHUB_OUTPUT - set by GitHub Actions; receives workflow, commit, branch, pull_requests,
#                   find_artifacts, find_name_is_regexp and find_search_artifacts.
# Optional environment (see action.yml for details):
#   WORKFLOW, PR, COMMIT, BRANCH, EVENT, RUN_ID, RUN_NUMBER, ARTIFACTS, NAME_IS_REGEXP,
#   REQUIRE_BRANCH_HEAD, CHECK_ARTIFACTS, SEARCH_ARTIFACTS

REPO="${REPO:-}"
WORKFLOW="${WORKFLOW:-}"
PR="${PR:-}"
COMMIT="${COMMIT:-}"
BRANCH="${BRANCH:-}"
RUN_ID="${RUN_ID:-}"
ARTIFACTS="${ARTIFACTS:-}"

fail() {
  echo "::error::$1"
  exit 1
}

is_true() {
  [[ "${1:-false}" == "true" ]]
}

[[ -z "${EVENT:-}" ]] || fail "event is no longer supported; use branch, commit or run_id"
[[ -z "${RUN_NUMBER:-}" ]] || fail "run_number is no longer supported; use run_id"

selectors=0
for value in "$PR" "$COMMIT" "$BRANCH" "$RUN_ID"; do
  [[ -z "$value" ]] || selectors=$((selectors + 1))
done
((selectors <= 1)) || fail "The following inputs cannot be used together: pr, commit, branch, run_id"

if [[ -z "$WORKFLOW" && -z "$RUN_ID" ]]; then
  WORKFLOW=$(gh api "repos/$REPO/actions/runs/$GITHUB_RUN_ID" --jq .workflow_id) \
    || fail "Could not infer the workflow from the current run"
  echo "==> Workflow (current): $WORKFLOW"
fi

if [[ -n "$PR" ]]; then
  COMMIT=$(gh api "repos/$REPO/pulls/$PR" --jq .head.sha) || fail "Pull request $PR not found in $REPO"
  echo "==> PR $PR head commit: $COMMIT"
fi

BRANCH="${BRANCH#refs/heads/}"

# find-workflow-run skips pull request runs by default and rejects them with require_branch_head.
pull_requests=include
is_true "${REQUIRE_BRANCH_HEAD:-}" && pull_requests=exclude

# Artifacts only steer the run search when asked to; otherwise the newest matching run is used and
# its artifacts are matched afterwards, as before.
find_artifacts=""
find_name_is_regexp=false
find_search_artifacts=false
if [[ -z "$RUN_ID" ]]; then
  if is_true "${SEARCH_ARTIFACTS:-}"; then
    [[ -n "$ARTIFACTS" ]] || fail "search_artifacts needs artifacts to be set"
    find_artifacts="$ARTIFACTS"
    find_name_is_regexp="${NAME_IS_REGEXP:-false}"
    find_search_artifacts=true
  elif is_true "${CHECK_ARTIFACTS:-}"; then
    find_artifacts="*"
    find_search_artifacts=true
  fi
fi

{
  echo "workflow=$WORKFLOW"
  echo "commit=$COMMIT"
  echo "branch=$BRANCH"
  echo "pull_requests=$pull_requests"
  echo "find_artifacts=$find_artifacts"
  echo "find_name_is_regexp=$find_name_is_regexp"
  echo "find_search_artifacts=$find_search_artifacts"
} >>"$GITHUB_OUTPUT"
