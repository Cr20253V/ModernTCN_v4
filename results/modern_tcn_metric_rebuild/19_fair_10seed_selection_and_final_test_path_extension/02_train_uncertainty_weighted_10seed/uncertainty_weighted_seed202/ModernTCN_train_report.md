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
| acc_main | 0.9659 |
| acc_turn | 0.5544 |
| acc_turn_pure | 0.5773 |
| acc_turn_transition | 0.4545 |
| main_confidence_mean | 0.9854 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0133 |
| turn_confidence_mean | 0.7650 |
| turn_low_conf_0p60_ratio | 0.2260 |
| turn_low_conf_0p70_ratio | 0.3795 |
| turn_right_recall | 0.5782 |
| turn_straight_recall | 0.5173 |
| turn_left_recall | 0.6149 |
| theta_mae_deg | 0.9102 |
| theta_abs_le_10_p95_abs_err_deg | 2.3794 |
| theta_neg_10_8_p95_abs_err_deg | 1.5798 |
| theta_pos_8_10_p95_abs_err_deg | 3.2131 |
| theta_abs_le_8_p95_abs_err_deg | 2.3572 |
| theta_neg_8_6_p95_abs_err_deg | 2.2768 |
| theta_pos_6_8_p95_abs_err_deg | 2.4304 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9389 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0417 |
| theta_flat_abs_p95_deg | 2.7700 |
| theta_flat_bias_deg | 0.2106 |
| theta_near_flat_abs_p95_deg | 2.1721 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3618 |
| theta_flat_turn_abs_p95_deg | 2.1300 |
| flat_recall | 0.9802 |
| stall_recall | 0.6354 |
| slope_recall | 0.9735 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7517 |
| downhill_recall | 0.7838 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    741,
    0,
    15
  ],
  [
    8,
    61,
    27
  ],
  [
    61,
    12,
    2677
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    462,
    179,
    158
  ],
  [
    398,
    1000,
    535
  ],
  [
    175,
    160,
    535
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.240409 |
| test_loss_turn_bundle_base | 0.261959 |
| test_loss_theta_bundle_base | 0.000272 |
| test_loss_transition_focal_raw | 1.067661 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.602719 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 38
- train_seconds: 211.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.4500 | 0.5403 |
| [0.60,0.70) | 28 | 0.3571 | 0.6550 |
| [0.70,0.80) | 37 | 0.4054 | 0.7514 |
| [0.80,0.90) | 88 | 0.3409 | 0.8540 |
| [0.90,1.00) | 3429 | 0.0172 | 0.9966 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 814 | 0.6081 | 0.5150 |
| [0.60,0.70) | 553 | 0.5063 | 0.6507 |
| [0.70,0.80) | 543 | 0.4825 | 0.7497 |
| [0.80,0.90) | 588 | 0.4507 | 0.8525 |
| [0.90,1.00) | 1104 | 0.2745 | 0.9676 |


## 验证集最佳点

```json
{
  "loss_total": 0.5863136383451532,
  "acc_main": 0.9401894451962111,
  "acc_turn": 0.5994587280108254,
  "acc_turn_pure": 0.6181579809898394,
  "acc_turn_transition": 0.5108695652173914,
  "false_turn_straight": 0.4984407484407484,
  "flat_recall": 0.939117199391172,
  "stall_recall": 0.2857142857142857,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0015220700152207,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.939117199391172,
    0.2857142857142857,
    0.9495994659546061
  ],
  "turn_right_recall": 0.6362559241706162,
  "turn_straight_recall": 0.5015592515592515,
  "turn_left_recall": 0.7691477885652643,
  "recall_turn": [
    0.6362559241706162,
    0.5015592515592515,
    0.7691477885652643
  ],
  "cm_turn": [
    [
      537,
      171,
      136
    ],
    [
      345,
      965,
      614
    ],
    [
      62,
      152,
      713
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      617,
      1,
      39
    ],
    [
      0,
      12,
      30
    ],
    [
      139,
      12,
      2845
    ]
  ],
  "main_confidence_mean": 0.9637188108243595,
  "main_confidence_error_mean": 0.7639468678161875,
  "main_low_conf_0p60_ratio": 0.05412719891745602,
  "main_low_conf_0p70_ratio": 0.06305818673883627,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 200,
      "error_rate": 0.43,
      "mean_confidence": 0.5365071676821696
    },
    {
      "bin": "[0.60,0.70)",
      "n": 33,
      "error_rate": 0.45454545454545453,
      "mean_confidence": 0.6578773906437715
    },
    {
      "bin": "[0.70,0.80)",
      "n": 42,
      "error_rate": 0.38095238095238093,
      "mean_confidence": 0.7462048280516166
    },
    {
      "bin": "[0.80,0.90)",
      "n": 61,
      "error_rate": 0.19672131147540983,
      "mean_confidence": 0.8617567355009046
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3359,
      "error_rate": 0.027389103899970228,
      "mean_confidence": 0.9967317222163163
    }
  ],
  "turn_confidence_mean": 0.7721424293001518,
  "turn_confidence_error_mean": 0.7026209060677978,
  "turn_low_conf_0p60_ratio": 0.23978349120433018,
  "turn_low_conf_0p70_ratio": 0.3602165087956698,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 886,
      "error_rate": 0.618510158013544,
      "mean_confidence": 0.5070143381533512
    },
    {
      "bin": "[0.60,0.70)",
      "n": 445,
      "error_rate": 0.451685393258427,
      "mean_confidence": 0.6506806345867394
    },
    {
      "bin": "[0.70,0.80)",
      "n": 527,
      "error_rate": 0.3908918406072106,
      "mean_confidence": 0.7516685950377968
    },
    {
      "bin": "[0.80,0.90)",
      "n": 547,
      "error_rate": 0.38939670932358317,
      "mean_confidence": 0.8518886656677733
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1290,
      "error_rate": 0.24186046511627907,
      "mean_confidence": 0.9706870081890715
    }
  ],
  "theta_mae_rad": 0.016363762319087982,
  "theta_mae_deg": 0.9375744462013245,
  "uphill_recall": 0.7784366576819407,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9674240350396934,
  "theta_flat_mae_deg": 1.006588101387024,
  "theta_flat_abs_p95_deg": 3.130256414413452,
  "theta_flat_abs_max_deg": 7.990250110626221,
  "theta_flat_bias_deg": 0.6509045362472534,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3282662630081177,
  "theta_near_flat_abs_p95_deg": 3.3733012676239014,
  "theta_near_flat_abs_max_deg": 7.990250110626221,
  "theta_near_flat_bias_deg": 1.073244571685791,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0545384883880615,
  "theta_flat_turn_abs_p95_deg": 3.0598690509796143,
  "theta_flat_turn_abs_max_deg": 7.990250110626221,
  "theta_flat_turn_bias_deg": 0.9237038493156433,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9375744462013245,
  "theta_slope_control_abs_p95_deg": 9.841696739196777,
  "theta_slope_control_abs_max_deg": 12.201709747314453,
  "theta_slope_control_bias_deg": 0.044754501432180405,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.937574565410614,
  "theta_all_rmse_deg": 1.2622687816619873,
  "theta_all_p95_abs_err_deg": 2.5598690509796143,
  "theta_all_max_abs_err_deg": 8.490249633789062,
  "theta_all_bias_deg": 0.044754501432180405,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9224403500556946,
  "theta_active_abs_ge_2_rmse_deg": 1.227596640586853,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.477055311203003,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.357645988464355,
  "theta_active_abs_ge_2_bias_deg": -0.08816958218812943,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.960767924785614,
  "theta_abs_le_8_rmse_deg": 1.2874643802642822,
  "theta_abs_le_8_p95_abs_err_deg": 2.5786826610565186,
  "theta_abs_le_8_max_abs_err_deg": 8.490249633789062,
  "theta_abs_le_8_bias_deg": 0.10598461329936981,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.937574565410614,
  "theta_abs_le_10_rmse_deg": 1.2622687816619873,
  "theta_abs_le_10_p95_abs_err_deg": 2.5598690509796143,
  "theta_abs_le_10_max_abs_err_deg": 8.490249633789062,
  "theta_abs_le_10_bias_deg": 0.044754501432180405,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6407139301300049,
  "theta_pos_8_10_rmse_deg": 0.8979190587997437,
  "theta_pos_8_10_p95_abs_err_deg": 1.9865473508834839,
  "theta_pos_8_10_max_abs_err_deg": 4.149640083312988,
  "theta_pos_8_10_bias_deg": 0.061907414346933365,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.042190432548523,
  "theta_neg_10_8_rmse_deg": 1.359151005744934,
  "theta_neg_10_8_p95_abs_err_deg": 2.338841199874878,
  "theta_neg_10_8_max_abs_err_deg": 7.297898769378662,
  "theta_neg_10_8_bias_deg": -0.4937686026096344,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.9004328846931458,
  "theta_pos_6_8_rmse_deg": 1.2165274620056152,
  "theta_pos_6_8_p95_abs_err_deg": 2.548668622970581,
  "theta_pos_6_8_max_abs_err_deg": 5.249997138977051,
  "theta_pos_6_8_bias_deg": 0.2395305037498474,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0711315870285034,
  "theta_neg_8_6_rmse_deg": 1.3970701694488525,
  "theta_neg_8_6_p95_abs_err_deg": 2.632223606109619,
  "theta_neg_8_6_max_abs_err_deg": 8.357645988464355,
  "theta_neg_8_6_bias_deg": -0.6331630945205688,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8539944887161255,
  "theta_neg_4_2_rmse_deg": 1.1359695196151733,
  "theta_neg_4_2_p95_abs_err_deg": 2.2877352237701416,
  "theta_neg_4_2_max_abs_err_deg": 5.248398303985596,
  "theta_neg_4_2_bias_deg": -0.0017062887782230973,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5491747856140137,
  "theta_neg_2_0p5_rmse_deg": 0.8321772813796997,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2447924613952637,
  "theta_neg_2_0p5_max_abs_err_deg": 6.490757465362549,
  "theta_neg_2_0p5_bias_deg": 0.036713577806949615,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1781413555145264,
  "theta_pos_0p5_2_rmse_deg": 1.4341400861740112,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3294460773468018,
  "theta_pos_0p5_2_max_abs_err_deg": 4.423578262329102,
  "theta_pos_0p5_2_bias_deg": 0.8251861333847046,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3698233757354571,
  "loss_turn": 1.0808683507013386,
  "loss_theta": 0.00048542145218420397,
  "loss_main_bundle_base": 0.3698233757354571,
  "loss_turn_bundle_base": 0.21617367612815516,
  "loss_theta_bundle_base": 0.0003165804170272458,
  "loss_main_bundle": 0.3698233757354571,
  "loss_turn_bundle": 0.21617367612815516,
  "loss_theta_bundle": 0.0003165804170272458,
  "loss_theta_flat": 0.00024235914992981405,
  "loss_theta_near_flat": 0.0009121406735809512,
  "loss_theta_error_excess": 0.0001476199313536972,
  "loss_theta_flat_excess": 9.158485730647151e-05,
  "loss_theta_near_flat_excess": 0.0005844127298276039,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00013134519602499742,
  "loss_theta_small_neg": 0.0003940788551683617,
  "loss_theta_small_neg_excess": 9.796667084128109e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4628299324535065,
  "loss_false_turn_straight": 0.34342393859797465,
  "loss_transition_focal_raw": 0.8337346344420004,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.3970385890912365,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
