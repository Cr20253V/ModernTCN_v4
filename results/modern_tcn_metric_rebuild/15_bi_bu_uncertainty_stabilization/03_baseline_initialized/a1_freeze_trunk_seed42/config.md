# ModernTCN run config

- model_family: `small`
- loss_mode: `bounded_uncertainty`
- run_tag: `a1_freeze_trunk_seed42`
- output_dir: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\15_bi_bu_uncertainty_stabilization\03_baseline_initialized\a1_freeze_trunk_seed42`
- git_hash: `e6bef51a3ed5e4bf6d0f59f24852439dd5a05823`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- input: `[batch,128,22]`

## Model Config

```json
{
  "input_dim": 22,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "temporal_padding": "same",
  "dropout": 0.15,
  "command_dropout_prob": 0.0,
  "command_dropout_start_index": -1,
  "command_dropout_feature_count": 0,
  "command_dropout_mode": "window_block",
  "expansion": 2,
  "readout_input_stats": true,
  "turn_head_source": "full",
  "turn_feature_indices": [
    0,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    13,
    21
  ],
  "lambda_turn": 0.2,
  "lambda_theta": 0.55,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.0,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.0,
  "lambda_theta_active_excess": 0.0,
  "lambda_theta_small_neg": 0.0,
  "lambda_theta_small_neg_excess": 0.0,
  "lambda_turn_release": 0.0,
  "lambda_false_turn_straight": 0.0,
  "lambda_transition_focal": 0.0,
  "lambda_stall_focal": 0.0,
  "lambda_theta_smooth": 0.0,
  "focal_gamma": 2.0,
  "theta_smooth_mode": "off",
  "theta_excess_target_deg": 1.0,
  "theta_flat_excess_target_deg": 0.5,
  "theta_true_zero_tol_deg": 0.0001,
  "theta_small_neg_min_deg": -4.0,
  "theta_small_neg_max_deg": -2.0,
  "theta_gate_mode": "none",
  "theta_gate_power": 1.0,
  "theta_gate_floor": 0.0,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.0,
    1.1,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_turn_lr_weight": 0.0,
  "select_turn_lr_target": 0.8,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.15,
  "select_theta_ref_deg": 5.0,
  "select_theta_p95_weight": 0.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 0.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 0.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.0,
  "select_theta_extreme_p95_target_deg": 1.0,
  "select_theta_edge_p95_weight": 0.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.0,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2,
  "freeze_mode": "trunk",
  "freeze_early_blocks": 3,
  "preserve_mode": "baseline",
  "lambda_preserve_main": 0.05,
  "lambda_preserve_turn": 0.05,
  "lambda_preserve_theta": 0.05,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## Dynamic Loss State

```json
{
  "loss_mode": "bounded_uncertainty",
  "gradnorm_alpha": 1.5,
  "s_range": 0.25,
  "s_prior_lambda": 0.01,
  "raw_s_main": -0.06511775404214859,
  "s_main": -0.01625646837055683,
  "weight_main": 1.0163893699645996,
  "raw_s_turn": -0.0650087296962738,
  "s_turn": -0.016229325905442238,
  "weight_turn": 1.0163617134094238,
  "raw_s_theta": -0.06501595675945282,
  "s_theta": -0.016231125220656395,
  "weight_theta": 1.016363501548767,
  "freeze_mode": "trunk",
  "freeze_early_blocks": 3,
  "preserve_mode": "baseline",
  "lambda_preserve_main": 0.05,
  "lambda_preserve_turn": 0.05,
  "lambda_preserve_theta": 0.05,
  "lambda_s_prior": 0.01
}
```
