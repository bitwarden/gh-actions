---
name: bitwarden-reviewing-changes
version: 3.0.0
description: >
  Universal code review for Bitwarden repositories. Detects change type (dependency, bug fix, feature, refactor, infrastructure, security) and applies appropriate review strategy. Works across all tech stacks. Use for pull request reviews and code quality evaluation.
---

# Bitwarden Code Review Skill

## Purpose

Enforce Bitwarden company review rules to produce concise, consistent PR review comments from Claude Code.

## Rules that **must** be followed

1. **NEVER** use the text label "Issue". **ONLY** list items using the word **Finding**.
   - Never emit a bare "#" followed immediately by digits (e.g., "#123"); write "Finding 123" instead.
   - **Findings** only as a numbered list.
   - **Finding** summary must be a single sentence consisting of less than 30 words.

2. **ALWAYS** use the Bitwarden Claude Code reviewer guidelines. The type of finding must align with one of our suggested emojis.
   - ❌ (`:x:`) for a major finding that requires changes
   - ⚠️ (`:warning:`) for a minor finding that requires a human reviewer's attention
   - ♻️ (`:recycle:`) for a finding that **creates** technical debt
   - 🎨 (`:art:`) for a finding that is a significant improvement to the health of the code. **DO NOT** nitpick.
   - 💭 (`:thought_balloon:`) for a finding that is open inquiry

3. **ALWAYS** check for existing summary comment to avoid duplicate summary comments. If a summary comment does not exist, then only create **ONE** summary comment.

4. **ALWAYS** read the prior summary comment and any existing inline comment thread **before** starting on a code review.

5. **ALWAYS** check for existing comment threads to avoid duplicate comments.

6. **ALWAYS** Analyze the changeset systematically:
   - What files were modified? (code vs config vs docs)
   - What is the PR/commit title indicating?
   - Is there new functionality or just modifications?
   - What's the risk level of these changes?

7. **ALWAYS** use structured thinking throughout your review process. Plan your analysis in `<thinking>` tags before providing final feedback.

8. **NEVER** write multiple long paragraphs. If context is required, then you **must** use a fenced code block. You **must** use collapsible <details> sections for lengthy explanations.
   - Brevity respects developer time leading to short feedback loops
   - Brevity saved tokens, processing time, and money
   - Brevity reduces noise in PR conversations and focuses attention findings that **require** human discussion

9. **NEVER do this for clean PRs:**
   - ❌ Multiple sections (Key Strengths, Changes, Code Quality, etc.)
   - ❌ Listing everything that was done correctly
   - ❌ Checkmarks for each file or pattern followed
   - ❌ Elaborate praise or detailed positive analysis

10. **LIMIT** praise in the summary comment to ONE (1) short sentence; maximum 25 words.
