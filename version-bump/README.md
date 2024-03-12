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
