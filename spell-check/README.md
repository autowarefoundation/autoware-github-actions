# spell-check

## Description

This action checks if the PR has miss spellings.  
As it is difficult to perfectly detect all miss spellings, it is recommended not to set this as [Required](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks).

## Usage

```yaml
jobs:
  spell-check:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Run spell-check
        uses: autowarefoundation/autoware-github-actions/spell-check@v1
        with:
          cspell-json-url: https://raw.githubusercontent.com/autowarefoundation/autoware-spell-check-dict/main/.cspell.json
          local-cspell-json: .cspell.json
          dict-packages: |
            https://github.com/tier4/cspell-dicts
          incremental-files-only: false
```

## Inputs

| Name                   | Required | Description                                                      |
| ---------------------- | -------- | ---------------------------------------------------------------- |
| cspell-json-url        | true     | The URL to the remote `.cspell.json`.                            |
| local-cspell-json      | false    | The path to the local `.cspell.json`.                            |
| dict-packages          | false    | The dict packages names referenced in `.cspell.json`.            |
| token                  | false    | The token for the remote `.cspell.json`.                         |
| incremental-files-only | false    | Limit the files checked to the ones in the pull request or push. |

## Outputs

None.
