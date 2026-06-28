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
| acc_main | 0.9584 |
| acc_turn | 0.5872 |
| acc_turn_pure | 0.6104 |
| acc_turn_transition | 0.4858 |
| main_confidence_mean | 0.9860 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0161 |
| turn_confidence_mean | 0.7811 |
| turn_low_conf_0p60_ratio | 0.2240 |
| turn_low_conf_0p70_ratio | 0.3501 |
| turn_right_recall | 0.5294 |
| turn_straight_recall | 0.6441 |
| turn_left_recall | 0.5138 |
| theta_mae_deg | 0.6323 |
| theta_abs_le_10_p95_abs_err_deg | 1.8677 |
| theta_neg_10_8_p95_abs_err_deg | 1.7053 |
| theta_pos_8_10_p95_abs_err_deg | 3.0913 |
| theta_abs_le_8_p95_abs_err_deg | 1.7658 |
| theta_neg_8_6_p95_abs_err_deg | 1.3600 |
| theta_pos_6_8_p95_abs_err_deg | 1.5477 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6981 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9738 |
| theta_flat_abs_p95_deg | 2.5472 |
| theta_flat_bias_deg | 0.0803 |
| theta_near_flat_abs_p95_deg | 1.7075 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1246 |
| theta_flat_turn_abs_p95_deg | 1.5760 |
| flat_recall | 0.9471 |
| stall_recall | 0.6354 |
| slope_recall | 0.9727 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.8008 |

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
    9,
    61,
    26
  ],
  [
    56,
    19,
    2675
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    423,
    267,
    109
  ],
  [
    363,
    1245,
    325
  ],
  [
    145,
    278,
    447
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.339254 |
| test_loss_turn_bundle_base | 0.100394 |
| test_loss_theta_bundle_base | 0.000166 |
| test_loss_transition_focal_raw | 1.157386 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.428588 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 65
- train_seconds: 978.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.5385 | 0.5486 |
| [0.60,0.70) | 32 | 0.4688 | 0.6536 |
| [0.70,0.80) | 41 | 0.2439 | 0.7464 |
| [0.80,0.90) | 58 | 0.5000 | 0.8671 |
| [0.90,1.00) | 3445 | 0.0238 | 0.9972 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 807 | 0.5799 | 0.5154 |
| [0.60,0.70) | 454 | 0.5198 | 0.6497 |
| [0.70,0.80) | 476 | 0.4769 | 0.7501 |
| [0.80,0.90) | 551 | 0.4374 | 0.8496 |
| [0.90,1.00) | 1314 | 0.2397 | 0.9721 |


## 验证集最佳点

```json
{
  "loss_total": 0.42233756991942617,
  "acc_main": 0.9426251691474966,
  "acc_turn": 0.6173207036535859,
  "acc_turn_pure": 0.6296296296296297,
  "acc_turn_transition": 0.5590062111801242,
  "false_turn_straight": 0.39501039501039503,
  "flat_recall": 0.958904109589041,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9469292389853138,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.958904109589041,
    0.38095238095238093,
    0.9469292389853138
  ],
  "turn_right_recall": 0.5924170616113744,
  "turn_straight_recall": 0.604989604989605,
  "turn_left_recall": 0.6655879180151025,
  "recall_turn": [
    0.5924170616113744,
    0.604989604989605,
    0.6655879180151025
  ],
  "cm_turn": [
    [
      500,
      234,
      110
    ],
    [
      331,
      1164,
      429
    ],
    [
      80,
      230,
      617
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
      140,
      19,
      2837
    ]
  ],
  "main_confidence_mean": 0.9669673225485318,
  "main_confidence_error_mean": 0.7506540737195032,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.061434370771312585,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.46774193548387094,
      "mean_confidence": 0.5341802052504152
    },
    {
      "bin": "[0.60,0.70)",
      "n": 41,
      "error_rate": 0.5365853658536586,
      "mean_confidence": 0.6539164346603206
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.1724137931034483,
      "mean_confidence": 0.7488188971922666
    },
    {
      "bin": "[0.80,0.90)",
      "n": 42,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.8589276206627604
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3397,
      "error_rate": 0.02531645569620253,
      "mean_confidence": 0.997640699656392
    }
  ],
  "turn_confidence_mean": 0.8008852546306384,
  "turn_confidence_error_mean": 0.723672001305558,
  "turn_low_conf_0p60_ratio": 0.20893098782138025,
  "turn_low_conf_0p70_ratio": 0.32205683355886333,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 772,
      "error_rate": 0.6347150259067358,
      "mean_confidence": 0.5151157157813383
    },
    {
      "bin": "[0.60,0.70)",
      "n": 418,
      "error_rate": 0.45933014354066987,
      "mean_confidence": 0.6490952906468143
    },
    {
      "bin": "[0.70,0.80)",
      "n": 404,
      "error_rate": 0.4430693069306931,
      "mean_confidence": 0.7492637905234774
    },
    {
      "bin": "[0.80,0.90)",
      "n": 495,
      "error_rate": 0.38181818181818183,
      "mean_confidence": 0.8544334898788333
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1606,
      "error_rate": 0.2266500622665006,
      "mean_confidence": 0.9742420317093027
    }
  ],
  "theta_mae_rad": 0.013798310421407223,
  "theta_mae_deg": 0.790584921836853,
  "uphill_recall": 0.769811320754717,
  "downhill_recall": 0.7986651835372637,
  "slope_sign_acc": 0.9619490829455243,
  "theta_flat_mae_deg": 1.134450912475586,
  "theta_flat_abs_p95_deg": 4.165439605712891,
  "theta_flat_abs_max_deg": 6.437896728515625,
  "theta_flat_bias_deg": 0.5422002077102661,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5528141260147095,
  "theta_near_flat_abs_p95_deg": 4.308414459228516,
  "theta_near_flat_abs_max_deg": 5.463287830352783,
  "theta_near_flat_bias_deg": 0.9929165840148926,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2432750463485718,
  "theta_flat_turn_abs_p95_deg": 4.165439605712891,
  "theta_flat_turn_abs_max_deg": 5.292373180389404,
  "theta_flat_turn_bias_deg": 0.4584115445613861,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.790584921836853,
  "theta_slope_control_abs_p95_deg": 9.446183204650879,
  "theta_slope_control_abs_max_deg": 12.622578620910645,
  "theta_slope_control_bias_deg": 0.0010542012751102448,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7905849814414978,
  "theta_all_rmse_deg": 1.2045361995697021,
  "theta_all_p95_abs_err_deg": 2.694718837738037,
  "theta_all_max_abs_err_deg": 7.008864402770996,
  "theta_all_bias_deg": 0.0010542015079408884,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7151777148246765,
  "theta_active_abs_ge_2_rmse_deg": 1.0540038347244263,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1434335708618164,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.008864402770996,
  "theta_active_abs_ge_2_bias_deg": -0.1176149919629097,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8260796070098877,
  "theta_abs_le_8_rmse_deg": 1.2447261810302734,
  "theta_abs_le_8_p95_abs_err_deg": 2.9044268131256104,
  "theta_abs_le_8_max_abs_err_deg": 7.008864402770996,
  "theta_abs_le_8_bias_deg": 0.03382651135325432,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7905849814414978,
  "theta_abs_le_10_rmse_deg": 1.2045361995697021,
  "theta_abs_le_10_p95_abs_err_deg": 2.694718837738037,
  "theta_abs_le_10_max_abs_err_deg": 7.008864402770996,
  "theta_abs_le_10_bias_deg": 0.0010542015079408884,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5180627107620239,
  "theta_pos_8_10_rmse_deg": 0.8398067951202393,
  "theta_pos_8_10_p95_abs_err_deg": 1.8110003471374512,
  "theta_pos_8_10_max_abs_err_deg": 4.978994846343994,
  "theta_pos_8_10_bias_deg": -0.19108164310455322,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.765756368637085,
  "theta_neg_10_8_rmse_deg": 1.171211838722229,
  "theta_neg_10_8_p95_abs_err_deg": 2.0607388019561768,
  "theta_neg_10_8_max_abs_err_deg": 5.9599528312683105,
  "theta_neg_10_8_bias_deg": -0.08238288015127182,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5716511011123657,
  "theta_pos_6_8_rmse_deg": 0.7797563672065735,
  "theta_pos_6_8_p95_abs_err_deg": 1.4292548894882202,
  "theta_pos_6_8_max_abs_err_deg": 3.1905040740966797,
  "theta_pos_6_8_bias_deg": -0.19415819644927979,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7638648152351379,
  "theta_neg_8_6_rmse_deg": 1.1399575471878052,
  "theta_neg_8_6_p95_abs_err_deg": 2.0065455436706543,
  "theta_neg_8_6_max_abs_err_deg": 7.008864402770996,
  "theta_neg_8_6_bias_deg": -0.0022410189267247915,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7787685990333557,
  "theta_neg_4_2_rmse_deg": 1.1069217920303345,
  "theta_neg_4_2_p95_abs_err_deg": 2.1909430027008057,
  "theta_neg_4_2_max_abs_err_deg": 5.380542278289795,
  "theta_neg_4_2_bias_deg": -0.41292548179626465,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6142206788063049,
  "theta_neg_2_0p5_rmse_deg": 0.9309574365615845,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6023225784301758,
  "theta_neg_2_0p5_max_abs_err_deg": 5.46011209487915,
  "theta_neg_2_0p5_bias_deg": -0.2352520227432251,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0692075490951538,
  "theta_pos_0p5_2_rmse_deg": 1.4874380826950073,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6654398441314697,
  "theta_pos_0p5_2_max_abs_err_deg": 4.665924549102783,
  "theta_pos_0p5_2_bias_deg": 0.7452297210693359,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3225401294086234,
  "loss_turn": 1.2437313265342351,
  "loss_theta": 0.00044185991792187237,
  "loss_main_bundle_base": 0.3225401294086234,
  "loss_turn_bundle_base": 0.0994985044425976,
  "loss_theta_bundle_base": 0.0002989310858026399,
  "loss_main_bundle": 0.3225401294086234,
  "loss_turn_bundle": 0.0994985044425976,
  "loss_theta_bundle": 0.0002989310858026399,
  "loss_theta_flat": 0.0003112046390950506,
  "loss_theta_near_flat": 0.0014371598489123808,
  "loss_theta_error_excess": 0.0001637645370606711,
  "loss_theta_flat_excess": 0.0001512274945135725,
  "loss_theta_near_flat_excess": 0.0010389348262661365,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010375339689561202,
  "loss_theta_small_neg": 0.00036974198645527736,
  "loss_theta_small_neg_excess": 0.00010812932728438138,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.33880652522363264,
  "loss_false_turn_straight": 0.27798067036113816,
  "loss_transition_focal_raw": 0.9047143653861885,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.169896925791727,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
