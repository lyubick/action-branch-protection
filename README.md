# Modify Branch Protection Rules

## Overview
This action can modify specified branch protection rules. Currently supported:
 - Lock/unlock specific branch

## Usage
To use action one can use code snippet below.
```yaml
jobs:
  my_cool_locker:
    runs-on: ubuntu-latest
    steps:
      - name: Lock branch
        with:
          access-token: access_token_here
          repository-name: owner/repository
          branch-name: cool_branch
          lock: true
      - name: Unlock branch
        uses: lyubick/action-branch-protection@v1
        with:
          access-token: access_token_here
          repository-name: owner/repository
          branch-name: cool_branch
          lock: false
```
One should provide following parameters:
- `access-token`, required, should be a valid GitHub access token, classic or fine-grained. For fine-grained token
one should use `Repository permissions -> Administration -> Read and Write`.
- `repository-name`, required, specify one's repository in a format `owner/repo`. One can use GitHub predefined variables
to get current repository `${{ github.repository }}`.
- `branch-name`, required, specify one's branch.
- `lock`, required, `true` if one wants to lock the branch and `false` otherwise.
