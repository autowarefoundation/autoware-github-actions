# register-autonomoustuff-repository

This action sets up the prerequisites for [pacmod3_msgs](https://github.com/astuff/pacmod3_msgs), which is used in Autoware.

## Usage

```yaml
- uses: autowarefoundation/autoware-github-actions/register-autonomoustuff-repository@tier4/proposal
  with:
    rosdistro: galactic
```

## Inputs

| Name      | Required | Description |
| --------- | -------- | ----------- |
| rosdistro | true     | ROS distro. |

## Outputs

None.
