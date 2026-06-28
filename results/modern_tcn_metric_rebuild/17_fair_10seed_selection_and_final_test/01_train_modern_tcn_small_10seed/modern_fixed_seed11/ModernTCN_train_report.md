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
| acc_main | 0.9595 |
| acc_turn | 0.5944 |
| acc_turn_pure | 0.6134 |
| acc_turn_transition | 0.5112 |
| main_confidence_mean | 0.9902 |
| main_low_conf_0p60_ratio | 0.0036 |
| main_low_conf_0p70_ratio | 0.0089 |
| turn_confidence_mean | 0.8241 |
| turn_low_conf_0p60_ratio | 0.1463 |
| turn_low_conf_0p70_ratio | 0.2649 |
| turn_right_recall | 0.6108 |
| turn_straight_recall | 0.6125 |
| turn_left_recall | 0.5391 |
| theta_mae_deg | 0.6426 |
| theta_abs_le_10_p95_abs_err_deg | 1.7763 |
| theta_neg_10_8_p95_abs_err_deg | 1.2500 |
| theta_pos_8_10_p95_abs_err_deg | 1.9894 |
| theta_abs_le_8_p95_abs_err_deg | 1.7818 |
| theta_neg_8_6_p95_abs_err_deg | 1.3499 |
| theta_pos_6_8_p95_abs_err_deg | 1.7784 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6240 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5937 |
| theta_flat_abs_p95_deg | 2.4788 |
| theta_flat_bias_deg | -0.2801 |
| theta_near_flat_abs_p95_deg | 1.6502 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2763 |
| theta_flat_turn_abs_p95_deg | 1.6685 |
| flat_recall | 0.9378 |
| stall_recall | 0.6667 |
| slope_recall | 0.9756 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7511 |
| downhill_recall | 0.8059 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    709,
    0,
    47
  ],
  [
    11,
    64,
    21
  ],
  [
    55,
    12,
    2683
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    488,
    220,
    91
  ],
  [
    363,
    1184,
    386
  ],
  [
    171,
    230,
    469
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.350629 |
| test_loss_turn_bundle_base | 0.114809 |
| test_loss_theta_bundle_base | 0.000162 |
| test_loss_transition_focal_raw | 1.422846 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.695323 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 92
- train_seconds: 1223.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 13 | 0.5385 | 0.5649 |
| [0.60,0.70) | 19 | 0.5789 | 0.6531 |
| [0.70,0.80) | 38 | 0.6053 | 0.7549 |
| [0.80,0.90) | 43 | 0.6512 | 0.8503 |
| [0.90,1.00) | 3489 | 0.0221 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 527 | 0.5996 | 0.5225 |
| [0.60,0.70) | 427 | 0.5340 | 0.6511 |
| [0.70,0.80) | 468 | 0.5214 | 0.7465 |
| [0.80,0.90) | 506 | 0.4348 | 0.8544 |
| [0.90,1.00) | 1674 | 0.2706 | 0.9757 |


## 验证集最佳点

```json
{
  "loss_total": 0.40435214462073793,
  "acc_main": 0.9442489851150203,
  "acc_turn": 0.6373477672530447,
  "acc_turn_pure": 0.6489675516224189,
  "acc_turn_transition": 0.5822981366459627,
  "false_turn_straight": 0.3981288981288981,
  "flat_recall": 0.9406392694063926,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9536048064085447,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.11904761904761904,
  "recall_main": [
    0.9406392694063926,
    0.3333333333333333,
    0.9536048064085447
  ],
  "turn_right_recall": 0.707345971563981,
  "turn_straight_recall": 0.6018711018711018,
  "turn_left_recall": 0.6472491909385113,
  "recall_turn": [
    0.707345971563981,
    0.6018711018711018,
    0.6472491909385113
  ],
  "cm_turn": [
    [
      597,
      203,
      44
    ],
    [
      407,
      1158,
      359
    ],
    [
      93,
      234,
      600
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      618,
      0,
      39
    ],
    [
      5,
      14,
      23
    ],
    [
      131,
      8,
      2857
    ]
  ],
  "main_confidence_mean": 0.9681919812260708,
  "main_confidence_error_mean": 0.7512468047355332,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.056833558863328824,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.46236559139784944,
      "mean_confidence": 0.49181208537603865
    },
    {
      "bin": "[0.60,0.70)",
      "n": 24,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6529869059046526
    },
    {
      "bin": "[0.70,0.80)",
      "n": 14,
      "error_rate": 0.35714285714285715,
      "mean_confidence": 0.7537557085824239
    },
    {
      "bin": "[0.80,0.90)",
      "n": 35,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.8510650393832085
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3436,
      "error_rate": 0.02677532013969732,
      "mean_confidence": 0.9982481899621974
    }
  ],
  "turn_confidence_mean": 0.8424672725135747,
  "turn_confidence_error_mean": 0.7686745877172422,
  "turn_low_conf_0p60_ratio": 0.1415426251691475,
  "turn_low_conf_0p70_ratio": 0.22083897158322058,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 523,
      "error_rate": 0.5908221797323135,
      "mean_confidence": 0.4880764326351869
    },
    {
      "bin": "[0.60,0.70)",
      "n": 293,
      "error_rate": 0.5358361774744027,
      "mean_confidence": 0.651840430202985
    },
    {
      "bin": "[0.70,0.80)",
      "n": 409,
      "error_rate": 0.45965770171149145,
      "mean_confidence": 0.7535744566881559
    },
    {
      "bin": "[0.80,0.90)",
      "n": 470,
      "error_rate": 0.451063829787234,
      "mean_confidence": 0.8534230184441398
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2000,
      "error_rate": 0.237,
      "mean_confidence": 0.9786712900828898
    }
  ],
  "theta_mae_rad": 0.013353094458580017,
  "theta_mae_deg": 0.7650759220123291,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.807007786429366,
  "slope_sign_acc": 0.9835751437174924,
  "theta_flat_mae_deg": 1.093949317932129,
  "theta_flat_abs_p95_deg": 3.748014450073242,
  "theta_flat_abs_max_deg": 10.677753448486328,
  "theta_flat_bias_deg": 0.36453136801719666,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4806272983551025,
  "theta_near_flat_abs_p95_deg": 5.062839984893799,
  "theta_near_flat_abs_max_deg": 10.677753448486328,
  "theta_near_flat_bias_deg": 0.4865145683288574,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3163299560546875,
  "theta_flat_turn_abs_p95_deg": 5.81085205078125,
  "theta_flat_turn_abs_max_deg": 10.677753448486328,
  "theta_flat_turn_bias_deg": -0.2831849753856659,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7650759220123291,
  "theta_slope_control_abs_p95_deg": 9.239850044250488,
  "theta_slope_control_abs_max_deg": 11.569416999816895,
  "theta_slope_control_bias_deg": 0.06171315535902977,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7650759220123291,
  "theta_all_rmse_deg": 1.2217940092086792,
  "theta_all_p95_abs_err_deg": 2.8390560150146484,
  "theta_all_max_abs_err_deg": 10.177754402160645,
  "theta_all_bias_deg": 0.06171315908432007,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6929565072059631,
  "theta_active_abs_ge_2_rmse_deg": 1.0679601430892944,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.396632671356201,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.230494022369385,
  "theta_active_abs_ge_2_bias_deg": -0.0046925731003284454,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7950807809829712,
  "theta_abs_le_8_rmse_deg": 1.268262267112732,
  "theta_abs_le_8_p95_abs_err_deg": 3.0478413105010986,
  "theta_abs_le_8_max_abs_err_deg": 10.177754402160645,
  "theta_abs_le_8_bias_deg": 0.08920031040906906,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7650759220123291,
  "theta_abs_le_10_rmse_deg": 1.2217940092086792,
  "theta_abs_le_10_p95_abs_err_deg": 2.8390560150146484,
  "theta_abs_le_10_max_abs_err_deg": 10.177754402160645,
  "theta_abs_le_10_bias_deg": 0.06171315908432007,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5805796980857849,
  "theta_pos_8_10_rmse_deg": 0.8634502291679382,
  "theta_pos_8_10_p95_abs_err_deg": 1.7383378744125366,
  "theta_pos_8_10_max_abs_err_deg": 4.835575580596924,
  "theta_pos_8_10_bias_deg": -0.3423527181148529,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6974184513092041,
  "theta_neg_10_8_rmse_deg": 1.1261637210845947,
  "theta_neg_10_8_p95_abs_err_deg": 1.6702916622161865,
  "theta_neg_10_8_max_abs_err_deg": 7.230494022369385,
  "theta_neg_10_8_bias_deg": 0.23884768784046173,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5208031535148621,
  "theta_pos_6_8_rmse_deg": 0.7675999999046326,
  "theta_pos_6_8_p95_abs_err_deg": 1.4801567792892456,
  "theta_pos_6_8_max_abs_err_deg": 3.352095365524292,
  "theta_pos_6_8_bias_deg": -0.14797453582286835,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7003518342971802,
  "theta_neg_8_6_rmse_deg": 1.044289231300354,
  "theta_neg_8_6_p95_abs_err_deg": 2.0417068004608154,
  "theta_neg_8_6_max_abs_err_deg": 6.210064888000488,
  "theta_neg_8_6_bias_deg": 0.009254815056920052,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6618244647979736,
  "theta_neg_4_2_rmse_deg": 0.9453408122062683,
  "theta_neg_4_2_p95_abs_err_deg": 1.9251869916915894,
  "theta_neg_4_2_max_abs_err_deg": 4.443645000457764,
  "theta_neg_4_2_bias_deg": -0.23725447058677673,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.42582419514656067,
  "theta_neg_2_0p5_rmse_deg": 0.5888651013374329,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0630196332931519,
  "theta_neg_2_0p5_max_abs_err_deg": 3.732330560684204,
  "theta_neg_2_0p5_bias_deg": -0.011428862810134888,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2940250635147095,
  "theta_pos_0p5_2_rmse_deg": 1.5626648664474487,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.416374683380127,
  "theta_pos_0p5_2_max_abs_err_deg": 4.701561450958252,
  "theta_pos_0p5_2_bias_deg": 0.8148105144500732,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3027764483701554,
  "loss_turn": 1.2658365482567773,
  "loss_theta": 0.0004546235238154027,
  "loss_main_bundle_base": 0.3027764483701554,
  "loss_turn_bundle_base": 0.10126692292372493,
  "loss_theta_bundle_base": 0.00030877888227872176,
  "loss_main_bundle": 0.3027764483701554,
  "loss_turn_bundle": 0.10126692292372493,
  "loss_theta_bundle": 0.00030877888227872176,
  "loss_theta_flat": 0.00031209863510130273,
  "loss_theta_near_flat": 0.0016800579564527423,
  "loss_theta_error_excess": 0.0001857098182288398,
  "loss_theta_flat_excess": 0.00015340976643570724,
  "loss_theta_near_flat_excess": 0.0012692587035525395,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011998614503785273,
  "loss_theta_small_neg": 0.00026906480660147876,
  "loss_theta_small_neg_excess": 6.954688237789711e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3623330244514713,
  "loss_false_turn_straight": 0.286108067159885,
  "loss_transition_focal_raw": 1.116567212996528,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.4520234882529115,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
