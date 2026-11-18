#!/usr/bin/env bash
set -euo pipefail

# Match the found run's artifacts against the requested names, set the action's outputs, and decide
# whether to download. Follows if_no_artifact_found when the run has nothing to download. A failed
# run lookup always fails the step, as it did in the node action.
#
# Names are comma-separated, with `*` as the only wildcard, and match whole names. An artifact is
# downloaded if it matches any name, so a name that matches nothing is not an error on its own.
#
# Required environment:
#   GH_TOKEN      - token with actions:read on REPO.
#   REPO          - owner/repo the workflow belongs to.
#   FIND_OUTCOME  - outcome of the find-workflow-run step.
#   GITHUB_OUTPUT - set by GitHub Actions; receives run_id, artifacts, artifact-build-commit,
#                   artifact-build-branch, found_artifact, dry_run, error_message, artifact_ids
#                   and download.
# Optional environment (see action.yml for details):
#   RUN_ID, ARTIFACTS, DRY_RUN, IF_NO_ARTIFACT_FOUND

RUN_ID="${RUN_ID:-}"
ARTIFACTS="${ARTIFACTS:-}"
DRY_RUN="${DRY_RUN:-}"
IF_NO_ARTIFACT_FOUND="${IF_NO_ARTIFACT_FOUND:-fail}"

output() {
  echo "$1=$2" >>"$GITHUB_OUTPUT"
}

# Nothing to download: report it as if_no_artifact_found asks, and skip the download step.
no_artifacts() {
  output found_artifact false
  case "$IF_NO_ARTIFACT_FOUND" in
    fail)
      echo "::error::$1"
      exit 1
      ;;
    warn) echo "::warning::$1" ;;
    *) echo "$1" ;;
  esac
  exit 0
}

if [[ "${FIND_OUTCOME:-}" != "success" || -z "$RUN_ID" ]]; then
  output found_artifact false
  output error_message "Run lookup failed; see the Find workflow run step for the reason"
  echo "::error::Run lookup failed; see the Find workflow run step for the reason"
  exit 1
fi

output run_id "$RUN_ID"

all=$(gh api --paginate "repos/$REPO/actions/runs/$RUN_ID/artifacts?per_page=100" --jq '.artifacts[]' | jq -s -c .)
artifacts=$(jq -c --arg patterns "${ARTIFACTS:-*}" '
  def glob_to_regex:
    "^" + (split("*") | map(gsub("(?<c>[.+?^${}()|\\[\\]\\\\/=!:])"; "\\\(.c)")) | join(".*")) + "$";
  ($patterns | split(",") | map(sub("^\\s+"; "") | sub("\\s+$"; "") | glob_to_regex)) as $res
  | map(select(.name as $name | any($res[]; . as $re | $name | test($re))))' <<<"$all")
output artifacts "$artifacts"

count=$(jq length <<<"$artifacts" | tr -d '\r')
if ((count > 0)); then
  output artifact-build-commit "$(jq -r '.[0].workflow_run.head_sha' <<<"$artifacts" | tr -d '\r')"
  output artifact-build-branch "$(jq -r '.[0].workflow_run.head_branch' <<<"$artifacts" | tr -d '\r')"
fi

echo "==> Run ID: $RUN_ID"
echo "==> Artifacts:"
jq -r '.[] | "\t\(.id)\t\(.name)\t\(.size_in_bytes) bytes\(if .expired then " (expired)" else "" end)"' <<<"$artifacts"

if [[ -n "$DRY_RUN" && "$DRY_RUN" != "false" ]]; then
  found=$( ((count > 0)) && echo true || echo false)
  output dry_run "$found"
  output found_artifact "$found"
  exit 0
fi

((count > 0)) || no_artifacts "no artifacts found"
[[ "$(jq 'any(.expired)' <<<"$artifacts" | tr -d '\r')" == "false" ]] \
  || no_artifacts "no downloadable artifacts found (expired)"

output found_artifact true
output artifact_ids "$(jq -r 'map(.id) | join(",")' <<<"$artifacts" | tr -d '\r')"
output download true
