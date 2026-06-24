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
  "lambda_turn": 0.24,
  "lambda_theta": 0.5,
  "lambda_theta_flat": 0.16,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.04,
  "lambda_theta_flat_excess": 0.05,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
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
  "select_theta_flat_peak_weight": 1.0,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.0,
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
| acc_main | 0.9684 |
| acc_turn | 0.5339 |
| acc_turn_pure | 0.5449 |
| acc_turn_transition | 0.4858 |
| main_confidence_mean | 0.9842 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0167 |
| turn_confidence_mean | 0.7412 |
| turn_low_conf_0p60_ratio | 0.2882 |
| turn_low_conf_0p70_ratio | 0.4334 |
| turn_right_recall | 0.7146 |
| turn_straight_recall | 0.4584 |
| turn_left_recall | 0.5356 |
| theta_mae_deg | 0.5681 |
| theta_abs_le_10_p95_abs_err_deg | 1.5724 |
| theta_neg_10_8_p95_abs_err_deg | 1.1571 |
| theta_pos_8_10_p95_abs_err_deg | 2.2060 |
| theta_abs_le_8_p95_abs_err_deg | 1.5595 |
| theta_neg_8_6_p95_abs_err_deg | 1.6223 |
| theta_pos_6_8_p95_abs_err_deg | 1.1765 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8696 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.5522 |
| theta_flat_abs_p95_deg | 2.7691 |
| theta_flat_bias_deg | 0.6058 |
| theta_near_flat_abs_p95_deg | 2.3176 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.8631 |
| theta_flat_turn_abs_p95_deg | 2.0843 |
| flat_recall | 0.9616 |
| stall_recall | 0.7083 |
| slope_recall | 0.9793 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7968 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    727,
    0,
    29
  ],
  [
    9,
    68,
    19
  ],
  [
    48,
    9,
    2693
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    571,
    130,
    98
  ],
  [
    632,
    886,
    415
  ],
  [
    206,
    198,
    466
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.216286 |
| test_loss_turn_bundle_base | 0.277089 |
| test_loss_theta_bundle_base | 0.000139 |
| test_loss_transition_focal_raw | 0.835414 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.587079 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 67
- train_seconds: 329.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.3333 | 0.5412 |
| [0.60,0.70) | 36 | 0.5833 | 0.6591 |
| [0.70,0.80) | 44 | 0.6136 | 0.7484 |
| [0.80,0.90) | 68 | 0.1765 | 0.8541 |
| [0.90,1.00) | 3430 | 0.0134 | 0.9964 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1038 | 0.5992 | 0.5089 |
| [0.60,0.70) | 523 | 0.5660 | 0.6470 |
| [0.70,0.80) | 537 | 0.5382 | 0.7519 |
| [0.80,0.90) | 468 | 0.4594 | 0.8532 |
| [0.90,1.00) | 1036 | 0.2481 | 0.9654 |


## 验证集最佳点

```json
{
  "loss_total": 0.5134022313945187,
  "acc_main": 0.9496617050067659,
  "acc_turn": 0.5807848443843031,
  "acc_turn_pure": 0.5925925925925926,
  "acc_turn_transition": 0.5248447204968945,
  "false_turn_straight": 0.5379417879417879,
  "flat_recall": 0.9634703196347032,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9546061415220294,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9634703196347032,
    0.38095238095238093,
    0.9546061415220294
  ],
  "turn_right_recall": 0.7286729857819905,
  "turn_straight_recall": 0.46205821205821207,
  "turn_left_recall": 0.6925566343042071,
  "recall_turn": [
    0.7286729857819905,
    0.46205821205821207,
    0.6925566343042071
  ],
  "cm_turn": [
    [
      615,
      162,
      67
    ],
    [
      607,
      889,
      428
    ],
    [
      149,
      136,
      642
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      633,
      0,
      24
    ],
    [
      0,
      16,
      26
    ],
    [
      125,
      11,
      2860
    ]
  ],
  "main_confidence_mean": 0.9698059761081826,
  "main_confidence_error_mean": 0.779420055429192,
  "main_low_conf_0p60_ratio": 0.005142083897158322,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 19,
      "error_rate": 0.5263157894736842,
      "mean_confidence": 0.5551731755215336
    },
    {
      "bin": "[0.60,0.70)",
      "n": 193,
      "error_rate": 0.41968911917098445,
      "mean_confidence": 0.6173056430568101
    },
    {
      "bin": "[0.70,0.80)",
      "n": 36,
      "error_rate": 0.3611111111111111,
      "mean_confidence": 0.7565509827596882
    },
    {
      "bin": "[0.80,0.90)",
      "n": 59,
      "error_rate": 0.15254237288135594,
      "mean_confidence": 0.8584557754105556
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3388,
      "error_rate": 0.02154663518299882,
      "mean_confidence": 0.9964167875284208
    }
  ],
  "turn_confidence_mean": 0.7522952582594636,
  "turn_confidence_error_mean": 0.6843501674113223,
  "turn_low_conf_0p60_ratio": 0.25899864682002705,
  "turn_low_conf_0p70_ratio": 0.42246278755074423,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 957,
      "error_rate": 0.6050156739811913,
      "mean_confidence": 0.5016580830085526
    },
    {
      "bin": "[0.60,0.70)",
      "n": 604,
      "error_rate": 0.4917218543046358,
      "mean_confidence": 0.6495921984120008
    },
    {
      "bin": "[0.70,0.80)",
      "n": 453,
      "error_rate": 0.4481236203090508,
      "mean_confidence": 0.7475883223283702
    },
    {
      "bin": "[0.80,0.90)",
      "n": 516,
      "error_rate": 0.35658914728682173,
      "mean_confidence": 0.8530949633165905
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1165,
      "error_rate": 0.24549356223175967,
      "mean_confidence": 0.9686145878992041
    }
  ],
  "theta_mae_rad": 0.012445091269910336,
  "theta_mae_deg": 0.7130511403083801,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9556528880372297,
  "theta_flat_mae_deg": 1.2985107898712158,
  "theta_flat_abs_p95_deg": 4.193209171295166,
  "theta_flat_abs_max_deg": 7.4894633293151855,
  "theta_flat_bias_deg": 1.2261855602264404,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.877931833267212,
  "theta_near_flat_abs_p95_deg": 4.240911483764648,
  "theta_near_flat_abs_max_deg": 7.794134140014648,
  "theta_near_flat_bias_deg": 1.7869328260421753,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.5901427268981934,
  "theta_flat_turn_abs_p95_deg": 4.193209171295166,
  "theta_flat_turn_abs_max_deg": 7.4894633293151855,
  "theta_flat_turn_bias_deg": 1.4668450355529785,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7130511403083801,
  "theta_slope_control_abs_p95_deg": 9.288004875183105,
  "theta_slope_control_abs_max_deg": 11.024219512939453,
  "theta_slope_control_bias_deg": 0.38054054975509644,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7130511403083801,
  "theta_all_rmse_deg": 1.113394021987915,
  "theta_all_p95_abs_err_deg": 2.4247939586639404,
  "theta_all_max_abs_err_deg": 7.989462852478027,
  "theta_all_bias_deg": 0.38054054975509644,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.5846643447875977,
  "theta_active_abs_ge_2_rmse_deg": 0.8644759654998779,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.6932094097137451,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.798094749450684,
  "theta_active_abs_ge_2_bias_deg": 0.19509699940681458,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7622964978218079,
  "theta_abs_le_8_rmse_deg": 1.171742558479309,
  "theta_abs_le_8_p95_abs_err_deg": 2.693209171295166,
  "theta_abs_le_8_max_abs_err_deg": 7.989462852478027,
  "theta_abs_le_8_bias_deg": 0.46543967723846436,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7130511403083801,
  "theta_abs_le_10_rmse_deg": 1.113394021987915,
  "theta_abs_le_10_p95_abs_err_deg": 2.4247939586639404,
  "theta_abs_le_10_max_abs_err_deg": 7.989462852478027,
  "theta_abs_le_10_bias_deg": 0.38054054975509644,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4662681221961975,
  "theta_pos_8_10_rmse_deg": 0.6684033274650574,
  "theta_pos_8_10_p95_abs_err_deg": 1.3861242532730103,
  "theta_pos_8_10_max_abs_err_deg": 3.712529420852661,
  "theta_pos_8_10_bias_deg": -0.05710366368293762,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.5450187921524048,
  "theta_neg_10_8_rmse_deg": 0.9547527432441711,
  "theta_neg_10_8_p95_abs_err_deg": 1.5544391870498657,
  "theta_neg_10_8_max_abs_err_deg": 6.564781665802002,
  "theta_neg_10_8_bias_deg": 0.10325346887111664,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5270541906356812,
  "theta_pos_6_8_rmse_deg": 0.8029619455337524,
  "theta_pos_6_8_p95_abs_err_deg": 1.3889926671981812,
  "theta_pos_6_8_max_abs_err_deg": 3.5005042552948,
  "theta_pos_6_8_bias_deg": 0.18620111048221588,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.5779709815979004,
  "theta_neg_8_6_rmse_deg": 0.859693706035614,
  "theta_neg_8_6_p95_abs_err_deg": 1.6185131072998047,
  "theta_neg_8_6_max_abs_err_deg": 5.312164783477783,
  "theta_neg_8_6_bias_deg": 0.10877884179353714,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5870563387870789,
  "theta_neg_4_2_rmse_deg": 0.8367207050323486,
  "theta_neg_4_2_p95_abs_err_deg": 1.5379191637039185,
  "theta_neg_4_2_max_abs_err_deg": 6.798094749450684,
  "theta_neg_4_2_bias_deg": 0.06499093770980835,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5785332918167114,
  "theta_neg_2_0p5_rmse_deg": 0.8068946003913879,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3697763681411743,
  "theta_neg_2_0p5_max_abs_err_deg": 4.605189323425293,
  "theta_neg_2_0p5_bias_deg": 0.49127915501594543,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.2595336437225342,
  "theta_pos_0p5_2_rmse_deg": 1.5797450542449951,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.693209171295166,
  "theta_pos_0p5_2_max_abs_err_deg": 5.080094337463379,
  "theta_pos_0p5_2_bias_deg": 1.24629807472229,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2621946400895977,
  "loss_turn": 1.045559871212878,
  "loss_theta": 0.0003776839295186667,
  "loss_main_bundle_base": 0.2621946400895977,
  "loss_turn_bundle_base": 0.2509343617017279,
  "loss_theta_bundle_base": 0.00027322876445932693,
  "loss_main_bundle": 0.2621946400895977,
  "loss_turn_bundle": 0.2509343617017279,
  "loss_theta_bundle": 0.00027322876445932693,
  "loss_theta_flat": 0.0003891692070203174,
  "loss_theta_near_flat": 0.001728859836177671,
  "loss_theta_error_excess": 0.00014006764472352596,
  "loss_theta_flat_excess": 0.00021383652971122298,
  "loss_theta_near_flat_excess": 0.0012688766854924826,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 5.825195332415054e-05,
  "loss_theta_small_neg": 0.00020787796854383043,
  "loss_theta_small_neg_excess": 4.844623278742669e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4604194763710115,
  "loss_false_turn_straight": 0.36584222685339,
  "loss_transition_focal_raw": 0.7121519581874749,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.812568742722394,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
