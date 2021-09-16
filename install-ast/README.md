# Install Azure Sign Tool (AST)

We use an EV SSL cert on an HSM in an Azure Key Vault to sign our Windows executables that we distribute outside of the
Windows Store. We use the [AzureSignTool](https://github.com/vcsjones/AzureSignTool) to do this. Since it is a pretty
involved process to install, needs a pinned commit version, and is in multiple projects, a composite action is the best
way of keeping uniformity in our actions.

See the [AzureSignTool README](https://github.com/vcsjones/AzureSignTool) or our [Desktop sign.js](https://github.com/bitwarden/desktop/blob/hotfix/pinning-ast-version/sign.js)
for usage examples.

## Requirements
- Windows OS
