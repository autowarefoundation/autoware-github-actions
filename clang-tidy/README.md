# clang-tidy

This action analyzes code using Clang-Tidy.
This workflow depends on `colcon-build` action.

## Usage

```yaml
jobs:
  clang-tidy:
    runs-on: ubuntu-latest
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

| Name                   | Required | Description                                                                   |
| ---------------------- | -------- | ----------------------------------------------------------------------------- |
| rosdistro              | true     | The ROS distro.                                                               |
| clang-tidy-config-url  | true     | The URL to `.clang-tidy`.                                                     |
| clang-tidy-ignore-path | false    | Ignore file relative to `source-directory`. Defaults to `.clang-tidy-ignore`. |
| source-directory       | false    | Source checkout directory relative to the workspace. Defaults to `.`.         |
| target-packages        | true     | The target packages to analyze by Clang-Tidy.                                 |
| target-files           | false    | The target files, relative to `source-directory`.                             |
| build-depends-repos    | false    | The `.repos` file that includes build dependencies.                           |
| cmake-build-type       | false    | The value for `CMAKE_BUILD_TYPE`.                                             |
| token                  | false    | The token for build dependencies and `.clang-tidy`.                           |

## Outputs

None.

## Nested source checkouts

When the repository is checked out under `src/`, set `source-directory` to the checkout path:

```yaml
- uses: actions/checkout@v7
  with:
    path: src/${{ github.event.repository.name }}

- uses: autowarefoundation/autoware-github-actions/clang-tidy@v1
  with:
    rosdistro: jazzy
    target-packages: my_package
    source-directory: src/${{ github.event.repository.name }}
    clang-tidy-config-url: https://raw.githubusercontent.com/autowarefoundation/autoware/main/.clang-tidy-ci
```

Dependency installation and builds still run from `$GITHUB_WORKSPACE`, and the compilation database stays in `$GITHUB_WORKSPACE/build`. The action downloads `.clang-tidy` into the source directory and runs file discovery, ignore matching, and analysis there. Existing repository-relative ignore patterns keep their meaning without rewriting. The clang-tidy cache uses the downloaded configuration's hash.

When sharing a build cache with `colcon-build`, use the same `cache-key-element` in both actions for the same checkout layout. Use distinct values for different checkout layouts because cached build files contain source paths.
