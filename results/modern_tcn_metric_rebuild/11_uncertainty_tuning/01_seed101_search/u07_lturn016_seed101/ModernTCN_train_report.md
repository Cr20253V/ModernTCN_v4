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
  "lambda_turn": 0.16,
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
| acc_main | 0.9731 |
| acc_turn | 0.5530 |
| acc_turn_pure | 0.5725 |
| acc_turn_transition | 0.4680 |
| main_confidence_mean | 0.9886 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0125 |
| turn_confidence_mean | 0.8084 |
| turn_low_conf_0p60_ratio | 0.1707 |
| turn_low_conf_0p70_ratio | 0.2807 |
| turn_right_recall | 0.6120 |
| turn_straight_recall | 0.5142 |
| turn_left_recall | 0.5851 |
| theta_mae_deg | 0.8172 |
| theta_abs_le_10_p95_abs_err_deg | 2.1167 |
| theta_neg_10_8_p95_abs_err_deg | 2.1242 |
| theta_pos_8_10_p95_abs_err_deg | 3.7240 |
| theta_abs_le_8_p95_abs_err_deg | 1.9336 |
| theta_neg_8_6_p95_abs_err_deg | 1.9084 |
| theta_pos_6_8_p95_abs_err_deg | 1.8665 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7281 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5208 |
| theta_flat_abs_p95_deg | 2.5199 |
| theta_flat_bias_deg | -0.0660 |
| theta_near_flat_abs_p95_deg | 1.9856 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1166 |
| theta_flat_turn_abs_p95_deg | 1.6922 |
| flat_recall | 0.9669 |
| stall_recall | 0.6979 |
| slope_recall | 0.9844 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7678 |
| downhill_recall | 0.7906 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    731,
    0,
    25
  ],
  [
    10,
    67,
    19
  ],
  [
    36,
    7,
    2707
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    489,
    160,
    150
  ],
  [
    453,
    994,
    486
  ],
  [
    211,
    150,
    509
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.296620 |
| test_loss_turn_bundle_base | 0.240674 |
| test_loss_theta_bundle_base | 0.000235 |
| test_loss_transition_focal_raw | 1.276106 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.341299 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 60
- train_seconds: 307.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.5500 | 0.5471 |
| [0.60,0.70) | 25 | 0.2800 | 0.6424 |
| [0.70,0.80) | 34 | 0.1471 | 0.7441 |
| [0.80,0.90) | 33 | 0.2727 | 0.8498 |
| [0.90,1.00) | 3490 | 0.0186 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 615 | 0.6033 | 0.5158 |
| [0.60,0.70) | 396 | 0.5429 | 0.6493 |
| [0.70,0.80) | 492 | 0.5549 | 0.7483 |
| [0.80,0.90) | 569 | 0.4921 | 0.8520 |
| [0.90,1.00) | 1530 | 0.3078 | 0.9703 |


## 验证集最佳点

```json
{
  "loss_total": 0.5568716883820675,
  "acc_main": 0.9485791610284168,
  "acc_turn": 0.6064952638700947,
  "acc_turn_pure": 0.6250409701737135,
  "acc_turn_transition": 0.5186335403726708,
  "false_turn_straight": 0.48544698544698545,
  "flat_recall": 0.9680365296803652,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.951935914552737,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9680365296803652,
    0.40476190476190477,
    0.951935914552737
  ],
  "turn_right_recall": 0.6421800947867299,
  "turn_straight_recall": 0.5145530145530145,
  "turn_left_recall": 0.7648327939590076,
  "recall_turn": [
    0.6421800947867299,
    0.5145530145530145,
    0.7648327939590076
  ],
  "cm_turn": [
    [
      542,
      190,
      112
    ],
    [
      420,
      990,
      514
    ],
    [
      76,
      142,
      709
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      636,
      0,
      21
    ],
    [
      0,
      17,
      25
    ],
    [
      135,
      9,
      2852
    ]
  ],
  "main_confidence_mean": 0.9665870394699477,
  "main_confidence_error_mean": 0.740133961357175,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.058186738836265225,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4639175257731959,
      "mean_confidence": 0.5071745528399773
    },
    {
      "bin": "[0.60,0.70)",
      "n": 21,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6562666948278262
    },
    {
      "bin": "[0.70,0.80)",
      "n": 24,
      "error_rate": 0.25,
      "mean_confidence": 0.7651701434194645
    },
    {
      "bin": "[0.80,0.90)",
      "n": 46,
      "error_rate": 0.06521739130434782,
      "mean_confidence": 0.859487418104181
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3410,
      "error_rate": 0.02463343108504399,
      "mean_confidence": 0.9974971091859994
    }
  ],
  "turn_confidence_mean": 0.8315161617651063,
  "turn_confidence_error_mean": 0.7720894946174589,
  "turn_low_conf_0p60_ratio": 0.11393775372124493,
  "turn_low_conf_0p70_ratio": 0.2635994587280108,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 421,
      "error_rate": 0.5534441805225653,
      "mean_confidence": 0.527001769147997
    },
    {
      "bin": "[0.60,0.70)",
      "n": 553,
      "error_rate": 0.5822784810126582,
      "mean_confidence": 0.6464757426226635
    },
    {
      "bin": "[0.70,0.80)",
      "n": 430,
      "error_rate": 0.4883720930232558,
      "mean_confidence": 0.7509343639818634
    },
    {
      "bin": "[0.80,0.90)",
      "n": 526,
      "error_rate": 0.4847908745247148,
      "mean_confidence": 0.8515630393761533
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1765,
      "error_rate": 0.24589235127478754,
      "mean_confidence": 0.9757843920772634
    }
  ],
  "theta_mae_rad": 0.016613608226180077,
  "theta_mae_deg": 0.9518895745277405,
  "uphill_recall": 0.7827493261455526,
  "downhill_recall": 0.7903225806451613,
  "slope_sign_acc": 0.9674240350396934,
  "theta_flat_mae_deg": 1.0594285726547241,
  "theta_flat_abs_p95_deg": 3.33575439453125,
  "theta_flat_abs_max_deg": 8.173174858093262,
  "theta_flat_bias_deg": 0.3549199402332306,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.37559175491333,
  "theta_near_flat_abs_p95_deg": 3.3954215049743652,
  "theta_near_flat_abs_max_deg": 8.173174858093262,
  "theta_near_flat_bias_deg": 0.6357747912406921,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1722458600997925,
  "theta_flat_turn_abs_p95_deg": 3.335754156112671,
  "theta_flat_turn_abs_max_deg": 8.173174858093262,
  "theta_flat_turn_bias_deg": 0.12253572046756744,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9518895745277405,
  "theta_slope_control_abs_p95_deg": 9.706878662109375,
  "theta_slope_control_abs_max_deg": 12.693147659301758,
  "theta_slope_control_bias_deg": -0.34783831238746643,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9518896341323853,
  "theta_all_rmse_deg": 1.2767812013626099,
  "theta_all_p95_abs_err_deg": 2.511550188064575,
  "theta_all_max_abs_err_deg": 7.673174858093262,
  "theta_all_bias_deg": -0.34783828258514404,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9283072352409363,
  "theta_active_abs_ge_2_rmse_deg": 1.2259244918823242,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3949129581451416,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.783327579498291,
  "theta_active_abs_ge_2_bias_deg": -0.501947820186615,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9385818839073181,
  "theta_abs_le_8_rmse_deg": 1.2806657552719116,
  "theta_abs_le_8_p95_abs_err_deg": 2.618204116821289,
  "theta_abs_le_8_max_abs_err_deg": 7.673174858093262,
  "theta_abs_le_8_bias_deg": -0.24462293088436127,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9518896341323853,
  "theta_abs_le_10_rmse_deg": 1.2767812013626099,
  "theta_abs_le_10_p95_abs_err_deg": 2.511550188064575,
  "theta_abs_le_10_max_abs_err_deg": 7.673174858093262,
  "theta_abs_le_10_bias_deg": -0.34783828258514404,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9505264163017273,
  "theta_pos_8_10_rmse_deg": 1.1329872608184814,
  "theta_pos_8_10_p95_abs_err_deg": 2.0684714317321777,
  "theta_pos_8_10_max_abs_err_deg": 5.0277581214904785,
  "theta_pos_8_10_bias_deg": -0.850616455078125,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.0665267705917358,
  "theta_neg_10_8_rmse_deg": 1.3777257204055786,
  "theta_neg_10_8_p95_abs_err_deg": 2.555319309234619,
  "theta_neg_10_8_max_abs_err_deg": 5.7055487632751465,
  "theta_neg_10_8_bias_deg": -0.7147380113601685,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8323450684547424,
  "theta_pos_6_8_rmse_deg": 1.0264480113983154,
  "theta_pos_6_8_p95_abs_err_deg": 2.0041913986206055,
  "theta_pos_6_8_max_abs_err_deg": 3.7260520458221436,
  "theta_pos_6_8_bias_deg": -0.6284335851669312,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0058479309082031,
  "theta_neg_8_6_rmse_deg": 1.3441201448440552,
  "theta_neg_8_6_p95_abs_err_deg": 2.411282777786255,
  "theta_neg_8_6_max_abs_err_deg": 5.686665058135986,
  "theta_neg_8_6_bias_deg": -0.700599193572998,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8817348480224609,
  "theta_neg_4_2_rmse_deg": 1.1648701429367065,
  "theta_neg_4_2_p95_abs_err_deg": 2.307713031768799,
  "theta_neg_4_2_max_abs_err_deg": 4.591091632843018,
  "theta_neg_4_2_bias_deg": -0.4642850458621979,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6001582145690918,
  "theta_neg_2_0p5_rmse_deg": 0.8305898904800415,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6732401847839355,
  "theta_neg_2_0p5_max_abs_err_deg": 4.011911392211914,
  "theta_neg_2_0p5_bias_deg": -0.13998077809810638,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1245198249816895,
  "theta_pos_0p5_2_rmse_deg": 1.3591747283935547,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.2070980072021484,
  "theta_pos_0p5_2_max_abs_err_deg": 4.063088893890381,
  "theta_pos_0p5_2_bias_deg": 0.5818457007408142,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3427545316971042,
  "loss_turn": 1.3362645716402624,
  "loss_theta": 0.0004964668145252037,
  "loss_main_bundle_base": 0.3427545316971042,
  "loss_turn_bundle_base": 0.21380232747175373,
  "loss_theta_bundle_base": 0.00031484511852767244,
  "loss_main_bundle": 0.3427545316971042,
  "loss_turn_bundle": 0.21380232747175373,
  "loss_theta_bundle": 0.00031484511852767244,
  "loss_theta_flat": 0.00017825539199983845,
  "loss_theta_near_flat": 0.001130023100495298,
  "loss_theta_error_excess": 0.00015076719037306286,
  "loss_theta_flat_excess": 9.063671014123755e-05,
  "loss_theta_near_flat_excess": 0.0007623181742942402,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001285935630873778,
  "loss_theta_small_neg": 0.00041469466761926614,
  "loss_theta_small_neg_excess": 0.00010971584502170909,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.45269525801215993,
  "loss_false_turn_straight": 0.34955322868285227,
  "loss_transition_focal_raw": 1.142529997886921,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.894416282339996,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
