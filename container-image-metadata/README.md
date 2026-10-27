# Container Image Metadata

Generates OCI container image labels and annotations from a standard Bitwarden label set by wrapping [`docker/metadata-action`](https://github.com/docker/metadata-action). The same label block is used for both labels and annotations.

The action only produces metadata. Tags, building, registry login and signing remain the caller's steps. `images`, `tags` and `flavor` are passed through unchanged for callers that also want tags generated.

## Usage

```yaml
- name: Generate image metadata
  id: metadata
  uses: bitwarden/gh-actions/container-image-metadata@main
  with:
    title: api
    version: ${{ steps.version.outputs.version }}

- name: Build and push
  uses: docker/build-push-action@... # pinned
  with:
    tags: ${{ env._IMAGE_TAGS }}
    labels: ${{ steps.metadata.outputs.labels }}
    annotations: ${{ steps.metadata.outputs.annotations }}
```

See [EXAMPLES.md](EXAMPLES.md) for more ways to use this action.

## Inputs

| Input                  | Required | Default                     | Description                                                                                                                                          |
| ---------------------- | -------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`                | Yes      |                             | `org.opencontainers.image.title`                                                                                                                     |
| `version`              | No       | derived from tags           | `org.opencontainers.image.version`                                                                                                                   |
| `revision`             | No       | PR head SHA or `github.sha` | `org.opencontainers.image.revision`                                                                                                                  |
| `vendor`               | No       | `Bitwarden Inc.`            | `org.opencontainers.image.vendor`                                                                                                                    |
| `url`                  | No       | `https://bitwarden.com`     | `org.opencontainers.image.url`                                                                                                                       |
| `description`          | No       | auto-detected               | `org.opencontainers.image.description`                                                                                                               |
| `licenses`             | No       | auto-detected               | `org.opencontainers.image.licenses` (SPDX expression)                                                                                                |
| `source`               | No       | auto-detected               | `org.opencontainers.image.source`                                                                                                                    |
| `extra-labels`         | No       | `""`                        | Additional `key=value` labels, one per line                                                                                                          |
| `include-ci-run-label` | No       | `false`                     | Adds `com.bitwarden.ci.run` with a link to the workflow run                                                                                          |
| `annotation-levels`    | No       | `manifest`                  | Comma-separated annotation levels. Use `index,manifest` when the build publishes an image index (multi-platform, or provenance attestations enabled) |
| `images`               | No       | `""`                        | Passed through to `docker/metadata-action`                                                                                                           |
| `tags`                 | No       | `""`                        | Passed through to `docker/metadata-action`                                                                                                           |
| `flavor`               | No       | `""`                        | Passed through to `docker/metadata-action`                                                                                                           |

"Auto-detected" means `docker/metadata-action` fills the field from the repository running the workflow. Cross-repository builds should set `description`, `licenses` and `source` explicitly.

"Derived from tags" means `docker/metadata-action` uses the primary tag version from the `tags` rules (or its default rules when `tags` is empty), e.g. `pr-123` or `main`. Set `version` explicitly when the image has a release version that differs from its tags. If no tag rule produces a version, the label is emitted with an empty value.

## Outputs

| Output        | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| `labels`      | Generated labels, one `key=value` per line                            |
| `annotations` | The same labels prefixed with each annotation level, e.g. `manifest:` |
| `tags`        | Generated tags. Bare tag names (e.g. `pr-123`) unless `images` is set |
| `json`        | All generated metadata as JSON                                        |

## Validation

The action fails when:

- `title` is empty
- a single-value input contains a line break
- an `extra-labels` line is not `key=value`, or its key does not match `^[A-Za-z0-9][A-Za-z0-9._-]*$`
- a label key appears twice, including an `extra-labels` key that repeats a standard one
- `include-ci-run-label` is not `true` or `false`
- `annotation-levels` is blank
