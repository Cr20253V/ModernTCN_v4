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
| acc_main | 0.9667 |
| acc_turn | 0.5972 |
| acc_turn_pure | 0.6124 |
| acc_turn_transition | 0.5306 |
| main_confidence_mean | 0.9911 |
| main_low_conf_0p60_ratio | 0.0028 |
| main_low_conf_0p70_ratio | 0.0114 |
| turn_confidence_mean | 0.8485 |
| turn_low_conf_0p60_ratio | 0.1346 |
| turn_low_conf_0p70_ratio | 0.2249 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.5898 |
| turn_left_recall | 0.6046 |
| theta_mae_deg | 0.5688 |
| theta_abs_le_10_p95_abs_err_deg | 1.5278 |
| theta_neg_10_8_p95_abs_err_deg | 1.1484 |
| theta_pos_8_10_p95_abs_err_deg | 2.5275 |
| theta_abs_le_8_p95_abs_err_deg | 1.4447 |
| theta_neg_8_6_p95_abs_err_deg | 1.3690 |
| theta_pos_6_8_p95_abs_err_deg | 1.5683 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2521 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3139 |
| theta_flat_abs_p95_deg | 2.2943 |
| theta_flat_bias_deg | -0.0813 |
| theta_near_flat_abs_p95_deg | 1.6834 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1475 |
| theta_flat_turn_abs_p95_deg | 1.3550 |
| flat_recall | 0.9656 |
| stall_recall | 0.6979 |
| slope_recall | 0.9764 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7534 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    730,
    1,
    25
  ],
  [
    10,
    67,
    19
  ],
  [
    55,
    10,
    2685
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    485,
    200,
    114
  ],
  [
    341,
    1140,
    452
  ],
  [
    158,
    186,
    526
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.355533 |
| test_loss_turn_bundle_base | 0.355151 |
| test_loss_theta_bundle_base | 0.000129 |
| test_loss_transition_focal_raw | 1.646837 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.979377 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 379.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 10 | 0.8000 | 0.5428 |
| [0.60,0.70) | 31 | 0.6129 | 0.6519 |
| [0.70,0.80) | 25 | 0.5600 | 0.7554 |
| [0.80,0.90) | 37 | 0.2432 | 0.8644 |
| [0.90,1.00) | 3499 | 0.0200 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 485 | 0.5918 | 0.5183 |
| [0.60,0.70) | 325 | 0.4923 | 0.6472 |
| [0.70,0.80) | 336 | 0.4732 | 0.7505 |
| [0.80,0.90) | 465 | 0.5118 | 0.8553 |
| [0.90,1.00) | 1991 | 0.3049 | 0.9768 |


## 验证集最佳点

```json
{
  "loss_total": 0.7083996143973406,
  "acc_main": 0.9431664411366711,
  "acc_turn": 0.6400541271989174,
  "acc_turn_pure": 0.655850540806293,
  "acc_turn_transition": 0.5652173913043478,
  "false_turn_straight": 0.41164241164241167,
  "flat_recall": 0.9406392694063926,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9512683578104139,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9406392694063926,
    0.40476190476190477,
    0.9512683578104139
  ],
  "turn_right_recall": 0.6267772511848341,
  "turn_straight_recall": 0.5883575883575883,
  "turn_left_recall": 0.7594390507011867,
  "recall_turn": [
    0.6267772511848341,
    0.5883575883575883,
    0.7594390507011867
  ],
  "cm_turn": [
    [
      529,
      202,
      113
    ],
    [
      279,
      1132,
      513
    ],
    [
      61,
      162,
      704
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      618,
      0,
      39
    ],
    [
      0,
      17,
      25
    ],
    [
      134,
      12,
      2850
    ]
  ],
  "main_confidence_mean": 0.9706475256833885,
  "main_confidence_error_mean": 0.7822841796541644,
  "main_low_conf_0p60_ratio": 0.04844384303112314,
  "main_low_conf_0p70_ratio": 0.055209742895805144,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 179,
      "error_rate": 0.46368715083798884,
      "mean_confidence": 0.5305038554386492
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.24,
      "mean_confidence": 0.6531656560486109
    },
    {
      "bin": "[0.70,0.80)",
      "n": 19,
      "error_rate": 0.42105263157894735,
      "mean_confidence": 0.7709543324880913
    },
    {
      "bin": "[0.80,0.90)",
      "n": 34,
      "error_rate": 0.29411764705882354,
      "mean_confidence": 0.8513234924910957
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3438,
      "error_rate": 0.029959278650378125,
      "mean_confidence": 0.9981559467171076
    }
  ],
  "turn_confidence_mean": 0.8662381187368298,
  "turn_confidence_error_mean": 0.792889962279778,
  "turn_low_conf_0p60_ratio": 0.12476319350473614,
  "turn_low_conf_0p70_ratio": 0.18998646820027063,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 461,
      "error_rate": 0.6442516268980477,
      "mean_confidence": 0.4828837784317336
    },
    {
      "bin": "[0.60,0.70)",
      "n": 241,
      "error_rate": 0.5020746887966805,
      "mean_confidence": 0.6509303270602828
    },
    {
      "bin": "[0.70,0.80)",
      "n": 290,
      "error_rate": 0.4689655172413793,
      "mean_confidence": 0.752064332183085
    },
    {
      "bin": "[0.80,0.90)",
      "n": 379,
      "error_rate": 0.44854881266490765,
      "mean_confidence": 0.8520921184435967
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2324,
      "error_rate": 0.2607573149741824,
      "mean_confidence": 0.9811637903747036
    }
  ],
  "theta_mae_rad": 0.013363574631512165,
  "theta_mae_deg": 0.7656763792037964,
  "uphill_recall": 0.7746630727762803,
  "downhill_recall": 0.8075639599555061,
  "slope_sign_acc": 0.9794689296468656,
  "theta_flat_mae_deg": 1.0210460424423218,
  "theta_flat_abs_p95_deg": 3.338451623916626,
  "theta_flat_abs_max_deg": 9.391289710998535,
  "theta_flat_bias_deg": 0.1535748541355133,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2653430700302124,
  "theta_near_flat_abs_p95_deg": 3.4147789478302,
  "theta_near_flat_abs_max_deg": 9.391289710998535,
  "theta_near_flat_bias_deg": 0.4262625277042389,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0126333236694336,
  "theta_flat_turn_abs_p95_deg": 4.034082889556885,
  "theta_flat_turn_abs_max_deg": 9.391289710998535,
  "theta_flat_turn_bias_deg": -0.08097916841506958,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7656763792037964,
  "theta_slope_control_abs_p95_deg": 9.217101097106934,
  "theta_slope_control_abs_max_deg": 12.546833992004395,
  "theta_slope_control_bias_deg": -0.061299171298742294,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7656763792037964,
  "theta_all_rmse_deg": 1.1430728435516357,
  "theta_all_p95_abs_err_deg": 2.460026502609253,
  "theta_all_max_abs_err_deg": 8.891290664672852,
  "theta_all_bias_deg": -0.061299171298742294,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7096757292747498,
  "theta_active_abs_ge_2_rmse_deg": 1.050950050354004,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.091139554977417,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.045554161071777,
  "theta_active_abs_ge_2_bias_deg": -0.10841940343379974,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7934057116508484,
  "theta_abs_le_8_rmse_deg": 1.1764057874679565,
  "theta_abs_le_8_p95_abs_err_deg": 2.610278606414795,
  "theta_abs_le_8_max_abs_err_deg": 8.891290664672852,
  "theta_abs_le_8_bias_deg": -0.052598051726818085,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7656763792037964,
  "theta_abs_le_10_rmse_deg": 1.1430728435516357,
  "theta_abs_le_10_p95_abs_err_deg": 2.460026502609253,
  "theta_abs_le_10_max_abs_err_deg": 8.891290664672852,
  "theta_abs_le_10_bias_deg": -0.061299171298742294,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6043056845664978,
  "theta_pos_8_10_rmse_deg": 0.7962271571159363,
  "theta_pos_8_10_p95_abs_err_deg": 1.5952342748641968,
  "theta_pos_8_10_max_abs_err_deg": 4.382437229156494,
  "theta_pos_8_10_bias_deg": -0.310920387506485,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6938582062721252,
  "theta_neg_10_8_rmse_deg": 1.1545246839523315,
  "theta_neg_10_8_p95_abs_err_deg": 2.2088770866394043,
  "theta_neg_10_8_max_abs_err_deg": 6.045554161071777,
  "theta_neg_10_8_bias_deg": 0.11859102547168732,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.564002513885498,
  "theta_pos_6_8_rmse_deg": 0.7851583361625671,
  "theta_pos_6_8_p95_abs_err_deg": 1.6327621936798096,
  "theta_pos_6_8_max_abs_err_deg": 3.515946388244629,
  "theta_pos_6_8_bias_deg": -0.13801664113998413,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7539064884185791,
  "theta_neg_8_6_rmse_deg": 1.1130905151367188,
  "theta_neg_8_6_p95_abs_err_deg": 1.966437816619873,
  "theta_neg_8_6_max_abs_err_deg": 5.888946056365967,
  "theta_neg_8_6_bias_deg": -0.23640868067741394,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8040741086006165,
  "theta_neg_4_2_rmse_deg": 1.143420934677124,
  "theta_neg_4_2_p95_abs_err_deg": 2.335325002670288,
  "theta_neg_4_2_max_abs_err_deg": 5.170037746429443,
  "theta_neg_4_2_bias_deg": -0.4711209833621979,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8082340359687805,
  "theta_neg_2_0p5_rmse_deg": 1.0839543342590332,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.371767044067383,
  "theta_neg_2_0p5_max_abs_err_deg": 4.010660171508789,
  "theta_neg_2_0p5_bias_deg": -0.587358832359314,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9777019619941711,
  "theta_pos_0p5_2_rmse_deg": 1.2147427797317505,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9634164571762085,
  "theta_pos_0p5_2_max_abs_err_deg": 3.8732190132141113,
  "theta_pos_0p5_2_bias_deg": 0.7107566595077515,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.38023905776672984,
  "loss_turn": 1.639513078723128,
  "loss_theta": 0.00039804280457982896,
  "loss_main_bundle_base": 0.38023905776672984,
  "loss_turn_bundle_base": 0.3279026209340205,
  "loss_theta_bundle_base": 0.00025794645942305244,
  "loss_main_bundle": 0.38023905776672984,
  "loss_turn_bundle": 0.3279026209340205,
  "loss_theta_bundle": 0.00025794645942305244,
  "loss_theta_flat": 0.0001793486034459496,
  "loss_theta_near_flat": 0.0011837977893317825,
  "loss_theta_error_excess": 0.00013738093614617316,
  "loss_theta_flat_excess": 7.951796937780991e-05,
  "loss_theta_near_flat_excess": 0.0008344422584129888,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010632025421356357,
  "loss_theta_small_neg": 0.00039588195153326803,
  "loss_theta_small_neg_excess": 0.00012133782850805271,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3751271909644704,
  "loss_false_turn_straight": 0.31238780991956894,
  "loss_transition_focal_raw": 1.451380595915695,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.032946887911865,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
