Invoke the `bitwarden-reviewing-changes` skill to perform a code review of this PR.

Note: The PR branch is already checked out in the current working directory.

**Critical Requirements:**
- Use "Finding [N]" terminology (never "Issue #N" - avoids GitHub auto-links)
- Create separate inline comment for each finding
- **Always** check for the existence of inline comment before adding another. **No** duplicate comments for the same finding are allowed.
- Use `<details>` tags for explanations inside inline comments
- Follow repo context from `.claude/CLAUDE.md`

The skill will handle the rest.
