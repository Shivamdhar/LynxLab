# Scenarios

## :heavy_exclamation_mark: Platform misconfigurations

### Risk
- Failed forensics
- Resource exhaustion

### Simulation

The current LynxLab stack enables logging of any event triggered within the authorizer Lambda function, based on the policy configured in `AuthorizationLambdaExecutionRole` in [root.yaml](root.yaml?plain=1#L104).

These logs can be leveraged for proactive monitoring of Lambda triggers, and CloudWatch alarms can be configured using custom metrics.

However, if the policy `Effect` is toggled to `Deny`, logging will be disabled. In such cases, the account owner will lose visibility into Lambda executions, creating a risk of incomplete forensics in the event of an incident.
