const _ = require('underscore')

// Setup the simple glob matching pattern for the artifact names
const matchesWithRegex = (stringToTest, regexRule) => {
    const escapeSpecialChars = (string) => string.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    const builtRegexRule = "^" + regexRule.split("*").map(escapeSpecialChars).join(".*") + "$";
    return new RegExp(builtRegexRule).test(stringToTest);
}

/* Handle the renmaing functionality
 * artifacts: 'artifact.txt|hello-world.txt'
 */
const splitArtifactInput = input => {
    const names = input.split("|");
    return {
        "pattern": names[0].trim(),
        "downloadName": names.length > 1 ? names[1].trim() : names[0].trim()
    }
}


const GetListOfArtifactsToDownload = (allArtifacts, artifactsInputFilter) => {
    const artifactsInput = _.map(artifactsInputFilter.split(","), input => splitArtifactInput(input))

    const artifactsToDownload = allArtifacts.filter(artifact => {
        return _.chain(artifactsInput)
            .map(input => matchesWithRegex(artifact.name, input.pattern))
            .reduce((prevValue, currValue) => prevValue || currValue)
            .value()
    })

    const renameCheckErrors = _.chain(artifactsInput)
        .reduce((counts, artifact) => {
            counts[artifact.pattern] = (counts[artifact.pattern] || 0) + 1;
            return counts;
        }, {})
        .filter(input => input.count > 1)
        .value();


    // need to add the new name to the artifactsDownload data
    const artifactData = _.map(artifactsToDownload, artifact => {
        const matchingPattern = _.chain(artifactsInput)
            .filter(input => {
                return matchesWithRegex(artifact.name, input.pattern)
            })
            .first()
            .value().downloadName;
        return {
            ...artifact,
            downloadName: matchingPattern
        }
    })

    return {
        artifactsToDownload: artifactData,
        errors: renameCheckErrors
    }
}

module.exports = {
    getListOfArtifactsToDownload: GetListOfArtifactsToDownload
}
