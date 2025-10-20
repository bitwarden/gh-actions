# Claude Code Configuration

This directory contains Claude Code configuration files for the gh-actions repository.

## Directory Structure

```
.claude/
├── CLAUDE.md              # General project context and guidelines
├── commands/              # Custom slash commands
│   └── review-pr.md      # /review-pr command for PR reviews
└── prompts/               # Workflow-specific prompts
    └── review-code.md    # Used by review-code.yml workflow
```

## Custom Commands

### `/review-pr` - Pull Request Review

Triggers a comprehensive PR code review in your current Claude Code session.

**Usage:**

1. Open Claude Code in this repository
2. Check out the PR branch you want to review
3. Tag @claude and type `/review-pr`

**What it does:**

-   Analyzes code quality and best practices
-   Checks for security vulnerabilities
-   Validates workflow linter compliance
-   Reviews performance and efficiency
-   Provides structured feedback with action items

**Example:**

```
@claude /review-pr
```

## Automated Workflow Reviews

The `review-code.yml` workflow uses the `.claude/prompts/review-code.md` to automatically review PRs via GitHub Actions in each Bitwarden repo. The `review-code.md` is used as a gate to execute the `review-code.yml` workflow. Repos without this file will not see Claude code reviews performed on each pull request.

**How it works:**

1. Workflow triggers on non-draft PRs
2. Reads `.claude/prompts/review-code.md` from the PR's branch
3. Posts review as a sticky comment
4. Updates comment on new commits

**To enable in our repos:**

1. Create `.claude/prompts/review-code.md` with review criteria
2. Workflow runs automatically on subsequent pull requests

## Best Practices

-   **Commands** (`.claude/commands/`): For interactive Claude Code sessions
-   **Prompts** (`.claude/prompts/`): For automated GitHub Actions workflows
-   **CLAUDE.md**: General project context available in all Claude interactions
