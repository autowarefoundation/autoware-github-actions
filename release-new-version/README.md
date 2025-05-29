# release-new-version

## Description

This action creates pull requests to update the version for autoware packages.

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
  update-versions:
    runs-on: ubuntu-22.04
    steps:
      - name: Generate token
        id: generate-token
        uses: actions/create-github-app-token@v1
        with:
          app-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.PRIVATE_KEY }}

      - name: Run
        uses: sasakisasaki/autoware-github-actions/release-new-version@testing/release-new-version
        with:
          github_token: ${{ steps.generate-token.outputs.token }}
          source_branch: main
          target_branch: humble
          bump_version: patch
          repository_owner: autowarefoundation
```

## Inputs

| Name              | Required | Default               | Description                                                |
| ----------------- | -------- | --------------------- | ---------------------------------------------------------- |
| github_token      | true     |                       | The GitHub token for authentication                        |
| source_branch     | true     | main                  | The branch to merge from                                   |
| target_branch     | true     | humble                | The branch to merge into (release branch)                  |
| bump_version      | true     | patch                 | The type of version bump (patch, minor, major)             |
| repository_owner  | false    | autowarefoundation    | The owner of the source repository (e.g., fork user/org)   |

## Outputs

None.
