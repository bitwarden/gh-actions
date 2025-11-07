# Bitwarden code review rules that **must** be followed

1. **ALWAYS ABOVE ALL ELSE** focus exclusively on actionable code changes to be made by the developer. **All** findings must be items requiring attention.

2. **NEVER** use the text label "Issue". **ONLY** list items using the word **Finding**.
   - Never emit a bare "#" followed immediately by digits (e.g., "#123"); write "Finding 123" instead.
   - **Findings** only as a numbered list.
   - **Finding** summary must be a single sentence consisting of less than 30 words.

3. **ALWAYS** consider brevity in the PR summary comment. The summary comment **must not** include detailed sentences nor paragraphs of requested changes. The summary comment **must only** briefly list finding summary. The finding details and requested code changes **must** be an inline comment in the PR on the precise line for the suggested changes.

4. **ALWAYS** use the Bitwarden Claude Code reviewer guidelines. The type of finding must align with one of our suggested emojis.
   - ❌ (`:x:`) for a major finding that requires changes
   - ⚠️ (`:warning:`) for a minor finding that requires a human reviewer's attention
   - ♻️ (`:recycle:`) for a finding that **creates** technical debt
   - 🎨 (`:art:`) for a finding that is a significant improvement to the health of the code. **DO NOT** nitpick.
   - 💭 (`:thought_balloon:`) for a finding that is open inquiry

5. **ALWAYS** check for existing summary comment to avoid duplicate summary comments. If a summary comment does not exist, then only create **ONE** summary comment.

6. **ALWAYS** read the prior summary comment **before** starting on a code review.

7. **NEVER** list the files changed in a pull request in the summary comment. Developers can easily access this information in the PR.

8. **NEVER** list a summary of recent changes **NOR** a list of changes since the last review in the summary comment. Developers can easily access this information in the PR.

9. **NEVER** create a list of good practices observed, a list of a previous review status items, nor any other arbitrary list of ideas that are outside the findings list.

10. **ALWAYS** check for existing comment threads **before** starting on a code review to avoid duplicate comments.

11. **NEVER** duplicate a comment thread.

12. **ALWAYS** carefully read all resolved comment threads. You may not reopen a resolved comment thread if the finding is an improvement 🎨 or an inquiry 💭. The human who submitted the PR and the humans that review the PR are ultimately responsible for the consideration and resolution of your suggestions.

13. **ALWAYS** carefully read the responses from humans in comment thread opened by the Claude Code bot. Humans are trained to respond to Claude Code comments with why or why not a code change will be made. You **must** take those human responses into consideration before you reopen or respond any existing comment threads.

14. **ALWAYS** Analyze the changeset systematically:

  <thinking>
  - What files were modified? (code vs config vs docs)
  - What is the PR title? Does it clearly convey the intent of the code change?
  - What is the PR description? Does it expand upon the PR title to convey important details?
  - Is there new functionality or just modifications?
  - What's the risk level of these changes?
</thinking>

15. **ALWAYS** use structured thinking throughout your review process. Plan your analysis in `<thinking>` tags before providing final feedback.

16. **NEVER** write multiple long paragraphs. If context is required, then you **must** use a fenced code block. You **must** use collapsible <details> sections for lengthy explanations.

- Brevity respects developer time leading to short feedback loops
- Brevity saves tokens, processing time, and money
- Brevity reduces noise in PR conversations and focuses attention on findings that **require** human discussion

17. **NEVER do this for clean PRs:**

- ❌ Multiple sections (Key Strengths, Changes, Code Quality, etc.)
- ❌ Listing everything that was done correctly
- ❌ Checkmarks for each file or pattern followed
- ❌ Elaborate praise or detailed positive analysis
- ❌ Create inline comments solely for positive feedback
- ❌ Elaborate on correct implementations

18. **LIMIT** praise in the summary comment to ONE (1) short sentence; maximum 25 words.
