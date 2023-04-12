#!/bin/bash

MISSING_VERSION_FILES=""
IFS=' ' read -ra lines <<< "$1"
for line in "${lines[@]}"; do
VERSION_PATTERN=$(cat "${line}" | grep 'uses: ' | grep -vE '#\s+v[0-9.]+(\s|$)')
if [[ $(grep -E 'uses: ' <<< $VERSION_PATTERN) ]]; then
  echo "Workflow file ${line} is missing one or more version tags"
  MISSING_VERSION_FILES+=" ${line}"
fi
done
# echo "$MISSING_VERSION_FILES" >> $GITHUB_OUTPUT
if [ $( wc -w <<< $MISSING_VERSION_FILES) -gt 0 ]; then
  # echo "### :mega: Workflow file ${MISSING_VERSION_FILES} is missing one or more version tags" >> $GITHUB_STEP_SUMMARY
  exit 1
fi