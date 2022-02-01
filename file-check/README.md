# check-file-existence

## Description

This action checks if the specified files exist.

## Usage

```yaml
jobs:
  file-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check file existence
        id: check-file-existence
        uses: autowarefoundation/autoware-github-actions/file-check@tier4/proposal
        with:
          files: README.yaml,LICENSE
          condition: or

      - name: Check result
        if: steps.file-check.outputs.exists == 'true'
        # Only executed if one of the files exists
        run: echo One of the files exists.
```

## Inputs

| Name      | Required | Description                                                                                                  |
| --------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| files     | true     | Comma-separated file names.                                                                                  |
| condition | true     | Set to `and` or`or`. If more than one file is specified, this condition determines whether to report `true`. |

## Outputs

| Name   | Description                                                                         |
| ------ | ----------------------------------------------------------------------------------- |
| exists | If the file exists, it will be set to `true`. Otherwise, it will be set to `false`. |
