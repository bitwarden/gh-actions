---
name: bitwarden-reviewing-changes
version: 3.0.0
description: >
  Universal code review for Bitwarden repositories. Detects change type (dependency, bug fix, feature, refactor, infrastructure, security) and applies appropriate review strategy. Works across all tech stacks. Use for pull request reviews and code quality evaluation.
---

# Bitwarden Code Review Skill

Universal code review orchestrator using progressive disclosure.

## Purpose

Enforce Bitwarden company review rules to produce concise, consistent PR review comments from Claude Code.

## **Hard rules that must be followed**

- **NEVER** use the text label "Issue". **ONLY** list items using the word **Finding**.
- Never emit a bare "#" followed immediately by digits (e.g., "#123"); write "Finding 123" instead.
- Limit Praise to 1 short sentence; maximum 15 words.
- **Findings** only as a numbered list. Each finding must be a single line:
  1. [Major|Minor|Info] Short summary <=12 words — Short suggestion <=20 words
- **NEVER** write long paragraphs. If context is required include a single fenced code block <=6 lines.
- **IMPORTANT**: Use structured thinking throughout your review process. Plan your analysis in `<thinking>` tags before providing final feedback.
- **ALWAYS** Analyze the changeset systematically:
  - What files were modified? (code vs config vs docs)
  - What is the PR/commit title indicating?
  - Is there new functionality or just modifications?
  - What's the risk level of these changes?
- **NEVER do this for clean PRs:**
  - ❌ Multiple sections (Key Strengths, Changes, Code Quality, etc.)
  - ❌ Listing everything that was done correctly
  - ❌ Checkmarks for each file or pattern followed
  - ❌ Elaborate praise or detailed positive analysis

**Why brevity matters:**

- Respects developer time (quick approval = move forward faster)
- Reduces noise in PR conversations
- Saves tokens and processing time
- Focuses attention on PRs that actually need discussion
