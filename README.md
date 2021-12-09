# autoware-github-actions

This is one of the prototype repositories for Autoware Core/Universe that AWF agreed to create in the [TSC meeting on 2021/11/17](https://discourse.ros.org/t/technical-steering-committee-tsc-meeting-36-2021-11-17-minutes/23168).

Please see [autowarefoundation/autoware](https://github.com/autowarefoundation/autoware) for more details.

---

This repository contains [Reusable Workflows](https://docs.github.com/ja/actions/learn-github-actions/reusing-workflows) and [Composite Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions) for [Autoware](https://github.com/autowarefoundation/autoware).

## Supported reusable workflows

### [semantic-pull-request](.github/workflows/semantic-pull-request.yaml)

This workflow checks if the PR title complies with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  
The settings are based on [commitizen/conventional-commit-types](https://github.com/commitizen/conventional-commit-types).  
This just wraps [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request).

#### Usage

```yaml
name: semantic-pull-request

on:
  pull_request_target:
    types:
      - opened
      - edited
      - synchronize

jobs:
  semantic-pull-request:
    uses: autowarefoundation/autoware-github-actions/.github/workflows/semantic-pull-request.yaml@tier4/proposal
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

## Supported composite actions

Please see the `README.md` in each directory.

- [clang-tidy](./clang-tidy/README.md)
- [colcon-build-and-test](./colcon-build-and-test/README.md)
- [delete-closed-pr-docs](./delete-closed-pr-docs/README.md)
- [deploy-docs](./deploy-docs/README.md)
- [get-modified-packages](./get-modified-packages/README.md)
- [get-self-packages](./get-self-packages/README.md)
- [pre-commit](./pre-commit/README.md)
- [register-autonomoustuff-repository](./register-autonomoustuff-repository/README.md)
- [spell-check](./spell-check/README.md)
