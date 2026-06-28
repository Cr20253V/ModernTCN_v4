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
| acc_main | 0.9634 |
| acc_turn | 0.5689 |
| acc_turn_pure | 0.5868 |
| acc_turn_transition | 0.4903 |
| main_confidence_mean | 0.9832 |
| main_low_conf_0p60_ratio | 0.0086 |
| main_low_conf_0p70_ratio | 0.0189 |
| turn_confidence_mean | 0.7911 |
| turn_low_conf_0p60_ratio | 0.2138 |
| turn_low_conf_0p70_ratio | 0.3309 |
| turn_right_recall | 0.6571 |
| turn_straight_recall | 0.5127 |
| turn_left_recall | 0.6126 |
| theta_mae_deg | 0.7673 |
| theta_abs_le_10_p95_abs_err_deg | 2.0553 |
| theta_neg_10_8_p95_abs_err_deg | 2.0553 |
| theta_pos_8_10_p95_abs_err_deg | 3.0253 |
| theta_abs_le_8_p95_abs_err_deg | 1.9586 |
| theta_neg_8_6_p95_abs_err_deg | 1.9731 |
| theta_pos_6_8_p95_abs_err_deg | 1.9391 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9565 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0079 |
| theta_flat_abs_p95_deg | 2.4933 |
| theta_flat_bias_deg | 0.5143 |
| theta_near_flat_abs_p95_deg | 2.3479 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.6768 |
| theta_flat_turn_abs_p95_deg | 2.0910 |
| flat_recall | 0.9828 |
| stall_recall | 0.6771 |
| slope_recall | 0.9680 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7391 |
| downhill_recall | 0.7860 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    743,
    1,
    12
  ],
  [
    10,
    65,
    21
  ],
  [
    80,
    8,
    2662
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    525,
    146,
    128
  ],
  [
    466,
    991,
    476
  ],
  [
    148,
    189,
    533
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.307348 |
| test_loss_turn_bundle_base | 0.290362 |
| test_loss_theta_bundle_base | 0.000216 |
| test_loss_transition_focal_raw | 1.233872 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.251119 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 45
- train_seconds: 243.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 31 | 0.2903 | 0.5505 |
| [0.60,0.70) | 37 | 0.3243 | 0.6498 |
| [0.70,0.80) | 43 | 0.2558 | 0.7468 |
| [0.80,0.90) | 72 | 0.1944 | 0.8525 |
| [0.90,1.00) | 3419 | 0.0252 | 0.9964 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 770 | 0.6078 | 0.5099 |
| [0.60,0.70) | 422 | 0.5284 | 0.6488 |
| [0.70,0.80) | 432 | 0.5139 | 0.7518 |
| [0.80,0.90) | 536 | 0.4235 | 0.8517 |
| [0.90,1.00) | 1442 | 0.2864 | 0.9721 |


## 验证集最佳点

```json
{
  "loss_total": 0.5614470991455977,
  "acc_main": 0.9428958051420839,
  "acc_turn": 0.6010825439783491,
  "acc_turn_pure": 0.615535889872173,
  "acc_turn_transition": 0.532608695652174,
  "false_turn_straight": 0.48492723492723494,
  "flat_recall": 0.9467275494672754,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9495994659546061,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.09523809523809523,
  "recall_main": [
    0.9467275494672754,
    0.40476190476190477,
    0.9495994659546061
  ],
  "turn_right_recall": 0.6777251184834123,
  "turn_straight_recall": 0.5150727650727651,
  "turn_left_recall": 0.7098166127292341,
  "recall_turn": [
    0.6777251184834123,
    0.5150727650727651,
    0.7098166127292341
  ],
  "cm_turn": [
    [
      572,
      203,
      69
    ],
    [
      487,
      991,
      446
    ],
    [
      102,
      167,
      658
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      622,
      0,
      35
    ],
    [
      4,
      17,
      21
    ],
    [
      141,
      10,
      2845
    ]
  ],
  "main_confidence_mean": 0.9618331704360872,
  "main_confidence_error_mean": 0.7319467092056907,
  "main_low_conf_0p60_ratio": 0.05250338294993234,
  "main_low_conf_0p70_ratio": 0.060081190798376184,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 194,
      "error_rate": 0.4793814432989691,
      "mean_confidence": 0.48493028938805505
    },
    {
      "bin": "[0.60,0.70)",
      "n": 28,
      "error_rate": 0.25,
      "mean_confidence": 0.6558568588693113
    },
    {
      "bin": "[0.70,0.80)",
      "n": 44,
      "error_rate": 0.22727272727272727,
      "mean_confidence": 0.7520452132778548
    },
    {
      "bin": "[0.80,0.90)",
      "n": 63,
      "error_rate": 0.30158730158730157,
      "mean_confidence": 0.8574336777651961
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3366,
      "error_rate": 0.0243612596553773,
      "mean_confidence": 0.9965611365087004
    }
  ],
  "turn_confidence_mean": 0.8074636838527743,
  "turn_confidence_error_mean": 0.7312106608567922,
  "turn_low_conf_0p60_ratio": 0.19404600811907985,
  "turn_low_conf_0p70_ratio": 0.29851150202976995,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 717,
      "error_rate": 0.6345885634588564,
      "mean_confidence": 0.494369482252279
    },
    {
      "bin": "[0.60,0.70)",
      "n": 386,
      "error_rate": 0.5284974093264249,
      "mean_confidence": 0.6488870255122436
    },
    {
      "bin": "[0.70,0.80)",
      "n": 424,
      "error_rate": 0.45990566037735847,
      "mean_confidence": 0.7530580006173367
    },
    {
      "bin": "[0.80,0.90)",
      "n": 455,
      "error_rate": 0.45494505494505494,
      "mean_confidence": 0.8508829220144732
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1713,
      "error_rate": 0.24109748978400466,
      "mean_confidence": 0.9761801981523964
    }
  ],
  "theta_mae_rad": 0.015968285501003265,
  "theta_mae_deg": 0.9149153232574463,
  "uphill_recall": 0.7725067385444744,
  "downhill_recall": 0.8047830923248054,
  "slope_sign_acc": 0.9594853545031481,
  "theta_flat_mae_deg": 1.257151484489441,
  "theta_flat_abs_p95_deg": 3.4354591369628906,
  "theta_flat_abs_max_deg": 10.571314811706543,
  "theta_flat_bias_deg": 0.8665052056312561,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5977188348770142,
  "theta_near_flat_abs_p95_deg": 3.4365243911743164,
  "theta_near_flat_abs_max_deg": 10.571314811706543,
  "theta_near_flat_bias_deg": 1.370224118232727,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.315247893333435,
  "theta_flat_turn_abs_p95_deg": 3.7246320247650146,
  "theta_flat_turn_abs_max_deg": 10.571314811706543,
  "theta_flat_turn_bias_deg": 1.1502009630203247,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9149153232574463,
  "theta_slope_control_abs_p95_deg": 9.421341896057129,
  "theta_slope_control_abs_max_deg": 13.426661491394043,
  "theta_slope_control_bias_deg": 0.19359438121318817,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9149152040481567,
  "theta_all_rmse_deg": 1.3328769207000732,
  "theta_all_p95_abs_err_deg": 2.6526615619659424,
  "theta_all_max_abs_err_deg": 11.071313858032227,
  "theta_all_bias_deg": 0.19359438121318817,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8398654460906982,
  "theta_active_abs_ge_2_rmse_deg": 1.2092655897140503,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.312119483947754,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.810711860656738,
  "theta_active_abs_ge_2_bias_deg": 0.04603016749024391,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9532058835029602,
  "theta_abs_le_8_rmse_deg": 1.378090500831604,
  "theta_abs_le_8_p95_abs_err_deg": 2.8386542797088623,
  "theta_abs_le_8_max_abs_err_deg": 11.071313858032227,
  "theta_abs_le_8_bias_deg": 0.2789932191371918,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9149152040481567,
  "theta_abs_le_10_rmse_deg": 1.3328769207000732,
  "theta_abs_le_10_p95_abs_err_deg": 2.6526615619659424,
  "theta_abs_le_10_max_abs_err_deg": 11.071313858032227,
  "theta_abs_le_10_bias_deg": 0.19359438121318817,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7906843423843384,
  "theta_pos_8_10_rmse_deg": 1.0164856910705566,
  "theta_pos_8_10_p95_abs_err_deg": 1.8521273136138916,
  "theta_pos_8_10_max_abs_err_deg": 5.8670477867126465,
  "theta_pos_8_10_bias_deg": -0.4383663237094879,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7154372334480286,
  "theta_neg_10_8_rmse_deg": 1.2205034494400024,
  "theta_neg_10_8_p95_abs_err_deg": 2.1122522354125977,
  "theta_neg_10_8_max_abs_err_deg": 7.050554275512695,
  "theta_neg_10_8_bias_deg": 0.10973086953163147,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.686718761920929,
  "theta_pos_6_8_rmse_deg": 0.9231040477752686,
  "theta_pos_6_8_p95_abs_err_deg": 1.899595856666565,
  "theta_pos_6_8_max_abs_err_deg": 3.8280656337738037,
  "theta_pos_6_8_bias_deg": 0.032487526535987854,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7961040735244751,
  "theta_neg_8_6_rmse_deg": 1.1922452449798584,
  "theta_neg_8_6_p95_abs_err_deg": 2.275601387023926,
  "theta_neg_8_6_max_abs_err_deg": 7.810711860656738,
  "theta_neg_8_6_bias_deg": 0.24026191234588623,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8767098784446716,
  "theta_neg_4_2_rmse_deg": 1.2652238607406616,
  "theta_neg_4_2_p95_abs_err_deg": 2.5281972885131836,
  "theta_neg_4_2_max_abs_err_deg": 5.569502353668213,
  "theta_neg_4_2_bias_deg": -0.10075610876083374,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.9505677223205566,
  "theta_neg_2_0p5_rmse_deg": 1.2365857362747192,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.2743613719940186,
  "theta_neg_2_0p5_max_abs_err_deg": 6.4676384925842285,
  "theta_neg_2_0p5_bias_deg": 0.09112541377544403,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1248524188995361,
  "theta_pos_0p5_2_rmse_deg": 1.339213252067566,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9677023887634277,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9078433513641357,
  "theta_pos_0p5_2_bias_deg": 0.9659817218780518,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.306862422206889,
  "loss_turn": 1.2710415759493114,
  "loss_theta": 0.0005410696410243835,
  "loss_main_bundle_base": 0.306862422206889,
  "loss_turn_bundle_base": 0.2542083199114535,
  "loss_theta_bundle_base": 0.00037636306465771023,
  "loss_main_bundle": 0.306862422206889,
  "loss_turn_bundle": 0.2542083199114535,
  "loss_theta_bundle": 0.00037636306465771023,
  "loss_theta_flat": 0.0004400861451311884,
  "loss_theta_near_flat": 0.0015306535372586168,
  "loss_theta_error_excess": 0.0002095445162422592,
  "loss_theta_flat_excess": 0.00021205116497993948,
  "loss_theta_near_flat_excess": 0.0011290413852092962,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001548719752680117,
  "loss_theta_small_neg": 0.0004900615834360073,
  "loss_theta_small_neg_excess": 0.00017723292002078846,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4423888170509442,
  "loss_false_turn_straight": 0.34253394874732773,
  "loss_transition_focal_raw": 0.9764985855119316,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.7877915977842704,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
