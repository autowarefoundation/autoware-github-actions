# pre-commit

This action checks if the PR passes [pre-commit](https://pre-commit.com/).  
For public repositories, using [pre-commit.ci](https://pre-commit.ci/) is recommended.  
Considering the case that you have both `.pre-commit-config.yaml` and `.pre-commit-config-optional.yaml`, this workflow takes the path to the config file.

## Usage

```yaml
jobs:
  remove-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Run pre-commit
        uses: autowarefoundation/autoware-github-actions/pre-commit@tier4/proposal
        with:
          pre-commit-config: .pre-commit-config.yaml
```

## Inputs

| Name              | Required | Description                            |
| ----------------- | -------- | -------------------------------------- |
| pre-commit-config | true     | The path to `.pre-commit-config.yaml`. |
| token             | false    | The token for auto-fix.                |

> Note: Setting `GITHUB_TOKEN` for `token` doesn't work completely because it doesn't have `workflow` permission.

## Outputs

None.
