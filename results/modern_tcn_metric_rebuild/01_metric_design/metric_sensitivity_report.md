# Metric Sensitivity Report

Node 2 is development-only. It exists to test whether ranking is stable before freeze.

## Result

- Top-3 proxy ranking is stable across v0-v3.
- No candidate crosses the sensitivity threshold used for class-E labeling.
- Any mid-pack reordering is small and does not affect the decision frontier.

## Practical note

- Official candidate decisions must use the frozen vFinal only.
- Development-only rankings must not be copied into candidate decision artifacts.
