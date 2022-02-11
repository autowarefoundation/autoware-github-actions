# spell-check

## Description

This action checks if the PR has miss spellings.  
As it is difficult to perfectly detect all miss spellings, it is recommended not to set this as [Required](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks).

## Usage

```yaml
jobs:
  spell-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v2

      - name: Run spell-check
        uses: autowarefoundation/autoware-github-actions/spell-check@tier4/proposal
        with:
          cspell-json-url: https://raw.githubusercontent.com/tier4/autoware-spell-check-dict/main/.cspell.json
```

## Inputs

| Name            | Required | Description                   |
| --------------- | -------- | ----------------------------- |
| cspell-json-url | true     | The URL to `.cspell.json`.    |
| token           | false    | The token for `.cspell.json`. |

## Outputs

None.
