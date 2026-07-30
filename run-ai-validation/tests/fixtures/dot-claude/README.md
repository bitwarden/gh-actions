# `.claude/` config (fixture)

A minimal repository-level `.claude/` directory used by the `test-validate-ai.yml`
workflow to exercise the non-plugin path of the `run-ai-validation` action, the
way a repo like [bitwarden/tech-breakdowns](https://github.com/bitwarden/tech-breakdowns/tree/main/.claude)
carries Claude config without being a plugin marketplace.

Editing any file under `.claude/` here makes the action's change detection treat
the pull request as a Claude-related change, which triggers the AI-driven review.
Nothing here is loaded as real config; the nested path keeps it out of the way of
Claude Code's own `.claude/` lookup.
