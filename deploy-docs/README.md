# deploy-docs

This action deploys [MkDocs](https://www.mkdocs.org/) documentation by [mike](https://github.com/jimporter/mike).  
When it is used for pull requests, it finds the files changed and adds a comment that includes the URLs to the files.
Note that this workflow installs the limited number of plugins that are used in [Autoware](https://github.com/autowarefoundation/autoware).

## Usage

```yaml
jobs:
  deploy-docs:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Deploy docs
        uses: autowarefoundation/autoware-github-actions/deploy-docs@tier4/proposal
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name  | Required | Description                       |
| ----- | -------- | --------------------------------- |
| token | true     | The token for push to `gh-pages`. |

## Outputs

None.
