---
name: generate-action
description: "Generate a new custom GitHub Action with full compliance checks. Orchestrates define, scaffold, implement, evaluate, and validate phases via the action-generator agent."
argument-hint: "[action-name-or-description]"
---

# Generate Action

You are creating a new custom GitHub Action for the Bitwarden `gh-actions` repository.

This is a phased, AI-powered workflow that will guide you through the entire process:

1. **Define** — Gather requirements interactively (action type, name, inputs/outputs, integrations)
2. **Scaffold** — Generate the directory structure and boilerplate files
3. **Implement** — Write the actual action logic
4. **Evaluate** — Review completeness (input/output coverage, error handling, edge cases)
5. **Validate** — Check formatting, structure, and Bitwarden workflow linter compliance

Delegate to the `action-generator` agent to orchestrate this workflow. Pass along any context the user has already provided about the action they want to create.

The user's request: $ARGUMENTS
