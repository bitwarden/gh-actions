# Version Bump Action

A Github Action that will replace versions in JSON, PLIST, and XML files. Specifically created for interacting with AndroidManifest, iOS development plists, and Node package JSON files.

## Usage

```yml
- name: Bump Android Version
uses: ./version-bump
with:
    version: ${{ github.event.inputs.version_number }}
    file_path: "./AndroidManifest.xml"
```

