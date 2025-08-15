# GitHub Copilot Instructions for Bitwarden GitHub Actions

## Repository Overview

This repository contains a collection of custom GitHub Actions used by Bitwarden to simplify and standardize CI/CD pipelines across their projects. The repository follows a modular structure where each action is self-contained in its own directory with its own `action.yml` file.

**Repository Details:**
- **Type**: GitHub Actions collection
- **Size**: Medium-sized repository with ~20 custom actions
- **Languages**: TypeScript, Python, JavaScript, Shell scripts, YAML
- **Target Runtime**: GitHub Actions runners (primarily Ubuntu)

## Build and Validation Instructions

### Prerequisites
- Node.js (version 22+ for TypeScript actions)
- Python 3.13+ (for Python-based actions)
- Docker (for containerized actions)

### Initial Setup
1. **Always run `npm install` first** in the repository root to install development dependencies including Prettier, Husky, and lint-staged.

### Code Formatting and Linting
- **Code formatting**: This repository uses Prettier for all file types
- **Pre-commit hooks**: Husky is configured to run lint-staged on commit
- **Command**: `npx prettier --cache --write --ignore-unknown .` (formats all files)
- **Automatic formatting**: Runs automatically on commit via pre-commit hook

### Workflow Linter Rules Compliance

All suggestions and reviews concerning workflow files (e.g., changes to `.github/workflows/`) **must respect the rules defined by the Bitwarden Workflow Linter**.

