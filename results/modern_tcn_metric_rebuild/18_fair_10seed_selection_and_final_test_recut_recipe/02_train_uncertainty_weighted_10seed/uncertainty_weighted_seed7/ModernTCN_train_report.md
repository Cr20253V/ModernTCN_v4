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
  "select_theta_flat_bias_target_deg": 0.15,
  "freeze_mode": "none",
  "freeze_early_blocks": 3,
  "preserve_mode": "none",
  "lambda_preserve_main": 0.0,
  "lambda_preserve_turn": 0.0,
  "lambda_preserve_theta": 0.0,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9684 |
| acc_turn | 0.5852 |
| acc_turn_pure | 0.5988 |
| acc_turn_transition | 0.5261 |
| main_confidence_mean | 0.9900 |
| main_low_conf_0p60_ratio | 0.0069 |
| main_low_conf_0p70_ratio | 0.0119 |
| turn_confidence_mean | 0.8401 |
| turn_low_conf_0p60_ratio | 0.1299 |
| turn_low_conf_0p70_ratio | 0.2515 |
| turn_right_recall | 0.5695 |
| turn_straight_recall | 0.5773 |
| turn_left_recall | 0.6172 |
| theta_mae_deg | 0.5704 |
| theta_abs_le_10_p95_abs_err_deg | 1.5073 |
| theta_neg_10_8_p95_abs_err_deg | 1.5274 |
| theta_pos_8_10_p95_abs_err_deg | 2.3177 |
| theta_abs_le_8_p95_abs_err_deg | 1.3859 |
| theta_neg_8_6_p95_abs_err_deg | 1.4042 |
| theta_pos_6_8_p95_abs_err_deg | 1.1567 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3283 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5117 |
| theta_flat_abs_p95_deg | 2.4604 |
| theta_flat_bias_deg | -0.0045 |
| theta_near_flat_abs_p95_deg | 1.5406 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1157 |
| theta_flat_turn_abs_p95_deg | 1.5254 |
| flat_recall | 0.9603 |
| stall_recall | 0.6979 |
| slope_recall | 0.9800 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7586 |
| downhill_recall | 0.7957 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    726,
    0,
    30
  ],
  [
    9,
    67,
    20
  ],
  [
    44,
    11,
    2695
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    455,
    199,
    145
  ],
  [
    346,
    1116,
    471
  ],
  [
    122,
    211,
    537
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.387217 |
| test_loss_turn_bundle_base | 0.354948 |
| test_loss_theta_bundle_base | 0.000133 |
| test_loss_transition_focal_raw | 1.616864 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.541743 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 85
- train_seconds: 366.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 25 | 0.4400 | 0.5416 |
| [0.60,0.70) | 18 | 0.5000 | 0.6649 |
| [0.70,0.80) | 24 | 0.1667 | 0.7631 |
| [0.80,0.90) | 42 | 0.3333 | 0.8503 |
| [0.90,1.00) | 3493 | 0.0218 | 0.9981 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 468 | 0.6004 | 0.5297 |
| [0.60,0.70) | 438 | 0.5320 | 0.6557 |
| [0.70,0.80) | 389 | 0.4987 | 0.7510 |
| [0.80,0.90) | 440 | 0.4659 | 0.8493 |
| [0.90,1.00) | 1867 | 0.3112 | 0.9775 |


## 验证集最佳点

```json
{
  "loss_total": 0.667974876970335,
  "acc_main": 0.9456021650879567,
  "acc_turn": 0.6449255751014885,
  "acc_turn_pure": 0.6548672566371682,
  "acc_turn_transition": 0.5978260869565217,
  "false_turn_straight": 0.38825363825363823,
  "flat_recall": 0.9254185692541856,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9586114819759679,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.9254185692541856,
    0.3333333333333333,
    0.9586114819759679
  ],
  "turn_right_recall": 0.6646919431279621,
  "turn_straight_recall": 0.6117463617463618,
  "turn_left_recall": 0.6957928802588996,
  "recall_turn": [
    0.6646919431279621,
    0.6117463617463618,
    0.6957928802588996
  ],
  "cm_turn": [
    [
      561,
      226,
      57
    ],
    [
      377,
      1177,
      370
    ],
    [
      88,
      194,
      645
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      608,
      0,
      49
    ],
    [
      3,
      14,
      25
    ],
    [
      110,
      14,
      2872
    ]
  ],
  "main_confidence_mean": 0.9732824817266683,
  "main_confidence_error_mean": 0.7882869235981822,
  "main_low_conf_0p60_ratio": 0.004871447902571042,
  "main_low_conf_0p70_ratio": 0.0557510148849797,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 18,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.5400431882090996
    },
    {
      "bin": "[0.60,0.70)",
      "n": 188,
      "error_rate": 0.4627659574468085,
      "mean_confidence": 0.6132702391215384
    },
    {
      "bin": "[0.70,0.80)",
      "n": 22,
      "error_rate": 0.5454545454545454,
      "mean_confidence": 0.7655498883172673
    },
    {
      "bin": "[0.80,0.90)",
      "n": 42,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8611865409481557
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3425,
      "error_rate": 0.02394160583941606,
      "mean_confidence": 0.9980295636130289
    }
  ],
  "turn_confidence_mean": 0.8552989394243741,
  "turn_confidence_error_mean": 0.7801045795891294,
  "turn_low_conf_0p60_ratio": 0.13315290933694182,
  "turn_low_conf_0p70_ratio": 0.20866035182679296,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 492,
      "error_rate": 0.6443089430894309,
      "mean_confidence": 0.48970516445605367
    },
    {
      "bin": "[0.60,0.70)",
      "n": 279,
      "error_rate": 0.4910394265232975,
      "mean_confidence": 0.6479878959879001
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.43636363636363634,
      "mean_confidence": 0.7528401799742942
    },
    {
      "bin": "[0.80,0.90)",
      "n": 418,
      "error_rate": 0.43301435406698563,
      "mean_confidence": 0.8551834678714515
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2176,
      "error_rate": 0.24494485294117646,
      "mean_confidence": 0.9801020534550898
    }
  ],
  "theta_mae_rad": 0.012098745442926884,
  "theta_mae_deg": 0.6932070255279541,
  "uphill_recall": 0.7897574123989218,
  "downhill_recall": 0.8097886540600667,
  "slope_sign_acc": 0.9789214344374487,
  "theta_flat_mae_deg": 0.9347634315490723,
  "theta_flat_abs_p95_deg": 3.9566431045532227,
  "theta_flat_abs_max_deg": 5.7828216552734375,
  "theta_flat_bias_deg": 0.5150019526481628,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.1846526861190796,
  "theta_near_flat_abs_p95_deg": 3.9566476345062256,
  "theta_near_flat_abs_max_deg": 6.210314750671387,
  "theta_near_flat_bias_deg": 0.8180749416351318,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.7977147102355957,
  "theta_flat_turn_abs_p95_deg": 3.9566431045532227,
  "theta_flat_turn_abs_max_deg": 4.86079216003418,
  "theta_flat_turn_bias_deg": 0.515595555305481,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.6932070255279541,
  "theta_slope_control_abs_p95_deg": 8.988958358764648,
  "theta_slope_control_abs_max_deg": 12.114130020141602,
  "theta_slope_control_bias_deg": 0.2672465741634369,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.6932069063186646,
  "theta_all_rmse_deg": 1.0672922134399414,
  "theta_all_p95_abs_err_deg": 2.4566431045532227,
  "theta_all_max_abs_err_deg": 7.2714948654174805,
  "theta_all_bias_deg": 0.2672466039657593,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6402354836463928,
  "theta_active_abs_ge_2_rmse_deg": 0.9665898680686951,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9221925735473633,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.2714948654174805,
  "theta_active_abs_ge_2_bias_deg": 0.21291571855545044,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.6994208097457886,
  "theta_abs_le_8_rmse_deg": 1.0813428163528442,
  "theta_abs_le_8_p95_abs_err_deg": 2.4566431045532227,
  "theta_abs_le_8_max_abs_err_deg": 6.715214252471924,
  "theta_abs_le_8_bias_deg": 0.2778797447681427,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.6932069063186646,
  "theta_abs_le_10_rmse_deg": 1.0672922134399414,
  "theta_abs_le_10_p95_abs_err_deg": 2.4566431045532227,
  "theta_abs_le_10_max_abs_err_deg": 7.2714948654174805,
  "theta_abs_le_10_bias_deg": 0.2672466039657593,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5102936029434204,
  "theta_pos_8_10_rmse_deg": 0.6991019248962402,
  "theta_pos_8_10_p95_abs_err_deg": 1.5317840576171875,
  "theta_pos_8_10_max_abs_err_deg": 4.082085609436035,
  "theta_pos_8_10_bias_deg": -0.21274875104427338,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8264026641845703,
  "theta_neg_10_8_rmse_deg": 1.2425018548965454,
  "theta_neg_10_8_p95_abs_err_deg": 2.1424663066864014,
  "theta_neg_10_8_max_abs_err_deg": 7.2714948654174805,
  "theta_neg_10_8_bias_deg": 0.6650523543357849,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5067418813705444,
  "theta_pos_6_8_rmse_deg": 0.7800039052963257,
  "theta_pos_6_8_p95_abs_err_deg": 1.311888575553894,
  "theta_pos_6_8_max_abs_err_deg": 3.6479194164276123,
  "theta_pos_6_8_bias_deg": -0.018228789791464806,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.684307873249054,
  "theta_neg_8_6_rmse_deg": 1.014578938484192,
  "theta_neg_8_6_p95_abs_err_deg": 1.9683387279510498,
  "theta_neg_8_6_max_abs_err_deg": 6.715214252471924,
  "theta_neg_8_6_bias_deg": 0.23151516914367676,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5568681359291077,
  "theta_neg_4_2_rmse_deg": 0.8091066479682922,
  "theta_neg_4_2_p95_abs_err_deg": 1.5800751447677612,
  "theta_neg_4_2_max_abs_err_deg": 4.610417366027832,
  "theta_neg_4_2_bias_deg": 0.11384157091379166,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5749204158782959,
  "theta_neg_2_0p5_rmse_deg": 0.7333396077156067,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2162777185440063,
  "theta_neg_2_0p5_max_abs_err_deg": 3.565045118331909,
  "theta_neg_2_0p5_bias_deg": 0.061396896839141846,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0985468626022339,
  "theta_pos_0p5_2_rmse_deg": 1.4280072450637817,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.4566431045532227,
  "theta_pos_0p5_2_max_abs_err_deg": 4.0108489990234375,
  "theta_pos_0p5_2_bias_deg": 0.7095662951469421,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.34964812124533645,
  "loss_turn": 1.5904914276848303,
  "loss_theta": 0.00034700511236068906,
  "loss_main_bundle_base": 0.34964812124533645,
  "loss_turn_bundle_base": 0.31809829208944423,
  "loss_theta_bundle_base": 0.00022846741745335394,
  "loss_main_bundle": 0.34964812124533645,
  "loss_turn_bundle": 0.31809829208944423,
  "loss_theta_bundle": 0.00022846741745335394,
  "loss_theta_flat": 0.00018784823836853054,
  "loss_theta_near_flat": 0.0010649050830255978,
  "loss_theta_error_excess": 0.00012189018144012342,
  "loss_theta_flat_excess": 0.00011006948841253361,
  "loss_theta_near_flat_excess": 0.0007463007963877499,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.97830196369423e-05,
  "loss_theta_small_neg": 0.00019812660835430036,
  "loss_theta_small_neg_excess": 4.202262642726801e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3568765092686484,
  "loss_false_turn_straight": 0.2954294638398213,
  "loss_transition_focal_raw": 1.4314634215041329,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.381130552654666,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
