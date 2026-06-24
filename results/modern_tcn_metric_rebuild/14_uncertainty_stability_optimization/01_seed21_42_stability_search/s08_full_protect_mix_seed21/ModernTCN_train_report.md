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
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.06,
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
  "select_stall_weight": 0.25,
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
  "select_theta_flat_peak_weight": 1.1,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.1,
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
| acc_main | 0.9528 |
| acc_turn | 0.5655 |
| acc_turn_pure | 0.5872 |
| acc_turn_transition | 0.4709 |
| main_confidence_mean | 0.9848 |
| main_low_conf_0p60_ratio | 0.0097 |
| main_low_conf_0p70_ratio | 0.0186 |
| turn_confidence_mean | 0.8012 |
| turn_low_conf_0p60_ratio | 0.1863 |
| turn_low_conf_0p70_ratio | 0.3015 |
| turn_right_recall | 0.6533 |
| turn_straight_recall | 0.5391 |
| turn_left_recall | 0.5437 |
| theta_mae_deg | 0.7069 |
| theta_abs_le_10_p95_abs_err_deg | 2.0192 |
| theta_neg_10_8_p95_abs_err_deg | 2.0940 |
| theta_pos_8_10_p95_abs_err_deg | 2.7336 |
| theta_abs_le_8_p95_abs_err_deg | 1.9453 |
| theta_neg_8_6_p95_abs_err_deg | 1.8625 |
| theta_pos_6_8_p95_abs_err_deg | 1.3104 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8960 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7815 |
| theta_flat_abs_p95_deg | 2.3349 |
| theta_flat_bias_deg | -0.0092 |
| theta_near_flat_abs_p95_deg | 1.6182 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2114 |
| theta_flat_turn_abs_p95_deg | 1.5401 |
| flat_recall | 0.9180 |
| stall_recall | 0.6458 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7466 |
| downhill_recall | 0.8150 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    694,
    0,
    62
  ],
  [
    9,
    62,
    25
  ],
  [
    59,
    15,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    522,
    171,
    106
  ],
  [
    483,
    1042,
    408
  ],
  [
    205,
    192,
    473
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.306566 |
| test_loss_turn_bundle_base | 0.341089 |
| test_loss_theta_bundle_base | 0.000222 |
| test_loss_transition_focal_raw | 1.253659 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.329973 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 52
- train_seconds: 289.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 35 | 0.7143 | 0.5479 |
| [0.60,0.70) | 32 | 0.5938 | 0.6392 |
| [0.70,0.80) | 31 | 0.4839 | 0.7572 |
| [0.80,0.90) | 75 | 0.4667 | 0.8626 |
| [0.90,1.00) | 3429 | 0.0222 | 0.9972 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 671 | 0.5797 | 0.5078 |
| [0.60,0.70) | 415 | 0.5422 | 0.6481 |
| [0.70,0.80) | 503 | 0.5686 | 0.7527 |
| [0.80,0.90) | 504 | 0.4782 | 0.8492 |
| [0.90,1.00) | 1509 | 0.2810 | 0.9740 |


## 验证集最佳点

```json
{
  "loss_total": 0.5808423258938873,
  "acc_main": 0.9385656292286875,
  "acc_turn": 0.6143437077131259,
  "acc_turn_pure": 0.6286463454605048,
  "acc_turn_transition": 0.546583850931677,
  "false_turn_straight": 0.4693347193347193,
  "flat_recall": 0.9178082191780822,
  "stall_recall": 0.5,
  "slope_recall": 0.9492656875834445,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9178082191780822,
    0.5,
    0.9492656875834445
  ],
  "turn_right_recall": 0.7061611374407583,
  "turn_straight_recall": 0.5306652806652806,
  "turn_left_recall": 0.7044228694714132,
  "recall_turn": [
    0.7061611374407583,
    0.5306652806652806,
    0.7044228694714132
  ],
  "cm_turn": [
    [
      596,
      200,
      48
    ],
    [
      484,
      1021,
      419
    ],
    [
      115,
      159,
      653
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      603,
      0,
      54
    ],
    [
      0,
      21,
      21
    ],
    [
      139,
      13,
      2844
    ]
  ],
  "main_confidence_mean": 0.9683147957679379,
  "main_confidence_error_mean": 0.7755362444108925,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.05872801082543978,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.4731182795698925,
      "mean_confidence": 0.5792093907684205
    },
    {
      "bin": "[0.60,0.70)",
      "n": 31,
      "error_rate": 0.5161290322580645,
      "mean_confidence": 0.6331653514131135
    },
    {
      "bin": "[0.70,0.80)",
      "n": 46,
      "error_rate": 0.3695652173913043,
      "mean_confidence": 0.7530989132766829
    },
    {
      "bin": "[0.80,0.90)",
      "n": 51,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8597660576114227
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3381,
      "error_rate": 0.026323572907423837,
      "mean_confidence": 0.9973592069910937
    }
  ],
  "turn_confidence_mean": 0.8156096266687038,
  "turn_confidence_error_mean": 0.7394365905776048,
  "turn_low_conf_0p60_ratio": 0.1753721244925575,
  "turn_low_conf_0p70_ratio": 0.2752368064952639,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 648,
      "error_rate": 0.6080246913580247,
      "mean_confidence": 0.4985159959818501
    },
    {
      "bin": "[0.60,0.70)",
      "n": 369,
      "error_rate": 0.5474254742547425,
      "mean_confidence": 0.6514213092323615
    },
    {
      "bin": "[0.70,0.80)",
      "n": 455,
      "error_rate": 0.45714285714285713,
      "mean_confidence": 0.7503208285888017
    },
    {
      "bin": "[0.80,0.90)",
      "n": 502,
      "error_rate": 0.4701195219123506,
      "mean_confidence": 0.8495708683885623
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1721,
      "error_rate": 0.22370714700755376,
      "mean_confidence": 0.9775619925037289
    }
  ],
  "theta_mae_rad": 0.01419304870069027,
  "theta_mae_deg": 0.8132017254829407,
  "uphill_recall": 0.7725067385444744,
  "downhill_recall": 0.8147942157953282,
  "slope_sign_acc": 0.9622228305502327,
  "theta_flat_mae_deg": 1.1741245985031128,
  "theta_flat_abs_p95_deg": 4.044068336486816,
  "theta_flat_abs_max_deg": 9.244338035583496,
  "theta_flat_bias_deg": 0.7004286646842957,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6468815803527832,
  "theta_near_flat_abs_p95_deg": 4.655941009521484,
  "theta_near_flat_abs_max_deg": 9.244338035583496,
  "theta_near_flat_bias_deg": 1.201014518737793,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3892918825149536,
  "theta_flat_turn_abs_p95_deg": 4.970010280609131,
  "theta_flat_turn_abs_max_deg": 9.244338035583496,
  "theta_flat_turn_bias_deg": 0.7979626059532166,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8132017254829407,
  "theta_slope_control_abs_p95_deg": 9.119937896728516,
  "theta_slope_control_abs_max_deg": 12.033529281616211,
  "theta_slope_control_bias_deg": 0.3110803961753845,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8132017254829407,
  "theta_all_rmse_deg": 1.233036756515503,
  "theta_all_p95_abs_err_deg": 2.5440680980682373,
  "theta_all_max_abs_err_deg": 9.74433708190918,
  "theta_all_bias_deg": 0.3110804259777069,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7340542078018188,
  "theta_active_abs_ge_2_rmse_deg": 1.0584534406661987,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.066915512084961,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.749055862426758,
  "theta_active_abs_ge_2_bias_deg": 0.2256993055343628,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8594012260437012,
  "theta_abs_le_8_rmse_deg": 1.2815759181976318,
  "theta_abs_le_8_p95_abs_err_deg": 2.6979360580444336,
  "theta_abs_le_8_max_abs_err_deg": 9.74433708190918,
  "theta_abs_le_8_bias_deg": 0.3722921311855316,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8132017254829407,
  "theta_abs_le_10_rmse_deg": 1.233036756515503,
  "theta_abs_le_10_p95_abs_err_deg": 2.5440680980682373,
  "theta_abs_le_10_max_abs_err_deg": 9.74433708190918,
  "theta_abs_le_10_bias_deg": 0.3110804259777069,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5538298487663269,
  "theta_pos_8_10_rmse_deg": 0.7331298589706421,
  "theta_pos_8_10_p95_abs_err_deg": 1.3077247142791748,
  "theta_pos_8_10_max_abs_err_deg": 4.846503257751465,
  "theta_pos_8_10_bias_deg": -0.3317550718784332,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6838973760604858,
  "theta_neg_10_8_rmse_deg": 1.2171919345855713,
  "theta_neg_10_8_p95_abs_err_deg": 1.9629384279251099,
  "theta_neg_10_8_max_abs_err_deg": 7.019230842590332,
  "theta_neg_10_8_bias_deg": 0.4441143572330475,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5512211322784424,
  "theta_pos_6_8_rmse_deg": 0.7680853009223938,
  "theta_pos_6_8_p95_abs_err_deg": 1.56657075881958,
  "theta_pos_6_8_max_abs_err_deg": 3.2954115867614746,
  "theta_pos_6_8_bias_deg": -0.04183521866798401,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7191924452781677,
  "theta_neg_8_6_rmse_deg": 1.0955467224121094,
  "theta_neg_8_6_p95_abs_err_deg": 1.8887754678726196,
  "theta_neg_8_6_max_abs_err_deg": 7.749055862426758,
  "theta_neg_8_6_bias_deg": 0.0830601379275322,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8234199285507202,
  "theta_neg_4_2_rmse_deg": 1.0717265605926514,
  "theta_neg_4_2_p95_abs_err_deg": 2.0328357219696045,
  "theta_neg_4_2_max_abs_err_deg": 6.11381196975708,
  "theta_neg_4_2_bias_deg": 0.456451416015625,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5062375664710999,
  "theta_neg_2_0p5_rmse_deg": 0.6708554625511169,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1844431161880493,
  "theta_neg_2_0p5_max_abs_err_deg": 3.4999074935913086,
  "theta_neg_2_0p5_bias_deg": -0.09538870304822922,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.221375584602356,
  "theta_pos_0p5_2_rmse_deg": 1.5613940954208374,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5440680980682373,
  "theta_pos_0p5_2_max_abs_err_deg": 4.321765899658203,
  "theta_pos_0p5_2_bias_deg": 0.8710348010063171,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.31003789893667816,
  "loss_turn": 1.1270083885876832,
  "loss_theta": 0.00046316225995991447,
  "loss_main_bundle_base": 0.31003789893667816,
  "loss_turn_bundle_base": 0.2704820048502559,
  "loss_theta_bundle_base": 0.00032241696627944183,
  "loss_main_bundle": 0.31003789893667816,
  "loss_turn_bundle": 0.2704820048502559,
  "loss_theta_bundle": 0.00032241696627944183,
  "loss_theta_flat": 0.0002500218139953367,
  "loss_theta_near_flat": 0.00165647011778301,
  "loss_theta_error_excess": 0.00018048087051544711,
  "loss_theta_flat_excess": 0.0001380608729044283,
  "loss_theta_near_flat_excess": 0.0012534068289297318,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010366532367153827,
  "loss_theta_small_neg": 0.0003493565902745928,
  "loss_theta_small_neg_excess": 7.619306855922922e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.41071204389061106,
  "loss_false_turn_straight": 0.3274223300133087,
  "loss_transition_focal_raw": 0.9243186634674124,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.7616528579377397,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
