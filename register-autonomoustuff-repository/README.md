# register-autonomoustuff-repository

This action sets up the prerequisites for [pacmod3_msgs](https://github.com/astuff/pacmod3_msgs), which is used in Autoware.

> Note: This action assumes the caller workflow has installed `rosdep`.

## Usage

```yaml
jobs:
  build:
    runs-on: ubuntu-22.04
    container: ros:galactic
    steps:
      - name: Check out repository
        uses: actions/checkout@v3

      - name: Register AutonomouStuff repository
        uses: autowarefoundation/autoware-github-actions/register-autonomoustuff-repository@v1
        with:
          rosdistro: galactic

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

| Name      | Required | Description     |
| --------- | -------- | --------------- |
| rosdistro | true     | The ROS distro. |

## Outputs

None.
