# Run Code Review

Runs an AI-powered code review using Claude Code with Bitwarden plugins.

## Modes

| Mode                | Label             | Behavior                                     |
| ------------------- | ----------------- | -------------------------------------------- |
| `current` (default) | `ai-review`       | Tag mode with built-in sticky comment        |
| `vnext`             | `ai-review-vnext` | Agent mode with `upsert-code-review-comment` |

- **`current`** — Claude Code Action manages progress tracking and sticky comments via tag mode.
- **`vnext`** — Our plugin prompt is the sole instruction. Sticky comment is managed by `upsert-code-review-comment` before and after the review. Claude writes its summary to `/tmp/review-summary.md`, which is posted to the PR automatically.

See [docs/review-code-workflow-update-process.md](../docs/review-code-workflow-update-process.md) for architecture and development lifecycle.
