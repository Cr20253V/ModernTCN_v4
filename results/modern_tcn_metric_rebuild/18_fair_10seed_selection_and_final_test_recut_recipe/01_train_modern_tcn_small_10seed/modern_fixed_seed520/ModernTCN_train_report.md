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
| acc_main | 0.9653 |
| acc_turn | 0.5844 |
| acc_turn_pure | 0.5981 |
| acc_turn_transition | 0.5246 |
| main_confidence_mean | 0.9908 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0100 |
| turn_confidence_mean | 0.8563 |
| turn_low_conf_0p60_ratio | 0.1274 |
| turn_low_conf_0p70_ratio | 0.2043 |
| turn_right_recall | 0.6658 |
| turn_straight_recall | 0.5644 |
| turn_left_recall | 0.5540 |
| theta_mae_deg | 0.5995 |
| theta_abs_le_10_p95_abs_err_deg | 1.7072 |
| theta_neg_10_8_p95_abs_err_deg | 2.1616 |
| theta_pos_8_10_p95_abs_err_deg | 2.9653 |
| theta_abs_le_8_p95_abs_err_deg | 1.5192 |
| theta_neg_8_6_p95_abs_err_deg | 1.4145 |
| theta_pos_6_8_p95_abs_err_deg | 1.4057 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8351 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5394 |
| theta_flat_abs_p95_deg | 2.7028 |
| theta_flat_bias_deg | -0.2018 |
| theta_near_flat_abs_p95_deg | 1.8383 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2957 |
| theta_flat_turn_abs_p95_deg | 1.6689 |
| flat_recall | 0.9643 |
| stall_recall | 0.6458 |
| slope_recall | 0.9767 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7540 |
| downhill_recall | 0.7934 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    729,
    0,
    27
  ],
  [
    9,
    62,
    25
  ],
  [
    53,
    11,
    2686
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    532,
    153,
    114
  ],
  [
    450,
    1091,
    392
  ],
  [
    161,
    227,
    482
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.339858 |
| test_loss_turn_bundle_base | 0.379219 |
| test_loss_theta_bundle_base | 0.000146 |
| test_loss_transition_focal_raw | 1.778978 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.782018 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 379.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.5500 | 0.5435 |
| [0.60,0.70) | 16 | 0.3125 | 0.6438 |
| [0.70,0.80) | 23 | 0.3913 | 0.7456 |
| [0.80,0.90) | 47 | 0.5745 | 0.8570 |
| [0.90,1.00) | 3496 | 0.0209 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 459 | 0.5904 | 0.5329 |
| [0.60,0.70) | 277 | 0.5199 | 0.6501 |
| [0.70,0.80) | 363 | 0.5152 | 0.7497 |
| [0.80,0.90) | 477 | 0.5283 | 0.8534 |
| [0.90,1.00) | 2026 | 0.3174 | 0.9775 |


## 验证集最佳点

```json
{
  "loss_total": 0.7038897991664355,
  "acc_main": 0.9407307171853857,
  "acc_turn": 0.63382949932341,
  "acc_turn_pure": 0.6440511307767945,
  "acc_turn_transition": 0.5854037267080745,
  "false_turn_straight": 0.4267151767151767,
  "flat_recall": 0.9375951293759512,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9499332443257676,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.047619047619047616,
  "recall_main": [
    0.9375951293759512,
    0.3333333333333333,
    0.9499332443257676
  ],
  "turn_right_recall": 0.7298578199052133,
  "turn_straight_recall": 0.5732848232848233,
  "turn_left_recall": 0.6720604099244876,
  "recall_turn": [
    0.7298578199052133,
    0.5732848232848233,
    0.6720604099244876
  ],
  "cm_turn": [
    [
      616,
      184,
      44
    ],
    [
      453,
      1103,
      368
    ],
    [
      107,
      197,
      623
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      616,
      0,
      41
    ],
    [
      2,
      14,
      26
    ],
    [
      141,
      9,
      2846
    ]
  ],
  "main_confidence_mean": 0.9738965121039026,
  "main_confidence_error_mean": 0.8098475986618389,
  "main_low_conf_0p60_ratio": 0.0062246278755074425,
  "main_low_conf_0p70_ratio": 0.05791610284167794,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 23,
      "error_rate": 0.2608695652173913,
      "mean_confidence": 0.5472599749377216
    },
    {
      "bin": "[0.60,0.70)",
      "n": 191,
      "error_rate": 0.4712041884816754,
      "mean_confidence": 0.6260074810019182
    },
    {
      "bin": "[0.70,0.80)",
      "n": 20,
      "error_rate": 0.5,
      "mean_confidence": 0.7566227773567096
    },
    {
      "bin": "[0.80,0.90)",
      "n": 30,
      "error_rate": 0.4,
      "mean_confidence": 0.8600695231461806
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3431,
      "error_rate": 0.02943748178373652,
      "mean_confidence": 0.9983849206317302
    }
  ],
  "turn_confidence_mean": 0.8617231969348467,
  "turn_confidence_error_mean": 0.783957116382874,
  "turn_low_conf_0p60_ratio": 0.1307171853856563,
  "turn_low_conf_0p70_ratio": 0.20595399188092017,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 483,
      "error_rate": 0.6521739130434783,
      "mean_confidence": 0.5219201803531397
    },
    {
      "bin": "[0.60,0.70)",
      "n": 278,
      "error_rate": 0.5251798561151079,
      "mean_confidence": 0.6519936728312792
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.5545454545454546,
      "mean_confidence": 0.749181171211973
    },
    {
      "bin": "[0.80,0.90)",
      "n": 428,
      "error_rate": 0.48130841121495327,
      "mean_confidence": 0.8502481730157672
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2176,
      "error_rate": 0.23115808823529413,
      "mean_confidence": 0.9832672426313865
    }
  ],
  "theta_mae_rad": 0.013184360228478909,
  "theta_mae_deg": 0.7554081678390503,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.803670745272525,
  "slope_sign_acc": 0.970161511086778,
  "theta_flat_mae_deg": 1.1363943815231323,
  "theta_flat_abs_p95_deg": 4.290311336517334,
  "theta_flat_abs_max_deg": 7.300698280334473,
  "theta_flat_bias_deg": 0.49082499742507935,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4603606462478638,
  "theta_near_flat_abs_p95_deg": 4.290396690368652,
  "theta_near_flat_abs_max_deg": 7.300698280334473,
  "theta_near_flat_bias_deg": 0.9075902700424194,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0092576742172241,
  "theta_flat_turn_abs_p95_deg": 4.290311336517334,
  "theta_flat_turn_abs_max_deg": 7.300698280334473,
  "theta_flat_turn_bias_deg": 0.4945654273033142,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7554081678390503,
  "theta_slope_control_abs_p95_deg": 9.069637298583984,
  "theta_slope_control_abs_max_deg": 12.857210159301758,
  "theta_slope_control_bias_deg": 0.031805772334337234,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7554081082344055,
  "theta_all_rmse_deg": 1.1620396375656128,
  "theta_all_p95_abs_err_deg": 2.7804205417633057,
  "theta_all_max_abs_err_deg": 7.8006978034973145,
  "theta_all_bias_deg": 0.03180576488375664,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6718608140945435,
  "theta_active_abs_ge_2_rmse_deg": 0.9906582236289978,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9381147623062134,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.1207275390625,
  "theta_active_abs_ge_2_bias_deg": -0.06885365396738052,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7750205993652344,
  "theta_abs_le_8_rmse_deg": 1.1905500888824463,
  "theta_abs_le_8_p95_abs_err_deg": 2.790311336517334,
  "theta_abs_le_8_max_abs_err_deg": 7.8006978034973145,
  "theta_abs_le_8_bias_deg": 0.0559145025908947,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7554081082344055,
  "theta_abs_le_10_rmse_deg": 1.1620396375656128,
  "theta_abs_le_10_p95_abs_err_deg": 2.7804205417633057,
  "theta_abs_le_10_max_abs_err_deg": 7.8006978034973145,
  "theta_abs_le_10_bias_deg": 0.03180576488375664,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7257683277130127,
  "theta_pos_8_10_rmse_deg": 0.9609925150871277,
  "theta_pos_8_10_p95_abs_err_deg": 1.5638073682785034,
  "theta_pos_8_10_max_abs_err_deg": 5.583103656768799,
  "theta_pos_8_10_bias_deg": -0.4812195897102356,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6186578273773193,
  "theta_neg_10_8_rmse_deg": 1.1017019748687744,
  "theta_neg_10_8_p95_abs_err_deg": 1.629568099975586,
  "theta_neg_10_8_max_abs_err_deg": 6.880793571472168,
  "theta_neg_10_8_bias_deg": 0.3485344350337982,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6258348226547241,
  "theta_pos_6_8_rmse_deg": 0.8029589653015137,
  "theta_pos_6_8_p95_abs_err_deg": 1.6412336826324463,
  "theta_pos_6_8_max_abs_err_deg": 2.9721224308013916,
  "theta_pos_6_8_bias_deg": -0.3130124807357788,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.724341094493866,
  "theta_neg_8_6_rmse_deg": 1.0809553861618042,
  "theta_neg_8_6_p95_abs_err_deg": 2.3183107376098633,
  "theta_neg_8_6_max_abs_err_deg": 7.1207275390625,
  "theta_neg_8_6_bias_deg": 0.07719999551773071,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6464924812316895,
  "theta_neg_4_2_rmse_deg": 0.9329699277877808,
  "theta_neg_4_2_p95_abs_err_deg": 1.9943625926971436,
  "theta_neg_4_2_max_abs_err_deg": 4.387475490570068,
  "theta_neg_4_2_bias_deg": -0.09163506329059601,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6052812337875366,
  "theta_neg_2_0p5_rmse_deg": 0.8428202271461487,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3950611352920532,
  "theta_neg_2_0p5_max_abs_err_deg": 4.742764472961426,
  "theta_neg_2_0p5_bias_deg": 0.02660262957215309,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.273470401763916,
  "theta_pos_0p5_2_rmse_deg": 1.6366420984268188,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.790311336517334,
  "theta_pos_0p5_2_max_abs_err_deg": 4.260841369628906,
  "theta_pos_0p5_2_bias_deg": 0.4164389371871948,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.40023617007251683,
  "loss_turn": 1.5169071384953872,
  "loss_theta": 0.0004113317831483681,
  "loss_main_bundle_base": 0.40023617007251683,
  "loss_turn_bundle_base": 0.30338143549042884,
  "loss_theta_bundle_base": 0.0002721803223525826,
  "loss_main_bundle": 0.40023617007251683,
  "loss_turn_bundle": 0.30338143549042884,
  "loss_theta_bundle": 0.0002721803223525826,
  "loss_theta_flat": 0.00023990804147074052,
  "loss_theta_near_flat": 0.0014539078474725333,
  "loss_theta_error_excess": 0.00015684070055535586,
  "loss_theta_flat_excess": 0.0001424537819913552,
  "loss_theta_near_flat_excess": 0.0010680085352744216,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.316839608165318e-05,
  "loss_theta_small_neg": 0.0002626998192414576,
  "loss_theta_small_neg_excess": 6.766812333173002e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3641328145347848,
  "loss_false_turn_straight": 0.3168489889056499,
  "loss_transition_focal_raw": 1.32064062581172,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.131154360853606,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
