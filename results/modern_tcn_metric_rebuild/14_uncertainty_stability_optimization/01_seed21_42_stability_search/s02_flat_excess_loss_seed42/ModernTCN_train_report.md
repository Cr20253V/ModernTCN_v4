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
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.06,
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
  "theta_flat_excess_target_deg": 0.45,
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
  "select_theta_flat_peak_weight": 1.4,
  "select_theta_flat_peak_target_deg": 4.8,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.6,
  "select_theta_edge_p95_target_deg": 1.25,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9625 |
| acc_turn | 0.4847 |
| acc_turn_pure | 0.5063 |
| acc_turn_transition | 0.3905 |
| main_confidence_mean | 0.9764 |
| main_low_conf_0p60_ratio | 0.0130 |
| main_low_conf_0p70_ratio | 0.0253 |
| turn_confidence_mean | 0.6892 |
| turn_low_conf_0p60_ratio | 0.3967 |
| turn_low_conf_0p70_ratio | 0.5547 |
| turn_right_recall | 0.5670 |
| turn_straight_recall | 0.4330 |
| turn_left_recall | 0.5241 |
| theta_mae_deg | 1.0423 |
| theta_abs_le_10_p95_abs_err_deg | 2.4629 |
| theta_neg_10_8_p95_abs_err_deg | 2.3707 |
| theta_pos_8_10_p95_abs_err_deg | 2.6186 |
| theta_abs_le_8_p95_abs_err_deg | 2.4641 |
| theta_neg_8_6_p95_abs_err_deg | 2.0768 |
| theta_pos_6_8_p95_abs_err_deg | 2.1035 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.8515 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.8950 |
| theta_flat_abs_p95_deg | 3.4902 |
| theta_flat_bias_deg | -0.7415 |
| theta_near_flat_abs_p95_deg | 3.2199 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -1.2042 |
| theta_flat_turn_abs_p95_deg | 2.9353 |
| flat_recall | 0.9749 |
| stall_recall | 0.7083 |
| slope_recall | 0.9680 |
| flat_as_stall_ratio | 0.0026 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7425 |
| downhill_recall | 0.7855 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    737,
    2,
    17
  ],
  [
    9,
    68,
    19
  ],
  [
    66,
    22,
    2662
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    453,
    207,
    139
  ],
  [
    562,
    837,
    534
  ],
  [
    258,
    156,
    456
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.231007 |
| test_loss_turn_bundle_base | 0.228119 |
| test_loss_theta_bundle_base | 0.000466 |
| test_loss_transition_focal_raw | 0.806395 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.259090 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 25
- train_seconds: 220.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 47 | 0.4468 | 0.5371 |
| [0.60,0.70) | 44 | 0.5909 | 0.6560 |
| [0.70,0.80) | 35 | 0.3429 | 0.7491 |
| [0.80,0.90) | 101 | 0.0990 | 0.8538 |
| [0.90,1.00) | 3375 | 0.0196 | 0.9927 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1429 | 0.6123 | 0.4975 |
| [0.60,0.70) | 569 | 0.6186 | 0.6501 |
| [0.70,0.80) | 450 | 0.5311 | 0.7482 |
| [0.80,0.90) | 447 | 0.4832 | 0.8516 |
| [0.90,1.00) | 707 | 0.2461 | 0.9679 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.3905
- theta_mae_deg <= 0.7000 未满足，实际 1.0423

## 验证集最佳点

```json
{
  "loss_total": 0.4110450195766108,
  "acc_main": 0.9423545331529093,
  "acc_turn": 0.5418132611637347,
  "acc_turn_pure": 0.5519501802687643,
  "acc_turn_transition": 0.4937888198757764,
  "false_turn_straight": 0.5867983367983368,
  "flat_recall": 0.817351598173516,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9753004005340454,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.817351598173516,
    0.5476190476190477,
    0.9753004005340454
  ],
  "turn_right_recall": 0.6362559241706162,
  "turn_straight_recall": 0.4132016632016632,
  "turn_left_recall": 0.7227615965480043,
  "recall_turn": [
    0.6362559241706162,
    0.4132016632016632,
    0.7227615965480043
  ],
  "cm_turn": [
    [
      537,
      168,
      139
    ],
    [
      504,
      795,
      625
    ],
    [
      161,
      96,
      670
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      537,
      0,
      120
    ],
    [
      0,
      23,
      19
    ],
    [
      61,
      13,
      2922
    ]
  ],
  "main_confidence_mean": 0.9554791026384213,
  "main_confidence_error_mean": 0.6948934250554034,
  "main_low_conf_0p60_ratio": 0.055209742895805144,
  "main_low_conf_0p70_ratio": 0.06684709066305819,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 204,
      "error_rate": 0.5098039215686274,
      "mean_confidence": 0.5043499334049827
    },
    {
      "bin": "[0.60,0.70)",
      "n": 43,
      "error_rate": 0.32558139534883723,
      "mean_confidence": 0.655455447764364
    },
    {
      "bin": "[0.70,0.80)",
      "n": 63,
      "error_rate": 0.31746031746031744,
      "mean_confidence": 0.7497237319241014
    },
    {
      "bin": "[0.80,0.90)",
      "n": 101,
      "error_rate": 0.16831683168316833,
      "mean_confidence": 0.8547501361765716
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3284,
      "error_rate": 0.01766138855054811,
      "mean_confidence": 0.9944765391947108
    }
  ],
  "turn_confidence_mean": 0.7242533139117798,
  "turn_confidence_error_mean": 0.6647945298151398,
  "turn_low_conf_0p60_ratio": 0.3193504736129905,
  "turn_low_conf_0p70_ratio": 0.4765899864682003,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1180,
      "error_rate": 0.6076271186440678,
      "mean_confidence": 0.5091718945501904
    },
    {
      "bin": "[0.60,0.70)",
      "n": 581,
      "error_rate": 0.5507745266781411,
      "mean_confidence": 0.6466633698792189
    },
    {
      "bin": "[0.70,0.80)",
      "n": 500,
      "error_rate": 0.498,
      "mean_confidence": 0.7472736878562891
    },
    {
      "bin": "[0.80,0.90)",
      "n": 482,
      "error_rate": 0.3630705394190871,
      "mean_confidence": 0.8508261126272701
    },
    {
      "bin": "[0.90,1.00)",
      "n": 952,
      "error_rate": 0.24369747899159663,
      "mean_confidence": 0.9620238563240409
    }
  ],
  "theta_mae_rad": 0.020401909947395325,
  "theta_mae_deg": 1.1689432859420776,
  "uphill_recall": 0.8576819407008086,
  "downhill_recall": 0.807007786429366,
  "slope_sign_acc": 0.960580344921982,
  "theta_flat_mae_deg": 1.3575034141540527,
  "theta_flat_abs_p95_deg": 3.5425140857696533,
  "theta_flat_abs_max_deg": 6.858531475067139,
  "theta_flat_bias_deg": 0.03880453109741211,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.7772431373596191,
  "theta_near_flat_abs_p95_deg": 3.599057674407959,
  "theta_near_flat_abs_max_deg": 6.858531475067139,
  "theta_near_flat_bias_deg": 0.028622016310691833,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.6193690299987793,
  "theta_flat_turn_abs_p95_deg": 3.745537042617798,
  "theta_flat_turn_abs_max_deg": 6.858531475067139,
  "theta_flat_turn_bias_deg": -0.49667373299598694,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.1689432859420776,
  "theta_slope_control_abs_p95_deg": 9.124982833862305,
  "theta_slope_control_abs_max_deg": 13.079558372497559,
  "theta_slope_control_bias_deg": 0.15562677383422852,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.168943166732788,
  "theta_all_rmse_deg": 1.515594720840454,
  "theta_all_p95_abs_err_deg": 3.0417585372924805,
  "theta_all_max_abs_err_deg": 8.437766075134277,
  "theta_all_bias_deg": 0.15562677383422852,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.1275933980941772,
  "theta_active_abs_ge_2_rmse_deg": 1.4553757905960083,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.7004756927490234,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.437766075134277,
  "theta_active_abs_ge_2_bias_deg": 0.18124499917030334,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.1525999307632446,
  "theta_abs_le_8_rmse_deg": 1.5015177726745605,
  "theta_abs_le_8_p95_abs_err_deg": 3.041810989379883,
  "theta_abs_le_8_max_abs_err_deg": 8.437766075134277,
  "theta_abs_le_8_bias_deg": 0.12379996478557587,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.168943166732788,
  "theta_abs_le_10_rmse_deg": 1.515594720840454,
  "theta_abs_le_10_p95_abs_err_deg": 3.0417585372924805,
  "theta_abs_le_10_max_abs_err_deg": 8.437766075134277,
  "theta_abs_le_10_bias_deg": 0.15562677383422852,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9161363244056702,
  "theta_pos_8_10_rmse_deg": 1.149437427520752,
  "theta_pos_8_10_p95_abs_err_deg": 2.0506789684295654,
  "theta_pos_8_10_max_abs_err_deg": 4.864419460296631,
  "theta_pos_8_10_bias_deg": -0.5743246674537659,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.5652045011520386,
  "theta_neg_10_8_rmse_deg": 1.9108000993728638,
  "theta_neg_10_8_p95_abs_err_deg": 3.424635410308838,
  "theta_neg_10_8_max_abs_err_deg": 7.472696781158447,
  "theta_neg_10_8_bias_deg": 1.16904878616333,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.9733901619911194,
  "theta_pos_6_8_rmse_deg": 1.2016979455947876,
  "theta_pos_6_8_p95_abs_err_deg": 2.3539533615112305,
  "theta_pos_6_8_max_abs_err_deg": 3.6733763217926025,
  "theta_pos_6_8_bias_deg": -0.3734859526157379,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.41739022731781,
  "theta_neg_8_6_rmse_deg": 1.6768457889556885,
  "theta_neg_8_6_p95_abs_err_deg": 2.705131769180298,
  "theta_neg_8_6_max_abs_err_deg": 6.6946001052856445,
  "theta_neg_8_6_bias_deg": 0.6098122596740723,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9761900901794434,
  "theta_neg_4_2_rmse_deg": 1.2271454334259033,
  "theta_neg_4_2_p95_abs_err_deg": 2.3818113803863525,
  "theta_neg_4_2_max_abs_err_deg": 4.664846420288086,
  "theta_neg_4_2_bias_deg": 0.03834801912307739,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6040561199188232,
  "theta_neg_2_0p5_rmse_deg": 0.835891604423523,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8224714994430542,
  "theta_neg_2_0p5_max_abs_err_deg": 4.049003601074219,
  "theta_neg_2_0p5_bias_deg": -0.2011902630329132,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.5076340436935425,
  "theta_pos_0p5_2_rmse_deg": 1.783249020576477,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.2310378551483154,
  "theta_pos_0p5_2_max_abs_err_deg": 4.78098726272583,
  "theta_pos_0p5_2_bias_deg": 0.5463989973068237,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.19973712236858673,
  "loss_turn": 1.053741981389558,
  "loss_theta": 0.0006997121968375915,
  "loss_main_bundle_base": 0.19973712236858673,
  "loss_turn_bundle_base": 0.2107483996711016,
  "loss_theta_bundle_base": 0.0005594989319057211,
  "loss_main_bundle": 0.19973712236858673,
  "loss_turn_bundle": 0.2107483996711016,
  "loss_theta_bundle": 0.0005594989319057211,
  "loss_theta_flat": 0.0007282404362946164,
  "loss_theta_near_flat": 0.0015108135487904447,
  "loss_theta_error_excess": 0.00023611631828545515,
  "loss_theta_flat_excess": 0.0004287181646202052,
  "loss_theta_near_flat_excess": 0.0010729348292972524,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00020609831087592439,
  "loss_theta_small_neg": 0.0004585401513909919,
  "loss_theta_small_neg_excess": 0.00010442785704549381,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4809635526353193,
  "loss_false_turn_straight": 0.3842839746981738,
  "loss_transition_focal_raw": 0.6490184993801968,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 1.457018425082883,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
