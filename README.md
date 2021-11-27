# autoware-github-actions

This is one of the prototype repositories for Autoware Core/Universe that AWF agreed to create in the [TSC meeting on 2021/11/17](https://discourse.ros.org/t/technical-steering-committee-tsc-meeting-36-2021-11-17-minutes/23168).

Please see [autowarefoundation/autoware](https://github.com/autowarefoundation/autoware) for more details.

---

This repository contains [Reusable Workflows](https://docs.github.com/ja/actions/learn-github-actions/reusing-workflows) for [Autoware](https://github.com/autowarefoundation/autoware).

## Usage

Call reusable workflows from your workflow like this.  
Please change `{workflow}` and `{version}` based on your task.

```yaml
name: your-workflow

on:
  pull_request:

jobs:
  reusable-workflow:
    uses: kenji-miyake/github-actions/.github/workflows/{workflow}.yaml@{version}
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

## Supported actions

### [reusable-clang-tidy.yaml](.github/workflows/reusable-clang-tidy.yaml)

Analyze code using Clang-Tidy.
This workflow depends on `reusable-colcon-build-and-test.yaml`.

### [reusable-colcon-build-and-test.yaml](.github/workflows/reusable-colcon-build-and-test.yaml)

Setup workspace, build, and run tests.

### [reusable-generate-docs.yaml](.github/workflows/reusable-generate-docs.yaml)

Generate [MkDocs](https://www.mkdocs.org/) documentation.
When used for pull requests, it finds the files changed and adds a comment that includes the URLs to the files.
Note that this workflow installs the limited number of plugins that are used in [Autoware](https://github.com/autowarefoundation/autoware).

### [reusable-get-docs-version-name.yaml](.github/workflows/reusable-get-docs-version-name.yaml)

Get document version based on the branch name or the PR number.

### [reusable-get-modified-packages.yaml](.github/workflows/reusable-get-modified-packages.yaml)

Get ROS packages modified in the pull request.

### [reusable-get-modified-source-files.yaml](.github/workflows/reusable-get-modified-source-files.yaml)

Get source files (.cpp/.hpp) modified in the pull request.

### [reusable-get-self-packages.yaml](.github/workflows/reusable-get-self-packages.yaml)

Get ROS packages in the repository.

### [reusable-pre-commit.yaml](.github/workflows/reusable-pre-commit.yaml)

Check if the PR passes [pre-commit](https://pre-commit.com/).  
For public repositories, using [pre-commit.ci](https://pre-commit.ci/) is recommended.  
Considering the case that you have both `.pre-commit-config.yaml` and `.pre-commit-config-optional.yaml`, this workflow takes the path to the config file.

### [reusable-remove-docs.yaml](.github/workflows/reusable-remove-docs.yaml)

Remove documents added by `reusable-generate-docs.yaml`.

### [reusable-semantic-pull-request.yaml](.github/workflows/reusable-semantic-pull-request.yaml)

Check if the PR title complies with [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).  
The settings are based on [commitizen/conventional-commit-types](https://github.com/commitizen/conventional-commit-types).  
This just wraps [amannn/action-semantic-pull-request](https://github.com/amannn/action-semantic-pull-request).

### [reusable-spell-check.yaml](.github/workflows/reusable-spell-check.yaml)

Check if the PR has miss spellings.  
As it is difficult to perfectly detect all miss spellings, it is recommended not to set this as [Required](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/troubleshooting-required-status-checks).
