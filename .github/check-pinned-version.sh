#!/bin/bash

MISSING_VERSION_FILES="";
IFS=' ' read -ra lines <<< "${CHANGED_FILES}"
for line in "${lines[@]}"; do
  VERSION_PATTERN=cat "${line}" | grep 'uses: ' | awk -F "@" '{print $2}' | awk -F "#" '{print $2}'
  # v starts a release tag, n is for our actions that have "no release tag" comment
  if ! echo $VERSION_PATTERN | grep -qE ' v'; then
    echo "Workflow file ${line} is missing a version tag"
    MISSING_VERSION_FILES+=" ${line} "
  fi
done
echo "### :mega: Workflow files ${MISSING_VERSION_FILES} is missing actions version tag" >> $GITHUB_STEP_SUMMARY
exit 1