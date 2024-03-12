# Version Next Action

A Github Action that will calcaulate the next release version based on input.

## Usage

```yml
- name: Get Next Release Version
uses: ./version-next
with:
    version: ${{ inputs.version_number }}
```
