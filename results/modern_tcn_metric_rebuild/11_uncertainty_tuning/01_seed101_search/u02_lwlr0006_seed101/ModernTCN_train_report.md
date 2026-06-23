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
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9689 |
| acc_turn | 0.5908 |
| acc_turn_pure | 0.6076 |
| acc_turn_transition | 0.5171 |
| main_confidence_mean | 0.9903 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0130 |
| turn_confidence_mean | 0.8479 |
| turn_low_conf_0p60_ratio | 0.1371 |
| turn_low_conf_0p70_ratio | 0.2396 |
| turn_right_recall | 0.6170 |
| turn_straight_recall | 0.6048 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.6719 |
| theta_abs_le_10_p95_abs_err_deg | 1.7238 |
| theta_neg_10_8_p95_abs_err_deg | 1.6574 |
| theta_pos_8_10_p95_abs_err_deg | 2.7911 |
| theta_abs_le_8_p95_abs_err_deg | 1.6417 |
| theta_neg_8_6_p95_abs_err_deg | 1.6419 |
| theta_pos_6_8_p95_abs_err_deg | 1.5110 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2322 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6561 |
| theta_flat_abs_p95_deg | 2.4640 |
| theta_flat_bias_deg | -0.0597 |
| theta_near_flat_abs_p95_deg | 1.9757 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2616 |
| theta_flat_turn_abs_p95_deg | 1.7836 |
| flat_recall | 0.9643 |
| stall_recall | 0.7083 |
| slope_recall | 0.9793 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7569 |
| downhill_recall | 0.7946 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    729,
    0,
    27
  ],
  [
    10,
    68,
    18
  ],
  [
    52,
    5,
    2693
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    493,
    205,
    101
  ],
  [
    373,
    1169,
    391
  ],
  [
    168,
    236,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.370539 |
| test_loss_turn_bundle_base | 0.377854 |
| test_loss_theta_bundle_base | 0.000161 |
| test_loss_transition_focal_raw | 1.699051 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.068943 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 88
- train_seconds: 388.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.2917 | 0.5307 |
| [0.60,0.70) | 23 | 0.5652 | 0.6529 |
| [0.70,0.80) | 18 | 0.2778 | 0.7586 |
| [0.80,0.90) | 38 | 0.3158 | 0.8526 |
| [0.90,1.00) | 3499 | 0.0214 | 0.9984 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 494 | 0.6275 | 0.5307 |
| [0.60,0.70) | 369 | 0.5176 | 0.6470 |
| [0.70,0.80) | 344 | 0.4680 | 0.7545 |
| [0.80,0.90) | 394 | 0.5025 | 0.8546 |
| [0.90,1.00) | 2001 | 0.3068 | 0.9780 |


## 验证集最佳点

```json
{
  "loss_total": 0.7209984344784397,
  "acc_main": 0.9420838971583221,
  "acc_turn": 0.6346414073071719,
  "acc_turn_pure": 0.6473287446738775,
  "acc_turn_transition": 0.5745341614906833,
  "false_turn_straight": 0.4028066528066528,
  "flat_recall": 0.943683409436834,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.9506008010680908,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.943683409436834,
    0.30952380952380953,
    0.9506008010680908
  ],
  "turn_right_recall": 0.6327014218009479,
  "turn_straight_recall": 0.5971933471933472,
  "turn_left_recall": 0.7141316073354909,
  "recall_turn": [
    0.6327014218009479,
    0.5971933471933472,
    0.7141316073354909
  ],
  "cm_turn": [
    [
      534,
      212,
      98
    ],
    [
      301,
      1149,
      474
    ],
    [
      42,
      223,
      662
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      620,
      0,
      37
    ],
    [
      1,
      13,
      28
    ],
    [
      139,
      9,
      2848
    ]
  ],
  "main_confidence_mean": 0.9688167588255965,
  "main_confidence_error_mean": 0.7607606559527177,
  "main_low_conf_0p60_ratio": 0.0503382949932341,
  "main_low_conf_0p70_ratio": 0.05412719891745602,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 186,
      "error_rate": 0.4731182795698925,
      "mean_confidence": 0.49915018893135094
    },
    {
      "bin": "[0.60,0.70)",
      "n": 14,
      "error_rate": 0.5,
      "mean_confidence": 0.6491924043811316
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.2962962962962963,
      "mean_confidence": 0.754399859519374
    },
    {
      "bin": "[0.80,0.90)",
      "n": 35,
      "error_rate": 0.34285714285714286,
      "mean_confidence": 0.8571234381356274
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3433,
      "error_rate": 0.02883775123798427,
      "mean_confidence": 0.998391837610324
    }
  ],
  "turn_confidence_mean": 0.8633909356608883,
  "turn_confidence_error_mean": 0.7890149527820266,
  "turn_low_conf_0p60_ratio": 0.12774018944519622,
  "turn_low_conf_0p70_ratio": 0.1986468200270636,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 472,
      "error_rate": 0.6440677966101694,
      "mean_confidence": 0.48924328956534274
    },
    {
      "bin": "[0.60,0.70)",
      "n": 262,
      "error_rate": 0.4847328244274809,
      "mean_confidence": 0.6513486265700955
    },
    {
      "bin": "[0.70,0.80)",
      "n": 292,
      "error_rate": 0.5068493150684932,
      "mean_confidence": 0.754906398571403
    },
    {
      "bin": "[0.80,0.90)",
      "n": 409,
      "error_rate": 0.5012224938875306,
      "mean_confidence": 0.8504167544536895
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2260,
      "error_rate": 0.2504424778761062,
      "mean_confidence": 0.982477970564764
    }
  ],
  "theta_mae_rad": 0.014222213998436928,
  "theta_mae_deg": 0.8148728013038635,
  "uphill_recall": 0.7757412398921832,
  "downhill_recall": 0.8042269187986651,
  "slope_sign_acc": 0.9690665206679442,
  "theta_flat_mae_deg": 1.0307812690734863,
  "theta_flat_abs_p95_deg": 3.602234125137329,
  "theta_flat_abs_max_deg": 6.316073417663574,
  "theta_flat_bias_deg": 0.34904348850250244,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3955049514770508,
  "theta_near_flat_abs_p95_deg": 3.7331326007843018,
  "theta_near_flat_abs_max_deg": 6.316073417663574,
  "theta_near_flat_bias_deg": 0.7222601175308228,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1086833477020264,
  "theta_flat_turn_abs_p95_deg": 3.602159261703491,
  "theta_flat_turn_abs_max_deg": 6.316073417663574,
  "theta_flat_turn_bias_deg": 0.16288912296295166,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8148728013038635,
  "theta_slope_control_abs_p95_deg": 9.016369819641113,
  "theta_slope_control_abs_max_deg": 12.23672103881836,
  "theta_slope_control_bias_deg": -0.17685876786708832,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8148727416992188,
  "theta_all_rmse_deg": 1.1538692712783813,
  "theta_all_p95_abs_err_deg": 2.4305052757263184,
  "theta_all_max_abs_err_deg": 6.010361194610596,
  "theta_all_bias_deg": -0.17685876786708832,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7675256729125977,
  "theta_active_abs_ge_2_rmse_deg": 1.0619566440582275,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1151561737060547,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.010361194610596,
  "theta_active_abs_ge_2_bias_deg": -0.29218509793281555,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8266687393188477,
  "theta_abs_le_8_rmse_deg": 1.1713848114013672,
  "theta_abs_le_8_p95_abs_err_deg": 2.6260874271392822,
  "theta_abs_le_8_max_abs_err_deg": 5.816072940826416,
  "theta_abs_le_8_bias_deg": -0.14329169690608978,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8148727416992188,
  "theta_abs_le_10_rmse_deg": 1.1538692712783813,
  "theta_abs_le_10_p95_abs_err_deg": 2.4305052757263184,
  "theta_abs_le_10_max_abs_err_deg": 6.010361194610596,
  "theta_abs_le_10_bias_deg": -0.17685876786708832,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.875923752784729,
  "theta_pos_8_10_rmse_deg": 1.0074542760849,
  "theta_pos_8_10_p95_abs_err_deg": 1.536011815071106,
  "theta_pos_8_10_max_abs_err_deg": 4.699394226074219,
  "theta_pos_8_10_bias_deg": -0.768505871295929,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6523818969726562,
  "theta_neg_10_8_rmse_deg": 1.143126130104065,
  "theta_neg_10_8_p95_abs_err_deg": 2.1551601886749268,
  "theta_neg_10_8_max_abs_err_deg": 6.010361194610596,
  "theta_neg_10_8_bias_deg": 0.13935992121696472,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7850987315177917,
  "theta_pos_6_8_rmse_deg": 0.9693384766578674,
  "theta_pos_6_8_p95_abs_err_deg": 1.7510586977005005,
  "theta_pos_6_8_max_abs_err_deg": 3.003795862197876,
  "theta_pos_6_8_bias_deg": -0.5551135540008545,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7585400938987732,
  "theta_neg_8_6_rmse_deg": 1.128061294555664,
  "theta_neg_8_6_p95_abs_err_deg": 2.322497844696045,
  "theta_neg_8_6_max_abs_err_deg": 5.660746097564697,
  "theta_neg_8_6_bias_deg": 0.08683007210493088,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7884880900382996,
  "theta_neg_4_2_rmse_deg": 1.075623631477356,
  "theta_neg_4_2_p95_abs_err_deg": 2.027294397354126,
  "theta_neg_4_2_max_abs_err_deg": 4.913649559020996,
  "theta_neg_4_2_bias_deg": -0.46886318922042847,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5871462225914001,
  "theta_neg_2_0p5_rmse_deg": 0.856777548789978,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6106793880462646,
  "theta_neg_2_0p5_max_abs_err_deg": 4.281617164611816,
  "theta_neg_2_0p5_bias_deg": -0.1916232854127884,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0356987714767456,
  "theta_pos_0p5_2_rmse_deg": 1.2989181280136108,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.102159261703491,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9604671001434326,
  "theta_pos_0p5_2_bias_deg": 0.49625831842422485,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.40433994497756026,
  "loss_turn": 1.5819824833347285,
  "loss_theta": 0.000405527623080433,
  "loss_main_bundle_base": 0.40433994497756026,
  "loss_turn_bundle_base": 0.31639649997060776,
  "loss_theta_bundle_base": 0.00026198663870572126,
  "loss_main_bundle": 0.40433994497756026,
  "loss_turn_bundle": 0.31639649997060776,
  "loss_theta_bundle": 0.00026198663870572126,
  "loss_theta_flat": 0.00019357307448053407,
  "loss_theta_near_flat": 0.0011717498238502178,
  "loss_theta_error_excess": 0.00012697962210236397,
  "loss_theta_flat_excess": 0.00010311283870791249,
  "loss_theta_near_flat_excess": 0.0008074980898960638,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.368686546591716e-05,
  "loss_theta_small_neg": 0.00035047724339556507,
  "loss_theta_small_neg_excess": 9.081910854408389e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.37586760334620134,
  "loss_false_turn_straight": 0.30026649952902684,
  "loss_transition_focal_raw": 1.5060393307141264,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.900778719775391,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
