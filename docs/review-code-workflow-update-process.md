# Review Code Workflow

## Architecture

`_review-code.yml` is a reusable workflow that runs Claude Code reviews on PRs. It uses a single composite action (`run-code-review/action.yml`) with a `mode` parameter for routing.

```
_review-code.yml
  ├── check-permission   — verifies PR author has write access
  ├── validation         — reads PR labels, outputs review_variant
  └── review             — calls run-code-review/ with mode={current|vnext}
```

Label routing:

| Label             | `mode`    | Behavior                                     |
| ----------------- | --------- | -------------------------------------------- |
| `ai-review`       | `current` | Tag mode with built-in sticky comment        |
| `ai-review-vnext` | `vnext`   | Agent mode with `upsert-code-review-comment` |
| Neither           | —         | Review skipped                               |

If both labels are present, `ai-review-vnext` takes precedence.

## Development Lifecycle

1. **Modify** — Edit the vnext-conditional steps in `run-code-review/action.yml`. Do not change current-mode steps.
2. **Test** — Apply `ai-review-vnext` label to PRs in downstream repos. Compare against current-mode reviews.
3. **Iterate** — Repeat steps 1-2 until satisfied.
4. **Promote** — Update current-mode steps to match vnext. Merge.
