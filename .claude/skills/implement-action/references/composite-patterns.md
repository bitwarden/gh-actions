# Composite Action — Implementation Patterns

Distilled from: `check-permission`, `get-pull-request-threads`, `update-pr-comment`, `container-tag`

---

## Step Structure

Every composite step follows this shape:

```yaml
- name: Descriptive step name
  id: step-id
  shell: bash
  env:
    INPUT_NAME: ${{ inputs.input_name }}
    SENSITIVE_TOKEN: ${{ inputs.token }}
  run: |
    set -e

    # === Input Validation ===
    # ... validate all inputs before any logic ...

    # === Core Logic ===
    # ... business logic ...

    # === Set Outputs ===
    echo "output_name=value" >> "$GITHUB_OUTPUT"
```

Key rules:
- Every `run:` block starts with `set -e`
- Every input is passed through `env:` — never inline `${{ inputs.* }}` in `run:`
- Sections are separated with comment headers for readability
- Step `id` must match the output `value` references in the action.yml outputs block

---

## Input Validation

Validate all inputs at the top of the run block, before any business logic.

### Required non-empty string

```bash
if [[ -z "$INPUT_NAME" ]]; then
  echo "::error::Input 'input_name' is required but was empty."
  exit 1
fi
```

### Enum validation

```bash
if [[ ! "$FAILURE_MODE" =~ ^(fail|skip|continue)$ ]]; then
  echo "::error::Invalid failure_mode: must be 'fail', 'skip', or 'continue', got '$FAILURE_MODE'"
  exit 1
fi
```

### Positive integer

```bash
if [[ -z "$PR_NUMBER" ]] || [[ ! "$PR_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "::error::Invalid pr_number: must be a positive integer"
  exit 1
fi
```

### Repository format (owner/repo)

```bash
if [[ -z "$REPOSITORY" ]] || [[ ! "$REPOSITORY" =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]]; then
  echo "::error::Invalid repository format: must be 'owner/repo'"
  exit 1
fi
```

### GitHub username format

```bash
if [[ -z "$USERNAME" ]] || [[ ! "$USERNAME" =~ ^[A-Za-z0-9]([A-Za-z0-9-]{0,37}[A-Za-z0-9])?(\[bot\])?$ ]]; then
  echo "::error::Invalid username format."
  exit 1
fi
```

### Mutually exclusive inputs

```bash
if [[ -n "$BODY_INPUT" && -n "$BODY_FILE_INPUT" ]]; then
  echo "::error::Cannot specify both 'body' and 'body_file' inputs"
  exit 1
fi
```

### File path existence

```bash
if [[ ! -f "$BODY_FILE_INPUT" ]]; then
  echo "::warning::body_file not found at ${BODY_FILE_INPUT}, skipping"
  exit 0
fi
```

---

## Output Setting

Always write to `$GITHUB_OUTPUT`. Quote the variable.

```bash
echo "output_name=$VALUE" >> "$GITHUB_OUTPUT"
```

For multiple outputs, set each on its own line:

```bash
echo "has_permission=$HAS_PERM" >> "$GITHUB_OUTPUT"
echo "user_permission=$USER_PERMISSION" >> "$GITHUB_OUTPUT"
echo "should_proceed=$SHOULD_PROCEED" >> "$GITHUB_OUTPUT"
```

---

## Error Handling

### Annotations

Use GitHub Actions annotations for user-facing messages:

```bash
echo "::error::Description of what went wrong"    # Fails visibly in the UI
echo "::warning::Non-fatal issue"                  # Yellow warning
echo "::notice::Informational message"             # Neutral info
```

### API call with error capture

Capture stderr and check the return code:

```bash
if ! RESPONSE=$(gh api "repos/$REPO/endpoint" --jq '.field' 2>&1); then
  echo "::error::API call failed: $RESPONSE"
  exit 1
fi
```

### Graceful degradation for non-critical calls

```bash
if ! COMMENTS=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json comments 2>&1); then
  echo "::warning::Failed to retrieve comments: $COMMENTS"
  COMMENTS='{"comments":[]}'
fi
```

---

## GitHub API Patterns

### REST API via gh cli

```bash
RESPONSE=$(gh api "repos/${REPOSITORY}/issues/${PR_NUMBER}/comments" \
  --method POST \
  --field body="$BODY")

COMMENT_ID=$(echo "$RESPONSE" | jq -r '.id')
```

### GraphQL API via gh cli

```bash
GRAPHQL_QUERY='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      # ... fields ...
    }
  }
}'

RESPONSE=$(gh api graphql \
  -f query="$GRAPHQL_QUERY" \
  -f owner="$OWNER" \
  -f repo="$REPO" \
  -F pr="$PR_NUMBER")
```

### Parsing owner/repo from combined input

```bash
OWNER="${REPOSITORY%/*}"
REPO="${REPOSITORY#*/}"
```

---

## Conditional Logic

### Mode/strategy switching with case statement

```bash
case "$FAILURE_MODE" in
  fail)
    echo "::error::Permission denied."
    echo "should_proceed=false" >> "$GITHUB_OUTPUT"
    exit 1
    ;;
  skip)
    echo "::warning::Permission denied. Marking for skip."
    echo "should_proceed=false" >> "$GITHUB_OUTPUT"
    exit 0
    ;;
  continue)
    echo "::notice::Permission denied. Continuing."
    echo "should_proceed=true" >> "$GITHUB_OUTPUT"
    exit 0
    ;;
esac
```

### Create-or-update pattern

```bash
if [[ -z "$EXISTING_ID" ]]; then
  RESPONSE=$(gh api "repos/${REPO}/issues/${PR}/comments" \
    --method POST --field body="$BODY")
  CREATED="true"
else
  RESPONSE=$(gh api "repos/${REPO}/issues/comments/${EXISTING_ID}" \
    --method PATCH --field body="$BODY")
  CREATED="false"
fi
```

---

## String Transformation

### Sanitization pipeline

```bash
# Lowercase, strip prefix, replace invalid chars, collapse dashes, trim, truncate
IMAGE_TAG=$(tr '[:upper:]' '[:lower:]' <<< "${INPUT}" \
  | sed -E 's/^v//; s/[^a-z0-9._-]+/-/g; s/-+/-/g; s/^[.-]+|[.-]+$//g' \
  | cut -c1-128 \
  | sed -E 's/[.-]$//')
```

### Ref stripping (branches and tags)

```bash
if [[ "${REF_INPUT}" == refs/* ]]; then
  BRANCH_NAME=$(sed 's|^refs/heads/||; s|^refs/tags/||' <<< "${REF_INPUT}")
else
  BRANCH_NAME="${REF_INPUT}"
fi
```

---

## JSON Processing with jq

### Build structured output

```bash
OUTPUT_JSON=$(jq -n \
  --argjson data "$API_RESPONSE" \
  --arg pr_number "$PR_NUMBER" \
  --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  '{
    pr_number: ($pr_number | tonumber),
    timestamp: $timestamp,
    items: ($data.nodes | map({ id: .id, value: .value }))
  }')

echo "$OUTPUT_JSON" > "$OUTPUT_PATH"
```

### Extract values from JSON response

```bash
TOTAL=$(echo "$OUTPUT_JSON" | jq -r '.total')
STATUS=$(echo "$OUTPUT_JSON" | jq -r '.status')
```
