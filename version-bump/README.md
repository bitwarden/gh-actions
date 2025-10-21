# Version Bump Action

A Github Action that will replace versions in JSON, PLIST, YAML, and XML files.
Specifically created for interacting with AndroidManifest, iOS development plists, Helm Charts, and Node package JSON files.

## Usage

```yml
- name: Bump Android Version
  uses: ./version-bump
  with:
    version: ${{ inputs.version_number }}
    file_path: "./AndroidManifest.xml"
```

## Local Testing

To build and test the Docker action locally, use the `test-local.sh` script:

```bash
# Test with default version (2123.4.5)
./test-local.sh

# Test with a specific version
./test-local.sh 2024.1.0
```

This script will:

1. Build the Docker image locally
2. Run the action against all test fixtures in `tests/fixtures/` in a copied directory
3. Verify that version updates were applied correctly
4. Display a summary of changes
