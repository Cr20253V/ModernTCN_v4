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
  "lambda_theta": 0.5,
  "lambda_theta_flat": 0.1,
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
  "select_theta_edge_p95_weight": 1.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9647 |
| acc_turn | 0.5974 |
| acc_turn_pure | 0.6124 |
| acc_turn_transition | 0.5320 |
| main_confidence_mean | 0.9915 |
| main_low_conf_0p60_ratio | 0.0064 |
| main_low_conf_0p70_ratio | 0.0114 |
| turn_confidence_mean | 0.8584 |
| turn_low_conf_0p60_ratio | 0.1299 |
| turn_low_conf_0p70_ratio | 0.2082 |
| turn_right_recall | 0.5995 |
| turn_straight_recall | 0.5954 |
| turn_left_recall | 0.6000 |
| theta_mae_deg | 0.6035 |
| theta_abs_le_10_p95_abs_err_deg | 1.5208 |
| theta_neg_10_8_p95_abs_err_deg | 1.3894 |
| theta_pos_8_10_p95_abs_err_deg | 2.4170 |
| theta_abs_le_8_p95_abs_err_deg | 1.4723 |
| theta_neg_8_6_p95_abs_err_deg | 1.3982 |
| theta_pos_6_8_p95_abs_err_deg | 1.3489 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6041 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4771 |
| theta_flat_abs_p95_deg | 2.7540 |
| theta_flat_bias_deg | 0.5328 |
| theta_near_flat_abs_p95_deg | 2.0826 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.5912 |
| theta_flat_turn_abs_p95_deg | 1.9732 |
| flat_recall | 0.9577 |
| stall_recall | 0.6979 |
| slope_recall | 0.9760 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7523 |
| downhill_recall | 0.7968 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    724,
    0,
    32
  ],
  [
    11,
    67,
    18
  ],
  [
    57,
    9,
    2684
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    479,
    189,
    131
  ],
  [
    349,
    1151,
    433
  ],
  [
    149,
    199,
    522
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.406085 |
| test_loss_turn_bundle_base | 0.409794 |
| test_loss_theta_bundle_base | 0.000127 |
| test_loss_transition_focal_raw | 1.981815 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.466637 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 103
- train_seconds: 448.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 23 | 0.6522 | 0.5605 |
| [0.60,0.70) | 18 | 0.6111 | 0.6446 |
| [0.70,0.80) | 23 | 0.4348 | 0.7491 |
| [0.80,0.90) | 27 | 0.3333 | 0.8536 |
| [0.90,1.00) | 3511 | 0.0234 | 0.9987 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 468 | 0.5812 | 0.5230 |
| [0.60,0.70) | 282 | 0.5426 | 0.6497 |
| [0.70,0.80) | 340 | 0.4912 | 0.7520 |
| [0.80,0.90) | 439 | 0.5308 | 0.8530 |
| [0.90,1.00) | 2073 | 0.3015 | 0.9810 |


## 验证集最佳点

```json
{
  "loss_total": 0.7597802041670627,
  "acc_main": 0.9445196211096076,
  "acc_turn": 0.6554803788903925,
  "acc_turn_pure": 0.6728941330711242,
  "acc_turn_transition": 0.5729813664596274,
  "false_turn_straight": 0.38253638253638256,
  "flat_recall": 0.9528158295281582,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9506008010680908,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9528158295281582,
    0.38095238095238093,
    0.9506008010680908
  ],
  "turn_right_recall": 0.6445497630331753,
  "turn_straight_recall": 0.6174636174636174,
  "turn_left_recall": 0.7443365695792881,
  "recall_turn": [
    0.6445497630331753,
    0.6174636174636174,
    0.7443365695792881
  ],
  "cm_turn": [
    [
      544,
      216,
      84
    ],
    [
      300,
      1188,
      436
    ],
    [
      67,
      170,
      690
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      626,
      0,
      31
    ],
    [
      0,
      16,
      26
    ],
    [
      137,
      11,
      2848
    ]
  ],
  "main_confidence_mean": 0.9710201666774323,
  "main_confidence_error_mean": 0.7795115596959027,
  "main_low_conf_0p60_ratio": 0.0489851150202977,
  "main_low_conf_0p70_ratio": 0.05548037889039242,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 181,
      "error_rate": 0.46408839779005523,
      "mean_confidence": 0.531871983407225
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.20833333333333334,
      "mean_confidence": 0.6461859183099491
    },
    {
      "bin": "[0.70,0.80)",
      "n": 23,
      "error_rate": 0.2608695652173913,
      "mean_confidence": 0.763177412452901
    },
    {
      "bin": "[0.80,0.90)",
      "n": 27,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.8566827334836167
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3440,
      "error_rate": 0.028488372093023257,
      "mean_confidence": 0.9986798577170034
    }
  ],
  "turn_confidence_mean": 0.8729842270354278,
  "turn_confidence_error_mean": 0.7939724025899749,
  "turn_low_conf_0p60_ratio": 0.11502029769959404,
  "turn_low_conf_0p70_ratio": 0.17645466847090663,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 425,
      "error_rate": 0.6423529411764706,
      "mean_confidence": 0.4831080338360405
    },
    {
      "bin": "[0.60,0.70)",
      "n": 227,
      "error_rate": 0.4801762114537445,
      "mean_confidence": 0.6481299408897147
    },
    {
      "bin": "[0.70,0.80)",
      "n": 311,
      "error_rate": 0.5337620578778135,
      "mean_confidence": 0.7485193943751932
    },
    {
      "bin": "[0.80,0.90)",
      "n": 355,
      "error_rate": 0.428169014084507,
      "mean_confidence": 0.8533184930973038
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2377,
      "error_rate": 0.24106015986537652,
      "mean_confidence": 0.9833877624036163
    }
  ],
  "theta_mae_rad": 0.013522647321224213,
  "theta_mae_deg": 0.7747905850410461,
  "uphill_recall": 0.7773584905660378,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9622228305502327,
  "theta_flat_mae_deg": 1.1752510070800781,
  "theta_flat_abs_p95_deg": 4.198280334472656,
  "theta_flat_abs_max_deg": 6.025941371917725,
  "theta_flat_bias_deg": 0.8436276912689209,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5026050806045532,
  "theta_near_flat_abs_p95_deg": 4.198966979980469,
  "theta_near_flat_abs_max_deg": 6.382323265075684,
  "theta_near_flat_bias_deg": 1.17218017578125,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1013779640197754,
  "theta_flat_turn_abs_p95_deg": 4.198280334472656,
  "theta_flat_turn_abs_max_deg": 5.73104190826416,
  "theta_flat_turn_bias_deg": 0.6120756268501282,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7747905850410461,
  "theta_slope_control_abs_p95_deg": 9.160396575927734,
  "theta_slope_control_abs_max_deg": 12.243851661682129,
  "theta_slope_control_bias_deg": 0.2739608883857727,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7747905850410461,
  "theta_all_rmse_deg": 1.1980547904968262,
  "theta_all_p95_abs_err_deg": 2.805504560470581,
  "theta_all_max_abs_err_deg": 7.103650093078613,
  "theta_all_bias_deg": 0.2739608883857727,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6869726181030273,
  "theta_active_abs_ge_2_rmse_deg": 1.0677886009216309,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2485482692718506,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.103650093078613,
  "theta_active_abs_ge_2_bias_deg": 0.14903730154037476,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8185859322547913,
  "theta_abs_le_8_rmse_deg": 1.2488597631454468,
  "theta_abs_le_8_p95_abs_err_deg": 3.0496785640716553,
  "theta_abs_le_8_max_abs_err_deg": 6.494501113891602,
  "theta_abs_le_8_bias_deg": 0.3338705897331238,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7747905850410461,
  "theta_abs_le_10_rmse_deg": 1.1980547904968262,
  "theta_abs_le_10_p95_abs_err_deg": 2.805504560470581,
  "theta_abs_le_10_max_abs_err_deg": 7.103650093078613,
  "theta_abs_le_10_bias_deg": 0.2739608883857727,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5539109706878662,
  "theta_pos_8_10_rmse_deg": 0.7292445302009583,
  "theta_pos_8_10_p95_abs_err_deg": 1.257893681526184,
  "theta_pos_8_10_max_abs_err_deg": 4.513693332672119,
  "theta_pos_8_10_bias_deg": -0.24192868173122406,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6267872452735901,
  "theta_neg_10_8_rmse_deg": 1.1386656761169434,
  "theta_neg_10_8_p95_abs_err_deg": 1.8239139318466187,
  "theta_neg_10_8_max_abs_err_deg": 7.103650093078613,
  "theta_neg_10_8_bias_deg": 0.28893426060676575,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.4691682755947113,
  "theta_pos_6_8_rmse_deg": 0.6804718971252441,
  "theta_pos_6_8_p95_abs_err_deg": 1.3081550598144531,
  "theta_pos_6_8_max_abs_err_deg": 2.992323637008667,
  "theta_pos_6_8_bias_deg": 0.010560773313045502,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7431354522705078,
  "theta_neg_8_6_rmse_deg": 1.1181690692901611,
  "theta_neg_8_6_p95_abs_err_deg": 2.21244740486145,
  "theta_neg_8_6_max_abs_err_deg": 6.494501113891602,
  "theta_neg_8_6_bias_deg": 0.15047049522399902,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6302030086517334,
  "theta_neg_4_2_rmse_deg": 0.9089536070823669,
  "theta_neg_4_2_p95_abs_err_deg": 1.6803768873214722,
  "theta_neg_4_2_max_abs_err_deg": 5.319762706756592,
  "theta_neg_4_2_bias_deg": 0.10321547836065292,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.610809862613678,
  "theta_neg_2_0p5_rmse_deg": 0.8536125421524048,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4025306701660156,
  "theta_neg_2_0p5_max_abs_err_deg": 4.897871971130371,
  "theta_neg_2_0p5_bias_deg": 0.2738463282585144,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.424943447113037,
  "theta_pos_0p5_2_rmse_deg": 1.6960127353668213,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6982805728912354,
  "theta_pos_0p5_2_max_abs_err_deg": 4.253968715667725,
  "theta_pos_0p5_2_bias_deg": 1.1213555335998535,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.4150920602965581,
  "loss_turn": 1.7220950527991268,
  "loss_theta": 0.0004371849461635058,
  "loss_main_bundle_base": 0.4150920602965581,
  "loss_turn_bundle_base": 0.34441901976910594,
  "loss_theta_bundle_base": 0.0002691240572271029,
  "loss_main_bundle": 0.4150920602965581,
  "loss_turn_bundle": 0.34441901976910594,
  "loss_theta_bundle": 0.0002691240572271029,
  "loss_theta_flat": 0.00029893036235387893,
  "loss_theta_near_flat": 0.0013372172635862747,
  "loss_theta_error_excess": 0.00016626412182364547,
  "loss_theta_flat_excess": 0.0001640043314554223,
  "loss_theta_near_flat_excess": 0.0009592763616745038,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00012325336842379295,
  "loss_theta_small_neg": 0.0002484310470431342,
  "loss_theta_small_neg_excess": 5.8063461306802324e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3807355115152341,
  "loss_false_turn_straight": 0.277819433070326,
  "loss_transition_focal_raw": 1.749641947817254,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 5.057362062200012,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
