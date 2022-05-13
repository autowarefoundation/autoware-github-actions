# sync-files

## Description

This action syncs files between repositories.  
It uses [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request/) for creating pull requests and [peter-evans/enable-pull-request-automerge](https://github.com/peter-evans/enable-pull-request-automerge) for enabling auto-merge.

Note that you need `workflow` permission for the token if you copy workflow files of GitHub Actions.

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
| files/source          | true     | -                                            | The path to the file in the target repository.                                           |
| files/dest            | false    | The same as `files/source`.                  | The path where to place the synced file in the base repository.                          |
| files/replace         | false    | `true`                                       | Whether to replace the synced file if it already exists.                                 |
| files/delete-orphaned | false    | `true`                                       | Whether to delete the synced file if it does not exist in the target repository anymore. |
| files/pre-command     | false    | `""`                                         | The command executed before copying the file.                                            |
| files/post-command    | false    | `""`                                         | The command executed after copying the file.                                             |

In the `pre-command` and `post-command` options, the following special variables can be used:

- `{source}`: The sync source file
- `{target}`: The sync target file

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
