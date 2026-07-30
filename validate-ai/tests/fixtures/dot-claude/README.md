# `.claude/` config (fixture)

A minimal repository-level `.claude/` directory used by the `test-validate-ai.yml`
workflow to exercise the non-plugin path of the `validate-ai` action, the
way a repo like [bitwarden/tech-breakdowns](https://github.com/bitwarden/tech-breakdowns/tree/main/.claude)
carries Claude config without being a plugin marketplace.

Editing any file under `.claude/` here makes the action's change detection treat
the pull request as a Claude-related change, which triggers the AI-driven review.
Claude Code discovers this nested `.claude/` as directory-scoped skills and agents
whenever someone works under `dot-claude/`, so keep the fixture content inert.
