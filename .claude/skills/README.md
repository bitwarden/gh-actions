# Bitwarden Claude Skills

This directory defines company-wide Claude Code _skills_ used by our reusable workflows across Bitwarden repositories.

## 🧩 Overview

Each subfolder represents a _Claude Skill_, which defines how Claude should behave in specific contexts (e.g., reviewing code, triaging issues, writing documentation).

The appropriate skill is loaded by the reusable workflow to accomplish the task.

## ⚙️ Adding a New Skill

1. Create a new subfolder: `.claude/skills/<new-skill-name>/`
2. Add at minimum a `SKILL.md` file.
3. (Optional) Add a `postprocess.md` or `README.md` if the logic is non-trivial.
4. Update reusable workflows or prompts to call it via `/run <skill-name>`.

> 🔒 **Important:** All skills must comply with the global `.claude/CLAUDE.md` rules for tone, verbosity, and markdown format.

## Bitwarden Review Changes Skill

This repo supports **two-tier skill composition** for the code reviewing skill.

### Central Skills

- `bitwarden-reviewing-changes/`
- Company-wide code review standards
- Fetched automatically by reusable workflows
- Applied to ALL Bitwarden repos

### Repo-Specific Skills (Optional)

- `reviewing-changes/`
- Domain-specific overrides (e.g., Android, iOS, sdk, etc.)
- Committed in individual repos
- Takes precedence over central skill when conflicts occur
