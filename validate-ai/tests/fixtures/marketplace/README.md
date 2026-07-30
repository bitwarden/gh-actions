# Example Marketplace (fixture)

A fixture Claude Code plugin marketplace used by the `test-validate-ai.yml`
workflow to exercise the bundled validation scripts (`validate-plugin-structure.sh`
and `validate-marketplace.sh`) against a known-good tree. It is not a real
marketplace.

## Plugins

| Plugin                                    | Version | Description                                              |
| ----------------------------------------- | ------- | -------------------------------------------------------- |
| [example-plugin](plugins/example-plugin/) | 1.0.0   | Fixture plugin used to exercise the validate-ai scripts. |
