import sys
import argparse
import os
import yaml
import json
import urllib3 as urllib


def workflow_files(input: str) -> list:
    """
    Takes in an argument of directory and/or files in string format from the CLI.
    Returns a sorted set of all workflow files in the path(s) specified.
    """
    workflow_files = []
    for path in input.split():
        if os.path.isfile(path):
            workflow_files.append(path)
        elif os.path.isdir(path):
            for subdir, dirs, files in os.walk(path):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    if filepath.endswith((".yml", ".yaml")):
                        workflow_files.append(filepath)

    return sorted(set(workflow_files))


def get_action_update(action_id):
    """
    Takes in an action id (bitwarden/gh-actions/version-bump@03ad9a873c39cdc95dd8d77dbbda67f84db43945)
    and checks the action repo for the newest version.
    If there is a new version, return the url to the updated version.
    """
    try:
        if "." in action_id:
            # Handle local workflow calls, return None since there will be no updates.
            return None

        path, *hash = action_id.split("@")
        http = urllib.PoolManager()
        headers = {"user-agent": "bw-linter"}

        if os.getenv("GITHUB_TOKEN", None):
            headers["Authorization"] = f"Token {os.environ['GITHUB_TOKEN']}"

        if "bitwarden" in path:
            path_list = path.split("/", 2)
            url = f"https://api.github.com/repos/{path_list[0]}/{path_list[1]}/commits?path={path_list[2]}"
            r = http.request("GET", url, headers=headers)
            sha = json.loads(r.data)[0]["sha"]
            if sha not in hash:
                return f"https://github.com/{path_list[0]}/{path_list[1]}/commit/{sha}"
        else:
            # Get tag from latest release
            r = http.request(
                "GET",
                f"https://api.github.com/repos/{path}/releases/latest",
                headers=headers,
            )

            tag_name = json.loads(r.data)["tag_name"]

            # Get the URL to the commit for the tag
            r = http.request(
                "GET",
                f"https://api.github.com/repos/{path}/git/ref/tags/{tag_name}",
                headers=headers,
            )
            if json.loads(r.data)["object"]["type"] == "commit":
                sha = json.loads(r.data)["object"]["sha"]
            else:
                url = json.loads(r.data)["object"]["url"]
                # Follow the URL and get the commit sha for tags
                r = http.request("GET", url, headers=headers)
                sha = json.loads(r.data)["object"]["sha"]

            if sha not in hash:
                return f"https://github.com/{path}/commit/{sha}"
    except:
        print(f"! Error trying to find latest version of action: {action_id}")
        return None


def lint(filename):

    findings = []

    with open(filename) as file:
        workflow = yaml.load(file, Loader=yaml.FullLoader)

        # Check for 'name' key for the workflow.
        if "name" not in workflow:
            findings.append("- Name key missing for workflow.")
        # Check for 'name' value to be capitalized in workflow.
        elif not workflow["name"][0].isupper():
            findings.append(
                f"- Name value for workflow is not capitalized. [{workflow['name']}]"
            )

        # Loop through jobs in workflow.
        if "jobs" in workflow:
            jobs = workflow["jobs"]
            for job_key in jobs:
                job = jobs[job_key]

                # Make sure runner is using pinned version.
                runner = job.get("runs-on", "")
                if "-latest" in runner:
                    findings.append(
                        f"- Runner version is set to '{runner}', but needs to be pinned to a version."
                    )

                # Check for 'name' key for job.
                if "name" not in job:
                    findings.append(f"- Name key missing for job key '{job_key}'.")
                # Check for 'name' value to be capitalized in job.
                elif not job["name"][0].isupper():
                    findings.append(
                        f"- Name value of job key '{job_key}' is not capitalized. [{job['name']}]"
                    )

                # If the job has environment variables defined, then make sure they start with an underscore.
                if "env" in job:
                    for k in job["env"].keys():
                        if k[0] != "_":
                            findings.append(
                                f"- Environment variable '{k}' of job key '{job_key}' does not start with an underscore."
                            )

                # Loop through steps in job.
                steps = job.get("steps", "")
                for i, step in enumerate(steps, start=1):
                    # Check for 'name' key for step.
                    if "name" not in step:
                        findings.append(
                            f"- Name key missing for step {str(i)} of job key '{job_key}'."
                        )
                    # Check for 'name' value to be capitalized in step.
                    elif not step["name"][0].isupper():
                        findings.append(
                            f"- Name value in step {str(i)} of job key '{job_key}' is not capitalized. [{step['name']}]"
                        )

                    if "uses" in step:

                        # If the step has a 'uses' key, check value hash.
                        try:
                            _, hash = step["uses"].split("@")

                            # Check to make sure SHA1 hash is 40 characters.
                            if len(hash) != 40:
                                findings.append(
                                    f"- Step {str(i)} of job key '{job_key}' does not have a valid action hash. (not 40 characters)"
                                )

                            # Attempts to convert the hash to a integer
                            # which will succeed if all characters are hexadecimal
                            try:
                                int(hash, 16)
                            except ValueError:
                                findings.append(
                                    f"- Step {str(i)} of job key '{job_key}' does not have a valid action hash. (not all hexadecimal characters)"
                                )
                        except:
                            findings.append(
                                f"- Step {str(i)} of job key '{job_key}' does not have a valid action hash. (missing '@' character)"
                            )

                        # If the step has a 'uses' key, check the action id repo for an update.
                        update_available = get_action_update(step["uses"])
                        if update_available:
                            findings.append(
                                f"- Step {str(i)} of job key '{job_key}' uses an outdated action, consider updating it '{update_available}'."
                            )

                    # If the step has a 'run' key and only has one command, check if it's a single line.
                    if "run" in step:
                        if step["run"].count("\n") == 1:
                            findings.append(
                                f"- Run in step {str(i)} of job key '{job_key}' should be a single line."
                            )

    if len(findings) > 0:
        print("#", filename)
        for finding in findings:
            print(finding)
        print()


def main(input_args=None):

    # Pull the arguments from the command line
    if not input_args:
        input_args = sys.argv[1:]

    # Read arguments from command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file or directory input")
    args = parser.parse_args(input_args)

    # Get all the workflow files.
    input_files = workflow_files(args.input)

    # If there are files to lint, lint each file.
    if len(input_files) > 0:
        for filename in input_files:
            lint(filename)
    else:
        print(f'File(s)/Directory: "{args.input}"  does not exist, exiting.')

if __name__ == "__main__":
    main()
