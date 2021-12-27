# clang-tidy

This action analyzes code using Clang-Tidy.
This workflow depends on `colcon-build-and-test` action.

## Usage

```yaml
jobs:
  clang-tidy:
    runs-on: ubuntu-latest
    container: ros:galactic
    needs: build-and-test
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@tier4/proposal

      - name: Run clang-tidy
        if: ${{ steps.get-modified-packages.outputs.modified-packages != '' }}
        uses: autowarefoundation/autoware-github-actions/clang-tidy@tier4/proposal
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          clang-tidy-config-url: https://raw.githubusercontent.com/autowarefoundation/autoware/tier4/proposal/.clang-tidy
          build-depends-repos: build_depends.repos
```

## Inputs

| Name                  | Required | Description                                         |
| --------------------- | -------- | --------------------------------------------------- |
| rosdistro             | true     | ROS distro.                                         |
| target-packages       | true     | The target packages to analyse by Clang-Tidy.       |
| clang-tidy-config-url | true     | The URL to `.clang-tidy`.                           |
| build-depends-repos   | false    | `.repos` file that includes build dependencies.     |
| token                 | false    | The token for build dependencies and `.clang-tidy`. |

## Outputs

None.
