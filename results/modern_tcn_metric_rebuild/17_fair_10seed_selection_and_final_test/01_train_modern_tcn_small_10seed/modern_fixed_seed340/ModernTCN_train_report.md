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
| acc_main | 0.9606 |
| acc_turn | 0.6152 |
| acc_turn_pure | 0.6346 |
| acc_turn_transition | 0.5306 |
| main_confidence_mean | 0.9855 |
| main_low_conf_0p60_ratio | 0.0061 |
| main_low_conf_0p70_ratio | 0.0164 |
| turn_confidence_mean | 0.7898 |
| turn_low_conf_0p60_ratio | 0.1960 |
| turn_low_conf_0p70_ratio | 0.3395 |
| turn_right_recall | 0.5632 |
| turn_straight_recall | 0.6622 |
| turn_left_recall | 0.5586 |
| theta_mae_deg | 0.6287 |
| theta_abs_le_10_p95_abs_err_deg | 1.9276 |
| theta_neg_10_8_p95_abs_err_deg | 2.3892 |
| theta_pos_8_10_p95_abs_err_deg | 2.9891 |
| theta_abs_le_8_p95_abs_err_deg | 1.6604 |
| theta_neg_8_6_p95_abs_err_deg | 1.9001 |
| theta_pos_6_8_p95_abs_err_deg | 1.7412 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3217 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6703 |
| theta_flat_abs_p95_deg | 2.4965 |
| theta_flat_bias_deg | -0.0707 |
| theta_near_flat_abs_p95_deg | 1.6346 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1261 |
| theta_flat_turn_abs_p95_deg | 1.3076 |
| flat_recall | 0.9352 |
| stall_recall | 0.6979 |
| slope_recall | 0.9767 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0729 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.8031 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    707,
    0,
    49
  ],
  [
    7,
    67,
    22
  ],
  [
    51,
    13,
    2686
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    450,
    252,
    97
  ],
  [
    297,
    1280,
    356
  ],
  [
    91,
    293,
    486
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.359578 |
| test_loss_turn_bundle_base | 0.098426 |
| test_loss_theta_bundle_base | 0.000176 |
| test_loss_transition_focal_raw | 1.041443 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.864146 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 71
- train_seconds: 1035.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 22 | 0.5000 | 0.5556 |
| [0.60,0.70) | 37 | 0.5946 | 0.6631 |
| [0.70,0.80) | 49 | 0.3878 | 0.7427 |
| [0.80,0.90) | 59 | 0.3220 | 0.8520 |
| [0.90,1.00) | 3435 | 0.0207 | 0.9975 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 706 | 0.5057 | 0.5278 |
| [0.60,0.70) | 517 | 0.4681 | 0.6484 |
| [0.70,0.80) | 503 | 0.4911 | 0.7507 |
| [0.80,0.90) | 539 | 0.4156 | 0.8490 |
| [0.90,1.00) | 1337 | 0.2364 | 0.9737 |


## 验证集最佳点

```json
{
  "loss_total": 0.4807308855172907,
  "acc_main": 0.9336941813261164,
  "acc_turn": 0.6373477672530447,
  "acc_turn_pure": 0.6476565060635857,
  "acc_turn_transition": 0.5885093167701864,
  "false_turn_straight": 0.303014553014553,
  "flat_recall": 0.8995433789954338,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.8995433789954338,
    0.3333333333333333,
    0.9495994659546061
  ],
  "turn_right_recall": 0.5509478672985783,
  "turn_straight_recall": 0.696985446985447,
  "turn_left_recall": 0.5922330097087378,
  "recall_turn": [
    0.5509478672985783,
    0.696985446985447,
    0.5922330097087378
  ],
  "cm_turn": [
    [
      465,
      333,
      46
    ],
    [
      280,
      1341,
      303
    ],
    [
      58,
      320,
      549
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      591,
      1,
      65
    ],
    [
      0,
      14,
      28
    ],
    [
      132,
      19,
      2845
    ]
  ],
  "main_confidence_mean": 0.9643133070120646,
  "main_confidence_error_mean": 0.7682743339489201,
  "main_low_conf_0p60_ratio": 0.05412719891745602,
  "main_low_conf_0p70_ratio": 0.06387009472259811,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 200,
      "error_rate": 0.445,
      "mean_confidence": 0.5344840504869997
    },
    {
      "bin": "[0.60,0.70)",
      "n": 36,
      "error_rate": 0.5833333333333334,
      "mean_confidence": 0.645877755187833
    },
    {
      "bin": "[0.70,0.80)",
      "n": 45,
      "error_rate": 0.4222222222222222,
      "mean_confidence": 0.757333296381386
    },
    {
      "bin": "[0.80,0.90)",
      "n": 48,
      "error_rate": 0.2708333333333333,
      "mean_confidence": 0.8594500061826539
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3366,
      "error_rate": 0.030600118835412953,
      "mean_confidence": 0.9975209927188019
    }
  ],
  "turn_confidence_mean": 0.7994543548452674,
  "turn_confidence_error_mean": 0.7184429174560023,
  "turn_low_conf_0p60_ratio": 0.20243572395128553,
  "turn_low_conf_0p70_ratio": 0.31610284167794317,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 748,
      "error_rate": 0.5561497326203209,
      "mean_confidence": 0.4825584174006512
    },
    {
      "bin": "[0.60,0.70)",
      "n": 420,
      "error_rate": 0.5404761904761904,
      "mean_confidence": 0.6485594823414804
    },
    {
      "bin": "[0.70,0.80)",
      "n": 406,
      "error_rate": 0.4729064039408867,
      "mean_confidence": 0.7461629641542645
    },
    {
      "bin": "[0.80,0.90)",
      "n": 456,
      "error_rate": 0.3530701754385965,
      "mean_confidence": 0.8551620692706556
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1665,
      "error_rate": 0.2066066066066066,
      "mean_confidence": 0.9776210782703326
    }
  ],
  "theta_mae_rad": 0.013185635209083557,
  "theta_mae_deg": 0.7554811835289001,
  "uphill_recall": 0.7816711590296496,
  "downhill_recall": 0.8120133481646273,
  "slope_sign_acc": 0.9608540925266904,
  "theta_flat_mae_deg": 1.0150882005691528,
  "theta_flat_abs_p95_deg": 3.7221574783325195,
  "theta_flat_abs_max_deg": 6.58587121963501,
  "theta_flat_bias_deg": 0.5499352216720581,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3854483366012573,
  "theta_near_flat_abs_p95_deg": 3.722189426422119,
  "theta_near_flat_abs_max_deg": 6.249512672424316,
  "theta_near_flat_bias_deg": 0.8496115803718567,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1215978860855103,
  "theta_flat_turn_abs_p95_deg": 3.7221574783325195,
  "theta_flat_turn_abs_max_deg": 5.850774765014648,
  "theta_flat_turn_bias_deg": 0.4047074317932129,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7554811835289001,
  "theta_slope_control_abs_p95_deg": 9.300677299499512,
  "theta_slope_control_abs_max_deg": 12.43667221069336,
  "theta_slope_control_bias_deg": 0.12362086772918701,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7554812431335449,
  "theta_all_rmse_deg": 1.1444532871246338,
  "theta_all_p95_abs_err_deg": 2.4005188941955566,
  "theta_all_max_abs_err_deg": 8.795682907104492,
  "theta_all_bias_deg": 0.12362086772918701,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.69855135679245,
  "theta_active_abs_ge_2_rmse_deg": 1.045579433441162,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0872669219970703,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.795682907104492,
  "theta_active_abs_ge_2_bias_deg": 0.030133383348584175,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7774887681007385,
  "theta_abs_le_8_rmse_deg": 1.146669864654541,
  "theta_abs_le_8_p95_abs_err_deg": 2.455101490020752,
  "theta_abs_le_8_max_abs_err_deg": 6.594699382781982,
  "theta_abs_le_8_bias_deg": 0.1419600397348404,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7554812431335449,
  "theta_abs_le_10_rmse_deg": 1.1444532871246338,
  "theta_abs_le_10_p95_abs_err_deg": 2.4005188941955566,
  "theta_abs_le_10_max_abs_err_deg": 8.795682907104492,
  "theta_abs_le_10_bias_deg": 0.12362086772918701,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.565008819103241,
  "theta_pos_8_10_rmse_deg": 0.8340958952903748,
  "theta_pos_8_10_p95_abs_err_deg": 1.6880333423614502,
  "theta_pos_8_10_max_abs_err_deg": 5.370633125305176,
  "theta_pos_8_10_bias_deg": -0.2273864895105362,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7619609832763672,
  "theta_neg_10_8_rmse_deg": 1.375220537185669,
  "theta_neg_10_8_p95_abs_err_deg": 2.5191335678100586,
  "theta_neg_10_8_max_abs_err_deg": 8.795682907104492,
  "theta_neg_10_8_bias_deg": 0.32462969422340393,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5882126092910767,
  "theta_pos_6_8_rmse_deg": 0.8355347514152527,
  "theta_pos_6_8_p95_abs_err_deg": 1.8711179494857788,
  "theta_pos_6_8_max_abs_err_deg": 3.328273296356201,
  "theta_pos_6_8_bias_deg": -0.01950322836637497,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7594223022460938,
  "theta_neg_8_6_rmse_deg": 1.087845802307129,
  "theta_neg_8_6_p95_abs_err_deg": 2.305940628051758,
  "theta_neg_8_6_max_abs_err_deg": 6.389893531799316,
  "theta_neg_8_6_bias_deg": 0.2065688818693161,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7040720582008362,
  "theta_neg_4_2_rmse_deg": 1.0168616771697998,
  "theta_neg_4_2_p95_abs_err_deg": 1.994066596031189,
  "theta_neg_4_2_max_abs_err_deg": 6.594699382781982,
  "theta_neg_4_2_bias_deg": -0.12475550174713135,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6307663917541504,
  "theta_neg_2_0p5_rmse_deg": 0.8794891834259033,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5784013271331787,
  "theta_neg_2_0p5_max_abs_err_deg": 4.878030776977539,
  "theta_neg_2_0p5_bias_deg": 0.2625153660774231,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9687293171882629,
  "theta_pos_0p5_2_rmse_deg": 1.3527404069900513,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.2369589805603027,
  "theta_pos_0p5_2_max_abs_err_deg": 4.81389856338501,
  "theta_pos_0p5_2_bias_deg": 0.5690951943397522,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.37355822744163025,
  "loss_turn": 1.3362766133270987,
  "loss_theta": 0.00039891662334938846,
  "loss_main_bundle_base": 0.37355822744163025,
  "loss_turn_bundle_base": 0.1069021268670872,
  "loss_theta_bundle_base": 0.00027053174951853525,
  "loss_main_bundle": 0.37355822744163025,
  "loss_turn_bundle": 0.1069021268670872,
  "loss_theta_bundle": 0.00027053174951853525,
  "loss_theta_flat": 0.0002777978692031106,
  "loss_theta_near_flat": 0.0011174818541046802,
  "loss_theta_error_excess": 0.00014149825125226955,
  "loss_theta_flat_excess": 0.000128644106941769,
  "loss_theta_near_flat_excess": 0.0007769297250276822,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010716939688104435,
  "loss_theta_small_neg": 0.0003090608209851721,
  "loss_theta_small_neg_excess": 8.574246587973726e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.30006796111918593,
  "loss_false_turn_straight": 0.22865122084446624,
  "loss_transition_focal_raw": 1.0321826863192092,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.074590356621755,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
