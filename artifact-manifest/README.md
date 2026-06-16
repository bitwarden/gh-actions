# Artifact Manifest Action

## Description
The `artifact-manifest` action builds and uploads, or downloads and parses, a CI artifact manifest — a JSON inventory of all artifacts produced by a workflow run. It supports two modes: `upload` to collect and publish the manifest at the end of a build, and `download` to retrieve and parse it in a downstream workflow.

Use this action to create an auditable record of exactly what a run produced, pass artifact metadata between workflows, or support supply chain visibility for both GitHub Actions native artifacts and external artifacts like container images or release blobs.

## Key Features
- **Dual upload/download modes**: One action handles both publishing and consuming the manifest
- **Flexible artifact selection**: Include all GHA artifacts with `*`, or specify by name
- **External artifact support**: Merge non-GHA artifacts (container images, blobs, release assets) via `additional_artifacts`
- **Paginated API handling**: Correctly handles runs with more than 100 artifacts
- **No external dependencies**: Pure Python standard library — no pip installs required

## How to Use It

### Upload Mode
Add this step at the end of a build job, after all artifacts have been uploaded:

```yaml
- name: Upload artifact manifest
  uses: bitwarden/gh-actions/artifact-manifest@main
  env:
    GITHUB_TOKEN: ${{ github.token }}
  with:
    mode: upload
    gha_artifacts: |
      my-build-artifact
      my-test-results
    additional_artifacts: |
      {
        "my-container-image": {
          "type": "container_image",
          "image": "ghcr.io/myorg/myrepo",
          "tag": "1.2.3",
          "sha": "sha256:abc123..."
        }
      }
```

Inputs:
- `mode`: Set to `upload`
- `gha_artifacts`: Newline-separated list of GHA artifact names that have been uploaded to the current run to include. Use `*` to include all artifacts from the run (the manifest itself is always excluded). Omit to include none.
- `additional_artifacts`: JSON object of non-GHA artifact entries to merge into the manifest. Keys are logical artifact names; values are type-specific objects.

Environment:
- `GITHUB_TOKEN`: GitHub token used to query the run's artifact list. **Required.** Pass the default token via `env: GITHUB_TOKEN: ${{ github.token }}`, or use a GitHub App token for cross-repo access or elevated permissions.

### Download Mode
Reference the manifest in a downstream workflow using the run ID from the upstream run:

```yaml
- name: Download artifact manifest
  id: manifest
  uses: bitwarden/gh-actions/artifact-manifest@main
  env:
    GITHUB_TOKEN: ${{ github.token }}
  with:
    mode: download
    run_id: ${{ github.event.workflow_run.id }}

- name: Print raw manifest
  env:
    MANIFEST: ${{ steps.manifest.outputs.manifest }}
  run: echo "$MANIFEST"

- name: Print container image SHA manifest
  env:
    IMAGE_SHA: ${{ fromJSON(steps.manifest.outputs.manifest).artifacts.my-docker-image.sha }}
  run: echo "$IMAGE_SHA"
```

Inputs:
- `mode`: Set to `download`
- `run_id`: The workflow run ID to download the manifest from. Required.
- `repo`: The `owner/repo` to download from. Defaults to the current repository.

Environment:
- `GITHUB_TOKEN`: GitHub token with artifact read access. **Required.** Pass the default token via `env: GITHUB_TOKEN: ${{ github.token }}`, or use a GitHub App token for cross-repo downloads with `actions: read` permission on the target repository.

Outputs:
- `manifest`: The full manifest as a JSON string, accessible via `${{ steps.<step-id>.outputs.manifest }}`. Also available in upload mode.

- Individual values can be accessed using `fromJSON()`:

  ```yaml
  env:
    IMAGE_SHA: ${{ fromJSON(steps.<step-id>.outputs.manifest).artifacts.my-container-image.sha }}
  run: echo "$IMAGE_SHA"
  ```

### Using Custom Tokens

For cross-repo access or elevated permissions, use a GitHub App token passed via the `env` parameter:

```yaml
- name: Generate app token
  id: app-token
  uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0
  with:
    app-id: ${{ vars.APP_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}
    repositories: target-repo  # Optional: scope to specific repos

- name: Download manifest from another repo
  uses: bitwarden/gh-actions/artifact-manifest@main
  env:
    GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
  with:
    mode: download
    run_id: ${{ github.event.workflow_run.id }}
    repo: other-org/other-repo
```

### CI/CD Workflow Handoff Example

A common pattern is to have a CI workflow build and upload the manifest, then trigger a CD workflow that downloads and uses it:

**CI Workflow (build.yml):**
```yaml
name: Build
on:
  push:
    branches: [main]

permissions: {}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: read
    steps:
      - name: Checkout
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3

      # ... build steps that create artifacts ...

      - name: Upload artifact manifest
        uses: bitwarden/gh-actions/artifact-manifest@main
        env:
          GITHUB_TOKEN: ${{ github.token }}
        with:
          mode: upload
          gha_artifacts: |
            build-output
            test-results
          additional_artifacts: |
            {
              "app-image": {
                "type": "container_image",
                "registry": "ghcr.io",
                "image": "myorg/myapp",
                "tag": "${{ github.sha }}",
                "digest": "sha256:..."
              }
            }
```

