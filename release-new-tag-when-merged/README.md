# release-new-version-when-merged

## Description

This action automatically creates a new tag when a commit is merged, based on the version specified in the `package.xml` files. It checks for the latest version tag and creates a new tag if the version is newer.

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
  tag-on-merge:
    if: |
      github.event.pull_request.merged == true &&
      contains(
        join(github.event.pull_request.labels.*.name, ','),
        'release:bump-version'
      )
  release-tag:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.PRIVATE_KEY }}

      - name: Run
        uses: autowarefoundation/autoware-github-actions/release-new-tag-when-merged@v1
        with:
          github_token: ${{ steps.generate-token.outputs.token }}
          commit_sha: ${{ github.event.pull_request.merge_commit_sha }}
```

## Inputs

| Name         | Required | Description                         |
| ------------ | -------- | ----------------------------------- |
| github_token | true     | The GitHub token for authentication |
| commit_sha   | true     | The commit SHA to release           |

## Outputs

None.
