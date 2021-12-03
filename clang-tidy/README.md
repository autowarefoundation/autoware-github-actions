# clang-tidy

## Inputs

| Name                  | Required | Description                                     |
| --------------------- | -------- | ----------------------------------------------- |
| rosdistro             | true     | ROS distro.                                     |
| build-depends-repos   | true     | VCS repositories containing build dependencies. |
| target-files          | true     | Target files to run clang-tidy on.              |
| compile-commands-hash | true     | Calculated hash of compile_commands.json.       |
| token                 | false    | If the repository is private, specify a token.  |

## Sample Workflow Steps

```yaml
- name: Run clang-tidy
  uses: autowarefoundation/autoware-github-actions/clang-tidy@tier4/proposal
  with:
    rosdistro: galactic
    build-depends-repos: build_depends.repos
    target-files: ${{ steps.get-modified-source-files.outputs.modified-source-files }}
    compile-commands-hash: ${{ steps.build-and-test.outputs.compile-commands-hash }}
```
