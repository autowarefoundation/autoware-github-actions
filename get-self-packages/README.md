# get-self-packages

This action gets the list of ROS packages in the repository.

## Usage

```yaml
jobs:
  get-self-packages:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Get self packages
        id: get-self-packages
        uses: autowarefoundation/autoware-github-actions/get-self-packages@v1
```

## Inputs

None.

## Outputs

| Name          | Description                                 |
| ------------- | ------------------------------------------- |
| self-packages | The list of ROS packages in the repository. |
