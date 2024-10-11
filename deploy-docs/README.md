# deploy-docs

This action deploys [MkDocs](https://www.mkdocs.org/) documentation by [mike](https://github.com/jimporter/mike).  
When it is used for pull requests, it finds the files changed and adds a comment that includes the URLs to the files.
Note that this workflow installs the limited number of plugins that are used in [Autoware](https://github.com/autowarefoundation/autoware).

## Usage

```yaml
jobs:
  deploy-docs:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Deploy docs
        uses: autowarefoundation/autoware-github-actions/deploy-docs@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          latest: ${{ github.ref_name == github.event.repository.default_branch }}
```

## Inputs

| Name                    | Required | Description                           |
| ----------------------- | -------- | ------------------------------------- |
| token                   | true     | The token for push to `gh-pages`.     |
| latest                  | true     | Whether to create the `latest` alias. |
| mkdocs-requirements-txt | false    | `requirements.txt` for MkDocs         |

## Outputs

None.
