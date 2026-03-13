# Run Code Review

Runs an AI-powered code review using Claude Code with Bitwarden plugins.

## Modes

Both modes retrieve existing PR review threads before invoking Claude and load the same Bitwarden plugin set.

### `current` (default)

Uses the built-in `claude-code-action` features `use_sticky_comment` and `track_progress` for comment management.

### `vnext`

Creates a placeholder PR comment via `update-pr-comment`, then passes the comment ID to Claude. Claude writes its final summary to `/tmp/review-summary.md`. A post-step updates the PR comment from that file. Grants the `Write` tool so Claude can produce the summary file.

## Development Lifecycle

1. **Understand** -- Read `action.yml` and this README. Steps are gated by `if: inputs.mode == 'current'` or `if: inputs.mode == 'vnext'`. The caller workflow (`_review-code.yml`) maps PR labels to the `mode` input; this action only sees the mode value.
2. **Plan** -- Define what you want to change and why. Current-mode steps are production; vnext-mode steps are the experiment. Know which you are targeting before editing.
3. **Modify** -- Add or edit vnext-gated steps in `action.yml`. Do not change current-mode steps.
4. **Test** -- Apply the `ai-review-vnext` label to PRs in downstream repos and compare against current-mode reviews.
5. **Iterate** -- Repeat steps 3-4 until satisfied.
6. **Promote** -- In a separate PR, update current-mode steps to match vnext, remove the vnext-specific steps, and merge.
7. **Document** -- Update the Modes section of this README to describe the new current and vnext behaviors.
