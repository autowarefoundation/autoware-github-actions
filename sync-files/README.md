# sync-files

## Description

This action syncs files between repositories.  
It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests.

Note that you need `workflow` permission for the token if you copy workflow files of GitHub Actions.

## Initial setup (within `autowarefoundation` org)

This action uses the <https://github.com/apps/awf-autoware-bot> app to create pull requests.

### Secrets

For this action to use this bot, it requires the following secrets:

- `APP_ID`: The app ID of the bot.
  - Can be found in [awf-autoware-bot App Settings](https://github.com/organizations/autowarefoundation/settings/apps/awf-autoware-bot) General, About section.
- `PRIVATE_KEY`: The private key of the bot.
  - Can be found/generated in [awf-autoware-bot App Settings](https://github.com/organizations/autowarefoundation/settings/apps/awf-autoware-bot) General, Private keys section.

Then these secrets need to be set in the repository settings.

- Target Repository GitHub Page, Settings, Secrets and variables, Actions, New repository secret, `APP_ID` and `PRIVATE_KEY`

### App settings

Also, you need to install the app to the target repository.

- [awf-autoware-bot App Settings](https://github.com/organizations/autowarefoundation/settings/apps/awf-autoware-bot) Install App section, Repository access, Only select repositories, add the target repository.

### Additional repository settings

For this action to work properly, the following settings are required in the target repository.

- Target Repository GitHub Page, Settings, General, Pull Requests, Allow auto-merge # Enable

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

      - name: Run sync-files
        uses: autowarefoundation/autoware-github-actions/sync-files@v1
        with:
          token: ${{ steps.generate-token.outputs.token }}
          auto-merge-method: squash
```

Create `.github/sync-files.yaml` like this.

```yaml
- repository: autowarefoundation/autoware
  files:
    - source: .github/dependabot.yaml
```

The specifications are:

- The settings for each repository are listed at the top level.

  ```yaml
  - repository: org1/repo1
    files: ...

  - repository: org1/repo2
    files: ...

  - repository: org2/repo
    files: ...
  ```

- The data format for each repository is the following.

| Name                  | Required | Default                                      | Description                                                                              |
| --------------------- | -------- | -------------------------------------------- | ---------------------------------------------------------------------------------------- |
| repository            | true     | -                                            | The target repository.                                                                   |
| ref                   | false    | The default branch of the target repository. | The version of the target repository.                                                    |
| source-dir            | false    | Not prefixed.                                | The prefix common to `files/source`. This does not apply to the default of `files/dest`. |
| files/source          | true     | -                                            | The path to the file in the target repository.                                           |
| files/dest            | false    | The same as `files/source`.                  | The path where to place the synced file in the base repository.                          |
| files/replace         | false    | `true`                                       | Whether to replace the synced file if it already exists.                                 |
| files/delete-orphaned | false    | `true`                                       | Whether to delete the synced file if it does not exist in the target repository anymore. |
| files/pre-commands    | false    | `""`                                         | The multi-line commands executed before copying the file.                                |
| files/post-commands   | false    | `""`                                         | The multi-line commands executed after copying the file.                                 |

In the `pre-commands` and `post-commands` options, the following special variables can be used:

- `{source}`: The sync source file
- `{dest}`: The sync dest file

Example:

```yaml
- repository: autowarefoundation/autoware
  files:
    - source: .pre-commit-config.yaml
      post-commands: |
        sd -f ms "[^\n]*shellcheck-py\n.*?\n\n" "" {dest}
```

## Inputs

| Name              | Required | Description                                           |
| ----------------- | -------- | ----------------------------------------------------- |
| token             | true     | The token for pull requests.                          |
| config            | false    | The path to `sync-files.yaml`.                        |
| pr-base           | false    | Refer to `peter-evans/create-pull-request`.           |
| pr-branch         | false    | The same as above.                                    |
| pr-title          | false    | The same as above.                                    |
| pr-commit-message | false    | The same as above.                                    |
| pr-labels         | false    | The same as above.                                    |
| pr-assignees      | false    | The same as above.                                    |
| pr-reviewers      | false    | The same as above.                                    |
| auto-merge-method | false    | Refer to `peter-evans/enable-pull-request-automerge`. |

## Outputs

None.
