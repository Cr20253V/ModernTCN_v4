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
  "lambda_theta_error_excess": 0.0,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.0,
  "lambda_theta_active_excess": 0.0,
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
    1.0,
    1.1,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_turn_lr_weight": 0.0,
  "select_turn_lr_target": 0.8,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.15,
  "select_theta_ref_deg": 5.0,
  "select_theta_p95_weight": 0.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 0.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 0.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.0,
  "select_theta_extreme_p95_target_deg": 1.0,
  "select_theta_edge_p95_weight": 0.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.0,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2,
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
| acc_main | 0.9670 |
| acc_turn | 0.5788 |
| acc_turn_pure | 0.5974 |
| acc_turn_transition | 0.4978 |
| main_confidence_mean | 0.9877 |
| main_low_conf_0p60_ratio | 0.0094 |
| main_low_conf_0p70_ratio | 0.0153 |
| turn_confidence_mean | 0.8373 |
| turn_low_conf_0p60_ratio | 0.1452 |
| turn_low_conf_0p70_ratio | 0.2401 |
| turn_right_recall | 0.6120 |
| turn_straight_recall | 0.5763 |
| turn_left_recall | 0.5540 |
| theta_mae_deg | 0.6794 |
| theta_abs_le_10_p95_abs_err_deg | 1.8275 |
| theta_neg_10_8_p95_abs_err_deg | 1.3394 |
| theta_pos_8_10_p95_abs_err_deg | 2.7551 |
| theta_abs_le_8_p95_abs_err_deg | 1.7706 |
| theta_neg_8_6_p95_abs_err_deg | 1.7457 |
| theta_pos_6_8_p95_abs_err_deg | 1.5541 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5686 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5545 |
| theta_flat_abs_p95_deg | 2.5565 |
| theta_flat_bias_deg | -0.4761 |
| theta_near_flat_abs_p95_deg | 2.3973 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5854 |
| theta_flat_turn_abs_p95_deg | 2.2504 |
| flat_recall | 0.9696 |
| stall_recall | 0.7188 |
| slope_recall | 0.9749 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7494 |
| downhill_recall | 0.7928 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    733,
    0,
    23
  ],
  [
    9,
    69,
    18
  ],
  [
    65,
    4,
    2681
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    489,
    181,
    129
  ],
  [
    432,
    1114,
    387
  ],
  [
    198,
    190,
    482
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.333101 |
| test_loss_turn_bundle_base | 0.313487 |
| test_loss_theta_bundle_base | 0.000177 |
| test_loss_transition_focal_raw | 1.469700 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.539931 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 0
- train_seconds: 0.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 34 | 0.5588 | 0.5477 |
| [0.60,0.70) | 21 | 0.4762 | 0.6452 |
| [0.70,0.80) | 32 | 0.2500 | 0.7511 |
| [0.80,0.90) | 36 | 0.3056 | 0.8558 |
| [0.90,1.00) | 3479 | 0.0204 | 0.9976 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 523 | 0.6157 | 0.5127 |
| [0.60,0.70) | 342 | 0.6111 | 0.6497 |
| [0.70,0.80) | 355 | 0.5014 | 0.7537 |
| [0.80,0.90) | 523 | 0.4876 | 0.8545 |
| [0.90,1.00) | 1859 | 0.2975 | 0.9742 |


## 验证集最佳点

```json
{
  "loss_total": 0.6467656424927883,
  "acc_main": 0.9669627984453082,
  "acc_turn": 0.5788450860632982,
  "acc_turn_pure": 0.5974070283179802,
  "acc_turn_transition": 0.4977645305514158,
  "false_turn_straight": 0.42369374030005175,
  "flat_recall": 0.9695767195767195,
  "stall_recall": 0.71875,
  "slope_recall": 0.974909090909091,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.09375,
  "recall_main": [
    0.9695767195767195,
    0.71875,
    0.974909090909091
  ],
  "turn_right_recall": 0.6120150187734669,
  "turn_straight_recall": 0.5763062596999483,
  "turn_left_recall": 0.5540229885057472,
  "recall_turn": [
    0.6120150187734669,
    0.5763062596999483,
    0.5540229885057472
  ],
  "cm_turn": [
    [
      489,
      181,
      129
    ],
    [
      432,
      1114,
      387
    ],
    [
      198,
      190,
      482
    ]
  ],
  "n_turn_transition": 671,
  "n_turn_pure": 2931,
  "cm_main": [
    [
      733,
      0,
      23
    ],
    [
      9,
      69,
      18
    ],
    [
      65,
      4,
      2681
    ]
  ],
  "main_confidence_mean": 0.9876970443819668,
  "main_confidence_error_mean": 0.8583919479086624,
  "main_low_conf_0p60_ratio": 0.009439200444197668,
  "main_low_conf_0p70_ratio": 0.01526929483620211,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 34,
      "error_rate": 0.5588235294117647,
      "mean_confidence": 0.5476946204512925
    },
    {
      "bin": "[0.60,0.70)",
      "n": 21,
      "error_rate": 0.47619047619047616,
      "mean_confidence": 0.6451861315294569
    },
    {
      "bin": "[0.70,0.80)",
      "n": 32,
      "error_rate": 0.25,
      "mean_confidence": 0.7510864427280344
    },
    {
      "bin": "[0.80,0.90)",
      "n": 36,
      "error_rate": 0.3055555555555556,
      "mean_confidence": 0.8557785268568797
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3479,
      "error_rate": 0.02040816326530612,
      "mean_confidence": 0.9976060462409421
    }
  ],
  "turn_confidence_mean": 0.83726716650093,
  "turn_confidence_error_mean": 0.7813580563852969,
  "turn_low_conf_0p60_ratio": 0.14519711271515826,
  "turn_low_conf_0p70_ratio": 0.24014436424208774,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 523,
      "error_rate": 0.615678776290631,
      "mean_confidence": 0.512742255324414
    },
    {
      "bin": "[0.60,0.70)",
      "n": 342,
      "error_rate": 0.6111111111111112,
      "mean_confidence": 0.6496568420862001
    },
    {
      "bin": "[0.70,0.80)",
      "n": 355,
      "error_rate": 0.5014084507042254,
      "mean_confidence": 0.7536527108067077
    },
    {
      "bin": "[0.80,0.90)",
      "n": 523,
      "error_rate": 0.4875717017208413,
      "mean_confidence": 0.854491307532483
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1859,
      "error_rate": 0.29747175901022055,
      "mean_confidence": 0.9742032426209419
    }
  ],
  "theta_mae_rad": 0.011857676319777966,
  "theta_mae_deg": 0.6793947815895081,
  "uphill_recall": 0.7494266055045872,
  "downhill_recall": 0.7928490351872872,
  "slope_sign_acc": 0.9746149458071877,
  "theta_flat_mae_deg": 0.6804767847061157,
  "theta_flat_abs_p95_deg": 2.556459426879883,
  "theta_flat_abs_max_deg": 5.335740089416504,
  "theta_flat_bias_deg": -0.4760620892047882,
  "theta_flat_n": 756.0,
  "theta_near_flat_mae_deg": 0.7597319483757019,
  "theta_near_flat_abs_p95_deg": 2.3973114490509033,
  "theta_near_flat_abs_max_deg": 5.335740089416504,
  "theta_near_flat_bias_deg": -0.5854495167732239,
  "theta_near_flat_n": 278.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.7237989902496338,
  "theta_flat_turn_abs_p95_deg": 2.250434398651123,
  "theta_flat_turn_abs_max_deg": 4.876500129699707,
  "theta_flat_turn_bias_deg": -0.6099697351455688,
  "theta_flat_turn_n": 141.0,
  "theta_slope_control_mae_deg": 0.6793947815895081,
  "theta_slope_control_abs_p95_deg": 9.625502586364746,
  "theta_slope_control_abs_max_deg": 12.749197959899902,
  "theta_slope_control_bias_deg": -0.2525699734687805,
  "theta_slope_control_n": 3506.0,
  "theta_all_mae_deg": 0.6793947815895081,
  "theta_all_rmse_deg": 0.9201287627220154,
  "theta_all_p95_abs_err_deg": 1.8274656534194946,
  "theta_all_max_abs_err_deg": 6.077713489532471,
  "theta_all_bias_deg": -0.2525699734687805,
  "theta_all_n": 3506.0,
  "theta_active_abs_ge_2_mae_deg": 0.6790974140167236,
  "theta_active_abs_ge_2_rmse_deg": 0.9289533495903015,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.83830726146698,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.077713489532471,
  "theta_active_abs_ge_2_bias_deg": -0.19112996757030487,
  "theta_active_abs_ge_2_n": 2750.0,
  "theta_abs_le_8_mae_deg": 0.6618751883506775,
  "theta_abs_le_8_rmse_deg": 0.8755007982254028,
  "theta_abs_le_8_p95_abs_err_deg": 1.7706108093261719,
  "theta_abs_le_8_max_abs_err_deg": 5.811408996582031,
  "theta_abs_le_8_bias_deg": -0.25670430064201355,
  "theta_abs_le_8_n": 2815.0,
  "theta_abs_le_10_mae_deg": 0.6793947815895081,
  "theta_abs_le_10_rmse_deg": 0.9201287627220154,
  "theta_abs_le_10_p95_abs_err_deg": 1.8274656534194946,
  "theta_abs_le_10_max_abs_err_deg": 6.077713489532471,
  "theta_abs_le_10_bias_deg": -0.2525699734687805,
  "theta_abs_le_10_n": 3506.0,
  "theta_pos_8_10_mae_deg": 0.9173101782798767,
  "theta_pos_8_10_rmse_deg": 1.301466941833496,
  "theta_pos_8_10_p95_abs_err_deg": 2.755056858062744,
  "theta_pos_8_10_max_abs_err_deg": 6.077713489532471,
  "theta_pos_8_10_bias_deg": -0.4389483332633972,
  "theta_pos_8_10_n": 328.0,
  "theta_neg_10_8_mae_deg": 0.6002802848815918,
  "theta_neg_10_8_rmse_deg": 0.8381986021995544,
  "theta_neg_10_8_p95_abs_err_deg": 1.3394113779067993,
  "theta_neg_10_8_max_abs_err_deg": 4.854050636291504,
  "theta_neg_10_8_bias_deg": -0.052101049572229385,
  "theta_neg_10_8_n": 363.0,
  "theta_pos_6_8_mae_deg": 0.5540636777877808,
  "theta_pos_6_8_rmse_deg": 0.7625554800033569,
  "theta_pos_6_8_p95_abs_err_deg": 1.5540721416473389,
  "theta_pos_6_8_max_abs_err_deg": 3.742820978164673,
  "theta_pos_6_8_bias_deg": 0.00013053858128841966,
  "theta_pos_6_8_n": 378.0,
  "theta_neg_8_6_mae_deg": 0.6559375524520874,
  "theta_neg_8_6_rmse_deg": 0.8323327898979187,
  "theta_neg_8_6_p95_abs_err_deg": 1.7457143068313599,
  "theta_neg_8_6_max_abs_err_deg": 4.081316947937012,
  "theta_neg_8_6_bias_deg": -0.28892046213150024,
  "theta_neg_8_6_n": 378.0,
  "theta_neg_4_2_mae_deg": 0.7348068952560425,
  "theta_neg_4_2_rmse_deg": 0.922282338142395,
  "theta_neg_4_2_p95_abs_err_deg": 1.859179973602295,
  "theta_neg_4_2_max_abs_err_deg": 4.31748628616333,
  "theta_neg_4_2_bias_deg": -0.4921816885471344,
  "theta_neg_4_2_n": 330.0,
  "theta_neg_2_0p5_mae_deg": 0.6102249622344971,
  "theta_neg_2_0p5_rmse_deg": 0.7803658843040466,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.568618893623352,
  "theta_neg_2_0p5_max_abs_err_deg": 2.711951732635498,
  "theta_neg_2_0p5_bias_deg": -0.40880441665649414,
  "theta_neg_2_0p5_n": 207.0,
  "theta_pos_0p5_2_mae_deg": 0.6528353095054626,
  "theta_pos_0p5_2_rmse_deg": 0.8134311437606812,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.5544679164886475,
  "theta_pos_0p5_2_max_abs_err_deg": 3.1619760990142822,
  "theta_pos_0p5_2_bias_deg": -0.4152231216430664,
  "theta_pos_0p5_2_n": 271.0,
  "loss_main": 0.3331013734218174,
  "loss_turn": 1.5674374358379992,
  "loss_theta": 0.00025772682898137503,
  "loss_main_bundle_base": 0.3331013734218174,
  "loss_turn_bundle_base": 0.31348749226593164,
  "loss_theta_bundle_base": 0.0001767743433174625,
  "loss_main_bundle": 0.3331013734218174,
  "loss_turn_bundle": 0.31348749226593164,
  "loss_theta_bundle": 0.0001767743433174625,
  "loss_theta_flat": 0.00029187151972930476,
  "loss_theta_near_flat": 0.0004347848412743679,
  "loss_theta_error_excess": 5.5492254996544025e-05,
  "loss_theta_flat_excess": 0.00011035892000625625,
  "loss_theta_near_flat_excess": 0.00022638659419565318,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 5.9037307680800126e-05,
  "loss_theta_small_neg": 0.0002611149183086904,
  "loss_theta_small_neg_excess": 3.7203169242895315e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.41572827964541254,
  "loss_false_turn_straight": 0.3097978324889475,
  "loss_transition_focal_raw": 1.4697002403475323,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.5399309142857938,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
