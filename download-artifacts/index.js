const core = require('@actions/core')

const action = require('./action.js')

const main = async () => {
    const inputs = {
        token: core.getInput("github_token", { required: true }),
        workflow: core.getInput("workflow", { required: true }),
        owner: core.getInput("repo", { required: true }).split("/")[0],
        repo: core.getInput("repo", { required: true }).split("/")[1],
        pathFromAction: core.getInput("path", { required: true }),
        artifactNamesFromAction: core.getInput("artifacts") ? core.getInput("artifacts") : "*",
        workflowConclusion: core.getInput("workflow_conclusion"),
        pr: core.getInput("pr"),
        commit: core.getInput("commit"),
        branch: core.getInput("branch"),
        event: core.getInput("event"),
        runID: core.getInput("run_id"),
        runNumber: core.getInput("run_number"),
        checkArtifacts: core.getInput("check_artifacts")
    }

    action.run(inputs)
}

main()
