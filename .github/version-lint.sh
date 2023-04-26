#!/bin/bash

MISSING_VERSION_FILES=""
FILES_TO_CHANGE=$(tr ' ' '\n' <<< "$1")

while IFS= read -r line; do
  VERSION_PATTERN=$(cat "${line}" | grep 'uses: ' | grep -vE '#\s+v[0-9.]+(\s|$)')

  if [[ ! -z "$VERSION_PATTERN" ]]; then
    while IFS= read -r each_line; do
      if ! grep -qE 'bitwarden/gh-actions/*' <<< $each_line ; then
        MISSING_VERSION_FILES+=" ${line} "
      fi
    done <<< "$VERSION_PATTERN"
  fi
done <<< "$FILES_TO_CHANGE"

MISSING_FILES=$(echo $MISSING_VERSION_FILES | tr '\n' ' ')
if [ -n "$MISSING_VERSION_FILES" ]; then
  echo "### :mega: Workflow files ${MISSING_FILES} are missing actions version tag" # >> $GITHUB_STEP_SUMMARY
  exit 1
fi
