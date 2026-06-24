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
  "lambda_theta_flat": 0.2,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.1,
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
  "theta_flat_excess_target_deg": 0.4,
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
  "select_theta_flat_peak_weight": 1.8,
  "select_theta_flat_peak_target_deg": 4.8,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 0.7,
  "select_theta_edge_p95_target_deg": 1.25,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9672 |
| acc_turn | 0.5894 |
| acc_turn_pure | 0.5995 |
| acc_turn_transition | 0.5455 |
| main_confidence_mean | 0.9887 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0178 |
| turn_confidence_mean | 0.8502 |
| turn_low_conf_0p60_ratio | 0.1288 |
| turn_low_conf_0p70_ratio | 0.2171 |
| turn_right_recall | 0.5807 |
| turn_straight_recall | 0.6151 |
| turn_left_recall | 0.5402 |
| theta_mae_deg | 0.6579 |
| theta_abs_le_10_p95_abs_err_deg | 1.7112 |
| theta_neg_10_8_p95_abs_err_deg | 1.8740 |
| theta_pos_8_10_p95_abs_err_deg | 2.2598 |
| theta_abs_le_8_p95_abs_err_deg | 1.6656 |
| theta_neg_8_6_p95_abs_err_deg | 1.4432 |
| theta_pos_6_8_p95_abs_err_deg | 1.6167 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4509 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5706 |
| theta_flat_abs_p95_deg | 2.2292 |
| theta_flat_bias_deg | -0.3719 |
| theta_near_flat_abs_p95_deg | 1.6427 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3480 |
| theta_flat_turn_abs_p95_deg | 1.3399 |
| flat_recall | 0.9537 |
| stall_recall | 0.6875 |
| slope_recall | 0.9807 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7597 |
| downhill_recall | 0.7985 |

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
    10,
    66,
    20
  ],
  [
    46,
    7,
    2697
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    464,
    207,
    128
  ],
  [
    296,
    1189,
    448
  ],
  [
    135,
    265,
    470
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.308812 |
| test_loss_turn_bundle_base | 0.357554 |
| test_loss_theta_bundle_base | 0.000186 |
| test_loss_transition_focal_raw | 1.502065 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.186763 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 81
- train_seconds: 371.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.4583 | 0.5490 |
| [0.60,0.70) | 40 | 0.3250 | 0.6628 |
| [0.70,0.80) | 24 | 0.4583 | 0.7605 |
| [0.80,0.90) | 31 | 0.4194 | 0.8566 |
| [0.90,1.00) | 3483 | 0.0201 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 464 | 0.5927 | 0.5219 |
| [0.60,0.70) | 318 | 0.5849 | 0.6505 |
| [0.70,0.80) | 393 | 0.5369 | 0.7483 |
| [0.80,0.90) | 449 | 0.4878 | 0.8520 |
| [0.90,1.00) | 1978 | 0.2973 | 0.9792 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.5455

## 验证集最佳点

```json
{
  "loss_total": 0.5980645449784192,
  "acc_main": 0.9420838971583221,
  "acc_turn": 0.6527740189445196,
  "acc_turn_pure": 0.6624057686004589,
  "acc_turn_transition": 0.6071428571428571,
  "false_turn_straight": 0.3659043659043659,
  "flat_recall": 0.939117199391172,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9499332443257676,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.939117199391172,
    0.42857142857142855,
    0.9499332443257676
  ],
  "turn_right_recall": 0.6255924170616114,
  "turn_straight_recall": 0.6340956340956341,
  "turn_left_recall": 0.7162891046386192,
  "recall_turn": [
    0.6255924170616114,
    0.6340956340956341,
    0.7162891046386192
  ],
  "cm_turn": [
    [
      528,
      229,
      87
    ],
    [
      261,
      1220,
      443
    ],
    [
      43,
      220,
      664
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      617,
      0,
      40
    ],
    [
      0,
      18,
      24
    ],
    [
      144,
      6,
      2846
    ]
  ],
  "main_confidence_mean": 0.9720126167109012,
  "main_confidence_error_mean": 0.7851611957311477,
  "main_low_conf_0p60_ratio": 0.050608930987821384,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 187,
      "error_rate": 0.44919786096256686,
      "mean_confidence": 0.5928148802217774
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.52,
      "mean_confidence": 0.6645677402753808
    },
    {
      "bin": "[0.70,0.80)",
      "n": 22,
      "error_rate": 0.5909090909090909,
      "mean_confidence": 0.74156685669036
    },
    {
      "bin": "[0.80,0.90)",
      "n": 52,
      "error_rate": 0.36538461538461536,
      "mean_confidence": 0.8570093039488771
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3409,
      "error_rate": 0.024933998239953067,
      "mean_confidence": 0.9983095007292149
    }
  ],
  "turn_confidence_mean": 0.85728272752397,
  "turn_confidence_error_mean": 0.7806520380003814,
  "turn_low_conf_0p60_ratio": 0.12963464140730718,
  "turn_low_conf_0p70_ratio": 0.20351826792963465,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 479,
      "error_rate": 0.6367432150313153,
      "mean_confidence": 0.48122780874719234
    },
    {
      "bin": "[0.60,0.70)",
      "n": 273,
      "error_rate": 0.48717948717948717,
      "mean_confidence": 0.6543178616344936
    },
    {
      "bin": "[0.70,0.80)",
      "n": 324,
      "error_rate": 0.43209876543209874,
      "mean_confidence": 0.7509081698064686
    },
    {
      "bin": "[0.80,0.90)",
      "n": 429,
      "error_rate": 0.3962703962703963,
      "mean_confidence": 0.8519963899536852
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2190,
      "error_rate": 0.24429223744292236,
      "mean_confidence": 0.9816082572043471
    }
  ],
  "theta_mae_rad": 0.012857113964855671,
  "theta_mae_deg": 0.7366583347320557,
  "uphill_recall": 0.7746630727762803,
  "downhill_recall": 0.8058954393770856,
  "slope_sign_acc": 0.9748152203668218,
  "theta_flat_mae_deg": 1.0106860399246216,
  "theta_flat_abs_p95_deg": 3.6569454669952393,
  "theta_flat_abs_max_deg": 5.985214710235596,
  "theta_flat_bias_deg": 0.22304196655750275,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3499521017074585,
  "theta_near_flat_abs_p95_deg": 3.657011032104492,
  "theta_near_flat_abs_max_deg": 6.587342739105225,
  "theta_near_flat_bias_deg": 0.6195878982543945,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0537443161010742,
  "theta_flat_turn_abs_p95_deg": 3.6569454669952393,
  "theta_flat_turn_abs_max_deg": 5.762345790863037,
  "theta_flat_turn_bias_deg": 0.11824753880500793,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7366583347320557,
  "theta_slope_control_abs_p95_deg": 9.49043083190918,
  "theta_slope_control_abs_max_deg": 12.557784080505371,
  "theta_slope_control_bias_deg": -0.15973810851573944,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7366583347320557,
  "theta_all_rmse_deg": 1.0893633365631104,
  "theta_all_p95_abs_err_deg": 2.25512957572937,
  "theta_all_max_abs_err_deg": 6.795154094696045,
  "theta_all_bias_deg": -0.15973809361457825,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6765661239624023,
  "theta_active_abs_ge_2_rmse_deg": 0.9938704967498779,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9671545028686523,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.795154094696045,
  "theta_active_abs_ge_2_bias_deg": -0.24367886781692505,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7762032151222229,
  "theta_abs_le_8_rmse_deg": 1.1171190738677979,
  "theta_abs_le_8_p95_abs_err_deg": 2.39288330078125,
  "theta_abs_le_8_max_abs_err_deg": 5.867803573608398,
  "theta_abs_le_8_bias_deg": -0.1562858521938324,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7366583347320557,
  "theta_abs_le_10_rmse_deg": 1.0893633365631104,
  "theta_abs_le_10_p95_abs_err_deg": 2.25512957572937,
  "theta_abs_le_10_max_abs_err_deg": 6.795154094696045,
  "theta_abs_le_10_bias_deg": -0.15973809361457825,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.47401487827301025,
  "theta_pos_8_10_rmse_deg": 0.7098088264465332,
  "theta_pos_8_10_p95_abs_err_deg": 1.4310500621795654,
  "theta_pos_8_10_max_abs_err_deg": 5.4033732414245605,
  "theta_pos_8_10_bias_deg": -0.20968571305274963,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6673125624656677,
  "theta_neg_10_8_rmse_deg": 1.1662864685058594,
  "theta_neg_10_8_p95_abs_err_deg": 2.0557966232299805,
  "theta_neg_10_8_max_abs_err_deg": 6.795154094696045,
  "theta_neg_10_8_bias_deg": -0.13830573856830597,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5508468747138977,
  "theta_pos_6_8_rmse_deg": 0.8070870637893677,
  "theta_pos_6_8_p95_abs_err_deg": 1.5768667459487915,
  "theta_pos_6_8_max_abs_err_deg": 3.581543445587158,
  "theta_pos_6_8_bias_deg": -0.14227837324142456,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7248601317405701,
  "theta_neg_8_6_rmse_deg": 1.0268571376800537,
  "theta_neg_8_6_p95_abs_err_deg": 1.871631383895874,
  "theta_neg_8_6_max_abs_err_deg": 5.867803573608398,
  "theta_neg_8_6_bias_deg": -0.3711789548397064,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7936980724334717,
  "theta_neg_4_2_rmse_deg": 1.127091884613037,
  "theta_neg_4_2_p95_abs_err_deg": 2.243055820465088,
  "theta_neg_4_2_max_abs_err_deg": 5.623660087585449,
  "theta_neg_4_2_bias_deg": -0.6026486754417419,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5664558410644531,
  "theta_neg_2_0p5_rmse_deg": 0.7830554246902466,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5611894130706787,
  "theta_neg_2_0p5_max_abs_err_deg": 3.456186532974243,
  "theta_neg_2_0p5_bias_deg": -0.4547119438648224,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1497687101364136,
  "theta_pos_0p5_2_rmse_deg": 1.428601622581482,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.17106294631958,
  "theta_pos_0p5_2_max_abs_err_deg": 4.213242053985596,
  "theta_pos_0p5_2_bias_deg": 0.5687824487686157,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.27698089035180007,
  "loss_turn": 1.6040496602593965,
  "loss_theta": 0.00036145663808864894,
  "loss_main_bundle_base": 0.27698089035180007,
  "loss_turn_bundle_base": 0.3208099349425836,
  "loss_theta_bundle_base": 0.0002737179794490554,
  "loss_main_bundle": 0.27698089035180007,
  "loss_turn_bundle": 0.3208099349425836,
  "loss_theta_bundle": 0.0002737179794490554,
  "loss_theta_flat": 0.00023712252742999658,
  "loss_theta_near_flat": 0.0010576355400531779,
  "loss_theta_error_excess": 0.00011659031998916215,
  "loss_theta_flat_excess": 0.0001276535593511279,
  "loss_theta_near_flat_excess": 0.0007743089967085923,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.897447945356006e-05,
  "loss_theta_small_neg": 0.00038314876318323214,
  "loss_theta_small_neg_excess": 0.0001174173715772644,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3191651237511022,
  "loss_false_turn_straight": 0.2768833990429348,
  "loss_transition_focal_raw": 1.4387521509549936,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.774321758182527,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
