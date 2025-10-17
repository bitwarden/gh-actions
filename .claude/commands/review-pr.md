---
description: Review the current pull request with comprehensive code analysis
---

You are conducting a thorough pull request code review for the Bitwarden gh-actions repository.

## Current Context
- Repository: bitwarden/gh-actions
- This is a collection of reusable GitHub Actions workflows and custom actions
- The code must follow Bitwarden's workflow linter rules
- Security and reliability are paramount

## Review Instructions

Perform a comprehensive review of the current PR with focus on:

### 1. **Code Quality & Best Practices**
- Adherence to GitHub Actions best practices
- Proper error handling and validation
- Code maintainability and clarity
- Appropriate use of GitHub Actions syntax

### 2. **Security Implications**
- No hardcoded secrets or credentials
- Proper permission scoping
- Input validation and sanitization
- Protection against command injection
- Safe handling of user-provided data

### 3. **Workflow Linter Compliance**
Verify compliance with Bitwarden workflow linter rules:
- Actions pinned to commit SHA with version comment
- Permissions explicitly defined
- Runner versions pinned (e.g., ubuntu-24.04)
- Proper naming conventions (capitalized)
- Only approved actions are used

### 4. **Performance & Efficiency**
- Appropriate caching strategies
- Parallel job execution where possible
- Minimal redundant operations
- Efficient use of GitHub Actions resources

### 5. **Testing & Validation**
- Adequate test coverage for new features
- Test workflows follow established patterns
- Integration with existing test infrastructure

## Output Format

Provide a structured review with:

1. **Summary of Changes**
   - High-level overview of what this PR accomplishes
   - Key files modified and their impact

2. **Critical Issues** (if any)
   - Security vulnerabilities
   - Breaking changes
   - Non-compliant code that must be fixed

3. **Suggested Improvements**
   - Optimization opportunities
   - Better patterns or approaches
   - Documentation enhancements

4. **Good Practices Observed**
   - Notable positive aspects (be concise)
   - Correct security implementations
   - Well-structured code

5. **Action Items**
   - Specific tasks for the author
   - Priority level (Critical/High/Medium/Low)

Use collapsible `<details>` sections for lengthy explanations to keep the review readable.

**Important**: Focus on being thorough about issues and improvements. For good practices, be brief and just note what was done well.
