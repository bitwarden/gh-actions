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
- [ ] assert runs-on is pinned
- [ ] assert any environment variables start with "_"

#### shared steps
- [x] assert name exists
- [x] assert name is capitilized

#### uses steps
- [ ] assert valid hash format - correct length
- [ ] assert valid hash format - cast to hexidecimal
- [ ] assert valid action repo path format
- [ ] assert action exists in GitHub
- [ ] warn out of date Action
- [ ] warn using an unapproved Action

#### run steps
- [ ] assert correct format for single line run
```

