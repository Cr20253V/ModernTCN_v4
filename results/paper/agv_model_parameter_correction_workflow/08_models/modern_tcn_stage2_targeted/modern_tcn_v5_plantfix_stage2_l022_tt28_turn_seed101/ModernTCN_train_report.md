# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

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
  "lambda_turn": 0.22,
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
    1.45,
    0.75,
    1.45
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.8,
  "select_turn_weight": 0.62,
  "select_turn_transition_weight": 1.35,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.7,
  "select_turn_lr_target": 0.88,
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
| acc_main | 0.9553 |
| acc_turn | 0.5572 |
| acc_turn_pure | 0.5674 |
| acc_turn_transition | 0.5127 |
| main_confidence_mean | 0.9867 |
| main_low_conf_0p60_ratio | 0.0089 |
| main_low_conf_0p70_ratio | 0.0139 |
| turn_confidence_mean | 0.8082 |
| turn_low_conf_0p60_ratio | 0.1705 |
| turn_low_conf_0p70_ratio | 0.2854 |
| turn_right_recall | 0.6320 |
| turn_straight_recall | 0.4904 |
| turn_left_recall | 0.6368 |
| theta_mae_deg | 0.7609 |
| theta_abs_le_10_p95_abs_err_deg | 2.0561 |
| theta_neg_10_8_p95_abs_err_deg | 1.7322 |
| theta_pos_8_10_p95_abs_err_deg | 3.1471 |
| theta_abs_le_8_p95_abs_err_deg | 1.9237 |
| theta_neg_8_6_p95_abs_err_deg | 2.4651 |
| theta_pos_6_8_p95_abs_err_deg | 1.7045 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9616 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5007 |
| theta_flat_abs_p95_deg | 2.3549 |
| theta_flat_bias_deg | 0.1611 |
| theta_near_flat_abs_p95_deg | 1.5904 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0888 |
| theta_flat_turn_abs_p95_deg | 1.5175 |
| flat_recall | 0.9286 |
| stall_recall | 0.6667 |
| slope_recall | 0.9727 |
| uphill_recall | 0.7483 |
| downhill_recall | 0.8082 |

- best_epoch: 55
- train_seconds: 740.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 32 | 0.7812 | 0.5540 |
| [0.60,0.70) | 18 | 0.4444 | 0.6458 |
| [0.70,0.80) | 31 | 0.4194 | 0.7543 |
| [0.80,0.90) | 56 | 0.4107 | 0.8570 |
| [0.90,1.00) | 3465 | 0.0266 | 0.9966 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 614 | 0.5489 | 0.5188 |
| [0.60,0.70) | 414 | 0.5821 | 0.6496 |
| [0.70,0.80) | 538 | 0.5651 | 0.7495 |
| [0.80,0.90) | 471 | 0.4501 | 0.8522 |
| [0.90,1.00) | 1565 | 0.3201 | 0.9707 |


## 验证集最佳点

