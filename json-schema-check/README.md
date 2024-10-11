# json-schema-check

## Description

This action checks if the ROS 2 parameter files (`config/*.param.yaml`) of packages comply with the format of their template JSON Schema file (`schema/*.schema.json`).

## Usage

```yaml
jobs:
  json-schema-check:
    runs-on: ubuntu-22.04
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Run json-schema-check
        uses: autowarefoundation/autoware-github-actions/json-schema-check@v1
```

## Inputs

None.

## Outputs

None.
