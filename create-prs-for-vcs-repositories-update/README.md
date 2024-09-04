# create-prs-for-vcs-repositories-update

## Description

This action creates pull requests for updating the vcs repositories in the autoware repository.

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
    runs-on: ubuntu-latest
    steps:
      - name: Generate token
        id: generate-token
        uses: tibdex/github-app-token@v1
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.PRIVATE_KEY }}

      - name: Run 
        uses: sasakisasaki/autoware-github-actions/create-prs-for-vcs-repositories-update@add-feature-for-creating-prs-which-update-vcs-repositories
        with:
          token: ${{ steps.generate-token.outputs.token }}
          repo_name: autowarefoundation/autoware_dummy_repository
          parent_dir: .
          base_branch: main
          new_branch_prefix: feat/update-
          autoware_repos_file_name: autoware.repos
          verbosity: 0
```

## Inputs

| Name                     | Required | Default                                      | Description                                                                                                                   |
| ------------------------ | -------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| token                    | true     |                                              | The token for pull requests.                                                                                                  |
| repo_name                | true     |                                              | The name of the repository to create pull requests.                                                                           |
| parent_dir               | false    | .                                            | The parent directory of the repository.                                                                                       |
| base_branch              | false    | main                                         | The base branch to create pull requests.                                                                                      |
| new_branch_prefix        | false    | feat/update-                                 | The prefix of the new branch name. The branch name will be `{new_branch_prefix}-{user_name}/{repository_name}/{new_version}`. |
| autoware_repos_file_name | false    | autoware.repos                               | The name of the vcs imported repository's file (e.g. autoware.repos).                                                         |
| verbosity                | false    | 0                                            | The verbosity level (0 - 2).                                                                                                  |

## Outputs

None.
