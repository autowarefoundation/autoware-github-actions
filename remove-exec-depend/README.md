# remove-exec-depend

This action removes `<exec_depend>` from `package.xml`.  
Please see [here](https://github.com/autowarefoundation/autoware.universe/issues/184#issuecomment-993620219) for more details.

## Usage

```yaml
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    container: ros:galactic
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Remove exec_depend
        uses: autowarefoundation/autoware-github-actions/remove-exec-depend@tier4/proposal

      - name: Get self packages
        id: get-self-packages
        uses: autowarefoundation/autoware-github-actions/get-self-packages@tier4/proposal

      - name: Build and test
        uses: autowarefoundation/autoware-github-actions/colcon-build-and-test@tier4/proposal
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-self-packages.outputs.self-packages }}
          build-depends-repos: build_depends.repos
```

## Inputs

None.

## Outputs

None.
