# Codecov GitHub Action Proxy

This is a proxy action that wraps the official [Codecov GitHub Action](https://github.com/codecov/codecov-action).

## Updating to a New Version

When a new version of the Codecov action is released, follow these steps:

### 1. Copy Inputs from original action
- Visit the [Codecov action repository](https://github.com/codecov/codecov-action/blob/main/action.yml)
- Copy all input definitions from the upstream `action.yml`
- Paste them into the `inputs` section of this action's `action.yml`

### 2. Update the Composite Action Step
- For any new inputs, add corresponding `with:` entries in the composite step that passes them through to the codecov action
- For any removed inputs, remove the corresponding `with:` entries
- Ensure the `uses:` reference is updated to the new version git hash and tag in the comment

### 3. Update the Version Pin
- Update the `version:` input in the composite step to the new release version
- **⚠️ Note:** `version: v11.2.3` is currently pinned and should not be bumped until this issue is resolved: https://github.com/getsentry/prevent-cli/issues/101

## Example

The `action.yml` file defines all available inputs that can be passed to this proxy action, which are then forwarded to the upstream Codecov action in the composite step.
