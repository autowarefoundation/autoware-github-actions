# autoware-github-actions

This repository contains [Reusable Workflows](https://docs.github.com/ja/actions/learn-github-actions/reusing-workflows) and [Composite Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions) for [Autoware](https://github.com/autowarefoundation/autoware).

## Supported reusable workflows

### [check-secret](.github/workflows/check-secret.yaml)

This workflow checks if a certain secret is set.

#### Usage

```yaml
jobs:
  check-secret:
    uses: autowarefoundation/autoware-github-actions/.github/workflows/check-secret.yaml@v1
    secrets:
      secret: ${{ secrets.APP_ID }}

  sync-files:
    needs: check-secret
    if: ${{ needs.check-secret.outputs.set == 'true' }}
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}
```

### [prevent-no-label-execution](.github/workflows/prevent-no-label-execution.yaml)

This workflow checks if the PR has a specific label.  
It is useful for preventing `pull_request_target` event and self-hosted runners from being executed without the label.

#### Usage

```yaml
jobs:
  prevent-no-label-execution:
    uses: autowarefoundation/autoware-github-actions/.github/workflows/prevent-no-label-execution.yaml@v1
    with:
      label: ARM64

  build-and-test-arm:
    needs: prevent-no-label-execution
    if: ${{ needs.prevent-no-label-execution.outputs.run == 'true' }}
    runs-on: [self-hosted, linux, ARM64]
    # ...
```

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
    uses: autowarefoundation/autoware-github-actions/.github/workflows/semantic-pull-request.yaml@v1
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

## Supported composite actions

See the `README.md` in each directory.

- [clang-tidy](./clang-tidy/README.md)
- [colcon-build](./colcon-build/README.md)
- [colcon-test](./colcon-test/README.md)
- [delete-closed-pr-docs](./delete-closed-pr-docs/README.md)
- [deploy-docs](./deploy-docs/README.md)
- [generate-changelog](./generate-changelog/README.md)
- [get-modified-packages](./get-modified-packages/README.md)
- [get-self-packages](./get-self-packages/README.md)
- [json-schema-check](./json-schema-check/README.md)
- [pre-commit](./pre-commit/README.md)
- [register-autonomoustuff-repository](./register-autonomoustuff-repository/README.md)
- [remove-exec-depend](./remove-exec-depend/README.md)
- [set-git-config](./set-git-config/README.md)
- [spell-check](./spell-check/README.md)
- [sync-branches](./sync-branches/README.md)
- [sync-files](./sync-files/README.md)
- [update-codeowners-from-packages](./update-codeowners-from-packages/README.md)
