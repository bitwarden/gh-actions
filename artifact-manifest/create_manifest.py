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
    # the GH API uses pagination.
    # it returns 'rel="next"', followed by a page URL, in the link header if there's another page of results.
    # keep looping until we've processed all pages.
    while url:
        req = Request(url, headers=headers)
        try:
            with urlopen(req) as resp:
                data = json.loads(resp.read())
                link_header = resp.headers.get("Link", "")
        except HTTPError as e:
            print(f"::error::GitHub API error: {e.code} {e.reason}", file=sys.stderr)
            sys.exit(1)
        artifacts.extend(data["artifacts"])
        url = None
        for part in link_header.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
    return artifacts


def main():
    run_id = os.environ["_RUN_ID"]
    repository = os.environ["_REPOSITORY"]
    sha = os.environ["_SHA"]
    ref = os.environ["_REF"]
    workflow = os.environ["_WORKFLOW"]
    actor = os.environ["_ACTOR"]
    gha_artifacts_input = os.environ.get("_GHA_ARTIFACTS", "").strip()
    additional_artifacts_raw = os.environ.get("_ADDITIONAL_ARTIFACTS", "{}").strip() or "{}"

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
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("::error::GITHUB_TOKEN environment variable is required when using gha_artifacts.", file=sys.stderr)
            sys.exit(1)
        all_artifacts = get_run_artifacts(token, repository, run_id)

        if gha_artifacts_input == "*":
            selected = [a for a in all_artifacts if a["name"] != "artifact-manifest"]
        else:
            requested = {name.strip() for name in gha_artifacts_input.splitlines() if name.strip()}
            selected = [a for a in all_artifacts if a["name"] in requested]
            missing = requested - {a["name"] for a in selected}
            if missing:
                print(f"::error::Requested GHA artifacts not found in this run: {', '.join(sorted(missing))}", file=sys.stderr)
                sys.exit(1)

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

    if not isinstance(additional, dict):
        print("::error::additional_artifacts must be a JSON object", file=sys.stderr)
        sys.exit(1)

    duplicates = manifest["artifacts"].keys() & additional.keys()
    if duplicates:
        print(f"::error::Duplicate artifact keys in additional_artifacts: {', '.join(sorted(duplicates))}", file=sys.stderr)
        sys.exit(1)

    manifest["artifacts"].update(additional)

    with open("artifact_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
