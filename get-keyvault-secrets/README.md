# Get Key Vault Secrets Action

Fetches secrets from an Azure Key Vault instance and sets them as output variables.

Secrets are automatically masked in logs and available to subsequent steps via `${{ steps.<id>.outputs.<secret-name> }}`.

## Inputs

| Input      | Description                                      | Required |
| ---------- | ------------------------------------------------ | -------- |
| `keyvault` | Name of the Azure Key Vault                      | Yes      |
| `secrets`  | Comma-separated list of secret names to retrieve | Yes      |

## Outputs

Each secret is set as an output using its name as the key.

| Output          | Description                       |
| --------------- | --------------------------------- |
| `<secret-name>` | The value of the retrieved secret |

## Prerequisites

Authenticate with Azure using [`bitwarden/gh-actions/azure-login`](../azure-login) before using this action.

The Azure identity used must have `Get` permission on the Key Vault secrets.

## Example

```yaml
jobs:
  example:
    name: Example
    runs-on: ubuntu-24.04
    permissions:
      id-token: write
    steps:
      - name: Azure Login
        uses: bitwarden/gh-actions/azure-login@main
        with:
          subscription_id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          tenant_id: ${{ secrets.AZURE_TENANT_ID }}
          client_id: ${{ secrets.AZURE_CLIENT_ID }}

      - name: Get Key Vault Secrets
        id: get-secrets
        uses: bitwarden/gh-actions/get-keyvault-secrets@main
        with:
          keyvault: my-key-vault
          secrets: 'secret-one,secret-two'

      - name: Azure Logout
        uses: bitwarden/gh-actions/azure-logout@main

      - name: Use Secrets
        run: echo "Do something with ${{ steps.get-secrets.outputs.secret-one }}"
```

## Development

After making changes to `src/main.ts` or any dependencies, rebuild the bundle and commit the output:

```bash
npm install
npm run build
```

Commit the following files:

- `src/main.ts` — source changes
- `package.json` and `package-lock.json` — dependency changes
- `dist/index.js` — compiled bundle (required for the action to run)
- `dist/licenses.txt` — bundled dependency licenses
- `dist/package.json` — ESM module declaration