```json
{
  "loss_total": 0.5993717081975872,
  "acc_main": 0.9466847090663059,
  "acc_turn": 0.5986468200270636,
  "acc_turn_pure": 0.6204523107177975,
  "acc_turn_transition": 0.4953416149068323,
  "flat_recall": 0.9649923896499238,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9516021361815754,
  "recall_main": [
    0.9649923896499238,
    0.30952380952380953,
    0.9516021361815754
  ],
  "turn_right_recall": 0.7156398104265402,
  "turn_straight_recall": 0.4688149688149688,
  "turn_left_recall": 0.761596548004315,
  "recall_turn": [
    0.7156398104265402,
    0.4688149688149688,
    0.761596548004315
  ],
  "cm_turn": [
    [
      604,
      176,
      64
    ],
    [
      557,
      902,
      465
    ],
    [
      99,
      122,
      706
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
      13,
      29
    ],
    [
      134,
      11,
      2851
    ]
  ],
  "main_confidence_mean": 0.9775204473072239,
  "main_confidence_error_mean": 0.8302643125695656,
  "main_low_conf_0p60_ratio": 0.0035182679296346412,
  "main_low_conf_0p70_ratio": 0.008930987821380243,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 13,
      "error_rate": 0.6923076923076923,
      "mean_confidence": 0.5494801111282009
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.2,
      "mean_confidence": 0.6603868741722181
    },
    {
      "bin": "[0.70,0.80)",
      "n": 186,
      "error_rate": 0.45698924731182794,
      "mean_confidence": 0.7074755729778702
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.2978723404255319,
      "mean_confidence": 0.8601497253759323
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3429,
      "error_rate": 0.02478856809565471,
      "mean_confidence": 0.9972498046676957
    }
  ],
  "turn_confidence_mean": 0.8231077036204062,
  "turn_confidence_error_mean": 0.7534813796192487,
  "turn_low_conf_0p60_ratio": 0.16373477672530445,
  "turn_low_conf_0p70_ratio": 0.2700947225981056,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 605,
      "error_rate": 0.6181818181818182,
      "mean_confidence": 0.5042134788348903
    },
    {
      "bin": "[0.60,0.70)",
      "n": 393,
      "error_rate": 0.5725190839694656,
      "mean_confidence": 0.64924622318417
    },
    {
      "bin": "[0.70,0.80)",
      "n": 405,
      "error_rate": 0.4888888888888889,
      "mean_confidence": 0.7494359922714288
    },
    {
      "bin": "[0.80,0.90)",
      "n": 471,
      "error_rate": 0.4564755838641189,
      "mean_confidence": 0.8512923785157573
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1821,
      "error_rate": 0.2586490939044481,
      "mean_confidence": 0.9756725740362786
    }
  ],
  "theta_mae_rad": 0.015767112374305725,
  "theta_mae_deg": 0.9033889174461365,
  "uphill_recall": 0.7757412398921832,
  "downhill_recall": 0.7981090100111234,
  "slope_sign_acc": 0.9690665206679442,
  "theta_flat_mae_deg": 1.248472809791565,
  "theta_flat_abs_p95_deg": 3.853135824203491,
  "theta_flat_abs_max_deg": 11.12342357635498,
  "theta_flat_bias_deg": 0.5119290351867676,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5760445594787598,
  "theta_near_flat_abs_p95_deg": 4.436872959136963,
  "theta_near_flat_abs_max_deg": 11.12342357635498,
  "theta_near_flat_bias_deg": 0.6141232848167419,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3567556142807007,
  "theta_flat_turn_abs_p95_deg": 4.897069931030273,
  "theta_flat_turn_abs_max_deg": 11.12342357635498,
  "theta_flat_turn_bias_deg": -0.11428376287221909,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9033889174461365,
  "theta_slope_control_abs_p95_deg": 8.93765640258789,
  "theta_slope_control_abs_max_deg": 13.436370849609375,
  "theta_slope_control_bias_deg": 0.309945672750473,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9033889770507812,
  "theta_all_rmse_deg": 1.3153544664382935,
  "theta_all_p95_abs_err_deg": 2.73447585105896,
  "theta_all_max_abs_err_deg": 10.62342357635498,
  "theta_all_bias_deg": 0.30994564294815063,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8277146816253662,
  "theta_active_abs_ge_2_rmse_deg": 1.18215012550354,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4297993183135986,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.014720916748047,
  "theta_active_abs_ge_2_bias_deg": 0.26565226912498474,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9199162721633911,
  "theta_abs_le_8_rmse_deg": 1.346968173980713,
  "theta_abs_le_8_p95_abs_err_deg": 2.8485562801361084,
  "theta_abs_le_8_max_abs_err_deg": 10.62342357635498,
  "theta_abs_le_8_bias_deg": 0.37646016478538513,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9033889770507812,
  "theta_abs_le_10_rmse_deg": 1.3153544664382935,
  "theta_abs_le_10_p95_abs_err_deg": 2.73447585105896,
  "theta_abs_le_10_max_abs_err_deg": 10.62342357635498,
  "theta_abs_le_10_bias_deg": 0.30994564294815063,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8053810000419617,
  "theta_pos_8_10_rmse_deg": 0.9628339409828186,
  "theta_pos_8_10_p95_abs_err_deg": 1.8124871253967285,
  "theta_pos_8_10_max_abs_err_deg": 4.233946323394775,
  "theta_pos_8_10_bias_deg": -0.5756076574325562,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8624426126480103,
  "theta_neg_10_8_rmse_deg": 1.3531044721603394,
  "theta_neg_10_8_p95_abs_err_deg": 2.6165316104888916,
  "theta_neg_10_8_max_abs_err_deg": 6.478096008300781,
  "theta_neg_10_8_bias_deg": 0.6447669267654419,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.563948929309845,
  "theta_pos_6_8_rmse_deg": 0.8024733066558838,
  "theta_pos_6_8_p95_abs_err_deg": 1.842860221862793,
  "theta_pos_6_8_max_abs_err_deg": 3.291175127029419,
  "theta_pos_6_8_bias_deg": -0.05863567069172859,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0522243976593018,
  "theta_neg_8_6_rmse_deg": 1.3919594287872314,
  "theta_neg_8_6_p95_abs_err_deg": 2.562495708465576,
  "theta_neg_8_6_max_abs_err_deg": 6.251553058624268,
  "theta_neg_8_6_bias_deg": 0.6121819615364075,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7811267375946045,
  "theta_neg_4_2_rmse_deg": 1.0671958923339844,
  "theta_neg_4_2_p95_abs_err_deg": 2.2772302627563477,
  "theta_neg_4_2_max_abs_err_deg": 4.306926250457764,
  "theta_neg_4_2_bias_deg": 0.29483762383461,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7532703876495361,
  "theta_neg_2_0p5_rmse_deg": 1.0078104734420776,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8454324007034302,
  "theta_neg_2_0p5_max_abs_err_deg": 4.897588729858398,
  "theta_neg_2_0p5_bias_deg": 0.040261201560497284,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4502670764923096,
  "theta_pos_0p5_2_rmse_deg": 1.7233705520629883,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.520606756210327,
  "theta_pos_0p5_2_max_abs_err_deg": 4.778015613555908,
  "theta_pos_0p5_2_bias_deg": 1.1881320476531982,
  "theta_pos_0p5_2_n": 163.0
}
```
