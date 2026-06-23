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
  "select_theta_flat_p95_weight": 0.55,
  "select_theta_flat_p95_target_deg": 0.6,
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
  "select_theta_flat_bias_weight": 0.45,
  "select_theta_flat_bias_target_deg": 0.1
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9617 |
| acc_turn | 0.5927 |
| acc_turn_pure | 0.6131 |
| acc_turn_transition | 0.5037 |
| main_confidence_mean | 0.9871 |
| main_low_conf_0p60_ratio | 0.0086 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.7733 |
| turn_low_conf_0p60_ratio | 0.2460 |
| turn_low_conf_0p70_ratio | 0.3573 |
| turn_right_recall | 0.5594 |
| turn_straight_recall | 0.5970 |
| turn_left_recall | 0.6138 |
| theta_mae_deg | 0.8518 |
| theta_abs_le_10_p95_abs_err_deg | 2.0856 |
| theta_neg_10_8_p95_abs_err_deg | 1.9156 |
| theta_pos_8_10_p95_abs_err_deg | 3.1783 |
| theta_abs_le_8_p95_abs_err_deg | 1.9824 |
| theta_neg_8_6_p95_abs_err_deg | 1.9733 |
| theta_pos_6_8_p95_abs_err_deg | 1.8957 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7924 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.4132 |
| theta_flat_abs_p95_deg | 3.1402 |
| theta_flat_bias_deg | 0.0823 |
| theta_near_flat_abs_p95_deg | 2.3038 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2361 |
| theta_flat_turn_abs_p95_deg | 2.2572 |
| flat_recall | 0.9392 |
| stall_recall | 0.6979 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7563 |
| downhill_recall | 0.8025 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    710,
    0,
    46
  ],
  [
    11,
    67,
    18
  ],
  [
    54,
    9,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    447,
    213,
    139
  ],
  [
    344,
    1154,
    435
  ],
  [
    119,
    217,
    534
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.342457 |
| test_loss_turn_bundle_base | 0.274965 |
| test_loss_theta_bundle_base | 0.000270 |
| test_loss_transition_focal_raw | 1.169752 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.262776 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 47
- train_seconds: 261.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 31 | 0.2903 | 0.5391 |
| [0.60,0.70) | 18 | 0.5000 | 0.6559 |
| [0.70,0.80) | 26 | 0.3462 | 0.7449 |
| [0.80,0.90) | 53 | 0.3208 | 0.8536 |
| [0.90,1.00) | 3474 | 0.0271 | 0.9967 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 886 | 0.5226 | 0.5060 |
| [0.60,0.70) | 401 | 0.5112 | 0.6460 |
| [0.70,0.80) | 454 | 0.4559 | 0.7506 |
| [0.80,0.90) | 574 | 0.4443 | 0.8509 |
| [0.90,1.00) | 1287 | 0.2618 | 0.9703 |


## 验证集最佳点

```json
{
  "loss_total": 0.5283441141590537,
  "acc_main": 0.9499323410013532,
  "acc_turn": 0.6097428958051421,
  "acc_turn_pure": 0.621107833497214,
  "acc_turn_transition": 0.5559006211180124,
  "false_turn_straight": 0.4371101871101871,
  "flat_recall": 0.9710806697108066,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9529372496662216,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9710806697108066,
    0.40476190476190477,
    0.9529372496662216
  ],
  "turn_right_recall": 0.566350710900474,
  "turn_straight_recall": 0.5628898128898129,
  "turn_left_recall": 0.7464940668824164,
  "recall_turn": [
    0.566350710900474,
    0.5628898128898129,
    0.7464940668824164
  ],
  "cm_turn": [
    [
      478,
      236,
      130
    ],
    [
      322,
      1083,
      519
    ],
    [
      59,
      176,
      692
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      638,
      0,
      19
    ],
    [
      0,
      17,
      25
    ],
    [
      123,
      18,
      2855
    ]
  ],
  "main_confidence_mean": 0.9717031000593855,
  "main_confidence_error_mean": 0.7815101556226787,
  "main_low_conf_0p60_ratio": 0.04871447902571042,
  "main_low_conf_0p70_ratio": 0.0516914749661705,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 180,
      "error_rate": 0.46111111111111114,
      "mean_confidence": 0.5920654891981038
    },
    {
      "bin": "[0.60,0.70)",
      "n": 11,
      "error_rate": 0.36363636363636365,
      "mean_confidence": 0.6543007998839917
    },
    {
      "bin": "[0.70,0.80)",
      "n": 32,
      "error_rate": 0.375,
      "mean_confidence": 0.7510815537729366
    },
    {
      "bin": "[0.80,0.90)",
      "n": 57,
      "error_rate": 0.14035087719298245,
      "mean_confidence": 0.8518065597616897
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3415,
      "error_rate": 0.022840409956076134,
      "mean_confidence": 0.9968041798646842
    }
  ],
  "turn_confidence_mean": 0.803561205691087,
  "turn_confidence_error_mean": 0.7250981930957902,
  "turn_low_conf_0p60_ratio": 0.19783491204330175,
  "turn_low_conf_0p70_ratio": 0.3023004059539919,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 731,
      "error_rate": 0.627906976744186,
      "mean_confidence": 0.4988613984700655
    },
    {
      "bin": "[0.60,0.70)",
      "n": 386,
      "error_rate": 0.4792746113989637,
      "mean_confidence": 0.6502939265812785
    },
    {
      "bin": "[0.70,0.80)",
      "n": 411,
      "error_rate": 0.46715328467153283,
      "mean_confidence": 0.7531445567201708
    },
    {
      "bin": "[0.80,0.90)",
      "n": 566,
      "error_rate": 0.46113074204946997,
      "mean_confidence": 0.8558175313603735
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1601,
      "error_rate": 0.2154903185509057,
      "mean_confidence": 0.9741051727199334
    }
  ],
  "theta_mae_rad": 0.015846360474824905,
  "theta_mae_deg": 0.907929539680481,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.796440489432703,
  "slope_sign_acc": 0.9679715302491103,
  "theta_flat_mae_deg": 1.157240867614746,
  "theta_flat_abs_p95_deg": 3.349926471710205,
  "theta_flat_abs_max_deg": 11.764995574951172,
  "theta_flat_bias_deg": 0.20803503692150116,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.48896062374115,
  "theta_near_flat_abs_p95_deg": 3.5398478507995605,
  "theta_near_flat_abs_max_deg": 11.764995574951172,
  "theta_near_flat_bias_deg": 0.3800593316555023,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.366631031036377,
  "theta_flat_turn_abs_p95_deg": 6.0209527015686035,
  "theta_flat_turn_abs_max_deg": 11.764995574951172,
  "theta_flat_turn_bias_deg": -0.24814769625663757,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.907929539680481,
  "theta_slope_control_abs_p95_deg": 9.781718254089355,
  "theta_slope_control_abs_max_deg": 12.39073371887207,
  "theta_slope_control_bias_deg": -0.022989582270383835,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9079294204711914,
  "theta_all_rmse_deg": 1.3337607383728027,
  "theta_all_p95_abs_err_deg": 2.617485523223877,
  "theta_all_max_abs_err_deg": 11.264996528625488,
  "theta_all_bias_deg": -0.022989580407738686,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8532572984695435,
  "theta_active_abs_ge_2_rmse_deg": 1.2451430559158325,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.3304758071899414,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.164521217346191,
  "theta_active_abs_ge_2_bias_deg": -0.07365152984857559,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9351192116737366,
  "theta_abs_le_8_rmse_deg": 1.3714983463287354,
  "theta_abs_le_8_p95_abs_err_deg": 2.6174991130828857,
  "theta_abs_le_8_max_abs_err_deg": 11.264996528625488,
  "theta_abs_le_8_bias_deg": 0.02204093150794506,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9079294204711914,
  "theta_abs_le_10_rmse_deg": 1.3337607383728027,
  "theta_abs_le_10_p95_abs_err_deg": 2.617485523223877,
  "theta_abs_le_10_max_abs_err_deg": 11.264996528625488,
  "theta_abs_le_10_bias_deg": -0.022989580407738686,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5220201015472412,
  "theta_pos_8_10_rmse_deg": 0.777005136013031,
  "theta_pos_8_10_p95_abs_err_deg": 1.5231574773788452,
  "theta_pos_8_10_max_abs_err_deg": 3.747718095779419,
  "theta_pos_8_10_bias_deg": -0.022888751700520515,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.069124460220337,
  "theta_neg_10_8_rmse_deg": 1.451076626777649,
  "theta_neg_10_8_p95_abs_err_deg": 2.7408976554870605,
  "theta_neg_10_8_max_abs_err_deg": 6.883883476257324,
  "theta_neg_10_8_bias_deg": -0.4063057601451874,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6351467370986938,
  "theta_pos_6_8_rmse_deg": 0.9246120452880859,
  "theta_pos_6_8_p95_abs_err_deg": 1.8926384449005127,
  "theta_pos_6_8_max_abs_err_deg": 3.9087488651275635,
  "theta_pos_6_8_bias_deg": 0.22354888916015625,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0020911693572998,
  "theta_neg_8_6_rmse_deg": 1.3023905754089355,
  "theta_neg_8_6_p95_abs_err_deg": 2.414949417114258,
  "theta_neg_8_6_max_abs_err_deg": 5.767034530639648,
  "theta_neg_8_6_bias_deg": -0.37715741991996765,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.870671272277832,
  "theta_neg_4_2_rmse_deg": 1.2086479663848877,
  "theta_neg_4_2_p95_abs_err_deg": 2.356015920639038,
  "theta_neg_4_2_max_abs_err_deg": 6.612084865570068,
  "theta_neg_4_2_bias_deg": -0.23449291288852692,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7881883978843689,
  "theta_neg_2_0p5_rmse_deg": 1.0898131132125854,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.39560866355896,
  "theta_neg_2_0p5_max_abs_err_deg": 4.916449069976807,
  "theta_neg_2_0p5_bias_deg": -0.36800533533096313,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.140632152557373,
  "theta_pos_0p5_2_rmse_deg": 1.3796550035476685,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.087015151977539,
  "theta_pos_0p5_2_max_abs_err_deg": 4.976288795471191,
  "theta_pos_0p5_2_bias_deg": 0.8101434111595154,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.26472331204014315,
  "loss_turn": 1.3162990120331555,
  "loss_theta": 0.0005419675994561091,
  "loss_main_bundle_base": 0.26472331204014315,
  "loss_turn_bundle_base": 0.26325980632972973,
  "loss_theta_bundle_base": 0.0003609943261756959,
  "loss_main_bundle": 0.26472331204014315,
  "loss_turn_bundle": 0.26325980632972973,
  "loss_theta_bundle": 0.0003609943261756959,
  "loss_theta_flat": 0.00028992803021035094,
  "loss_theta_near_flat": 0.0014520311689682314,
  "loss_theta_error_excess": 0.0002136706774714069,
  "loss_theta_flat_excess": 0.0001232228249264818,
  "loss_theta_near_flat_excess": 0.0010675550202797488,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00017437245074142254,
  "loss_theta_small_neg": 0.0004397976689522075,
  "loss_theta_small_neg_excess": 0.00013978771869463692,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.377631892491742,
  "loss_false_turn_straight": 0.2985929919515153,
  "loss_transition_focal_raw": 1.1079541241203175,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.8799142546798953,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
