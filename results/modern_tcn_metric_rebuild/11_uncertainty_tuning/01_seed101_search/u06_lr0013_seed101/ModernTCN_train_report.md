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
| acc_main | 0.9697 |
| acc_turn | 0.5775 |
| acc_turn_pure | 0.5923 |
| acc_turn_transition | 0.5127 |
| main_confidence_mean | 0.9885 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0167 |
| turn_confidence_mean | 0.8250 |
| turn_low_conf_0p60_ratio | 0.1557 |
| turn_low_conf_0p70_ratio | 0.2593 |
| turn_right_recall | 0.6233 |
| turn_straight_recall | 0.5970 |
| turn_left_recall | 0.4920 |
| theta_mae_deg | 0.8149 |
| theta_abs_le_10_p95_abs_err_deg | 2.0140 |
| theta_neg_10_8_p95_abs_err_deg | 1.2673 |
| theta_pos_8_10_p95_abs_err_deg | 2.6418 |
| theta_abs_le_8_p95_abs_err_deg | 1.9742 |
| theta_neg_8_6_p95_abs_err_deg | 1.4667 |
| theta_pos_6_8_p95_abs_err_deg | 1.9578 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7236 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9782 |
| theta_flat_abs_p95_deg | 2.8363 |
| theta_flat_bias_deg | -0.7236 |
| theta_near_flat_abs_p95_deg | 2.4439 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.9828 |
| theta_flat_turn_abs_p95_deg | 2.3342 |
| flat_recall | 0.9603 |
| stall_recall | 0.7188 |
| slope_recall | 0.9811 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7580 |
| downhill_recall | 0.7980 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    726,
    0,
    30
  ],
  [
    9,
    69,
    18
  ],
  [
    40,
    12,
    2698
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    498,
    212,
    89
  ],
  [
    432,
    1154,
    347
  ],
  [
    190,
    252,
    428
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.323007 |
| test_loss_turn_bundle_base | 0.342849 |
| test_loss_theta_bundle_base | 0.000248 |
| test_loss_transition_focal_raw | 1.555037 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.442917 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 69
- train_seconds: 332.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.2917 | 0.5453 |
| [0.60,0.70) | 36 | 0.4444 | 0.6324 |
| [0.70,0.80) | 18 | 0.3333 | 0.7390 |
| [0.80,0.90) | 38 | 0.3158 | 0.8548 |
| [0.90,1.00) | 3486 | 0.0195 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 561 | 0.6203 | 0.5076 |
| [0.60,0.70) | 373 | 0.5523 | 0.6523 |
| [0.70,0.80) | 423 | 0.5012 | 0.7521 |
| [0.80,0.90) | 485 | 0.4660 | 0.8528 |
| [0.90,1.00) | 1760 | 0.3011 | 0.9727 |


## 验证集最佳点

```json
{
  "loss_total": 0.5691585353327379,
  "acc_main": 0.9493910690121786,
  "acc_turn": 0.6346414073071719,
  "acc_turn_pure": 0.6486397902327106,
  "acc_turn_transition": 0.5683229813664596,
  "false_turn_straight": 0.4028066528066528,
  "flat_recall": 0.9649923896499238,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9516021361815754,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9649923896499238,
    0.5476190476190477,
    0.9516021361815754
  ],
  "turn_right_recall": 0.6492890995260664,
  "turn_straight_recall": 0.5971933471933472,
  "turn_left_recall": 0.6990291262135923,
  "recall_turn": [
    0.6492890995260664,
    0.5971933471933472,
    0.6990291262135923
  ],
  "cm_turn": [
    [
      548,
      217,
      79
    ],
    [
      386,
      1149,
      389
    ],
    [
      91,
      188,
      648
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      634,
      0,
      23
    ],
    [
      0,
      23,
      19
    ],
    [
      132,
      13,
      2851
    ]
  ],
  "main_confidence_mean": 0.9697120510923426,
  "main_confidence_error_mean": 0.7596370188074326,
  "main_low_conf_0p60_ratio": 0.04871447902571042,
  "main_low_conf_0p70_ratio": 0.0557510148849797,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 180,
      "error_rate": 0.45555555555555555,
      "mean_confidence": 0.5356011334994747
    },
    {
      "bin": "[0.60,0.70)",
      "n": 26,
      "error_rate": 0.2692307692307692,
      "mean_confidence": 0.6547423075798022
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.20689655172413793,
      "mean_confidence": 0.7478196381334112
    },
    {
      "bin": "[0.80,0.90)",
      "n": 41,
      "error_rate": 0.2926829268292683,
      "mean_confidence": 0.8515011723755842
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3419,
      "error_rate": 0.023398654577361802,
      "mean_confidence": 0.9982615405633104
    }
  ],
  "turn_confidence_mean": 0.8412383824035673,
  "turn_confidence_error_mean": 0.7624586033699956,
  "turn_low_conf_0p60_ratio": 0.1496617050067659,
  "turn_low_conf_0p70_ratio": 0.22679296346414074,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 553,
      "error_rate": 0.6112115732368897,
      "mean_confidence": 0.4793178856096248
    },
    {
      "bin": "[0.60,0.70)",
      "n": 285,
      "error_rate": 0.49473684210526314,
      "mean_confidence": 0.6500268551076145
    },
    {
      "bin": "[0.70,0.80)",
      "n": 345,
      "error_rate": 0.4666666666666667,
      "mean_confidence": 0.7534427675043495
    },
    {
      "bin": "[0.80,0.90)",
      "n": 480,
      "error_rate": 0.48125,
      "mean_confidence": 0.854018563295624
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2032,
      "error_rate": 0.2357283464566929,
      "mean_confidence": 0.9784393274421697
    }
  ],
  "theta_mae_rad": 0.017350420355796814,
  "theta_mae_deg": 0.9941058158874512,
  "uphill_recall": 0.7741239892183288,
  "downhill_recall": 0.7997775305895439,
  "slope_sign_acc": 0.9627703257596496,
  "theta_flat_mae_deg": 1.4116957187652588,
  "theta_flat_abs_p95_deg": 4.117137908935547,
  "theta_flat_abs_max_deg": 7.36986780166626,
  "theta_flat_bias_deg": -0.2021358162164688,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6595098972320557,
  "theta_near_flat_abs_p95_deg": 4.119417667388916,
  "theta_near_flat_abs_max_deg": 7.36986780166626,
  "theta_near_flat_bias_deg": 0.10120204091072083,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3296544551849365,
  "theta_flat_turn_abs_p95_deg": 4.117123603820801,
  "theta_flat_turn_abs_max_deg": 7.36986780166626,
  "theta_flat_turn_bias_deg": -0.5333654880523682,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9941058158874512,
  "theta_slope_control_abs_p95_deg": 8.800220489501953,
  "theta_slope_control_abs_max_deg": 11.611042022705078,
  "theta_slope_control_bias_deg": -0.3241422474384308,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.994105875492096,
  "theta_all_rmse_deg": 1.3129637241363525,
  "theta_all_p95_abs_err_deg": 2.61712384223938,
  "theta_all_max_abs_err_deg": 6.869867324829102,
  "theta_all_bias_deg": -0.3241422474384308,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9025316834449768,
  "theta_active_abs_ge_2_rmse_deg": 1.1782439947128296,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2722396850585938,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.673539161682129,
  "theta_active_abs_ge_2_bias_deg": -0.35089731216430664,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0266447067260742,
  "theta_abs_le_8_rmse_deg": 1.3367977142333984,
  "theta_abs_le_8_p95_abs_err_deg": 2.61712384223938,
  "theta_abs_le_8_max_abs_err_deg": 6.869867324829102,
  "theta_abs_le_8_bias_deg": -0.32843708992004395,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.994105875492096,
  "theta_abs_le_10_rmse_deg": 1.3129637241363525,
  "theta_abs_le_10_p95_abs_err_deg": 2.61712384223938,
  "theta_abs_le_10_max_abs_err_deg": 6.869867324829102,
  "theta_abs_le_10_bias_deg": -0.3241422474384308,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.0369857549667358,
  "theta_pos_8_10_rmse_deg": 1.2349599599838257,
  "theta_pos_8_10_p95_abs_err_deg": 2.376457452774048,
  "theta_pos_8_10_max_abs_err_deg": 5.294275283813477,
  "theta_pos_8_10_bias_deg": -0.917281448841095,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.673576295375824,
  "theta_neg_10_8_rmse_deg": 1.1783925294876099,
  "theta_neg_10_8_p95_abs_err_deg": 2.27614688873291,
  "theta_neg_10_8_max_abs_err_deg": 6.673539161682129,
  "theta_neg_10_8_bias_deg": 0.31580236554145813,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.0345529317855835,
  "theta_pos_6_8_rmse_deg": 1.2346049547195435,
  "theta_pos_6_8_p95_abs_err_deg": 2.3053417205810547,
  "theta_pos_6_8_max_abs_err_deg": 3.158496618270874,
  "theta_pos_6_8_bias_deg": -0.8352592587471008,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.67402184009552,
  "theta_neg_8_6_rmse_deg": 0.9672190546989441,
  "theta_neg_8_6_p95_abs_err_deg": 1.7368779182434082,
  "theta_neg_8_6_max_abs_err_deg": 4.785019397735596,
  "theta_neg_8_6_bias_deg": -0.19923867285251617,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7782379984855652,
  "theta_neg_4_2_rmse_deg": 1.0083218812942505,
  "theta_neg_4_2_p95_abs_err_deg": 1.9395793676376343,
  "theta_neg_4_2_max_abs_err_deg": 4.6194329261779785,
  "theta_neg_4_2_bias_deg": -0.3059450089931488,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.9102891683578491,
  "theta_neg_2_0p5_rmse_deg": 1.0736219882965088,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8433836698532104,
  "theta_neg_2_0p5_max_abs_err_deg": 2.846731662750244,
  "theta_neg_2_0p5_bias_deg": -0.8282840847969055,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.630723237991333,
  "theta_pos_0p5_2_rmse_deg": 1.8446465730667114,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.83616304397583,
  "theta_pos_0p5_2_max_abs_err_deg": 3.938948631286621,
  "theta_pos_0p5_2_bias_deg": 0.16572345793247223,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2732959794336791,
  "loss_turn": 1.4774977342685602,
  "loss_theta": 0.0005249751502703447,
  "loss_main_bundle_base": 0.2732959794336791,
  "loss_turn_bundle_base": 0.2954995513688244,
  "loss_theta_bundle_base": 0.0003630039804830583,
  "loss_main_bundle": 0.2732959794336791,
  "loss_turn_bundle": 0.2954995513688244,
  "loss_theta_bundle": 0.0003630039804830583,
  "loss_theta_flat": 0.00045920507177390433,
  "loss_theta_near_flat": 0.001530700492268083,
  "loss_theta_error_excess": 0.00016134100234739643,
  "loss_theta_flat_excess": 0.0002545515995306317,
  "loss_theta_near_flat_excess": 0.0010745086676928848,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011095983710824304,
  "loss_theta_small_neg": 0.00030567332091193056,
  "loss_theta_small_neg_excess": 6.077107526009073e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3675080017969315,
  "loss_false_turn_straight": 0.29321575938284156,
  "loss_transition_focal_raw": 1.256335272727703,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.3104926567444717,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
