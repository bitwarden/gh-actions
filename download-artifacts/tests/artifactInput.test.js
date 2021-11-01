const artifactInput = require('../artifactInput.js')


const allArtifacts = [
    { "id": 1234, "name": "artifact1.txt", "size_in_bytes": 42 },
    { "id": 1235, "name": "artifact2.txt", "size_in_bytes": 42 },
    { "id": 1236, "name": "dump.zip", "size_in_bytes": 42 },
    { "id": 1237, "name": "artifact11.txt", "size_in_bytes": 42 },
    { "id": 1238, "name": "artifact12.txt", "size_in_bytes": 42 }
]

test('single artifact filtering', () => {
    const artifactFilters = `artifact1.txt`

    expect(artifactInput.getListOfArtifactsToDownload(allArtifacts, artifactFilters)).toStrictEqual({
        artifactsToDownload: [{ "id": 1234, "name": "artifact1.txt", "size_in_bytes": 42, "downloadName": "artifact1.txt" }],
        errors: []
    })
})

test('multiple artifact filtering', () => {
    const artifactFilters = `artifact1.txt,
                             artifact2.txt,
                             dump.zip`

    expect(artifactInput.getListOfArtifactsToDownload(allArtifacts, artifactFilters)).toStrictEqual({
        artifactsToDownload: [
            { "id": 1234, "name": "artifact1.txt", "size_in_bytes": 42, downloadName: "artifact1.txt" },
            { "id": 1235, "name": "artifact2.txt", "size_in_bytes": 42, downloadName: "artifact2.txt" },
            { "id": 1236, "name": "dump.zip", "size_in_bytes": 42, downloadName: "dump.zip" }
        ],
        errors: []
    })
})

test('single artifact filtering with rename', () => {
    const artifactFilters = `artifact1.txt|renamed_artifact1.txt`

    expect(artifactInput.getListOfArtifactsToDownload(allArtifacts, artifactFilters)).toStrictEqual({
        artifactsToDownload: [{ "id": 1234, "name": "artifact1.txt", "size_in_bytes": 42, downloadName: "renamed_artifact1.txt" }],
        errors: []
    })
})

test('multiple artifact filtering with rename', () => {
    const artifactFilters = `artifact1.txt|renamed_artifact1.txt,
                             artifact2.txt|renamed_artifact2.txt,
                             dump.zip|renamed_dump.zip`

    expect(artifactInput.getListOfArtifactsToDownload(allArtifacts, artifactFilters)).toStrictEqual({
        artifactsToDownload: [
            { "id": 1234, "name": "artifact1.txt", "size_in_bytes": 42, downloadName: "renamed_artifact1.txt" },
            { "id": 1235, "name": "artifact2.txt", "size_in_bytes": 42, downloadName: "renamed_artifact2.txt" },
            { "id": 1236, "name": "dump.zip", "size_in_bytes": 42, downloadName: "renamed_dump.zip" }
        ],
        errors: []
    })
})
