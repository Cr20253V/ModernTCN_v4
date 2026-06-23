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
  "lambda_theta": 0.65,
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
| acc_main | 0.9681 |
| acc_turn | 0.5869 |
| acc_turn_pure | 0.6063 |
| acc_turn_transition | 0.5022 |
| main_confidence_mean | 0.9892 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0144 |
| turn_confidence_mean | 0.8360 |
| turn_low_conf_0p60_ratio | 0.1435 |
| turn_low_conf_0p70_ratio | 0.2401 |
| turn_right_recall | 0.5995 |
| turn_straight_recall | 0.5820 |
| turn_left_recall | 0.5862 |
| theta_mae_deg | 0.5384 |
| theta_abs_le_10_p95_abs_err_deg | 1.5189 |
| theta_neg_10_8_p95_abs_err_deg | 1.3566 |
| theta_pos_8_10_p95_abs_err_deg | 2.1585 |
| theta_abs_le_8_p95_abs_err_deg | 1.4372 |
| theta_neg_8_6_p95_abs_err_deg | 1.2910 |
| theta_pos_6_8_p95_abs_err_deg | 1.4910 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4203 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5866 |
| theta_flat_abs_p95_deg | 2.4163 |
| theta_flat_bias_deg | 0.0808 |
| theta_near_flat_abs_p95_deg | 1.5990 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2050 |
| theta_flat_turn_abs_p95_deg | 1.5249 |
| flat_recall | 0.9537 |
| stall_recall | 0.6354 |
| slope_recall | 0.9836 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7655 |
| downhill_recall | 0.7974 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    0,
    35
  ],
  [
    11,
    61,
    24
  ],
  [
    41,
    4,
    2705
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
    390,
    1125,
    418
  ],
  [
    155,
    205,
    510
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.379189 |
| test_loss_turn_bundle_base | 0.329923 |
| test_loss_theta_bundle_base | 0.000132 |
| test_loss_transition_focal_raw | 1.576566 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.370422 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 382.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.2500 | 0.5426 |
| [0.60,0.70) | 28 | 0.5714 | 0.6595 |
| [0.70,0.80) | 23 | 0.2609 | 0.7511 |
| [0.80,0.90) | 39 | 0.2308 | 0.8527 |
| [0.90,1.00) | 3488 | 0.0224 | 0.9981 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 517 | 0.6015 | 0.5236 |
| [0.60,0.70) | 348 | 0.6063 | 0.6541 |
| [0.70,0.80) | 431 | 0.4919 | 0.7508 |
| [0.80,0.90) | 488 | 0.4201 | 0.8492 |
| [0.90,1.00) | 1818 | 0.3020 | 0.9763 |


## 验证集最佳点

```json
{
  "loss_total": 0.6273691880686841,
  "acc_main": 0.9412719891745602,
  "acc_turn": 0.6230040595399188,
  "acc_turn_pure": 0.63913470993117,
  "acc_turn_transition": 0.546583850931677,
  "false_turn_straight": 0.43347193347193347,
  "flat_recall": 0.9269406392694064,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.951935914552737,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9269406392694064,
    0.40476190476190477,
    0.951935914552737
  ],
  "turn_right_recall": 0.6433649289099526,
  "turn_straight_recall": 0.5665280665280665,
  "turn_left_recall": 0.7216828478964401,
  "recall_turn": [
    0.6433649289099526,
    0.5665280665280665,
    0.7216828478964401
  ],
  "cm_turn": [
    [
      543,
      216,
      85
    ],
    [
      346,
      1090,
      488
    ],
    [
      74,
      184,
      669
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
      17,
      25
    ],
    [
      133,
      11,
      2852
    ]
  ],
  "main_confidence_mean": 0.9708306795477066,
  "main_confidence_error_mean": 0.7786962993432628,
  "main_low_conf_0p60_ratio": 0.0516914749661705,
  "main_low_conf_0p70_ratio": 0.059810554803788905,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 191,
      "error_rate": 0.4869109947643979,
      "mean_confidence": 0.5798504102916909
    },
    {
      "bin": "[0.60,0.70)",
      "n": 30,
      "error_rate": 0.4,
      "mean_confidence": 0.6570638743311231
    },
    {
      "bin": "[0.70,0.80)",
      "n": 26,
      "error_rate": 0.2692307692307692,
      "mean_confidence": 0.7543959713975636
    },
    {
      "bin": "[0.80,0.90)",
      "n": 36,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8575456610365139
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3412,
      "error_rate": 0.027256740914419694,
      "mean_confidence": 0.9983206557091087
    }
  ],
  "turn_confidence_mean": 0.8509808152384593,
  "turn_confidence_error_mean": 0.7781748386404278,
  "turn_low_conf_0p60_ratio": 0.12855209742895804,
  "turn_low_conf_0p70_ratio": 0.2178619756427605,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 475,
      "error_rate": 0.6505263157894737,
      "mean_confidence": 0.5036055074688067
    },
    {
      "bin": "[0.60,0.70)",
      "n": 330,
      "error_rate": 0.5212121212121212,
      "mean_confidence": 0.6509527782990465
    },
    {
      "bin": "[0.70,0.80)",
      "n": 369,
      "error_rate": 0.4986449864498645,
      "mean_confidence": 0.750410970087555
    },
    {
      "bin": "[0.80,0.90)",
      "n": 463,
      "error_rate": 0.4535637149028078,
      "mean_confidence": 0.8524772863435028
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2058,
      "error_rate": 0.25170068027210885,
      "mean_confidence": 0.9809273313315785
    }
  ],
  "theta_mae_rad": 0.01217740960419178,
  "theta_mae_deg": 0.6977141499519348,
  "uphill_recall": 0.7805929919137466,
  "downhill_recall": 0.8075639599555061,
  "slope_sign_acc": 0.9674240350396934,
  "theta_flat_mae_deg": 1.043945074081421,
  "theta_flat_abs_p95_deg": 4.055437088012695,
  "theta_flat_abs_max_deg": 8.278863906860352,
  "theta_flat_bias_deg": 0.49025943875312805,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4999659061431885,
  "theta_near_flat_abs_p95_deg": 4.085360050201416,
  "theta_near_flat_abs_max_deg": 8.278863906860352,
  "theta_near_flat_bias_deg": 0.9492422342300415,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1858842372894287,
  "theta_flat_turn_abs_p95_deg": 4.055437088012695,
  "theta_flat_turn_abs_max_deg": 8.278863906860352,
  "theta_flat_turn_bias_deg": 0.3041402995586395,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.6977141499519348,
  "theta_slope_control_abs_p95_deg": 9.313443183898926,
  "theta_slope_control_abs_max_deg": 11.073131561279297,
  "theta_slope_control_bias_deg": 0.20779825747013092,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.6977142095565796,
  "theta_all_rmse_deg": 1.1092720031738281,
  "theta_all_p95_abs_err_deg": 2.5554370880126953,
  "theta_all_max_abs_err_deg": 7.77886438369751,
  "theta_all_bias_deg": 0.20779825747013092,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6217883825302124,
  "theta_active_abs_ge_2_rmse_deg": 0.9559771418571472,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.015223503112793,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.897023677825928,
  "theta_active_abs_ge_2_bias_deg": 0.14585669338703156,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7309426665306091,
  "theta_abs_le_8_rmse_deg": 1.1465495824813843,
  "theta_abs_le_8_p95_abs_err_deg": 2.652130603790283,
  "theta_abs_le_8_max_abs_err_deg": 7.77886438369751,
  "theta_abs_le_8_bias_deg": 0.20324616134166718,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.6977142095565796,
  "theta_abs_le_10_rmse_deg": 1.1092720031738281,
  "theta_abs_le_10_p95_abs_err_deg": 2.5554370880126953,
  "theta_abs_le_10_max_abs_err_deg": 7.77886438369751,
  "theta_abs_le_10_bias_deg": 0.20779825747013092,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.45570188760757446,
  "theta_pos_8_10_rmse_deg": 0.6781280040740967,
  "theta_pos_8_10_p95_abs_err_deg": 1.5037477016448975,
  "theta_pos_8_10_max_abs_err_deg": 3.572120428085327,
  "theta_pos_8_10_bias_deg": -0.004212013445794582,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6611340641975403,
  "theta_neg_10_8_rmse_deg": 1.1396533250808716,
  "theta_neg_10_8_p95_abs_err_deg": 2.3140547275543213,
  "theta_neg_10_8_max_abs_err_deg": 6.897023677825928,
  "theta_neg_10_8_bias_deg": 0.4622131586074829,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.48260587453842163,
  "theta_pos_6_8_rmse_deg": 0.7444696426391602,
  "theta_pos_6_8_p95_abs_err_deg": 1.4403506517410278,
  "theta_pos_6_8_max_abs_err_deg": 3.626185655593872,
  "theta_pos_6_8_bias_deg": 0.06371595710515976,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7862220406532288,
  "theta_neg_8_6_rmse_deg": 1.1277762651443481,
  "theta_neg_8_6_p95_abs_err_deg": 2.288422107696533,
  "theta_neg_8_6_max_abs_err_deg": 6.6851067543029785,
  "theta_neg_8_6_bias_deg": 0.458116352558136,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6589676737785339,
  "theta_neg_4_2_rmse_deg": 0.9534016847610474,
  "theta_neg_4_2_p95_abs_err_deg": 2.0511043071746826,
  "theta_neg_4_2_max_abs_err_deg": 4.671046733856201,
  "theta_neg_4_2_bias_deg": -0.218085378408432,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.4924699068069458,
  "theta_neg_2_0p5_rmse_deg": 0.761078953742981,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5194220542907715,
  "theta_neg_2_0p5_max_abs_err_deg": 4.883296012878418,
  "theta_neg_2_0p5_bias_deg": -0.06047385558485985,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0210245847702026,
  "theta_pos_0p5_2_rmse_deg": 1.4316766262054443,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5554370880126953,
  "theta_pos_0p5_2_max_abs_err_deg": 4.591259002685547,
  "theta_pos_0p5_2_bias_deg": 0.5013987421989441,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3249729779318318,
  "loss_turn": 1.5105697462458734,
  "loss_theta": 0.0003748610175904063,
  "loss_main_bundle_base": 0.3249729779318318,
  "loss_turn_bundle_base": 0.302113953736864,
  "loss_theta_bundle_base": 0.00028226766187895507,
  "loss_main_bundle": 0.3249729779318318,
  "loss_turn_bundle": 0.302113953736864,
  "loss_theta_bundle": 0.00028226766187895507,
  "loss_theta_flat": 0.00019117356419743134,
  "loss_theta_near_flat": 0.0014260964640775374,
  "loss_theta_error_excess": 0.00014045782297779081,
  "loss_theta_flat_excess": 0.00011586339127847986,
  "loss_theta_near_flat_excess": 0.0010488354176262718,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.644286165017375e-05,
  "loss_theta_small_neg": 0.00027283099801336314,
  "loss_theta_small_neg_excess": 7.095753346161516e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3973220970537085,
  "loss_false_turn_straight": 0.3261289828039797,
  "loss_transition_focal_raw": 1.271969233152831,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.186890978209866,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
