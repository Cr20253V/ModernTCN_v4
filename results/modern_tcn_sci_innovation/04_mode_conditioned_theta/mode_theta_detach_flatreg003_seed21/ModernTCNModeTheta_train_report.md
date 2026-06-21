# ModernTCN-small mode-conditioned theta experts 训练报告

## 固定约束

- model_family: `small_mode_theta`
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

## E4 Mode-Conditioned Theta Experts

- theta fusion: `sum(softmax(main_logits) * theta_experts)`.
- theta_gate_detach: `True`
- flat_theta_reg_lambda: `0.030000`
- theta_expert_hidden: `0`

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
  "theta_gate_detach": true,
  "flat_theta_reg_lambda": 0.03,
  "theta_expert_hidden": 0
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9584 |
| acc_turn | 0.5794 |
| acc_turn_pure | 0.5995 |
| acc_turn_transition | 0.4918 |
| main_confidence_mean | 0.9863 |
| main_low_conf_0p60_ratio | 0.0069 |
| main_low_conf_0p70_ratio | 0.0144 |
| turn_confidence_mean | 0.8162 |
| turn_low_conf_0p60_ratio | 0.1810 |
| turn_low_conf_0p70_ratio | 0.2998 |
| turn_right_recall | 0.5820 |
| turn_straight_recall | 0.6301 |
| turn_left_recall | 0.4644 |
| theta_mae_deg | 0.6669 |
| theta_abs_le_10_p95_abs_err_deg | 1.7276 |
| theta_neg_10_8_p95_abs_err_deg | 1.2815 |
| theta_pos_8_10_p95_abs_err_deg | 2.8699 |
| theta_abs_le_8_p95_abs_err_deg | 1.6052 |
| theta_neg_8_6_p95_abs_err_deg | 1.2356 |
| theta_pos_6_8_p95_abs_err_deg | 1.4528 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8835 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5882 |
| theta_flat_abs_p95_deg | 2.7307 |
| theta_flat_bias_deg | -0.2693 |
| theta_near_flat_abs_p95_deg | 1.4473 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0125 |
| theta_flat_turn_abs_p95_deg | 1.2719 |
| flat_recall | 0.9365 |
| stall_recall | 0.7083 |
| slope_recall | 0.9731 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7511 |
| downhill_recall | 0.8019 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    708,
    1,
    47
  ],
  [
    8,
    68,
    20
  ],
  [
    64,
    10,
    2676
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    465,
    253,
    81
  ],
  [
    383,
    1218,
    332
  ],
  [
    175,
    291,
    404
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.324966 |
| test_loss_turn_bundle_base | 0.341418 |
| test_loss_theta_bundle_base | 0.000236 |
| test_loss_transition_focal_raw | 1.492911 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.294024 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000470 |
| test_loss_flat_theta_expert_reg_weighted | 0.000014 |

- best_epoch: 65
- train_seconds: 313.4

## E3 Gate Statistics

| metric | value |
|---|---:|
| test_gate_all_finite | nan |
| test_gate_single_collapse | nan |
| test_gate_mean_entropy | nan |
| test_gate_interpretability_score | nan |
| test_gate_yaw_transition_minus_overall | nan |
| test_gate_drive_stall_minus_overall | nan |
| test_gate_velocity_slope_flat_abs_delta | nan |

```json
{}
```

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 25 | 0.6000 | 0.5547 |
| [0.60,0.70) | 27 | 0.4815 | 0.6515 |
| [0.70,0.80) | 49 | 0.6122 | 0.7513 |
| [0.80,0.90) | 64 | 0.3125 | 0.8613 |
| [0.90,1.00) | 3437 | 0.0209 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 652 | 0.6227 | 0.5271 |
| [0.60,0.70) | 428 | 0.5304 | 0.6499 |
| [0.70,0.80) | 380 | 0.5684 | 0.7510 |
| [0.80,0.90) | 452 | 0.4757 | 0.8519 |
| [0.90,1.00) | 1690 | 0.2669 | 0.9749 |


## 验证集最佳点

```json
{
  "loss_total": 0.5572740459151778,
  "acc_main": 0.9456021650879567,
  "acc_turn": 0.6535859269282814,
  "acc_turn_pure": 0.6601114388725008,
  "acc_turn_transition": 0.6226708074534162,
  "false_turn_straight": 0.3477130977130977,
  "flat_recall": 0.9421613394216134,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9546061415220294,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9421613394216134,
    0.35714285714285715,
    0.9546061415220294
  ],
  "turn_right_recall": 0.6741706161137441,
  "turn_straight_recall": 0.6522869022869023,
  "turn_left_recall": 0.6375404530744336,
  "recall_turn": [
    0.6741706161137441,
    0.6522869022869023,
    0.6375404530744336
  ],
  "cm_turn": [
    [
      569,
      256,
      19
    ],
    [
      356,
      1255,
      313
    ],
    [
      97,
      239,
      591
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      619,
      0,
      38
    ],
    [
      0,
      15,
      27
    ],
    [
      123,
      13,
      2860
    ]
  ],
  "main_confidence_mean": 0.9676980024016011,
  "main_confidence_error_mean": 0.7493868903733428,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.05764546684709066,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4484536082474227,
      "mean_confidence": 0.5245530986375524
    },
    {
      "bin": "[0.60,0.70)",
      "n": 19,
      "error_rate": 0.3157894736842105,
      "mean_confidence": 0.6565218380153415
    },
    {
      "bin": "[0.70,0.80)",
      "n": 25,
      "error_rate": 0.44,
      "mean_confidence": 0.7470278155842301
    },
    {
      "bin": "[0.80,0.90)",
      "n": 46,
      "error_rate": 0.34782608695652173,
      "mean_confidence": 0.8491052591371857
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3411,
      "error_rate": 0.023746701846965697,
      "mean_confidence": 0.9978517635608393
    }
  ],
  "turn_confidence_mean": 0.8318542827077191,
  "turn_confidence_error_mean": 0.7546012368938918,
  "turn_low_conf_0p60_ratio": 0.1634641407307172,
  "turn_low_conf_0p70_ratio": 0.25602165087956696,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 604,
      "error_rate": 0.5728476821192053,
      "mean_confidence": 0.5061211941418761
    },
    {
      "bin": "[0.60,0.70)",
      "n": 342,
      "error_rate": 0.48830409356725146,
      "mean_confidence": 0.6486871814697892
    },
    {
      "bin": "[0.70,0.80)",
      "n": 351,
      "error_rate": 0.43304843304843305,
      "mean_confidence": 0.7503309272688335
    },
    {
      "bin": "[0.80,0.90)",
      "n": 483,
      "error_rate": 0.4140786749482402,
      "mean_confidence": 0.8530393238748246
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1915,
      "error_rate": 0.21671018276762402,
      "mean_confidence": 0.9769029808761149
    }
  ],
  "theta_mae_rad": 0.013532668352127075,
  "theta_mae_deg": 0.7753647565841675,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8075639599555061,
  "slope_sign_acc": 0.9734464823432795,
  "theta_flat_mae_deg": 0.8512526750564575,
  "theta_flat_abs_p95_deg": 2.5460426807403564,
  "theta_flat_abs_max_deg": 9.947822570800781,
  "theta_flat_bias_deg": 0.3821171522140503,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.578355312347412,
  "theta_near_flat_abs_p95_deg": 4.871059894561768,
  "theta_near_flat_abs_max_deg": 31.96359634399414,
  "theta_near_flat_bias_deg": 1.202038288116455,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1736762523651123,
  "theta_flat_turn_abs_p95_deg": 3.48569655418396,
  "theta_flat_turn_abs_max_deg": 9.947822570800781,
  "theta_flat_turn_bias_deg": 0.7868260145187378,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7753647565841675,
  "theta_slope_control_abs_p95_deg": 9.142279624938965,
  "theta_slope_control_abs_max_deg": 17.108905792236328,
  "theta_slope_control_bias_deg": -0.019994085654616356,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7753646969795227,
  "theta_all_rmse_deg": 1.196006178855896,
  "theta_all_p95_abs_err_deg": 2.2631165981292725,
  "theta_all_max_abs_err_deg": 13.709207534790039,
  "theta_all_bias_deg": -0.019994089379906654,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7587229609489441,
  "theta_active_abs_ge_2_rmse_deg": 1.1669039726257324,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2877116203308105,
  "theta_active_abs_ge_2_max_abs_err_deg": 13.709207534790039,
  "theta_active_abs_ge_2_bias_deg": -0.10817401856184006,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7934327125549316,
  "theta_abs_le_8_rmse_deg": 1.2155561447143555,
  "theta_abs_le_8_p95_abs_err_deg": 2.359208583831787,
  "theta_abs_le_8_max_abs_err_deg": 13.709207534790039,
  "theta_abs_le_8_bias_deg": 0.005746312905102968,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7753646969795227,
  "theta_abs_le_10_rmse_deg": 1.196006178855896,
  "theta_abs_le_10_p95_abs_err_deg": 2.2631165981292725,
  "theta_abs_le_10_max_abs_err_deg": 13.709207534790039,
  "theta_abs_le_10_bias_deg": -0.019994089379906654,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7380459904670715,
  "theta_pos_8_10_rmse_deg": 1.042345404624939,
  "theta_pos_8_10_p95_abs_err_deg": 1.4657188653945923,
  "theta_pos_8_10_max_abs_err_deg": 8.25499153137207,
  "theta_pos_8_10_bias_deg": -0.46596962213516235,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6595680713653564,
  "theta_neg_10_8_rmse_deg": 1.1743543148040771,
  "theta_neg_10_8_p95_abs_err_deg": 2.418438196182251,
  "theta_neg_10_8_max_abs_err_deg": 7.596320152282715,
  "theta_neg_10_8_bias_deg": 0.2146398425102234,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7551097869873047,
  "theta_pos_6_8_rmse_deg": 0.9816879630088806,
  "theta_pos_6_8_p95_abs_err_deg": 1.9058616161346436,
  "theta_pos_6_8_max_abs_err_deg": 3.5946567058563232,
  "theta_pos_6_8_bias_deg": -0.34140071272850037,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.701266884803772,
  "theta_neg_8_6_rmse_deg": 1.1786595582962036,
  "theta_neg_8_6_p95_abs_err_deg": 2.1666882038116455,
  "theta_neg_8_6_max_abs_err_deg": 9.653827667236328,
  "theta_neg_8_6_bias_deg": 0.12835779786109924,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6871177554130554,
  "theta_neg_4_2_rmse_deg": 1.0118404626846313,
  "theta_neg_4_2_p95_abs_err_deg": 2.0350935459136963,
  "theta_neg_4_2_max_abs_err_deg": 5.340812683105469,
  "theta_neg_4_2_bias_deg": 0.08085206151008606,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5770595669746399,
  "theta_neg_2_0p5_rmse_deg": 0.7449507117271423,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1765804290771484,
  "theta_neg_2_0p5_max_abs_err_deg": 4.861213684082031,
  "theta_neg_2_0p5_bias_deg": 0.037888459861278534,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.7118200659751892,
  "theta_pos_0p5_2_rmse_deg": 0.8337453007698059,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.4838387966156006,
  "theta_pos_0p5_2_max_abs_err_deg": 3.43088698387146,
  "theta_pos_0p5_2_bias_deg": 0.17192299664020538,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.27966836294882674,
  "loss_turn": 1.3864094249934402,
  "loss_theta": 0.0004357588293515423,
  "loss_main_bundle_base": 0.27966836294882674,
  "loss_turn_bundle_base": 0.27728189355384997,
  "loss_theta_bundle_base": 0.00029812713247548704,
  "loss_main_bundle": 0.27966836294882674,
  "loss_turn_bundle": 0.27728189355384997,
  "loss_theta_bundle": 0.000323788982150315,
  "loss_theta_flat": 0.0002816633355371523,
  "loss_theta_near_flat": 0.0010012125899966084,
  "loss_theta_error_excess": 0.00017434645736807736,
  "loss_theta_flat_excess": 0.00011649550169934606,
  "loss_theta_near_flat_excess": 0.0006917302508231036,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00015942851332043385,
  "loss_theta_small_neg": 0.0003088208734270825,
  "loss_theta_small_neg_excess": 8.615473959667744e-05,
  "loss_flat_theta_expert_reg": 0.0008553949870605209,
  "loss_flat_theta_expert_reg_weighted": 2.5661849137253842e-05,
  "loss_turn_release": 0.3082216050369975,
  "loss_false_turn_straight": 0.2565284002214388,
  "loss_transition_focal_raw": 1.0982098676193712,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.4993761885039136,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