Each workflow file must comply with the following linter rules ([source directory](https://github.com/bitwarden/workflow-linter/tree/main/src/bitwarden_workflow_linter/rules)):

- **check_pr_target.py**: Ensures workflows using pull_request_target only run using the default branch (usually `main`).
- **job_environment_prefix.py**: Enforces required environment variable naming conventions for jobs.
- **name_capitalized.py**: Validates that workflow and job names begin with a capital letter.
- **name_exists.py**: Checks that every workflow and job has a name defined.
- **permissions_exist.py**: Verifies that the `permissions` key is explicitly set for each workflow or each job inside the workflow.
- **pinned_job_runner.py**: Ensures job runners are pinned to specific versions.
- **run_actionlint.py**: Runs `actionlint` to provide additional workflow checks.
- **step_approved.py**: Only allows steps that have been explicitly approved by Bitwarden tracked in ([approved actions directory](https://github.com/bitwarden/workflow-linter/blob/main/src/bitwarden_workflow_linter/default_actions.json)).
- **step_pinned.py**: Verifies that every workflow step using an external GitHub action in the `uses` key is pinned to a hash with the version in a comment.
- **underscore_outputs.py**: Enforces that all GitHub outputs with more than one word use an underscore.

Refer to the [rules directory](https://github.com/bitwarden/workflow-linter/tree/main/src/bitwarden_workflow_linter/rules) for further details or updates to rule logic.

**Trigger**: Automatic on PR when `.github/workflows/**` files change
**Setup**: The linter downloads configuration from `bitwarden/workflow-linter` repository
**Command**: `bwwl lint -f <workflow_files>`
**Python requirement**: Python 3.13+ with `pip install bitwarden_workflow_linter`

### Testing Individual Actions
Each action has its own test workflow in `.github/workflows/test-*.yml`:
- `test-version-bump.yml` - Tests version bumping functionality
- `test-get-secrets.yml` - Tests Azure Key Vault integration  
- `test-download-artifacts.yml` - Tests artifact downloading
- `test-release-version-check.yml` - Tests release version validation
- And others...

**Test execution**: Tests run automatically on PRs affecting specific action directories.

### TypeScript Actions Build Process
For TypeScript-based actions (e.g., `get-keyvault-secrets`):
1. Source files are in `src/` directory
2. **Always run `npm run build`** or `tsc` to compile TypeScript to JavaScript
3. Compiled output goes to `lib/` directory
4. The `action.yml` references the compiled `lib/main.js` file
5. **Critical**: Always commit both source AND compiled files

### Docker-based Actions
For containerized actions (e.g., `version-bump`, `get-checksum`):
- Use `Dockerfile` in action directory
- Python scripts use `main.py` as entry point
- **No local build required** - Docker builds during action execution

## Project Layout and Architecture

### Repository Structure
```
/
├── package.json                    # Root dependencies (Prettier, Husky, lint-staged)
├── .husky/pre-commit              # Git pre-commit hook configuration
├── .github/
│   ├── workflows/                 # CI/CD workflows and action tests
│   │   ├── workflow-linter.yml    # Workflow validation
│   │   ├── test-*.yml            # Individual action tests
│   │   └── *.yml                 # Various CI workflows
│   └── copilot-instructions.md   # This file
└── [action-name]/                 # Each action in its own directory
    ├── action.yml                 # Action definition (required)
    ├── README.md                  # Action documentation
    ├── main.py|main.js|Dockerfile # Action implementation
    ├── package.json              # Dependencies (if Node.js)
    ├── tsconfig.json             # TypeScript config (if applicable)
    ├── src/                      # TypeScript source (if applicable)
    ├── lib/                      # Compiled output (if TypeScript)
    └── tests/fixtures/           # Test data files
```

### Key Actions by Type

**TypeScript/Node.js Actions:**
- `get-keyvault-secrets/` - Azure Key Vault integration
- `download-artifacts/` - Artifact management

**Python/Docker Actions:**
- `version-bump/` - File version updating (JSON, XML, PLIST, YAML)
- `get-checksum/` - SHA256 checksum generation
- `crowdin/` - Translation management

**Shell/YAML Actions:**
- `azure-login/`, `azure-logout/` - Azure authentication
- `setup-docker-trust/` - Docker configuration
- Various reporting and utility actions

### CI/CD Validation Pipeline

**Pre-commit Checks:**
1. Prettier formatting (automatic via Husky)
2. Lint-staged validation

**Pull Request Checks:**
1. Workflow linting (if `.github/workflows/` changed)
2. Action-specific tests (if action directory changed)
3. Various security and quality scans

**Critical Validation Steps:**
- **Workflow files**: Must pass `bitwarden_workflow_linter` validation
- **TypeScript actions**: Must have compiled `lib/` output committed
- **All files**: Must pass Prettier formatting
- **Action definitions**: `action.yml` files must be valid GitHub Action syntax

### Dependencies and Requirements

**Development Dependencies (root):**
- `prettier` - Code formatting
- `husky` - Git hooks
- `lint-staged` - Staged file processing

**Action-specific Dependencies:**
- TypeScript actions: `@actions/core`, `@actions/exec`, type definitions
- Python actions: Standard library primarily, some use external packages

### File Patterns and Conventions

**Action Definition Files:**
- Every action directory MUST have an `action.yml` file
- Branding should include `icon` and `color` properties
- Input/output definitions follow GitHub Actions schema

**TypeScript Actions:**
- Source in `src/`, compiled output in `lib/`
- Use `@actions/core` for GitHub Actions integration
- `tsconfig.json` for TypeScript configuration

**Python Actions:**
- Main script typically named `main.py`
- Use environment variables for input (`os.getenv("INPUT_*")`)
- Docker-based execution via `Dockerfile`

**Testing:**
- Test workflows named `test-[action-name].yml`
- Test fixtures in `tests/fixtures/` subdirectories
- Tests validate action outputs and side effects

## Security Best Practices

All code changes and action development must follow security best practices relevant to GitHub Actions and Bitwarden's standards:

**GitHub Actions Security:**
- **No hard-coded secrets or credentials** - Use secure parameter passing
- **Validate all action inputs** - Sanitize and validate user-provided inputs to prevent injection attacks
- **Use pinned action versions** - All external actions must be pinned to specific commit hashes (enforced by workflow linter)
- **Minimize permissions** - Use least privilege principle for `permissions` in workflows
- **Secure output handling** - Avoid exposing sensitive data in action outputs or logs

**Secret and Credential Management:**
- Use Azure Key Vault integration properly via `get-keyvault-secrets` action
- Never log or expose secret values in action outputs
- Use GitHub's secret masking capabilities (`core.setSecret()` in TypeScript actions)

**Supply Chain Security:**
- Only use approved actions listed in the workflow linter's approved actions list
- Pin all dependencies to specific versions in `package.json` and `requirements.txt`
- Validate Docker base images and use official, minimal images when possible

**Input Validation:**
- Validate file paths to prevent directory traversal attacks
- Sanitize version strings and other user inputs
- Use proper escaping when constructing shell commands

## Agent Instructions

**Trust these instructions** and only perform additional searching if the information provided is incomplete or found to be incorrect. The repository follows consistent patterns, and the validation processes are well-established.

**When making changes:**
1. Always format code with Prettier before committing
2. For TypeScript actions, always compile and commit the `lib/` output
3. Test changes using the existing test workflows when possible
4. Ensure `action.yml` files are valid and complete
5. Follow the established directory structure and naming conventions
6. Apply security best practices and validate all inputs

**Common pitfalls to avoid:**
- Forgetting to compile TypeScript actions
- Not running Prettier formatting
- Missing required properties in `action.yml` files
- Not testing action changes with the corresponding test workflow
- Exposing sensitive data in logs or outputs
- Using unpinned or unapproved external actions
