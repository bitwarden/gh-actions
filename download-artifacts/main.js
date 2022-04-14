const core = require('@actions/core')
const github = require('@actions/github')
const AdmZip = require('adm-zip')
const filesize = require('filesize')
const pathname = require('path')
const fs = require('fs')

async function main() {
    try {
        const token = core.getInput("github_token", { required: true })
        const workflow = core.getInput("workflow", { required: true })
        const [owner, repo] = core.getInput("repo", { required: true }).split("/")
        const pathFromAction = core.getInput("path", { required: true })
        const artifactNamesFromAction = core.getInput("artifacts") ? core.getInput("artifacts") : "*"
        let workflowConclusion = core.getInput("workflow_conclusion")
        let pr = core.getInput("pr")
        let commit = core.getInput("commit")
        let branch = core.getInput("branch")
        let event = core.getInput("event")
        let runID = core.getInput("run_id")
        let runNumber = core.getInput("run_number")
        let checkArtifacts = core.getInput("check_artifacts")

        const client = github.getOctokit(token)

        console.log("==> Workflow:", workflow)
        console.log("==> Repo:", owner + "/" + repo)
        console.log("==> Conclusion:", workflowConclusion)

        if (pr) {
            console.log("==> PR:", pr)

            const pull = await client.pulls.get({
                owner: owner,
                repo: repo,
                pull_number: pr,
            })
            commit = pull.data.head.sha
        }

        /*
        if (workflow.includes(".yml") || workflow.includes(".yaml")) {
            try {
                workflow = client.actions.listRepoWorkflows({
                    owner: owner,
                    repo: repo
                }).filter(workflow => workflow.path == `.github/workflows/${workflow}`)[0].name
            } catch (error) {
                throw new Error("No matching workflow found in this repository")
            }
        }
        */

        if (commit) {
            console.log("==> Commit:", commit)
        }

        if (branch) {
            branch = branch.replace(/^refs\/heads\//, "")
            console.log("==> Branch:", branch)
        }

        if (event) {
            console.log("==> Event:", event)
        }

        if (runNumber) {
            console.log("==> RunNumber:", runNumber)
        }

        if (!runID) {
            const runs = await client.actions.listWorkflowRuns({
                owner: owner,
                repo: repo,
                workflow_id: workflow
            }).then(runs => {
                console.log(`Type of runs: ${typeof(runs)}\nruns: ${runs}`)
                return runs.filter(run => run.head_branch == branch)
                .sort((a, b) => {
                    a_date = new Date(a.created_at)
                    b_date = new Date(b.created_at)
                    return a_date - b_date
                })
            })

            for (const run of runs.data) {
                if (commit && run.head_sha != commit) {
                    continue
                }
                if (runNumber && run.run_number != runNumber) {
                    continue
                }
                if (workflowConclusion && (workflowConclusion != run.conclusion && workflowConclusion != run.status)) {
                    continue
                }
                if (checkArtifacts) {
                    let artifacts = await client.actions.listWorkflowRunArtifacts({
                        owner: owner,
                        repo: repo,
                        run_id: run.id,
                    })
                    if (artifacts.data.artifacts.length == 0) {
                        continue
                    }
                }
                runID = run.id
                break
            }
        }

        if (runID) {
            console.log("==> RunID:", runID)
        } else {
            throw new Error("no matching workflow run found")
        }

        const allArtifacts = await client.paginate(client.actions.listWorkflowRunArtifacts, {
            owner: owner,
            repo: repo,
            run_id: runID,
        })

        // One artifact, a list of artifacts, or all if `name` input is not specified.
        const matchesWithRegex = (stringToTest, regexRule) => {
            const escapeSpecialChars = (string) => string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
            const builtRegexRule = "^" + regexRule.split("*").map(escapeSpecialChars).join(".*") + "$"
            return new RegExp(builtRegexRule).test(stringToTest)
        }
        const artifactNames = artifactNamesFromAction.split(",").map(artifactName => artifactName.trim())

        const artifactsToDownload = allArtifacts.filter(artifact => {
            return artifactNames.map(name => matchesWithRegex(artifact.name, name)).reduce((prevValue, currValue) => prevValue || currValue)
        })

        if (artifactsToDownload.length == 0)
            throw new Error("no artifacts found")

        for (const artifact of artifactsToDownload) {
            console.log("==> Artifact:", artifact.id)

            const size = filesize(artifact.size_in_bytes, { base: 10 })

            console.log(`==> Downloading: ${artifact.name}.zip (${size})`)

            const zip = await client.actions.downloadArtifact({
                owner: owner,
                repo: repo,
                artifact_id: artifact.id,
                archive_format: "zip",
            })

            //const dir = artifacts.length == 1 ? pathFromAction : pathname.join(path, artifact.name)

            fs.mkdirSync(pathFromAction, { recursive: true })

            const adm = new AdmZip(Buffer.from(zip.data))

            adm.getEntries().forEach((entry) => {
                const action = entry.isDirectory ? "creating" : "inflating"
                const filepath = pathname.join(pathFromAction, entry.entryName)

                console.log(`  ${action}: ${filepath}`)
            })

            adm.extractAllTo(pathFromAction, true)
        }
    } catch (error) {
        core.setFailed(error.message)
    }
}

main()
