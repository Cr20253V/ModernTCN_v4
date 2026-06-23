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
  "lambda_theta": 0.65,
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
| acc_main | 0.9647 |
| acc_turn | 0.5766 |
| acc_turn_pure | 0.5885 |
| acc_turn_transition | 0.5246 |
| main_confidence_mean | 0.9862 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0153 |
| turn_confidence_mean | 0.8257 |
| turn_low_conf_0p60_ratio | 0.1491 |
| turn_low_conf_0p70_ratio | 0.2593 |
| turn_right_recall | 0.6408 |
| turn_straight_recall | 0.5665 |
| turn_left_recall | 0.5402 |
| theta_mae_deg | 0.9078 |
| theta_abs_le_10_p95_abs_err_deg | 2.1769 |
| theta_neg_10_8_p95_abs_err_deg | 1.4535 |
| theta_pos_8_10_p95_abs_err_deg | 2.8962 |
| theta_abs_le_8_p95_abs_err_deg | 2.1052 |
| theta_neg_8_6_p95_abs_err_deg | 1.7591 |
| theta_pos_6_8_p95_abs_err_deg | 2.1368 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9190 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0868 |
| theta_flat_abs_p95_deg | 2.8183 |
| theta_flat_bias_deg | -0.8824 |
| theta_near_flat_abs_p95_deg | 2.4072 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.9909 |
| theta_flat_turn_abs_p95_deg | 2.2776 |
| flat_recall | 0.9590 |
| stall_recall | 0.6667 |
| slope_recall | 0.9767 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7529 |
| downhill_recall | 0.7968 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    725,
    0,
    31
  ],
  [
    10,
    64,
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
    512,
    175,
    112
  ],
  [
    420,
    1095,
    418
  ],
  [
    157,
    243,
    470
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.378720 |
| test_loss_turn_bundle_base | 0.305989 |
| test_loss_theta_bundle_base | 0.000325 |
| test_loss_transition_focal_raw | 1.308078 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.353896 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 67
- train_seconds: 328.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.2609 | 0.5484 |
| [0.60,0.70) | 32 | 0.3125 | 0.6485 |
| [0.70,0.80) | 49 | 0.5510 | 0.7545 |
| [0.80,0.90) | 55 | 0.2727 | 0.8551 |
| [0.90,1.00) | 3443 | 0.0200 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 537 | 0.5829 | 0.5357 |
| [0.60,0.70) | 397 | 0.5516 | 0.6481 |
| [0.70,0.80) | 475 | 0.5453 | 0.7507 |
| [0.80,0.90) | 513 | 0.4873 | 0.8535 |
| [0.90,1.00) | 1680 | 0.2881 | 0.9730 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5246
- theta_mae_deg <= 0.7000 未满足，实际 0.9078

## 验证集最佳点

```json
{
  "loss_total": 0.5336128492639255,
  "acc_main": 0.9469553450608931,
  "acc_turn": 0.6227334235453316,
  "acc_turn_pure": 0.6312684365781711,
  "acc_turn_transition": 0.5822981366459627,
  "false_turn_straight": 0.4365904365904366,
  "flat_recall": 0.9634703196347032,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9509345794392523,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9634703196347032,
    0.40476190476190477,
    0.9509345794392523
  ],
  "turn_right_recall": 0.6386255924170616,
  "turn_straight_recall": 0.5634095634095634,
  "turn_left_recall": 0.7313915857605178,
  "recall_turn": [
    0.6386255924170616,
    0.5634095634095634,
    0.7313915857605178
  ],
  "cm_turn": [
    [
      539,
      210,
      95
    ],
    [
      377,
      1084,
      463
    ],
    [
      59,
      190,
      678
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      633,
      1,
      23
    ],
    [
      1,
      17,
      24
    ],
    [
      137,
      10,
      2849
    ]
  ],
  "main_confidence_mean": 0.9719281386978369,
  "main_confidence_error_mean": 0.7962170816886739,
  "main_low_conf_0p60_ratio": 0.007307171853856563,
  "main_low_conf_0p70_ratio": 0.058186738836265225,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 27,
      "error_rate": 0.2962962962962963,
      "mean_confidence": 0.5492715344261155
    },
    {
      "bin": "[0.60,0.70)",
      "n": 188,
      "error_rate": 0.44680851063829785,
      "mean_confidence": 0.6436473906038895
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.37037037037037035,
      "mean_confidence": 0.7477100556441959
    },
    {
      "bin": "[0.80,0.90)",
      "n": 55,
      "error_rate": 0.2,
      "mean_confidence": 0.8575258189574426
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3398,
      "error_rate": 0.02442613301942319,
      "mean_confidence": 0.9970825014951201
    }
  ],
  "turn_confidence_mean": 0.8244214134981162,
  "turn_confidence_error_mean": 0.7439284706859014,
  "turn_low_conf_0p60_ratio": 0.17564276048714478,
  "turn_low_conf_0p70_ratio": 0.2644113667117727,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 649,
      "error_rate": 0.6147919876733436,
      "mean_confidence": 0.4989465360947752
    },
    {
      "bin": "[0.60,0.70)",
      "n": 328,
      "error_rate": 0.5457317073170732,
      "mean_confidence": 0.6511497854701253
    },
    {
      "bin": "[0.70,0.80)",
      "n": 390,
      "error_rate": 0.4846153846153846,
      "mean_confidence": 0.7514893268531392
    },
    {
      "bin": "[0.80,0.90)",
      "n": 467,
      "error_rate": 0.4132762312633833,
      "mean_confidence": 0.853195563291386
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1861,
      "error_rate": 0.23320795271359485,
      "mean_confidence": 0.976529030513717
    }
  ],
  "theta_mae_rad": 0.01804671809077263,
  "theta_mae_deg": 1.0340007543563843,
  "uphill_recall": 0.7762803234501348,
  "downhill_recall": 0.796440489432703,
  "slope_sign_acc": 0.957021626060772,
  "theta_flat_mae_deg": 1.2198102474212646,
  "theta_flat_abs_p95_deg": 3.3134024143218994,
  "theta_flat_abs_max_deg": 6.128530979156494,
  "theta_flat_bias_deg": -0.263681024312973,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4975123405456543,
  "theta_near_flat_abs_p95_deg": 3.3149261474609375,
  "theta_near_flat_abs_max_deg": 5.673434257507324,
  "theta_near_flat_bias_deg": 0.1154356598854065,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3226442337036133,
  "theta_flat_turn_abs_p95_deg": 3.8137624263763428,
  "theta_flat_turn_abs_max_deg": 5.673434257507324,
  "theta_flat_turn_bias_deg": -0.33147937059402466,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.0340007543563843,
  "theta_slope_control_abs_p95_deg": 9.314704895019531,
  "theta_slope_control_abs_max_deg": 12.831340789794922,
  "theta_slope_control_bias_deg": -0.5817574858665466,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.0340007543563843,
  "theta_all_rmse_deg": 1.3012539148330688,
  "theta_all_p95_abs_err_deg": 2.429934024810791,
  "theta_all_max_abs_err_deg": 6.9025983810424805,
  "theta_all_bias_deg": -0.5817574858665466,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9932541251182556,
  "theta_active_abs_ge_2_rmse_deg": 1.240916132926941,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1274447441101074,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.9025983810424805,
  "theta_active_abs_ge_2_bias_deg": -0.6515092253684998,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0667887926101685,
  "theta_abs_le_8_rmse_deg": 1.3268367052078247,
  "theta_abs_le_8_p95_abs_err_deg": 2.486766815185547,
  "theta_abs_le_8_max_abs_err_deg": 6.358013153076172,
  "theta_abs_le_8_bias_deg": -0.5807527303695679,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.0340007543563843,
  "theta_abs_le_10_rmse_deg": 1.3012539148330688,
  "theta_abs_le_10_p95_abs_err_deg": 2.429934024810791,
  "theta_abs_le_10_max_abs_err_deg": 6.9025983810424805,
  "theta_abs_le_10_bias_deg": -0.5817574858665466,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.0207772254943848,
  "theta_pos_8_10_rmse_deg": 1.1671934127807617,
  "theta_pos_8_10_p95_abs_err_deg": 1.9409972429275513,
  "theta_pos_8_10_max_abs_err_deg": 4.878559589385986,
  "theta_pos_8_10_bias_deg": -0.9054430723190308,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7684237957000732,
  "theta_neg_10_8_rmse_deg": 1.2073686122894287,
  "theta_neg_10_8_p95_abs_err_deg": 2.359233856201172,
  "theta_neg_10_8_max_abs_err_deg": 6.9025983810424805,
  "theta_neg_10_8_bias_deg": -0.26102542877197266,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.0582832098007202,
  "theta_pos_6_8_rmse_deg": 1.1847831010818481,
  "theta_pos_6_8_p95_abs_err_deg": 1.9608042240142822,
  "theta_pos_6_8_max_abs_err_deg": 3.498429536819458,
  "theta_pos_6_8_bias_deg": -0.8917898535728455,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0799683332443237,
  "theta_neg_8_6_rmse_deg": 1.3668591976165771,
  "theta_neg_8_6_p95_abs_err_deg": 2.4867382049560547,
  "theta_neg_8_6_max_abs_err_deg": 6.358013153076172,
  "theta_neg_8_6_bias_deg": -0.708730161190033,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9645552635192871,
  "theta_neg_4_2_rmse_deg": 1.213722586631775,
  "theta_neg_4_2_p95_abs_err_deg": 2.3632924556732178,
  "theta_neg_4_2_max_abs_err_deg": 5.367589473724365,
  "theta_neg_4_2_bias_deg": -0.7644472122192383,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8304875493049622,
  "theta_neg_2_0p5_rmse_deg": 0.9792131185531616,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.55649733543396,
  "theta_neg_2_0p5_max_abs_err_deg": 3.9237091541290283,
  "theta_neg_2_0p5_bias_deg": -0.7523550391197205,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2376068830490112,
  "theta_pos_0p5_2_rmse_deg": 1.4392114877700806,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.352159023284912,
  "theta_pos_0p5_2_max_abs_err_deg": 4.356558322906494,
  "theta_pos_0p5_2_bias_deg": -0.2260911613702774,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.27252825158213406,
  "loss_turn": 1.3033623428886734,
  "loss_theta": 0.0005157029649264183,
  "loss_main_bundle_base": 0.27252825158213406,
  "loss_turn_bundle_base": 0.2606724725282563,
  "loss_theta_bundle_base": 0.0004121238953517107,
  "loss_main_bundle": 0.27252825158213406,
  "loss_turn_bundle": 0.2606724725282563,
  "loss_theta_bundle": 0.0004121238953517107,
  "loss_theta_flat": 0.0004875730501339142,
  "loss_theta_near_flat": 0.001134580670016615,
  "loss_theta_error_excess": 0.00013806147564515088,
  "loss_theta_flat_excess": 0.00025976539880266674,
  "loss_theta_near_flat_excess": 0.0007443322713457864,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011505138113085277,
  "loss_theta_small_neg": 0.00044327178690834563,
  "loss_theta_small_neg_excess": 0.00010699814513400676,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4008893891584244,
  "loss_false_turn_straight": 0.31556981720524324,
  "loss_transition_focal_raw": 1.0529713690038947,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.1253925726049343,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
