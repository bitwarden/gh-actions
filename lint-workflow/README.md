# lint-workflow

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

#### workflows

- [x] assert name exists
- [x] assert name is capitalized

#### jobs

- [x] assert name exists
- [x] assert name is capitalized
- [x] assert runs-on is pinned
- [x] assert any environment variables start with "_"

#### shared steps
- [x] assert name exists
- [x] assert name is capitilized

#### uses steps
- [x] assert valid hash format - correct length
- [x] assert valid hash format - cast to hexidecimal
- [x] warn using an unapproved Action
- [x] warn out of date Action
- [ ] (DEPRECATED) assert action exists in GitHub (deprecated in favor of the approved list of actions)
- [ ] (DEPRECATED) assert valid action repo path format (deprecated in favor fo the approved list of actions)

#### run steps
- [ ] assert correct format for single line run
```