**CD Workflow (deploy.yml):**
```yaml
name: Deploy
on:
  workflow_run:
    workflows: ["Build"]
    types: [completed]
    branches: [main]

permissions: {}

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3

      - name: Generate app token
        id: app-token
        uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1 # v3.2.0
        with:
          app-id: ${{ vars.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Download artifact manifest
        id: manifest
        uses: bitwarden/gh-actions/artifact-manifest@main
        env:
          GITHUB_TOKEN: ${{ steps.app-token.outputs.token }}
        with:
          mode: download
          run_id: ${{ github.event.workflow_run.id }}

      - name: Deploy using manifest data
        env:
          IMAGE_DIGEST: ${{ fromJSON(steps.manifest.outputs.manifest).artifacts.app-image.digest }}
          BUILD_SHA: ${{ fromJSON(steps.manifest.outputs.manifest).sha }}
        run: |
          echo "Deploying image: $IMAGE_DIGEST"
          echo "Built from commit: $BUILD_SHA"
          # ... deployment logic ...
```

## Manifest Schema

The action produces `artifact_manifest.json`. The schema is versioned via `manifest_version` and is intended to be a stable, machine-readable record of a workflow run's outputs.

### Top-level fields

| Field | Type | Description |
|---|---|---|
| `manifest_version` | string | Schema version. Currently `"1"`. |
| `run_id` | string | GitHub Actions workflow run ID. |
| `repository` | string | Repository in `owner/repo` format. |
| `sha` | string | Full commit SHA the workflow ran against. |
| `ref` | string | Branch or tag name (e.g. `main`, `rc`). |
| `workflow_name` | string | Name of the workflow that produced the manifest. |
| `actor` | string | GitHub user or app that triggered the run. |
| `manifest_build_time` | string | ISO 8601 UTC timestamp of when the manifest was built. |
| `artifacts` | object | Map of artifact name → artifact entry. See below. |

### Artifact entries

Each key in `artifacts` is the logical artifact name. The `type` field identifies the artifact kind; all other fields are type-specific.

#### `gha_artifact` — GitHub Actions native artifact

Populated automatically from the run when using `gha_artifacts`.

| Field | Type | Description |
|---|---|---|
| `type` | string | `"gha_artifact"` |
| `run_id` | string | Run ID the artifact was uploaded in. |
| `name` | string | Artifact name as uploaded via `actions/upload-artifact`. |
| `checksum` | string | Digest provided by GitHub, if available. Empty string otherwise. |

#### Custom types — non-GHA artifacts

Provided via `additional_artifacts`. The `type` field is required; all other fields are defined by the caller and passed through as-is. See **_How to use it_** section for an example of using `additional_artifacts`.

### Example

```json
{
  "manifest_version": "1",
  "run_id": "12345678",
  "repository": "myorg/myrepo",
  "sha": "abc123def456",
  "ref": "main",
  "workflow_name": "Build",
  "actor": "github-actions[bot]",
  "manifest_build_time": "2025-01-15T10:30:00Z",
  "artifacts": {
    "my-build-artifact": {
      "type": "gha_artifact",
      "run_id": "12345678",
      "name": "my-build-artifact",
      "checksum": "sha256:abc123..."
    },
    "my-container-image": {
      "type": "container_image",
      "image": "ghcr.io/myorg/myrepo",
      "tag": "1.2.3",
      "sha": "sha256:123abc..."
    }
  }
}
```

## Requirements
- Python 3.6 or later must be available on the runner (present by default on GitHub-hosted runners)
- For `upload` mode, the GitHub token must have `actions: read` permission to query the run artifacts from the GitHub API
- The `gh` CLI must be available on the runner for download mode (present by default on GitHub-hosted runners)
- In `download` mode, for cross-repo downloads, pass a custom token with `actions: read` on the target repository via `env: GITHUB_TOKEN` — the default `GITHUB_TOKEN` is scoped to the current repository only

## Troubleshooting

### "Requested GHA artifacts not found in this run" error
- Verify the artifact name in `gha_artifacts` exactly matches the `name` field used in `actions/upload-artifact`
- Names are case-sensitive
- Ensure the upload step ran before the manifest step in the same workflow run
- Use `*` to include all artifacts and inspect the manifest to confirm available names

### "Failed to parse additional_artifacts" error
- The `additional_artifacts` input must be valid JSON
- Validate your JSON using a linter before passing it to the action
- Multiline YAML block scalars (`|`) can introduce unexpected indentation — use a single-line string or a `fromJSON` expression if constructing the value dynamically

### "Run ID is required for `download` mode" error
- The `run_id` input is required when `mode` is `download`
- In `workflow_run`-triggered workflows, use `${{ github.event.workflow_run.id }}`
- In manually triggered or other contexts, pass the run ID explicitly

### Artifact not found during download
- Confirm the upstream run completed successfully and the manifest was uploaded
- Verify `repo` points to the correct repository if downloading cross-repo
- The artifact is uploaded under the name `artifact-manifest` — it must not have been deleted or expired
