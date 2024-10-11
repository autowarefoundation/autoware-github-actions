# pre-commit

This action checks if the PR passes [pre-commit](https://pre-commit.com/).  
For public repositories, using [pre-commit.ci](https://pre-commit.ci/) is recommended.  
Considering the case that you have both `.pre-commit-config.yaml` and `.pre-commit-config-optional.yaml`, this workflow takes the path to the config file.

## Usage

```yaml
jobs:
  pre-commit:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Check out repository
        uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.ref }}

      - name: Run pre-commit
        uses: autowarefoundation/autoware-github-actions/pre-commit@v1
        with:
          pre-commit-config: .pre-commit-config.yaml
          token: ${{ steps.generate-token.outputs.token }}
```

## Inputs

| Name              | Required | Description                                                             |
| ----------------- | -------- | ----------------------------------------------------------------------- |
| pre-commit-config | true     | The path to `.pre-commit-config.yaml`.                                  |
| base-branch       | false    | The base branch to search for modified files. Check all files if empty. |
| token             | false    | The token for auto-fix.                                                 |

> Note: Setting `GITHUB_TOKEN` for `token` doesn't work completely because it doesn't have `workflow` permission.

## Outputs

None.
