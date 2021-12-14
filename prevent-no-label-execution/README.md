# prevent-no-label-execution

## Description

This action checks if the PR has a specific label.  
It is useful for preventing `pull_request_target` event and self-hosted runners from being executed without the label.

## Usage

```yaml
jobs:
  prevent-no-label-execution:
    runs-on: ubuntu-latest
    steps:
      - name: Prevent no label execution
        uses: autowarefoundation/autoware-github-actions/prevent-no-label-execution@tier4/proposal
        with:
          label: ARM64

  build-and-test-arm:
    needs: check-run-condition
    if: ${{ needs.check-run-condition.outputs.run == 'true' }}
    runs-on: [self-hosted, linux, ARM64]
    # ...
```

## Inputs

| Name  | Required | Description         |
| ----- | -------- | ------------------- |
| label | true     | The label to check. |

## Outputs

| Name | Description                |
| ---- | -------------------------- |
| run  | Whether to run the action. |
