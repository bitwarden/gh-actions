# Composite Action for logging into Azure

This action provides a centralized way to login to Azure.

## Inputs

- Required
    - subscription_id
        - Description: Provides the Azure subscription ID.
        - Example:
            ```
                subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
            ```
    - tenant_id
        - Description: Provides the Azure tenant ID.
        - Example:
            ```
                tenant_id: ${{ secrets.AZURE_TENANT_ID }}
            ```
    - client_id
        - Description: Provides the Azure client ID.
        - Example:
            ```
                client_id: ${{ secrets.AZURE_CLIENT_ID }}
            ```

## Examples
### Step Snippet
```
      - name: Azure Login
        uses: bitwarden/gh-actions/azure-login@main
        with:
          subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          client_id: ${{ secrets.AZURE_CLIENT_ID }}
```

### Workflow
#### Repository without environment specific secrets
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
      - name: Azure Login
        uses: bitwarden/gh-actions/azure-login@main
        with:
          subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          client_id: ${{ secrets.AZURE_CLIENT_ID }}

      - name: Get KV Secrets
        id: get-kv-secrets
        uses: bitwarden/gh-actions/get-keyvault-secrets@main
        with:
          keyvault: gh-example-repository
          secrets: "example-secret-1,example-secret-2"

      - name: Azure Logout
        uses: bitwarden/gh-actions/azure-logout@main

      - name: Use Secrets
        shell: bash
        run: |
           # Use ${{ steps.get-kv-secrets.output.example-secret-1}} in some way
```

#### Repository with environment specific secrets
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
    environment: Development # This will be used during login to authenticate
    steps:
      - name: Azure Login
        uses: bitwarden/gh-actions/get-secrets@main
        with:
          subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          client_id: ${{ secrets.AZURE_CLIENT_ID }}

      - name: Get KV Secrets
        id: get-kv-secrets
        uses: bitwarden/gh-actions/get-keyvault-secrets@main
        with:
          keyvault: gh-example-repository
          secrets: "example-secret-1,example-secret-2"

      - name: Azure Logout
        uses: bitwarden/gh-actions/azure-logout@main

      - name: Use Secrets
        shell: bash
        run: |
           # Use ${{ steps.get-kv-secrets.output.example-secret-1}} in some way
```
