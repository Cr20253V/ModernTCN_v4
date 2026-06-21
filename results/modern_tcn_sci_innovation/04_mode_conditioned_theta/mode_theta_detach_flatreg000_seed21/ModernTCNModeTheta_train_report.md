# ModernTCN-small mode-conditioned theta experts 训练报告

## 固定约束

- model_family: `small_mode_theta`
- loss_mode: `fixed`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## E4 Mode-Conditioned Theta Experts

- theta fusion: `sum(softmax(main_logits) * theta_experts)`.
- theta_gate_detach: `True`
- flat_theta_reg_lambda: `0.000000`
- theta_expert_hidden: `0`

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
  "theta_gate_detach": true,
  "flat_theta_reg_lambda": 0.0,
  "theta_expert_hidden": 0
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9703 |
| acc_turn | 0.5875 |
| acc_turn_pure | 0.6059 |
| acc_turn_transition | 0.5067 |
| main_confidence_mean | 0.9868 |
| main_low_conf_0p60_ratio | 0.0081 |
| main_low_conf_0p70_ratio | 0.0158 |
| turn_confidence_mean | 0.8217 |
| turn_low_conf_0p60_ratio | 0.1713 |
| turn_low_conf_0p70_ratio | 0.2835 |
| turn_right_recall | 0.6408 |
| turn_straight_recall | 0.5913 |
| turn_left_recall | 0.5299 |
| theta_mae_deg | 0.6515 |
| theta_abs_le_10_p95_abs_err_deg | 1.8495 |
| theta_neg_10_8_p95_abs_err_deg | 1.2058 |
| theta_pos_8_10_p95_abs_err_deg | 3.6929 |
| theta_abs_le_8_p95_abs_err_deg | 1.6597 |
| theta_neg_8_6_p95_abs_err_deg | 1.3028 |
| theta_pos_6_8_p95_abs_err_deg | 1.5133 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.3753 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0375 |
| theta_flat_abs_p95_deg | 2.6265 |
| theta_flat_bias_deg | 0.1755 |
| theta_near_flat_abs_p95_deg | 1.5225 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.4042 |
| theta_flat_turn_abs_p95_deg | 1.5683 |
| flat_recall | 0.9683 |
| stall_recall | 0.6979 |
| slope_recall | 0.9804 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7643 |
| downhill_recall | 0.7872 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    732,
    0,
    24
  ],
  [
    9,
    67,
    20
  ],
  [
    41,
    13,
    2696
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    512,
    195,
    92
  ],
  [
    430,
    1143,
    360
  ],
  [
    160,
    249,
    461
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.300476 |
| test_loss_turn_bundle_base | 0.305720 |
| test_loss_theta_bundle_base | 0.000409 |
| test_loss_transition_focal_raw | 1.340960 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.154466 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000511 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 66
- train_seconds: 310.5

## E3 Gate Statistics

| metric | value |
|---|---:|
| test_gate_all_finite | nan |
| test_gate_single_collapse | nan |
| test_gate_mean_entropy | nan |
| test_gate_interpretability_score | nan |
| test_gate_yaw_transition_minus_overall | nan |
| test_gate_drive_stall_minus_overall | nan |
| test_gate_velocity_slope_flat_abs_delta | nan |

```json
{}
```

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 29 | 0.4828 | 0.5541 |
| [0.60,0.70) | 28 | 0.2857 | 0.6546 |
| [0.70,0.80) | 38 | 0.1842 | 0.7545 |
| [0.80,0.90) | 45 | 0.2667 | 0.8557 |
| [0.90,1.00) | 3462 | 0.0191 | 0.9974 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 617 | 0.5997 | 0.5270 |
| [0.60,0.70) | 404 | 0.5371 | 0.6506 |
| [0.70,0.80) | 385 | 0.5662 | 0.7534 |
| [0.80,0.90) | 508 | 0.4587 | 0.8530 |
| [0.90,1.00) | 1688 | 0.2654 | 0.9765 |


## 验证集最佳点

```json
{
  "loss_total": 0.5628637621786662,
  "acc_main": 0.9456021650879567,
  "acc_turn": 0.6514208389715832,
  "acc_turn_pure": 0.6617502458210422,
  "acc_turn_transition": 0.6024844720496895,
  "false_turn_straight": 0.3814968814968815,
  "flat_recall": 0.969558599695586,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9492656875834445,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.047619047619047616,
  "recall_main": [
    0.969558599695586,
    0.30952380952380953,
    0.9492656875834445
  ],
  "turn_right_recall": 0.716824644549763,
  "turn_straight_recall": 0.6185031185031185,
  "turn_left_recall": 0.6601941747572816,
  "recall_turn": [
    0.716824644549763,
    0.6185031185031185,
    0.6601941747572816
  ],
  "cm_turn": [
    [
      605,
      195,
      44
    ],
    [
      400,
      1190,
      334
    ],
    [
      88,
      227,
      612
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      637,
      0,
      20
    ],
    [
      2,
      13,
      27
    ],
    [
      137,
      15,
      2844
    ]
  ],
  "main_confidence_mean": 0.971550162001401,
  "main_confidence_error_mean": 0.7762326999173939,
  "main_low_conf_0p60_ratio": 0.0489851150202977,
  "main_low_conf_0p70_ratio": 0.05331529093369418,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 181,
      "error_rate": 0.4696132596685083,
      "mean_confidence": 0.548360572208755
    },
    {
      "bin": "[0.60,0.70)",
      "n": 16,
      "error_rate": 0.4375,
      "mean_confidence": 0.6488903827985113
    },
    {
      "bin": "[0.70,0.80)",
      "n": 19,
      "error_rate": 0.2631578947368421,
      "mean_confidence": 0.7480793128818558
    },
    {
      "bin": "[0.80,0.90)",
      "n": 31,
      "error_rate": 0.3548387096774194,
      "mean_confidence": 0.8483321058619302
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3448,
      "error_rate": 0.02697215777262181,
      "mean_confidence": 0.9976016637686022
    }
  ],
  "turn_confidence_mean": 0.8348282859194222,
  "turn_confidence_error_mean": 0.750726225108225,
  "turn_low_conf_0p60_ratio": 0.17320703653585928,
  "turn_low_conf_0p70_ratio": 0.260893098782138,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 640,
      "error_rate": 0.609375,
      "mean_confidence": 0.5128011225669648
    },
    {
      "bin": "[0.60,0.70)",
      "n": 324,
      "error_rate": 0.5154320987654321,
      "mean_confidence": 0.6525990396549823
    },
    {
      "bin": "[0.70,0.80)",
      "n": 343,
      "error_rate": 0.42565597667638483,
      "mean_confidence": 0.7524852606757882
    },
    {
      "bin": "[0.80,0.90)",
      "n": 392,
      "error_rate": 0.3903061224489796,
      "mean_confidence": 0.8508973063736265
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1996,
      "error_rate": 0.21643286573146292,
      "mean_confidence": 0.9786580764884449
    }
  ],
  "theta_mae_rad": 0.014047524891793728,
  "theta_mae_deg": 0.8048638701438904,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.7908787541713015,
  "slope_sign_acc": 0.963044073364358,
  "theta_flat_mae_deg": 1.1264601945877075,
  "theta_flat_abs_p95_deg": 4.211609840393066,
  "theta_flat_abs_max_deg": 9.720921516418457,
  "theta_flat_bias_deg": 0.8571515083312988,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5247153043746948,
  "theta_near_flat_abs_p95_deg": 4.372113227844238,
  "theta_near_flat_abs_max_deg": 9.720921516418457,
  "theta_near_flat_bias_deg": 1.1926803588867188,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3394805192947388,
  "theta_flat_turn_abs_p95_deg": 4.928560733795166,
  "theta_flat_turn_abs_max_deg": 9.720921516418457,
  "theta_flat_turn_bias_deg": 0.8825599551200867,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8048638701438904,
  "theta_slope_control_abs_p95_deg": 9.362735748291016,
  "theta_slope_control_abs_max_deg": 34.13869094848633,
  "theta_slope_control_bias_deg": 0.09583967179059982,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8048638105392456,
  "theta_all_rmse_deg": 1.4714224338531494,
  "theta_all_p95_abs_err_deg": 2.8367486000061035,
  "theta_all_max_abs_err_deg": 26.683612823486328,
  "theta_all_bias_deg": 0.09583967179059982,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7343401908874512,
  "theta_active_abs_ge_2_rmse_deg": 1.3895682096481323,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4427995681762695,
  "theta_active_abs_ge_2_max_abs_err_deg": 26.683612823486328,
  "theta_active_abs_ge_2_bias_deg": -0.07111021131277084,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8444669842720032,
  "theta_abs_le_8_rmse_deg": 1.5057705640792847,
  "theta_abs_le_8_p95_abs_err_deg": 2.8954050540924072,
  "theta_abs_le_8_max_abs_err_deg": 26.683612823486328,
  "theta_abs_le_8_bias_deg": 0.1257004737854004,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8048638105392456,
  "theta_abs_le_10_rmse_deg": 1.4714224338531494,
  "theta_abs_le_10_p95_abs_err_deg": 2.8367486000061035,
  "theta_abs_le_10_max_abs_err_deg": 26.683612823486328,
  "theta_abs_le_10_bias_deg": 0.09583967179059982,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6489822864532471,
  "theta_pos_8_10_rmse_deg": 1.4135026931762695,
  "theta_pos_8_10_p95_abs_err_deg": 1.4453871250152588,
  "theta_pos_8_10_max_abs_err_deg": 19.078739166259766,
  "theta_pos_8_10_bias_deg": -0.20657818019390106,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.626414954662323,
  "theta_neg_10_8_rmse_deg": 1.2102972269058228,
  "theta_neg_10_8_p95_abs_err_deg": 2.251371145248413,
  "theta_neg_10_8_max_abs_err_deg": 7.813429355621338,
  "theta_neg_10_8_bias_deg": 0.14936873316764832,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6782562732696533,
  "theta_pos_6_8_rmse_deg": 1.0543522834777832,
  "theta_pos_6_8_p95_abs_err_deg": 2.3531975746154785,
  "theta_pos_6_8_max_abs_err_deg": 6.565696716308594,
  "theta_pos_6_8_bias_deg": -0.09940334409475327,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7625611424446106,
  "theta_neg_8_6_rmse_deg": 1.7277835607528687,
  "theta_neg_8_6_p95_abs_err_deg": 1.9321693181991577,
  "theta_neg_8_6_max_abs_err_deg": 26.683612823486328,
  "theta_neg_8_6_bias_deg": -0.22139468789100647,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6711803674697876,
  "theta_neg_4_2_rmse_deg": 1.1264935731887817,
  "theta_neg_4_2_p95_abs_err_deg": 2.4557602405548096,
  "theta_neg_4_2_max_abs_err_deg": 5.855589389801025,
  "theta_neg_4_2_bias_deg": -0.08753824979066849,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5721877217292786,
  "theta_neg_2_0p5_rmse_deg": 0.7815141081809998,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3070876598358154,
  "theta_neg_2_0p5_max_abs_err_deg": 5.234719753265381,
  "theta_neg_2_0p5_bias_deg": 0.3773159682750702,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.246901035308838,
  "theta_pos_0p5_2_rmse_deg": 1.6039612293243408,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.7115964889526367,
  "theta_pos_0p5_2_max_abs_err_deg": 4.900625228881836,
  "theta_pos_0p5_2_bias_deg": 1.038147211074829,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3165523393550971,
  "loss_turn": 1.2293045120407022,
  "loss_theta": 0.0006596150198549344,
  "loss_main_bundle_base": 0.3165523393550971,
  "loss_turn_bundle_base": 0.24586090612476025,
  "loss_theta_bundle_base": 0.00045051817998513125,
  "loss_main_bundle": 0.3165523393550971,
  "loss_turn_bundle": 0.24586090612476025,
  "loss_theta_bundle": 0.00045051817998513125,
  "loss_theta_flat": 0.00030254714524295277,
  "loss_theta_near_flat": 0.0016589927278031849,
  "loss_theta_error_excess": 0.0003668642399921769,
  "loss_theta_flat_excess": 0.00017841628562592743,
  "loss_theta_near_flat_excess": 0.0012705121319555124,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00033081030230594266,
  "loss_theta_small_neg": 0.0003873711114456935,
  "loss_theta_small_neg_excess": 0.0001613377225229262,
  "loss_flat_theta_expert_reg": 0.0013304790303600052,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3597867829631888,
  "loss_false_turn_straight": 0.28325639735700636,
  "loss_transition_focal_raw": 1.0167090103171352,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.401344362679612,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
