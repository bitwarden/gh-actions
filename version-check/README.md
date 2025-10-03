# Version Check Action

## Summary

Given a version and the validation type, will validate that the version is valid.<br>
If the validation fails, the action run will result in an exit code of 1.

## Inputs
- Version - Version number string
- Validation Type - Whether to use SemVer or CalVer (default) validation

## Outputs
None

## Example Snippets

Validating SemVer
```
    steps:
      - name: Validate version - semver
        uses: bitwarden/gh-actions/version-check@main
        with:
          version: 1.0.0
          validation_type: semver
```

Validating CalVer
```
    steps:
      - name: Validate version - calver
        uses: bitwarden/gh-actions/version-check@main
        with:
          version: 2025.6.1
          validation_type: calver # This is also the default if not provided
```
