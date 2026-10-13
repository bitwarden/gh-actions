# Examples

The action's outputs feed `docker/build-push-action`:

```yaml
- name: Build and push image
  uses: docker/build-push-action@... # pinned
  with:
    labels: ${{ steps.metadata.outputs.labels }}
    annotations: ${{ steps.metadata.outputs.annotations }}
```

The examples below set `annotation-levels: index,manifest` because they assume the build publishes an image index (multi-platform, or provenance attestations enabled). Leave it at the default `manifest` for single-platform builds without provenance.

## Single project with a project label

`revision`, `vendor` and `url` use the action defaults. `source`, `description` and `licenses` are auto-detected from the repository.

```yaml
- name: Generate image metadata
  id: metadata
  uses: bitwarden/gh-actions/container-image-metadata@main
  with:
    title: Bitwarden Example Service
    version: ${{ steps.version.outputs.version }}
    annotation-levels: index,manifest
    extra-labels: |
      com.bitwarden.project=example-service
```

## Matrix of services

Title, description and project label come from the matrix entry, so one step serves every image.

```yaml
- name: Generate image metadata
  id: metadata
  uses: bitwarden/gh-actions/container-image-metadata@main
  with:
    title: Bitwarden ${{ matrix.project_name }}
    version: ${{ steps.version.outputs.version }}
    description: ${{ matrix.description || 'Bitwarden service' }}
    annotation-levels: index,manifest
    extra-labels: |
      com.bitwarden.project=${{ matrix.project_name }}
```

## Product-specific URL

Overrides the default `url` for an image that belongs to a specific product page.

```yaml
- name: Generate image metadata
  id: metadata
  uses: bitwarden/gh-actions/container-image-metadata@main
  with:
    title: Bitwarden ${{ matrix.title }}
    version: ${{ steps.version.outputs.version }}
    description: ${{ matrix.description }}
    url: https://bitwarden.com/products/example
    annotation-levels: index,manifest
```

## Bundled image with component labels

`revision` is the commit actually checked out, `source` is set explicitly, and `extra-labels` records which component images went into the bundle.

```yaml
- name: Resolve built revision
  id: revision
  run: echo "sha=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"

- name: Generate image metadata
  id: metadata
  uses: bitwarden/gh-actions/container-image-metadata@main
  with:
    title: Bitwarden Bundle
    version: ${{ steps.version.outputs.version }}
    revision: ${{ steps.revision.outputs.sha }}
    description: All-in-one Bitwarden container
    source: https://github.com/${{ github.repository }}
    annotation-levels: index,manifest
    extra-labels: |
      com.bitwarden.server.image=${{ steps.components.outputs.server_image }}
      com.bitwarden.server.tag=${{ steps.components.outputs.server_tag }}
      com.bitwarden.web.image=${{ steps.components.outputs.web_image }}
      com.bitwarden.web.tag=${{ steps.components.outputs.web_tag }}
```
