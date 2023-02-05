# set-cuda-path

This action set the cuda path into GITHUB_ENV amd GITHUB_PATH.

## Usage

```yaml
jobs:
  set-cuda-path:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Set cuda path
        id: set-cuda-path
        uses: autowarefoundation/autoware-github-actions/set-cuda-path@v1
```

## Inputs

None.

## Outputs

None.
