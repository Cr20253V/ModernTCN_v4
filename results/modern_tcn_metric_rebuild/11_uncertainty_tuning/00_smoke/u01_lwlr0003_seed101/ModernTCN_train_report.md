# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `uncertainty_weighting`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## E2 hard-sample focal settings

- lambda_transition_focal: `0.0`
- lambda_stall_focal: `0.0`
- lambda_theta_smooth: `0.0`
- focal_gamma: `2.0`
- theta_smooth_mode: `off`
- theta_smooth_status: `disabled_contract_limited`

## 配置

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
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.1,
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
    1.4,
    0.8,
    1.4
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.5,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.6,
  "select_turn_lr_target": 0.88,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.3,
  "select_theta_ref_deg": 2.0,
  "select_theta_p95_weight": 0.8,
  "select_theta_p95_target_deg": 1.2,
  "select_theta_flat_p95_weight": 0.35,
  "select_theta_flat_p95_target_deg": 0.7,
  "select_theta_near_flat_p95_weight": 0.2,
  "select_theta_near_flat_p95_target_deg": 0.7,
  "select_theta_true_zero_p95_weight": 0.45,
  "select_theta_true_zero_p95_target_deg": 0.5,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.7,
  "select_theta_edge_p95_target_deg": 1.5,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.5781 |
