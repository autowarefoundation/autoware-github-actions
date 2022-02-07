# colcon-test

This action runs `colcon test` with label.
Note that you need to build target packages before running this action.

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container: ros:galactic
    steps:
      - name: Check out repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@tier4/proposal

      - name: Build
        if: ${{ steps.get-modified-packages.outputs.modified-packages != '' }}
        uses: autowarefoundation/autoware-github-actions/colcon-build@tier4/proposal
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          build-depends-repos: build_depends.repos

  test:
    needs: build
    runs-on: ubuntu-latest
    container: ros:galactic
    strategy:
      matrix:
        label: [gtest, launch_test]
    steps:
      - name: Check out repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@tier4/proposal

      - name: Test
        id: test
        if: ${{ steps.get-modified-packages.outputs.modified-packages != '' }}
        uses: autowarefoundation/autoware-github-actions/colcon-test@tier4/proposal
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          build-depends-repos: build_depends.repos
          label: ${{ matrix.label }}

      - name: Upload coverage to Codecov
        if: ${{ steps.test.outputs.coverage-reports != '' }}
        uses: codecov/codecov-action@v2
        with:
          files: ${{ steps.test.outputs.coverage-reports }}
          fail_ci_if_error: true
          verbose: true
          flags: ${{ matrix.label }}
```

## Inputs

| Name                | Required | Description                                     |
| ------------------- | -------- | ----------------------------------------------- |
| rosdistro           | true     | ROS distro.                                     |
| target-packages     | true     | The target packages to test.                    |
| build-depends-repos | false    | `.repos` file that includes build dependencies. |
| label               | false    | Specify test label for test.                    |
| token               | false    | The token for build dependencies.               |

## Outputs

| Name             | Description                 |
| ---------------- | --------------------------- |
| coverage-reports | Generated coverage reports. |
