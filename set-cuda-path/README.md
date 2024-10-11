# set-cuda-path

This action set the CUDA path into GITHUB_ENV amd GITHUB_PATH.

## Usage

```yaml
jobs:
  set-cuda-path:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Set CUDA path
        id: set-cuda-path
        uses: autowarefoundation/autoware-github-actions/set-cuda-path@v1
```

## Inputs

None.

## Outputs

None.
