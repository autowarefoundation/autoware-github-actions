# colcon-build-and-test

## Inputs

| Name                | Required | Description                                     |
| ------------------- | -------- | ----------------------------------------------- |
| rosdistro           | true     | ROS distro.                                     |
| build-depends-repos | true     | VCS repositories containing build dependencies. |
| target-packages     | true     | Target packages to build and test.              |
| token               | false    | If the repository is private, specify a token.  |

## Outputs

| Name                  | Description                               |
| --------------------- | ----------------------------------------- |
| compile-commands-hash | Calculated hash of compile_commands.json. |

## Sample Workflow Steps

```yaml
- name: Build and test
  id: build-and-test
  uses: autowarefoundation/autoware-github-actions/colcon-build-and-test@@tier4/proposal
  with:
    rosdistro: galactic
    build-depends-repos: build_depends.repos
    target-packages: ${{ steps.get-modified-packages.outputs.modified-packages }}
```
