Reusable workflow that runs Checkmarx SAST (Static Application Security Testing) scans on your repository. It authenticates via Azure Key Vault to retrieve Checkmarx credentials, performs the scan, and optionally uploads SARIF results to GitHub's code scanning dashboard.

## Key Features

* **Incremental scanning**: Automatically performs incremental scans on pull requests for faster feedback, with full scans on other events.
* **SARIF integration**: Uploads scan results to GitHub's Security tab via the code scanning API.
* **Azure Key Vault authentication**: Securely retrieves Checkmarx credentials from Azure Key Vault using OIDC-based login.
* **Concurrency control**: Cancels redundant in-progress scans when new commits are pushed to the same branch or PR.

## How To Use It

### Setup

1. Ensure your repository has access to the required Azure secrets (`AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`) for OIDC-based login.
2. Verify that the Azure Key Vault `gh-org-bitwarden` contains the secrets `CHECKMARX-TENANT`, `CHECKMARX-CLIENT-ID`, and `CHECKMARX-SECRET`.

### Usage

See [checkmarx.yml](./checkmarx.yml) template for a calling workflow.

```yaml
jobs:
  sast:
    uses: bitwarden/gh-actions/.github/workflows/_checkmarx.yml@main
    with:
      incremental: true    # optional, defaults to true on pull_request events
      upload-sarif: true   # optional, defaults to true
    secrets:
      AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
```

### Inputs

| Name           | Type    | Default                                              | Description                       |
| -------------- | ------- | ---------------------------------------------------- | --------------------------------- |
| `incremental`  | boolean | `true` on `pull_request` events, `false` otherwise   | Perform an incremental SAST scan  |
| `upload-sarif` | boolean | `true`                                               | Upload SARIF results to GitHub    |

### Secrets

| Name                    | Required | Description                          |
| ----------------------- | -------- | ------------------------------------ |
| `AZURE_SUBSCRIPTION_ID` | Yes      | Azure subscription ID for OIDC login |
| `AZURE_TENANT_ID`       | Yes      | Azure tenant ID for OIDC login       |
| `AZURE_CLIENT_ID`       | Yes      | Azure client ID for OIDC login       |

## Requirements

* Azure Key Vault must `gh-org-bitwarden` be accessible with the provided credentials.

### GitHub Permissions

| Permission        | Access | Reason                                |
| ----------------- | ------ | ------------------------------------- |
| `contents`        | read   | Check out repository source code      |
| `pull-requests`   | write  | Post scan comments on pull requests   |
| `security-events` | write  | Upload SARIF results to code scanning |
| `id-token`        | write  | OIDC authentication with Azure        |


## References

* [Checkmarx/ast-github-action](https://github.com/Checkmarx/ast-github-action)
* [Bitwarden - Application Security - Scan Management](https://bitwarden.atlassian.net/wiki/x/AYDIPw)
