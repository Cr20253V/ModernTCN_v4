# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
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
| acc_main | 0.9589 |
| acc_turn | 0.5861 |
| acc_turn_pure | 0.6012 |
| acc_turn_transition | 0.5201 |
| main_confidence_mean | 0.9889 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0117 |
| turn_confidence_mean | 0.8410 |
| turn_low_conf_0p60_ratio | 0.1455 |
| turn_low_conf_0p70_ratio | 0.2443 |
| turn_right_recall | 0.6921 |
| turn_straight_recall | 0.5846 |
| turn_left_recall | 0.4920 |
| theta_mae_deg | 0.6184 |
| theta_abs_le_10_p95_abs_err_deg | 1.7572 |
| theta_neg_10_8_p95_abs_err_deg | 3.2698 |
| theta_pos_8_10_p95_abs_err_deg | 2.9065 |
| theta_abs_le_8_p95_abs_err_deg | 1.4872 |
| theta_neg_8_6_p95_abs_err_deg | 1.6119 |
| theta_pos_6_8_p95_abs_err_deg | 1.5026 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6942 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4779 |
| theta_flat_abs_p95_deg | 2.4594 |
| theta_flat_bias_deg | 0.0551 |
| theta_near_flat_abs_p95_deg | 1.5991 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0272 |
| theta_flat_turn_abs_p95_deg | 1.8737 |
| flat_recall | 0.9418 |
| stall_recall | 0.6979 |
| slope_recall | 0.9727 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7951 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    712,
    0,
    44
  ],
  [
    9,
    67,
    20
  ],
  [
    58,
    17,
    2675
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    553,
    165,
    81
  ],
  [
    459,
    1130,
    344
  ],
  [
    174,
    268,
    428
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.350536 |
| test_loss_turn_bundle_base | 0.332635 |
| test_loss_theta_bundle_base | 0.000158 |
| test_loss_transition_focal_raw | 1.534179 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.646603 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 76
- train_seconds: 353.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.3913 | 0.5542 |
| [0.60,0.70) | 19 | 0.7368 | 0.6493 |
| [0.70,0.80) | 28 | 0.5357 | 0.7506 |
| [0.80,0.90) | 59 | 0.4915 | 0.8579 |
| [0.90,1.00) | 3473 | 0.0233 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 524 | 0.6145 | 0.5240 |
| [0.60,0.70) | 356 | 0.5646 | 0.6506 |
| [0.70,0.80) | 346 | 0.4884 | 0.7482 |
| [0.80,0.90) | 465 | 0.5118 | 0.8518 |
| [0.90,1.00) | 1911 | 0.2936 | 0.9777 |


## 验证集最佳点

```json
{
  "loss_total": 0.6686983606328177,
  "acc_main": 0.9426251691474966,
  "acc_turn": 0.6500676589986468,
  "acc_turn_pure": 0.6633890527695837,
  "acc_turn_transition": 0.5869565217391305,
  "false_turn_straight": 0.3903326403326403,
  "flat_recall": 0.9482496194824962,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9482496194824962,
    0.4523809523809524,
    0.94826435246996
  ],
  "turn_right_recall": 0.7393364928909952,
  "turn_straight_recall": 0.6096673596673596,
  "turn_left_recall": 0.6526429341963322,
  "recall_turn": [
    0.7393364928909952,
    0.6096673596673596,
    0.6526429341963322
  ],
  "cm_turn": [
    [
      624,
      205,
      15
    ],
    [
      467,
      1173,
      284
    ],
    [
      105,
      217,
      605
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      623,
      0,
      34
    ],
    [
      0,
      19,
      23
    ],
    [
      144,
      11,
      2841
    ]
  ],
  "main_confidence_mean": 0.9709123341600319,
  "main_confidence_error_mean": 0.7791735877100943,
  "main_low_conf_0p60_ratio": 0.04952638700947226,
  "main_low_conf_0p70_ratio": 0.05412719891745602,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 183,
      "error_rate": 0.45901639344262296,
      "mean_confidence": 0.5566932656354382
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.47058823529411764,
      "mean_confidence": 0.6473137900256708
    },
    {
      "bin": "[0.70,0.80)",
      "n": 33,
      "error_rate": 0.5454545454545454,
      "mean_confidence": 0.743152575315953
    },
    {
      "bin": "[0.80,0.90)",
      "n": 37,
      "error_rate": 0.1891891891891892,
      "mean_confidence": 0.8568886571515529
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3425,
      "error_rate": 0.027737226277372264,
      "mean_confidence": 0.9980767758772445
    }
  ],
  "turn_confidence_mean": 0.8552070862224195,
  "turn_confidence_error_mean": 0.7895443362580817,
  "turn_low_conf_0p60_ratio": 0.12855209742895804,
  "turn_low_conf_0p70_ratio": 0.2189445196211096,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 475,
      "error_rate": 0.5852631578947368,
      "mean_confidence": 0.5040418574979657
    },
    {
      "bin": "[0.60,0.70)",
      "n": 334,
      "error_rate": 0.4281437125748503,
      "mean_confidence": 0.6498061795301866
    },
    {
      "bin": "[0.70,0.80)",
      "n": 309,
      "error_rate": 0.47896440129449835,
      "mean_confidence": 0.7525382536033367
    },
    {
      "bin": "[0.80,0.90)",
      "n": 456,
      "error_rate": 0.4649122807017544,
      "mean_confidence": 0.8583026133772611
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2121,
      "error_rate": 0.2413955681282414,
      "mean_confidence": 0.9804878478329853
    }
  ],
  "theta_mae_rad": 0.014584526419639587,
  "theta_mae_deg": 0.835631787776947,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.7953281423804227,
  "slope_sign_acc": 0.9657815494114427,
  "theta_flat_mae_deg": 1.0837149620056152,
  "theta_flat_abs_p95_deg": 4.0818328857421875,
  "theta_flat_abs_max_deg": 8.037656784057617,
  "theta_flat_bias_deg": 0.6576204299926758,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5184483528137207,
  "theta_near_flat_abs_p95_deg": 4.625378608703613,
  "theta_near_flat_abs_max_deg": 8.037656784057617,
  "theta_near_flat_bias_deg": 1.283164143562317,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1810129880905151,
  "theta_flat_turn_abs_p95_deg": 4.664734363555908,
  "theta_flat_turn_abs_max_deg": 8.037656784057617,
  "theta_flat_turn_bias_deg": 0.911793053150177,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.835631787776947,
  "theta_slope_control_abs_p95_deg": 9.128993034362793,
  "theta_slope_control_abs_max_deg": 12.893843650817871,
  "theta_slope_control_bias_deg": 0.19161692261695862,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8356317281723022,
  "theta_all_rmse_deg": 1.2352651357650757,
  "theta_all_p95_abs_err_deg": 2.6606616973876953,
  "theta_all_max_abs_err_deg": 8.537656784057617,
  "theta_all_bias_deg": 0.1916169375181198,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7812289595603943,
  "theta_active_abs_ge_2_rmse_deg": 1.0977132320404053,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.36555552482605,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.039720058441162,
  "theta_active_abs_ge_2_bias_deg": 0.08942588418722153,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.851414680480957,
  "theta_abs_le_8_rmse_deg": 1.2685056924819946,
  "theta_abs_le_8_p95_abs_err_deg": 2.838844060897827,
  "theta_abs_le_8_max_abs_err_deg": 8.537656784057617,
  "theta_abs_le_8_bias_deg": 0.22640582919120789,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8356317281723022,
  "theta_abs_le_10_rmse_deg": 1.2352651357650757,
  "theta_abs_le_10_p95_abs_err_deg": 2.6606616973876953,
  "theta_abs_le_10_max_abs_err_deg": 8.537656784057617,
  "theta_abs_le_10_bias_deg": 0.1916169375181198,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7305700778961182,
  "theta_pos_8_10_rmse_deg": 0.914100170135498,
  "theta_pos_8_10_p95_abs_err_deg": 1.6321536302566528,
  "theta_pos_8_10_max_abs_err_deg": 5.184846878051758,
  "theta_pos_8_10_bias_deg": -0.44042882323265076,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8081966042518616,
  "theta_neg_10_8_rmse_deg": 1.2328219413757324,
  "theta_neg_10_8_p95_abs_err_deg": 2.2355966567993164,
  "theta_neg_10_8_max_abs_err_deg": 6.713477611541748,
  "theta_neg_10_8_bias_deg": 0.5385348200798035,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6734231114387512,
  "theta_pos_6_8_rmse_deg": 0.8980898857116699,
  "theta_pos_6_8_p95_abs_err_deg": 1.7553256750106812,
  "theta_pos_6_8_max_abs_err_deg": 3.8726606369018555,
  "theta_pos_6_8_bias_deg": -0.2738112807273865,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9341947436332703,
  "theta_neg_8_6_rmse_deg": 1.2941741943359375,
  "theta_neg_8_6_p95_abs_err_deg": 2.3844566345214844,
  "theta_neg_8_6_max_abs_err_deg": 7.039720058441162,
  "theta_neg_8_6_bias_deg": 0.2228516787290573,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7123518586158752,
  "theta_neg_4_2_rmse_deg": 1.0251494646072388,
  "theta_neg_4_2_p95_abs_err_deg": 2.0394694805145264,
  "theta_neg_4_2_max_abs_err_deg": 5.143712520599365,
  "theta_neg_4_2_bias_deg": -0.11838902533054352,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5041710138320923,
  "theta_neg_2_0p5_rmse_deg": 0.7592220902442932,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2176916599273682,
  "theta_neg_2_0p5_max_abs_err_deg": 4.415122985839844,
  "theta_neg_2_0p5_bias_deg": -0.0950574204325676,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2064731121063232,
  "theta_pos_0p5_2_rmse_deg": 1.5387953519821167,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5818326473236084,
  "theta_pos_0p5_2_max_abs_err_deg": 4.532716751098633,
  "theta_pos_0p5_2_bias_deg": 0.62801593542099,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.39050863936079694,
  "loss_turn": 1.3894516046379513,
  "loss_theta": 0.00046479957408545203,
  "loss_main_bundle_base": 0.39050863936079694,
  "loss_turn_bundle_base": 0.2778903256491815,
  "loss_theta_bundle_base": 0.0002993956623638001,
  "loss_main_bundle": 0.39050863936079694,
  "loss_turn_bundle": 0.2778903256491815,
  "loss_theta_bundle": 0.0002993956623638001,
  "loss_theta_flat": 0.00020574428995643365,
  "loss_theta_near_flat": 0.0014755192804761503,
  "loss_theta_error_excess": 0.0001695188632540856,
  "loss_theta_flat_excess": 0.0001226545145500089,
  "loss_theta_near_flat_excess": 0.0010982651590036936,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010590624108788316,
  "loss_theta_small_neg": 0.0003186897345703897,
  "loss_theta_small_neg_excess": 8.954717533890389e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3713893289978998,
  "loss_false_turn_straight": 0.2931220037527433,
  "loss_transition_focal_raw": 1.1726107311990812,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.754106687305745,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
