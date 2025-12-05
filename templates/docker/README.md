# Docker Workflow Templates

These workflow templates can be copied and modified as necessary to support building, releasing, and publishing docker images.

## General Flow
1. Build and Push
2. Release
3. Publish

## Templates

### Build and Push
There are currently 2 versions of this template:
- `build_push_acr.yml`
- `build_push_ghcr.yml`

These can be combined if necessary for pushing to both ACR and GHCR.

Purpose: These build the docker image and push it out to registries if tags are set to be pushed (See below)

Tags that are pushed:
- On push to main: `dev`
- On PR: `pr-#`

---

### Release
The `release.yml` workflow handles release both ACR and GHCR.
It can be modified to adjust to only doing one by removing the respective job.

This will do 2 things:
1. Create a GitHub Release
2. Publish the `dev` tag as the release version tag in ACR and GHCR

Tags that are pushed:
- Release version tag

---

### Publish
The `publish.yml` workflow handles publishing both ACR and GHCR.
It can be modified to adjust to only doing one by removing the respective job

This will copy the tag corresponding to the latest release to the `latest` tag

Tags that are pushed:
- `latest`
