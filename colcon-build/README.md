# colcon-build

This action runs `colcon build`.

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-22.04
    container: ros:galactic
    steps:
      - name: Check out repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@v1

      - name: Build
        if: ${{ steps.get-modified-packages.outputs.modified-packages != '' }}
        uses: autowarefoundation/autoware-github-actions/colcon-build@v1
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          build-depends-repos: build_depends.repos
          packages-above-repos: packages_above.repos
```

## Inputs

| Name                         | Required | Description                                                                                                             |
| ---------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| rosdistro                    | true     | ROS distro.                                                                                                             |
| target-packages              | true     | The target packages to build.                                                                                           |
| build-depends-repos          | false    | The `.repos` file that includes build dependencies.                                                                     |
| packages-above-repos         | false    | The `.repos` file that includes above build dependencies.                                                               |
| cmake-build-type             | false    | The value for `CMAKE_BUILD_TYPE`.                                                                                       |
| token                        | false    | The token for build dependencies.                                                                                       |
| include-eol-distros          | false    | If true, adds `--include-eol-distros` to `rosdep update`.                                                               |
| cache-key-element            | false    | This value is added to the github actions cache key.                                                                    |
| build-pre-command            | false    | This command is prepended to the `colcon build` to avoid draining resources.                                            |
| colcon-parallel-workers-flag | false    | Will be appended to the colcon build command to limit number of packages built in parallel. e.g. "--parallel-workers 3" |
| makeflags                    | false    | Will be exported as MAKEFLAGS environment variable for colcon build step. e.g. "-j 4"                                   |

## Outputs

None.
