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
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9625 |
| acc_turn | 0.5033 |
| acc_turn_pure | 0.5227 |
| acc_turn_transition | 0.4188 |
| main_confidence_mean | 0.9845 |
| main_low_conf_0p60_ratio | 0.0097 |
| main_low_conf_0p70_ratio | 0.0158 |
| turn_confidence_mean | 0.6947 |
| turn_low_conf_0p60_ratio | 0.3762 |
| turn_low_conf_0p70_ratio | 0.5602 |
| turn_right_recall | 0.5720 |
| turn_straight_recall | 0.4397 |
| turn_left_recall | 0.5816 |
| theta_mae_deg | 0.6505 |
| theta_abs_le_10_p95_abs_err_deg | 1.7497 |
| theta_neg_10_8_p95_abs_err_deg | 1.0768 |
| theta_pos_8_10_p95_abs_err_deg | 3.4752 |
| theta_abs_le_8_p95_abs_err_deg | 1.7249 |
| theta_neg_8_6_p95_abs_err_deg | 1.5267 |
| theta_pos_6_8_p95_abs_err_deg | 1.3930 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.3182 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8982 |
| theta_flat_abs_p95_deg | 2.9356 |
| theta_flat_bias_deg | -0.4136 |
| theta_near_flat_abs_p95_deg | 1.8237 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3513 |
| theta_flat_turn_abs_p95_deg | 1.7970 |
| flat_recall | 0.9392 |
| stall_recall | 0.6875 |
| slope_recall | 0.9785 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.8053 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    710,
    0,
    46
  ],
  [
    10,
    66,
    20
  ],
  [
    49,
    10,
    2691
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    457,
    188,
    154
  ],
  [
    489,
    850,
    594
  ],
  [
    207,
    157,
    506
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.305795 |
| test_loss_turn_bundle_base | 0.228173 |
| test_loss_theta_bundle_base | 0.000179 |
| test_loss_transition_focal_raw | 0.785618 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.172349 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 43
- train_seconds: 246.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 35 | 0.4857 | 0.5292 |
| [0.60,0.70) | 22 | 0.4545 | 0.6438 |
| [0.70,0.80) | 33 | 0.3939 | 0.7528 |
| [0.80,0.90) | 73 | 0.3014 | 0.8557 |
| [0.90,1.00) | 3439 | 0.0212 | 0.9963 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1355 | 0.6244 | 0.5057 |
| [0.60,0.70) | 663 | 0.5626 | 0.6476 |
| [0.70,0.80) | 439 | 0.4533 | 0.7473 |
| [0.80,0.90) | 406 | 0.3941 | 0.8522 |
| [0.90,1.00) | 739 | 0.2855 | 0.9655 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4188

## 验证集最佳点

```json
{
  "loss_total": 0.4308173160349726,
  "acc_main": 0.9510148849797023,
  "acc_turn": 0.5818673883626523,
  "acc_turn_pure": 0.5978367748279253,
  "acc_turn_transition": 0.5062111801242236,
  "false_turn_straight": 0.5358627858627859,
  "flat_recall": 0.9634703196347032,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9552736982643525,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9634703196347032,
    0.4523809523809524,
    0.9552736982643525
  ],
  "turn_right_recall": 0.6943127962085308,
  "turn_straight_recall": 0.46413721413721415,
  "turn_left_recall": 0.7238403451995685,
  "recall_turn": [
    0.6943127962085308,
    0.46413721413721415,
    0.7238403451995685
  ],
  "cm_turn": [
    [
      586,
      186,
      72
    ],
    [
      519,
      893,
      512
    ],
    [
      129,
      127,
      671
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      633,
      0,
      24
    ],
    [
      0,
      19,
      23
    ],
    [
      128,
      6,
      2862
    ]
  ],
  "main_confidence_mean": 0.9646314391679442,
  "main_confidence_error_mean": 0.738927882509217,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.05764546684709066,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.45454545454545453,
      "mean_confidence": 0.5096192839961069
    },
    {
      "bin": "[0.60,0.70)",
      "n": 26,
      "error_rate": 0.23076923076923078,
      "mean_confidence": 0.6538478824006522
    },
    {
      "bin": "[0.70,0.80)",
      "n": 43,
      "error_rate": 0.16279069767441862,
      "mean_confidence": 0.7607647199704912
    },
    {
      "bin": "[0.80,0.90)",
      "n": 48,
      "error_rate": 0.0625,
      "mean_confidence": 0.8526586614504126
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3391,
      "error_rate": 0.023591860808021232,
      "mean_confidence": 0.9962765608869109
    }
  ],
  "turn_confidence_mean": 0.7194760362451157,
  "turn_confidence_error_mean": 0.6592483200923492,
  "turn_low_conf_0p60_ratio": 0.32205683355886333,
  "turn_low_conf_0p70_ratio": 0.47280108254397835,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1190,
      "error_rate": 0.5647058823529412,
      "mean_confidence": 0.5002740979622847
    },
    {
      "bin": "[0.60,0.70)",
      "n": 557,
      "error_rate": 0.4362657091561939,
      "mean_confidence": 0.6503744083629518
    },
    {
      "bin": "[0.70,0.80)",
      "n": 580,
      "error_rate": 0.4810344827586207,
      "mean_confidence": 0.7493100699509906
    },
    {
      "bin": "[0.80,0.90)",
      "n": 486,
      "error_rate": 0.33539094650205764,
      "mean_confidence": 0.8491225476625166
    },
    {
      "bin": "[0.90,1.00)",
      "n": 882,
      "error_rate": 0.21315192743764172,
      "mean_confidence": 0.9678070670712722
    }
  ],
  "theta_mae_rad": 0.01342175342142582,
  "theta_mae_deg": 0.7690097689628601,
  "uphill_recall": 0.7849056603773585,
  "downhill_recall": 0.7953281423804227,
  "slope_sign_acc": 0.9720777443197371,
  "theta_flat_mae_deg": 1.0954285860061646,
  "theta_flat_abs_p95_deg": 4.141896724700928,
  "theta_flat_abs_max_deg": 7.041942119598389,
  "theta_flat_bias_deg": 0.21641090512275696,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5399835109710693,
  "theta_near_flat_abs_p95_deg": 4.141907215118408,
  "theta_near_flat_abs_max_deg": 7.041942119598389,
  "theta_near_flat_bias_deg": 0.6936773061752319,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2673801183700562,
  "theta_flat_turn_abs_p95_deg": 4.141896724700928,
  "theta_flat_turn_abs_max_deg": 7.041942119598389,
  "theta_flat_turn_bias_deg": 0.09139569103717804,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7690097689628601,
  "theta_slope_control_abs_p95_deg": 9.420309066772461,
  "theta_slope_control_abs_max_deg": 11.681418418884277,
  "theta_slope_control_bias_deg": -0.08596830815076828,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7690098285675049,
  "theta_all_rmse_deg": 1.1608253717422485,
  "theta_all_p95_abs_err_deg": 2.641896963119507,
  "theta_all_max_abs_err_deg": 7.541942119598389,
  "theta_all_bias_deg": -0.08596830815076828,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6974287033081055,
  "theta_active_abs_ge_2_rmse_deg": 1.0097991228103638,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9308727979660034,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.050153732299805,
  "theta_active_abs_ge_2_bias_deg": -0.15227775275707245,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8039730191230774,
  "theta_abs_le_8_rmse_deg": 1.2035537958145142,
  "theta_abs_le_8_p95_abs_err_deg": 2.641896963119507,
  "theta_abs_le_8_max_abs_err_deg": 7.541942119598389,
  "theta_abs_le_8_bias_deg": -0.0634002685546875,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7690098285675049,
  "theta_abs_le_10_rmse_deg": 1.1608253717422485,
  "theta_abs_le_10_p95_abs_err_deg": 2.641896963119507,
  "theta_abs_le_10_max_abs_err_deg": 7.541942119598389,
  "theta_abs_le_10_bias_deg": -0.08596830815076828,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6056551933288574,
  "theta_pos_8_10_rmse_deg": 0.736683189868927,
  "theta_pos_8_10_p95_abs_err_deg": 1.1582114696502686,
  "theta_pos_8_10_max_abs_err_deg": 3.936826467514038,
  "theta_pos_8_10_bias_deg": -0.3197370171546936,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6376489400863647,
  "theta_neg_10_8_rmse_deg": 1.14302396774292,
  "theta_neg_10_8_p95_abs_err_deg": 2.106381416320801,
  "theta_neg_10_8_max_abs_err_deg": 7.050153732299805,
  "theta_neg_10_8_bias_deg": -0.04021337628364563,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.578494131565094,
  "theta_pos_6_8_rmse_deg": 0.8464175462722778,
  "theta_pos_6_8_p95_abs_err_deg": 1.6688495874404907,
  "theta_pos_6_8_max_abs_err_deg": 3.9796760082244873,
  "theta_pos_6_8_bias_deg": -0.09824619442224503,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.670159637928009,
  "theta_neg_8_6_rmse_deg": 1.0166513919830322,
  "theta_neg_8_6_p95_abs_err_deg": 1.8093023300170898,
  "theta_neg_8_6_max_abs_err_deg": 6.576350688934326,
  "theta_neg_8_6_bias_deg": -0.06492254137992859,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7389519810676575,
  "theta_neg_4_2_rmse_deg": 1.0714365243911743,
  "theta_neg_4_2_p95_abs_err_deg": 2.0596773624420166,
  "theta_neg_4_2_max_abs_err_deg": 5.352911949157715,
  "theta_neg_4_2_bias_deg": -0.32059094309806824,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.48125478625297546,
  "theta_neg_2_0p5_rmse_deg": 0.658560574054718,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3003604412078857,
  "theta_neg_2_0p5_max_abs_err_deg": 2.7611846923828125,
  "theta_neg_2_0p5_bias_deg": -0.2301873415708542,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2053848505020142,
  "theta_pos_0p5_2_rmse_deg": 1.52459716796875,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.641896963119507,
  "theta_pos_0p5_2_max_abs_err_deg": 3.6202681064605713,
  "theta_pos_0p5_2_bias_deg": 0.13812227547168732,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.23821555668833452,
  "loss_turn": 0.961635050641345,
  "loss_theta": 0.0004104347024550876,
  "loss_main_bundle_base": 0.23821555668833452,
  "loss_turn_bundle_base": 0.19232701393441676,
  "loss_theta_bundle_base": 0.0002747454317236201,
  "loss_main_bundle": 0.23821555668833452,
  "loss_turn_bundle": 0.19232701393441676,
  "loss_theta_bundle": 0.0002747454317236201,
  "loss_theta_flat": 0.00027170747898818976,
  "loss_theta_near_flat": 0.0014604053284572147,
  "loss_theta_error_excess": 0.00014700105043045586,
  "loss_theta_flat_excess": 0.00016842466667022082,
  "loss_theta_near_flat_excess": 0.0010656377305346006,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.051392934598906e-05,
  "loss_theta_small_neg": 0.0003495363443295934,
  "loss_theta_small_neg_excess": 0.00010161359882025055,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4515672447071669,
  "loss_false_turn_straight": 0.35680295341069707,
  "loss_transition_focal_raw": 0.6371630620891896,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.585437839521154,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
