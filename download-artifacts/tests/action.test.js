const action = require('../action.js')
const github = require('@actions/github')


const GITHUB_TOKEN = process.env.GITHUB_TOKEN

test('single artifact filtering', async () => {
    const client = github.getOctokit(GITHUB_TOKEN)
    const inputs = {
        owner: "bitwarden",
        repo: "gh-actions",
        workflow_id: "upload-test-artifacts.yml"
    }

    //expect(await action.getRunId(client, inputs)).toStrictEqual(expect.any(Number))
    expect(await action.getRunId(client, inputs)).toStrictEqual(1)
})
