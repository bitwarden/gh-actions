# Claude Code Configuration

This directory contains Claude Code configuration files for the gh-actions repository.

## Directory Structure

```
.claude/
├── CLAUDE.md              # General project context and guidelines
├── commands/              # Custom slash commands
│   └── review-pr.md
└── prompts/               # Workflow-specific prompts
    └── bitwarden-review-code.md
    └── review-code.md
```

## Automated Workflow Reviews

The `review-code.yml` workflow uses TWO prompt files:

1. **Bitwarden company-wide prompt** (`.claude/prompts/bitwarden-review-code.md`)
   - Stored in `bitwarden/gh-actions` repository
   - Contains common review criteria for all Bitwarden repos
   - Intended to be focused on Claude's behavior when reviewing code
   - Automatically fetched during workflow execution

2. **Repository-specific gate** (`.claude/prompts/review-code.md`)
   - Must exist in each repo that wants Claude reviews
   - Contains repo-specific review instructions
   - Acts as an "opt-in" gate for the review process

**How it works:**

1. Workflow triggers on a PR
2. PR is validated as viable for a Claude Code review
3. Workflow pulls the `.claude/prompts/bitwarden-review-code.md` file from the `gh-actions` repo.
4. Workflow pulls the `.claude/prompts/review-code.md` file from the caller's repo (e.g. `server`, `clients`, `sdk-internal`, etc.)
5. Workflow combines information from Steps 3 and 4 to create a Claude Code Action PR review prompt
6. Claude executes the GitHub Action and appends feedback in the form of a summary comment with findings and inline comments (if necessary).

**To enable in our repos:**

1. Create `.claude/prompts/review-code.md` with review criteria
2. Workflow runs automatically on subsequent pull requests

## Custom Commands

### `/review-pr` - Pull Request Review

Triggers a comprehensive PR code review in your current Claude Code session.

**Usage:**

1. Open Claude Code in this repository
2. Check out the PR branch you want to review
3. Tag @claude and type `/review-pr`

**What it does:**

- Analyzes code quality and best practices
- Checks for security vulnerabilities
- Validates workflow linter compliance
- Reviews performance and efficiency
- Provides structured feedback with action items

**Example:**

```
@claude /review-pr
```

## Best Practices

- **Commands** (`.claude/commands/`): For interactive Claude Code sessions
- **Prompts** (`.claude/prompts/`): For automated GitHub Actions workflows
- **CLAUDE.md**: General project context available in all Claude interactions
