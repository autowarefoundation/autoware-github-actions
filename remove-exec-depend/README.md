# remove-exec-depend

This action removes `<exec_depend>` from `package.xml`.  
Refer to [here](https://github.com/autowarefoundation/autoware.universe/issues/184#issuecomment-993620219) for more details.

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-22.04
    container: ros:galactic
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Remove exec_depend
        uses: autowarefoundation/autoware-github-actions/remove-exec-depend@v1

      - name: Get self packages
        id: get-self-packages
        uses: autowarefoundation/autoware-github-actions/get-self-packages@v1

      - name: Build
        uses: autowarefoundation/autoware-github-actions/colcon-build@v1
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-self-packages.outputs.self-packages }}
          build-depends-repos: build_depends.repos
```

## Inputs

None.

## Outputs

None.
