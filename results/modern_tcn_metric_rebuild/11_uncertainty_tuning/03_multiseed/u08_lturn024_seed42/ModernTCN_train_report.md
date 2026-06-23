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
| acc_main | 0.9589 |
| acc_turn | 0.5777 |
| acc_turn_pure | 0.5933 |
| acc_turn_transition | 0.5097 |
| main_confidence_mean | 0.9831 |
| main_low_conf_0p60_ratio | 0.0130 |
| main_low_conf_0p70_ratio | 0.0214 |
| turn_confidence_mean | 0.7849 |
| turn_low_conf_0p60_ratio | 0.2199 |
| turn_low_conf_0p70_ratio | 0.3479 |
| turn_right_recall | 0.5645 |
| turn_straight_recall | 0.6022 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.8821 |
| theta_abs_le_10_p95_abs_err_deg | 2.2548 |
| theta_neg_10_8_p95_abs_err_deg | 2.2360 |
| theta_pos_8_10_p95_abs_err_deg | 3.1378 |
| theta_abs_le_8_p95_abs_err_deg | 2.2281 |
| theta_neg_8_6_p95_abs_err_deg | 2.2106 |
| theta_pos_6_8_p95_abs_err_deg | 1.9628 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0561 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9722 |
| theta_flat_abs_p95_deg | 2.8108 |
| theta_flat_bias_deg | -0.4199 |
| theta_near_flat_abs_p95_deg | 2.1447 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5347 |
| theta_flat_turn_abs_p95_deg | 2.1087 |
| flat_recall | 0.9471 |
| stall_recall | 0.6771 |
| slope_recall | 0.9720 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7443 |
| downhill_recall | 0.8031 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    716,
    0,
    40
  ],
  [
    8,
    65,
    23
  ],
  [
    61,
    16,
    2673
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    451,
    231,
    117
  ],
  [
    389,
    1164,
    380
  ],
  [
    178,
    226,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.357533 |
| test_loss_turn_bundle_base | 0.358785 |
| test_loss_theta_bundle_base | 0.000270 |
| test_loss_transition_focal_raw | 1.326726 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.645724 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 53
- train_seconds: 280.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 47 | 0.5957 | 0.5310 |
| [0.60,0.70) | 30 | 0.3000 | 0.6467 |
| [0.70,0.80) | 35 | 0.3143 | 0.7578 |
| [0.80,0.90) | 56 | 0.2321 | 0.8514 |
| [0.90,1.00) | 3434 | 0.0253 | 0.9967 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 792 | 0.5745 | 0.5131 |
| [0.60,0.70) | 461 | 0.4967 | 0.6504 |
| [0.70,0.80) | 443 | 0.5327 | 0.7487 |
| [0.80,0.90) | 499 | 0.4088 | 0.8517 |
| [0.90,1.00) | 1407 | 0.2822 | 0.9696 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5097
- theta_mae_deg <= 0.7000 未满足，实际 0.8821

## 验证集最佳点

```json
{
  "loss_total": 0.5435259791285163,
  "acc_main": 0.9434370771312585,
  "acc_turn": 0.6438430311231393,
  "acc_turn_pure": 0.6594559160930842,
  "acc_turn_transition": 0.5698757763975155,
  "false_turn_straight": 0.3898128898128898,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9469292389853138,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9573820395738204,
    0.47619047619047616,
    0.9469292389853138
  ],
  "turn_right_recall": 0.6374407582938388,
  "turn_straight_recall": 0.6101871101871101,
  "turn_left_recall": 0.7195253505933118,
  "recall_turn": [
    0.6374407582938388,
    0.6101871101871101,
    0.7195253505933118
  ],
  "cm_turn": [
    [
      538,
      220,
      86
    ],
    [
      313,
      1174,
      437
    ],
    [
      67,
      193,
      667
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      629,
      0,
      28
    ],
    [
      0,
      20,
      22
    ],
    [
      140,
      19,
      2837
    ]
  ],
  "main_confidence_mean": 0.9632513014560208,
  "main_confidence_error_mean": 0.7371381852678377,
  "main_low_conf_0p60_ratio": 0.05602165087956698,
  "main_low_conf_0p70_ratio": 0.06630581867388363,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 207,
      "error_rate": 0.45893719806763283,
      "mean_confidence": 0.5424687801026356
    },
    {
      "bin": "[0.60,0.70)",
      "n": 38,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.6492682228830917
    },
    {
      "bin": "[0.70,0.80)",
      "n": 43,
      "error_rate": 0.23255813953488372,
      "mean_confidence": 0.7598399843428023
    },
    {
      "bin": "[0.80,0.90)",
      "n": 54,
      "error_rate": 0.18518518518518517,
      "mean_confidence": 0.855082760638529
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3353,
      "error_rate": 0.022666269012824338,
      "mean_confidence": 0.9971377096713311
    }
  ],
  "turn_confidence_mean": 0.8074112849705833,
  "turn_confidence_error_mean": 0.7319191692178529,
  "turn_low_conf_0p60_ratio": 0.17889039242219215,
  "turn_low_conf_0p70_ratio": 0.2968876860622463,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 661,
      "error_rate": 0.5779122541603631,
      "mean_confidence": 0.5047905214612439
    },
    {
      "bin": "[0.60,0.70)",
      "n": 436,
      "error_rate": 0.481651376146789,
      "mean_confidence": 0.6504066691506568
    },
    {
      "bin": "[0.70,0.80)",
      "n": 460,
      "error_rate": 0.42391304347826086,
      "mean_confidence": 0.7501938470210298
    },
    {
      "bin": "[0.80,0.90)",
      "n": 483,
      "error_rate": 0.31262939958592134,
      "mean_confidence": 0.8511613638800933
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1655,
      "error_rate": 0.2283987915407855,
      "mean_confidence": 0.9727738653456061
    }
  ],
  "theta_mae_rad": 0.016565265133976936,
  "theta_mae_deg": 0.9491197466850281,
  "uphill_recall": 0.7649595687331536,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9682452778538188,
  "theta_flat_mae_deg": 1.0105745792388916,
  "theta_flat_abs_p95_deg": 3.3071956634521484,
  "theta_flat_abs_max_deg": 9.244478225708008,
  "theta_flat_bias_deg": 0.2663128972053528,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3905465602874756,
  "theta_near_flat_abs_p95_deg": 3.307237148284912,
  "theta_near_flat_abs_max_deg": 9.244478225708008,
  "theta_near_flat_bias_deg": 0.6082568168640137,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2130496501922607,
  "theta_flat_turn_abs_p95_deg": 3.3071956634521484,
  "theta_flat_turn_abs_max_deg": 9.244478225708008,
  "theta_flat_turn_bias_deg": 0.2692953050136566,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9491197466850281,
  "theta_slope_control_abs_p95_deg": 9.618226051330566,
  "theta_slope_control_abs_max_deg": 12.866558074951172,
  "theta_slope_control_bias_deg": -0.4473090171813965,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9491196870803833,
  "theta_all_rmse_deg": 1.3223817348480225,
  "theta_all_p95_abs_err_deg": 2.807190179824829,
  "theta_all_max_abs_err_deg": 9.744478225708008,
  "theta_all_bias_deg": -0.44730904698371887,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9356431365013123,
  "theta_active_abs_ge_2_rmse_deg": 1.2678760290145874,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.519284725189209,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.210205078125,
  "theta_active_abs_ge_2_bias_deg": -0.6038008332252502,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9847152829170227,
  "theta_abs_le_8_rmse_deg": 1.3613574504852295,
  "theta_abs_le_8_p95_abs_err_deg": 2.8071959018707275,
  "theta_abs_le_8_max_abs_err_deg": 9.744478225708008,
  "theta_abs_le_8_bias_deg": -0.4495207667350769,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9491196870803833,
  "theta_abs_le_10_rmse_deg": 1.3223817348480225,
  "theta_abs_le_10_p95_abs_err_deg": 2.807190179824829,
  "theta_abs_le_10_max_abs_err_deg": 9.744478225708008,
  "theta_abs_le_10_bias_deg": -0.44730904698371887,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6597263813018799,
  "theta_pos_8_10_rmse_deg": 0.8760637044906616,
  "theta_pos_8_10_p95_abs_err_deg": 1.4904407262802124,
  "theta_pos_8_10_max_abs_err_deg": 5.399595737457275,
  "theta_pos_8_10_bias_deg": -0.46723467111587524,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.9405959248542786,
  "theta_neg_10_8_rmse_deg": 1.3626099824905396,
  "theta_neg_10_8_p95_abs_err_deg": 2.6054065227508545,
  "theta_neg_10_8_max_abs_err_deg": 6.210205078125,
  "theta_neg_10_8_bias_deg": -0.4082167446613312,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6951344013214111,
  "theta_pos_6_8_rmse_deg": 0.9165743589401245,
  "theta_pos_6_8_p95_abs_err_deg": 1.9262555837631226,
  "theta_pos_6_8_max_abs_err_deg": 3.7247118949890137,
  "theta_pos_6_8_bias_deg": -0.3870641887187958,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.103692889213562,
  "theta_neg_8_6_rmse_deg": 1.4224063158035278,
  "theta_neg_8_6_p95_abs_err_deg": 2.497959613800049,
  "theta_neg_8_6_max_abs_err_deg": 6.1861371994018555,
  "theta_neg_8_6_bias_deg": -0.9037586450576782,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.91880863904953,
  "theta_neg_4_2_rmse_deg": 1.2605681419372559,
  "theta_neg_4_2_p95_abs_err_deg": 2.367154836654663,
  "theta_neg_4_2_max_abs_err_deg": 5.556211948394775,
  "theta_neg_4_2_bias_deg": -0.7174385786056519,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6177000999450684,
  "theta_neg_2_0p5_rmse_deg": 0.79933100938797,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4815866947174072,
  "theta_neg_2_0p5_max_abs_err_deg": 4.150993824005127,
  "theta_neg_2_0p5_bias_deg": -0.08387093245983124,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9133918881416321,
  "theta_pos_0p5_2_rmse_deg": 1.1814216375350952,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.035592555999756,
  "theta_pos_0p5_2_max_abs_err_deg": 3.4690277576446533,
  "theta_pos_0p5_2_bias_deg": 0.25134995579719543,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2561944950094726,
  "loss_turn": 1.1957459266195438,
  "loss_theta": 0.0005325807352060092,
  "loss_main_bundle_base": 0.2561944950094726,
  "loss_turn_bundle_base": 0.2869790148589866,
  "loss_theta_bundle_base": 0.0003524649479484415,
  "loss_main_bundle": 0.2561944950094726,
  "loss_turn_bundle": 0.2869790148589866,
  "loss_theta_bundle": 0.0003524649479484415,
  "loss_theta_flat": 0.0002882917082385842,
  "loss_theta_near_flat": 0.0012743009399264768,
  "loss_theta_error_excess": 0.000187184195697726,
  "loss_theta_flat_excess": 0.00014124164726876266,
  "loss_theta_near_flat_excess": 0.000916361989968876,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001559133464435849,
  "loss_theta_small_neg": 0.0004784388005473879,
  "loss_theta_small_neg_excess": 0.00015816272909693793,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3481625482984422,
  "loss_false_turn_straight": 0.27325386792945605,
  "loss_transition_focal_raw": 0.9741540199042334,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.0372358243342736,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
