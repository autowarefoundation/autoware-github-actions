# colcon-build-and-test

This action runs `colcon build` and `colcon test`.

## Usage

```yaml
jobs:
  colcon-build-and-test:
    runs-on: ubuntu-latest
    container: ros:galactic
    outputs:
      compile-commands-hash: ${{ steps.build-and-test.outputs.compile-commands-hash }}
    steps:
      - name: Get modified packages
        id: get-modified-packages
        uses: autowarefoundation/autoware-github-actions/get-modified-packages@tier4/proposal

      - name: Build and test
        id: build-and-test
        uses: autowarefoundation/autoware-github-actions/colcon-build-and-test@tier4/proposal
        with:
          rosdistro: galactic
          target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
          build-depends-repos: build_depends.repos
```

## Inputs

| Name                | Required | Description                                     |
| ------------------- | -------- | ----------------------------------------------- |
| rosdistro           | true     | ROS distro.                                     |
| target-packages     | true     | The target packages to build and test.          |
| build-depends-repos | false    | `.repos` file that includes build dependencies. |
| token               | false    | The token for build dependencies.               |

## Outputs

None.
