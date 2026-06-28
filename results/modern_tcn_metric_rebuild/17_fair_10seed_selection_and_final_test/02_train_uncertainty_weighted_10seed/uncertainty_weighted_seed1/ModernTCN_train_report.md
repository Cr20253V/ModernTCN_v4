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
| acc_main | 0.9667 |
| acc_turn | 0.6127 |
| acc_turn_pure | 0.6308 |
| acc_turn_transition | 0.5335 |
| main_confidence_mean | 0.9896 |
| main_low_conf_0p60_ratio | 0.0086 |
| main_low_conf_0p70_ratio | 0.0125 |
| turn_confidence_mean | 0.8634 |
| turn_low_conf_0p60_ratio | 0.1113 |
| turn_low_conf_0p70_ratio | 0.2052 |
| turn_right_recall | 0.5332 |
| turn_straight_recall | 0.6482 |
| turn_left_recall | 0.6069 |
| theta_mae_deg | 0.6703 |
| theta_abs_le_10_p95_abs_err_deg | 1.7621 |
| theta_neg_10_8_p95_abs_err_deg | 1.2859 |
| theta_pos_8_10_p95_abs_err_deg | 3.5987 |
| theta_abs_le_8_p95_abs_err_deg | 1.7028 |
| theta_neg_8_6_p95_abs_err_deg | 1.5327 |
| theta_pos_6_8_p95_abs_err_deg | 1.2681 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5349 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3516 |
| theta_flat_abs_p95_deg | 2.4276 |
| theta_flat_bias_deg | -0.3351 |
| theta_near_flat_abs_p95_deg | 1.4677 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2069 |
| theta_flat_turn_abs_p95_deg | 1.4201 |
| flat_recall | 0.9511 |
| stall_recall | 0.6979 |
| slope_recall | 0.9804 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7580 |
| downhill_recall | 0.8008 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    719,
    0,
    37
  ],
  [
    9,
    67,
    20
  ],
  [
    44,
    10,
    2696
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    426,
    231,
    142
  ],
  [
    208,
    1253,
    472
  ],
  [
    119,
    223,
    528
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.302035 |
| test_loss_turn_bundle_base | 0.163956 |
| test_loss_theta_bundle_base | 0.000163 |
| test_loss_transition_focal_raw | 1.931095 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.099571 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 115
- train_seconds: 1474.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 31 | 0.3548 | 0.5537 |
| [0.60,0.70) | 14 | 0.2857 | 0.6480 |
| [0.70,0.80) | 26 | 0.5000 | 0.7518 |
| [0.80,0.90) | 43 | 0.3721 | 0.8558 |
| [0.90,1.00) | 3488 | 0.0218 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 401 | 0.6234 | 0.5207 |
| [0.60,0.70) | 338 | 0.5325 | 0.6514 |
| [0.70,0.80) | 319 | 0.4420 | 0.7481 |
| [0.80,0.90) | 424 | 0.4552 | 0.8516 |
| [0.90,1.00) | 2120 | 0.2976 | 0.9817 |


## 验证集最佳点

```json
{
  "loss_total": 0.4719201594147534,
  "acc_main": 0.9431664411366711,
  "acc_turn": 0.6698240866035182,
  "acc_turn_pure": 0.6784660766961652,
  "acc_turn_transition": 0.6288819875776398,
  "false_turn_straight": 0.3503118503118503,
  "flat_recall": 0.928462709284627,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.928462709284627,
    0.40476190476190477,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6149289099526066,
  "turn_straight_recall": 0.6496881496881497,
  "turn_left_recall": 0.761596548004315,
  "recall_turn": [
    0.6149289099526066,
    0.6496881496881497,
    0.761596548004315
  ],
  "cm_turn": [
    [
      519,
      229,
      96
    ],
    [
      194,
      1250,
      480
    ],
    [
      33,
      188,
      706
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      610,
      0,
      47
    ],
    [
      3,
      17,
      22
    ],
    [
      132,
      6,
      2858
    ]
  ],
  "main_confidence_mean": 0.9681665698845512,
  "main_confidence_error_mean": 0.7567416407381571,
  "main_low_conf_0p60_ratio": 0.052232746955345064,
  "main_low_conf_0p70_ratio": 0.05899864682002706,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 193,
      "error_rate": 0.46632124352331605,
      "mean_confidence": 0.5402171889856492
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.52,
      "mean_confidence": 0.6531689558456714
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.3448275862068966,
      "mean_confidence": 0.7482622240005384
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.2127659574468085,
      "mean_confidence": 0.850892322581571
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3401,
      "error_rate": 0.025580711555424875,
      "mean_confidence": 0.9982630963527476
    }
  ],
  "turn_confidence_mean": 0.8731403677539522,
  "turn_confidence_error_mean": 0.798454656127224,
  "turn_low_conf_0p60_ratio": 0.1250338294993234,
  "turn_low_conf_0p70_ratio": 0.19025710419485792,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 462,
      "error_rate": 0.6233766233766234,
      "mean_confidence": 0.5054021771593366
    },
    {
      "bin": "[0.60,0.70)",
      "n": 241,
      "error_rate": 0.44398340248962653,
      "mean_confidence": 0.6484576298855746
    },
    {
      "bin": "[0.70,0.80)",
      "n": 244,
      "error_rate": 0.46311475409836067,
      "mean_confidence": 0.749330528339602
    },
    {
      "bin": "[0.80,0.90)",
      "n": 351,
      "error_rate": 0.39886039886039887,
      "mean_confidence": 0.8542628006093969
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2397,
      "error_rate": 0.23863162286191072,
      "mean_confidence": 0.9819760835511284
    }
  ],
  "theta_mae_rad": 0.013879453763365746,
  "theta_mae_deg": 0.7952340841293335,
  "uphill_recall": 0.7849056603773585,
  "downhill_recall": 0.8058954393770856,
  "slope_sign_acc": 0.9696140158773611,
  "theta_flat_mae_deg": 1.1096417903900146,
  "theta_flat_abs_p95_deg": 4.156070232391357,
  "theta_flat_abs_max_deg": 10.28762149810791,
  "theta_flat_bias_deg": 0.5309140086174011,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.638170599937439,
  "theta_near_flat_abs_p95_deg": 5.867619514465332,
  "theta_near_flat_abs_max_deg": 10.28762149810791,
  "theta_near_flat_bias_deg": 1.1719073057174683,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.452574610710144,
  "theta_flat_turn_abs_p95_deg": 6.597543716430664,
  "theta_flat_turn_abs_max_deg": 10.28762149810791,
  "theta_flat_turn_bias_deg": 0.8503623008728027,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7952340841293335,
  "theta_slope_control_abs_p95_deg": 9.038461685180664,
  "theta_slope_control_abs_max_deg": 11.816431999206543,
  "theta_slope_control_bias_deg": -0.15206041932106018,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7952341437339783,
  "theta_all_rmse_deg": 1.2344859838485718,
  "theta_all_p95_abs_err_deg": 2.6556756496429443,
  "theta_all_max_abs_err_deg": 10.78762149810791,
  "theta_all_bias_deg": -0.15206041932106018,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7262868881225586,
  "theta_active_abs_ge_2_rmse_deg": 1.0058640241622925,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0001723766326904,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.742839813232422,
  "theta_active_abs_ge_2_bias_deg": -0.30183151364326477,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8360844850540161,
  "theta_abs_le_8_rmse_deg": 1.3051519393920898,
  "theta_abs_le_8_p95_abs_err_deg": 2.6556756496429443,
  "theta_abs_le_8_max_abs_err_deg": 10.78762149810791,
  "theta_abs_le_8_bias_deg": -0.14965324103832245,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7952341437339783,
  "theta_abs_le_10_rmse_deg": 1.2344859838485718,
  "theta_abs_le_10_p95_abs_err_deg": 2.6556756496429443,
  "theta_abs_le_10_max_abs_err_deg": 10.78762149810791,
  "theta_abs_le_10_bias_deg": -0.15206041932106018,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6776987314224243,
  "theta_pos_8_10_rmse_deg": 0.8705454468727112,
  "theta_pos_8_10_p95_abs_err_deg": 1.452931523323059,
  "theta_pos_8_10_max_abs_err_deg": 4.833204746246338,
  "theta_pos_8_10_bias_deg": -0.4743337333202362,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5671612620353699,
  "theta_neg_10_8_rmse_deg": 0.8809298276901245,
  "theta_neg_10_8_p95_abs_err_deg": 1.4837843179702759,
  "theta_neg_10_8_max_abs_err_deg": 5.4209208488464355,
  "theta_neg_10_8_bias_deg": 0.15529988706111908,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5403565764427185,
  "theta_pos_6_8_rmse_deg": 0.7152395248413086,
  "theta_pos_6_8_p95_abs_err_deg": 1.2835372686386108,
  "theta_pos_6_8_max_abs_err_deg": 2.8864786624908447,
  "theta_pos_6_8_bias_deg": -0.3201991319656372,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.5985123515129089,
  "theta_neg_8_6_rmse_deg": 0.8862208724021912,
  "theta_neg_8_6_p95_abs_err_deg": 1.7151635885238647,
  "theta_neg_8_6_max_abs_err_deg": 4.505100250244141,
  "theta_neg_8_6_bias_deg": -0.037718452513217926,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8882869482040405,
  "theta_neg_4_2_rmse_deg": 1.1392978429794312,
  "theta_neg_4_2_p95_abs_err_deg": 2.302197217941284,
  "theta_neg_4_2_max_abs_err_deg": 4.246248245239258,
  "theta_neg_4_2_bias_deg": -0.7031128406524658,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.46011611819267273,
  "theta_neg_2_0p5_rmse_deg": 0.654190719127655,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.198291301727295,
  "theta_neg_2_0p5_max_abs_err_deg": 3.7354929447174072,
  "theta_neg_2_0p5_bias_deg": -0.1721043884754181,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0194817781448364,
  "theta_pos_0p5_2_rmse_deg": 1.4471615552902222,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6556756496429443,
  "theta_pos_0p5_2_max_abs_err_deg": 4.02219295501709,
  "theta_pos_0p5_2_bias_deg": 0.3205569088459015,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3430166649640978,
  "loss_turn": 1.6075223677213202,
  "loss_theta": 0.00046403726370039826,
  "loss_main_bundle_base": 0.3430166649640978,
  "loss_turn_bundle_base": 0.12860178713748516,
  "loss_theta_bundle_base": 0.0003017079007133831,
  "loss_main_bundle": 0.3430166649640978,
  "loss_turn_bundle": 0.12860178713748516,
  "loss_theta_bundle": 0.0003017079007133831,
  "loss_theta_flat": 0.0002430458005774654,
  "loss_theta_near_flat": 0.0020273106456236444,
  "loss_theta_error_excess": 0.00018924284466140283,
  "loss_theta_flat_excess": 0.00012877167871560256,
  "loss_theta_near_flat_excess": 0.0016063583596371345,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 7.859764009087469e-05,
  "loss_theta_small_neg": 0.00039613871136995305,
  "loss_theta_small_neg_excess": 8.762214200965636e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3398812391357912,
  "loss_false_turn_straight": 0.2635422276224593,
  "loss_transition_focal_raw": 1.546723729767238,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.8723293350252996,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
