# Register AutonomouStuff repository

## Inputs

- rosdistro
  - ROS distribution to register into rosdep

## Outputs

- None

## Sample Workflow Steps

```yaml
- uses: actions/checkout@v2
  with:
    fetch-depth: 0

- uses: autowarefoundation/autoware-github-actions/register-autonomoustuff-repository@tier4/proposal
  id: register-autonomoustuff-repository
  with:
    rosdistro: galactic
```
