# build-docs-preview

This action builds the [MkDocs](https://www.mkdocs.org/) site of a pull request and uploads it as an artifact.
It runs the code of the pull request, so use it only in a job with a read-only token and no secrets.
The [publish-docs-preview](../publish-docs-preview/README.md) action then publishes the site in a separate workflow.

The site is a plain `mkdocs build`, without [mike](https://github.com/jimporter/mike), so the preview has no version selector.

## Usage

Name the workflow `build-docs-preview`, because the publish workflow starts after a workflow with this name.

```yaml
name: build-docs-preview

on:
  pull_request:

permissions: {}

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  build-docs-preview:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Check out repository
        uses: actions/checkout@v7
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false

      - name: Build docs preview
        uses: autowarefoundation/autoware-github-actions/build-docs-preview@v1
        with:
          mkdocs-requirements-txt: mkdocs-requirements.txt
```

## Inputs

| Name                    | Required | Description                                                                         |
| ----------------------- | -------- | ----------------------------------------------------------------------------------- |
| mkdocs-requirements-txt | false    | `requirements.txt` for MkDocs. The default is the file of the `deploy-docs` action. |
| artifact-name           | false    | The name of the artifact. The default is `docs-preview`.                            |

## Outputs

None.
