# get-modified-packages

This action get the list of ROS packages modified in the pull request.

## Usage

```yaml
jobs:
  get-modified-packages:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@tier4/proposal
```

## Inputs

None.

## Outputs

| Name              | Description                                           |
| ----------------- | ----------------------------------------------------- |
| modified-packages | The list of ROS packages modified in the pull request |
