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
  "lambda_theta": 0.6,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.05,
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
  "theta_neg_weight": 1.1,
  "theta_pos_weight": 1.35,
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
  "select_theta_flat_peak_weight": 0.6,
  "select_theta_flat_peak_target_deg": 5.2,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.5,
  "select_theta_edge_p95_target_deg": 1.1,
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
| acc_turn | 0.6011 |
| acc_turn_pure | 0.6203 |
| acc_turn_transition | 0.5171 |
| main_confidence_mean | 0.9899 |
| main_low_conf_0p60_ratio | 0.0092 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.8572 |
| turn_low_conf_0p60_ratio | 0.1160 |
| turn_low_conf_0p70_ratio | 0.2088 |
| turn_right_recall | 0.6308 |
| turn_straight_recall | 0.6125 |
| turn_left_recall | 0.5483 |
| theta_mae_deg | 0.5422 |
| theta_abs_le_10_p95_abs_err_deg | 1.5749 |
| theta_neg_10_8_p95_abs_err_deg | 1.8078 |
| theta_pos_8_10_p95_abs_err_deg | 2.6312 |
| theta_abs_le_8_p95_abs_err_deg | 1.4314 |
| theta_neg_8_6_p95_abs_err_deg | 1.5467 |
| theta_pos_6_8_p95_abs_err_deg | 1.4231 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4106 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4460 |
| theta_flat_abs_p95_deg | 2.6199 |
| theta_flat_bias_deg | -0.0378 |
| theta_near_flat_abs_p95_deg | 1.5850 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1221 |
| theta_flat_turn_abs_p95_deg | 2.0082 |
| flat_recall | 0.9484 |
| stall_recall | 0.6979 |
| slope_recall | 0.9851 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7661 |
| downhill_recall | 0.8014 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    717,
    0,
    39
  ],
  [
    8,
    67,
    21
  ],
  [
    32,
    9,
    2709
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    504,
    193,
    102
  ],
  [
    381,
    1184,
    368
  ],
  [
    143,
    250,
    477
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.327490 |
| test_loss_turn_bundle_base | 0.406844 |
| test_loss_theta_bundle_base | 0.000126 |
| test_loss_transition_focal_raw | 1.921600 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.655769 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 96
- train_seconds: 467.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 33 | 0.3636 | 0.5477 |
| [0.60,0.70) | 17 | 0.3529 | 0.6606 |
| [0.70,0.80) | 24 | 0.3333 | 0.7559 |
| [0.80,0.90) | 30 | 0.4000 | 0.8628 |
| [0.90,1.00) | 3498 | 0.0203 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 418 | 0.6077 | 0.5319 |
| [0.60,0.70) | 334 | 0.5808 | 0.6518 |
| [0.70,0.80) | 391 | 0.4783 | 0.7507 |
| [0.80,0.90) | 444 | 0.4775 | 0.8517 |
| [0.90,1.00) | 2015 | 0.2928 | 0.9807 |


## 验证集最佳点

```json
{
  "loss_total": 0.7322711589694507,
  "acc_main": 0.9415426251691476,
  "acc_turn": 0.6535859269282814,
  "acc_turn_pure": 0.6610947230416256,
  "acc_turn_transition": 0.6180124223602484,
  "false_turn_straight": 0.38357588357588357,
  "flat_recall": 0.9269406392694064,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9532710280373832,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9269406392694064,
    0.3333333333333333,
    0.9532710280373832
  ],
  "turn_right_recall": 0.7085308056872038,
  "turn_straight_recall": 0.6164241164241164,
  "turn_left_recall": 0.6806903991370011,
  "recall_turn": [
    0.7085308056872038,
    0.6164241164241164,
    0.6806903991370011
  ],
  "cm_turn": [
    [
      598,
      229,
      17
    ],
    [
      411,
      1186,
      327
    ],
    [
      114,
      182,
      631
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      609,
      0,
      48
    ],
    [
      0,
      14,
      28
    ],
    [
      128,
      12,
      2856
    ]
  ],
  "main_confidence_mean": 0.9710078538947684,
  "main_confidence_error_mean": 0.7709236017472497,
  "main_low_conf_0p60_ratio": 0.05006765899864682,
  "main_low_conf_0p70_ratio": 0.053585926928281465,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 185,
      "error_rate": 0.4702702702702703,
      "mean_confidence": 0.5312830784391995
    },
    {
      "bin": "[0.60,0.70)",
      "n": 13,
      "error_rate": 0.7692307692307693,
      "mean_confidence": 0.6516833359399785
    },
    {
      "bin": "[0.70,0.80)",
      "n": 31,
      "error_rate": 0.2903225806451613,
      "mean_confidence": 0.765626381585441
    },
    {
      "bin": "[0.80,0.90)",
      "n": 26,
      "error_rate": 0.46153846153846156,
      "mean_confidence": 0.8587423998532147
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3440,
      "error_rate": 0.028488372093023257,
      "mean_confidence": 0.998561932278304
    }
  ],
  "turn_confidence_mean": 0.871991079025092,
  "turn_confidence_error_mean": 0.8083482387974652,
  "turn_low_conf_0p60_ratio": 0.12151556156968876,
  "turn_low_conf_0p70_ratio": 0.19269282814614344,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 449,
      "error_rate": 0.6124721603563474,
      "mean_confidence": 0.5193244820373537
    },
    {
      "bin": "[0.60,0.70)",
      "n": 263,
      "error_rate": 0.4372623574144487,
      "mean_confidence": 0.6511276604888337
    },
    {
      "bin": "[0.70,0.80)",
      "n": 283,
      "error_rate": 0.4734982332155477,
      "mean_confidence": 0.7528081097536681
    },
    {
      "bin": "[0.80,0.90)",
      "n": 362,
      "error_rate": 0.38950276243093923,
      "mean_confidence": 0.8492582568568184
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2338,
      "error_rate": 0.2630453378956373,
      "mean_confidence": 0.9825096603130552
    }
  ],
  "theta_mae_rad": 0.01328785065561533,
  "theta_mae_deg": 0.7613376975059509,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8109010011123471,
  "slope_sign_acc": 0.9646865589926088,
  "theta_flat_mae_deg": 1.1395872831344604,
  "theta_flat_abs_p95_deg": 4.511157989501953,
  "theta_flat_abs_max_deg": 6.366511821746826,
  "theta_flat_bias_deg": 0.5880293846130371,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5371521711349487,
  "theta_near_flat_abs_p95_deg": 4.680031776428223,
  "theta_near_flat_abs_max_deg": 6.306757926940918,
  "theta_near_flat_bias_deg": 1.1777750253677368,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.16953706741333,
  "theta_flat_turn_abs_p95_deg": 4.511157989501953,
  "theta_flat_turn_abs_max_deg": 6.1513566970825195,
  "theta_flat_turn_bias_deg": 0.6374812126159668,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7613376975059509,
  "theta_slope_control_abs_p95_deg": 9.275498390197754,
  "theta_slope_control_abs_max_deg": 12.504636764526367,
  "theta_slope_control_bias_deg": 0.19996953010559082,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7613378167152405,
  "theta_all_rmse_deg": 1.2354196310043335,
  "theta_all_p95_abs_err_deg": 3.011157989501953,
  "theta_all_max_abs_err_deg": 7.606400489807129,
  "theta_all_bias_deg": 0.19996951520442963,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6783905029296875,
  "theta_active_abs_ge_2_rmse_deg": 1.0535908937454224,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.34966778755188,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.606400489807129,
  "theta_active_abs_ge_2_bias_deg": 0.11487096548080444,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8141157031059265,
  "theta_abs_le_8_rmse_deg": 1.2957552671432495,
  "theta_abs_le_8_p95_abs_err_deg": 3.1589674949645996,
  "theta_abs_le_8_max_abs_err_deg": 7.606400489807129,
  "theta_abs_le_8_bias_deg": 0.2190389335155487,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7613378167152405,
  "theta_abs_le_10_rmse_deg": 1.2354196310043335,
  "theta_abs_le_10_p95_abs_err_deg": 3.011157989501953,
  "theta_abs_le_10_max_abs_err_deg": 7.606400489807129,
  "theta_abs_le_10_bias_deg": 0.19996951520442963,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4724408984184265,
  "theta_pos_8_10_rmse_deg": 0.6826345324516296,
  "theta_pos_8_10_p95_abs_err_deg": 1.421794056892395,
  "theta_pos_8_10_max_abs_err_deg": 4.3149027824401855,
  "theta_pos_8_10_bias_deg": -0.10559608042240143,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6060851216316223,
  "theta_neg_10_8_rmse_deg": 1.1424561738967896,
  "theta_neg_10_8_p95_abs_err_deg": 1.859710931777954,
  "theta_neg_10_8_max_abs_err_deg": 7.235263347625732,
  "theta_neg_10_8_bias_deg": 0.34853652119636536,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5583216547966003,
  "theta_pos_6_8_rmse_deg": 0.814758837223053,
  "theta_pos_6_8_p95_abs_err_deg": 1.6859599351882935,
  "theta_pos_6_8_max_abs_err_deg": 3.369448184967041,
  "theta_pos_6_8_bias_deg": -0.06685430556535721,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8030216693878174,
  "theta_neg_8_6_rmse_deg": 1.1757354736328125,
  "theta_neg_8_6_p95_abs_err_deg": 2.2279934883117676,
  "theta_neg_8_6_max_abs_err_deg": 7.606400489807129,
  "theta_neg_8_6_bias_deg": 0.28094425797462463,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7005749940872192,
  "theta_neg_4_2_rmse_deg": 1.025017261505127,
  "theta_neg_4_2_p95_abs_err_deg": 2.061984062194824,
  "theta_neg_4_2_max_abs_err_deg": 5.738806247711182,
  "theta_neg_4_2_bias_deg": -0.22838278114795685,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6579428911209106,
  "theta_neg_2_0p5_rmse_deg": 0.9670937061309814,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.7735960483551025,
  "theta_neg_2_0p5_max_abs_err_deg": 5.621267795562744,
  "theta_neg_2_0p5_bias_deg": -0.14665447175502777,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.130020022392273,
  "theta_pos_0p5_2_rmse_deg": 1.6495709419250488,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.011157989501953,
  "theta_pos_0p5_2_max_abs_err_deg": 4.594539642333984,
  "theta_pos_0p5_2_bias_deg": 0.5223307013511658,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.412787468265616,
  "loss_turn": 1.5958398657012858,
  "loss_theta": 0.000455049997830766,
  "loss_main_bundle_base": 0.412787468265616,
  "loss_turn_bundle_base": 0.31916797636165023,
  "loss_theta_bundle_base": 0.0003157200711808912,
  "loss_main_bundle": 0.412787468265616,
  "loss_turn_bundle": 0.31916797636165023,
  "loss_theta_bundle": 0.0003157200711808912,
  "loss_theta_flat": 0.00023224442111842897,
  "loss_theta_near_flat": 0.0016463628373989717,
  "loss_theta_error_excess": 0.00018782742932396,
  "loss_theta_flat_excess": 0.0001542914473563009,
  "loss_theta_near_flat_excess": 0.0012521936909008283,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010858721568684581,
  "loss_theta_small_neg": 0.00031367858127641704,
  "loss_theta_small_neg_excess": 8.812605709603739e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.33081406187946644,
  "loss_false_turn_straight": 0.29455841113088577,
  "loss_transition_focal_raw": 1.3782650748834882,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.217179852861588,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
