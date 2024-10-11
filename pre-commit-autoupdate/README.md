# pre-commit-autoupdate

This action updates the versions of pre-commit hooks.

It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests.

## Usage

```yaml
jobs:
  sync-files:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Run pre-commit-autoupdate
        uses: autowarefoundation/autoware-github-actions/pre-commit-autoupdate@v1
        with:
          token: ${{ steps.generate-token.outputs.token }}
          pre-commit-config: .pre-commit-config.yaml
          auto-merge-method: squash
```

## Inputs

| Name              | Required | Description                                           |
| ----------------- | -------- | ----------------------------------------------------- |
| token             | true     | The token for pull requests.                          |
| pre-commit-config | true     | The path to `.pre-commit-config.yaml`.                |
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
