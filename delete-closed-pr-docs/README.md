# delete-closed-pr-docs

This action deletes documents of closed pull requests deployed by `deploy-docs` action.

## Usage

```yaml
jobs:
  delete-closed-pr-docs:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Delete closed PR docs
          uses: autowarefoundation/autoware-github-actions/delete-closed-pr-docs@v1
          with:
            token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name  | Required | Description                       |
| ----- | -------- | --------------------------------- |
| token | true     | The token for push to `gh-pages`. |

## Outputs

None.
