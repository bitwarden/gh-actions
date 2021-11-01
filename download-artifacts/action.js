const github = require('@actions/github')
const AdmZip = require('adm-zip')
const filesize = require('filesize')
const pathname = require('path')
const _ = require('underscore')
const fs = require('fs')

const artifactInputs = require('./artifactInput.js')


const getRunId = async (client, inputs) => {
    if (inputs.runID) {
        console.log("==> RunID:", inputs.runID)
    } else {
        const restInputs = {
            owner: inputs.owner,
            repo: inputs.repo,
            workflow_id: inputs.workflow,
            branch: inputs.branch,
            event: inputs.event,
        }

        const workflowRun = _.chain(client.paginate(client.rest.listWorkflowRuns, restInputs))
            .filter(run => {
                return (
                    (inputs.commit && run.head_sha != inputs.commit)
                    && (inputs.runNumber && run.run_number != inputs.runNumber)
                    && (inputs.workflowConclusion && (inputs.workflowConclusion != run.conclusion && inputs.workflowConclusion != run.status))
                )
            })
            .value()

        console.log(`runs: ${workflowRun}`)

            //.filter(run => {
            //    const artifacts = clients.rest.actions.listWorkflowRunArtifacts({
            //        owner: inputs.owner,
            //        repo: inputs.repo,
            //        run_id: run.id
            //    })
            //    return artifacts.data.artifacts.length > 0 ? true : false
            //})
            //.first()
            //.value()

        if (!workflowRun)
            throw new Error("cannot find the workflow")
            
        return workflowRun.id 
    }
}

const run = async inputs => {
    try {
        const client = github.getOctokit(token)

        _.chain(inputs)
            .keys()
            .each(key => {
                if (key)
                    console.log(`==> ${key}: ${inputs[key]}`)
            })
            .value()

        if (inputs.pr) {
            console.log("==> PR:", pr)

            const pull = await client.pulls.get({
                owner: owner,
                repo: repo,
                pull_number: pr,
            })
            commit = pull.data.head.sha
        }


        const runId = getRunId(client, inputs)

        const allArtifacts = await client.paginate(client.rest.actions.listWorkflowRunArtifacts, {
            owner: owner,
            repo: repo,
            run_id: runID,
        })

        const { artifactsToDownload, renameCheckErrors } = artifactInputs.getListOfArtifactsToDownload(allArtifacts, artifactNamesFromAction)

        if (artifactsToDownload.length == 0)
            throw new Error("no artifacts found")
        
        if (renameCheckErrors.length > 0) {
            _.each(renameCheckErrors, element => {
                console.log(`==> Multiple matches on "${element.namePattern}". Cannot use the artifact rename functionality`)
            })

            throw new Error("!!! trying to use the artifact rename functionality on a glob pattern with multiple matches")
        }

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

module.exports = {
    getRunId: getRunId
}
