#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError


def get_run_artifacts(token, repository, run_id):
    url = f"https://api.github.com/repos/{repository}/actions/runs/{run_id}/artifacts?per_page=100"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    artifacts = []
    # keep looping as long as we have urls to call
    while url:
        # build the request object
        req = Request(url, headers=headers)
        try:
            # call the url
            with urlopen(req) as resp:
                data = json.loads(resp.read())
                # grab the "next page" link that GitHub includes in the response header
                link_header = resp.headers.get("Link", "")
        except HTTPError as e:
            print(f"::error::GitHub API error: {e.code} {e.reason}", file=sys.stderr)
            sys.exit(1)
        # combine the list of artifacts from the response with existing list of artifacts
        artifacts.extend(data["artifacts"])
        # set var to None. loop will exit if we don't find any "next page" links
        url = None
        # loop through all the links in the response header and capture any that are "next page" links
        for part in link_header.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return artifacts


def main():
    # get all the ENV vars
    token = os.environ["GH_TOKEN"]
    run_id = os.environ["_RUN_ID"]
    repository = os.environ["_REPOSITORY"]
    sha = os.environ["_SHA"]
    ref = os.environ["_REF"]
    workflow = os.environ["_WORKFLOW"]
    actor = os.environ["_ACTOR"]
    gha_artifacts_input = os.environ.get("_GHA_ARTIFACTS", "").strip()
    additional_artifacts_raw = os.environ.get("_ADDITIONAL_ARTIFACTS", "{}").strip() or "{}"

    # build the manifest skeleton
    manifest = {
        "manifest_version": "1",
        "run_id": run_id,
        "repository": repository,
        "sha": sha,
        "ref": ref,
        "workflow_name": workflow,
        "actor": actor,
        "manifest_build_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "artifacts": {},
    }

    if gha_artifacts_input:
        # grab all the artifacts from the given run
        all_artifacts = get_run_artifacts(token, repository, run_id)

        # if a wildcard is passed in, select all artifacts uploaded to the given run
        if gha_artifacts_input == "*":
            selected = [a for a in all_artifacts if a["name"] != "artifact-manifest"]
        else:
            # make a set of artifacts that were passed in as input
            requested = {name.strip() for name in gha_artifacts_input.splitlines() if name.strip()}
            # filter the full artifact list down to only the ones that were requested
            selected = [a for a in all_artifacts if a["name"] in requested]
            # find any requested artifacts that weren't present in the run
            missing = requested - {a["name"] for a in selected}
            if missing:
                print(f"::error::Requested GHA artifacts not found in this run: {', '.join(sorted(missing))}", file=sys.stderr)
                sys.exit(1)

        # loop through the list of artifacts and add them to the manifest JSON
        for artifact in selected:
            manifest["artifacts"][artifact["name"]] = {
                "type": "gha_artifact",
                "run_id": run_id,
                "name": artifact["name"],
                "checksum": artifact.get("digest", ""),
            }

    # merge any additional artifacts passed in with the GHA artifacts
    try:
        additional = json.loads(additional_artifacts_raw)
    except json.JSONDecodeError as e:
        print(f"::error::Failed to parse additional_artifacts: {e}", file=sys.stderr)
        sys.exit(1)

    manifest["artifacts"].update(additional)

    # write the manifest to a file
    with open("artifact_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
