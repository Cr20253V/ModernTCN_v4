# ModernTCN Control Freeze - 2026-05-04

This freeze records the current ModernTCN integration baseline before a new
demo path is designed.  The goal is to stop tuning against
`path_industrial_lite.mat` and preserve the working model/control state for
later comparison.

## Frozen Model

- Run tag: `transition_rich_v3_theta_head_E_online_aug_seed73`
- Seed: `73`
- Checkpoint: `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.pt`
- ONNX: `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.onnx`
- Dataset/scaler: `data/tcn/TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
- Base model: `transition_rich_v3_kinTurnD_seed73`
- Fine-tune mode: theta head only; backbone/main/turn heads frozen.

The default MATLAB online loader now points to this model:

- `src/ModernTCN/ModernTCN_state_classifier.m`
- `src/ModernTCN/ModernTCN_load_predictor.m`
- `src/ModernTCN/ModernTCN_replay_closed_loop_yraw.m`

## Frozen Control Policy

- Keep `label_turn` as the only ModernTCN output allowed to affect MPC in the
  current saved baseline.
- Keep `theta_hat` diagnostic-only for the frozen baseline.
- Do not continue tuning thresholds or MPC weights on `path_industrial_lite.mat`.
- Do not use pure `theta_hat` scheduling as a frozen behavior.

If a theta scheduling experiment is needed later, use a guarded experimental
branch and connect the same guarded `theta_sched` signal to both:

- `RhoFilter/theta_in`
- `Adaptive MPC Controller/md`

Keep the plant/S-Function physical road slope input connected to the true path
slope signal.  Do not feed `theta_sched` into the plant.

## Current Metrics

Offline test metrics on `TCN_dataset_v3_transition_rich_clean_turn_aug.mat`:

| metric | value |
|---|---:|
| acc_main | 0.975190 |
| acc_turn | 0.789399 |
| acc_turn_transition | 0.594417 |
| turn_left_recall | 0.959647 |
| theta_slope_mae_deg | 0.719220 |
| theta_flat_abs_p95_deg | 0.969151 |
| theta_flat_bias_deg | 0.007806 |
| theta_near_flat_abs_p95_deg | 0.969155 |
| theta_flat_turn_abs_p95_deg | 0.646942 |
| slope_sign_acc | 1.000000 |

Stable closed-loop diagnostic, with `theta_hat` not connected to scheduling:

| zone | e_y_rmse | e_psi_rmse | theta_mae_deg |
|---|---:|---:|---:|
| pure_turn | 0.027732 | 0.067691 | 0.000000 |
| pure_slope | 0.005693 | 0.019004 | 0.641560 |
| composite | 0.009716 | 0.021662 | 0.472310 |
| closure | 0.005824 | 0.054901 | 0.000707 |

## Known Non-Frozen Item

`theta_hat` closed-loop scheduling is not frozen.  A direct or weakly guarded
connection caused large error growth on `path_industrial_lite.mat` because
closed-loop distribution shift led to false slope activation in the later path
segments.  This should be revisited only after the final demo path is designed.

## Next Resume Point

When the new demo path is ready:

1. Run the baseline with `theta_hat` diagnostic-only.
2. Export `out.mat`.
3. Evaluate per-zone main/turn/theta metrics.
4. Decide whether the demo needs `label_turn` only, or a guarded theta scheduling
   experiment.
5. Add only small targeted samples if the demo path reveals a missing case.
