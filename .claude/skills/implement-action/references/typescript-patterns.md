# TypeScript Action — Implementation Patterns

Distilled from: `get-keyvault-secrets`

---

## Entry Point Structure

Every TypeScript action follows this shape in `src/main.ts`:

```typescript
import * as core from '@actions/core';

async function run(): Promise<void> {
  try {
    // === Read Inputs ===
    const requiredInput = core.getInput('input_name', { required: true });
    const optionalInput = core.getInput('optional_input', { required: false }) || 'default';

    // === Validate Inputs ===
    // ... validation logic ...

    // === Mask Sensitive Values ===
    core.setSecret(sensitiveValue);

    // === Core Logic ===
    // ... business logic ...

    // === Set Outputs ===
    core.setOutput('output_name', value);
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

run();
```

Key rules:
- Single `run()` async function as the entry point
- Entire body wrapped in try/catch
- `core.setFailed()` in the catch block — never throw unhandled
- Read all inputs at the top, validate immediately after

---

## Input Reading

### Required input

```typescript
const keyvault = core.getInput('keyvault', { required: true });
```

GitHub Actions will fail the step if a required input is missing, but always validate the value too.

### Optional input with default

```typescript
const format = core.getInput('format', { required: false }) || 'json';
```

### Comma-separated list input

```typescript
const secretNames = core.getInput('secrets', { required: true })
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);
```

### Boolean input

```typescript
const verbose = core.getInput('verbose', { required: false }).toLowerCase() === 'true';
```

---

## Input Validation

Validate after reading, before any business logic:

```typescript
if (!inputValue.match(/^[a-z0-9-]+$/)) {
  throw new Error(`Invalid input_name: must be lowercase alphanumeric with hyphens, got '${inputValue}'`);
}

if (secretNames.length === 0) {
  throw new Error('Input "secrets" must contain at least one secret name');
}
```

The throw will be caught by the outer try/catch and passed to `core.setFailed()`.

---

## Secret Masking

Mask sensitive values **before any logging or output setting**:

```typescript
core.setSecret(secret.value);
core.setOutput(secretName, secret.value);
```

Order matters — if you set the output before masking, the value may appear in logs.

---

## Output Setting

```typescript
core.setOutput('result', value);
core.setOutput('count', items.length.toString());
```

Outputs are always strings. Convert numbers and booleans explicitly.

---

## Error Handling

### Top-level catch

Every action uses this pattern:

```typescript
catch (error) {
  core.setFailed(error instanceof Error ? error.message : String(error));
}
```

### Typed error handling for SDK calls

```typescript
try {
  const secret = await client.getSecret(secretName);
  if (secret.value === undefined) {
    throw new Error(`Secret "${secretName}" has no value`);
  }
} catch (error) {
  if (error instanceof RestError && error.statusCode === 404) {
    throw new Error(`Secret "${secretName}" not found in vault "${keyvault}"`);
  }
  throw error; // Re-throw unexpected errors
}
```

### Iterating with error accumulation

```typescript
const errors: string[] = [];
for (const name of items) {
  try {
    // ... process item ...
  } catch (error) {
    errors.push(`${name}: ${error instanceof Error ? error.message : String(error)}`);
  }
}
if (errors.length > 0) {
  throw new Error(`Failed to process ${errors.length} item(s):\n${errors.join('\n')}`);
}
```

---

## Azure SDK Integration

### Credential and client setup

```typescript
import { AzureCliCredential } from '@azure/identity';
import { SecretClient } from '@azure/keyvault-secrets';

const credential = new AzureCliCredential();
const client = new SecretClient(
  `https://${keyvault}.vault.azure.net`,
  credential,
);
```

### Retrieving secrets with masking

```typescript
for (const secretName of secretNames) {
  const secret = await client.getSecret(secretName);
  if (secret.value === undefined) {
    throw new Error(`Secret "${secretName}" has no value`);
  }
  core.setSecret(secret.value);
  core.setOutput(secretName, secret.value);
}
```

---

## Package Dependencies

### Minimum required

```json
{
  "dependencies": {
    "@actions/core": "^1.11.1"
  },
  "devDependencies": {
    "@vercel/ncc": "^0.38.4",
    "typescript": "^5.9.3"
  }
}
```

### Common additions by integration

| Integration | Package |
|---|---|
| GitHub API | `@actions/github` |
| Shell execution | `@actions/exec` |
| File globbing | `@actions/glob` |
| Azure Key Vault | `@azure/identity`, `@azure/keyvault-secrets` |
| Azure Storage | `@azure/identity`, `@azure/storage-blob` |
| HTTP requests | `@actions/http-client` |

Only add dependencies required by the SPEC.md integrations.
