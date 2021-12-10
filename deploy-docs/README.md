# deploy-docs

This action deploys [MkDocs](https://www.mkdocs.org/) documentation by [mike](https://github.com/jimporter/mike).  
When used for pull requests, it finds the files changed and adds a comment that includes the URLs to the files.

## Usage

```yaml
jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Get docs version name
        id: get-docs-version-name
        uses: autowarefoundation/autoware-github-actions/get-docs-version-name@tier4/proposal

      - name: Deploy docs
        uses: autowarefoundation/autoware-github-actions/deploy-docs@tier4/proposal
        with:
          version-name: ${{ steps.get-docs-version-name.outputs.version-name }}
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name         | Required | Description                              |
| ------------ | -------- | ---------------------------------------- |
| version-name | true     | The version name of the docs for `mike`. |
| token        | true     | The token used for `git push`.           |

## Outputs

None.
