#!/usr/bin/env bash
set -euo pipefail

# Detect git-modified files in the working tree and emit them for upload.
#
# Only modifications to existing tracked files are supported. The action fails
# if any files are added (new/untracked) or deleted, because the downstream
# consumer commits the downloaded files over an existing checkout and cannot
# safely reconcile additions or removals.
#
# Required environment:
#   MODIFIED_FILES_LIST - path to write the newline-separated list of modified
#                         files to (consumed by tar in the next step).
#   GITHUB_OUTPUT       - set by GitHub Actions; receives `count` and
#                         `modified_files` outputs.

modified=()
added=()
deleted=()
other=()

# core.quotepath=false keeps non-ASCII paths unquoted so tar can read them.
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  status="${line:0:2}"
  path="${line:3}"
  x="${status:0:1}"
  y="${status:1:1}"

  if [[ "$status" == "??" ]]; then
    added+=("$path")
  elif [[ "$x" == "A" || "$y" == "A" ]]; then
    added+=("$path")
  elif [[ "$x" == "D" || "$y" == "D" ]]; then
    deleted+=("$path")
  elif [[ "$x" == "R" || "$y" == "R" || "$x" == "C" || "$y" == "C" ]]; then
    other+=("$path ($status)")
  elif [[ "$x" == "M" || "$y" == "M" || "$x" == "T" || "$y" == "T" ]]; then
    modified+=("$path")
  else
    other+=("$path ($status)")
  fi
done < <(git -c core.quotepath=false status --porcelain)

fail=0
if [[ ${#added[@]} -gt 0 ]]; then
  echo "::error::Detected added/untracked files, which are not supported:"
  printf '::error::  %s\n' "${added[@]}"
  fail=1
fi
if [[ ${#deleted[@]} -gt 0 ]]; then
  echo "::error::Detected deleted files, which are not supported:"
  printf '::error::  %s\n' "${deleted[@]}"
  fail=1
fi
if [[ ${#other[@]} -gt 0 ]]; then
  echo "::error::Detected renamed/copied/unsupported changes, which are not supported:"
  printf '::error::  %s\n' "${other[@]}"
  fail=1
fi
if [[ $fail -ne 0 ]]; then
  exit 1
fi

if [[ ${#modified[@]} -eq 0 ]]; then
  echo "::error::No modified files detected. Nothing to upload."
  exit 1
fi

echo "Detected ${#modified[@]} modified file(s):"
printf '  %s\n' "${modified[@]}"

# Write the list for tar consumption (one path per line).
printf '%s\n' "${modified[@]}" > "$MODIFIED_FILES_LIST"

# Emit step outputs.
{
  echo "count=${#modified[@]}"
  echo "modified_files<<EOF"
  printf '%s\n' "${modified[@]}"
  echo "EOF"
} >> "$GITHUB_OUTPUT"
