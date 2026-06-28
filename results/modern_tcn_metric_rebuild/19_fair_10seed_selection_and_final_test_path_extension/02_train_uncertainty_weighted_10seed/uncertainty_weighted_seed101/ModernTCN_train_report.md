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
| acc_main | 0.9675 |
| acc_turn | 0.5872 |
| acc_turn_pure | 0.6090 |
| acc_turn_transition | 0.4918 |
| main_confidence_mean | 0.9902 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.8429 |
| turn_low_conf_0p60_ratio | 0.1291 |
| turn_low_conf_0p70_ratio | 0.2243 |
| turn_right_recall | 0.6245 |
| turn_straight_recall | 0.5649 |
| turn_left_recall | 0.6023 |
| theta_mae_deg | 0.6092 |
| theta_abs_le_10_p95_abs_err_deg | 1.5222 |
| theta_neg_10_8_p95_abs_err_deg | 1.1722 |
| theta_pos_8_10_p95_abs_err_deg | 2.2707 |
| theta_abs_le_8_p95_abs_err_deg | 1.4931 |
| theta_neg_8_6_p95_abs_err_deg | 1.2909 |
| theta_pos_6_8_p95_abs_err_deg | 1.3541 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3999 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3718 |
| theta_flat_abs_p95_deg | 2.3351 |
| theta_flat_bias_deg | -0.2715 |
| theta_near_flat_abs_p95_deg | 1.6103 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2369 |
| theta_flat_turn_abs_p95_deg | 1.4257 |
| flat_recall | 0.9590 |
| stall_recall | 0.6979 |
| slope_recall | 0.9793 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.7963 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    725,
    1,
    30
  ],
  [
    10,
    67,
    19
  ],
  [
    48,
    9,
    2693
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    499,
    177,
    123
  ],
  [
    405,
    1092,
    436
  ],
  [
    174,
    172,
    524
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.358239 |
| test_loss_turn_bundle_base | 0.348057 |
| test_loss_theta_bundle_base | 0.000141 |
| test_loss_transition_focal_raw | 1.571383 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.833756 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 360.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.5000 | 0.5451 |
| [0.60,0.70) | 26 | 0.4615 | 0.6488 |
| [0.70,0.80) | 24 | 0.5833 | 0.7436 |
| [0.80,0.90) | 26 | 0.1923 | 0.8636 |
| [0.90,1.00) | 3502 | 0.0211 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 465 | 0.5978 | 0.5233 |
| [0.60,0.70) | 343 | 0.5306 | 0.6523 |
| [0.70,0.80) | 420 | 0.5381 | 0.7503 |
| [0.80,0.90) | 504 | 0.4940 | 0.8529 |
| [0.90,1.00) | 1870 | 0.2952 | 0.9754 |


## 验证集最佳点

```json
{
  "loss_total": 0.69609032661247,
  "acc_main": 0.9437077131258458,
  "acc_turn": 0.6433017591339648,
  "acc_turn_pure": 0.653556211078335,
  "acc_turn_transition": 0.59472049689441,
  "false_turn_straight": 0.41683991683991684,
  "flat_recall": 0.939117199391172,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9522696929238985,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.939117199391172,
    0.40476190476190477,
    0.9522696929238985
  ],
  "turn_right_recall": 0.6919431279620853,
  "turn_straight_recall": 0.5831600831600832,
  "turn_left_recall": 0.7238403451995685,
  "recall_turn": [
    0.6919431279620853,
    0.5831600831600832,
    0.7238403451995685
  ],
  "cm_turn": [
    [
      584,
      213,
      47
    ],
    [
      392,
      1122,
      410
    ],
    [
      94,
      162,
      671
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      617,
      0,
      40
    ],
    [
      0,
      17,
      25
    ],
    [
      129,
      14,
      2853
    ]
  ],
  "main_confidence_mean": 0.9723952043802182,
  "main_confidence_error_mean": 0.7938785987306678,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.056562922868741546,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.44623655913978494,
      "mean_confidence": 0.5711552739752651
    },
    {
      "bin": "[0.60,0.70)",
      "n": 23,
      "error_rate": 0.2608695652173913,
      "mean_confidence": 0.6578961646319844
    },
    {
      "bin": "[0.70,0.80)",
      "n": 20,
      "error_rate": 0.55,
      "mean_confidence": 0.7672482761708384
    },
    {
      "bin": "[0.80,0.90)",
      "n": 29,
      "error_rate": 0.41379310344827586,
      "mean_confidence": 0.8534355956683962
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3437,
      "error_rate": 0.027931335466977014,
      "mean_confidence": 0.9984111695202709
    }
  ],
  "turn_confidence_mean": 0.8603726724676368,
  "turn_confidence_error_mean": 0.7895878687539533,
  "turn_low_conf_0p60_ratio": 0.1263870094722598,
  "turn_low_conf_0p70_ratio": 0.1929634641407307,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 467,
      "error_rate": 0.6124197002141327,
      "mean_confidence": 0.4844686158762424
    },
    {
      "bin": "[0.60,0.70)",
      "n": 246,
      "error_rate": 0.532520325203252,
      "mean_confidence": 0.6526353649805094
    },
    {
      "bin": "[0.70,0.80)",
      "n": 317,
      "error_rate": 0.48264984227129337,
      "mean_confidence": 0.7518124601801344
    },
    {
      "bin": "[0.80,0.90)",
      "n": 432,
      "error_rate": 0.4166666666666667,
      "mean_confidence": 0.8503906636964864
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2233,
      "error_rate": 0.25436632333184056,
      "mean_confidence": 0.9792156582062349
    }
  ],
  "theta_mae_rad": 0.013083613477647305,
  "theta_mae_deg": 0.7496358156204224,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.807007786429366,
  "slope_sign_acc": 0.9742677251574049,
  "theta_flat_mae_deg": 1.1052800416946411,
  "theta_flat_abs_p95_deg": 3.7904953956604004,
  "theta_flat_abs_max_deg": 8.600711822509766,
  "theta_flat_bias_deg": 0.22704419493675232,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.396988034248352,
  "theta_near_flat_abs_p95_deg": 3.7915308475494385,
  "theta_near_flat_abs_max_deg": 8.600711822509766,
  "theta_near_flat_bias_deg": 0.5637257099151611,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1070942878723145,
  "theta_flat_turn_abs_p95_deg": 3.7904820442199707,
  "theta_flat_turn_abs_max_deg": 8.600711822509766,
  "theta_flat_turn_bias_deg": -0.009519115090370178,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7496358156204224,
  "theta_slope_control_abs_p95_deg": 9.11798095703125,
  "theta_slope_control_abs_max_deg": 12.316254615783691,
  "theta_slope_control_bias_deg": -0.03801921382546425,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7496358156204224,
  "theta_all_rmse_deg": 1.1377016305923462,
  "theta_all_p95_abs_err_deg": 2.4074079990386963,
  "theta_all_max_abs_err_deg": 8.100712776184082,
  "theta_all_bias_deg": -0.03801920637488365,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6716458797454834,
  "theta_active_abs_ge_2_rmse_deg": 1.0116652250289917,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.070995330810547,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.6100687980651855,
  "theta_active_abs_ge_2_bias_deg": -0.09614560008049011,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7868238091468811,
  "theta_abs_le_8_rmse_deg": 1.1782251596450806,
  "theta_abs_le_8_p95_abs_err_deg": 2.5829720497131348,
  "theta_abs_le_8_max_abs_err_deg": 8.100712776184082,
  "theta_abs_le_8_bias_deg": -0.023247627541422844,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7496358156204224,
  "theta_abs_le_10_rmse_deg": 1.1377016305923462,
  "theta_abs_le_10_p95_abs_err_deg": 2.4074079990386963,
  "theta_abs_le_10_max_abs_err_deg": 8.100712776184082,
  "theta_abs_le_10_bias_deg": -0.03801920637488365,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5665068626403809,
  "theta_pos_8_10_rmse_deg": 0.757084310054779,
  "theta_pos_8_10_p95_abs_err_deg": 1.4935798645019531,
  "theta_pos_8_10_max_abs_err_deg": 4.444910526275635,
  "theta_pos_8_10_bias_deg": -0.35997194051742554,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6194587349891663,
  "theta_neg_10_8_rmse_deg": 1.1087629795074463,
  "theta_neg_10_8_p95_abs_err_deg": 2.2087860107421875,
  "theta_neg_10_8_max_abs_err_deg": 6.6100687980651855,
  "theta_neg_10_8_bias_deg": 0.16379296779632568,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5076930522918701,
  "theta_pos_6_8_rmse_deg": 0.7566760182380676,
  "theta_pos_6_8_p95_abs_err_deg": 1.4727497100830078,
  "theta_pos_6_8_max_abs_err_deg": 3.405866861343384,
  "theta_pos_6_8_bias_deg": -0.2043416053056717,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6777933239936829,
  "theta_neg_8_6_rmse_deg": 1.0236607789993286,
  "theta_neg_8_6_p95_abs_err_deg": 1.970456838607788,
  "theta_neg_8_6_max_abs_err_deg": 6.205629825592041,
  "theta_neg_8_6_bias_deg": -0.11912369728088379,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7302177548408508,
  "theta_neg_4_2_rmse_deg": 0.9817152619361877,
  "theta_neg_4_2_p95_abs_err_deg": 1.7141185998916626,
  "theta_neg_4_2_max_abs_err_deg": 4.713889122009277,
  "theta_neg_4_2_bias_deg": -0.416281133890152,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6151437759399414,
  "theta_neg_2_0p5_rmse_deg": 0.827156126499176,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.596286654472351,
  "theta_neg_2_0p5_max_abs_err_deg": 3.974696397781372,
  "theta_neg_2_0p5_bias_deg": -0.45309314131736755,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3306770324707031,
  "theta_pos_0p5_2_rmse_deg": 1.5818196535110474,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3819339275360107,
  "theta_pos_0p5_2_max_abs_err_deg": 3.8408806324005127,
  "theta_pos_0p5_2_bias_deg": 0.6412919163703918,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3972660830282229,
  "loss_turn": 1.4927947744787626,
  "loss_theta": 0.0003942921963590922,
  "loss_main_bundle_base": 0.3972660830282229,
  "loss_turn_bundle_base": 0.29855895899790713,
  "loss_theta_bundle_base": 0.000265295062805192,
  "loss_main_bundle": 0.3972660830282229,
  "loss_turn_bundle": 0.29855895899790713,
  "loss_theta_bundle": 0.000265295062805192,
  "loss_theta_flat": 0.00026254092510291833,
  "loss_theta_near_flat": 0.0012771027051769349,
  "loss_theta_error_excess": 0.00013973202379306978,
  "loss_theta_flat_excess": 0.00012396678903336288,
  "loss_theta_near_flat_excess": 0.000909086133521025,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.94283372181227e-05,
  "loss_theta_small_neg": 0.0002909470809225361,
  "loss_theta_small_neg_excess": 6.689761613835284e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.37703480477746026,
  "loss_false_turn_straight": 0.31370524966507063,
  "loss_transition_focal_raw": 1.3542933973149776,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.708099442147763,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
