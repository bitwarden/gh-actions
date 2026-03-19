# Sonar workflow

## Summary

Runs a SonarCloud quality scan on pull requests and pushes. Retrieves a Bitwarden-managed Sonar token from Azure Key Vault and analyzes the repository using the configured Sonar scanner.

## Usage

See [`sonar.yml`](./sonar.yml) for a calling workflow template.

The calling workflow must pass the following secrets:

```yaml
jobs:
  quality:
    uses: bitwarden/gh-actions/.github/workflows/_sonar.yml@main
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
```

## Inputs

| Input                   | Type     | Required | Default   | Description                                            |
| ----------------------- | -------- | -------- | --------- | ------------------------------------------------------ |
| `sonar-config`          | `string` | No       | `default` | Scanner configuration: `default`, `maven`, or `dotnet` |
| `sonar-sources`         | `string` | No       | —         | Glob pattern(s) for source files to include            |
| `sonar-tests`           | `string` | No       | —         | Glob pattern(s) for test files to include              |
| `sonar-test-inclusions` | `string` | No       | —         | Glob pattern(s) for test files to include in analysis  |
| `sonar-exclusions`      | `string` | No       | —         | Glob pattern(s) for files to exclude from analysis     |

Secrets:

- `AZURE_SUBSCRIPTION_ID`
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`

## Outputs

None

## Requirements

- The calling repository must have access to the `gh-org-bitwarden` Azure Key Vault, which contains the `SONAR-TOKEN` secret used to authenticate with SonarCloud.

### GitHub Permissions

The calling workflow must grant the following GitHub permissions to the `_sonar.yml` workflow:

| Permission      | Access  | Reason                                     |
| --------------- | ------- | ------------------------------------------ |
| `contents`      | `read`  | Check out the repository                   |
| `id-token`      | `write` | Authenticate with Azure via OIDC           |
| `pull-requests` | `write` | Post Sonar analysis results as PR comments |

## Features

- Supports three scanner configurations: `default` (sonarqube-scan-action), `maven`, and `dotnet`
- Automatically sets the PR key for pull request analysis
- Configurable source, test, and exclusion paths

## Special Considerations

- For `dotnet` config: installs `dotnet-sonarscanner` and runs a full `dotnet build` as part of analysis
- For `maven` config: runs `mvn clean install sonar:sonar`
- For `default` config: uses [`sonarsource/sonarqube-scan-action`](https://github.com/sonarsource/sonarqube-scan-action)

## Troubleshooting

| Symptom                            | Likely cause                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Workflow fails at secret retrieval | Azure credentials are missing or the calling workflow did not pass the required secrets               |
| Sonar analysis not tied to PR      | Ensure the workflow is triggered by `pull_request` so the PR key is populated                         |
| `dotnet build` fails               | The repository requires additional setup steps before the scan; add them before calling this workflow |
