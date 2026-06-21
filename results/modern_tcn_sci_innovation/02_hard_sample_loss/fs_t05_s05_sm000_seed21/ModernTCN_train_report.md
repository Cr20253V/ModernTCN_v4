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

- lambda_transition_focal: `0.5`
- lambda_stall_focal: `0.5`
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
  "lambda_transition_focal": 0.5,
  "lambda_stall_focal": 0.5,
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
| acc_main | 0.9373 |
| acc_turn | 0.4900 |
| acc_turn_pure | 0.4927 |
| acc_turn_transition | 0.4784 |
| main_confidence_mean | 0.9683 |
| main_low_conf_0p60_ratio | 0.0222 |
| main_low_conf_0p70_ratio | 0.0350 |
| turn_confidence_mean | 0.6439 |
| turn_low_conf_0p60_ratio | 0.4883 |
| turn_low_conf_0p70_ratio | 0.6777 |
| turn_right_recall | 0.5820 |
| turn_straight_recall | 0.4858 |
| turn_left_recall | 0.4149 |
| theta_mae_deg | 0.7824 |
| theta_abs_le_10_p95_abs_err_deg | 2.1808 |
| theta_neg_10_8_p95_abs_err_deg | 2.0297 |
| theta_pos_8_10_p95_abs_err_deg | 3.3648 |
| theta_abs_le_8_p95_abs_err_deg | 2.0651 |
| theta_neg_8_6_p95_abs_err_deg | 2.1539 |
| theta_pos_6_8_p95_abs_err_deg | 1.7684 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7994 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7188 |
| theta_flat_abs_p95_deg | 2.4716 |
| theta_flat_bias_deg | 0.0651 |
| theta_near_flat_abs_p95_deg | 1.7171 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1537 |
| theta_flat_turn_abs_p95_deg | 1.5874 |
| flat_recall | 0.9312 |
| stall_recall | 0.6562 |
| slope_recall | 0.9487 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7139 |
| downhill_recall | 0.8031 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    704,
    1,
    51
  ],
  [
    10,
    63,
    23
  ],
  [
    125,
    16,
    2609
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    465,
    220,
    114
  ],
  [
    504,
    939,
    490
  ],
  [
    223,
    286,
    361
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.363673 |
| test_loss_turn_bundle_base | 0.228211 |
| test_loss_theta_bundle_base | 0.000233 |
| test_loss_transition_focal_raw | 0.662677 |
| test_loss_transition_focal_weighted | 0.331339 |
| test_loss_stall_focal_raw | 3.234040 |
| test_loss_stall_focal_weighted | 1.617020 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 38
- train_seconds: 259.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 80 | 0.6250 | 0.5553 |
| [0.60,0.70) | 46 | 0.3696 | 0.6531 |
| [0.70,0.80) | 66 | 0.3485 | 0.7558 |
| [0.80,0.90) | 154 | 0.2013 | 0.8604 |
| [0.90,1.00) | 3256 | 0.0322 | 0.9923 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1759 | 0.5850 | 0.5043 |
| [0.60,0.70) | 682 | 0.5616 | 0.6477 |
| [0.70,0.80) | 424 | 0.5542 | 0.7458 |
| [0.80,0.90) | 295 | 0.4678 | 0.8476 |
| [0.90,1.00) | 442 | 0.1176 | 0.9597 |


## 验证集最佳点

```json
{
  "loss_total": 2.110045841227365,
  "acc_main": 0.926657645466847,
  "acc_turn": 0.5634641407307172,
  "acc_turn_pure": 0.5624385447394297,
  "acc_turn_transition": 0.5683229813664596,
  "false_turn_straight": 0.4797297297297297,
  "flat_recall": 0.9649923896499238,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9255674232309746,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9649923896499238,
    0.40476190476190477,
    0.9255674232309746
  ],
  "turn_right_recall": 0.6741706161137441,
  "turn_straight_recall": 0.5202702702702703,
  "turn_left_recall": 0.552319309600863,
  "recall_turn": [
    0.6741706161137441,
    0.5202702702702703,
    0.552319309600863
  ],
  "cm_turn": [
    [
      569,
      195,
      80
    ],
    [
      514,
      1001,
      409
    ],
    [
      131,
      284,
      512
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      634,
      0,
      23
    ],
    [
      0,
      17,
      25
    ],
    [
      195,
      28,
      2773
    ]
  ],
  "main_confidence_mean": 0.9491190440347971,
  "main_confidence_error_mean": 0.7377330709566902,
  "main_low_conf_0p60_ratio": 0.05953991880920163,
  "main_low_conf_0p70_ratio": 0.07577807848443843,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 220,
      "error_rate": 0.4590909090909091,
      "mean_confidence": 0.5015389977377327
    },
    {
      "bin": "[0.60,0.70)",
      "n": 60,
      "error_rate": 0.36666666666666664,
      "mean_confidence": 0.653985950952512
    },
    {
      "bin": "[0.70,0.80)",
      "n": 66,
      "error_rate": 0.4393939393939394,
      "mean_confidence": 0.7536901179439699
    },
    {
      "bin": "[0.80,0.90)",
      "n": 112,
      "error_rate": 0.22321428571428573,
      "mean_confidence": 0.8503057907085133
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3237,
      "error_rate": 0.02903923385851097,
      "mean_confidence": 0.9924125223371851
    }
  ],
  "turn_confidence_mean": 0.6668816136715985,
  "turn_confidence_error_mean": 0.61236698016226,
  "turn_low_conf_0p60_ratio": 0.43599458728010826,
  "turn_low_conf_0p70_ratio": 0.6075778078484438,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1611,
      "error_rate": 0.5251396648044693,
      "mean_confidence": 0.5031048853112475
    },
    {
      "bin": "[0.60,0.70)",
      "n": 634,
      "error_rate": 0.5094637223974764,
      "mean_confidence": 0.6480654575148805
    },
    {
      "bin": "[0.70,0.80)",
      "n": 514,
      "error_rate": 0.4260700389105058,
      "mean_confidence": 0.7482600600970444
    },
    {
      "bin": "[0.80,0.90)",
      "n": 372,
      "error_rate": 0.3870967741935484,
      "mean_confidence": 0.8474861523835627
    },
    {
      "bin": "[0.90,1.00)",
      "n": 564,
      "error_rate": 0.14361702127659576,
      "mean_confidence": 0.9625559798566246
    }
  ],
  "theta_mae_rad": 0.016863061115145683,
  "theta_mae_deg": 0.9661821722984314,
  "uphill_recall": 0.7417789757412399,
  "downhill_recall": 0.7897664071190211,
  "slope_sign_acc": 0.9676977826444019,
  "theta_flat_mae_deg": 1.1794190406799316,
  "theta_flat_abs_p95_deg": 3.731248140335083,
  "theta_flat_abs_max_deg": 9.110183715820312,
  "theta_flat_bias_deg": 0.7505581378936768,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6617786884307861,
  "theta_near_flat_abs_p95_deg": 4.0587897300720215,
  "theta_near_flat_abs_max_deg": 9.110183715820312,
  "theta_near_flat_bias_deg": 1.1144492626190186,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.4967206716537476,
  "theta_flat_turn_abs_p95_deg": 4.845766067504883,
  "theta_flat_turn_abs_max_deg": 9.110183715820312,
  "theta_flat_turn_bias_deg": 0.826919674873352,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9661821722984314,
  "theta_slope_control_abs_p95_deg": 9.708937644958496,
  "theta_slope_control_abs_max_deg": 14.043110847473145,
  "theta_slope_control_bias_deg": -0.1241026371717453,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.966182291507721,
  "theta_all_rmse_deg": 1.3603628873825073,
  "theta_all_p95_abs_err_deg": 2.7836098670959473,
  "theta_all_max_abs_err_deg": 9.610182762145996,
  "theta_all_bias_deg": -0.1241026371717453,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9194208979606628,
  "theta_active_abs_ge_2_rmse_deg": 1.2456603050231934,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.5447335243225098,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.304315090179443,
  "theta_active_abs_ge_2_bias_deg": -0.31590908765792847,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9676641225814819,
  "theta_abs_le_8_rmse_deg": 1.3736417293548584,
  "theta_abs_le_8_p95_abs_err_deg": 2.783963680267334,
  "theta_abs_le_8_max_abs_err_deg": 9.610182762145996,
  "theta_abs_le_8_bias_deg": -0.0025430312380194664,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.966182291507721,
  "theta_abs_le_10_rmse_deg": 1.3603628873825073,
  "theta_abs_le_10_p95_abs_err_deg": 2.7836098670959473,
  "theta_abs_le_10_max_abs_err_deg": 9.610182762145996,
  "theta_abs_le_10_bias_deg": -0.1241026371717453,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.8396959900856018,
  "theta_pos_8_10_rmse_deg": 1.0286037921905518,
  "theta_pos_8_10_p95_abs_err_deg": 1.901282787322998,
  "theta_pos_8_10_max_abs_err_deg": 4.918840408325195,
  "theta_pos_8_10_bias_deg": -0.6328651905059814,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 1.0822442770004272,
  "theta_neg_10_8_rmse_deg": 1.5322860479354858,
  "theta_neg_10_8_p95_abs_err_deg": 3.185061454772949,
  "theta_neg_10_8_max_abs_err_deg": 6.474250316619873,
  "theta_neg_10_8_bias_deg": -0.6410257816314697,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7503734827041626,
  "theta_pos_6_8_rmse_deg": 0.9608124494552612,
  "theta_pos_6_8_p95_abs_err_deg": 1.9215075969696045,
  "theta_pos_6_8_max_abs_err_deg": 3.494239091873169,
  "theta_pos_6_8_bias_deg": -0.3571772575378418,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.249173641204834,
  "theta_neg_8_6_rmse_deg": 1.5608394145965576,
  "theta_neg_8_6_p95_abs_err_deg": 2.794034957885742,
  "theta_neg_8_6_max_abs_err_deg": 7.304315090179443,
  "theta_neg_8_6_bias_deg": -0.9440478086471558,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7406175136566162,
  "theta_neg_4_2_rmse_deg": 1.0037583112716675,
  "theta_neg_4_2_p95_abs_err_deg": 1.9908043146133423,
  "theta_neg_4_2_max_abs_err_deg": 4.663531303405762,
  "theta_neg_4_2_bias_deg": -0.2798011600971222,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5815876722335815,
  "theta_neg_2_0p5_rmse_deg": 0.8167967796325684,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1891311407089233,
  "theta_neg_2_0p5_max_abs_err_deg": 5.475682735443115,
  "theta_neg_2_0p5_bias_deg": 0.16911110281944275,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1508166790008545,
  "theta_pos_0p5_2_rmse_deg": 1.4095652103424072,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.231248140335083,
  "theta_pos_0p5_2_max_abs_err_deg": 4.048047065734863,
  "theta_pos_0p5_2_bias_deg": 0.9698894619941711,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3032528800393312,
  "loss_turn": 1.002564778105332,
  "loss_theta": 0.0005638818352178233,
  "loss_main_bundle_base": 0.3032528800393312,
  "loss_turn_bundle_base": 0.20051296054913645,
  "loss_theta_bundle_base": 0.00036713857259172873,
  "loss_main_bundle": 1.6315017198758133,
  "loss_turn_bundle": 0.4781769786216571,
  "loss_theta_bundle": 0.00036713857259172873,
  "loss_theta_flat": 0.0002709002861329663,
  "loss_theta_near_flat": 0.0016918523147316583,
  "loss_theta_error_excess": 0.00020491719365319053,
  "loss_theta_flat_excess": 0.00013656790978848653,
  "loss_theta_near_flat_excess": 0.0012571330228253331,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014249663386876405,
  "loss_theta_small_neg": 0.000305190945519273,
  "loss_theta_small_neg_excess": 6.280626871822217e-05,
  "loss_turn_release": 0.34853150296921015,
  "loss_false_turn_straight": 0.29984240990852956,
  "loss_transition_focal_raw": 0.5553280329107432,
  "loss_transition_focal_weighted": 0.2776640164553716,
  "loss_stall_focal_raw": 2.6564976864887324,
  "loss_stall_focal_weighted": 1.3282488432443662,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
