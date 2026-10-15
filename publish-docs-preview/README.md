# publish-docs-preview

This action publishes the site that [build-docs-preview](../build-docs-preview/README.md) built to [Cloudflare Pages](https://pages.cloudflare.com/).
Then it adds a comment to the pull request with the URL of the preview and of each changed page.

The preview of pull request 123 is at `https://pr-123.<project>.pages.dev/`.
Each new commit replaces the preview at this URL.
The comment also links a fixed URL for the commit.

## Why the preview is on Cloudflare Pages

A pull request can change the HTML and JavaScript of its site.
On GitHub Pages, all sites of the organization share the origin `autowarefoundation.github.io`, so a preview there runs on the same origin as the real documentation.
On Cloudflare Pages, a preview has its own origin.
The Cloudflare token can change previews only, and it cannot write to any repository.
For these reasons, every commit gets a preview without a label.

## How the action keeps the token away from the code of the pull request

The code of the pull request runs only in the `build-docs-preview` workflow.
This workflow has a read-only token and no secrets.

This action runs in a `workflow_run` workflow.
GitHub always takes a `workflow_run` workflow from the default branch, so a pull request cannot change it.
The action treats the built site as data:

- It finds the pull request from the GitHub API, by the head commit and the head repository of the build. It never reads the pull request number from the artifact.
- It skips a build that is not the head commit of an open pull request.
- It refuses a site without `index.html`, and a site with links, hidden files, or special files.
- It refuses a site with the Cloudflare Pages control files `_worker.js`, `_routes.json`, `_headers`, or `_redirects` at its root. `_worker.js` runs as server code on Cloudflare.
- It leaves out files larger than 25 MiB, because Cloudflare Pages refuses them. The comment lists these files.
- It runs Wrangler in an empty workspace, so that Wrangler finds no `functions` directory and no `wrangler.toml` file.

## Setup

Do these steps one time for the Cloudflare account:

1. Create a Cloudflare account that holds only the previews. The Pages permission of a token covers all projects of an account.
2. Create an API token with the permission `Account` > `Cloudflare Pages` > `Edit`, for this account only.
3. Add the token as the secret `CLOUDFLARE_API_TOKEN` and the account ID as the secret `CLOUDFLARE_ACCOUNT_ID`. Use organization secrets, and give access to the repositories with documentation.

Do this step one time for each repository:

1. Create a Pages project for the repository, for example `autoware-documentation-preview`:

   ```bash
   npx wrangler pages project create autoware-documentation-preview --production-branch main
   ```

The project never gets a production deployment. Every deployment uses a `pr-<number>` branch.

## Usage

Do not check out code in this job.
Give the job only the permissions that this example shows.

```yaml
name: publish-docs-preview

on:
  workflow_run:
    workflows:
      - build-docs-preview
    types:
      - completed

permissions: {}

jobs:
  publish-docs-preview:
    if: ${{ github.event.workflow_run.event == 'pull_request' && github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    permissions:
      actions: read
      pull-requests: write
    concurrency:
      group: ${{ github.workflow }}-${{ github.event.workflow_run.head_repository.full_name }}-${{ github.event.workflow_run.head_branch }}
      cancel-in-progress: true
    steps:
      - name: Publish docs preview
        uses: autowarefoundation/autoware-github-actions/publish-docs-preview@v1
        with:
          cloudflare-api-token: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          cloudflare-account-id: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          cloudflare-project: autoware-documentation-preview
```

## Inputs

| Name                  | Required | Description                                                                        |
| --------------------- | -------- | ---------------------------------------------------------------------------------- |
| cloudflare-api-token  | true     | A Cloudflare API token with the `Cloudflare Pages` `Edit` permission.              |
| cloudflare-account-id | true     | The ID of the Cloudflare account.                                                  |
| cloudflare-project    | true     | The name of the Cloudflare Pages project.                                          |
| artifact-name         | false    | The name of the artifact of `build-docs-preview`. The default is `docs-preview`.   |
| github-token          | false    | A token with `actions: read` and `pull-requests: write`. The default is the token of the job. |

## Outputs

| Name        | Description                                                              |
| ----------- | ------------------------------------------------------------------------ |
| preview-url | The URL of the preview of the pull request, empty if nothing was published. |
