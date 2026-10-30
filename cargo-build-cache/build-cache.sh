#!/usr/bin/env bash
# Lets a cached `target/` directory be reused, so Cargo only rebuilds the crates that changed.
#
# Cargo decides whether a workspace crate is up to date by comparing the modification times of its
# source files with those of its build output. A fresh checkout gives every file the current time,
# which makes every workspace crate look changed.
#
#   build-cache.sh mark <pending>     After restoring the cache, before the build: set all tracked
#                                     files to a fixed old time, then mark as new only the files
#                                     whose hash differs from the record stored with the cache. Writes
#                                     the hashes of the files the build is about to compile to
#                                     <pending>.
#   build-cache.sh record <pending>   After a successful build: store <pending> next to the build
#                                     output, as the record of its inputs.
#
# The hashes are taken before the build, so a later step that rewrites a tracked file (a test that
# updates a snapshot, for example) can't make the record claim content that was never compiled.
# Tracked files must not change between `mark` and the build.
#
# Run it from the Cargo workspace root. Only the files git tracks below that directory are listed.
#
# If there is no stored record, `mark` leaves every file at its checkout time, so Cargo rebuilds all
# workspace crates. That is slower but never stale.
set -euo pipefail

INPUTS_FILE="target/.build-cache-inputs"

# Prints "<hash>\t<path>" for every tracked file that exists in the working tree. The hash is of
# the working-tree content (not the index), so local modifications made before the build count.
# Paths are read NUL-separated so they are never quoted or split. `git hash-object --stdin-paths`
# reads one path per line, so a path containing a newline can't be listed: fail in that case.
list_build_inputs() {
  local paths
  paths=$(mktemp)
  git ls-files -z --cached | while IFS= read -r -d '' path; do
    if [ -e "$path" ] || [ -L "$path" ]; then
      printf '%s\0' "$path"
    fi
  done > "$paths"
  if [ "$(tr -cd '\n' < "$paths" | wc -c)" -gt 0 ]; then
    echo "A tracked path contains a newline, can't record build inputs." >&2
    rm -f "$paths"
    return 1
  fi
  # `git hash-object --stdin-paths` resolves paths from the repository root, not the current
  # directory, so the paths are prefixed with the current directory's path within the repository.
  local prefix top
  prefix=$(git rev-parse --show-prefix)
  top=$(git rev-parse --show-toplevel)
  # Checked explicitly: callers run this in an `if`, where `set -e` does not apply.
  if ! tr '\0' '\n' < "$paths" | awk -v prefix="$prefix" '{ print prefix $0 }' \
    | git -C "$top" hash-object --stdin-paths | paste - <(tr '\0' '\n' < "$paths"); then
    rm -f "$paths"
    return 1
  fi
  rm -f "$paths"
}

record() {
  local pending=$1
  if [ ! -f "$pending" ]; then
    echo "No build inputs were listed before the build, can't record them." >&2
    return 1
  fi
  mkdir -p target
  cp "$pending" "$INPUTS_FILE"
  echo "Recorded $(wc -l < "$INPUTS_FILE" | tr -d ' ') build inputs"
}

mark() {
  local pending=$1
  rm -f "$pending"
  if ! list_build_inputs > "$pending"; then
    rm -f "$pending"
    echo "Building all workspace crates."
    return
  fi

  if [ ! -f "$INPUTS_FILE" ]; then
    echo "No record of the cached build's inputs, building all workspace crates."
    return
  fi

  local recorded changed count
  recorded=$(mktemp)
  changed=$(mktemp)
  # The record only describes the restored build output. Remove it, so a cache saved later without
  # a fresh record makes the next run rebuild everything instead of trusting an old record.
  mv "$INPUTS_FILE" "$recorded"

  # A file is changed if it is new or its content differs from the recorded list. The hash is
  # everything before the first tab, the path everything after it.
  awk 'NR == FNR { i = index($0, "\t"); recorded[substr($0, i + 1)] = substr($0, 1, i - 1); next }
    { i = index($0, "\t"); path = substr($0, i + 1); if (recorded[path] != substr($0, 1, i - 1)) print path }' \
    "$recorded" "$pending" > "$changed"

  git ls-files -z | xargs -0 touch -h -c -t 200001010000 --

  count=$(wc -l < "$changed" | tr -d ' ')
  echo "Files changed since the cached build: $count"
  if [ "$count" -gt 0 ]; then
    tr '\n' '\0' < "$changed" | xargs -0 touch -h -c --
    head -50 "$changed"
  fi
  rm -f "$recorded" "$changed"
}

if [ $# -ne 2 ]; then
  echo "Usage: $0 record|mark <pending>" >&2
  exit 2
fi

case "$1" in
  record) record "$2" ;;
  mark) mark "$2" ;;
  *)
    echo "Usage: $0 record|mark <pending>" >&2
    exit 2
    ;;
esac
