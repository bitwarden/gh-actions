# Setup Aikido Endpoint Protection

Installs [Aikido Endpoint Protection](https://help.aikido.dev/aikido-device-protection/deploying-aikido-endpoint/device-protection-mdm-guides/linux/device-protection-in-github-actions) on a GitHub-hosted Linux runner so package manager downloads in later steps are checked against the organization's Aikido policy.

Aikido's documented setup pipes an install script from their `main` branch into `sudo sh`. This action skips that script. It downloads the agent `.deb` from a pinned [`AikidoSec/safechain-internals`](https://github.com/AikidoSec/safechain-internals/releases) release, verifies it against a pinned SHA-256, and installs it in container mode.

## Usage

Run it before any step that installs packages.

```yaml
- name: Set up Aikido Endpoint Protection
  uses: bitwarden/gh-actions/setup-aikido-endpoint-protection@main
  with:
    token: ${{ secrets.AIKIDO_TOKEN }}

- name: Install Node dependencies
  run: npm ci
```

## Behavior

- The agent's proxy and CA settings are exported through `$GITHUB_ENV`, so every later step in the job (including `uses:` steps) sends its traffic through the agent. There is no need to source `/etc/profile.d/aikido-*.sh` yourself.
- The action fails the job unless Aikido returns a 403 for its `safe-chain-test` package, so a broken install can't silently leave the job unprotected.
- On fork pull requests the token is empty because forks can't read secrets. The action logs a warning and skips. An empty token in any other context fails the job.
- Only Linux X64 runners are supported.
- `npm ci` inside a `docker build` is not covered, because BuildKit doesn't use the runner's proxy or CA.

## Updating

Renovate tracks `AikidoSec/safechain-internals` releases and updates `_AIKIDO_ENDPOINT_VERSION` and `_AIKIDO_ENDPOINT_SHA256` together. Before approving the PR, confirm the new hash matches both of these:

- the `digest` GitHub reports for `EndpointProtection-amd64.deb` (`gh release view <tag> -R AikidoSec/safechain-internals --json assets`)
- `SHA256_AMD64_DEB` in Aikido's [`install-endpoint-linux.sh`](https://github.com/AikidoSec/safe-chain/blob/main/install-scripts/install-endpoint-linux.sh)
