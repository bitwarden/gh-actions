import argparse
import os
import yaml


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

                # Check for 'name' key for job.
                if "name" not in job:
                    findings.append(f"- Name key missing for job key '{job_key}'.")
                # Check for 'name' value to be capitallized in job.
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
                steps = job["steps"]
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

                    # If the step has a 'uses' key, check value hash.
                    if "uses" in step:
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

    if len(findings) > 0:
        print("#", filename)
        for finding in findings:
            print(finding)
        print()


def main():

    # Read arguments from command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="file or directory input")
    args = parser.parse_args()

    # Set up list for files to lint.
    input_files = []

    # Check if argument is file, then append to input files.
    if os.path.isfile(args.input):
        input_files.append(args.input)
    # Check if argument is directory, then recursively add all *.yml and *.yaml files to input files.
    elif os.path.isdir(args.input):
        for subdir, dirs, files in os.walk(args.input):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.endswith(".yml") or filepath.endswith(".yaml"):
                    input_files.append(filepath)
    else:
        print("File/Directory does not exist, exiting.")

    for filename in input_files:
        lint(filename)


if __name__ == "__main__":
    main()
