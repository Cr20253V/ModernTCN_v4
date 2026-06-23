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
  "lambda_turn": 0.24,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
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
| acc_main | 0.9675 |
| acc_turn | 0.5744 |
| acc_turn_pure | 0.5906 |
| acc_turn_transition | 0.5037 |
| main_confidence_mean | 0.9896 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8489 |
| turn_low_conf_0p60_ratio | 0.1316 |
| turn_low_conf_0p70_ratio | 0.2254 |
| turn_right_recall | 0.6283 |
| turn_straight_recall | 0.5541 |
| turn_left_recall | 0.5701 |
| theta_mae_deg | 0.6171 |
| theta_abs_le_10_p95_abs_err_deg | 1.6832 |
| theta_neg_10_8_p95_abs_err_deg | 1.4848 |
| theta_pos_8_10_p95_abs_err_deg | 2.5883 |
| theta_abs_le_8_p95_abs_err_deg | 1.6502 |
| theta_neg_8_6_p95_abs_err_deg | 1.6931 |
| theta_pos_6_8_p95_abs_err_deg | 1.7333 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3864 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6538 |
| theta_flat_abs_p95_deg | 2.8854 |
| theta_flat_bias_deg | 0.3451 |
| theta_near_flat_abs_p95_deg | 1.6177 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.4094 |
| theta_flat_turn_abs_p95_deg | 1.3726 |
| flat_recall | 0.9537 |
| stall_recall | 0.6875 |
| slope_recall | 0.9811 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7597 |
| downhill_recall | 0.7991 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    0,
    35
  ],
  [
    10,
    66,
    20
  ],
  [
    44,
    8,
    2698
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    502,
    195,
    102
  ],
  [
    449,
    1071,
    413
  ],
  [
    179,
    195,
    496
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.358514 |
| test_loss_turn_bundle_base | 0.430313 |
| test_loss_theta_bundle_base | 0.000149 |
| test_loss_transition_focal_raw | 1.667470 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.197516 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 82
- train_seconds: 378.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.3846 | 0.5495 |
| [0.60,0.70) | 23 | 0.3478 | 0.6576 |
| [0.70,0.80) | 32 | 0.3125 | 0.7516 |
| [0.80,0.90) | 38 | 0.3421 | 0.8701 |
| [0.90,1.00) | 3483 | 0.0218 | 0.9985 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 474 | 0.6414 | 0.5332 |
| [0.60,0.70) | 338 | 0.5947 | 0.6495 |
| [0.70,0.80) | 363 | 0.5096 | 0.7519 |
| [0.80,0.90) | 489 | 0.5031 | 0.8548 |
| [0.90,1.00) | 1938 | 0.3080 | 0.9776 |


## 验证集最佳点

```json
{
  "loss_total": 0.745089109163323,
  "acc_main": 0.9456021650879567,
  "acc_turn": 0.6489851150202977,
  "acc_turn_pure": 0.6594559160930842,
  "acc_turn_transition": 0.5993788819875776,
  "false_turn_straight": 0.4095634095634096,
  "flat_recall": 0.969558599695586,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.969558599695586,
    0.38095238095238093,
    0.94826435246996
  ],
  "turn_right_recall": 0.7097156398104265,
  "turn_straight_recall": 0.5904365904365905,
  "turn_left_recall": 0.7152103559870551,
  "recall_turn": [
    0.7097156398104265,
    0.5904365904365905,
    0.7152103559870551
  ],
  "cm_turn": [
    [
      599,
      217,
      28
    ],
    [
      437,
      1136,
      351
    ],
    [
      119,
      145,
      663
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
      0,
      16,
      26
    ],
    [
      144,
      11,
      2841
    ]
  ],
  "main_confidence_mean": 0.9728569749665377,
  "main_confidence_error_mean": 0.7842894963112313,
  "main_low_conf_0p60_ratio": 0.04952638700947226,
  "main_low_conf_0p70_ratio": 0.05466847090663058,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 183,
      "error_rate": 0.45901639344262296,
      "mean_confidence": 0.5717783470487188
    },
    {
      "bin": "[0.60,0.70)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.6515715162974973
    },
    {
      "bin": "[0.70,0.80)",
      "n": 26,
      "error_rate": 0.4230769230769231,
      "mean_confidence": 0.7561690504008602
    },
    {
      "bin": "[0.80,0.90)",
      "n": 20,
      "error_rate": 0.2,
      "mean_confidence": 0.8581476063066239
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3447,
      "error_rate": 0.026979982593559618,
      "mean_confidence": 0.9982210266159656
    }
  ],
  "turn_confidence_mean": 0.8704140813079649,
  "turn_confidence_error_mean": 0.804492170180324,
  "turn_low_conf_0p60_ratio": 0.12070365358592693,
  "turn_low_conf_0p70_ratio": 0.1918809201623816,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 446,
      "error_rate": 0.5919282511210763,
      "mean_confidence": 0.5255334451381939
    },
    {
      "bin": "[0.60,0.70)",
      "n": 263,
      "error_rate": 0.532319391634981,
      "mean_confidence": 0.6510001654922332
    },
    {
      "bin": "[0.70,0.80)",
      "n": 296,
      "error_rate": 0.4831081081081081,
      "mean_confidence": 0.7520117515980455
    },
    {
      "bin": "[0.80,0.90)",
      "n": 419,
      "error_rate": 0.4295942720763723,
      "mean_confidence": 0.8537004102080585
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2271,
      "error_rate": 0.2509907529722589,
      "mean_confidence": 0.9820709467312377
    }
  ],
  "theta_mae_rad": 0.013392424210906029,
  "theta_mae_deg": 0.7673293352127075,
  "uphill_recall": 0.7719676549865229,
  "downhill_recall": 0.7947719688542826,
  "slope_sign_acc": 0.9712565015056118,
  "theta_flat_mae_deg": 1.0279452800750732,
  "theta_flat_abs_p95_deg": 3.339144229888916,
  "theta_flat_abs_max_deg": 6.731099605560303,
  "theta_flat_bias_deg": 0.5893428921699524,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.324859857559204,
  "theta_near_flat_abs_p95_deg": 3.3933441638946533,
  "theta_near_flat_abs_max_deg": 6.731099605560303,
  "theta_near_flat_bias_deg": 0.9807776808738708,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1647281646728516,
  "theta_flat_turn_abs_p95_deg": 3.1587934494018555,
  "theta_flat_turn_abs_max_deg": 6.731099605560303,
  "theta_flat_turn_bias_deg": 0.6783091425895691,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7673293352127075,
  "theta_slope_control_abs_p95_deg": 9.43319034576416,
  "theta_slope_control_abs_max_deg": 12.982259750366211,
  "theta_slope_control_bias_deg": 0.10862616449594498,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7673293948173523,
  "theta_all_rmse_deg": 1.1515048742294312,
  "theta_all_p95_abs_err_deg": 2.517531633377075,
  "theta_all_max_abs_err_deg": 7.101241588592529,
  "theta_all_bias_deg": 0.10862617194652557,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7101781964302063,
  "theta_active_abs_ge_2_rmse_deg": 1.0895516872406006,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1649227142333984,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.101241588592529,
  "theta_active_abs_ge_2_bias_deg": 0.0032086530700325966,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7940890192985535,
  "theta_abs_le_8_rmse_deg": 1.1761200428009033,
  "theta_abs_le_8_p95_abs_err_deg": 2.517531633377075,
  "theta_abs_le_8_max_abs_err_deg": 7.101241588592529,
  "theta_abs_le_8_bias_deg": 0.14650119841098785,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7673293948173523,
  "theta_abs_le_10_rmse_deg": 1.1515048742294312,
  "theta_abs_le_10_p95_abs_err_deg": 2.517531633377075,
  "theta_abs_le_10_max_abs_err_deg": 7.101241588592529,
  "theta_abs_le_10_bias_deg": 0.10862617194652557,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5808391571044922,
  "theta_pos_8_10_rmse_deg": 0.7899472117424011,
  "theta_pos_8_10_p95_abs_err_deg": 1.448244571685791,
  "theta_pos_8_10_max_abs_err_deg": 4.734377861022949,
  "theta_pos_8_10_bias_deg": -0.15385788679122925,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7293167114257812,
  "theta_neg_10_8_rmse_deg": 1.2459794282913208,
  "theta_neg_10_8_p95_abs_err_deg": 2.831916332244873,
  "theta_neg_10_8_max_abs_err_deg": 7.06428861618042,
  "theta_neg_10_8_bias_deg": 0.05332906171679497,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5518555045127869,
  "theta_pos_6_8_rmse_deg": 0.8056755065917969,
  "theta_pos_6_8_p95_abs_err_deg": 1.8640000820159912,
  "theta_pos_6_8_max_abs_err_deg": 3.380838394165039,
  "theta_pos_6_8_bias_deg": -0.09320873767137527,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8481752872467041,
  "theta_neg_8_6_rmse_deg": 1.2402751445770264,
  "theta_neg_8_6_p95_abs_err_deg": 2.5183141231536865,
  "theta_neg_8_6_max_abs_err_deg": 6.571755409240723,
  "theta_neg_8_6_bias_deg": -0.043261073529720306,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7294977307319641,
  "theta_neg_4_2_rmse_deg": 1.0290976762771606,
  "theta_neg_4_2_p95_abs_err_deg": 2.217125177383423,
  "theta_neg_4_2_max_abs_err_deg": 4.161088466644287,
  "theta_neg_4_2_bias_deg": 0.0035110318567603827,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7002952098846436,
  "theta_neg_2_0p5_rmse_deg": 0.9680792689323425,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.743172526359558,
  "theta_neg_2_0p5_max_abs_err_deg": 4.647187232971191,
  "theta_neg_2_0p5_bias_deg": -0.031160904094576836,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.114962100982666,
  "theta_pos_0p5_2_rmse_deg": 1.3690351247787476,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.357032060623169,
  "theta_pos_0p5_2_max_abs_err_deg": 3.555288791656494,
  "theta_pos_0p5_2_bias_deg": 0.850135087966919,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3775217879125004,
  "loss_turn": 1.5304351647587364,
  "loss_theta": 0.00040390185160494343,
  "loss_main_bundle_base": 0.3775217879125004,
  "loss_turn_bundle_base": 0.3673044311258241,
  "loss_theta_bundle_base": 0.0002628933297752507,
  "loss_main_bundle": 0.3775217879125004,
  "loss_turn_bundle": 0.3673044311258241,
  "loss_theta_bundle": 0.0002628933297752507,
  "loss_theta_flat": 0.0001703549947125156,
  "loss_theta_near_flat": 0.000959622567955591,
  "loss_theta_error_excess": 0.00014328196808142545,
  "loss_theta_flat_excess": 7.16983600418256e-05,
  "loss_theta_near_flat_excess": 0.0006254175692073325,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001314061575108277,
  "loss_theta_small_neg": 0.0003197316161854034,
  "loss_theta_small_neg_excess": 8.232251335980172e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3639400672283482,
  "loss_false_turn_straight": 0.3079749990703288,
  "loss_transition_focal_raw": 1.3835322440073843,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.399671553235201,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
