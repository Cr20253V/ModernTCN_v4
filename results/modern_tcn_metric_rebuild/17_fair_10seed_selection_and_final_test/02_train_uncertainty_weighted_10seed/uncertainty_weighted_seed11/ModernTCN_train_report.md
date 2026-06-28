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
| acc_main | 0.9714 |
| acc_turn | 0.6066 |
| acc_turn_pure | 0.6278 |
| acc_turn_transition | 0.5142 |
| main_confidence_mean | 0.9900 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0108 |
| turn_confidence_mean | 0.8603 |
| turn_low_conf_0p60_ratio | 0.1213 |
| turn_low_conf_0p70_ratio | 0.2079 |
| turn_right_recall | 0.6596 |
| turn_straight_recall | 0.6368 |
| turn_left_recall | 0.4908 |
| theta_mae_deg | 0.3691 |
| theta_abs_le_10_p95_abs_err_deg | 1.0446 |
| theta_neg_10_8_p95_abs_err_deg | 0.9805 |
| theta_pos_8_10_p95_abs_err_deg | 1.8455 |
| theta_abs_le_8_p95_abs_err_deg | 0.9717 |
| theta_neg_8_6_p95_abs_err_deg | 0.8714 |
| theta_pos_6_8_p95_abs_err_deg | 0.9650 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.1029 |
| theta_pos_0p5_2_p95_abs_err_deg | 0.8772 |
| theta_flat_abs_p95_deg | 2.2495 |
| theta_flat_bias_deg | 0.1805 |
| theta_near_flat_abs_p95_deg | 1.4647 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2354 |
| theta_flat_turn_abs_p95_deg | 1.2280 |
| flat_recall | 0.9524 |
| stall_recall | 0.6562 |
| slope_recall | 0.9876 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7724 |
| downhill_recall | 0.7974 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    720,
    0,
    36
  ],
  [
    8,
    63,
    25
  ],
  [
    30,
    4,
    2716
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    527,
    194,
    78
  ],
  [
    398,
    1231,
    304
  ],
  [
    190,
    253,
    427
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.332259 |
| test_loss_turn_bundle_base | 0.151152 |
| test_loss_theta_bundle_base | 0.000068 |
| test_loss_transition_focal_raw | 1.936137 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.824870 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 151
- train_seconds: 1891.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.4231 | 0.5523 |
| [0.60,0.70) | 13 | 0.3077 | 0.6559 |
| [0.70,0.80) | 38 | 0.3158 | 0.7492 |
| [0.80,0.90) | 34 | 0.3824 | 0.8470 |
| [0.90,1.00) | 3491 | 0.0180 | 0.9985 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 437 | 0.5927 | 0.5159 |
| [0.60,0.70) | 312 | 0.4968 | 0.6469 |
| [0.70,0.80) | 301 | 0.4452 | 0.7530 |
| [0.80,0.90) | 419 | 0.4463 | 0.8497 |
| [0.90,1.00) | 2133 | 0.3197 | 0.9794 |


## 验证集最佳点

```json
{
  "loss_total": 0.3954867231991036,
  "acc_main": 0.9466847090663059,
  "acc_turn": 0.6606224627875508,
  "acc_turn_pure": 0.6660111438872501,
  "acc_turn_transition": 0.6350931677018633,
  "false_turn_straight": 0.35654885654885654,
  "flat_recall": 0.9421613394216134,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9546061415220294,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.07142857142857142,
  "recall_main": [
    0.9421613394216134,
    0.4523809523809524,
    0.9546061415220294
  ],
  "turn_right_recall": 0.7049763033175356,
  "turn_straight_recall": 0.6434511434511434,
  "turn_left_recall": 0.6558791801510249,
  "recall_turn": [
    0.7049763033175356,
    0.6434511434511434,
    0.6558791801510249
  ],
  "cm_turn": [
    [
      595,
      203,
      46
    ],
    [
      374,
      1238,
      312
    ],
    [
      106,
      213,
      608
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
      3,
      19,
      20
    ],
    [
      127,
      9,
      2860
    ]
  ],
  "main_confidence_mean": 0.9736187539804565,
  "main_confidence_error_mean": 0.7774150493817219,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.05250338294993234,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.46703296703296704,
      "mean_confidence": 0.5805810093931646
    },
    {
      "bin": "[0.60,0.70)",
      "n": 12,
      "error_rate": 0.4166666666666667,
      "mean_confidence": 0.6547685690594837
    },
    {
      "bin": "[0.70,0.80)",
      "n": 24,
      "error_rate": 0.5,
      "mean_confidence": 0.7391328237100726
    },
    {
      "bin": "[0.80,0.90)",
      "n": 39,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.8570004098472555
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3438,
      "error_rate": 0.02326934264107039,
      "mean_confidence": 0.9984980004847097
    }
  ],
  "turn_confidence_mean": 0.8777650323260928,
  "turn_confidence_error_mean": 0.8070346541402642,
  "turn_low_conf_0p60_ratio": 0.11962110960757781,
  "turn_low_conf_0p70_ratio": 0.18619756427604872,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 442,
      "error_rate": 0.6357466063348416,
      "mean_confidence": 0.5390815140390717
    },
    {
      "bin": "[0.60,0.70)",
      "n": 246,
      "error_rate": 0.5121951219512195,
      "mean_confidence": 0.6504479477994789
    },
    {
      "bin": "[0.70,0.80)",
      "n": 277,
      "error_rate": 0.47653429602888087,
      "mean_confidence": 0.7492108067692275
    },
    {
      "bin": "[0.80,0.90)",
      "n": 359,
      "error_rate": 0.4178272980501393,
      "mean_confidence": 0.8548554669486208
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2371,
      "error_rate": 0.23829607760438634,
      "mean_confidence": 0.9829747212025897
    }
  ],
  "theta_mae_rad": 0.010058271698653698,
  "theta_mae_deg": 0.5762965083122253,
  "uphill_recall": 0.7811320754716982,
  "downhill_recall": 0.8058954393770856,
  "slope_sign_acc": 0.9739939775526965,
  "theta_flat_mae_deg": 1.0034561157226562,
  "theta_flat_abs_p95_deg": 4.497889518737793,
  "theta_flat_abs_max_deg": 10.64136028289795,
  "theta_flat_bias_deg": 0.6193205118179321,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5275238752365112,
  "theta_near_flat_abs_p95_deg": 4.937760829925537,
  "theta_near_flat_abs_max_deg": 10.64136028289795,
  "theta_near_flat_bias_deg": 0.8751005530357361,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1752519607543945,
  "theta_flat_turn_abs_p95_deg": 5.851212024688721,
  "theta_flat_turn_abs_max_deg": 10.64136028289795,
  "theta_flat_turn_bias_deg": 0.006649364717304707,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.5762965083122253,
  "theta_slope_control_abs_p95_deg": 9.287277221679688,
  "theta_slope_control_abs_max_deg": 10.749341011047363,
  "theta_slope_control_bias_deg": 0.25588369369506836,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.5762964487075806,
  "theta_all_rmse_deg": 1.0765198469161987,
  "theta_all_p95_abs_err_deg": 2.4363908767700195,
  "theta_all_max_abs_err_deg": 10.141361236572266,
  "theta_all_bias_deg": 0.25588366389274597,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.4826236069202423,
  "theta_active_abs_ge_2_rmse_deg": 0.8053527474403381,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.8052712678909302,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.818299293518066,
  "theta_active_abs_ge_2_bias_deg": 0.176184743642807,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.6116315722465515,
  "theta_abs_le_8_rmse_deg": 1.138327956199646,
  "theta_abs_le_8_p95_abs_err_deg": 2.9329311847686768,
  "theta_abs_le_8_max_abs_err_deg": 10.141361236572266,
  "theta_abs_le_8_bias_deg": 0.28243735432624817,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.5762964487075806,
  "theta_abs_le_10_rmse_deg": 1.0765198469161987,
  "theta_abs_le_10_p95_abs_err_deg": 2.4363908767700195,
  "theta_abs_le_10_max_abs_err_deg": 10.141361236572266,
  "theta_abs_le_10_bias_deg": 0.25588366389274597,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.3478299677371979,
  "theta_pos_8_10_rmse_deg": 0.5210399627685547,
  "theta_pos_8_10_p95_abs_err_deg": 1.1625702381134033,
  "theta_pos_8_10_max_abs_err_deg": 2.172067403793335,
  "theta_pos_8_10_bias_deg": 0.010716795921325684,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5080090761184692,
  "theta_neg_10_8_rmse_deg": 0.9469214081764221,
  "theta_neg_10_8_p95_abs_err_deg": 1.4598183631896973,
  "theta_neg_10_8_max_abs_err_deg": 6.818299293518066,
  "theta_neg_10_8_bias_deg": 0.27931565046310425,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.4210776686668396,
  "theta_pos_6_8_rmse_deg": 0.7511879801750183,
  "theta_pos_6_8_p95_abs_err_deg": 1.267325758934021,
  "theta_pos_6_8_max_abs_err_deg": 3.760772705078125,
  "theta_pos_6_8_bias_deg": 0.19474902749061584,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.47165390849113464,
  "theta_neg_8_6_rmse_deg": 0.7324734330177307,
  "theta_neg_8_6_p95_abs_err_deg": 1.4272279739379883,
  "theta_neg_8_6_max_abs_err_deg": 5.719083309173584,
  "theta_neg_8_6_bias_deg": 0.10453498363494873,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.48748451471328735,
  "theta_neg_4_2_rmse_deg": 0.7618836760520935,
  "theta_neg_4_2_p95_abs_err_deg": 1.5735232830047607,
  "theta_neg_4_2_max_abs_err_deg": 6.254194736480713,
  "theta_neg_4_2_bias_deg": -0.009619773365557194,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.3372158110141754,
  "theta_neg_2_0p5_rmse_deg": 0.5044881701469421,
  "theta_neg_2_0p5_p95_abs_err_deg": 0.9658279418945312,
  "theta_neg_2_0p5_max_abs_err_deg": 3.6075730323791504,
  "theta_neg_2_0p5_bias_deg": 0.22233127057552338,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9962433576583862,
  "theta_pos_0p5_2_rmse_deg": 1.5727547407150269,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.9978508949279785,
  "theta_pos_0p5_2_max_abs_err_deg": 4.856681823730469,
  "theta_pos_0p5_2_bias_deg": 0.8697373270988464,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2712882090969886,
  "loss_turn": 1.5495518615668455,
  "loss_theta": 0.00035298361417148084,
  "loss_main_bundle_base": 0.2712882090969886,
  "loss_turn_bundle_base": 0.1239641471447093,
  "loss_theta_bundle_base": 0.00023436132789789844,
  "loss_main_bundle": 0.2712882090969886,
  "loss_turn_bundle": 0.1239641471447093,
  "loss_theta_bundle": 0.00023436132789789844,
  "loss_theta_flat": 0.00021738546438846316,
  "loss_theta_near_flat": 0.0019385914226895619,
  "loss_theta_error_excess": 0.00016133998334313287,
  "loss_theta_flat_excess": 0.00014189999545706136,
  "loss_theta_near_flat_excess": 0.0015386488512334829,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 6.067080379166629e-05,
  "loss_theta_small_neg": 0.0001718873794443265,
  "loss_theta_small_neg_excess": 4.299202528186722e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.31433037103270967,
  "loss_false_turn_straight": 0.2738661521584481,
  "loss_transition_focal_raw": 1.3691782799076808,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.442456452679593,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
