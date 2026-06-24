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
  "lambda_theta_flat": 0.14,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.04,
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
  "select_theta_flat_peak_weight": 1.2,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9645 |
| acc_turn | 0.5522 |
| acc_turn_pure | 0.5705 |
| acc_turn_transition | 0.4724 |
| main_confidence_mean | 0.9845 |
| main_low_conf_0p60_ratio | 0.0119 |
| main_low_conf_0p70_ratio | 0.0203 |
| turn_confidence_mean | 0.7607 |
| turn_low_conf_0p60_ratio | 0.2579 |
| turn_low_conf_0p70_ratio | 0.3923 |
| turn_right_recall | 0.5807 |
| turn_straight_recall | 0.5168 |
| turn_left_recall | 0.6046 |
| theta_mae_deg | 0.7589 |
| theta_abs_le_10_p95_abs_err_deg | 1.8919 |
| theta_neg_10_8_p95_abs_err_deg | 1.8132 |
| theta_pos_8_10_p95_abs_err_deg | 3.8123 |
| theta_abs_le_8_p95_abs_err_deg | 1.7061 |
| theta_neg_8_6_p95_abs_err_deg | 1.6623 |
| theta_pos_6_8_p95_abs_err_deg | 1.6418 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5812 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7430 |
| theta_flat_abs_p95_deg | 2.3838 |
| theta_flat_bias_deg | 0.1349 |
| theta_near_flat_abs_p95_deg | 1.6154 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2522 |
| theta_flat_turn_abs_p95_deg | 1.4343 |
| flat_recall | 0.9630 |
| stall_recall | 0.6354 |
| slope_recall | 0.9764 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7517 |
| downhill_recall | 0.7957 |

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
    61,
    25
  ],
  [
    56,
    9,
    2685
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    464,
    193,
    142
  ],
  [
    370,
    999,
    564
  ],
  [
    161,
    183,
    526
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.350652 |
| test_loss_turn_bundle_base | 0.247510 |
| test_loss_theta_bundle_base | 0.000201 |
| test_loss_transition_focal_raw | 0.909971 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.830694 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 52
- train_seconds: 268.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 43 | 0.3953 | 0.5424 |
| [0.60,0.70) | 30 | 0.4667 | 0.6499 |
| [0.70,0.80) | 29 | 0.2069 | 0.7533 |
| [0.80,0.90) | 62 | 0.2258 | 0.8532 |
| [0.90,1.00) | 3438 | 0.0224 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 929 | 0.6459 | 0.5081 |
| [0.60,0.70) | 484 | 0.5124 | 0.6508 |
| [0.70,0.80) | 469 | 0.4968 | 0.7491 |
| [0.80,0.90) | 518 | 0.4093 | 0.8482 |
| [0.90,1.00) | 1202 | 0.2662 | 0.9672 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4724
- theta_mae_deg <= 0.7000 未满足，实际 0.7589

## 验证集最佳点

```json
{
  "loss_total": 0.43988059365539656,
  "acc_main": 0.9491204330175913,
  "acc_turn": 0.6162381596752368,
  "acc_turn_pure": 0.6286463454605048,
  "acc_turn_transition": 0.5574534161490683,
  "false_turn_straight": 0.4693347193347193,
  "flat_recall": 0.9817351598173516,
  "stall_recall": 0.5,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9817351598173516,
    0.5,
    0.94826435246996
  ],
  "turn_right_recall": 0.6409952606635071,
  "turn_straight_recall": 0.5306652806652806,
  "turn_left_recall": 0.7713052858683926,
  "recall_turn": [
    0.6409952606635071,
    0.5306652806652806,
    0.7713052858683926
  ],
  "cm_turn": [
    [
      541,
      193,
      110
    ],
    [
      394,
      1021,
      509
    ],
    [
      59,
      153,
      715
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      645,
      0,
      12
    ],
    [
      0,
      21,
      21
    ],
    [
      147,
      8,
      2841
    ]
  ],
  "main_confidence_mean": 0.9655425539009572,
  "main_confidence_error_mean": 0.7324867857494811,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.4497354497354497,
      "mean_confidence": 0.5092201099096102
    },
    {
      "bin": "[0.60,0.70)",
      "n": 23,
      "error_rate": 0.43478260869565216,
      "mean_confidence": 0.6624131882764118
    },
    {
      "bin": "[0.70,0.80)",
      "n": 40,
      "error_rate": 0.2,
      "mean_confidence": 0.7572198846342844
    },
    {
      "bin": "[0.80,0.90)",
      "n": 51,
      "error_rate": 0.21568627450980393,
      "mean_confidence": 0.854318910006576
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3392,
      "error_rate": 0.021816037735849055,
      "mean_confidence": 0.9971528811217737
    }
  ],
  "turn_confidence_mean": 0.7806594888163146,
  "turn_confidence_error_mean": 0.7027994088857553,
  "turn_low_conf_0p60_ratio": 0.21596752368064953,
  "turn_low_conf_0p70_ratio": 0.3320703653585927,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 798,
      "error_rate": 0.6052631578947368,
      "mean_confidence": 0.49493327361220735
    },
    {
      "bin": "[0.60,0.70)",
      "n": 429,
      "error_rate": 0.5174825174825175,
      "mean_confidence": 0.6524641221195732
    },
    {
      "bin": "[0.70,0.80)",
      "n": 526,
      "error_rate": 0.41634980988593157,
      "mean_confidence": 0.7504845899431414
    },
    {
      "bin": "[0.80,0.90)",
      "n": 575,
      "error_rate": 0.3373913043478261,
      "mean_confidence": 0.8513580744584217
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1367,
      "error_rate": 0.2194586686174104,
      "mean_confidence": 0.9695590075499335
    }
  ],
  "theta_mae_rad": 0.015028235502541065,
  "theta_mae_deg": 0.8610544204711914,
  "uphill_recall": 0.7660377358490567,
  "downhill_recall": 0.796440489432703,
  "slope_sign_acc": 0.9679715302491103,
  "theta_flat_mae_deg": 0.964816689491272,
  "theta_flat_abs_p95_deg": 3.878542423248291,
  "theta_flat_abs_max_deg": 8.033893585205078,
  "theta_flat_bias_deg": 0.6194802522659302,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2951096296310425,
  "theta_near_flat_abs_p95_deg": 3.878542423248291,
  "theta_near_flat_abs_max_deg": 8.033893585205078,
  "theta_near_flat_bias_deg": 0.8875817060470581,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0523444414138794,
  "theta_flat_turn_abs_p95_deg": 3.878542423248291,
  "theta_flat_turn_abs_max_deg": 8.033893585205078,
  "theta_flat_turn_bias_deg": 0.4620268940925598,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8610544204711914,
  "theta_slope_control_abs_p95_deg": 8.759468078613281,
  "theta_slope_control_abs_max_deg": 11.397396087646484,
  "theta_slope_control_bias_deg": 0.07007455825805664,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8610543608665466,
  "theta_all_rmse_deg": 1.2051441669464111,
  "theta_all_p95_abs_err_deg": 2.378542423248291,
  "theta_all_max_abs_err_deg": 8.533893585205078,
  "theta_all_bias_deg": 0.07007455825805664,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8383001089096069,
  "theta_active_abs_ge_2_rmse_deg": 1.1138930320739746,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0763802528381348,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.574268341064453,
  "theta_active_abs_ge_2_bias_deg": -0.05040591582655907,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8423411846160889,
  "theta_abs_le_8_rmse_deg": 1.2076679468154907,
  "theta_abs_le_8_p95_abs_err_deg": 2.4195315837860107,
  "theta_abs_le_8_max_abs_err_deg": 8.533893585205078,
  "theta_abs_le_8_bias_deg": 0.05444084852933884,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8610543608665466,
  "theta_abs_le_10_rmse_deg": 1.2051441669464111,
  "theta_abs_le_10_p95_abs_err_deg": 2.378542423248291,
  "theta_abs_le_10_max_abs_err_deg": 8.533893585205078,
  "theta_abs_le_10_bias_deg": 0.07007455825805664,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8690327405929565,
  "theta_pos_8_10_rmse_deg": 1.019205927848816,
  "theta_pos_8_10_p95_abs_err_deg": 1.6623417139053345,
  "theta_pos_8_10_max_abs_err_deg": 4.755879878997803,
  "theta_pos_8_10_bias_deg": -0.6050267219543457,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.0121885538101196,
  "theta_neg_10_8_rmse_deg": 1.3495532274246216,
  "theta_neg_10_8_p95_abs_err_deg": 2.20574688911438,
  "theta_neg_10_8_max_abs_err_deg": 6.574268341064453,
  "theta_neg_10_8_bias_deg": 0.8898932933807373,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8686339855194092,
  "theta_pos_6_8_rmse_deg": 1.0395605564117432,
  "theta_pos_6_8_p95_abs_err_deg": 1.9126017093658447,
  "theta_pos_6_8_max_abs_err_deg": 3.5978829860687256,
  "theta_pos_6_8_bias_deg": -0.4498707950115204,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7080307006835938,
  "theta_neg_8_6_rmse_deg": 0.985360324382782,
  "theta_neg_8_6_p95_abs_err_deg": 1.9497036933898926,
  "theta_neg_8_6_max_abs_err_deg": 5.341565132141113,
  "theta_neg_8_6_bias_deg": 0.34512096643447876,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7623429894447327,
  "theta_neg_4_2_rmse_deg": 1.0764175653457642,
  "theta_neg_4_2_p95_abs_err_deg": 2.240708351135254,
  "theta_neg_4_2_max_abs_err_deg": 6.3134260177612305,
  "theta_neg_4_2_bias_deg": -0.14785818755626678,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5142495632171631,
  "theta_neg_2_0p5_rmse_deg": 0.6884680986404419,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2843177318572998,
  "theta_neg_2_0p5_max_abs_err_deg": 3.119450092315674,
  "theta_neg_2_0p5_bias_deg": 0.34813910722732544,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9706465601921082,
  "theta_pos_0p5_2_rmse_deg": 1.3647314310073853,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.378542423248291,
  "theta_pos_0p5_2_max_abs_err_deg": 4.9086384773254395,
  "theta_pos_0p5_2_bias_deg": 0.5727553367614746,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2158958152359974,
  "loss_turn": 1.1184314782629154,
  "loss_theta": 0.0004424051177330033,
  "loss_main_bundle_base": 0.2158958152359974,
  "loss_turn_bundle_base": 0.22368630028464637,
  "loss_theta_bundle_base": 0.00029848301448450956,
  "loss_main_bundle": 0.2158958152359974,
  "loss_turn_bundle": 0.22368630028464637,
  "loss_theta_bundle": 0.00029848301448450956,
  "loss_theta_flat": 0.0002264877677035719,
  "loss_theta_near_flat": 0.0012444718847686427,
  "loss_theta_error_excess": 0.00014633660185253512,
  "loss_theta_flat_excess": 0.00012454173455068247,
  "loss_theta_near_flat_excess": 0.0009173002212493603,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010125943589060792,
  "loss_theta_small_neg": 0.0003530383289789123,
  "loss_theta_small_neg_excess": 9.765547652730745e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.40771430306570133,
  "loss_false_turn_straight": 0.3239735113267808,
  "loss_transition_focal_raw": 0.8028972018878096,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.2559926653747313,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
