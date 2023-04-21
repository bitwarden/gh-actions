from dataclasses import dataclass, field

#from pydantic import BaseModel, Extra, Field, root_validator
from ruamel.yaml.comments import CommentedMap


@dataclass
class Step:
    name: str = None
    env: CommentedMap = None
    uses: str = None
    run: str = None

    #@root_validator
    #def check_uses_or_run(cls, values):
    #    uses, run = values.get('uses'), values.get('run')

    #    if uses is None and run is None:
    #        raise ValueError("Either 'uses' or 'run' must be set")

    #    if uses is not None and run is not None:
    #        raise ValueError("cannot set both 'uses' and 'run'")

    #    return values
