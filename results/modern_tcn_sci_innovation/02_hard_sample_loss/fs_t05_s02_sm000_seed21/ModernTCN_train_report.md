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

- lambda_transition_focal: `0.5`
- lambda_stall_focal: `0.2`
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
  "lambda_transition_focal": 0.5,
  "lambda_stall_focal": 0.2,
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
| acc_main | 0.9567 |
| acc_turn | 0.4839 |
| acc_turn_pure | 0.4787 |
| acc_turn_transition | 0.5067 |
| main_confidence_mean | 0.9744 |
| main_low_conf_0p60_ratio | 0.0125 |
| main_low_conf_0p70_ratio | 0.0289 |
| turn_confidence_mean | 0.6126 |
| turn_low_conf_0p60_ratio | 0.5316 |
| turn_low_conf_0p70_ratio | 0.7224 |
| turn_right_recall | 0.5019 |
| turn_straight_recall | 0.4351 |
| turn_left_recall | 0.5759 |
| theta_mae_deg | 0.9545 |
| theta_abs_le_10_p95_abs_err_deg | 2.4752 |
| theta_neg_10_8_p95_abs_err_deg | 2.5837 |
| theta_pos_8_10_p95_abs_err_deg | 3.7539 |
| theta_abs_le_8_p95_abs_err_deg | 2.3710 |
| theta_neg_8_6_p95_abs_err_deg | 2.3760 |
| theta_pos_6_8_p95_abs_err_deg | 2.0331 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0891 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.6388 |
| theta_flat_abs_p95_deg | 2.6736 |
| theta_flat_bias_deg | -0.4003 |
| theta_near_flat_abs_p95_deg | 2.1228 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4056 |
| theta_flat_turn_abs_p95_deg | 2.1850 |
| flat_recall | 0.9312 |
| stall_recall | 0.6979 |
| slope_recall | 0.9727 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7466 |
| downhill_recall | 0.8087 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    704,
    0,
    52
  ],
  [
    9,
    67,
    20
  ],
  [
    41,
    34,
    2675
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    401,
    224,
    174
  ],
  [
    466,
    841,
    626
  ],
  [
    182,
    187,
    501
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.305479 |
| test_loss_turn_bundle_base | 0.217453 |
| test_loss_theta_bundle_base | 0.000330 |
| test_loss_transition_focal_raw | 0.571200 |
| test_loss_transition_focal_weighted | 0.285600 |
| test_loss_stall_focal_raw | 2.944072 |
| test_loss_stall_focal_weighted | 0.588815 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 28
- train_seconds: 203.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 45 | 0.3778 | 0.5390 |
| [0.60,0.70) | 59 | 0.4746 | 0.6504 |
| [0.70,0.80) | 60 | 0.2667 | 0.7529 |
| [0.80,0.90) | 99 | 0.1818 | 0.8534 |
| [0.90,1.00) | 3339 | 0.0231 | 0.9935 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1915 | 0.5681 | 0.4911 |
| [0.60,0.70) | 687 | 0.5473 | 0.6421 |
| [0.70,0.80) | 469 | 0.5245 | 0.7483 |
| [0.80,0.90) | 295 | 0.3966 | 0.8506 |
| [0.90,1.00) | 236 | 0.1356 | 0.9454 |


## 验证集最佳点

```json
{
  "loss_total": 1.296513811854774,
  "acc_main": 0.9412719891745602,
  "acc_turn": 0.5050067658998647,
  "acc_turn_pure": 0.5027859718125205,
  "acc_turn_transition": 0.515527950310559,
  "false_turn_straight": 0.5878378378378378,
  "flat_recall": 0.9482496194824962,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9472630173564753,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9482496194824962,
    0.40476190476190477,
    0.9472630173564753
  ],
  "turn_right_recall": 0.5533175355450237,
  "turn_straight_recall": 0.41216216216216217,
  "turn_left_recall": 0.6537216828478964,
  "recall_turn": [
    0.5533175355450237,
    0.41216216216216217,
    0.6537216828478964
  ],
  "cm_turn": [
    [
      467,
      195,
      182
    ],
    [
      519,
      793,
      612
    ],
    [
      152,
      169,
      606
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
      17,
      25
    ],
    [
      128,
      30,
      2838
    ]
  ],
  "main_confidence_mean": 0.9620534513254825,
  "main_confidence_error_mean": 0.8002238451624358,
  "main_low_conf_0p60_ratio": 0.010284167794316644,
  "main_low_conf_0p70_ratio": 0.06982408660351827,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 38,
      "error_rate": 0.42105263157894735,
      "mean_confidence": 0.5535000418144321
    },
    {
      "bin": "[0.60,0.70)",
      "n": 220,
      "error_rate": 0.40454545454545454,
      "mean_confidence": 0.6775652435552754
    },
    {
      "bin": "[0.70,0.80)",
      "n": 53,
      "error_rate": 0.3018867924528302,
      "mean_confidence": 0.7567044846979245
    },
    {
      "bin": "[0.80,0.90)",
      "n": 128,
      "error_rate": 0.1171875,
      "mean_confidence": 0.854776565854008
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3256,
      "error_rate": 0.024877149877149878,
      "mean_confidence": 0.993603626952778
    }
  ],
  "turn_confidence_mean": 0.6337139027091997,
  "turn_confidence_error_mean": 0.5973038918908566,
  "turn_low_conf_0p60_ratio": 0.4871447902571042,
  "turn_low_conf_0p70_ratio": 0.6768606224627876,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1800,
      "error_rate": 0.5555555555555556,
      "mean_confidence": 0.49707612426913983
    },
    {
      "bin": "[0.60,0.70)",
      "n": 701,
      "error_rate": 0.5734664764621968,
      "mean_confidence": 0.6469070530650308
    },
    {
      "bin": "[0.70,0.80)",
      "n": 494,
      "error_rate": 0.5222672064777328,
      "mean_confidence": 0.7479127963539309
    },
    {
      "bin": "[0.80,0.90)",
      "n": 357,
      "error_rate": 0.37254901960784315,
      "mean_confidence": 0.8552417745163952
    },
    {
      "bin": "[0.90,1.00)",
      "n": 343,
      "error_rate": 0.10495626822157435,
      "mean_confidence": 0.9287573403097944
    }
  ],
  "theta_mae_rad": 0.017718417569994926,
  "theta_mae_deg": 1.0151904821395874,
  "uphill_recall": 0.7730458221024259,
  "downhill_recall": 0.7997775305895439,
  "slope_sign_acc": 0.9668765398302764,
  "theta_flat_mae_deg": 1.080826759338379,
  "theta_flat_abs_p95_deg": 2.9804296493530273,
  "theta_flat_abs_max_deg": 9.417802810668945,
  "theta_flat_bias_deg": 0.3338858187198639,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5872688293457031,
  "theta_near_flat_abs_p95_deg": 4.627111911773682,
  "theta_near_flat_abs_max_deg": 9.417802810668945,
  "theta_near_flat_bias_deg": 0.8035150766372681,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.4304691553115845,
  "theta_flat_turn_abs_p95_deg": 5.49857759475708,
  "theta_flat_turn_abs_max_deg": 9.417802810668945,
  "theta_flat_turn_bias_deg": 0.5538215637207031,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.0151904821395874,
  "theta_slope_control_abs_p95_deg": 9.005035400390625,
  "theta_slope_control_abs_max_deg": 12.801239967346191,
  "theta_slope_control_bias_deg": 0.3266555666923523,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.015190601348877,
  "theta_all_rmse_deg": 1.4481433629989624,
  "theta_all_p95_abs_err_deg": 2.8305106163024902,
  "theta_all_max_abs_err_deg": 9.917801856994629,
  "theta_all_bias_deg": 0.3266555368900299,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.0007970333099365,
  "theta_active_abs_ge_2_rmse_deg": 1.4017692804336548,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.7766475677490234,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.566125869750977,
  "theta_active_abs_ge_2_bias_deg": 0.32507002353668213,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9986847043037415,
  "theta_abs_le_8_rmse_deg": 1.4364299774169922,
  "theta_abs_le_8_p95_abs_err_deg": 2.840636730194092,
  "theta_abs_le_8_max_abs_err_deg": 9.917801856994629,
  "theta_abs_le_8_bias_deg": 0.2884802520275116,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.015190601348877,
  "theta_abs_le_10_rmse_deg": 1.4481433629989624,
  "theta_abs_le_10_p95_abs_err_deg": 2.8305106163024902,
  "theta_abs_le_10_max_abs_err_deg": 9.917801856994629,
  "theta_abs_le_10_bias_deg": 0.3266555368900299,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7747586369514465,
  "theta_pos_8_10_rmse_deg": 1.0237300395965576,
  "theta_pos_8_10_p95_abs_err_deg": 1.8744266033172607,
  "theta_pos_8_10_max_abs_err_deg": 4.30124044418335,
  "theta_pos_8_10_bias_deg": -0.27567169070243835,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.4002456665039062,
  "theta_neg_10_8_rmse_deg": 1.857927918434143,
  "theta_neg_10_8_p95_abs_err_deg": 3.585334300994873,
  "theta_neg_10_8_max_abs_err_deg": 8.566125869750977,
  "theta_neg_10_8_bias_deg": 1.264272689819336,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8971496820449829,
  "theta_pos_6_8_rmse_deg": 1.256287693977356,
  "theta_pos_6_8_p95_abs_err_deg": 2.669625997543335,
  "theta_pos_6_8_max_abs_err_deg": 4.704781532287598,
  "theta_pos_6_8_bias_deg": -0.26358655095100403,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0684099197387695,
  "theta_neg_8_6_rmse_deg": 1.4317506551742554,
  "theta_neg_8_6_p95_abs_err_deg": 2.7647013664245605,
  "theta_neg_8_6_max_abs_err_deg": 8.456912994384766,
  "theta_neg_8_6_bias_deg": 0.7482737898826599,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.927258312702179,
  "theta_neg_4_2_rmse_deg": 1.2643662691116333,
  "theta_neg_4_2_p95_abs_err_deg": 2.5998315811157227,
  "theta_neg_4_2_max_abs_err_deg": 6.67967414855957,
  "theta_neg_4_2_bias_deg": 0.454321026802063,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6227881908416748,
  "theta_neg_2_0p5_rmse_deg": 0.8460819125175476,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3703644275665283,
  "theta_neg_2_0p5_max_abs_err_deg": 4.260255336761475,
  "theta_neg_2_0p5_bias_deg": -0.053600020706653595,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.902907133102417,
  "theta_pos_0p5_2_rmse_deg": 1.195371150970459,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.7106126546859741,
  "theta_pos_0p5_2_max_abs_err_deg": 5.252908229827881,
  "theta_pos_0p5_2_bias_deg": 0.20469431579113007,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.277114524860666,
  "loss_turn": 1.0431978386374385,
  "loss_theta": 0.0006389573604909448,
  "loss_main_bundle_base": 0.277114524860666,
  "loss_turn_bundle_base": 0.20863957174011433,
  "loss_theta_bundle_base": 0.0004474009180120766,
  "loss_main_bundle": 0.8021065521950006,
  "loss_turn_bundle": 0.49395984235409957,
  "loss_theta_bundle": 0.0004474009180120766,
  "loss_theta_flat": 0.000509215445036865,
  "loss_theta_near_flat": 0.0014028169941888045,
  "loss_theta_error_excess": 0.00025255409920341127,
  "loss_theta_flat_excess": 0.0002439986319323379,
  "loss_theta_near_flat_excess": 0.0009960037882027692,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00022240805932171315,
  "loss_theta_small_neg": 0.0004790227646442919,
  "loss_theta_small_neg_excess": 0.00014033610866169088,
  "loss_turn_release": 0.40882368345060593,
  "loss_false_turn_straight": 0.36150118608597326,
  "loss_transition_focal_raw": 0.5706405547862123,
  "loss_transition_focal_weighted": 0.28532027739310617,
  "loss_stall_focal_raw": 2.624960069897231,
  "loss_stall_focal_weighted": 0.5249920209995296,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
