# sync-branches

## Description

This action syncs branches including remote repositories.  
It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests.

Note that you need `workflow` permission for the token if you copy workflow files of GitHub Actions.

## Usage

```yaml
jobs:
  sync-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Run sync-branches
        uses: autowarefoundation/autoware-github-actions/sync-branches@v1
        with:
          token: ${{ steps.generate-token.outputs.token }}
          base-branch: main
          sync-target-repository: https://github.com/autowarefoundation/autoware.git
          sync-target-branch: main
          sync-branch: sync-upstream
          pr-title: "chore: sync upstream"
          pr-body-header: "This PR syncs changes from the upstream repository."
          auto-merge-method: merge
```

## Inputs

| Name                   | Required | Description                                             |
| ---------------------- | -------- | ------------------------------------------------------- |
| token                  | true     | The token for pull requests.                            |
| base-branch            | true     | The base branch of the sync PR.                         |
| base-repo              | false    | The base repository. Default is the current repository. |
| sync-pr-branch         | true     | The branch of the sync PR .                             |
| sync-target-repository | true     | The sync target repository.                             |
| sync-target-branch     | true     | The sync target branch.                                 |
| pr-title               | true     | Refer to `peter-evans/create-pull-request`.             |
| pr-labels              | false    | The same as above.                                      |
| pr-assignees           | false    | The same as above.                                      |
| pr-reviewers           | false    | The same as above.                                      |
| auto-merge-method      | false    | Refer to `peter-evans/enable-pull-request-automerge`.   |
| pr-body-header         | false    | Text to prepend before the changelog in PR body.        |

## Outputs

| Name             | Description                      |
| ---------------- | -------------------------------- |
| pull-request-url | URL of the created pull request. |
