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
  "lambda_turn": 0.08,
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
    1.08,
    1.0,
    1.08
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.4,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.2,
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
| acc_main | 0.9645 |
| acc_turn | 0.5805 |
| acc_turn_pure | 0.6025 |
| acc_turn_transition | 0.4844 |
| main_confidence_mean | 0.9870 |
| main_low_conf_0p60_ratio | 0.0061 |
| main_low_conf_0p70_ratio | 0.0153 |
| turn_confidence_mean | 0.7953 |
| turn_low_conf_0p60_ratio | 0.2057 |
| turn_low_conf_0p70_ratio | 0.3293 |
| turn_right_recall | 0.5382 |
| turn_straight_recall | 0.6182 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.5960 |
| theta_abs_le_10_p95_abs_err_deg | 1.8158 |
| theta_neg_10_8_p95_abs_err_deg | 2.1130 |
| theta_pos_8_10_p95_abs_err_deg | 2.5479 |
| theta_abs_le_8_p95_abs_err_deg | 1.5100 |
| theta_neg_8_6_p95_abs_err_deg | 1.5226 |
| theta_pos_6_8_p95_abs_err_deg | 1.3822 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3158 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2744 |
| theta_flat_abs_p95_deg | 2.1899 |
| theta_flat_bias_deg | -0.1611 |
| theta_near_flat_abs_p95_deg | 1.8346 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1264 |
| theta_flat_turn_abs_p95_deg | 1.5996 |
| flat_recall | 0.9669 |
| stall_recall | 0.6979 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0729 |
| uphill_recall | 0.7523 |
| downhill_recall | 0.7883 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    731,
    0,
    25
  ],
  [
    7,
    67,
    22
  ],
  [
    66,
    8,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    430,
    252,
    117
  ],
  [
    334,
    1195,
    404
  ],
  [
    165,
    239,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.315586 |
| test_loss_turn_bundle_base | 0.116099 |
| test_loss_theta_bundle_base | 0.000146 |
| test_loss_transition_focal_raw | 1.272447 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.685460 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 75
- train_seconds: 1619.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 22 | 0.5000 | 0.5402 |
| [0.60,0.70) | 33 | 0.7576 | 0.6483 |
| [0.70,0.80) | 40 | 0.4250 | 0.7457 |
| [0.80,0.90) | 50 | 0.2200 | 0.8524 |
| [0.90,1.00) | 3457 | 0.0185 | 0.9978 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 741 | 0.6005 | 0.5174 |
| [0.60,0.70) | 445 | 0.5169 | 0.6483 |
| [0.70,0.80) | 449 | 0.4833 | 0.7512 |
| [0.80,0.90) | 503 | 0.4473 | 0.8493 |
| [0.90,1.00) | 1464 | 0.2691 | 0.9756 |


## 验证集最佳点

```json
{
  "loss_total": 0.4093563383099836,
  "acc_main": 0.9415426251691476,
  "acc_turn": 0.6462787550744249,
  "acc_turn_pure": 0.6561783021960013,
  "acc_turn_transition": 0.5993788819875776,
  "false_turn_straight": 0.3575883575883576,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.2619047619047619,
  "slope_recall": 0.9489319092122831,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.16666666666666666,
  "recall_main": [
    0.9512937595129376,
    0.2619047619047619,
    0.9489319092122831
  ],
  "turn_right_recall": 0.6457345971563981,
  "turn_straight_recall": 0.6424116424116424,
  "turn_left_recall": 0.6548004314994607,
  "recall_turn": [
    0.6457345971563981,
    0.6424116424116424,
    0.6548004314994607
  ],
  "cm_turn": [
    [
      545,
      254,
      45
    ],
    [
      331,
      1236,
      357
    ],
    [
      82,
      238,
      607
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      625,
      0,
      32
    ],
    [
      7,
      11,
      24
    ],
    [
      143,
      10,
      2843
    ]
  ],
  "main_confidence_mean": 0.9672697080980667,
  "main_confidence_error_mean": 0.765101427671855,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.06035182679296346,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4587628865979381,
      "mean_confidence": 0.5390980943985993
    },
    {
      "bin": "[0.60,0.70)",
      "n": 29,
      "error_rate": 0.3793103448275862,
      "mean_confidence": 0.6500888117175533
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.3103448275862069,
      "mean_confidence": 0.75316185203386
    },
    {
      "bin": "[0.80,0.90)",
      "n": 43,
      "error_rate": 0.37209302325581395,
      "mean_confidence": 0.8575726973778581
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3400,
      "error_rate": 0.02676470588235294,
      "mean_confidence": 0.9976196017273496
    }
  ],
  "turn_confidence_mean": 0.8167684887903068,
  "turn_confidence_error_mean": 0.7387136419750449,
  "turn_low_conf_0p60_ratio": 0.1780784844384303,
  "turn_low_conf_0p70_ratio": 0.27253044654939107,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 658,
      "error_rate": 0.5790273556231003,
      "mean_confidence": 0.48886449049217257
    },
    {
      "bin": "[0.60,0.70)",
      "n": 349,
      "error_rate": 0.4813753581661891,
      "mean_confidence": 0.6485262259650887
    },
    {
      "bin": "[0.70,0.80)",
      "n": 433,
      "error_rate": 0.3787528868360277,
      "mean_confidence": 0.7498651490652675
    },
    {
      "bin": "[0.80,0.90)",
      "n": 485,
      "error_rate": 0.42061855670103093,
      "mean_confidence": 0.8529668300229682
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1770,
      "error_rate": 0.22033898305084745,
      "mean_confidence": 0.9782884499254905
    }
  ],
  "theta_mae_rad": 0.012882648967206478,
  "theta_mae_deg": 0.7381213903427124,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.7975528364849833,
  "slope_sign_acc": 0.9756364631809472,
  "theta_flat_mae_deg": 0.9558821320533752,
  "theta_flat_abs_p95_deg": 3.562722682952881,
  "theta_flat_abs_max_deg": 6.211294651031494,
  "theta_flat_bias_deg": 0.24961403012275696,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2722936868667603,
  "theta_near_flat_abs_p95_deg": 3.6362156867980957,
  "theta_near_flat_abs_max_deg": 6.211294651031494,
  "theta_near_flat_bias_deg": 0.7283208966255188,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9754876494407654,
  "theta_flat_turn_abs_p95_deg": 4.098891735076904,
  "theta_flat_turn_abs_max_deg": 6.211294651031494,
  "theta_flat_turn_bias_deg": 0.3382568359375,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7381213903427124,
  "theta_slope_control_abs_p95_deg": 9.061799049377441,
  "theta_slope_control_abs_max_deg": 12.745542526245117,
  "theta_slope_control_bias_deg": -0.1760694682598114,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7381213903427124,
  "theta_all_rmse_deg": 1.0915693044662476,
  "theta_all_p95_abs_err_deg": 2.3275558948516846,
  "theta_all_max_abs_err_deg": 5.9200873374938965,
  "theta_all_bias_deg": -0.1760694682598114,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6903680562973022,
  "theta_active_abs_ge_2_rmse_deg": 0.9951180219650269,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9057499170303345,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.9200873374938965,
  "theta_active_abs_ge_2_bias_deg": -0.2694186270236969,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7493077516555786,
  "theta_abs_le_8_rmse_deg": 1.112856149673462,
  "theta_abs_le_8_p95_abs_err_deg": 2.4434127807617188,
  "theta_abs_le_8_max_abs_err_deg": 5.9200873374938965,
  "theta_abs_le_8_bias_deg": -0.1648062914609909,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7381213903427124,
  "theta_abs_le_10_rmse_deg": 1.0915693044662476,
  "theta_abs_le_10_p95_abs_err_deg": 2.3275558948516846,
  "theta_abs_le_10_max_abs_err_deg": 5.9200873374938965,
  "theta_abs_le_10_bias_deg": -0.1760694682598114,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7157906889915466,
  "theta_pos_8_10_rmse_deg": 0.9135478138923645,
  "theta_pos_8_10_p95_abs_err_deg": 1.543960452079773,
  "theta_pos_8_10_max_abs_err_deg": 5.405610084533691,
  "theta_pos_8_10_bias_deg": -0.5701850056648254,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6656414270401001,
  "theta_neg_10_8_rmse_deg": 1.0748544931411743,
  "theta_neg_10_8_p95_abs_err_deg": 2.298705577850342,
  "theta_neg_10_8_max_abs_err_deg": 5.896070957183838,
  "theta_neg_10_8_bias_deg": 0.12901005148887634,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6574127674102783,
  "theta_pos_6_8_rmse_deg": 0.8300036191940308,
  "theta_pos_6_8_p95_abs_err_deg": 1.5877951383590698,
  "theta_pos_6_8_max_abs_err_deg": 3.163188934326172,
  "theta_pos_6_8_bias_deg": -0.4444679915904999,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7501473426818848,
  "theta_neg_8_6_rmse_deg": 1.1112022399902344,
  "theta_neg_8_6_p95_abs_err_deg": 2.0545239448547363,
  "theta_neg_8_6_max_abs_err_deg": 5.492328643798828,
  "theta_neg_8_6_bias_deg": -0.012696249410510063,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8227353096008301,
  "theta_neg_4_2_rmse_deg": 1.283071756362915,
  "theta_neg_4_2_p95_abs_err_deg": 2.841343641281128,
  "theta_neg_4_2_max_abs_err_deg": 5.9200873374938965,
  "theta_neg_4_2_bias_deg": -0.5571348071098328,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5892304182052612,
  "theta_neg_2_0p5_rmse_deg": 0.8327587246894836,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6951096057891846,
  "theta_neg_2_0p5_max_abs_err_deg": 3.863192319869995,
  "theta_neg_2_0p5_bias_deg": -0.36156174540519714,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9915962219238281,
  "theta_pos_0p5_2_rmse_deg": 1.2832748889923096,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0943315029144287,
  "theta_pos_0p5_2_max_abs_err_deg": 4.318543434143066,
  "theta_pos_0p5_2_bias_deg": 0.2902466058731079,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.30261277038609063,
  "loss_turn": 1.331310066221854,
  "loss_theta": 0.0003628810334582693,
  "loss_main_bundle_base": 0.30261277038609063,
  "loss_turn_bundle_base": 0.10650480301478557,
  "loss_theta_bundle_base": 0.00023875701311611505,
  "loss_main_bundle": 0.30261277038609063,
  "loss_turn_bundle": 0.10650480301478557,
  "loss_theta_bundle": 0.00023875701311611505,
  "loss_theta_flat": 0.0002035665465471573,
  "loss_theta_near_flat": 0.0010919201739147527,
  "loss_theta_error_excess": 0.00011915774566672128,
  "loss_theta_flat_excess": 0.00010714557440841687,
  "loss_theta_near_flat_excess": 0.0007572684187192536,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.78656638843853e-05,
  "loss_theta_small_neg": 0.0005017988512000127,
  "loss_theta_small_neg_excess": 0.00019042652266677243,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3104224146783594,
  "loss_false_turn_straight": 0.25273079730177117,
  "loss_transition_focal_raw": 1.1005634409648963,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.9687332421742854,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
