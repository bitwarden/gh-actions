# RC Cherry-pick Reusable Workflow

## Description
The `rc-cherry-pick.yml` and `_rc-cherry-pick.yml` workflows automate the process of cherry-picking commits from merged PRs into RC branches. When a PR is merged to main with a label like `rc-cherry-pick` or `hotfix-rc-cherry-pick`, the workflow automatically extracts all commits, cherry-picks them to the corresponding RC branch, and opens a draft PR for review.

## How to use it
1. Copy the `rc-cherry-pick.yml` workflow (not `_rc-cherry-pick.yml`) into the repo you want to perform the cherry-picking in
2. Create labels in the repo for each RC branch you want to cherry pick to. The labels should use the following syntax:
```
# syntax
<rc_branch_name>-cherry-pick

# example: will cherry-pick from main -> rc-hotfix
rc-hotfix-cherry-pick

# example: will cherry-pick from main -> rc
rc-cherry-pick
```

3. Update the `allowed_labels` input parameter in your repo's copy of `rc-cherry-pick.yml` to include all labels that should trigger the cherry-pick process. This parameter should be in the JSON list format. For example:
        
```
allowed_labels: '["rc-cherry-pick", "hotfix-rc-cherry-pick"]'
```
4. And that's it. Now whenever a PR  with an applicable label is merged into `main`, the `rc-cherry-pick.yml` in your repo will call the reusable `_rc-cherry-pick.yml` workflow, and the cherry-pick process will be triggered!



## Workflow Diagram
```mermaid
flowchart TB
    subgraph Trigger["Triggering Events"]
        A1[PR to main closed]
        A2[Manual workflow_dispatch
            Inputs:
            - source_pr *required*
            - label_override *optional*
            - override_merge_check *optional*
        ]
    end

    subgraph Caller["Caller Workflow<br/>(rc-cherry-pick.yml)"]
        B{Check: PR merged<br/>OR override?}
        C[Call _rc-cherry-pick.yml]
        D[Pass inputs:<br/>- source_pr<br/>- allowed_labels<br/>- label_override *optional*]
    end

    subgraph Reusable["Reusable Workflow (_rc-cherry-pick.yml)"]
        direction TB
        
        subgraph Job1["Job 1: evaluate-pr"]
            E1[Receive inputs]
            E2{label_override<br/>provided?}
            E3[Use override<br/>as single label]
            E4[Fetch actual PR labels<br/>via `gh pr view`]
            E5[Compare each PR label<br/>with allowed_labels list]
            E6{Found exactly<br/>one match?}
            E7[Strip '-cherry-pick' suffix<br/>to get RC branch name]
            E8[Set output:<br/>rc_branch]
            E9[❌ ERROR: Multiple<br/>cherry-pick labels]
            E10[Skip: No matching label]
        end
        
        subgraph Job2["Job 2: cherry-pick"]
            F1{rc_branch output<br/> empty?}
            F2[Checkout RC branch<br/>git checkout rc_branch]
            F3[Extract all commit SHAs<br/>from source PR]
            F4[Create new branch<br/>cherry-pick-PRX-to-RCY]
            F5[Loop: Cherry-pick<br/>each commit to new branch]
            F6{All commits<br/>succeeded?}
            F7[Push new branch]
            F8[Create draft PR<br/>to RC branch]
            F9[Set outputs:<br/>- cherry_pick_branch<br/>- pr_number]
            F10[❌ Abort & exit 1]
        end
    end

    subgraph Result["✅ End Result"]
        G1[Draft PR created:<br/>cherry-pick-PRX → RC branch]
        G2[Outputs returned to caller]
    end

    A1 --> B
    A2 --> B
    B -->|Yes| C
    B -->|No| Z[Skip]
    C --> D
    D --> E1

    E1 --> E2
    E2 -->|Yes| E3
    E2 -->|No| E4
    E3 --> E5
    E4 --> E5
    E5 --> E6
    E6 -->|Yes| E7
    E6 -->|No, multiple| E9
    E6 -->|No, zero| E10
    E7 --> E8
    E9 --> Z
    E10 --> Z

    E8 --> F1
    F1 -->|no| F2
    F1 -->|yes| Z
    F2 --> F3
    F3 --> F4
    F4 --> F5
    F5 --> F6
    F6 -->|Yes| F7
    F6 -->|No| F10
    F7 --> F8
    F8 --> F9
    F10 --> Z

    F9 --> G1
    F9 --> G2

    style Trigger fill:#e1f5ff
    style Caller fill:#fff4e1
    style Reusable fill:#e8f5e9
    style Result fill:#f3e5f5
    style E9 fill:#ffcdd2
    style E10 fill:#fff9c4
    style F10 fill:#ffcdd2
```

## Troubleshooting

### The workflow didn't trigger after merging my PR
- Verify the PR was merged to `main`, not just closed
- Check that the PR has exactly one allowed label
- Ensure the label exists in your `allowed_labels` list

### Cherry-pick failed with conflicts
- The workflow will create a failed draft PR
- Resolve conflicts manually on the cherry-pick branch
- Push your changes to update the PR

### "Multiple cherry-pick labels found..." error
- Only one cherry-pick label is allowed per PR
- Remove extra labels and re-run via workflow_dispatch
