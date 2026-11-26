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
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}
```

### [check-if-build-is-needed](.github/workflows/check-if-build-is-needed.yaml)

This workflow checks if a PR modifies a package or a build input.  
Use it with [require-label](.github/workflows/require-label.yaml), so that a PR with nothing to build, for example a CODEOWNERS sync PR, does not need the label.  
`package.xml` and the `COLCON_IGNORE`, `AMENT_IGNORE`, and `CATKIN_IGNORE` files are always build inputs. Give the other build inputs in `build-inputs`: the workflow file that calls this workflow, the workflows that it uses, and their local actions. Otherwise, a PR that changes only these files does not run the build without the label.  
Each line of `build-inputs` is a Git path pattern, not a GitHub Actions glob: `.github/actions` matches all files below that directory, and `*` also matches `/`. List only paths that exist in the repository: a line that matches no file gives a warning, because it can be a typo. A line that starts with `:` is an error.  
It accepts only the `pull_request` event.

Make `require-label / require-label` the required check of the branch. Do not require a job that is skipped at job level when `require-label` does not run:

- A skipped job passes a required check, so a required build job would also pass when `check-if-build-is-needed` fails.
- A skipped matrix job reports without its matrix suffix, for example `build-and-test-differential` and not `build-and-test-differential (humble)`, so a required matrix check stays missing and blocks the PR.

#### Usage

```yaml
jobs:
  check-if-build-is-needed:
    uses: autowarefoundation/autoware-github-actions/.github/workflows/check-if-build-is-needed.yaml@v1
    with:
      build-inputs: |
        .github/workflows/build-and-test-differential.yaml
        .github/actions

  require-label:
    # Without always() or !cancelled(), require-label does not run if check-if-build-is-needed fails,
    # and the required check stays missing.
    needs: check-if-build-is-needed
    uses: autowarefoundation/autoware-github-actions/.github/workflows/require-label.yaml@v1
    with:
      label: run:build-and-test-differential
      # Compare with 'false': with always() or !cancelled(), a check that did not finish gives an empty result,
      # and the PR must still need the label.
      # With the label, it runs anyway, so the label still starts the build, for example to test a CI change.
      run-condition: ${{ needs.check-if-build-is-needed.outputs.result != 'false' || contains(github.event.pull_request.labels.*.name, 'run:build-and-test-differential') }}

  build-and-test-differential:
    needs: require-label
    if: ${{ needs.require-label.outputs.result == 'true' }}
    runs-on: ubuntu-24.04
    # ...
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
