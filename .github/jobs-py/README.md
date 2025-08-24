# Action Jobs - Python Scripts

## Requirements
- pipenv (with Python 3.11)

## Notes
If we go with something like this for the initial IDP client tool, something like
[PyOxidizer](https://gregoryszorc.com/docs/pyoxidizer/main/pyoxidizer_getting_started.html) would be a good for anyone
that doesn't require custom plugins (if this is something that we would want to support). This would allow us to ship a
binary (and lessen the CI pipeline impacts of setting up and install all dependencies every time we need a job)

## Development
### Initial Setup
```
cp .env.example .env

# edit .env with a GitHub token with "read public repos" permissions
```

### MacOS (brew)
```
pipenv install
pipenv shell

pytest
```


### (Nix - jflinn...)
```
nix-shell
pipenv install
pipenv shell

pytest
```


## Jobs
### Get PR ID

Get the PR ID number associated with a commit on the default branch or return `None`

**Params:** (string)
**Return:** (string) int | None

#### Example
```yaml
      - name: Sparse Checkout of Jobs dir
        uses: actions/checkout@v4.1.1
        with:
          sparse-checkout: |
            .github/jobs-py

      - name: Setup Python
        uses: actions/setup-python@v4.7.1
        with:
          python-version: '3.11'

      - name: Install pipenv and setup project
        run: |
          pip install pipenv
          pipenv install

      - name: Assert
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          ID=$(python .github/jobs-py/src/get_pr_id.py "7d46c75af91adbfdfc70689f4d8b3405b26bda6b")
          if [[ "$ID" != "196" ]]; then
            exit 1
          fi
          exit 0
```


