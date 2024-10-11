# check-file-existence

## Description

This action checks if the specified files exist.

## Usage

```yaml
jobs:
  check-file-existence:
    runs-on: ubuntu-22.04
    steps:
      - name: Check file existence
        id: check-file-existence
        uses: autowarefoundation/autoware-github-actions/check-file-existence@v1
        with:
          files: |
            README.md
            LICENSE
          condition: or

      - name: Check result
        if: ${{ steps.check-file-existence.outputs.exists == 'true' }}
        run: echo "exists"
```

## Inputs

| Name      | Required | Description                                           |
| --------- | -------- | ----------------------------------------------------- |
| files     | true     | The file names to check the existence.                |
| condition | false    | The `and` or `or` condition for file existence check. |

## Outputs

| Name   | Description                               |
| ------ | ----------------------------------------- |
| exists | Whether the specified files exist or not. |
