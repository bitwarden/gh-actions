# Docker Workflow Templates for Service Images

These workflow templates can be copied and modified as necessary to support building docker images that are published as a service.
It is expected that these are incomplete as they contain distilled functionality which should be customized as needed

## General Flow
1. CI - Build images
2. CD - Deploy service to k8s

## Templates

### _docker.yml

This is a callable workflow that will build a docker image and push according to the provided inputs.

---

### ci.yml

This workflow builds the docker image and contains the triggers for when the docker image is built and if it's pushed.
This should be customized to meet the needs of the specific repository

---

### cd.yml

This workflow calls the devops repository's `deploy-k8s-service.yml` to deploy the service via GitOps.
This should be customized to meet the needs of the specific repository
