# patch_full Final Report

- decision: `NO_PROMOTION`
- stop_node: `D6_single_seed_gate`
- best_run: `full128_light_seed21`
- reason: formal single-seed full128 gate failed before the planned 9-run expansion.
- onnx/matlab/closed-loop: not executed.
- seq_len_256: `not allowed from this run; full128 did not pass the prerequisite gate.`

## Failures

- theta_mae_deg 2.19818 <= 1.2 failed
