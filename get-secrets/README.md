# Composite Action for getting secrets

This action provides a simple way to get secrets out of the supported secrets management systems.<br/>
Supported Secret Management Systems:
- Azure Key Vault

## Inputs

- secrets
    - Description: Provides the name of the secrets to retrieve.
    - Examples:
        ```
            secrets: secret-1
        ```
        ```
            secrets: |
            secret-1
            secret-2
        ```
- azure_subscription_id
    - Description: Provides the Azure subscription ID.
    - Example:
        ```
            azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        ```
- azure_tenant_id
    - Description: Provides the Azure tenant ID.
    - Example:
        ```
            azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
        ```
- azure_client_id
    - Description: Provides the Azure client ID.
    - Example:
        ```
            azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
        ```
- lookup_repo_client_id
    - Description: Specifies if the repository specific client ID should be looked up using the given client ID
        - This allows for using an org wide client ID to determine the repository specific client IDs
        - If specifying the client ID for the repository or getting secrets from an org wide id, set this to `"false"`.
    - Default: true

- keyvault_name
    - Description: Provides the key vault name where to retrieve secrets from
    - Default: "" (Will be determined using the calling repository's name)

- keyvault_environment
    - Description: Specifies the GitHub environment to use for determining the keyvault name.  Only used if `keyvault_name` is empty
    - Default: ""

### Workflow Usage Example
#### Azure Key Vault access
Repository without environment specific secrets
```
on:
  workflow_dispatch:
  push:
    branches:
      - "main"
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  example:
    name: Example Job
    runs-on: ubuntu-24.04
    steps:
      - name: Retrieve Secrets
        uses: bitwarden/gh-actions/get-secrets@main
        with:
          azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
          secrets: |
            secret-1
            secret-2
```

Repository with environment specific secrets
```
on:
  workflow_dispatch:
  push:
    branches:
      - "main"
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  example:
    name: Example Job
    runs-on: ubuntu-24.04
    environment: production
    steps:
      - name: Retrieve Secrets
        uses: bitwarden/gh-actions/get-secrets@main
        with:
          azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
          keyvault_environment: production
          secrets: |
            secret-1
            secret-2
```

Repository getting organization wide secrets or with a client ID that already specifies the repository specific client ID
```
on:
  workflow_dispatch:
  push:
    branches:
      - "main"
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  example:
    name: Example Job
    runs-on: ubuntu-24.04
    steps:
      - name: Retrieve Secrets
        uses: bitwarden/gh-actions/get-secrets@main
        with:
          azure_subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          azure_tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
          lookup_repo_client_id: "false"
          secrets: |
            secret-1
            secret-2
```
