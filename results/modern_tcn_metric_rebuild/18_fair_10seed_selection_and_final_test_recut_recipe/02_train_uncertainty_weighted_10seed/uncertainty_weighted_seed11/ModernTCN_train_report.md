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
| acc_main | 0.9656 |
| acc_turn | 0.5527 |
| acc_turn_pure | 0.5660 |
| acc_turn_transition | 0.4948 |
| main_confidence_mean | 0.9841 |
| main_low_conf_0p60_ratio | 0.0114 |
| main_low_conf_0p70_ratio | 0.0208 |
| turn_confidence_mean | 0.7518 |
| turn_low_conf_0p60_ratio | 0.2629 |
| turn_low_conf_0p70_ratio | 0.4200 |
| turn_right_recall | 0.6333 |
| turn_straight_recall | 0.5272 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.7523 |
| theta_abs_le_10_p95_abs_err_deg | 2.0871 |
| theta_neg_10_8_p95_abs_err_deg | 1.6493 |
| theta_pos_8_10_p95_abs_err_deg | 3.4708 |
| theta_abs_le_8_p95_abs_err_deg | 2.0043 |
| theta_neg_8_6_p95_abs_err_deg | 1.5447 |
| theta_pos_6_8_p95_abs_err_deg | 1.9426 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.1780 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9381 |
| theta_flat_abs_p95_deg | 2.8591 |
| theta_flat_bias_deg | -0.1173 |
| theta_near_flat_abs_p95_deg | 1.7795 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0035 |
| theta_flat_turn_abs_p95_deg | 1.8058 |
| flat_recall | 0.9563 |
| stall_recall | 0.6354 |
| slope_recall | 0.9796 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7592 |
| downhill_recall | 0.7963 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    723,
    0,
    33
  ],
  [
    8,
    61,
    27
  ],
  [
    47,
    9,
    2694
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    506,
    173,
    120
  ],
  [
    437,
    1019,
    477
  ],
  [
    211,
    193,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.350042 |
| test_loss_turn_bundle_base | 0.241468 |
| test_loss_theta_bundle_base | 0.000227 |
| test_loss_transition_focal_raw | 0.956546 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.183750 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 43
- train_seconds: 227.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 41 | 0.6098 | 0.5343 |
| [0.60,0.70) | 34 | 0.3529 | 0.6571 |
| [0.70,0.80) | 36 | 0.5000 | 0.7537 |
| [0.80,0.90) | 45 | 0.1556 | 0.8533 |
| [0.90,1.00) | 3446 | 0.0180 | 0.9968 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 947 | 0.5977 | 0.5110 |
| [0.60,0.70) | 566 | 0.5512 | 0.6526 |
| [0.70,0.80) | 497 | 0.4909 | 0.7517 |
| [0.80,0.90) | 495 | 0.4566 | 0.8496 |
| [0.90,1.00) | 1097 | 0.2397 | 0.9667 |


## 验证集最佳点

```json
{
  "loss_total": 0.518729847774454,
  "acc_main": 0.945872801082544,
  "acc_turn": 0.6029769959404601,
  "acc_turn_pure": 0.6148803670927565,
  "acc_turn_transition": 0.546583850931677,
  "false_turn_straight": 0.4979209979209979,
  "flat_recall": 0.958904109589041,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.951935914552737,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.047619047619047616,
  "recall_main": [
    0.958904109589041,
    0.30952380952380953,
    0.951935914552737
  ],
  "turn_right_recall": 0.7156398104265402,
  "turn_straight_recall": 0.502079002079002,
  "turn_left_recall": 0.7098166127292341,
  "recall_turn": [
    0.7156398104265402,
    0.502079002079002,
    0.7098166127292341
  ],
  "cm_turn": [
    [
      604,
      169,
      71
    ],
    [
      493,
      966,
      465
    ],
    [
      124,
      145,
      658
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      630,
      0,
      27
    ],
    [
      2,
      13,
      27
    ],
    [
      138,
      6,
      2852
    ]
  ],
  "main_confidence_mean": 0.9672914685915207,
  "main_confidence_error_mean": 0.7565949113669029,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.056562922868741546,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.4708994708994709,
      "mean_confidence": 0.5388438837925427
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.35,
      "mean_confidence": 0.6551750564693545
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.2647058823529412,
      "mean_confidence": 0.7512819941596858
    },
    {
      "bin": "[0.80,0.90)",
      "n": 57,
      "error_rate": 0.21052631578947367,
      "mean_confidence": 0.8510537114583508
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3395,
      "error_rate": 0.024447717231222386,
      "mean_confidence": 0.9970967104344437
    }
  ],
  "turn_confidence_mean": 0.7691197962526098,
  "turn_confidence_error_mean": 0.6990080640300578,
  "turn_low_conf_0p60_ratio": 0.22273342354533152,
  "turn_low_conf_0p70_ratio": 0.36535859269282817,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 823,
      "error_rate": 0.5941676792223572,
      "mean_confidence": 0.485209824714547
    },
    {
      "bin": "[0.60,0.70)",
      "n": 527,
      "error_rate": 0.444022770398482,
      "mean_confidence": 0.6545139044854663
    },
    {
      "bin": "[0.70,0.80)",
      "n": 514,
      "error_rate": 0.45330739299610895,
      "mean_confidence": 0.7502994526896284
    },
    {
      "bin": "[0.80,0.90)",
      "n": 548,
      "error_rate": 0.43795620437956206,
      "mean_confidence": 0.8501555603590526
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1283,
      "error_rate": 0.2112236944660951,
      "mean_confidence": 0.9712408168279428
    }
  ],
  "theta_mae_rad": 0.016247158870100975,
  "theta_mae_deg": 0.93089359998703,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.966602792225568,
  "theta_flat_mae_deg": 1.3316676616668701,
  "theta_flat_abs_p95_deg": 4.088479995727539,
  "theta_flat_abs_max_deg": 12.097867012023926,
  "theta_flat_bias_deg": 0.5088856220245361,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.9011441469192505,
  "theta_near_flat_abs_p95_deg": 6.136359214782715,
  "theta_near_flat_abs_max_deg": 12.097867012023926,
  "theta_near_flat_bias_deg": 0.6676050424575806,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.6616437435150146,
  "theta_flat_turn_abs_p95_deg": 6.892611503601074,
  "theta_flat_turn_abs_max_deg": 12.097867012023926,
  "theta_flat_turn_bias_deg": -0.5065487027168274,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.93089359998703,
  "theta_slope_control_abs_p95_deg": 9.174601554870605,
  "theta_slope_control_abs_max_deg": 13.110344886779785,
  "theta_slope_control_bias_deg": -0.1457768976688385,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9308934807777405,
  "theta_all_rmse_deg": 1.3866875171661377,
  "theta_all_p95_abs_err_deg": 2.592268943786621,
  "theta_all_max_abs_err_deg": 11.597867012023926,
  "theta_all_bias_deg": -0.1457768976688385,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8430068492889404,
  "theta_active_abs_ge_2_rmse_deg": 1.1498908996582031,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2240514755249023,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.332409858703613,
  "theta_active_abs_ge_2_bias_deg": -0.2893393933773041,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9653561115264893,
  "theta_abs_le_8_rmse_deg": 1.4467384815216064,
  "theta_abs_le_8_p95_abs_err_deg": 2.6984755992889404,
  "theta_abs_le_8_max_abs_err_deg": 11.597867012023926,
  "theta_abs_le_8_bias_deg": -0.10876673460006714,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9308934807777405,
  "theta_abs_le_10_rmse_deg": 1.3866875171661377,
  "theta_abs_le_10_p95_abs_err_deg": 2.592268943786621,
  "theta_abs_le_10_max_abs_err_deg": 11.597867012023926,
  "theta_abs_le_10_bias_deg": -0.1457768976688385,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8736909627914429,
  "theta_pos_8_10_rmse_deg": 1.0382829904556274,
  "theta_pos_8_10_p95_abs_err_deg": 1.7283360958099365,
  "theta_pos_8_10_max_abs_err_deg": 4.906783103942871,
  "theta_pos_8_10_bias_deg": -0.6408807039260864,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6958059072494507,
  "theta_neg_10_8_rmse_deg": 1.155158519744873,
  "theta_neg_10_8_p95_abs_err_deg": 1.884850025177002,
  "theta_neg_10_8_max_abs_err_deg": 8.332409858703613,
  "theta_neg_10_8_bias_deg": 0.042928144335746765,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8341122269630432,
  "theta_pos_6_8_rmse_deg": 1.064390778541565,
  "theta_pos_6_8_p95_abs_err_deg": 2.1706602573394775,
  "theta_pos_6_8_max_abs_err_deg": 3.961530923843384,
  "theta_pos_6_8_bias_deg": -0.4402022063732147,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7741960287094116,
  "theta_neg_8_6_rmse_deg": 1.129449725151062,
  "theta_neg_8_6_p95_abs_err_deg": 1.9074747562408447,
  "theta_neg_8_6_max_abs_err_deg": 6.3702192306518555,
  "theta_neg_8_6_bias_deg": -0.14233864843845367,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8538182973861694,
  "theta_neg_4_2_rmse_deg": 1.1922119855880737,
  "theta_neg_4_2_p95_abs_err_deg": 2.4658830165863037,
  "theta_neg_4_2_max_abs_err_deg": 4.45024299621582,
  "theta_neg_4_2_bias_deg": -0.5083779692649841,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5416914820671082,
  "theta_neg_2_0p5_rmse_deg": 0.7657392024993896,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6976327896118164,
  "theta_neg_2_0p5_max_abs_err_deg": 3.5387074947357178,
  "theta_neg_2_0p5_bias_deg": 0.22052942216396332,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.391241192817688,
  "theta_pos_0p5_2_rmse_deg": 1.6935503482818604,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.588480234146118,
  "theta_pos_0p5_2_max_abs_err_deg": 3.5668513774871826,
  "theta_pos_0p5_2_bias_deg": 0.8798184990882874,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3099074760696401,
  "loss_turn": 1.042205647170463,
  "loss_theta": 0.0005855082569855576,
  "loss_main_bundle_base": 0.3099074760696401,
  "loss_turn_bundle_base": 0.2084411356905639,
  "loss_theta_bundle_base": 0.0003812363405594746,
  "loss_main_bundle": 0.3099074760696401,
  "loss_turn_bundle": 0.2084411356905639,
  "loss_theta_bundle": 0.0003812363405594746,
  "loss_theta_flat": 0.00029866260087939235,
  "loss_theta_near_flat": 0.002453873519116511,
  "loss_theta_error_excess": 0.00024159650728850044,
  "loss_theta_flat_excess": 0.0001603479311336856,
  "loss_theta_near_flat_excess": 0.001963318649840734,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011287449795440223,
  "loss_theta_small_neg": 0.00043769615849779974,
  "loss_theta_small_neg_excess": 0.0001270640144913542,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.43366464962010776,
  "loss_false_turn_straight": 0.34035483005082334,
  "loss_transition_focal_raw": 0.7226971455614041,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.145451728187007,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
