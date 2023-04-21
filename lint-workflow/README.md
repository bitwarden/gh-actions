# lint-workflow

## Development
### Requirements

- Python 3.9
- pipenv

### Setup

```
pipenv install --dev
pipenv shell
```

### Testing

```
pipenv shell
pytest tests
```

### Code Reformatting

```
pipenv shell
black .
```


## Design
### Objects

**Workflow:**
**Jobs:**
**Steps (run || uses):** 


### Rules

```yaml
workflows:
  - assert name exists
  - assert name is capitalized
jobs:
  - assert runner is pinned
  - assert name exists
  - assert name is capitalized
  - assert any environment variables start with "_"
steps:
  shared: 
    - assert name exists
    - assert name is capitilized
  uses:
    - assert valid hash format - correct length
    - assert valid hash format - cast to hexidecimal
    - assert valid action repo path format
    - assert action exists in GitHub
    - warn out of date Action
  run:
    - assert correct format for single line run
```

