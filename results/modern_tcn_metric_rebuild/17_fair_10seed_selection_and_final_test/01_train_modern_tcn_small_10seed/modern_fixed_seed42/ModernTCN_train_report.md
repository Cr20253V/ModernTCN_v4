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
| acc_main | 0.9617 |
| acc_turn | 0.5769 |
| acc_turn_pure | 0.5967 |
| acc_turn_transition | 0.4903 |
| main_confidence_mean | 0.9866 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0119 |
| turn_confidence_mean | 0.7555 |
| turn_low_conf_0p60_ratio | 0.2568 |
| turn_low_conf_0p70_ratio | 0.3951 |
| turn_right_recall | 0.5469 |
| turn_straight_recall | 0.6063 |
| turn_left_recall | 0.5391 |
| theta_mae_deg | 0.7671 |
| theta_abs_le_10_p95_abs_err_deg | 2.0100 |
| theta_neg_10_8_p95_abs_err_deg | 1.1168 |
| theta_pos_8_10_p95_abs_err_deg | 2.7992 |
| theta_abs_le_8_p95_abs_err_deg | 1.9722 |
| theta_neg_8_6_p95_abs_err_deg | 1.8382 |
| theta_pos_6_8_p95_abs_err_deg | 1.9627 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4604 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8057 |
| theta_flat_abs_p95_deg | 2.8515 |
| theta_flat_bias_deg | 0.1078 |
| theta_near_flat_abs_p95_deg | 1.9039 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0617 |
| theta_flat_turn_abs_p95_deg | 1.9300 |
| flat_recall | 0.9630 |
| stall_recall | 0.6667 |
| slope_recall | 0.9716 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7500 |
| downhill_recall | 0.7900 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    728,
    0,
    28
  ],
  [
    10,
    64,
    22
  ],
  [
    65,
    13,
    2672
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    437,
    244,
    118
  ],
  [
    371,
    1172,
    390
  ],
  [
    127,
    274,
    469
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.306712 |
| test_loss_turn_bundle_base | 0.096609 |
| test_loss_theta_bundle_base | 0.000206 |
| test_loss_transition_focal_raw | 1.045294 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.181547 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 56
- train_seconds: 885.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.5652 | 0.5456 |
| [0.60,0.70) | 20 | 0.5000 | 0.6349 |
| [0.70,0.80) | 41 | 0.5366 | 0.7659 |
| [0.80,0.90) | 72 | 0.3750 | 0.8512 |
| [0.90,1.00) | 3446 | 0.0192 | 0.9970 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 925 | 0.5481 | 0.5039 |
| [0.60,0.70) | 498 | 0.5181 | 0.6506 |
| [0.70,0.80) | 534 | 0.4906 | 0.7503 |
| [0.80,0.90) | 524 | 0.4218 | 0.8485 |
| [0.90,1.00) | 1121 | 0.2462 | 0.9688 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4903
- theta_mae_deg <= 0.7000 未满足，实际 0.7671

## 验证集最佳点

```json
{
  "loss_total": 0.37369624226277187,
  "acc_main": 0.9502029769959405,
  "acc_turn": 0.6208389715832205,
  "acc_turn_pure": 0.6335627663061292,
  "acc_turn_transition": 0.5605590062111802,
  "false_turn_straight": 0.38513513513513514,
  "flat_recall": 0.969558599695586,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9529372496662216,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.969558599695586,
    0.4523809523809524,
    0.9529372496662216
  ],
  "turn_right_recall": 0.5699052132701422,
  "turn_straight_recall": 0.6148648648648649,
  "turn_left_recall": 0.6796116504854369,
  "recall_turn": [
    0.5699052132701422,
    0.6148648648648649,
    0.6796116504854369
  ],
  "cm_turn": [
    [
      481,
      250,
      113
    ],
    [
      318,
      1183,
      423
    ],
    [
      56,
      241,
      630
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
      19,
      23
    ],
    [
      132,
      9,
      2855
    ]
  ],
  "main_confidence_mean": 0.9673360453492431,
  "main_confidence_error_mean": 0.7360285586978976,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.43386243386243384,
      "mean_confidence": 0.4994617955691054
    },
    {
      "bin": "[0.60,0.70)",
      "n": 23,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.6509285619133692
    },
    {
      "bin": "[0.70,0.80)",
      "n": 16,
      "error_rate": 0.3125,
      "mean_confidence": 0.7566827080512941
    },
    {
      "bin": "[0.80,0.90)",
      "n": 43,
      "error_rate": 0.2558139534883721,
      "mean_confidence": 0.8568760622038819
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3424,
      "error_rate": 0.021904205607476634,
      "mean_confidence": 0.9976590120547013
    }
  ],
  "turn_confidence_mean": 0.7631583516189142,
  "turn_confidence_error_mean": 0.6910545720909311,
  "turn_low_conf_0p60_ratio": 0.25602165087956696,
  "turn_low_conf_0p70_ratio": 0.38457374830852503,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 946,
      "error_rate": 0.5665961945031712,
      "mean_confidence": 0.49439333723461215
    },
    {
      "bin": "[0.60,0.70)",
      "n": 475,
      "error_rate": 0.4336842105263158,
      "mean_confidence": 0.6498359410340557
    },
    {
      "bin": "[0.70,0.80)",
      "n": 464,
      "error_rate": 0.3857758620689655,
      "mean_confidence": 0.7498734879388349
    },
    {
      "bin": "[0.80,0.90)",
      "n": 524,
      "error_rate": 0.3606870229007634,
      "mean_confidence": 0.8506625716161528
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1286,
      "error_rate": 0.22628304821150855,
      "mean_confidence": 0.9718611619644516
    }
  ],
  "theta_mae_rad": 0.016233785077929497,
  "theta_mae_deg": 0.9301273226737976,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.7942157953281423,
  "slope_sign_acc": 0.9657815494114427,
  "theta_flat_mae_deg": 1.2292234897613525,
  "theta_flat_abs_p95_deg": 3.895153284072876,
  "theta_flat_abs_max_deg": 7.6635332107543945,
  "theta_flat_bias_deg": 0.7682303190231323,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.573914647102356,
  "theta_near_flat_abs_p95_deg": 3.8952324390411377,
  "theta_near_flat_abs_max_deg": 7.6635332107543945,
  "theta_near_flat_bias_deg": 1.1126327514648438,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.4612678289413452,
  "theta_flat_turn_abs_p95_deg": 3.895153284072876,
  "theta_flat_turn_abs_max_deg": 7.6635332107543945,
  "theta_flat_turn_bias_deg": 0.8719266653060913,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9301273226737976,
  "theta_slope_control_abs_p95_deg": 9.40689468383789,
  "theta_slope_control_abs_max_deg": 11.775418281555176,
  "theta_slope_control_bias_deg": -0.16714419424533844,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9301273822784424,
  "theta_all_rmse_deg": 1.2966783046722412,
  "theta_all_p95_abs_err_deg": 2.5059738159179688,
  "theta_all_max_abs_err_deg": 8.163533210754395,
  "theta_all_bias_deg": -0.16714417934417725,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8645378351211548,
  "theta_active_abs_ge_2_rmse_deg": 1.1732335090637207,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1050190925598145,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.631436347961426,
  "theta_active_abs_ge_2_bias_deg": -0.37226471304893494,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9864180684089661,
  "theta_abs_le_8_rmse_deg": 1.3500374555587769,
  "theta_abs_le_8_p95_abs_err_deg": 2.6525588035583496,
  "theta_abs_le_8_max_abs_err_deg": 8.163533210754395,
  "theta_abs_le_8_bias_deg": -0.11849568039178848,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9301273822784424,
  "theta_abs_le_10_rmse_deg": 1.2966783046722412,
  "theta_abs_le_10_p95_abs_err_deg": 2.5059738159179688,
  "theta_abs_le_10_max_abs_err_deg": 8.163533210754395,
  "theta_abs_le_10_bias_deg": -0.16714417934417725,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7132489085197449,
  "theta_pos_8_10_rmse_deg": 0.9368038177490234,
  "theta_pos_8_10_p95_abs_err_deg": 1.651625633239746,
  "theta_pos_8_10_max_abs_err_deg": 5.0560431480407715,
  "theta_pos_8_10_bias_deg": -0.547400712966919,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6717174649238586,
  "theta_neg_10_8_rmse_deg": 1.1389453411102295,
  "theta_neg_10_8_p95_abs_err_deg": 2.3031420707702637,
  "theta_neg_10_8_max_abs_err_deg": 6.210327625274658,
  "theta_neg_10_8_bias_deg": -0.1943155825138092,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8934556245803833,
  "theta_pos_6_8_rmse_deg": 1.0877071619033813,
  "theta_pos_6_8_p95_abs_err_deg": 2.007624387741089,
  "theta_pos_6_8_max_abs_err_deg": 3.2774550914764404,
  "theta_pos_6_8_bias_deg": -0.5833895206451416,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8570122718811035,
  "theta_neg_8_6_rmse_deg": 1.1815828084945679,
  "theta_neg_8_6_p95_abs_err_deg": 2.0085268020629883,
  "theta_neg_8_6_max_abs_err_deg": 6.064924240112305,
  "theta_neg_8_6_bias_deg": -0.5531278848648071,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8368386030197144,
  "theta_neg_4_2_rmse_deg": 1.1701970100402832,
  "theta_neg_4_2_p95_abs_err_deg": 2.210092782974243,
  "theta_neg_4_2_max_abs_err_deg": 6.529364109039307,
  "theta_neg_4_2_bias_deg": -0.3111984431743622,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6009474992752075,
  "theta_neg_2_0p5_rmse_deg": 0.830244779586792,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.688744068145752,
  "theta_neg_2_0p5_max_abs_err_deg": 3.930734872817993,
  "theta_neg_2_0p5_bias_deg": 0.0664060190320015,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.467613935470581,
  "theta_pos_0p5_2_rmse_deg": 1.7714755535125732,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.180304527282715,
  "theta_pos_0p5_2_max_abs_err_deg": 4.293308734893799,
  "theta_pos_0p5_2_bias_deg": 1.123704195022583,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2803587636218503,
  "loss_turn": 1.1625378471911356,
  "loss_theta": 0.0005121151989777049,
  "loss_main_bundle_base": 0.2803587636218503,
  "loss_turn_bundle_base": 0.09300302604014238,
  "loss_theta_bundle_base": 0.0003344492583597994,
  "loss_main_bundle": 0.2803587636218503,
  "loss_turn_bundle": 0.09300302604014238,
  "loss_theta_bundle": 0.0003344492583597994,
  "loss_theta_flat": 0.0002671827250788628,
  "loss_theta_near_flat": 0.0014676365307916626,
  "loss_theta_error_excess": 0.00017344619255624485,
  "loss_theta_flat_excess": 0.00014549689745881465,
  "loss_theta_near_flat_excess": 0.001059020419746224,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00012051663025555167,
  "loss_theta_small_neg": 0.0004109815484875654,
  "loss_theta_small_neg_excess": 0.00012705408339798248,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3568223879124379,
  "loss_false_turn_straight": 0.2799529323477868,
  "loss_transition_focal_raw": 0.8407908746128314,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.3880159411604662,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
