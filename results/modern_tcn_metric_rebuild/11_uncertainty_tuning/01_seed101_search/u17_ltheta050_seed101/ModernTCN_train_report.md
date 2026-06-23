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
  "lambda_theta": 0.5,
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
| acc_main | 0.9697 |
| acc_turn | 0.5983 |
| acc_turn_pure | 0.6087 |
| acc_turn_transition | 0.5529 |
| main_confidence_mean | 0.9908 |
| main_low_conf_0p60_ratio | 0.0047 |
| main_low_conf_0p70_ratio | 0.0114 |
| turn_confidence_mean | 0.8450 |
| turn_low_conf_0p60_ratio | 0.1352 |
| turn_low_conf_0p70_ratio | 0.2307 |
| turn_right_recall | 0.6233 |
| turn_straight_recall | 0.5830 |
| turn_left_recall | 0.6092 |
| theta_mae_deg | 0.5020 |
| theta_abs_le_10_p95_abs_err_deg | 1.4044 |
| theta_neg_10_8_p95_abs_err_deg | 1.4091 |
| theta_pos_8_10_p95_abs_err_deg | 2.2575 |
| theta_abs_le_8_p95_abs_err_deg | 1.3269 |
| theta_neg_8_6_p95_abs_err_deg | 1.1771 |
| theta_pos_6_8_p95_abs_err_deg | 1.7596 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2286 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3453 |
| theta_flat_abs_p95_deg | 2.5032 |
| theta_flat_bias_deg | 0.0935 |
| theta_near_flat_abs_p95_deg | 1.6873 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3120 |
| theta_flat_turn_abs_p95_deg | 1.3242 |
| flat_recall | 0.9524 |
| stall_recall | 0.6979 |
| slope_recall | 0.9840 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7626 |
| downhill_recall | 0.8014 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    720,
    0,
    36
  ],
  [
    10,
    67,
    19
  ],
  [
    32,
    12,
    2706
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    498,
    198,
    103
  ],
  [
    387,
    1127,
    419
  ],
  [
    150,
    190,
    530
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.349335 |
| test_loss_turn_bundle_base | 0.363757 |
| test_loss_theta_bundle_base | 0.000111 |
| test_loss_transition_focal_raw | 1.704758 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.576507 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 98
- train_seconds: 431.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 17 | 0.4118 | 0.5465 |
| [0.60,0.70) | 24 | 0.2083 | 0.6438 |
| [0.70,0.80) | 23 | 0.2174 | 0.7581 |
| [0.80,0.90) | 35 | 0.2000 | 0.8534 |
| [0.90,1.00) | 3503 | 0.0243 | 0.9983 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 487 | 0.5524 | 0.5126 |
| [0.60,0.70) | 344 | 0.4942 | 0.6503 |
| [0.70,0.80) | 379 | 0.4987 | 0.7545 |
| [0.80,0.90) | 457 | 0.4945 | 0.8526 |
| [0.90,1.00) | 1935 | 0.3065 | 0.9793 |


## 验证集最佳点

```json
{
  "loss_total": 0.7178329483259354,
  "acc_main": 0.9437077131258458,
  "acc_turn": 0.642489851150203,
  "acc_turn_pure": 0.6538839724680433,
  "acc_turn_transition": 0.5885093167701864,
  "false_turn_straight": 0.4028066528066528,
  "flat_recall": 0.958904109589041,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.958904109589041,
    0.38095238095238093,
    0.94826435246996
  ],
  "turn_right_recall": 0.6789099526066351,
  "turn_straight_recall": 0.5971933471933472,
  "turn_left_recall": 0.703344120819849,
  "recall_turn": [
    0.6789099526066351,
    0.5971933471933472,
    0.703344120819849
  ],
  "cm_turn": [
    [
      573,
      218,
      53
    ],
    [
      416,
      1149,
      359
    ],
    [
      100,
      175,
      652
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      630,
      0,
      27
    ],
    [
      0,
      16,
      26
    ],
    [
      135,
      20,
      2841
    ]
  ],
  "main_confidence_mean": 0.9694688167055224,
  "main_confidence_error_mean": 0.769898232535341,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.05466847090663058,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.46524064171123,
      "mean_confidence": 0.5267330318306487
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.26666666666666666,
      "mean_confidence": 0.6530965628168761
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.27586206896551724,
      "mean_confidence": 0.7574623879124418
    },
    {
      "bin": "[0.80,0.90)",
      "n": 37,
      "error_rate": 0.3783783783783784,
      "mean_confidence": 0.8516895861714993
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3427,
      "error_rate": 0.027721038809454333,
      "mean_confidence": 0.9980778606345243
    }
  ],
  "turn_confidence_mean": 0.8642733483297331,
  "turn_confidence_error_mean": 0.7922627594841345,
  "turn_low_conf_0p60_ratio": 0.1334235453315291,
  "turn_low_conf_0p70_ratio": 0.2040595399188092,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 493,
      "error_rate": 0.6064908722109533,
      "mean_confidence": 0.4866864429871075
    },
    {
      "bin": "[0.60,0.70)",
      "n": 261,
      "error_rate": 0.5172413793103449,
      "mean_confidence": 0.6522165307553791
    },
    {
      "bin": "[0.70,0.80)",
      "n": 274,
      "error_rate": 0.5328467153284672,
      "mean_confidence": 0.7534863229437524
    },
    {
      "bin": "[0.80,0.90)",
      "n": 348,
      "error_rate": 0.3793103448275862,
      "mean_confidence": 0.853927582290715
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2319,
      "error_rate": 0.2626131953428202,
      "mean_confidence": 0.9830543510283781
    }
  ],
  "theta_mae_rad": 0.012009051628410816,
  "theta_mae_deg": 0.6880679130554199,
  "uphill_recall": 0.7714285714285715,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9704352586914865,
  "theta_flat_mae_deg": 1.014389157295227,
  "theta_flat_abs_p95_deg": 4.253177165985107,
  "theta_flat_abs_max_deg": 7.026175498962402,
  "theta_flat_bias_deg": 0.5258473753929138,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3998252153396606,
  "theta_near_flat_abs_p95_deg": 4.257793426513672,
  "theta_near_flat_abs_max_deg": 7.026175498962402,
  "theta_near_flat_bias_deg": 0.940931499004364,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9956917762756348,
  "theta_flat_turn_abs_p95_deg": 4.253177165985107,
  "theta_flat_turn_abs_max_deg": 7.026175498962402,
  "theta_flat_turn_bias_deg": 0.2579136788845062,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.6880679130554199,
  "theta_slope_control_abs_p95_deg": 9.163618087768555,
  "theta_slope_control_abs_max_deg": 12.197246551513672,
  "theta_slope_control_bias_deg": 0.1275157928466797,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.6880679726600647,
  "theta_all_rmse_deg": 1.13229501247406,
  "theta_all_p95_abs_err_deg": 2.7080206871032715,
  "theta_all_max_abs_err_deg": 7.5286078453063965,
  "theta_all_bias_deg": 0.1275157928466797,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6165081858634949,
  "theta_active_abs_ge_2_rmse_deg": 0.9977492094039917,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.895751953125,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.5286078453063965,
  "theta_active_abs_ge_2_bias_deg": 0.04016472399234772,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7250626683235168,
  "theta_abs_le_8_rmse_deg": 1.1617178916931152,
  "theta_abs_le_8_p95_abs_err_deg": 2.7531774044036865,
  "theta_abs_le_8_max_abs_err_deg": 6.526175498962402,
  "theta_abs_le_8_bias_deg": 0.1459342986345291,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.6880679726600647,
  "theta_abs_le_10_rmse_deg": 1.13229501247406,
  "theta_abs_le_10_p95_abs_err_deg": 2.7080206871032715,
  "theta_abs_le_10_max_abs_err_deg": 7.5286078453063965,
  "theta_abs_le_10_bias_deg": 0.1275157928466797,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4749367833137512,
  "theta_pos_8_10_rmse_deg": 0.721450686454773,
  "theta_pos_8_10_p95_abs_err_deg": 1.3635401725769043,
  "theta_pos_8_10_max_abs_err_deg": 5.102728843688965,
  "theta_pos_8_10_bias_deg": -0.2118867039680481,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5900554656982422,
  "theta_neg_10_8_rmse_deg": 1.2175644636154175,
  "theta_neg_10_8_p95_abs_err_deg": 2.1508214473724365,
  "theta_neg_10_8_max_abs_err_deg": 7.5286078453063965,
  "theta_neg_10_8_bias_deg": 0.3160439729690552,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.3975638151168823,
  "theta_pos_6_8_rmse_deg": 0.6099149584770203,
  "theta_pos_6_8_p95_abs_err_deg": 1.3481662273406982,
  "theta_pos_6_8_max_abs_err_deg": 2.7346811294555664,
  "theta_pos_6_8_bias_deg": 0.013299951329827309,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6706859469413757,
  "theta_neg_8_6_rmse_deg": 1.0235778093338013,
  "theta_neg_8_6_p95_abs_err_deg": 1.778244137763977,
  "theta_neg_8_6_max_abs_err_deg": 6.272432804107666,
  "theta_neg_8_6_bias_deg": 0.05706115439534187,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6607098579406738,
  "theta_neg_4_2_rmse_deg": 1.0314205884933472,
  "theta_neg_4_2_p95_abs_err_deg": 1.9950554370880127,
  "theta_neg_4_2_max_abs_err_deg": 6.236837387084961,
  "theta_neg_4_2_bias_deg": -0.16651441156864166,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5211666226387024,
  "theta_neg_2_0p5_rmse_deg": 0.7396623492240906,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3920444250106812,
  "theta_neg_2_0p5_max_abs_err_deg": 4.204453945159912,
  "theta_neg_2_0p5_bias_deg": -0.10693200677633286,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0813264846801758,
  "theta_pos_0p5_2_rmse_deg": 1.5087010860443115,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.7531774044036865,
  "theta_pos_0p5_2_max_abs_err_deg": 4.386947154998779,
  "theta_pos_0p5_2_bias_deg": 0.7266812324523926,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3811976108725242,
  "loss_turn": 1.6819807709473233,
  "loss_theta": 0.0003905521655021707,
  "loss_main_bundle_base": 0.3811976108725242,
  "loss_turn_bundle_base": 0.3363961589110559,
  "loss_theta_bundle_base": 0.00023918379778237775,
  "loss_main_bundle": 0.3811976108725242,
  "loss_turn_bundle": 0.3363961589110559,
  "loss_theta_bundle": 0.00023918379778237775,
  "loss_theta_flat": 0.000209800422426971,
  "loss_theta_near_flat": 0.0013237326838207181,
  "loss_theta_error_excess": 0.0001569654453225706,
  "loss_theta_flat_excess": 0.000131434493639145,
  "loss_theta_near_flat_excess": 0.000977096119700239,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010883396567653295,
  "loss_theta_small_neg": 0.00031966592401961756,
  "loss_theta_small_neg_excess": 0.00011129628023372444,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3661345432107923,
  "loss_false_turn_straight": 0.30782020360594353,
  "loss_transition_focal_raw": 1.52271418374672,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.560355002899794,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
