# Cherry-pick Reusable Workflow

## Description
The `cherry-pick.yml` provides an automated, on-demand way to cherry-pick commits from merged PRs into destination branches (typically `rc` or `hotfix-rc` branches). This workflow is triggered via `workflow_dispatch`, allowing you to specify which PR to cherry-pick and where to cherry-pick it to.

## Key Features
- **Manual Control**: Trigger cherry-picks on-demand via a GitHub workflow run
- **Configurable Destination Branches**: Allow cherry-picking to any branch, or restrict to specific allow-listed branches
- **Automatic Labeling**: Successfully cherry-picked PRs are automatically labeled with `cherry-picked`
- **Validation**: Ensures source PR is merged to `main` and destination branch exists

## How to use it

### Setup
1. Copy the `cherry-pick.yml` workflow template into your repository's `.github/workflows/` directory
2. Update `cherry-pick.yml` with either `string` or `choice` input for the `dest_branch` input. Remove the other type from the yaml.

### Usage
1. Navigate to **Actions** → **Automated cherry pick** in your repository
2. Click **Run workflow**
3. Enter the required inputs:
   - **Pull request to cherry pick from**: The PR number (e.g., `123`)
   - **Destination branch to cherry pick to**: The target branch name (e.g., `rc-2024-01`)
4. Click **Run workflow**

The workflow will:
1. Validate that the source PR is merged to `main`
2. Validate that the destination branch exists
3. Cherry-pick the merge commit to the destination branch
4. Push the changes directly to the destination branch
5. Add the `cherry-picked` label to the source PR

## Workflow Diagram
```mermaid
flowchart TB
    subgraph Trigger["Triggering Event"]
        A[Manual workflow_dispatch<br/>Inputs:<br/>- source_pr *required*<br/>- dest_branch *required*]
    end

    subgraph Caller["cherry-pick.yml"]
        B[Receive inputs]
        C[Call _cherry-pick.yml]
        D[Pass inputs:<br/>- source_pr<br/>- dest_branch]
    end

    subgraph Reusable["_cherry-pick.yml"]
        direction TB

        subgraph Auth["Authentication"]
            E1[Log in to Azure]
            E2[Get GitHub App credentials<br/>from Key Vault]
            E3[Generate GitHub App token]
        end

        subgraph Validate["Validation"]
            F1[Checkout repo]
            F2{Destination branch<br/>exists?}
            F3[Fetch PR info via gh CLI]
            F4{Running in test mode?}
            F5{Only accpet PR base ref<br/>'cherry-pick-sim-main-*'}
            F6{Only accept PR base ref<br/>'main'}
            F7{PR state<br/>is 'MERGED'?}
            F8{Merge commit<br/>exists?}
            F9[Extract merge commit SHA]
        end

        subgraph CherryPick["Cherry Pick"]
            G1[Checkout destination branch<br/>with App token]
            G2[Configure git user]
            G3[Cherry-pick merge commit]
            G4{Cherry-pick<br/>succeeded?}
            G5[Push to destination branch]
            G6[Add 'cherry-picked' label to source PR]
        end

        subgraph Errors["Error Handling"]
            H1[❌ Branch not found]
            H2[❌ Invalid test base ref]
            H3[❌ Invalid base ref]
            H4[❌ PR not merged]
            H5[❌ No merge commit]
            H6[❌ Cherry-pick failed<br/>abort & exit]
        end
    end

    subgraph Result["✅ End Result"]
        I1[Commit cherry-picked to<br/>destination branch]
        I2[Source PR labeled<br/>'cherry-picked']
    end

    A --> B
    B --> C
    C --> D
    D --> E1

    E1 --> E2
    E2 --> E3
    E3 --> F1

    F1 --> F2
    F2 -->|No| H1
    F2 -->|Yes| F3
    F3 --> F4

    F4 -->|Yes, test mode| F5
    F4 -->|No, production| F6

    F5 -->|Valid| F7
    F5 -->|Invalid| H2

    F6 -->|Valid| F7
    F6 -->|Invalid| H3

    F7 -->|Merged| F8
    F7 -->|Not merged| H4

    F8 -->|Exists| F9
    F8 -->|Missing| H5

    F9 --> G1
    G1 --> G2
    G2 --> G3
    G3 --> G4
    G4 -->|No| H6
    G4 -->|Yes| G5
    G5 --> G6

    G6 --> I1
    G6 --> I2

    style Trigger fill:#e1f5ff
    style Caller fill:#fff4e1
    style Reusable fill:#e8f5e9
    style Auth fill:#f0f4ff
    style Validate fill:#fff8e1
    style CherryPick fill:#e0f2f1
    style Errors fill:#ffcdd2
    style Result fill:#f3e5f5
    style F4 fill:#ffe0b2
    style F5 fill:#fff9c4
```

## Requirements
- source PR must already be merged into `main`
- source PR must have been squash merged
- destination branch must already exist
- the `cherry-pick` label must exist in the repo

## Troubleshooting

### "Could not find destination branch" error
- Verify the destination branch name is spelled correctly
- Ensure the branch exists in the repository
- Branch names are case-sensitive

### "Invalid PR base ref" error
- The source PR must have `main` as its base branch
- PRs targeting other branches cannot be cherry-picked with this workflow

### "PR not merged" error
- The PR must be in `MERGED` state
- Closed (but not merged) PRs cannot be cherry-picked
- Wait for the PR to be fully merged before triggering the workflow

### Cherry-pick failed with conflicts
- The workflow will abort and exit with an error.
- You'll need to resolve conflicts manually:
  1. Check out the destination branch locally
  2. Cherry-pick the commit manually: `git cherry-pick <commit-sha>`
  3. Resolve conflicts
  4. Push your changes
  5. Open a PR

### "Failed to add label" warning
- This is a non-fatal error
- The cherry-pick succeeded, but labeling the PR failed
- You can manually add the `cherry-picked` label if needed
- Check that repo has the `cherry-pick` label created

## Testing

The workflow includes a test workflow at `.github/workflows/test-cherry-pick.yml` that:
1. Creates simulated branches and a test PR
2. Merges the test PR
3. Calls `_cherry-pick.yml` to cherry-pick the commit
4. Cleans up all test resources

This test workflow can be triggered via `workflow_dispatch` or automatically runs on changes to the `_cherry-pick.yml` reusable workflow.
