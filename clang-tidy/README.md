# clang-tidy

This action analyzes code using Clang-Tidy.
This workflow depends on `colcon-build` action.

## Usage

```yaml
jobs:
  clang-tidy:
    runs-on: ubuntu-22.04
    container: ros:galactic
    needs: build-and-test
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@v1

      - name: Run clang-tidy
        if: ${{ steps.get-modified-packages.outputs.modified-packages != '' }}
        uses: autowarefoundation/autoware-github-actions/clang-tidy@v1
        with:
          rosdistro: galactic
          clang-tidy-config-url: https://raw.githubusercontent.com/autowarefoundation/autoware/main/.clang-tidy
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          build-depends-repos: build_depends.repos
```

## Inputs

| Name                  | Required | Description                                         |
| --------------------- | -------- | --------------------------------------------------- |
| rosdistro             | true     | The ROS distro.                                     |
| clang-tidy-config-url | true     | The URL to `.clang-tidy`.                           |
| target-packages       | true     | The target packages to analyze by Clang-Tidy.       |
| target-files          | false    | The target files.                                   |
| build-depends-repos   | false    | The `.repos` file that includes build dependencies. |
| cmake-build-type      | false    | The value for `CMAKE_BUILD_TYPE`.                   |
| token                 | false    | The token for build dependencies and `.clang-tidy`. |

## Outputs

None.
