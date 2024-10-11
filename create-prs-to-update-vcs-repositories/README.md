# create-prs-to-update-vcs-repositories

## Description

This action creates pull requests to update the vcs repositories in the autoware repository.

## Initial setup (within `autowarefoundation` org)

This action uses the <https://github.com/apps/awf-autoware-bot> app to create pull requests.

### Secrets

For this action to use this bot, it requires the following secrets:

- `APP_ID`: The app ID of the bot.
- `PRIVATE_KEY`: The private key of the bot.

These secrets are already set if inside of the autoware repository.

## Usage

```yaml
jobs:
  sync-files:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Run
        uses: autowarefoundation/autoware-github-actions/create-prs-to-update-vcs-repositories@v1
        with:
          token: ${{ steps.generate-token.outputs.token }}
          repo_name: autowarefoundation/autoware
          parent_dir: .
          targets: major minor
          base_branch: main
          new_branch_prefix: feat/update-
          autoware_repos_file_name: autoware.repos
          verbosity: 0
```

## Inputs

| Name                     | Required | Default        | Description                                                                                                                   |
| ------------------------ | -------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| token                    | true     |                | The token for pull requests.                                                                                                  |
| repo_name                | true     |                | The name of the repository to create pull requests.                                                                           |
| targets                  | false    | any            | The target release types (choices: any, patch, minor, major).                                                                 |
| parent_dir               | false    | .              | The parent directory of the repository.                                                                                       |
| base_branch              | false    | main           | The base branch to create pull requests.                                                                                      |
| new_branch_prefix        | false    | feat/update-   | The prefix of the new branch name. The branch name will be `{new_branch_prefix}-{user_name}/{repository_name}/{new_version}`. |
| autoware_repos_file_name | false    | autoware.repos | The name of the vcs imported repository's file (e.g. autoware.repos).                                                         |
| verbosity                | false    | 0              | The verbosity level (0 - 2).                                                                                                  |

## Outputs

None.

## What kind of tags are handled?

- Monitors all vcs-imported repositories in the `autoware.repos` (if default) which have a version with regular expression pattern `r'\b(?<![^\s])\d+\.\d+\.\d+(?![-\w.+])\b'`.
  - This pattern match/mismatches for the following examples:

```plaintext
        "0.0.1",                # match
        "0.1.0",                # match
        "1.0.0",                # match
        "2.1.1",                # match
        "v0.0.1",               # mismatch
        "ros2-v0.0.4",          # mismatch
        "xxx-1.0.0-yyy",        # mismatch
        "v1.2.3-beta",          # mismatch
        "v1.0",                 # mismatch
        "v2",                   # mismatch
        "1.0.0-alpha+001",      # mismatch
        "v1.0.0-rc1+build.1",   # mismatch
        "2.0.0+build.1848",     # mismatch
        "2.0.1-alpha.1227",     # mismatch
        "1.0.0-alpha.beta",     # mismatch
        "ros_humble-v0.10.2"    # mismatch
```

## What kind of version update is possible?

- If there is a new version with pattern matched in the vcs-imported repositories, create a PR for each repository, respectively.
- The valid/invalid version update cases are as follows:
  - Valid ones (PR must be created):

```plaintext
    0.0.1  =>  0.0.2    # If `--target patch` or `--target any` is specified
    1.1.1  =>  1.2.1    # If `--target minor` or `--target any` is specified
    2.4.3  =>  3.0.0    # If `--target major` or `--target any` is specified
```

- Invalid ones (PR is not created):

```plaintext
    main       =>  0.0.1
    v0.0.1     =>  0.0.2
    xxx-0.0.1  =>  0.0.9
    0.0.1-rc1  =>  0.0.2
```
