# Register AutonomouStuff repository

## Inputs

- rosdistro
  - ROS distribution to register into rosdep

## Outputs

- None

## Sample Workflow Steps

```yaml
- uses: autowarefoundation/autoware-github-actions/register-autonomoustuff-repository@tier4/proposal
  with:
    rosdistro: galactic
```
