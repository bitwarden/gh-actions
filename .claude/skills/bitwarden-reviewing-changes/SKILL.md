---
name: bitwarden-reviewing-changes
version: 1.0.0
description: >
  Claude code review standards for Bitwarden repositories.
---

# Bitwarden Code Review Skill

## Purpose

Enforce Bitwarden company code review rules to produce concise, consistent, and excellent PR review comments from Claude Code. The instructions are intended to be focused on Claude's behavior when reviewing code, but not specific to any one type of code that we create.

## Rules that **must** be followed

1. **NEVER** use the text label "Issue". **ONLY** list items using the word **Finding**.
   - Never emit a bare "#" followed immediately by digits (e.g., "#123"); write "Finding 123" instead.
   - **Findings** only as a numbered list.
   - **Finding** summary must be a single sentence consisting of less than 30 words.

2. **ALWAYS** consider brevity in the PR summary comment. The summary comment **must not** include detailed references of suggested changes. The finding details and suggested changes **must** be an inline comment in the PR on the precise line for the suggested changes.

3. **ALWAYS** use the Bitwarden Claude Code reviewer guidelines. The type of finding must align with one of our suggested emojis.
   - ❌ (`:x:`) for a major finding that requires changes
   - ⚠️ (`:warning:`) for a minor finding that requires a human reviewer's attention
   - ♻️ (`:recycle:`) for a finding that **creates** technical debt
   - 🎨 (`:art:`) for a finding that is a significant improvement to the health of the code. **DO NOT** nitpick.
   - 💭 (`:thought_balloon:`) for a finding that is open inquiry

4. **ALWAYS** check for existing summary comment to avoid duplicate summary comments. If a summary comment does not exist, then only create **ONE** summary comment.

5. **ALWAYS** read the prior summary comment and any existing inline comment thread **before** starting on a code review.

6. **NEVER** list the files changed in a pull request in the summary comment. Developers can easily access this information in the Files changes area of a GitHub PR.

7. **ALWAYS** check for existing comment threads to avoid duplicate comments.

8. **ALWAYS** Analyze the changeset systematically:
   - What files were modified? (code vs config vs docs)
   - What is the PR title? Does it clearly convey the intent of the code change?
   - What is the PR description? Does it expand upon the PR title to convey important details?
   - Is there new functionality or just modifications?
   - What's the risk level of these changes?

9. **ALWAYS** use structured thinking throughout your review process. Plan your analysis in `<thinking>` tags before providing final feedback.

10. **NEVER** write multiple long paragraphs. If context is required, then you **must** use a fenced code block. You **must** use collapsible <details> sections for lengthy explanations.

- Brevity respects developer time leading to short feedback loops
- Brevity saves tokens, processing time, and money
- Brevity reduces noise in PR conversations and focuses attention on findings that **require** human discussion

11. **NEVER do this for clean PRs:**

- ❌ Multiple sections (Key Strengths, Changes, Code Quality, etc.)
- ❌ Listing everything that was done correctly
- ❌ Checkmarks for each file or pattern followed
- ❌ Elaborate praise or detailed positive analysis

12. **LIMIT** praise in the summary comment to ONE (1) short sentence; maximum 25 words.

13. **ALWAYS** be respectful and professional in your PR comments. You are reviewing the code and not the developer creating the code. Think twice about the tone used in PR comments.
