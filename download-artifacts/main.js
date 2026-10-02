const core = require('@actions/core')
const github = require('@actions/github')
const artifact = require('@actions/artifact')
const AdmZip = require('adm-zip')
const filesize = require('filesize')
const pathname = require('path')
const fs = require('fs')

// How many pages of 100 unfiltered runs to check for a newer run the filtered run search missed.
const UNFILTERED_PAGE_LIMIT = 20

async function downloadAction(name, path) {
    const artifactClient = new artifact.DefaultArtifactClient()

    // v6 API: first get artifact by name to retrieve its ID
    const { artifact: found } = await artifactClient.getArtifact(name)

    // Then download using the artifact ID
    await artifactClient.downloadArtifact(found.id, {
        path: path
    })

    core.setOutput("found_artifact", true)
}

async function main() {
    try {
        const token = core.getInput("github_token", { required: true })
        const [owner, repo] = core.getInput("repo", { required: true }).split("/")
        const path = core.getInput("path", { required: true })
        const names = core.getInput("artifacts") ? core.getInput("artifacts") : "*"
        const nameIsRegExp = core.getBooleanInput("name_is_regexp")
        const skipUnpack = core.getBooleanInput("skip_unpack")
        const ifNoArtifactFound = core.getInput("if_no_artifact_found")
        let workflow = core.getInput("workflow")
        let workflowConclusion = core.getInput("workflow_conclusion")
        let pr = core.getInput("pr")
        let commit = core.getInput("commit")
        let branch = core.getInput("branch")
        let event = core.getInput("event")
        let runID = core.getInput("run_id")
        let runNumber = core.getInput("run_number")
        let checkArtifacts = core.getBooleanInput("check_artifacts")
        let searchArtifacts = core.getBooleanInput("search_artifacts")
        const allowForks = core.getBooleanInput("allow_forks")
        const requireBranchHead = core.getBooleanInput("require_branch_head")
        let dryRun = core.getInput("dry_run")

        const client = github.getOctokit(token)

        core.info(`==> Repository: ${owner}/${repo}`)
        core.info(`==> Artifact name(s): ${names}`)
        core.info(`==> Local path: ${path}`)

        if (!workflow) {
            const run = await client.rest.actions.getWorkflowRun({
                owner: owner,
                repo: repo,
                run_id: runID || github.context.runId,
            })
            workflow = run.data.workflow_id
        }

        core.info(`==> Workflow name: ${workflow}`)
        core.info(`==> Workflow conclusion: ${workflowConclusion}`)

        const uniqueInputSets = [
            {
                "pr": pr,
                "commit": commit,
                "branch": branch,
                "run_id": runID
            }
        ]
        uniqueInputSets.forEach((inputSet) => {
            const inputs = Object.values(inputSet)
            const providedInputs = inputs.filter(input => input !== '')
            if (providedInputs.length > 1) {
                throw new Error(`The following inputs cannot be used together: ${Object.keys(inputSet).join(", ")}`)
            }
        })

        if (pr) {
            core.info(`==> PR: ${pr}`)
            const pull = await client.rest.pulls.get({
                owner: owner,
                repo: repo,
                pull_number: pr,
            })
            commit = pull.data.head.sha
            //branch = pull.data.head.ref
        }

        if (commit) {
            core.info(`==> Commit: ${commit}`)
        }

        if (branch) {
            branch = branch.replace(/^refs\/heads\//, "")
            core.info(`==> Branch: ${branch}`)
        }

        if (event) {
            core.info(`==> Event: ${event}`)
        }

        if (runNumber) {
            core.info(`==> Run number: ${runNumber}`)
        }

        core.info(`==> Allow forks: ${allowForks}`)

        if (requireBranchHead && !branch) {
            throw new Error("require_branch_head needs branch to be set")
        }

        if (!runID) {
            const isWantedRun = async (run) => {
                if (runNumber && run.run_number != runNumber) {
                    return false
                }
                if (workflowConclusion && (workflowConclusion != run.conclusion && workflowConclusion != run.status)) {
                    return false
                }
                if (!allowForks && run.head_repository.full_name !== `${owner}/${repo}`) {
                    core.info(`==> Skipping run from fork: ${run.head_repository.full_name}`)
                    return false
                }
                // A branch HEAD request wants a build of the branch itself, not a pull request build that shares its commit.
                // Pull request builds are requested with `pr`.
                if (requireBranchHead && run.event === "pull_request") {
                    core.info(`==> Skipping pull request run: ${run.id}`)
                    return false
                }
                if (checkArtifacts || searchArtifacts) {
                    let artifacts = await client.paginate(client.rest.actions.listWorkflowRunArtifacts, {
                        owner: owner,
                        repo: repo,
                        run_id: run.id,
                    })
                    if (!artifacts || artifacts.length == 0) {
                        return false
                    }
                    if (searchArtifacts) {
                        const artifact = artifacts.find((artifact) => {
                            if (nameIsRegExp) {
                                return artifact.name.match(name) !== null
                            }
                            return artifact.name == name
                        })
                        if (!artifact) {
                            return false
                        }
                    }
                }
                return true
            }

            let foundRun
            for await (const runs of client.paginate.iterator(client.rest.actions.listWorkflowRuns, {
                owner: owner,
                repo: repo,
                workflow_id: workflow,
                ...(branch ? { branch } : {}),
                ...(event ? { event } : {}),
                ...(commit ? { head_sha: commit } : {}),
            }
            )) {
                // Run IDs increase over time, so sorting by ID puts the newest run first without trusting the API order.
                for (const run of runs.data.sort((a, b) => b.id - a.id)) {
                    if (!(await isWantedRun(run))) {
                        continue
                    }
                    foundRun = run
                    break
                }
                if (foundRun) {
                    break
                }
            }

            // GitHub serves branch, event and head_sha filtered run queries from a search index that can leave runs
            // out with no sign anything is missing (dawidd6/action-download-artifact#428). The unfiltered list is
            // complete, so walk it newest first back to the search result and use any newer wanted run it missed.
            if (branch || event || commit) {
                let pages = 0
                walk: for await (const runs of client.paginate.iterator(client.rest.actions.listWorkflowRuns, {
                    owner: owner,
                    repo: repo,
                    workflow_id: workflow,
                    per_page: 100,
                }
                )) {
                    for (const run of runs.data.sort((a, b) => b.id - a.id)) {
                        if (foundRun && run.id <= foundRun.id) {
                            break walk
                        }
                        if ((branch && run.head_branch !== branch) || (event && run.event !== event) || (commit && run.head_sha !== commit)) {
                            continue
                        }
                        if (await isWantedRun(run)) {
                            core.warning(`Run search missed newer run ${run.id}` + (foundRun ? ` (returned ${foundRun.id})` : "") + `; using ${run.id}`)
                            foundRun = run
                            break walk
                        }
                    }
                    if (++pages >= UNFILTERED_PAGE_LIMIT) {
                        core.warning(`Checked the latest ${pages * 100} runs without reaching the run search result; using the search result`)
                        break
                    }
                }
            }

            if (foundRun && requireBranchHead) {
                const head = await client.rest.repos.getBranch({
                    owner: owner,
                    repo: repo,
                    branch: branch,
                })
                if (foundRun.head_sha !== head.data.commit.sha) {
                    throw new Error(`Newest matching run ${foundRun.id} was built from ${foundRun.head_sha}, but ${branch} HEAD is ${head.data.commit.sha}. Build the branch HEAD and try again.`)
                }
                core.info(`==> Run is at ${branch} HEAD: ${head.data.commit.sha}`)
            }

            if (foundRun) {
                runID = foundRun.id
                core.info(`==> (found) Run ID: ${runID}`)
                core.info(`==> (found) Run date: ${foundRun.created_at}`)
            }
        }

        if (!runID) {
            if (workflowConclusion && (workflowConclusion != 'in_progress')) {
                return setExitMessage(ifNoArtifactFound, "no matching workflow run found with any artifacts?")
            }

            try {
                return await downloadAction(name, path)
            } catch (error) {
                return setExitMessage(ifNoArtifactFound, "no matching artifact in this workflow?")
            }
        }

        core.setOutput("run_id", runID)

        let artifacts = await client.paginate(client.rest.actions.listWorkflowRunArtifacts, {
            owner: owner,
            repo: repo,
            run_id: runID,
        })

        // One artifact, a list of artifacts, or all if `artifacts` input is not specified.
        const matchesWithRegex = (stringToTest, regexRule) => {
            const escapeSpecialChars = (string) => string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
            const builtRegexRule = "^" + regexRule.split("*").map(escapeSpecialChars).join(".*") + "$"
            return new RegExp(builtRegexRule).test(stringToTest)
        }

        const artifactNames = names.split(",").map(artifactName => artifactName.trim())
        artifacts = artifacts.filter(artifact => {
            return artifactNames.map(name => matchesWithRegex(artifact.name, name)).reduce((prevValue, currValue) => prevValue || currValue)
        })

        core.setOutput("artifacts", artifacts)

        // The selected run can have no matching artifacts (e.g. they expired), so only read
        // the build info when there is an artifact to read it from.
        if (artifacts.length > 0) {
            const artifactBuildCommit = artifacts[0].workflow_run.head_sha;
            core.setOutput("artifact-build-commit", artifactBuildCommit);

            const artifactBuildBranch = artifacts[0].workflow_run.head_branch;
            core.setOutput("artifact-build-branch", artifactBuildBranch);
        }

        if (dryRun) {
            if (artifacts.length == 0) {
                core.setOutput("dry_run", false)
                core.setOutput("found_artifact", false)
                return
            } else {
                core.setOutput("dry_run", true)
                core.setOutput("found_artifact", true)
                core.info('==> (found) Artifacts')
                for (const artifact of artifacts) {
                    const size = filesize(artifact.size_in_bytes, { base: 10 })
                    core.info(`\t==> Artifact:`)
                    core.info(`\t==> ID: ${artifact.id}`)
                    core.info(`\t==> Name: ${artifact.name}`)
                    core.info(`\t==> Size: ${size}`)
                }
                return
            }
        }

        if (artifacts.length == 0) {
            return setExitMessage(ifNoArtifactFound, "no artifacts found")
        }

        core.setOutput("found_artifact", true)

        for (const artifact of artifacts) {
            core.info(`==> Artifact: ${artifact.id}`)

            const size = filesize(artifact.size_in_bytes, { base: 10 })

            core.info(`==> Downloading: ${artifact.name}.zip (${size})`)

            let zip
            try {
                zip = await client.rest.actions.downloadArtifact({
                    owner: owner,
                    repo: repo,
                    artifact_id: artifact.id,
                    archive_format: "zip",
                })
            } catch (error) {
                if (error.message === "Artifact has expired") {
                    return setExitMessage(ifNoArtifactFound, "no downloadable artifacts found (expired)")
                } else {
                    throw new Error(error.message)
                }
            }

            if (skipUnpack) {
                fs.mkdirSync(path, { recursive: true })
                fs.writeFileSync(`${pathname.join(path, artifact.name)}.zip`, Buffer.from(zip.data), 'binary')
                continue
            }

            const dir = path

            fs.mkdirSync(dir, { recursive: true })

            const adm = new AdmZip(Buffer.from(zip.data))

            core.startGroup(`==> Extracting: ${artifact.name}.zip`)
            adm.getEntries().forEach((entry) => {
                const action = entry.isDirectory ? "creating" : "inflating"
                const filepath = pathname.join(dir, entry.entryName)

                core.info(`  ${action}: ${filepath}`)
            })

            adm.extractAllTo(dir, true)
            core.endGroup()
        }
    } catch (error) {
        core.setOutput("found_artifact", false)
        core.setOutput("error_message", error.message)
        core.setFailed(error.message)
    }

    function setExitMessage(ifNoArtifactFound, message) {
        core.setOutput("found_artifact", false)

        switch (ifNoArtifactFound) {
            case "fail":
                core.setFailed(message)
                break
            case "warn":
                core.warning(message)
                break
            case "ignore":
            default:
                core.info(message)
                break
        }
    }
}

main()
