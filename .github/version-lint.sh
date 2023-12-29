#!/bin/bash

MISSING_VERSION_FILES=""
# Changed files input and trim with new line
FILES_TO_CHANGE=$(tr ' ' '\n' <<< "$1")

# Read each changed filenames from the input
while IFS= read -r line; do
  # Grep for lines with 'uses' and not having version tag
  VERSION_PATTERN=$(cat "${line}" | grep 'uses: ' | grep -vE '#\s+v[0-9.]+(\s|$)')

  # Check if $VERSION_PATTERN is not empty
  if [[ ! -z "$VERSION_PATTERN" ]]; then
    # Read each line that does not have version tag
    while IFS= read -r each_line; do
      # if the line does not contain bitwarden/gh-actions/* or a .github path
      if ! grep -qE 'bitwarden/gh-actions/*|.github/' <<< $each_line ; then
        echo "${each_line} in file ${line} is missing actions version tag"
        # Add that filename to the variable storing files with missing actions version
        MISSING_VERSION_FILES+=" ${line} "
      fi
    done <<< "$VERSION_PATTERN"
  fi
done <<< "$FILES_TO_CHANGE"

# Trim the variable to be a single line
MISSING_FILES=$(echo $MISSING_VERSION_FILES | tr '\n' ' ')
# Check if the variable is not empty
if [ -n "$MISSING_VERSION_FILES" ]; then
  EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)
  echo "text<<EOF"$'\n'"### :mega: Workflow files ${MISSING_FILES} are missing actions version tag"$'\n'EOF >> $GITHUB_OUTPUT
  echo "text<<EOF"$'\n'"### :mega: Workflow files ${MISSING_FILES} are missing actions version tag"$'\n'EOF  >> $GITHUB_STEP_SUMMARY
fi
