# remove-docs

## Inputs

| Name         | Required | Description                                    |
| ------------ | -------- | ---------------------------------------------- |
| version-name | true     | Version name to remove from the documentation. |
| token        | true     | If the repository is private, specify a token. |

## Sample Workflow Steps

```yaml
- name: Remove docs
  uses: autowarefoundation/autoware-github-actions/remove-docs@@tier4/proposal
  with:
    version-name: ${{ needs.get-docs-version-name.outputs.version-name }}
    token: ${{ secrets.GITHUB_TOKEN }}
```
