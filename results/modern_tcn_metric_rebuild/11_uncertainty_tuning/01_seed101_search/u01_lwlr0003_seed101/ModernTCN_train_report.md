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
| acc_main | 0.9664 |
| acc_turn | 0.5519 |
| acc_turn_pure | 0.5667 |
| acc_turn_transition | 0.4873 |
| main_confidence_mean | 0.9858 |
| main_low_conf_0p60_ratio | 0.0081 |
| main_low_conf_0p70_ratio | 0.0192 |
| turn_confidence_mean | 0.7863 |
| turn_low_conf_0p60_ratio | 0.2177 |
| turn_low_conf_0p70_ratio | 0.3445 |
| turn_right_recall | 0.6583 |
| turn_straight_recall | 0.4739 |
| turn_left_recall | 0.6276 |
| theta_mae_deg | 0.7801 |
| theta_abs_le_10_p95_abs_err_deg | 2.1203 |
| theta_neg_10_8_p95_abs_err_deg | 1.9900 |
| theta_pos_8_10_p95_abs_err_deg | 3.3943 |
| theta_abs_le_8_p95_abs_err_deg | 1.8575 |
| theta_neg_8_6_p95_abs_err_deg | 1.6909 |
| theta_pos_6_8_p95_abs_err_deg | 2.3133 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8111 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8504 |
| theta_flat_abs_p95_deg | 2.4951 |
| theta_flat_bias_deg | -0.0376 |
| theta_near_flat_abs_p95_deg | 1.9085 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0115 |
| theta_flat_turn_abs_p95_deg | 2.0101 |
| flat_recall | 0.9630 |
| stall_recall | 0.6875 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7575 |
| downhill_recall | 0.7911 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    728,
    0,
    28
  ],
  [
    10,
    66,
    20
  ],
  [
    57,
    6,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    526,
    146,
    127
  ],
  [
    489,
    916,
    528
  ],
  [
    185,
    139,
    546
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.271398 |
| test_loss_turn_bundle_base | 0.272761 |
| test_loss_theta_bundle_base | 0.000229 |
| test_loss_transition_focal_raw | 1.116412 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.957308 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 44
- train_seconds: 239.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 29 | 0.4138 | 0.5481 |
| [0.60,0.70) | 40 | 0.6500 | 0.6370 |
| [0.70,0.80) | 23 | 0.3913 | 0.7618 |
| [0.80,0.90) | 41 | 0.1707 | 0.8661 |
| [0.90,1.00) | 3469 | 0.0193 | 0.9964 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 784 | 0.5663 | 0.5177 |
| [0.60,0.70) | 457 | 0.5821 | 0.6503 |
| [0.70,0.80) | 433 | 0.5312 | 0.7496 |
| [0.80,0.90) | 542 | 0.4760 | 0.8516 |
| [0.90,1.00) | 1386 | 0.3001 | 0.9689 |


## 验证集最佳点

```json
{
  "loss_total": 0.49187865902509675,
  "acc_main": 0.9477672530446549,
  "acc_turn": 0.6002706359945873,
  "acc_turn_pure": 0.618813503769256,
  "acc_turn_transition": 0.5124223602484472,
  "false_turn_straight": 0.5280665280665281,
  "flat_recall": 0.9497716894977168,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9497716894977168,
    0.47619047619047616,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6670616113744076,
  "turn_straight_recall": 0.47193347193347196,
  "turn_left_recall": 0.8058252427184466,
  "recall_turn": [
    0.6670616113744076,
    0.47193347193347196,
    0.8058252427184466
  ],
  "cm_turn": [
    [
      563,
      178,
      103
    ],
    [
      452,
      908,
      564
    ],
    [
      64,
      116,
      747
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      624,
      0,
      33
    ],
    [
      0,
      20,
      22
    ],
    [
      128,
      10,
      2858
    ]
  ],
  "main_confidence_mean": 0.9693119590225344,
  "main_confidence_error_mean": 0.7795241175233113,
  "main_low_conf_0p60_ratio": 0.0062246278755074425,
  "main_low_conf_0p70_ratio": 0.058457374830852504,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 23,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.5494410494835391
    },
    {
      "bin": "[0.60,0.70)",
      "n": 193,
      "error_rate": 0.45595854922279794,
      "mean_confidence": 0.6220232651363441
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.20588235294117646,
      "mean_confidence": 0.7478610180871665
    },
    {
      "bin": "[0.80,0.90)",
      "n": 66,
      "error_rate": 0.16666666666666666,
      "mean_confidence": 0.8553955921943697
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3379,
      "error_rate": 0.022491861497484462,
      "mean_confidence": 0.9964595059423016
    }
  ],
  "turn_confidence_mean": 0.8087707750516098,
  "turn_confidence_error_mean": 0.7258349359557534,
  "turn_low_conf_0p60_ratio": 0.18430311231393776,
  "turn_low_conf_0p70_ratio": 0.2855209742895805,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 681,
      "error_rate": 0.644640234948605,
      "mean_confidence": 0.5011434225802222
    },
    {
      "bin": "[0.60,0.70)",
      "n": 374,
      "error_rate": 0.5882352941176471,
      "mean_confidence": 0.6498336254743379
    },
    {
      "bin": "[0.70,0.80)",
      "n": 454,
      "error_rate": 0.5110132158590308,
      "mean_confidence": 0.7536852310119844
    },
    {
      "bin": "[0.80,0.90)",
      "n": 523,
      "error_rate": 0.4608030592734226,
      "mean_confidence": 0.8519705568575355
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1663,
      "error_rate": 0.2074564040889958,
      "mean_confidence": 0.9719409927812583
    }
  ],
  "theta_mae_rad": 0.014782807789742947,
  "theta_mae_deg": 0.8469924330711365,
  "uphill_recall": 0.7805929919137466,
  "downhill_recall": 0.8025583982202447,
  "slope_sign_acc": 0.9709827539009034,
  "theta_flat_mae_deg": 1.0312949419021606,
  "theta_flat_abs_p95_deg": 3.4977805614471436,
  "theta_flat_abs_max_deg": 12.832765579223633,
  "theta_flat_bias_deg": 0.06131088361144066,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3648595809936523,
  "theta_near_flat_abs_p95_deg": 4.457904815673828,
  "theta_near_flat_abs_max_deg": 12.832765579223633,
  "theta_near_flat_bias_deg": 0.3264857828617096,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.398692011833191,
  "theta_flat_turn_abs_p95_deg": 6.527204513549805,
  "theta_flat_turn_abs_max_deg": 12.832765579223633,
  "theta_flat_turn_bias_deg": -0.3027290999889374,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8469924330711365,
  "theta_slope_control_abs_p95_deg": 9.036840438842773,
  "theta_slope_control_abs_max_deg": 12.832765579223633,
  "theta_slope_control_bias_deg": 0.046131670475006104,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8469924926757812,
  "theta_all_rmse_deg": 1.2657275199890137,
  "theta_all_p95_abs_err_deg": 2.587372303009033,
  "theta_all_max_abs_err_deg": 12.332765579223633,
  "theta_all_bias_deg": 0.046131666749715805,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8065763115882874,
  "theta_active_abs_ge_2_rmse_deg": 1.1646982431411743,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.524559497833252,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.345560550689697,
  "theta_active_abs_ge_2_bias_deg": 0.04280299320816994,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8432115316390991,
  "theta_abs_le_8_rmse_deg": 1.2695175409317017,
  "theta_abs_le_8_p95_abs_err_deg": 2.667431354522705,
  "theta_abs_le_8_max_abs_err_deg": 12.332765579223633,
  "theta_abs_le_8_bias_deg": 0.022654039785265923,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8469924926757812,
  "theta_abs_le_10_rmse_deg": 1.2657275199890137,
  "theta_abs_le_10_p95_abs_err_deg": 2.587372303009033,
  "theta_abs_le_10_max_abs_err_deg": 12.332765579223633,
  "theta_abs_le_10_bias_deg": 0.046131666749715805,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7807724475860596,
  "theta_pos_8_10_rmse_deg": 1.0292493104934692,
  "theta_pos_8_10_p95_abs_err_deg": 2.14953351020813,
  "theta_pos_8_10_max_abs_err_deg": 3.5774919986724854,
  "theta_pos_8_10_bias_deg": -0.3683896064758301,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.9465333819389343,
  "theta_neg_10_8_rmse_deg": 1.439581036567688,
  "theta_neg_10_8_p95_abs_err_deg": 2.9254133701324463,
  "theta_neg_10_8_max_abs_err_deg": 7.345560550689697,
  "theta_neg_10_8_bias_deg": 0.6676172018051147,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6808028221130371,
  "theta_pos_6_8_rmse_deg": 0.904822051525116,
  "theta_pos_6_8_p95_abs_err_deg": 1.7886791229248047,
  "theta_pos_6_8_max_abs_err_deg": 3.0434672832489014,
  "theta_pos_6_8_bias_deg": -0.2059151977300644,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7355377078056335,
  "theta_neg_8_6_rmse_deg": 1.112391471862793,
  "theta_neg_8_6_p95_abs_err_deg": 2.403623104095459,
  "theta_neg_8_6_max_abs_err_deg": 6.269460678100586,
  "theta_neg_8_6_bias_deg": 0.29136762022972107,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7740668654441833,
  "theta_neg_4_2_rmse_deg": 1.0620285272598267,
  "theta_neg_4_2_p95_abs_err_deg": 2.2087676525115967,
  "theta_neg_4_2_max_abs_err_deg": 3.837249517440796,
  "theta_neg_4_2_bias_deg": 0.02494649589061737,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8405337929725647,
  "theta_neg_2_0p5_rmse_deg": 1.1846057176589966,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.327333927154541,
  "theta_neg_2_0p5_max_abs_err_deg": 4.1892194747924805,
  "theta_neg_2_0p5_bias_deg": -0.45298057794570923,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.7863919138908386,
  "theta_pos_0p5_2_rmse_deg": 1.076533317565918,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.859070062637329,
  "theta_pos_0p5_2_max_abs_err_deg": 4.763340950012207,
  "theta_pos_0p5_2_bias_deg": 0.3865659832954407,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2556522209605603,
  "loss_turn": 1.1795568103880618,
  "loss_theta": 0.0004880131850383309,
  "loss_main_bundle_base": 0.2556522209605603,
  "loss_turn_bundle_base": 0.23591136381897132,
  "loss_theta_bundle_base": 0.0003150690009210042,
  "loss_main_bundle": 0.2556522209605603,
  "loss_turn_bundle": 0.23591136381897132,
  "loss_theta_bundle": 0.0003150690009210042,
  "loss_theta_flat": 0.00019755312946761477,
  "loss_theta_near_flat": 0.0015090228541072392,
  "loss_theta_error_excess": 0.00018628776903328498,
  "loss_theta_flat_excess": 8.093196134742948e-05,
  "loss_theta_near_flat_excess": 0.0011445264323174712,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00013640982279486586,
  "loss_theta_small_neg": 0.0003396073695434779,
  "loss_theta_small_neg_excess": 8.21954745727469e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4729540583406637,
  "loss_false_turn_straight": 0.3689829790705112,
  "loss_transition_focal_raw": 1.0195392987079646,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.9545610755687393,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
