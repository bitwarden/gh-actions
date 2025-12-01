# Claude Code Configuration

This directory contains Claude Code configuration files for the gh-actions repository.

## Directory Structure

```
.claude/
├── CLAUDE.md              # General project context and guidelines
├── commands/              # Custom slash commands
│   └── review-pr.md
└── prompts/               # Workflow-specific prompts
    └── review-code.md     # Repo specific review guidelines
```

## Automated Workflow Reviews

The `review-code.yml` workflow uses custom plugins from Bitwarden's AI plugin marketplace:

1. **Bitwarden code review agent**
   - Plugin hosted in `bitwarden/ai-plugins` repository
   - Contains specialized review agent, with common review criteria for all Bitwarden repos
   - Intended to be focused on Claude's behavior when reviewing code
   - Automatically installed during workflow execution

2. **Repository-specific review guidelines** (`.claude/prompts/review-code.md`)
   - Optional repo-specific review instructions

**How it works:**

1. Workflow triggers on a PR.
2. PR is validated as viable for a Claude Code review.
3. Workflow adds the `bitwarden/ai-plugins` marketplace and installs necessary plugins.
4. Workflow invokes the `bitwarden-code-reviewer` agent to perform a review of the pull request.
5. `bitwarden-code-reviewer` agent identifies and ingests the local repo's `.claude/prompts/review-code.md` file.
6. `bitwarden-code-reviewer` agent reviews the changes and appends feedback in the form of a brief summary comment with findings and inline comments (if necessary).

**To customize review guidelines in our repos:**

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
