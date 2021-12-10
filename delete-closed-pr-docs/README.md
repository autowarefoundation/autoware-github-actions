# delete-closed-pr-docs

This action deletes documents of closed pull requests deployed by `deploy-docs` action.

## Usage

```yaml
jobs:
  delete-closed-pr-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Delete closed PR docs
        uses: autowarefoundation/autoware-github-actions/delete-closed-pr-docs@tier4/proposal
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name  | Required | Description               |
| ----- | -------- | ------------------------- |
| token | true     | The token for `gh-pages`. |

## Outputs

None.