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
  "main_neg_slope_weight": 1.6,
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
| acc_main | 0.9620 |
| acc_turn | 0.5922 |
| acc_turn_pure | 0.6076 |
| acc_turn_transition | 0.5246 |
| main_confidence_mean | 0.9895 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0142 |
| turn_confidence_mean | 0.8420 |
| turn_low_conf_0p60_ratio | 0.1435 |
| turn_low_conf_0p70_ratio | 0.2368 |
| turn_right_recall | 0.6183 |
| turn_straight_recall | 0.5861 |
| turn_left_recall | 0.5816 |
| theta_mae_deg | 0.5803 |
| theta_abs_le_10_p95_abs_err_deg | 1.6637 |
| theta_neg_10_8_p95_abs_err_deg | 1.1410 |
| theta_pos_8_10_p95_abs_err_deg | 2.6399 |
| theta_abs_le_8_p95_abs_err_deg | 1.5042 |
| theta_neg_8_6_p95_abs_err_deg | 1.8768 |
| theta_pos_6_8_p95_abs_err_deg | 1.4977 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3066 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7294 |
| theta_flat_abs_p95_deg | 2.4998 |
| theta_flat_bias_deg | 0.0050 |
| theta_near_flat_abs_p95_deg | 1.6267 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0181 |
| theta_flat_turn_abs_p95_deg | 1.4065 |
| flat_recall | 0.9577 |
| stall_recall | 0.6979 |
| slope_recall | 0.9724 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7466 |
| downhill_recall | 0.7963 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    724,
    1,
    31
  ],
  [
    10,
    67,
    19
  ],
  [
    65,
    11,
    2674
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    494,
    191,
    114
  ],
  [
    376,
    1133,
    424
  ],
  [
    149,
    215,
    506
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.443371 |
| test_loss_turn_bundle_base | 0.341968 |
| test_loss_theta_bundle_base | 0.000143 |
| test_loss_transition_focal_raw | 1.573539 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.357743 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 85
- train_seconds: 385.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.6923 | 0.5450 |
| [0.60,0.70) | 25 | 0.6400 | 0.6551 |
| [0.70,0.80) | 24 | 0.4167 | 0.7522 |
| [0.80,0.90) | 32 | 0.3438 | 0.8542 |
| [0.90,1.00) | 3495 | 0.0235 | 0.9981 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 517 | 0.5725 | 0.5158 |
| [0.60,0.70) | 336 | 0.5714 | 0.6514 |
| [0.70,0.80) | 344 | 0.5349 | 0.7521 |
| [0.80,0.90) | 494 | 0.4838 | 0.8526 |
| [0.90,1.00) | 1911 | 0.2920 | 0.9772 |


## 验证集最佳点

```json
{
  "loss_total": 0.7750013606151482,
  "acc_main": 0.9404600811907984,
  "acc_turn": 0.6154262516914749,
  "acc_turn_pure": 0.6293018682399213,
  "acc_turn_transition": 0.5496894409937888,
  "false_turn_straight": 0.4386694386694387,
  "flat_recall": 0.9482496194824962,
  "stall_recall": 0.2619047619047619,
  "slope_recall": 0.94826435246996,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9482496194824962,
    0.2619047619047619,
    0.94826435246996
  ],
  "turn_right_recall": 0.6315165876777251,
  "turn_straight_recall": 0.5613305613305614,
  "turn_left_recall": 0.7130528586839266,
  "recall_turn": [
    0.6315165876777251,
    0.5613305613305614,
    0.7130528586839266
  ],
  "cm_turn": [
    [
      533,
      208,
      103
    ],
    [
      329,
      1080,
      515
    ],
    [
      70,
      196,
      661
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      623,
      0,
      34
    ],
    [
      0,
      11,
      31
    ],
    [
      143,
      12,
      2841
    ]
  ],
  "main_confidence_mean": 0.9670856910382942,
  "main_confidence_error_mean": 0.7686734700126088,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.056833558863328824,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.45161290322580644,
      "mean_confidence": 0.5053303430251354
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.375,
      "mean_confidence": 0.651363185504377
    },
    {
      "bin": "[0.70,0.80)",
      "n": 39,
      "error_rate": 0.28205128205128205,
      "mean_confidence": 0.7561876113584379
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.36363636363636365,
      "mean_confidence": 0.8647205954959108
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3413,
      "error_rate": 0.030471725754468208,
      "mean_confidence": 0.9978700180595879
    }
  ],
  "turn_confidence_mean": 0.8638090989352861,
  "turn_confidence_error_mean": 0.7956908093884761,
  "turn_low_conf_0p60_ratio": 0.12449255751014884,
  "turn_low_conf_0p70_ratio": 0.19377537212449256,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 460,
      "error_rate": 0.6478260869565218,
      "mean_confidence": 0.49807527524316564
    },
    {
      "bin": "[0.60,0.70)",
      "n": 256,
      "error_rate": 0.5234375,
      "mean_confidence": 0.6489092590625678
    },
    {
      "bin": "[0.70,0.80)",
      "n": 305,
      "error_rate": 0.5377049180327869,
      "mean_confidence": 0.753657482141519
    },
    {
      "bin": "[0.80,0.90)",
      "n": 440,
      "error_rate": 0.509090909090909,
      "mean_confidence": 0.8507439161722509
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2234,
      "error_rate": 0.26902417188898836,
      "mean_confidence": 0.9813546859736146
    }
  ],
  "theta_mae_rad": 0.012541286647319794,
  "theta_mae_deg": 0.7185627818107605,
  "uphill_recall": 0.7703504043126684,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9720777443197371,
  "theta_flat_mae_deg": 0.9748748540878296,
  "theta_flat_abs_p95_deg": 3.7006945610046387,
  "theta_flat_abs_max_deg": 6.610567569732666,
  "theta_flat_bias_deg": 0.616718053817749,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.301844835281372,
  "theta_near_flat_abs_p95_deg": 3.7029049396514893,
  "theta_near_flat_abs_max_deg": 6.54886531829834,
  "theta_near_flat_bias_deg": 0.9706020355224609,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.8501202464103699,
  "theta_flat_turn_abs_p95_deg": 3.700679063796997,
  "theta_flat_turn_abs_max_deg": 4.240455150604248,
  "theta_flat_turn_bias_deg": 0.5469104647636414,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7185627818107605,
  "theta_slope_control_abs_p95_deg": 9.380193710327148,
  "theta_slope_control_abs_max_deg": 11.309613227844238,
  "theta_slope_control_bias_deg": 0.09733272343873978,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7185627222061157,
  "theta_all_rmse_deg": 1.1086430549621582,
  "theta_all_p95_abs_err_deg": 2.4343044757843018,
  "theta_all_max_abs_err_deg": 6.56143856048584,
  "theta_all_bias_deg": 0.09733273088932037,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6623554825782776,
  "theta_active_abs_ge_2_rmse_deg": 1.0138301849365234,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.083448648452759,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.56143856048584,
  "theta_active_abs_ge_2_bias_deg": -0.016564538702368736,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7478463649749756,
  "theta_abs_le_8_rmse_deg": 1.1340975761413574,
  "theta_abs_le_8_p95_abs_err_deg": 2.619500160217285,
  "theta_abs_le_8_max_abs_err_deg": 6.56143856048584,
  "theta_abs_le_8_bias_deg": 0.10653448849916458,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7185627222061157,
  "theta_abs_le_10_rmse_deg": 1.1086430549621582,
  "theta_abs_le_10_p95_abs_err_deg": 2.4343044757843018,
  "theta_abs_le_10_max_abs_err_deg": 6.56143856048584,
  "theta_abs_le_10_bias_deg": 0.09733273088932037,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5497583746910095,
  "theta_pos_8_10_rmse_deg": 0.8230348229408264,
  "theta_pos_8_10_p95_abs_err_deg": 1.8950066566467285,
  "theta_pos_8_10_max_abs_err_deg": 5.023818016052246,
  "theta_pos_8_10_bias_deg": -0.10987859219312668,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6410796642303467,
  "theta_neg_10_8_rmse_deg": 1.142150640487671,
  "theta_neg_10_8_p95_abs_err_deg": 2.1854400634765625,
  "theta_neg_10_8_max_abs_err_deg": 6.439720630645752,
  "theta_neg_10_8_bias_deg": 0.22981922328472137,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5975056886672974,
  "theta_pos_6_8_rmse_deg": 0.8685474991798401,
  "theta_pos_6_8_p95_abs_err_deg": 1.7227942943572998,
  "theta_pos_6_8_max_abs_err_deg": 4.10134220123291,
  "theta_pos_6_8_bias_deg": -0.02380472794175148,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8025500774383545,
  "theta_neg_8_6_rmse_deg": 1.142369270324707,
  "theta_neg_8_6_p95_abs_err_deg": 2.3120570182800293,
  "theta_neg_8_6_max_abs_err_deg": 6.065056324005127,
  "theta_neg_8_6_bias_deg": -0.031887758523225784,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6620403528213501,
  "theta_neg_4_2_rmse_deg": 0.9394243359565735,
  "theta_neg_4_2_p95_abs_err_deg": 1.9993535280227661,
  "theta_neg_4_2_max_abs_err_deg": 6.130209922790527,
  "theta_neg_4_2_bias_deg": -0.19404610991477966,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5127887725830078,
  "theta_neg_2_0p5_rmse_deg": 0.773798942565918,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3790879249572754,
  "theta_neg_2_0p5_max_abs_err_deg": 4.494668006896973,
  "theta_neg_2_0p5_bias_deg": 0.1965799182653427,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1417086124420166,
  "theta_pos_0p5_2_rmse_deg": 1.4332709312438965,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.208200216293335,
  "theta_pos_0p5_2_max_abs_err_deg": 4.838594913482666,
  "theta_pos_0p5_2_bias_deg": 0.709491491317749,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.4465700846079722,
  "loss_turn": 1.6409067878865098,
  "loss_theta": 0.00037434405016464575,
  "loss_main_bundle_base": 0.4465700846079722,
  "loss_turn_bundle_base": 0.3281813621198373,
  "loss_theta_bundle_base": 0.0002499325246835589,
  "loss_main_bundle": 0.4465700846079722,
  "loss_turn_bundle": 0.3281813621198373,
  "loss_theta_bundle": 0.0002499325246835589,
  "loss_theta_flat": 0.0002285282004842628,
  "loss_theta_near_flat": 0.0010223253082839398,
  "loss_theta_error_excess": 0.00013026127703812386,
  "loss_theta_flat_excess": 0.00012705721029934898,
  "loss_theta_near_flat_excess": 0.0007011841851222318,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001010684110484173,
  "loss_theta_small_neg": 0.0002643329923763286,
  "loss_theta_small_neg_excess": 6.719080655401887e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.40774879278930176,
  "loss_false_turn_straight": 0.3336290075185334,
  "loss_transition_focal_raw": 1.4784952527292687,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.2971648302710586,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
