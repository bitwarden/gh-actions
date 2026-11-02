# Setup Aikido Endpoint Protection

Installs [Aikido Endpoint Protection](https://help.aikido.dev/aikido-device-protection/deploying-aikido-endpoint/device-protection-mdm-guides/linux/device-protection-in-github-actions) on a GitHub-hosted Linux runner so package manager downloads in later steps are checked against the organization's Aikido policy.

Aikido's documented setup pipes an install script from their `main` branch into `sudo sh`. This action skips that script. It downloads the agent `.deb` from a pinned [`AikidoSec/safechain-internals`](https://github.com/AikidoSec/safechain-internals/releases) release, verifies it against a pinned SHA-256, and installs it in container mode.

## Usage

Run it before any step that installs packages. The action reads the `AIKIDO-ENDPOINT-TOKEN` enrollment token from Azure Key Vault (`gh-org-bitwarden` by default), so the job needs `id-token: write`.

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - name: Set up Node
    uses: actions/setup-node@<sha> # vX.Y.Z
    with:
      node-version: '24'
      # No `cache: "npm"`. See Behavior.

  - name: Set up Aikido Endpoint Protection
    uses: bitwarden/gh-actions/setup-aikido-endpoint-protection@main
    with:
      azure-subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
      azure-tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      azure-client-id: ${{ secrets.AZURE_CLIENT_ID }}

  - name: Install Node dependencies
    run: npm ci
```

## Behavior

- The agent's proxy and CA settings are exported through `$GITHUB_ENV`, so every later step in the job (including `uses:` steps) sends its traffic through the agent. There is no need to source `/etc/profile.d/aikido-*.sh` yourself.
- The action fails the job unless Aikido returns a 403 for its `safe-chain-test` package, so a broken install can't silently leave the job unprotected.
- A package manager cache restored before installs (for example `actions/setup-node` with `cache: "npm"`) bypasses Aikido, because cached packages are installed from disk without going through the proxy. Don't enable package manager caching in jobs that rely on this action.
- On fork pull requests the Azure inputs are empty because forks can't read secrets. The action logs a warning and skips. Empty Azure inputs in any other context fail the job.
- Only Linux X64 runners are supported.
- `npm ci` inside a `docker build` is not covered, because BuildKit doesn't use the runner's proxy or CA.

## Updating

Renovate tracks `AikidoSec/safechain-internals` releases and updates `_AIKIDO_ENDPOINT_VERSION` and `_AIKIDO_ENDPOINT_SHA256` together. Before approving the PR, confirm the new hash matches both of these:

- the `digest` GitHub reports for `EndpointProtection-amd64.deb` (`gh release view <tag> -R AikidoSec/safechain-internals --json assets`)
- `SHA256_AMD64_DEB` in Aikido's [`install-endpoint-linux.sh`](https://github.com/AikidoSec/safe-chain/blob/main/install-scripts/install-endpoint-linux.sh)
