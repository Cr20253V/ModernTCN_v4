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
  "lambda_turn": 0.08,
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
    1.08,
    1.0,
    1.08
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.4,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.2,
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
| acc_main | 0.9567 |
| acc_turn | 0.6016 |
| acc_turn_pure | 0.6179 |
| acc_turn_transition | 0.5306 |
| main_confidence_mean | 0.9915 |
| main_low_conf_0p60_ratio | 0.0036 |
| main_low_conf_0p70_ratio | 0.0081 |
| turn_confidence_mean | 0.8486 |
| turn_low_conf_0p60_ratio | 0.1344 |
| turn_low_conf_0p70_ratio | 0.2310 |
| turn_right_recall | 0.5932 |
| turn_straight_recall | 0.6503 |
| turn_left_recall | 0.5011 |
| theta_mae_deg | 0.5251 |
| theta_abs_le_10_p95_abs_err_deg | 1.4754 |
| theta_neg_10_8_p95_abs_err_deg | 1.0532 |
| theta_pos_8_10_p95_abs_err_deg | 2.2935 |
| theta_abs_le_8_p95_abs_err_deg | 1.3397 |
| theta_neg_8_6_p95_abs_err_deg | 1.2004 |
| theta_pos_6_8_p95_abs_err_deg | 1.3179 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3088 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4070 |
| theta_flat_abs_p95_deg | 2.2385 |
| theta_flat_bias_deg | -0.1429 |
| theta_near_flat_abs_p95_deg | 1.4892 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1916 |
| theta_flat_turn_abs_p95_deg | 1.4248 |
| flat_recall | 0.9352 |
| stall_recall | 0.6250 |
| slope_recall | 0.9742 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7494 |
| downhill_recall | 0.8065 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    707,
    0,
    49
  ],
  [
    10,
    60,
    26
  ],
  [
    59,
    12,
    2679
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    474,
    223,
    102
  ],
  [
    339,
    1257,
    337
  ],
  [
    146,
    288,
    436
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.372420 |
| test_loss_turn_bundle_base | 0.128142 |
| test_loss_theta_bundle_base | 0.000116 |
| test_loss_transition_focal_raw | 1.645928 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.531716 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 103
- train_seconds: 2104.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 13 | 0.6923 | 0.5549 |
| [0.60,0.70) | 16 | 0.4375 | 0.6609 |
| [0.70,0.80) | 22 | 0.4091 | 0.7523 |
| [0.80,0.90) | 50 | 0.5400 | 0.8469 |
| [0.90,1.00) | 3501 | 0.0297 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 484 | 0.5826 | 0.5342 |
| [0.60,0.70) | 348 | 0.5402 | 0.6537 |
| [0.70,0.80) | 367 | 0.4877 | 0.7506 |
| [0.80,0.90) | 446 | 0.4978 | 0.8531 |
| [0.90,1.00) | 1957 | 0.2882 | 0.9784 |


## 验证集最佳点

```json
{
  "loss_total": 0.48612703780198774,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.6589986468200271,
  "acc_turn_pure": 0.671583087512291,
  "acc_turn_transition": 0.5993788819875776,
  "false_turn_straight": 0.33367983367983367,
  "flat_recall": 0.9619482496194824,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9499332443257676,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9619482496194824,
    0.35714285714285715,
    0.9499332443257676
  ],
  "turn_right_recall": 0.7014218009478673,
  "turn_straight_recall": 0.6663201663201663,
  "turn_left_recall": 0.6051779935275081,
  "recall_turn": [
    0.7014218009478673,
    0.6663201663201663,
    0.6051779935275081
  ],
  "cm_turn": [
    [
      592,
      219,
      33
    ],
    [
      353,
      1282,
      289
    ],
    [
      81,
      285,
      561
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      632,
      1,
      24
    ],
    [
      0,
      15,
      27
    ],
    [
      145,
      5,
      2846
    ]
  ],
  "main_confidence_mean": 0.9720205272721507,
  "main_confidence_error_mean": 0.7854225035994482,
  "main_low_conf_0p60_ratio": 0.04844384303112314,
  "main_low_conf_0p70_ratio": 0.05196211096075778,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 179,
      "error_rate": 0.4692737430167598,
      "mean_confidence": 0.552915620755738
    },
    {
      "bin": "[0.60,0.70)",
      "n": 13,
      "error_rate": 0.15384615384615385,
      "mean_confidence": 0.6573044357979221
    },
    {
      "bin": "[0.70,0.80)",
      "n": 33,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.7469533342218782
    },
    {
      "bin": "[0.80,0.90)",
      "n": 33,
      "error_rate": 0.2727272727272727,
      "mean_confidence": 0.8558089976570028
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3437,
      "error_rate": 0.027931335466977014,
      "mean_confidence": 0.9983147621582612
    }
  ],
  "turn_confidence_mean": 0.8587997006395948,
  "turn_confidence_error_mean": 0.7895707711839645,
  "turn_low_conf_0p60_ratio": 0.12476319350473614,
  "turn_low_conf_0p70_ratio": 0.20487144790257103,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 461,
      "error_rate": 0.5813449023861171,
      "mean_confidence": 0.4829339866434012
    },
    {
      "bin": "[0.60,0.70)",
      "n": 296,
      "error_rate": 0.4864864864864865,
      "mean_confidence": 0.6502154172110494
    },
    {
      "bin": "[0.70,0.80)",
      "n": 314,
      "error_rate": 0.4426751592356688,
      "mean_confidence": 0.7524882906357514
    },
    {
      "bin": "[0.80,0.90)",
      "n": 396,
      "error_rate": 0.4116161616161616,
      "mean_confidence": 0.8527459525565786
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2228,
      "error_rate": 0.24506283662477557,
      "mean_confidence": 0.9803410422146289
    }
  ],
  "theta_mae_rad": 0.012805844657123089,
  "theta_mae_deg": 0.7337208390235901,
  "uphill_recall": 0.7757412398921832,
  "downhill_recall": 0.7958843159065628,
  "slope_sign_acc": 0.9822064056939501,
  "theta_flat_mae_deg": 0.9914199113845825,
  "theta_flat_abs_p95_deg": 4.640933513641357,
  "theta_flat_abs_max_deg": 7.801989555358887,
  "theta_flat_bias_deg": 0.6399754285812378,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3613032102584839,
  "theta_near_flat_abs_p95_deg": 4.641288757324219,
  "theta_near_flat_abs_max_deg": 7.801989555358887,
  "theta_near_flat_bias_deg": 1.1404247283935547,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0086264610290527,
  "theta_flat_turn_abs_p95_deg": 4.640933036804199,
  "theta_flat_turn_abs_max_deg": 7.801989555358887,
  "theta_flat_turn_bias_deg": 0.8346713185310364,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7337208390235901,
  "theta_slope_control_abs_p95_deg": 8.9201078414917,
  "theta_slope_control_abs_max_deg": 11.295233726501465,
  "theta_slope_control_bias_deg": 0.12726682424545288,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7337208390235901,
  "theta_all_rmse_deg": 1.1446113586425781,
  "theta_all_p95_abs_err_deg": 2.475179433822632,
  "theta_all_max_abs_err_deg": 8.301989555358887,
  "theta_all_bias_deg": 0.12726682424545288,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6772093176841736,
  "theta_active_abs_ge_2_rmse_deg": 0.972081184387207,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1409332752227783,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.082419395446777,
  "theta_active_abs_ge_2_bias_deg": 0.014833727851510048,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7415740489959717,
  "theta_abs_le_8_rmse_deg": 1.1785478591918945,
  "theta_abs_le_8_p95_abs_err_deg": 2.6620066165924072,
  "theta_abs_le_8_max_abs_err_deg": 8.301989555358887,
  "theta_abs_le_8_bias_deg": 0.16720400750637054,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7337208390235901,
  "theta_abs_le_10_rmse_deg": 1.1446113586425781,
  "theta_abs_le_10_p95_abs_err_deg": 2.475179433822632,
  "theta_abs_le_10_max_abs_err_deg": 8.301989555358887,
  "theta_abs_le_10_bias_deg": 0.12726682424545288,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7181396484375,
  "theta_pos_8_10_rmse_deg": 0.8281447291374207,
  "theta_pos_8_10_p95_abs_err_deg": 1.3669915199279785,
  "theta_pos_8_10_max_abs_err_deg": 3.6891543865203857,
  "theta_pos_8_10_bias_deg": -0.5763041377067566,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6827400326728821,
  "theta_neg_10_8_rmse_deg": 1.128852128982544,
  "theta_neg_10_8_p95_abs_err_deg": 1.6435915231704712,
  "theta_neg_10_8_max_abs_err_deg": 7.075974941253662,
  "theta_neg_10_8_bias_deg": 0.5031343102455139,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5961441993713379,
  "theta_pos_6_8_rmse_deg": 0.8216662406921387,
  "theta_pos_6_8_p95_abs_err_deg": 1.6335880756378174,
  "theta_pos_6_8_max_abs_err_deg": 3.7969882488250732,
  "theta_pos_6_8_bias_deg": -0.2171168327331543,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6722736954689026,
  "theta_neg_8_6_rmse_deg": 1.0149189233779907,
  "theta_neg_8_6_p95_abs_err_deg": 1.8189400434494019,
  "theta_neg_8_6_max_abs_err_deg": 7.082419395446777,
  "theta_neg_8_6_bias_deg": -0.011988908983767033,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5493025183677673,
  "theta_neg_4_2_rmse_deg": 0.7989732027053833,
  "theta_neg_4_2_p95_abs_err_deg": 1.5107941627502441,
  "theta_neg_4_2_max_abs_err_deg": 5.652787208557129,
  "theta_neg_4_2_bias_deg": 0.011261285282671452,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4170936346054077,
  "theta_neg_2_0p5_rmse_deg": 0.6590588688850403,
  "theta_neg_2_0p5_p95_abs_err_deg": 0.985568642616272,
  "theta_neg_2_0p5_max_abs_err_deg": 4.597565650939941,
  "theta_neg_2_0p5_bias_deg": 0.11724436283111572,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1291022300720215,
  "theta_pos_0p5_2_rmse_deg": 1.6642268896102905,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.1409332752227783,
  "theta_pos_0p5_2_max_abs_err_deg": 4.580355644226074,
  "theta_pos_0p5_2_bias_deg": 0.4868760406970978,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.36630488008220397,
  "loss_turn": 1.4943977881832924,
  "loss_theta": 0.0003992415584953998,
  "loss_main_bundle_base": 0.36630488008220397,
  "loss_turn_bundle_base": 0.11955182021824046,
  "loss_theta_bundle_base": 0.00027034132655064737,
  "loss_main_bundle": 0.36630488008220397,
  "loss_turn_bundle": 0.11955182021824046,
  "loss_theta_bundle": 0.00027034132655064737,
  "loss_theta_flat": 0.00029348076573391577,
  "loss_theta_near_flat": 0.0014885055276165756,
  "loss_theta_error_excess": 0.00015222265547190582,
  "loss_theta_flat_excess": 0.00017250824850575597,
  "loss_theta_near_flat_excess": 0.0011228252239764765,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 7.929637771487647e-05,
  "loss_theta_small_neg": 0.00019044427197056045,
  "loss_theta_small_neg_excess": 3.974035668376432e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.32860341060790704,
  "loss_false_turn_straight": 0.24342910544959392,
  "loss_transition_focal_raw": 1.3381237645110515,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.8676870962924985,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