| acc_turn | 0.2969 |
| acc_turn_pure | 0.2727 |
| acc_turn_transition | 0.3793 |
| main_confidence_mean | 0.4662 |
| main_low_conf_0p60_ratio | 0.9141 |
| main_low_conf_0p70_ratio | 1.0000 |
| turn_confidence_mean | 0.3875 |
| turn_low_conf_0p60_ratio | 1.0000 |
| turn_low_conf_0p70_ratio | 1.0000 |
| turn_right_recall | 0.8000 |
| turn_straight_recall | 0.1711 |
| turn_left_recall | 0.1852 |
| theta_mae_deg | 22.6079 |
| theta_abs_le_10_p95_abs_err_deg | 66.4102 |
| theta_neg_10_8_p95_abs_err_deg | 43.0529 |
| theta_pos_8_10_p95_abs_err_deg | 27.9858 |
| theta_abs_le_8_p95_abs_err_deg | 69.5746 |
| theta_neg_8_6_p95_abs_err_deg | 20.0695 |
| theta_pos_6_8_p95_abs_err_deg | 51.7423 |
| theta_neg_2_0p5_p95_abs_err_deg | 71.7198 |
| theta_pos_0p5_2_p95_abs_err_deg | 37.2598 |
| theta_flat_abs_p95_deg | 64.7187 |
| theta_flat_bias_deg | -11.7689 |
| theta_near_flat_abs_p95_deg | 20.4494 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -4.3209 |
| theta_flat_turn_abs_p95_deg | 13.6468 |
| flat_recall | 0.3030 |
| stall_recall | 0.0000 |
| slope_recall | 0.7033 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.2500 |
| uphill_recall | 0.5441 |
| downhill_recall | 0.8929 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    10,
    0,
    23
  ],
  [
    1,
    0,
    3
  ],
  [
    27,
    0,
    64
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    20,
    2,
    3
  ],
  [
    42,
    13,
    21
  ],
  [
    21,
    1,
    5
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 1.002430 |
| test_loss_turn_bundle_base | 0.221288 |
| test_loss_theta_bundle_base | 0.275848 |
| test_loss_transition_focal_raw | 0.521098 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 1.006299 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 2
- train_seconds: 0.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 117 | 0.3932 | 0.4528 |
| [0.60,0.70) | 11 | 0.7273 | 0.6090 |
| [0.70,0.80) | 0 | nan | nan |
| [0.80,0.90) | 0 | nan | nan |
| [0.90,1.00) | 0 | nan | nan |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 128 | 0.7031 | 0.3875 |
| [0.60,0.70) | 0 | nan | nan |
| [0.70,0.80) | 0 | nan | nan |
| [0.80,0.90) | 0 | nan | nan |
| [0.90,1.00) | 0 | nan | nan |


## 验证集最佳点

```json
{
  "loss_total": 1.2561485767364502,
  "acc_main": 0.65625,
  "acc_turn": 0.296875,
  "acc_turn_pure": 0.2830188679245283,
  "acc_turn_transition": 0.36363636363636365,
  "false_turn_straight": 0.868421052631579,
  "flat_recall": 0.42857142857142855,
  "stall_recall": 0.0,
  "slope_recall": 0.7009345794392523,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": NaN,
  "recall_main": [
    0.42857142857142855,
    0.0,
    0.7009345794392523
  ],
  "turn_right_recall": 0.9130434782608695,
  "turn_straight_recall": 0.13157894736842105,
  "turn_left_recall": 0.2413793103448276,
  "recall_turn": [
    0.9130434782608695,
    0.13157894736842105,
    0.2413793103448276
  ],
  "cm_turn": [
    [
      21,
      2,
      0
    ],
    [
      54,
      10,
      12
    ],
    [
      19,
      3,
      7
    ]
  ],
  "n_turn_transition": 22,
  "n_turn_pure": 106,
  "cm_main": [
    [
      9,
      0,
      12
    ],
    [
      0,
      0,
      0
    ],
    [
      31,
      1,
      75
    ]
  ],
  "main_confidence_mean": 0.4625042556896531,
  "main_confidence_error_mean": 0.4774498547888845,
  "main_low_conf_0p60_ratio": 0.9296875,
  "main_low_conf_0p70_ratio": 0.9609375,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 119,
      "error_rate": 0.3277310924369748,
      "mean_confidence": 0.44339684714896144
    },
    {
      "bin": "[0.60,0.70)",
      "n": 4,
      "error_rate": 0.5,
      "mean_confidence": 0.6428984664179648
    },
    {
      "bin": "[0.70,0.80)",
      "n": 4,
      "error_rate": 0.75,
      "mean_confidence": 0.7483019754212487
    },
    {
      "bin": "[0.80,0.90)",
      "n": 1,
      "error_rate": 0.0,
      "mean_confidence": 0.8715181501923291
    },
    {
      "bin": "[0.90,1.00)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    }
  ],
  "turn_confidence_mean": 0.3838756302798745,
  "turn_confidence_error_mean": 0.38175229925035314,
  "turn_low_conf_0p60_ratio": 1.0,
  "turn_low_conf_0p70_ratio": 1.0,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 128,
      "error_rate": 0.703125,
      "mean_confidence": 0.3838756302798745
    },
    {
      "bin": "[0.60,0.70)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    },
    {
      "bin": "[0.70,0.80)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    },
    {
      "bin": "[0.80,0.90)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    },
    {
      "bin": "[0.90,1.00)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    }
  ],
  "theta_mae_rad": 0.23795518279075623,
  "theta_mae_deg": 13.633827209472656,
  "uphill_recall": 0.6212121212121212,
  "downhill_recall": 0.7419354838709677,
  "slope_sign_acc": 0.6875,
  "theta_flat_mae_deg": 18.965595245361328,
  "theta_flat_abs_p95_deg": 55.403350830078125,
  "theta_flat_abs_max_deg": 82.9007339477539,
  "theta_flat_bias_deg": -14.515016555786133,
  "theta_flat_n": 21.0,
  "theta_near_flat_mae_deg": 19.83052635192871,
  "theta_near_flat_abs_p95_deg": 62.55116271972656,
  "theta_near_flat_abs_max_deg": 82.9007339477539,
  "theta_near_flat_bias_deg": -12.826601028442383,
  "theta_near_flat_n": 10.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 24.067495346069336,
  "theta_flat_turn_abs_p95_deg": 69.33433532714844,
  "theta_flat_turn_abs_max_deg": 82.9007339477539,
  "theta_flat_turn_bias_deg": -16.466793060302734,
  "theta_flat_turn_n": 7.0,
  "theta_slope_control_mae_deg": 13.633827209472656,
  "theta_slope_control_abs_p95_deg": 48.45128631591797,
  "theta_slope_control_abs_max_deg": 82.9007339477539,
  "theta_slope_control_bias_deg": -9.131558418273926,
  "theta_slope_control_n": 128.0,
  "theta_all_mae_deg": 13.633827209472656,
  "theta_all_rmse_deg": 21.372766494750977,
  "theta_all_p95_abs_err_deg": 47.59920120239258,
  "theta_all_max_abs_err_deg": 82.4007339477539,
  "theta_all_bias_deg": -9.131559371948242,
  "theta_all_n": 128.0,
  "theta_active_abs_ge_2_mae_deg": 12.587404251098633,
  "theta_active_abs_ge_2_rmse_deg": 19.577585220336914,
  "theta_active_abs_ge_2_p95_abs_err_deg": 41.7896614074707,
  "theta_active_abs_ge_2_max_abs_err_deg": 66.8011474609375,
  "theta_active_abs_ge_2_bias_deg": -8.074993133544922,
  "theta_active_abs_ge_2_n": 107.0,
  "theta_abs_le_8_mae_deg": 15.038241386413574,
  "theta_abs_le_8_rmse_deg": 23.120458602905273,
  "theta_abs_le_8_p95_abs_err_deg": 55.4377555847168,
  "theta_abs_le_8_max_abs_err_deg": 82.4007339477539,
  "theta_abs_le_8_bias_deg": -11.012195587158203,
  "theta_abs_le_8_n": 105.0,
  "theta_abs_le_10_mae_deg": 13.633827209472656,
  "theta_abs_le_10_rmse_deg": 21.372766494750977,
  "theta_abs_le_10_p95_abs_err_deg": 47.59920120239258,
  "theta_abs_le_10_max_abs_err_deg": 82.4007339477539,
  "theta_abs_le_10_bias_deg": -9.131559371948242,
  "theta_abs_le_10_n": 128.0,
  "theta_pos_8_10_mae_deg": 6.009587287902832,
  "theta_pos_8_10_rmse_deg": 8.500604629516602,
  "theta_pos_8_10_p95_abs_err_deg": 17.572824478149414,
  "theta_pos_8_10_max_abs_err_deg": 22.790964126586914,
  "theta_pos_8_10_bias_deg": -2.597090005874634,
  "theta_pos_8_10_n": 13.0,
  "theta_neg_10_8_mae_deg": 8.798973083496094,
  "theta_neg_10_8_rmse_deg": 11.840872764587402,
  "theta_neg_10_8_p95_abs_err_deg": 23.51732063293457,
  "theta_neg_10_8_max_abs_err_deg": 24.303672790527344,
  "theta_neg_10_8_bias_deg": 2.1203129291534424,
  "theta_neg_10_8_n": 10.0,
  "theta_pos_6_8_mae_deg": 8.727798461914062,
  "theta_pos_6_8_rmse_deg": 11.3026704788208,
  "theta_pos_6_8_p95_abs_err_deg": 21.085405349731445,
  "theta_pos_6_8_max_abs_err_deg": 24.37473487854004,
  "theta_pos_6_8_bias_deg": -8.246581077575684,
  "theta_pos_6_8_n": 12.0,
  "theta_neg_8_6_mae_deg": 13.570746421813965,
  "theta_neg_8_6_rmse_deg": 18.12028694152832,
  "theta_neg_8_6_p95_abs_err_deg": 33.48075866699219,
  "theta_neg_8_6_max_abs_err_deg": 34.33326721191406,
  "theta_neg_8_6_bias_deg": -8.491029739379883,
  "theta_neg_8_6_n": 12.0,
  "theta_neg_4_2_mae_deg": 20.975645065307617,
  "theta_neg_4_2_rmse_deg": 30.609468460083008,
  "theta_neg_4_2_p95_abs_err_deg": 65.01481628417969,
  "theta_neg_4_2_max_abs_err_deg": 65.20205688476562,
  "theta_neg_4_2_bias_deg": -17.914079666137695,
  "theta_neg_4_2_n": 14.0,
  "theta_neg_2_0p5_mae_deg": 16.254941940307617,
  "theta_neg_2_0p5_rmse_deg": 18.98012351989746,
  "theta_neg_2_0p5_p95_abs_err_deg": 28.055095672607422,
  "theta_neg_2_0p5_max_abs_err_deg": 30.110382080078125,
  "theta_neg_2_0p5_bias_deg": -10.190335273742676,
  "theta_neg_2_0p5_n": 3.0,
  "theta_pos_0p5_2_mae_deg": 18.900920867919922,
  "theta_pos_0p5_2_rmse_deg": 29.434314727783203,
  "theta_pos_0p5_2_p95_abs_err_deg": 52.11433029174805,
  "theta_pos_0p5_2_max_abs_err_deg": 56.90334701538086,
  "theta_pos_0p5_2_bias_deg": -18.24729347229004,
  "theta_pos_0p5_2_n": 8.0,
  "loss_main": 0.9364165663719177,
  "loss_turn": 1.0855517387390137,
  "loss_theta": 0.1391477882862091,
  "loss_main_bundle_base": 0.9364165663719177,
  "loss_turn_bundle_base": 0.21711035072803497,
  "loss_theta_bundle_base": 0.10262172669172287,
  "loss_main_bundle": 0.9364165663719177,
  "loss_turn_bundle": 0.21711035072803497,
  "loss_theta_bundle": 0.10262172669172287,
  "loss_theta_flat": 0.07162836939096451,
  "loss_theta_near_flat": 0.2891320586204529,
  "loss_theta_error_excess": 0.13113833963871002,
  "loss_theta_flat_excess": 0.06801579147577286,
  "loss_theta_near_flat_excess": 0.2831733822822571,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.10938112437725067,
  "loss_theta_small_neg": 0.2854081690311432,
  "loss_theta_small_neg_excess": 0.2729336619377136,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.45730021595954895,
  "loss_false_turn_straight": 0.46771714091300964,
  "loss_transition_focal_raw": 0.47392719984054565,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 0.0,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
