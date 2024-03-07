# Bitwarden Workflow Linter

## Installation

## PyPi
```
Not yet implemented
```

### Locally
```
git clone git@github.com:bitwarden/gh-actions.git
cd gh-actions/lint-workflow-v2

pip install -e .
```

## Usage
### Setup settings.yaml

If a non-default configuration is desired (different than `src/bitwarden_workflow_linter/default_settings.yaml`), copy
the below and create a `settings.yaml` in the directory that `bwwl` will be running from.

```yaml
enabled_rules:
  - bitwarden_workflow_linter.rules.name_exists.RuleNameExists
  - bitwarden_workflow_linter.rules.name_capitalized.RuleNameCapitalized
  - bitwarden_workflow_linter.rules.pinned_job_runner.RuleJobRunnerVersionPinned
  - bitwarden_workflow_linter.rules.job_environment_prefix.RuleJobEnvironmentPrefix
  - bitwarden_workflow_linter.rules.step_pinned.RuleStepUsesPinned

approved_actions_path: default_actions.json
```


```
usage: bwwl [-h] [-v] {lint,actions} ...

positional arguments:
  {lint,actions}
    lint          Verify that a GitHub Action Workflow follows all of the Rules.
    actions       Add or Update Actions in the pre-approved list.

options:
  -h, --help      show this help message and exit
  -v, --verbose
```

## Development
### Requirements

- Python 3.11
- pipenv

### Setup

```
pipenv install --dev
pipenv shell
```

### Testing

All built-in `src/bitwarden_workflow_linter/rules` should have 100% code coverage and we should shoot for an overall coverage of 80%+.
We are lax on the
[imperative shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)
(code interacting with other systems; ie. disk, network, etc), but we strive to maintain a high coverage over the
functional core (objects and models).

```
pipenv shell
pytest tests --cov=src
```

### Code Reformatting

We adhere to PEP8 and use `black` to maintain this adherence. `black` should be run on any change being merged
to `main`.

```
pipenv shell
black .
```

### Linting

We loosely use [Google's Python style guide](https://google.github.io/styleguide/pyguide.html), but yield to
`black` when there is a conflict

```
pipenv shell
pylint --rcfile pylintrc src/ tests/
```

### Add a new Rule

A new Rule is created by extending the Rule base class and overriding the `fn(obj: Union[Workflow, Job, Step])` method.
Available attributes of `Workflows`, `Jobs` and `Steps` can be found in their definitons under `src/models`.

For a simple example, we'll take a look at enforcing the existence of the `name` key in a Job. This is already done by
default with the src.rules.name_exists.RuleNameExists, but provides a simple enough example to walk through.

```python
from typing import Union, Tuple

from ..rule import Rule
from ..models.job import Job
from ..models.workflow import Workflow
from ..models.step import Step
from ..utils import LintLevels, Settings


class RuleJobNameExists(Rule):
    def __init__(self, settings: Settings = None) -> None:
        self.message = "name must exist"
        self.on_fail: LintLevels = LintLevels.ERROR
        self.compatibility: List[Union[Workflow, Job, Step]] = [Job]
        self.settings: Settings = settings

    def fn(self, obj: Job) -> Tuple[bool, str]:
        """<doc block goes here> """
        if obj.name is not None:
            return True, ""
        return False, self.message
```

By default, a new Rule needs five things:

- `self.message`: The message to return to the user on a lint failure
- `self.on_fail`: The level of failure on a lint failure (NONE, WARNING, ERROR).
  NONE and WARNING will exit with a code of 0 (unless using `strict` mode for WARNING).
  ERROR will exit with a non-zero exit code
- `self.compatibility`: The list of objects this rule is compatible with. This is used to create separate instances of
  the Rule for each object in the Rules collection.
- `self.settings`: In general, this should default to what is shown here, but allows for overrides
- `self.fn`: The function doing the actual work to check the object and enforce the standard.

`fn` can be as simple or as complex as it needs to be to run a check on a _single_ object. This linter currently does
not support Rules that check against multiple objects at a time OR file level formatting (one empty between each step or
two empty lines between each job)


### ToDo

- [ ] Add Rule to assert correct format for single line run

