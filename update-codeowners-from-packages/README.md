# update-codeowners-from-packages

## Description

This action updates the `CODEOWNERS` file from ROS packages and codeowners.yaml.
It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests.

Note that you need `workflow` permission for the token if you copy workflow files of GitHub Actions.

## Usage

```yaml
jobs:
  update-codeowners-from-packages:
    runs-on: ubuntu-latest
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
| codeowners-group  | false    | The path to the group definition.                     |
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

## File format

codeowners.yaml

```yaml
users:
  - "@user-name"
  - "email.address@example.com"
groups:
  - "group-name"
```

codeowners-group.yaml

```yaml
group-name:
  - user-name-1
  - user-name-2
  - user-name-3
```
