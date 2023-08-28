# generate-changelog

## Description

This action generates the changelog using [git-cliff](https://github.com/orhun/git-cliff).

## Usage

```yaml
jobs:
  generate-changelog:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Run generate-changelog
        id: generate-changelog
        uses: autowarefoundation/autoware-github-actions/generate-changelog@v1

      - name: Show result
        run: |
          echo "$CHANGELOG"
        env:
          CHANGELOG: ${{ steps.generate-changelog.outputs.changelog }}
```

## Inputs

| Name                  | Required | Description                                              |
| --------------------- | -------- | -------------------------------------------------------- |
| git-cliff-args        | false    | The arguments for the `git-cliff` command.               |
| git-cliff-config      | false    | The path to the `git-cliff` config file.                 |
| trim-version-and-date | false    | Whether to trim the version and date from the changelog. |
| save-json-output      | false    | Save the output contents to artifact in json format.     |

## Outputs

| Name      | Description              |
| --------- | ------------------------ |
| changelog | The generated changelog. |
