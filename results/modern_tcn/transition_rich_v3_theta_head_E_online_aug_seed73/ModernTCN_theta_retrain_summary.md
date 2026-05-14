# ModernTCN theta retrain summary

Final candidate:

- run tag: `transition_rich_v3_theta_head_E_online_aug_seed73`
- checkpoint: `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.pt`
- ONNX: `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.onnx`
- base model: `transition_rich_v3_kinTurnD_seed73`
- training mode: frozen backbone/main/turn heads, theta head only
- online augmentation: `data/tcn/ModernTCN_theta_online_aug_industrial_lite_v2_seed73.npz`

Offline test metrics on `TCN_dataset_v3_transition_rich_clean_turn_aug.mat`:

| metric | baseline kinTurnD | final E |
|---|---:|---:|
| acc_main | 0.97519 | 0.97519 |
| acc_turn | 0.78940 | 0.78940 |
| acc_turn_transition | 0.59442 | 0.59442 |
| turn_left_recall | 0.95965 | 0.95965 |
| slope theta MAE deg | 0.39310 | 0.71922 |
| flat theta abs p95 deg | 1.25795 | 0.96915 |
| flat theta bias deg | 0.00389 | 0.00781 |
| near-flat theta abs p95 deg | 2.69894 | 0.96916 |
| flat-turn theta abs p95 deg | 0.90524 | 0.64694 |
| slope sign accuracy | 1.00000 | 1.00000 |

Closed-loop replay on the latest stable `out.mat`:

| zone | theta MAE deg | theta peak deg | main acc pct | turn acc05 pct |
|---|---:|---:|---:|---:|
| pure_turn | 0.00000 | 0.00000 | 100.0 | 98.321 |
| pure_slope | 0.64156 | 3.1630 | 93.9 | 92.4 |
| composite | 0.47231 | 2.7934 | 94.2 | 88.75 |
| closure | 0.00071 | 0.03833 | 100.0 | 86.281 |

Checks completed:

- PyTorch control-metric evaluation: passed target.
- PyTorch to ONNXRuntime consistency: passed.
- MATLAB full test-set inference: matched expected metrics.
- Simulink-wrapper y_raw replay: passed flat/closure theta target and slope MAE target.

Notes:

- Main/turn classification branches are unchanged from the base model because only `theta_head` was trainable.
- `ModernTCN_state_classifier`, `ModernTCN_load_predictor`, and replay defaults now point to this final candidate. A caller can still override with `modern_tcn_sim_cfg.run_tag` or `modern_tcn_sim_cfg.onnx_file`.
