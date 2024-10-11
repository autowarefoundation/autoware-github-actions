# update-codeowners-from-packages

## Description

This action updates the `CODEOWNERS` file from ROS packages.  
It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests.

Note that you need `workflow` permission for the token if you copy workflow files of GitHub Actions.

## Usage

```yaml
jobs:
  update-codeowners-from-packages:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Run update-codeowners-from-packages
        uses: autowarefoundation/autoware-github-actions/update-codeowners-from-packages@v1
        with:
          token: ${{ steps.generate-token.outputs.token }}
          auto-merge-method: squash
```

If you want to combine the automatically generated `CODEOWNERS` with the manually maintained `CODEOWNERS`, create a file such as `.github/CODEOWNERS-manual`.

## Inputs

| Name              | Required | Description                                           |
| ----------------- | -------- | ----------------------------------------------------- |
| token             | true     | The token for pull requests.                          |
| codeowners-manual | false    | The path to the manually maintained `CODEOWNERS`.     |
| global-codeowners | false    | The GitHub IDs of global codeowners.                  |
| pr-base           | false    | Refer to `peter-evans/create-pull-request`.           |
| pr-branch         | false    | The same as above.                                    |
| pr-title          | false    | The same as above.                                    |
| pr-commit-message | false    | The same as above.                                    |
| pr-labels         | false    | The same as above.                                    |
| pr-assignees      | false    | The same as above.                                    |
| pr-reviewers      | false    | The same as above.                                    |
| auto-merge-method | false    | Refer to `peter-evans/enable-pull-request-automerge`. |

## Outputs

None.
