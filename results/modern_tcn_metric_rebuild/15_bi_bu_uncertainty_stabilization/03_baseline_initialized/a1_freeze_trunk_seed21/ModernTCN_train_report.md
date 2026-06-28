# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `bounded_uncertainty`
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

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9661 |
| acc_turn | 0.5994 |
| acc_turn_pure | 0.6169 |
| acc_turn_transition | 0.5231 |
| main_confidence_mean | 0.9885 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0147 |
| turn_confidence_mean | 0.8259 |
| turn_low_conf_0p60_ratio | 0.1532 |
| turn_low_conf_0p70_ratio | 0.2710 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.6017 |
| turn_left_recall | 0.5874 |
| theta_mae_deg | 0.6378 |
| theta_abs_le_10_p95_abs_err_deg | 1.6836 |
| theta_neg_10_8_p95_abs_err_deg | 1.2294 |
| theta_pos_8_10_p95_abs_err_deg | 2.3328 |
| theta_abs_le_8_p95_abs_err_deg | 1.6572 |
| theta_neg_8_6_p95_abs_err_deg | 1.6313 |
| theta_pos_6_8_p95_abs_err_deg | 1.4718 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4658 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5464 |
| theta_flat_abs_p95_deg | 2.4094 |
| theta_flat_bias_deg | -0.1363 |
| theta_near_flat_abs_p95_deg | 2.0460 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3035 |
| theta_flat_turn_abs_p95_deg | 1.9918 |
| flat_recall | 0.9669 |
| stall_recall | 0.6979 |
| slope_recall | 0.9753 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7506 |
| downhill_recall | 0.7934 |

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
    9,
    67,
    20
  ],
  [
    62,
    6,
    2682
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    485,
    198,
    116
  ],
  [
    380,
    1163,
    390
  ],
  [
    168,
    191,
    511
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.340899 |
| test_loss_turn_bundle_base | 0.298731 |
| test_loss_theta_bundle_base | 0.000144 |
| test_loss_transition_focal_raw | 1.424347 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.730984 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 3.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.4783 | 0.5513 |
| [0.60,0.70) | 30 | 0.5667 | 0.6574 |
| [0.70,0.80) | 26 | 0.5769 | 0.7573 |
| [0.80,0.90) | 47 | 0.3404 | 0.8567 |
| [0.90,1.00) | 3476 | 0.0181 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 552 | 0.5453 | 0.5214 |
| [0.60,0.70) | 424 | 0.5259 | 0.6513 |
| [0.70,0.80) | 404 | 0.4950 | 0.7502 |
| [0.80,0.90) | 492 | 0.4431 | 0.8517 |
| [0.90,1.00) | 1730 | 0.2896 | 0.9761 |


## 验证集最佳点

```json
{
  "loss_total": 0.571221049196504,
  "acc_main": 0.9488497970230041,
  "acc_turn": 0.6300405953991881,
  "acc_turn_pure": 0.6453621763356276,
  "acc_turn_transition": 0.5574534161490683,
  "false_turn_straight": 0.4183991683991684,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.5,
  "slope_recall": 0.9546061415220294,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9512937595129376,
    0.5,
    0.9546061415220294
  ],
  "turn_right_recall": 0.6706161137440758,
  "turn_straight_recall": 0.5816008316008316,
  "turn_left_recall": 0.6936353829557713,
  "recall_turn": [
    0.6706161137440758,
    0.5816008316008316,
    0.6936353829557713
  ],
  "cm_turn": [
    [
      566,
      229,
      49
    ],
    [
      402,
      1119,
      403
    ],
    [
      92,
      192,
      643
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
      0,
      21,
      21
    ],
    [
      129,
      7,
      2860
    ]
  ],
  "main_confidence_mean": 0.9679122119744481,
  "main_confidence_error_mean": 0.7406889909434319,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.5266580296050707
    },
    {
      "bin": "[0.60,0.70)",
      "n": 29,
      "error_rate": 0.4482758620689655,
      "mean_confidence": 0.6298452909499418
    },
    {
      "bin": "[0.70,0.80)",
      "n": 23,
      "error_rate": 0.34782608695652173,
      "mean_confidence": 0.7541757321766446
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.2553191489361702,
      "mean_confidence": 0.8496265197178888
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3414,
      "error_rate": 0.0210896309314587,
      "mean_confidence": 0.9973754716324286
    }
  ],
  "turn_confidence_mean": 0.8376862972521519,
  "turn_confidence_error_mean": 0.7658176735889444,
  "turn_low_conf_0p60_ratio": 0.16184032476319352,
  "turn_low_conf_0p70_ratio": 0.2503382949932341,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 598,
      "error_rate": 0.617056856187291,
      "mean_confidence": 0.5173340674615146
    },
    {
      "bin": "[0.60,0.70)",
      "n": 327,
      "error_rate": 0.4617737003058104,
      "mean_confidence": 0.6492980675605777
    },
    {
      "bin": "[0.70,0.80)",
      "n": 348,
      "error_rate": 0.5028735632183908,
      "mean_confidence": 0.7505718417107454
    },
    {
      "bin": "[0.80,0.90)",
      "n": 460,
      "error_rate": 0.4043478260869565,
      "mean_confidence": 0.8527698116401419
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1962,
      "error_rate": 0.24770642201834864,
      "mean_confidence": 0.9786399152102968
    }
  ],
  "theta_mae_rad": 0.01375736016780138,
  "theta_mae_deg": 0.7882386445999146,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.803670745272525,
  "slope_sign_acc": 0.9791951820421572,
  "theta_flat_mae_deg": 1.1152198314666748,
  "theta_flat_abs_p95_deg": 4.163838863372803,
  "theta_flat_abs_max_deg": 8.245522499084473,
  "theta_flat_bias_deg": 0.27822670340538025,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4607895612716675,
  "theta_near_flat_abs_p95_deg": 4.169568061828613,
  "theta_near_flat_abs_max_deg": 8.245522499084473,
  "theta_near_flat_bias_deg": 0.5509979724884033,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.075782060623169,
  "theta_flat_turn_abs_p95_deg": 4.163838863372803,
  "theta_flat_turn_abs_max_deg": 8.245522499084473,
  "theta_flat_turn_bias_deg": -0.10255303233861923,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7882386445999146,
  "theta_slope_control_abs_p95_deg": 9.054744720458984,
  "theta_slope_control_abs_max_deg": 12.607345581054688,
  "theta_slope_control_bias_deg": 0.12093722075223923,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7882386445999146,
  "theta_all_rmse_deg": 1.1943551301956177,
  "theta_all_p95_abs_err_deg": 2.6638388633728027,
  "theta_all_max_abs_err_deg": 7.745522975921631,
  "theta_all_bias_deg": 0.12093722075223923,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7165341377258301,
  "theta_active_abs_ge_2_rmse_deg": 1.058634877204895,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1534066200256348,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.019725322723389,
  "theta_active_abs_ge_2_bias_deg": 0.08644483238458633,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.82591712474823,
  "theta_abs_le_8_rmse_deg": 1.2322468757629395,
  "theta_abs_le_8_p95_abs_err_deg": 2.7792069911956787,
  "theta_abs_le_8_max_abs_err_deg": 7.745522975921631,
  "theta_abs_le_8_bias_deg": 0.14168781042099,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7882386445999146,
  "theta_abs_le_10_rmse_deg": 1.1943551301956177,
  "theta_abs_le_10_p95_abs_err_deg": 2.6638388633728027,
  "theta_abs_le_10_max_abs_err_deg": 7.745522975921631,
  "theta_abs_le_10_bias_deg": 0.12093722075223923,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5542494058609009,
  "theta_pos_8_10_rmse_deg": 0.7476117014884949,
  "theta_pos_8_10_p95_abs_err_deg": 1.4071449041366577,
  "theta_pos_8_10_max_abs_err_deg": 3.974492311477661,
  "theta_pos_8_10_bias_deg": -0.34192851185798645,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7056268453598022,
  "theta_neg_10_8_rmse_deg": 1.2355400323867798,
  "theta_neg_10_8_p95_abs_err_deg": 2.3326199054718018,
  "theta_neg_10_8_max_abs_err_deg": 7.019725322723389,
  "theta_neg_10_8_bias_deg": 0.41521692276000977,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.4897136390209198,
  "theta_pos_6_8_rmse_deg": 0.6880226135253906,
  "theta_pos_6_8_p95_abs_err_deg": 1.4404678344726562,
  "theta_pos_6_8_max_abs_err_deg": 3.03830623626709,
  "theta_pos_6_8_bias_deg": -0.02997896820306778,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7977150678634644,
  "theta_neg_8_6_rmse_deg": 1.1573365926742554,
  "theta_neg_8_6_p95_abs_err_deg": 2.052055835723877,
  "theta_neg_8_6_max_abs_err_deg": 6.372982025146484,
  "theta_neg_8_6_bias_deg": -0.11306986212730408,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7035075426101685,
  "theta_neg_4_2_rmse_deg": 0.9769959449768066,
  "theta_neg_4_2_p95_abs_err_deg": 2.0488126277923584,
  "theta_neg_4_2_max_abs_err_deg": 3.7812817096710205,
  "theta_neg_4_2_bias_deg": 0.12498878687620163,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6415622234344482,
  "theta_neg_2_0p5_rmse_deg": 0.9231693148612976,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.0506086349487305,
  "theta_neg_2_0p5_max_abs_err_deg": 4.786978721618652,
  "theta_neg_2_0p5_bias_deg": -0.4177209734916687,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1934022903442383,
  "theta_pos_0p5_2_rmse_deg": 1.5437405109405518,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6638388633728027,
  "theta_pos_0p5_2_max_abs_err_deg": 3.8836257457733154,
  "theta_pos_0p5_2_bias_deg": 0.8118506073951721,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3104366405890985,
  "loss_turn": 1.30257701606002,
  "loss_theta": 0.00043461492739766533,
  "loss_main_bundle_base": 0.3104366405890985,
  "loss_turn_bundle_base": 0.26051540621965924,
  "loss_theta_bundle_base": 0.0002689990478552656,
  "loss_main_bundle": 0.3104366405890985,
  "loss_turn_bundle": 0.26051540621965924,
  "loss_theta_bundle": 0.0002689990478552656,
  "loss_theta_flat": 0.00024967360910764204,
  "loss_theta_near_flat": 0.0014912117184398138,
  "loss_theta_error_excess": 0.0001600749162829157,
  "loss_theta_flat_excess": 0.0001383776587652451,
  "loss_theta_near_flat_excess": 0.001087466309966169,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001074177983536099,
  "loss_theta_small_neg": 0.0002894790137705868,
  "loss_theta_small_neg_excess": 6.406716744041168e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.372641202835656,
  "loss_false_turn_straight": 0.30715281563295566,
  "loss_transition_focal_raw": 1.146112273413693,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.072139005085238,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.0012393780052661896
}
```
