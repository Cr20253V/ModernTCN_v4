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
  "lambda_turn": 0.24,
  "lambda_theta": 0.5,
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.04,
  "lambda_theta_flat_excess": 0.05,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
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
  "select_theta_flat_peak_weight": 1.0,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.0,
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
| acc_turn | 0.5192 |
| acc_turn_pure | 0.5329 |
| acc_turn_transition | 0.4590 |
| main_confidence_mean | 0.9854 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0169 |
| turn_confidence_mean | 0.7266 |
| turn_low_conf_0p60_ratio | 0.3184 |
| turn_low_conf_0p70_ratio | 0.4733 |
| turn_right_recall | 0.5657 |
| turn_straight_recall | 0.4553 |
| turn_left_recall | 0.6184 |
| theta_mae_deg | 0.6503 |
| theta_abs_le_10_p95_abs_err_deg | 1.7565 |
| theta_neg_10_8_p95_abs_err_deg | 1.3913 |
| theta_pos_8_10_p95_abs_err_deg | 2.3295 |
| theta_abs_le_8_p95_abs_err_deg | 1.7565 |
| theta_neg_8_6_p95_abs_err_deg | 1.4855 |
| theta_pos_6_8_p95_abs_err_deg | 1.4843 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0281 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7603 |
| theta_flat_abs_p95_deg | 2.9074 |
| theta_flat_bias_deg | -0.4608 |
| theta_near_flat_abs_p95_deg | 1.5661 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2523 |
| theta_flat_turn_abs_p95_deg | 1.6311 |
| flat_recall | 0.9484 |
| stall_recall | 0.6458 |
| slope_recall | 0.9825 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7638 |
| downhill_recall | 0.7997 |

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
    10,
    62,
    24
  ],
  [
    42,
    6,
    2702
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    452,
    187,
    160
  ],
  [
    408,
    880,
    645
  ],
  [
    181,
    151,
    538
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.260308 |
| test_loss_turn_bundle_base | 0.272570 |
| test_loss_theta_bundle_base | 0.000158 |
| test_loss_transition_focal_raw | 0.819288 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.004880 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 52
- train_seconds: 268.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.4444 | 0.5483 |
| [0.60,0.70) | 34 | 0.2353 | 0.6483 |
| [0.70,0.80) | 33 | 0.3939 | 0.7476 |
| [0.80,0.90) | 53 | 0.3396 | 0.8631 |
| [0.90,1.00) | 3455 | 0.0203 | 0.9963 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1147 | 0.6269 | 0.5103 |
| [0.60,0.70) | 558 | 0.5806 | 0.6499 |
| [0.70,0.80) | 498 | 0.5181 | 0.7496 |
| [0.80,0.90) | 462 | 0.4113 | 0.8480 |
| [0.90,1.00) | 937 | 0.2572 | 0.9651 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4590

## 验证集最佳点

```json
{
  "loss_total": 0.45904682809348357,
  "acc_main": 0.9447902571041948,
  "acc_turn": 0.5907983761840325,
  "acc_turn_pure": 0.6030809570632579,
  "acc_turn_transition": 0.532608695652174,
  "false_turn_straight": 0.5275467775467776,
  "flat_recall": 0.9482496194824962,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9512683578104139,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9482496194824962,
    0.42857142857142855,
    0.9512683578104139
  ],
  "turn_right_recall": 0.6208530805687204,
  "turn_straight_recall": 0.47245322245322247,
  "turn_left_recall": 0.8090614886731392,
  "recall_turn": [
    0.6208530805687204,
    0.47245322245322247,
    0.8090614886731392
  ],
  "cm_turn": [
    [
      524,
      194,
      126
    ],
    [
      374,
      909,
      641
    ],
    [
      80,
      97,
      750
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      623,
      0,
      34
    ],
    [
      0,
      18,
      24
    ],
    [
      140,
      6,
      2850
    ]
  ],
  "main_confidence_mean": 0.9641689001573668,
  "main_confidence_error_mean": 0.7188942343578043,
  "main_low_conf_0p60_ratio": 0.05385656292286874,
  "main_low_conf_0p70_ratio": 0.059810554803788905,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 199,
      "error_rate": 0.49748743718592964,
      "mean_confidence": 0.5174743149879028
    },
    {
      "bin": "[0.60,0.70)",
      "n": 22,
      "error_rate": 0.4090909090909091,
      "mean_confidence": 0.6426461938129411
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.35294117647058826,
      "mean_confidence": 0.7536085634545215
    },
    {
      "bin": "[0.80,0.90)",
      "n": 73,
      "error_rate": 0.2465753424657534,
      "mean_confidence": 0.8548804435068997
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3367,
      "error_rate": 0.019602019602019603,
      "mean_confidence": 0.9971664738941299
    }
  ],
  "turn_confidence_mean": 0.7518143449867607,
  "turn_confidence_error_mean": 0.6817297994122101,
  "turn_low_conf_0p60_ratio": 0.2722598105548038,
  "turn_low_conf_0p70_ratio": 0.3967523680649526,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1006,
      "error_rate": 0.5984095427435387,
      "mean_confidence": 0.5008581256241974
    },
    {
      "bin": "[0.60,0.70)",
      "n": 460,
      "error_rate": 0.46304347826086956,
      "mean_confidence": 0.6484950566378475
    },
    {
      "bin": "[0.70,0.80)",
      "n": 528,
      "error_rate": 0.44507575757575757,
      "mean_confidence": 0.7495597577592755
    },
    {
      "bin": "[0.80,0.90)",
      "n": 544,
      "error_rate": 0.3547794117647059,
      "mean_confidence": 0.8499557966167757
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1157,
      "error_rate": 0.23249783923941228,
      "mean_confidence": 0.965980552150652
    }
  ],
  "theta_mae_rad": 0.012511294335126877,
  "theta_mae_deg": 0.7168443202972412,
  "uphill_recall": 0.7784366576819407,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9739939775526965,
  "theta_flat_mae_deg": 0.910366415977478,
  "theta_flat_abs_p95_deg": 3.1789963245391846,
  "theta_flat_abs_max_deg": 5.98947286605835,
  "theta_flat_bias_deg": 0.17671719193458557,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.237114667892456,
  "theta_near_flat_abs_p95_deg": 3.1790823936462402,
  "theta_near_flat_abs_max_deg": 6.756316184997559,
  "theta_near_flat_bias_deg": 0.5304976105690002,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.006641149520874,
  "theta_flat_turn_abs_p95_deg": 3.1789963245391846,
  "theta_flat_turn_abs_max_deg": 5.326837062835693,
  "theta_flat_turn_bias_deg": 0.1335531771183014,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7168443202972412,
  "theta_slope_control_abs_p95_deg": 9.314350128173828,
  "theta_slope_control_abs_max_deg": 11.124480247497559,
  "theta_slope_control_bias_deg": -0.1596851497888565,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7168443202972412,
  "theta_all_rmse_deg": 1.0393165349960327,
  "theta_all_p95_abs_err_deg": 2.1992745399475098,
  "theta_all_max_abs_err_deg": 6.5164690017700195,
  "theta_all_bias_deg": -0.1596851497888565,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6744064688682556,
  "theta_active_abs_ge_2_rmse_deg": 0.9776713252067566,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9693574905395508,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.5164690017700195,
  "theta_active_abs_ge_2_bias_deg": -0.2334555983543396,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.743843138217926,
  "theta_abs_le_8_rmse_deg": 1.0637953281402588,
  "theta_abs_le_8_p95_abs_err_deg": 2.443303108215332,
  "theta_abs_le_8_max_abs_err_deg": 6.41701602935791,
  "theta_abs_le_8_bias_deg": -0.16640836000442505,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7168443202972412,
  "theta_abs_le_10_rmse_deg": 1.0393165349960327,
  "theta_abs_le_10_p95_abs_err_deg": 2.1992745399475098,
  "theta_abs_le_10_max_abs_err_deg": 6.5164690017700195,
  "theta_abs_le_10_bias_deg": -0.1596851497888565,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.552496612071991,
  "theta_pos_8_10_rmse_deg": 0.7482917308807373,
  "theta_pos_8_10_p95_abs_err_deg": 1.5808827877044678,
  "theta_pos_8_10_max_abs_err_deg": 3.7777175903320312,
  "theta_pos_8_10_bias_deg": -0.3111499547958374,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6542717814445496,
  "theta_neg_10_8_rmse_deg": 1.082265853881836,
  "theta_neg_10_8_p95_abs_err_deg": 1.7042291164398193,
  "theta_neg_10_8_max_abs_err_deg": 6.5164690017700195,
  "theta_neg_10_8_bias_deg": 0.05161372199654579,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6543199419975281,
  "theta_pos_6_8_rmse_deg": 0.9074204564094543,
  "theta_pos_6_8_p95_abs_err_deg": 1.7974144220352173,
  "theta_pos_6_8_max_abs_err_deg": 3.6792690753936768,
  "theta_pos_6_8_bias_deg": -0.293851375579834,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.619305431842804,
  "theta_neg_8_6_rmse_deg": 0.9177071452140808,
  "theta_neg_8_6_p95_abs_err_deg": 1.7134499549865723,
  "theta_neg_8_6_max_abs_err_deg": 6.0991082191467285,
  "theta_neg_8_6_bias_deg": -0.2122475653886795,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6940231919288635,
  "theta_neg_4_2_rmse_deg": 1.0057677030563354,
  "theta_neg_4_2_p95_abs_err_deg": 1.9590380191802979,
  "theta_neg_4_2_max_abs_err_deg": 6.41701602935791,
  "theta_neg_4_2_bias_deg": -0.3677366077899933,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.47361189126968384,
  "theta_neg_2_0p5_rmse_deg": 0.6800475120544434,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.288887619972229,
  "theta_neg_2_0p5_max_abs_err_deg": 3.8836522102355957,
  "theta_neg_2_0p5_bias_deg": -0.3222247362136841,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9990453720092773,
  "theta_pos_0p5_2_rmse_deg": 1.2097209692001343,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9137810468673706,
  "theta_pos_0p5_2_max_abs_err_deg": 4.21750020980835,
  "theta_pos_0p5_2_bias_deg": 0.33565810322761536,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.21656698945088057,
  "loss_turn": 1.009379096960344,
  "loss_theta": 0.00032908116129078276,
  "loss_main_bundle_base": 0.21656698945088057,
  "loss_turn_bundle_base": 0.24225097647861796,
  "loss_theta_bundle_base": 0.0002288651549608947,
  "loss_main_bundle": 0.21656698945088057,
  "loss_turn_bundle": 0.24225097647861796,
  "loss_theta_bundle": 0.0002288651549608947,
  "loss_theta_flat": 0.0002936538482379138,
  "loss_theta_near_flat": 0.0008752488582842405,
  "loss_theta_error_excess": 9.240143377814663e-05,
  "loss_theta_flat_excess": 0.00012022695129382656,
  "loss_theta_near_flat_excess": 0.0005597263781280737,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 7.632550995058729e-05,
  "loss_theta_small_neg": 0.00030405264482795635,
  "loss_theta_small_neg_excess": 7.854215071000365e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.44840440472666077,
  "loss_false_turn_straight": 0.35772576182072474,
  "loss_transition_focal_raw": 0.6695767068411242,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.3158889505726132,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
