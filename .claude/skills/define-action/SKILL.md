---
name: define-action
description: "Gather requirements for a new GitHub Action through interactive questions and produce a SPEC.md specification file."
argument-hint: "[action-name]"
allowed-tools:
  - Read
  - Bash(ls:*)
  - Bash(mkdir:*)
  - Write
  - Glob
---

# Define Action - Requirements Gathering

Gather requirements for a new custom GitHub Action in the Bitwarden `gh-actions` repository. The deliverable is a `SPEC.md` file in the new action's directory that downstream skills (scaffold-action, implement-action) consume.

## Context

This repository contains ~33 custom GitHub Actions. Actions come in three types:
- **Composite** (Shell/YAML): Most common. Single `action.yml` with shell steps. Best for wrapping other actions or simple bash logic.
- **TypeScript/Node.js**: For complex logic needing npm packages. Uses `@actions/core`, compiled with `ncc`. Example: `get-keyvault-secrets/`.
- **Docker/Python**: For isolated environments or Python-heavy logic. Multi-stage Dockerfile. Example: `version-bump/`.

## Input

The skill accepts an optional action name as an argument. If provided, it pre-fills the name and skips the naming question.

**Examples:**
- `define-action` -- start from scratch, ask all questions
- `define-action report-deploy-status` -- pre-fill name as `report-deploy-status`

## Procedure

### Step 1: Validate Name (if provided)

If an action name was provided as an argument:
1. Use `ls` in the repository root to verify the name does not conflict with an existing directory.
2. Validate the name is kebab-case (lowercase letters, numbers, hyphens only).
3. If the name conflicts or is invalid, report the issue and ask for a corrected name.

If no name was provided, proceed to Step 2.

### Step 2: Collect Requirements

Gather all of the following in as few rounds as possible. Present the full list of questions upfront so the user can answer in one or two responses rather than six rounds of back-and-forth.

**Core identity:**
- **Action name**: Must be kebab-case (e.g., `check-permission`, `get-keyvault-secrets`). Skip if already provided.
- **Action type**: Composite, TypeScript, or Docker/Python. Provide guidance:
  - Composite: Best for shell scripts, wrapping existing actions, simple orchestration. No build step.
  - TypeScript: Best for complex logic, API integrations needing typed SDKs, extensive `@actions/core` usage.
  - Docker/Python: Best for Python-based tools, complex file processing, or runner isolation.
- **Description**: One-line description for the `action.yml` description field.
- **Purpose**: Why does this action need to exist? What problem does it solve? Which Bitwarden repos will consume it?

**Inputs and outputs:**
- **Inputs**: For each: name (underscore_case), description, required (true/false), default value, whether it contains sensitive data.
- **Outputs**: For each: name (underscore_case), description, whether it contains sensitive data.
- Remind the user: multi-word input/output names MUST use underscores (workflow linter requirement). Sensitive inputs should use `env:` blocks, not inline in `run:`. Sensitive outputs must be masked.

**Integrations:**
- Azure (login, Key Vault, other services)?
- GitHub API (which endpoints)?
- External services (Slack, Crowdin, Docker Hub)?
- Other Bitwarden actions in this repo?

**Behavior:**
- Error handling strategy (fail fast, skip, degrade)?
- Idempotent (safe to re-run)?
- Platform requirements (Ubuntu only, or also macOS/Windows)?
- Required GitHub token permissions?

### Step 3: Validate

1. Use `ls` in the repository root to verify the action name does not conflict with an existing directory.
2. Use `Glob` with pattern `*/action.yml` to list existing actions for reference.
3. If either check reveals a conflict, report it and ask for a corrected name before proceeding.

### Step 4: Write SPEC.md

1. Run `mkdir -p {action-name}` to create the action directory.
2. Generate an ASCII architecture diagram for the `## Architecture Diagram` section. The diagram should show:
   - All inputs flowing into the action (mark sensitive inputs)
   - Processing steps in execution order (validation → core logic → output setting)
   - Integration points (Azure, GitHub API, external services) as callouts
   - All outputs flowing out
   - Error/failure paths where applicable
   - Use box-drawing characters (`┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼ ▼ ▶`) for clean rendering
3. Write `SPEC.md` to `{action-name}/SPEC.md` using the template below.

## Output Format

The `SPEC.md` file must follow this exact structure:

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
| {name} | {description} | {yes/no} | {value or N/A} | {yes/no} |

## Outputs
| Name | Description | Sensitive |
|------|-------------|-----------|
| {name} | {description} | {yes/no} |

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

## Architecture Diagram

\`\`\`
{ASCII diagram showing: inputs → processing steps → outputs, with integrations and error paths}
\`\`\`

## Implementation Notes
{Any additional context about expected behavior, edge cases, etc.}
```

**Zero-inputs case:** If the action has no inputs, write the Inputs table with a single row: `| N/A | No inputs required | N/A | N/A | N/A |`. Same pattern for Outputs.

## Important Notes

- This skill ONLY produces SPEC.md. It does not scaffold files or write implementation code.
- Do not make assumptions about inputs/outputs. Ask the user explicitly. If the user is vague, propose reasonable defaults based on similar actions in the repo, but confirm before writing.
- Always use underscore_case for input/output names (Bitwarden workflow linter requirement).
- Never include example secrets, credentials, or real Key Vault names in the SPEC.md.
- If the user abandons the process before all requirements are collected, do not write SPEC.md. Inform the user that the specification is incomplete.

## Related Skills

After producing SPEC.md, the next steps in the pipeline are:
- **scaffold-action**: Generate boilerplate files from the specification. Example: `scaffold-action {action-name}`
- **implement-action**: Write the working implementation. Example: `implement-action {action-name}`
- **evaluate-action**: Review implementation completeness. Example: `evaluate-action {action-name}`
- **validate-action**: Check formatting and linter compliance. Example: `validate-action {action-name}`
