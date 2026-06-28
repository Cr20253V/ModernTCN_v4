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
| acc_main | 0.9564 |
| acc_turn | 0.5777 |
| acc_turn_pure | 0.5930 |
| acc_turn_transition | 0.5112 |
| main_confidence_mean | 0.9869 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0167 |
| turn_confidence_mean | 0.8281 |
| turn_low_conf_0p60_ratio | 0.1577 |
| turn_low_conf_0p70_ratio | 0.2662 |
| turn_right_recall | 0.5895 |
| turn_straight_recall | 0.5592 |
| turn_left_recall | 0.6080 |
| theta_mae_deg | 0.8155 |
| theta_abs_le_10_p95_abs_err_deg | 2.0825 |
| theta_neg_10_8_p95_abs_err_deg | 1.3217 |
| theta_pos_8_10_p95_abs_err_deg | 3.5251 |
| theta_abs_le_8_p95_abs_err_deg | 2.0112 |
| theta_neg_8_6_p95_abs_err_deg | 1.4722 |
| theta_pos_6_8_p95_abs_err_deg | 1.8510 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.1378 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0711 |
| theta_flat_abs_p95_deg | 2.9065 |
| theta_flat_bias_deg | -0.6659 |
| theta_near_flat_abs_p95_deg | 1.8037 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4925 |
| theta_flat_turn_abs_p95_deg | 1.8789 |
| flat_recall | 0.9365 |
| stall_recall | 0.6354 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1354 |
| uphill_recall | 0.7460 |
| downhill_recall | 0.8076 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    708,
    0,
    48
  ],
  [
    13,
    61,
    22
  ],
  [
    69,
    5,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    471,
    194,
    134
  ],
  [
    334,
    1081,
    518
  ],
  [
    160,
    181,
    529
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.396247 |
| test_loss_turn_bundle_base | 0.340589 |
| test_loss_theta_bundle_base | 0.000249 |
| test_loss_transition_focal_raw | 1.403529 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.276982 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 75
- train_seconds: 334.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.5312 | 0.5436 |
| [0.60,0.70) | 28 | 0.1786 | 0.6544 |
| [0.70,0.80) | 32 | 0.4375 | 0.7519 |
| [0.80,0.90) | 38 | 0.4737 | 0.8544 |
| [0.90,1.00) | 3472 | 0.0297 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 568 | 0.5933 | 0.5300 |
| [0.60,0.70) | 391 | 0.5217 | 0.6487 |
| [0.70,0.80) | 386 | 0.5311 | 0.7526 |
| [0.80,0.90) | 517 | 0.4758 | 0.8511 |
| [0.90,1.00) | 1740 | 0.3040 | 0.9757 |


## 验证集最佳点

```json
{
  "loss_total": 0.5894418551731497,
  "acc_main": 0.9431664411366711,
  "acc_turn": 0.6438430311231393,
  "acc_turn_pure": 0.6545394952474598,
  "acc_turn_transition": 0.593167701863354,
  "false_turn_straight": 0.4194386694386694,
  "flat_recall": 0.9421613394216134,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9512683578104139,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.9421613394216134,
    0.38095238095238093,
    0.9512683578104139
  ],
  "turn_right_recall": 0.6919431279620853,
  "turn_straight_recall": 0.5805613305613305,
  "turn_left_recall": 0.7313915857605178,
  "recall_turn": [
    0.6919431279620853,
    0.5805613305613305,
    0.7313915857605178
  ],
  "cm_turn": [
    [
      584,
      214,
      46
    ],
    [
      389,
      1117,
      418
    ],
    [
      104,
      145,
      678
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      619,
      0,
      38
    ],
    [
      3,
      16,
      23
    ],
    [
      144,
      2,
      2850
    ]
  ],
  "main_confidence_mean": 0.9733362431525694,
  "main_confidence_error_mean": 0.7871217259751431,
  "main_low_conf_0p60_ratio": 0.005142083897158322,
  "main_low_conf_0p70_ratio": 0.055209742895805144,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.5421153350528091
    },
    {
      "bin": "[0.60,0.70)",
      "n": 185,
      "error_rate": 0.4648648648648649,
      "mean_confidence": 0.605312568516815
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.6296296296296297,
      "mean_confidence": 0.75673460404224
    },
    {
      "bin": "[0.80,0.90)",
      "n": 28,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.8582635867205035
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3436,
      "error_rate": 0.02619324796274738,
      "mean_confidence": 0.9981755492345212
    }
  ],
  "turn_confidence_mean": 0.8494462625362014,
  "turn_confidence_error_mean": 0.7808555683975733,
  "turn_low_conf_0p60_ratio": 0.14614343707713126,
  "turn_low_conf_0p70_ratio": 0.2313937753721245,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 540,
      "error_rate": 0.6,
      "mean_confidence": 0.5236798248958714
    },
    {
      "bin": "[0.60,0.70)",
      "n": 315,
      "error_rate": 0.5111111111111111,
      "mean_confidence": 0.6492032125486698
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.45454545454545453,
      "mean_confidence": 0.7520712871419645
    },
    {
      "bin": "[0.80,0.90)",
      "n": 417,
      "error_rate": 0.4172661870503597,
      "mean_confidence": 0.8511624911421223
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2093,
      "error_rate": 0.2422360248447205,
      "mean_confidence": 0.9786428758296938
    }
  ],
  "theta_mae_rad": 0.01699059084057808,
  "theta_mae_deg": 0.9734891057014465,
  "uphill_recall": 0.7757412398921832,
  "downhill_recall": 0.8058954393770856,
  "slope_sign_acc": 0.9726252395291541,
  "theta_flat_mae_deg": 1.2496051788330078,
  "theta_flat_abs_p95_deg": 3.7952542304992676,
  "theta_flat_abs_max_deg": 8.245017051696777,
  "theta_flat_bias_deg": 0.03768131136894226,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5830998420715332,
  "theta_near_flat_abs_p95_deg": 3.795585870742798,
  "theta_near_flat_abs_max_deg": 8.245017051696777,
  "theta_near_flat_bias_deg": 0.5627074241638184,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.37693452835083,
  "theta_flat_turn_abs_p95_deg": 4.671400547027588,
  "theta_flat_turn_abs_max_deg": 8.245017051696777,
  "theta_flat_turn_bias_deg": 0.27435997128486633,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9734891057014465,
  "theta_slope_control_abs_p95_deg": 9.374629020690918,
  "theta_slope_control_abs_max_deg": 12.730857849121094,
  "theta_slope_control_bias_deg": -0.5180320143699646,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9734891057014465,
  "theta_all_rmse_deg": 1.3057780265808105,
  "theta_all_p95_abs_err_deg": 2.504648447036743,
  "theta_all_max_abs_err_deg": 8.745017051696777,
  "theta_all_bias_deg": -0.5180320739746094,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9129389524459839,
  "theta_active_abs_ge_2_rmse_deg": 1.1802978515625,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1736552715301514,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.085438251495361,
  "theta_active_abs_ge_2_bias_deg": -0.6398957371711731,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0045430660247803,
  "theta_abs_le_8_rmse_deg": 1.3381115198135376,
  "theta_abs_le_8_p95_abs_err_deg": 2.6122677326202393,
  "theta_abs_le_8_max_abs_err_deg": 8.745017051696777,
  "theta_abs_le_8_bias_deg": -0.5053439736366272,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9734891057014465,
  "theta_abs_le_10_rmse_deg": 1.3057780265808105,
  "theta_abs_le_10_p95_abs_err_deg": 2.504648447036743,
  "theta_abs_le_10_max_abs_err_deg": 8.745017051696777,
  "theta_abs_le_10_bias_deg": -0.5180320739746094,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8607063889503479,
  "theta_pos_8_10_rmse_deg": 1.1148467063903809,
  "theta_pos_8_10_p95_abs_err_deg": 1.794883370399475,
  "theta_pos_8_10_max_abs_err_deg": 6.698632717132568,
  "theta_pos_8_10_bias_deg": -0.7186546325683594,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8239505887031555,
  "theta_neg_10_8_rmse_deg": 1.2032148838043213,
  "theta_neg_10_8_p95_abs_err_deg": 2.180850028991699,
  "theta_neg_10_8_max_abs_err_deg": 7.085438251495361,
  "theta_neg_10_8_bias_deg": -0.42191705107688904,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.9696041345596313,
  "theta_pos_6_8_rmse_deg": 1.1371688842773438,
  "theta_pos_6_8_p95_abs_err_deg": 2.083225727081299,
  "theta_pos_6_8_max_abs_err_deg": 3.1807126998901367,
  "theta_pos_6_8_bias_deg": -0.750778317451477,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9507468938827515,
  "theta_neg_8_6_rmse_deg": 1.2569223642349243,
  "theta_neg_8_6_p95_abs_err_deg": 2.3972079753875732,
  "theta_neg_8_6_max_abs_err_deg": 5.184367656707764,
  "theta_neg_8_6_bias_deg": -0.7641346454620361,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 1.0484633445739746,
  "theta_neg_4_2_rmse_deg": 1.322486162185669,
  "theta_neg_4_2_p95_abs_err_deg": 2.5856034755706787,
  "theta_neg_4_2_max_abs_err_deg": 4.775236129760742,
  "theta_neg_4_2_bias_deg": -0.9274476170539856,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8634535074234009,
  "theta_neg_2_0p5_rmse_deg": 1.0261083841323853,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.033749580383301,
  "theta_neg_2_0p5_max_abs_err_deg": 3.23004412651062,
  "theta_neg_2_0p5_bias_deg": -0.8002561926841736,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2124793529510498,
  "theta_pos_0p5_2_rmse_deg": 1.5271614789962769,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.7252204418182373,
  "theta_pos_0p5_2_max_abs_err_deg": 3.753596067428589,
  "theta_pos_0p5_2_bias_deg": 0.21745873987674713,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.31320154416061063,
  "loss_turn": 1.3793437332842444,
  "loss_theta": 0.0005192926591161401,
  "loss_main_bundle_base": 0.31320154416061063,
  "loss_turn_bundle_base": 0.27586875314722203,
  "loss_theta_bundle_base": 0.000371564398122717,
  "loss_main_bundle": 0.31320154416061063,
  "loss_turn_bundle": 0.27586875314722203,
  "loss_theta_bundle": 0.000371564398122717,
  "loss_theta_flat": 0.0005503621957178514,
  "loss_theta_near_flat": 0.001566894833976466,
  "loss_theta_error_excess": 0.00017130378819545238,
  "loss_theta_flat_excess": 0.0002733404818439922,
  "loss_theta_near_flat_excess": 0.0011282876333195328,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001134477265422385,
  "loss_theta_small_neg": 0.0005294291655115874,
  "loss_theta_small_neg_excess": 0.00015031127660838995,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36163694865003493,
  "loss_false_turn_straight": 0.3168318702338997,
  "loss_transition_focal_raw": 1.1254306303793427,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.492761009536351,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
