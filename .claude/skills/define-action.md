---
name: define-action
description: "Phase 1: Interactive requirements gathering for a new GitHub Action. Collects action type, name, inputs/outputs, integrations, and produces a structured SPEC.md."
---

# Define Action - Phase 1: Requirements Gathering

You are gathering requirements for a new custom GitHub Action in the Bitwarden `gh-actions` repository. Your goal is to produce a complete, structured specification that downstream phases will use to scaffold, implement, and validate the action.

## Context

This repository contains ~33 custom GitHub Actions used across Bitwarden's CI/CD pipelines. Actions come in three types:
- **Composite** (Shell/YAML): Most common (~25 actions). Single `action.yml` with shell steps. Best for wrapping other actions or simple bash logic.
- **TypeScript/Node.js**: For complex logic needing npm packages. Uses `@actions/core`, compiled with `ncc`. Example: `get-keyvault-secrets/`.
- **Docker/Python**: For isolated environments or Python-heavy logic. Multi-stage Dockerfile. Example: `version-bump/`.

## Procedure

### Step 1: Determine Action Type

Use AskUserQuestion to ask the user what type of action they want to create. Provide guidance:
- **Composite**: Best for shell scripts, wrapping existing actions, simple orchestration. No build step needed.
- **TypeScript**: Best for complex logic, API integrations needing typed SDKs, or when `@actions/core` features are needed extensively.
- **Docker/Python**: Best for Python-based tools, complex file processing, or when isolation from the runner environment is important.

### Step 2: Collect Core Identity

Ask the user for:
- **Action name**: Must be kebab-case (e.g., `check-permission`, `get-keyvault-secrets`). Validate format.
- **Description**: One-line description of what the action does (used in `action.yml` description field).
- **Purpose**: Why does this action need to exist? What problem does it solve? Which Bitwarden repos will consume it?

### Step 3: Collect Inputs and Outputs

Ask the user to describe:
- **Inputs**: For each input, collect: name (underscore_case), description, required (true/false), default value (if any), whether it contains sensitive data.
- **Outputs**: For each output, collect: name (underscore_case), description, whether it contains sensitive data.

Remind the user:
- Input/output names with multiple words MUST use underscores (enforced by workflow linter)
- Sensitive inputs should be passed via `env:` blocks, never inline in `run:` commands
- Sensitive outputs must be masked with `core.setSecret()` or equivalent

### Step 4: Collect Integration Details

Ask about:
- **Azure integration**: Does the action need Azure login, Key Vault access, or other Azure services?
- **GitHub API**: Does the action call GitHub APIs? Which endpoints?
- **External services**: Slack, Crowdin, Docker Hub, etc.?
- **Other Bitwarden actions**: Does it depend on or compose with other actions in this repo?

### Step 5: Collect Behavioral Details

Ask about:
- **Error handling**: How should failures be handled? Fail fast, skip, continue with degraded output?
- **Idempotency**: Can the action be safely re-run?
- **Platform requirements**: Ubuntu only, or also macOS/Windows runners?
- **Permissions needed**: What GitHub token permissions does the action require?

### Step 6: Produce SPEC.md

Create the action directory and write `{action-name}/SPEC.md` with this structure:

```markdown
# {Action Name} - Specification

## Overview
- **Name**: {action-name}
- **Type**: composite | typescript | docker
- **Description**: {one-line description}
- **Purpose**: {why this action exists}
- **Consumers**: {which repos will use this}

## Inputs
| Name | Description | Required | Default | Sensitive |
|------|-------------|----------|---------|-----------|
| ... | ... | ... | ... | ... |

## Outputs
| Name | Description | Sensitive |
|------|-------------|-----------|
| ... | ... | ... |

## Integrations
- **Azure**: {details or "None"}
- **GitHub API**: {details or "None"}
- **External Services**: {details or "None"}
- **Bitwarden Actions**: {dependencies on other actions in this repo}

## Behavior
- **Error Handling**: {strategy}
- **Idempotent**: {yes/no}
- **Platforms**: {ubuntu-only / cross-platform}
- **Permissions**: {required GitHub token permissions}

## Implementation Notes
{Any additional context from the user about expected behavior, edge cases, etc.}
```

## Important Rules

- Do NOT proceed to scaffolding. Your only job is to produce SPEC.md.
- Do NOT make assumptions about inputs/outputs. Ask the user explicitly.
- Validate that the action name doesn't conflict with existing directories in the repo. Check with `ls` first.
- If the user is vague about inputs/outputs, propose reasonable defaults based on similar actions in the repo, but confirm with the user.
- Always use underscore_case for input/output names (Bitwarden workflow linter requirement).
