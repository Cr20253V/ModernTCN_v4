# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `fixed`
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
| acc_main | 0.9647 |
| acc_turn | 0.5652 |
| acc_turn_pure | 0.5855 |
| acc_turn_transition | 0.4769 |
| main_confidence_mean | 0.9866 |
| main_low_conf_0p60_ratio | 0.0097 |
| main_low_conf_0p70_ratio | 0.0167 |
| turn_confidence_mean | 0.7999 |
| turn_low_conf_0p60_ratio | 0.1929 |
| turn_low_conf_0p70_ratio | 0.3134 |
| turn_right_recall | 0.5770 |
| turn_straight_recall | 0.5582 |
| turn_left_recall | 0.5701 |
| theta_mae_deg | 0.6631 |
| theta_abs_le_10_p95_abs_err_deg | 1.7305 |
| theta_neg_10_8_p95_abs_err_deg | 1.1165 |
| theta_pos_8_10_p95_abs_err_deg | 2.3458 |
| theta_abs_le_8_p95_abs_err_deg | 1.7219 |
| theta_neg_8_6_p95_abs_err_deg | 1.0507 |
| theta_pos_6_8_p95_abs_err_deg | 1.4760 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4415 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0919 |
| theta_flat_abs_p95_deg | 2.6594 |
| theta_flat_bias_deg | -0.1706 |
| theta_near_flat_abs_p95_deg | 1.8660 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2955 |
| theta_flat_turn_abs_p95_deg | 1.9715 |
| flat_recall | 0.9603 |
| stall_recall | 0.6354 |
| slope_recall | 0.9775 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7592 |
| downhill_recall | 0.7911 |

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
    61,
    26
  ],
  [
    50,
    12,
    2688
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    461,
    195,
    143
  ],
  [
    376,
    1079,
    478
  ],
  [
    210,
    164,
    496
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.303320 |
| test_loss_turn_bundle_base | 0.290922 |
| test_loss_theta_bundle_base | 0.000183 |
| test_loss_transition_focal_raw | 1.223776 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.368397 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 52
- train_seconds: 266.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 35 | 0.5429 | 0.5529 |
| [0.60,0.70) | 25 | 0.6400 | 0.6533 |
| [0.70,0.80) | 29 | 0.4138 | 0.7625 |
| [0.80,0.90) | 43 | 0.2326 | 0.8634 |
| [0.90,1.00) | 3470 | 0.0202 | 0.9967 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 695 | 0.6072 | 0.5132 |
| [0.60,0.70) | 434 | 0.5046 | 0.6505 |
| [0.70,0.80) | 490 | 0.4755 | 0.7481 |
| [0.80,0.90) | 469 | 0.4371 | 0.8525 |
| [0.90,1.00) | 1514 | 0.3217 | 0.9748 |


## 验证集最佳点

```json
{
  "loss_total": 0.5514534609082264,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.6081190798376184,
  "acc_turn_pure": 0.6207800721075057,
  "acc_turn_transition": 0.5481366459627329,
  "false_turn_straight": 0.4734927234927235,
  "flat_recall": 0.9345509893455098,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9549399198931909,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9345509893455098,
    0.42857142857142855,
    0.9549399198931909
  ],
  "turn_right_recall": 0.6860189573459715,
  "turn_straight_recall": 0.5265072765072765,
  "turn_left_recall": 0.7065803667745415,
  "recall_turn": [
    0.6860189573459715,
    0.5265072765072765,
    0.7065803667745415
  ],
  "cm_turn": [
    [
      579,
      181,
      84
    ],
    [
      440,
      1013,
      471
    ],
    [
      132,
      140,
      655
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      614,
      0,
      43
    ],
    [
      0,
      18,
      24
    ],
    [
      119,
      16,
      2861
    ]
  ],
  "main_confidence_mean": 0.9670649812820251,
  "main_confidence_error_mean": 0.7536993424259933,
  "main_low_conf_0p60_ratio": 0.05196211096075778,
  "main_low_conf_0p70_ratio": 0.05872801082543978,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 192,
      "error_rate": 0.453125,
      "mean_confidence": 0.5438229795698449
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.48,
      "mean_confidence": 0.6548238272931198
    },
    {
      "bin": "[0.70,0.80)",
      "n": 40,
      "error_rate": 0.3,
      "mean_confidence": 0.7521296298149313
    },
    {
      "bin": "[0.80,0.90)",
      "n": 49,
      "error_rate": 0.24489795918367346,
      "mean_confidence": 0.8553926434243556
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3389,
      "error_rate": 0.023310711124225437,
      "mean_confidence": 0.9974981036757019
    }
  ],
  "turn_confidence_mean": 0.8308514650992321,
  "turn_confidence_error_mean": 0.7722624426765614,
  "turn_low_conf_0p60_ratio": 0.15426251691474965,
  "turn_low_conf_0p70_ratio": 0.24303112313937753,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 570,
      "error_rate": 0.5982456140350877,
      "mean_confidence": 0.49752663737748914
    },
    {
      "bin": "[0.60,0.70)",
      "n": 328,
      "error_rate": 0.49085365853658536,
      "mean_confidence": 0.6538627373818271
    },
    {
      "bin": "[0.70,0.80)",
      "n": 410,
      "error_rate": 0.4585365853658537,
      "mean_confidence": 0.7496394066942466
    },
    {
      "bin": "[0.80,0.90)",
      "n": 547,
      "error_rate": 0.4606946983546618,
      "mean_confidence": 0.8561103471416878
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1840,
      "error_rate": 0.275,
      "mean_confidence": 0.9762470031217988
    }
  ],
  "theta_mae_rad": 0.014727411791682243,
  "theta_mae_deg": 0.8438184857368469,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.8103448275862069,
  "slope_sign_acc": 0.9786476868327402,
  "theta_flat_mae_deg": 1.3202800750732422,
  "theta_flat_abs_p95_deg": 4.15510892868042,
  "theta_flat_abs_max_deg": 11.374051094055176,
  "theta_flat_bias_deg": 0.4987495541572571,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.8003778457641602,
  "theta_near_flat_abs_p95_deg": 6.350964069366455,
  "theta_near_flat_abs_max_deg": 11.374051094055176,
  "theta_near_flat_bias_deg": 0.7004470229148865,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.5358428955078125,
  "theta_flat_turn_abs_p95_deg": 6.490353584289551,
  "theta_flat_turn_abs_max_deg": 11.374051094055176,
  "theta_flat_turn_bias_deg": -0.19161538779735565,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8438184857368469,
  "theta_slope_control_abs_p95_deg": 9.28738784790039,
  "theta_slope_control_abs_max_deg": 12.210803985595703,
  "theta_slope_control_bias_deg": 0.08742038905620575,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8438184261322021,
  "theta_all_rmse_deg": 1.3371660709381104,
  "theta_all_p95_abs_err_deg": 2.826563596725464,
  "theta_all_max_abs_err_deg": 10.874052047729492,
  "theta_all_bias_deg": 0.08742038905620575,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7393341064453125,
  "theta_active_abs_ge_2_rmse_deg": 1.0823110342025757,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2265706062316895,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.134095668792725,
  "theta_active_abs_ge_2_bias_deg": -0.0027809753082692623,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8808059692382812,
  "theta_abs_le_8_rmse_deg": 1.3917912244796753,
  "theta_abs_le_8_p95_abs_err_deg": 3.002068519592285,
  "theta_abs_le_8_max_abs_err_deg": 10.874052047729492,
  "theta_abs_le_8_bias_deg": 0.13189108669757843,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8438184261322021,
  "theta_abs_le_10_rmse_deg": 1.3371660709381104,
  "theta_abs_le_10_p95_abs_err_deg": 2.826563596725464,
  "theta_abs_le_10_max_abs_err_deg": 10.874052047729492,
  "theta_abs_le_10_bias_deg": 0.08742038905620575,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6717913150787354,
  "theta_pos_8_10_rmse_deg": 0.9029703140258789,
  "theta_pos_8_10_p95_abs_err_deg": 2.0702147483825684,
  "theta_pos_8_10_max_abs_err_deg": 3.7694668769836426,
  "theta_pos_8_10_bias_deg": -0.32169395685195923,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7040536999702454,
  "theta_neg_10_8_rmse_deg": 1.2283693552017212,
  "theta_neg_10_8_p95_abs_err_deg": 2.3112552165985107,
  "theta_neg_10_8_max_abs_err_deg": 7.134095668792725,
  "theta_neg_10_8_bias_deg": 0.12515932321548462,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.656851589679718,
  "theta_pos_6_8_rmse_deg": 0.9397088885307312,
  "theta_pos_6_8_p95_abs_err_deg": 1.917717456817627,
  "theta_pos_6_8_max_abs_err_deg": 4.076559066772461,
  "theta_pos_6_8_bias_deg": -0.07663926482200623,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6497942805290222,
  "theta_neg_8_6_rmse_deg": 1.002524971961975,
  "theta_neg_8_6_p95_abs_err_deg": 1.896148443222046,
  "theta_neg_8_6_max_abs_err_deg": 6.337076663970947,
  "theta_neg_8_6_bias_deg": -0.0553596168756485,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7410216331481934,
  "theta_neg_4_2_rmse_deg": 1.101415753364563,
  "theta_neg_4_2_p95_abs_err_deg": 2.039414644241333,
  "theta_neg_4_2_max_abs_err_deg": 5.96598482131958,
  "theta_neg_4_2_bias_deg": -0.2862571179866791,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5348116755485535,
  "theta_neg_2_0p5_rmse_deg": 0.764678418636322,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2597953081130981,
  "theta_neg_2_0p5_max_abs_err_deg": 5.1796488761901855,
  "theta_neg_2_0p5_bias_deg": -0.0032811607234179974,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4747055768966675,
  "theta_pos_0p5_2_rmse_deg": 1.8167674541473389,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6551053524017334,
  "theta_pos_0p5_2_max_abs_err_deg": 4.784787654876709,
  "theta_pos_0p5_2_bias_deg": 0.9471169710159302,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.29296045096865847,
  "loss_turn": 1.290627546368497,
  "loss_theta": 0.0005444659997995172,
  "loss_main_bundle_base": 0.29296045096865847,
  "loss_turn_bundle_base": 0.2581255177119104,
  "loss_theta_bundle_base": 0.00036748598091221123,
  "loss_main_bundle": 0.29296045096865847,
  "loss_turn_bundle": 0.2581255177119104,
  "loss_theta_bundle": 0.00036748598091221123,
  "loss_theta_flat": 0.00037138207404195623,
  "loss_theta_near_flat": 0.002415087936554452,
  "loss_theta_error_excess": 0.00024048386810218892,
  "loss_theta_flat_excess": 0.00019252245563298372,
  "loss_theta_near_flat_excess": 0.0019193737315208084,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011439623018705912,
  "loss_theta_small_neg": 0.0003643660465380144,
  "loss_theta_small_neg_excess": 0.00012282238852898104,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4265918723623872,
  "loss_false_turn_straight": 0.36127507772916706,
  "loss_transition_focal_raw": 1.0205856992524112,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.657667851562411,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
