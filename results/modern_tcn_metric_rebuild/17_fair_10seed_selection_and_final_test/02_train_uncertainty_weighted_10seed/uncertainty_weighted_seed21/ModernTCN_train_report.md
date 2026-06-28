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
| acc_main | 0.9572 |
| acc_turn | 0.5952 |
| acc_turn_pure | 0.6169 |
| acc_turn_transition | 0.5007 |
| main_confidence_mean | 0.9895 |
| main_low_conf_0p60_ratio | 0.0050 |
| main_low_conf_0p70_ratio | 0.0100 |
| turn_confidence_mean | 0.8223 |
| turn_low_conf_0p60_ratio | 0.1694 |
| turn_low_conf_0p70_ratio | 0.2829 |
| turn_right_recall | 0.5920 |
| turn_straight_recall | 0.6648 |
| turn_left_recall | 0.4437 |
| theta_mae_deg | 0.6678 |
| theta_abs_le_10_p95_abs_err_deg | 1.7466 |
| theta_neg_10_8_p95_abs_err_deg | 1.7480 |
| theta_pos_8_10_p95_abs_err_deg | 3.2768 |
| theta_abs_le_8_p95_abs_err_deg | 1.6044 |
| theta_neg_8_6_p95_abs_err_deg | 1.4207 |
| theta_pos_6_8_p95_abs_err_deg | 1.3226 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6938 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5950 |
| theta_flat_abs_p95_deg | 2.5713 |
| theta_flat_bias_deg | -0.2413 |
| theta_near_flat_abs_p95_deg | 1.6069 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0195 |
| theta_flat_turn_abs_p95_deg | 1.5688 |
| flat_recall | 0.9286 |
| stall_recall | 0.6979 |
| slope_recall | 0.9742 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7500 |
| downhill_recall | 0.8087 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    702,
    0,
    54
  ],
  [
    9,
    67,
    20
  ],
  [
    56,
    15,
    2679
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    473,
    234,
    92
  ],
  [
    377,
    1285,
    271
  ],
  [
    161,
    323,
    386
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.321786 |
| test_loss_turn_bundle_base | 0.121562 |
| test_loss_theta_bundle_base | 0.000163 |
| test_loss_transition_focal_raw | 1.472105 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.085018 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 89
- train_seconds: 1817.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 18 | 0.7222 | 0.5473 |
| [0.60,0.70) | 18 | 0.6667 | 0.6582 |
| [0.70,0.80) | 33 | 0.6970 | 0.7383 |
| [0.80,0.90) | 45 | 0.4000 | 0.8620 |
| [0.90,1.00) | 3488 | 0.0252 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 610 | 0.6000 | 0.5132 |
| [0.60,0.70) | 409 | 0.5086 | 0.6495 |
| [0.70,0.80) | 358 | 0.5279 | 0.7503 |
| [0.80,0.90) | 459 | 0.4488 | 0.8494 |
| [0.90,1.00) | 1766 | 0.2769 | 0.9767 |


## 验证集最佳点

```json
{
  "loss_total": 0.4493895671364419,
  "acc_main": 0.9358592692828146,
  "acc_turn": 0.6625169147496617,
  "acc_turn_pure": 0.6696165191740413,
  "acc_turn_transition": 0.6288819875776398,
  "false_turn_straight": 0.3134095634095634,
  "flat_recall": 0.9056316590563166,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9492656875834445,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9056316590563166,
    0.4523809523809524,
    0.9492656875834445
  ],
  "turn_right_recall": 0.6469194312796208,
  "turn_straight_recall": 0.6865904365904366,
  "turn_left_recall": 0.6267529665587918,
  "recall_turn": [
    0.6469194312796208,
    0.6865904365904366,
    0.6267529665587918
  ],
  "cm_turn": [
    [
      546,
      280,
      18
    ],
    [
      323,
      1321,
      280
    ],
    [
      61,
      285,
      581
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      595,
      0,
      62
    ],
    [
      0,
      19,
      23
    ],
    [
      140,
      12,
      2844
    ]
  ],
  "main_confidence_mean": 0.9689238693320084,
  "main_confidence_error_mean": 0.7824819713922418,
  "main_low_conf_0p60_ratio": 0.052232746955345064,
  "main_low_conf_0p70_ratio": 0.059810554803788905,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 193,
      "error_rate": 0.48186528497409326,
      "mean_confidence": 0.5447838159906193
    },
    {
      "bin": "[0.60,0.70)",
      "n": 28,
      "error_rate": 0.35714285714285715,
      "mean_confidence": 0.6457809845391559
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.38095238095238093,
      "mean_confidence": 0.7597741922390775
    },
    {
      "bin": "[0.80,0.90)",
      "n": 32,
      "error_rate": 0.34375,
      "mean_confidence": 0.8612391816650401
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3421,
      "error_rate": 0.033615901783104356,
      "mean_confidence": 0.9977882611161014
    }
  ],
  "turn_confidence_mean": 0.8300058508723903,
  "turn_confidence_error_mean": 0.7634826349339582,
  "turn_low_conf_0p60_ratio": 0.1634641407307172,
  "turn_low_conf_0p70_ratio": 0.24979702300405954,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 604,
      "error_rate": 0.5298013245033113,
      "mean_confidence": 0.4813517729092015
    },
    {
      "bin": "[0.60,0.70)",
      "n": 319,
      "error_rate": 0.43260188087774293,
      "mean_confidence": 0.6490641973516804
    },
    {
      "bin": "[0.70,0.80)",
      "n": 351,
      "error_rate": 0.43874643874643876,
      "mean_confidence": 0.7518614983861004
    },
    {
      "bin": "[0.80,0.90)",
      "n": 476,
      "error_rate": 0.38865546218487396,
      "mean_confidence": 0.8515412776331559
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1945,
      "error_rate": 0.23136246786632392,
      "mean_confidence": 0.9767849023620747
    }
  ],
  "theta_mae_rad": 0.013566398061811924,
  "theta_mae_deg": 0.77729731798172,
  "uphill_recall": 0.769811320754717,
  "downhill_recall": 0.8220244716351501,
  "slope_sign_acc": 0.9794689296468656,
  "theta_flat_mae_deg": 1.0982534885406494,
  "theta_flat_abs_p95_deg": 3.896146774291992,
  "theta_flat_abs_max_deg": 8.142107963562012,
  "theta_flat_bias_deg": 0.482412725687027,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.468130111694336,
  "theta_near_flat_abs_p95_deg": 4.872505187988281,
  "theta_near_flat_abs_max_deg": 8.142107963562012,
  "theta_near_flat_bias_deg": 1.0986639261245728,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.254620909690857,
  "theta_flat_turn_abs_p95_deg": 5.450430393218994,
  "theta_flat_turn_abs_max_deg": 8.142107963562012,
  "theta_flat_turn_bias_deg": 0.813662052154541,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.77729731798172,
  "theta_slope_control_abs_p95_deg": 9.495332717895508,
  "theta_slope_control_abs_max_deg": 13.620000839233398,
  "theta_slope_control_bias_deg": -0.12004103511571884,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7772972583770752,
  "theta_all_rmse_deg": 1.1578103303909302,
  "theta_all_p95_abs_err_deg": 2.3961451053619385,
  "theta_all_max_abs_err_deg": 8.642107009887695,
  "theta_all_bias_deg": -0.12004103511571884,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7069138884544373,
  "theta_active_abs_ge_2_rmse_deg": 0.9868524074554443,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8623064756393433,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.849689483642578,
  "theta_active_abs_ge_2_bias_deg": -0.25215455889701843,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8097346425056458,
  "theta_abs_le_8_rmse_deg": 1.2029191255569458,
  "theta_abs_le_8_p95_abs_err_deg": 2.4342362880706787,
  "theta_abs_le_8_max_abs_err_deg": 8.642107009887695,
  "theta_abs_le_8_bias_deg": -0.06599181145429611,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7772972583770752,
  "theta_abs_le_10_rmse_deg": 1.1578103303909302,
  "theta_abs_le_10_p95_abs_err_deg": 2.3961451053619385,
  "theta_abs_le_10_max_abs_err_deg": 8.642107009887695,
  "theta_abs_le_10_bias_deg": -0.12004103511571884,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5610188841819763,
  "theta_pos_8_10_rmse_deg": 0.7935274243354797,
  "theta_pos_8_10_p95_abs_err_deg": 1.5758970975875854,
  "theta_pos_8_10_max_abs_err_deg": 4.888725280761719,
  "theta_pos_8_10_bias_deg": -0.2822569012641907,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7212701439857483,
  "theta_neg_10_8_rmse_deg": 1.0758352279663086,
  "theta_neg_10_8_p95_abs_err_deg": 1.8288651704788208,
  "theta_neg_10_8_max_abs_err_deg": 5.849689483642578,
  "theta_neg_10_8_bias_deg": -0.41498392820358276,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6160163879394531,
  "theta_pos_6_8_rmse_deg": 0.7774364948272705,
  "theta_pos_6_8_p95_abs_err_deg": 1.5162824392318726,
  "theta_pos_6_8_max_abs_err_deg": 2.8827648162841797,
  "theta_pos_6_8_bias_deg": -0.14716890454292297,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7733370661735535,
  "theta_neg_8_6_rmse_deg": 1.0746511220932007,
  "theta_neg_8_6_p95_abs_err_deg": 1.8211252689361572,
  "theta_neg_8_6_max_abs_err_deg": 5.470362663269043,
  "theta_neg_8_6_bias_deg": -0.3431841731071472,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7906294465065002,
  "theta_neg_4_2_rmse_deg": 1.1022861003875732,
  "theta_neg_4_2_p95_abs_err_deg": 2.310696840286255,
  "theta_neg_4_2_max_abs_err_deg": 5.418536186218262,
  "theta_neg_4_2_bias_deg": -0.5920109748840332,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6617982983589172,
  "theta_neg_2_0p5_rmse_deg": 0.8739684820175171,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6513539552688599,
  "theta_neg_2_0p5_max_abs_err_deg": 4.1733622550964355,
  "theta_neg_2_0p5_bias_deg": -0.5018153190612793,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.126745343208313,
  "theta_pos_0p5_2_rmse_deg": 1.4445194005966187,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3961451053619385,
  "theta_pos_0p5_2_max_abs_err_deg": 4.66306209564209,
  "theta_pos_0p5_2_bias_deg": 0.6830116510391235,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.34241689260499564,
  "loss_turn": 1.3338844201884186,
  "loss_theta": 0.0004082153729605457,
  "loss_main_bundle_base": 0.34241689260499564,
  "loss_turn_bundle_base": 0.10671075051789032,
  "loss_theta_bundle_base": 0.0002619187148314358,
  "loss_main_bundle": 0.34241689260499564,
  "loss_turn_bundle": 0.10671075051789032,
  "loss_theta_bundle": 0.0002619187148314358,
  "loss_theta_flat": 0.00018864955868809198,
  "loss_theta_near_flat": 0.0015108133692052393,
  "loss_theta_error_excess": 0.00014414537613121326,
  "loss_theta_flat_excess": 0.00011076120313834541,
  "loss_theta_near_flat_excess": 0.0011202114840266225,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 7.555043876265e-05,
  "loss_theta_small_neg": 0.0003686420895324337,
  "loss_theta_small_neg_excess": 0.00010029139965697014,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.29832499716859384,
  "loss_false_turn_straight": 0.2522253653435326,
  "loss_transition_focal_raw": 1.0307960534289338,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.70322412467525,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
