from pydantic import BaseModel, Extra, Field, root_validator
from ruamel.yaml.comments import CommentedMap


class Step(BaseModel, extra=Extra.allow):
    name: str = None
    id: str = None
    env: CommentedMap = None
    uses: str = None
    with_field: CommentedMap = Field(None, alias="with")
    run: str = None

    #@root_validator
    #def check_uses_or_run(cls, values):
    #    uses, run = values.get('uses'), values.get('run')

    #    if uses is None and run is None:
    #        raise ValueError("Either 'uses' or 'run' must be set")

    #    if uses is not None and run is not None:
    #        raise ValueError("cannot set both 'uses' and 'run'")

    #    return values
