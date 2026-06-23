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
| acc_main | 0.9645 |
| acc_turn | 0.5875 |
| acc_turn_pure | 0.6049 |
| acc_turn_transition | 0.5112 |
| main_confidence_mean | 0.9907 |
| main_low_conf_0p60_ratio | 0.0056 |
| main_low_conf_0p70_ratio | 0.0105 |
| turn_confidence_mean | 0.8421 |
| turn_low_conf_0p60_ratio | 0.1269 |
| turn_low_conf_0p70_ratio | 0.2426 |
| turn_right_recall | 0.6320 |
| turn_straight_recall | 0.5877 |
| turn_left_recall | 0.5460 |
| theta_mae_deg | 0.5777 |
| theta_abs_le_10_p95_abs_err_deg | 1.6410 |
| theta_neg_10_8_p95_abs_err_deg | 1.0400 |
| theta_pos_8_10_p95_abs_err_deg | 2.7195 |
| theta_abs_le_8_p95_abs_err_deg | 1.5491 |
| theta_neg_8_6_p95_abs_err_deg | 1.4276 |
| theta_pos_6_8_p95_abs_err_deg | 1.4008 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7129 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7023 |
| theta_flat_abs_p95_deg | 2.6118 |
| theta_flat_bias_deg | -0.5320 |
| theta_near_flat_abs_p95_deg | 1.9358 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.5564 |
| theta_flat_turn_abs_p95_deg | 1.8227 |
| flat_recall | 0.9418 |
| stall_recall | 0.6979 |
| slope_recall | 0.9800 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7575 |
| downhill_recall | 0.8042 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    712,
    1,
    43
  ],
  [
    10,
    67,
    19
  ],
  [
    46,
    9,
    2695
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    505,
    182,
    112
  ],
  [
    409,
    1136,
    388
  ],
  [
    175,
    220,
    475
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.376219 |
| test_loss_turn_bundle_base | 0.342862 |
| test_loss_theta_bundle_base | 0.000150 |
| test_loss_transition_focal_raw | 1.535291 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.921339 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 82
- train_seconds: 379.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 20 | 0.6000 | 0.5593 |
| [0.60,0.70) | 18 | 0.3889 | 0.6494 |
| [0.70,0.80) | 28 | 0.2500 | 0.7439 |
| [0.80,0.90) | 27 | 0.3333 | 0.8463 |
| [0.90,1.00) | 3509 | 0.0265 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 457 | 0.6171 | 0.5310 |
| [0.60,0.70) | 417 | 0.5492 | 0.6463 |
| [0.70,0.80) | 361 | 0.5346 | 0.7505 |
| [0.80,0.90) | 476 | 0.4559 | 0.8521 |
| [0.90,1.00) | 1891 | 0.2988 | 0.9755 |


## 验证集最佳点

```json
{
  "loss_total": 0.6665863103731076,
  "acc_main": 0.9423545331529093,
  "acc_turn": 0.63382949932341,
  "acc_turn_pure": 0.6443788921665028,
  "acc_turn_transition": 0.5838509316770186,
  "false_turn_straight": 0.4230769230769231,
  "flat_recall": 0.939117199391172,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9512683578104139,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.939117199391172,
    0.35714285714285715,
    0.9512683578104139
  ],
  "turn_right_recall": 0.693127962085308,
  "turn_straight_recall": 0.5769230769230769,
  "turn_left_recall": 0.697950377562028,
  "recall_turn": [
    0.693127962085308,
    0.5769230769230769,
    0.697950377562028
  ],
  "cm_turn": [
    [
      585,
      224,
      35
    ],
    [
      423,
      1110,
      391
    ],
    [
      108,
      172,
      647
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
      15,
      27
    ],
    [
      130,
      16,
      2850
    ]
  ],
  "main_confidence_mean": 0.9722317748999898,
  "main_confidence_error_mean": 0.7934338616108055,
  "main_low_conf_0p60_ratio": 0.04925575101488498,
  "main_low_conf_0p70_ratio": 0.0530446549391069,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 182,
      "error_rate": 0.4725274725274725,
      "mean_confidence": 0.5615472226305445
    },
    {
      "bin": "[0.60,0.70)",
      "n": 14,
      "error_rate": 0.35714285714285715,
      "mean_confidence": 0.6499082440389682
    },
    {
      "bin": "[0.70,0.80)",
      "n": 24,
      "error_rate": 0.375,
      "mean_confidence": 0.7511235221593916
    },
    {
      "bin": "[0.80,0.90)",
      "n": 31,
      "error_rate": 0.22580645161290322,
      "mean_confidence": 0.8561520450067917
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3444,
      "error_rate": 0.03077816492450639,
      "mean_confidence": 0.9978305517982352
    }
  ],
  "turn_confidence_mean": 0.8550100483238101,
  "turn_confidence_error_mean": 0.7859553984756793,
  "turn_low_conf_0p60_ratio": 0.12882273342354533,
  "turn_low_conf_0p70_ratio": 0.21326116373477672,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 476,
      "error_rate": 0.6176470588235294,
      "mean_confidence": 0.49414347490511956
    },
    {
      "bin": "[0.60,0.70)",
      "n": 312,
      "error_rate": 0.5160256410256411,
      "mean_confidence": 0.6538070641172485
    },
    {
      "bin": "[0.70,0.80)",
      "n": 321,
      "error_rate": 0.4423676012461059,
      "mean_confidence": 0.7515900545835842
    },
    {
      "bin": "[0.80,0.90)",
      "n": 437,
      "error_rate": 0.4988558352402746,
      "mean_confidence": 0.8545185144788826
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2149,
      "error_rate": 0.25034899953466727,
      "mean_confidence": 0.9797008060253407
    }
  ],
  "theta_mae_rad": 0.013850669376552105,
  "theta_mae_deg": 0.7935848832130432,
  "uphill_recall": 0.7735849056603774,
  "downhill_recall": 0.8092324805339266,
  "slope_sign_acc": 0.9756364631809472,
  "theta_flat_mae_deg": 1.1953386068344116,
  "theta_flat_abs_p95_deg": 4.0473713874816895,
  "theta_flat_abs_max_deg": 7.5938720703125,
  "theta_flat_bias_deg": 0.09841948002576828,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.472157597541809,
  "theta_near_flat_abs_p95_deg": 4.054362773895264,
  "theta_near_flat_abs_max_deg": 7.5938720703125,
  "theta_near_flat_bias_deg": 0.5286272168159485,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.044565200805664,
  "theta_flat_turn_abs_p95_deg": 4.0473713874816895,
  "theta_flat_turn_abs_max_deg": 7.5938720703125,
  "theta_flat_turn_bias_deg": 0.03250660002231598,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7935848832130432,
  "theta_slope_control_abs_p95_deg": 9.179194450378418,
  "theta_slope_control_abs_max_deg": 11.968886375427246,
  "theta_slope_control_bias_deg": -0.1438753604888916,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.793584942817688,
  "theta_all_rmse_deg": 1.1677557229995728,
  "theta_all_p95_abs_err_deg": 2.59759259223938,
  "theta_all_max_abs_err_deg": 7.0938720703125,
  "theta_all_bias_deg": -0.1438753455877304,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7054833769798279,
  "theta_active_abs_ge_2_rmse_deg": 1.0236057043075562,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1400997638702393,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.568492889404297,
  "theta_active_abs_ge_2_bias_deg": -0.19700877368450165,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8393924832344055,
  "theta_abs_le_8_rmse_deg": 1.213761568069458,
  "theta_abs_le_8_p95_abs_err_deg": 2.7360312938690186,
  "theta_abs_le_8_max_abs_err_deg": 7.0938720703125,
  "theta_abs_le_8_bias_deg": -0.15330974757671356,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.793584942817688,
  "theta_abs_le_10_rmse_deg": 1.1677557229995728,
  "theta_abs_le_10_p95_abs_err_deg": 2.59759259223938,
  "theta_abs_le_10_max_abs_err_deg": 7.0938720703125,
  "theta_abs_le_10_bias_deg": -0.1438753455877304,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5733662247657776,
  "theta_pos_8_10_rmse_deg": 0.7994247078895569,
  "theta_pos_8_10_p95_abs_err_deg": 1.504830002784729,
  "theta_pos_8_10_max_abs_err_deg": 4.246951103210449,
  "theta_pos_8_10_bias_deg": -0.3482200801372528,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.627785325050354,
  "theta_neg_10_8_rmse_deg": 1.0809077024459839,
  "theta_neg_10_8_p95_abs_err_deg": 1.8652851581573486,
  "theta_neg_10_8_max_abs_err_deg": 6.568492889404297,
  "theta_neg_10_8_bias_deg": 0.1442902386188507,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5783030390739441,
  "theta_pos_6_8_rmse_deg": 0.8215221166610718,
  "theta_pos_6_8_p95_abs_err_deg": 1.5831897258758545,
  "theta_pos_6_8_max_abs_err_deg": 3.2771825790405273,
  "theta_pos_6_8_bias_deg": -0.2921745777130127,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7875425815582275,
  "theta_neg_8_6_rmse_deg": 1.1321005821228027,
  "theta_neg_8_6_p95_abs_err_deg": 2.2581164836883545,
  "theta_neg_8_6_max_abs_err_deg": 5.736144065856934,
  "theta_neg_8_6_bias_deg": -0.2115747183561325,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8082501888275146,
  "theta_neg_4_2_rmse_deg": 1.0546685457229614,
  "theta_neg_4_2_p95_abs_err_deg": 2.106919527053833,
  "theta_neg_4_2_max_abs_err_deg": 4.5235595703125,
  "theta_neg_4_2_bias_deg": -0.5132243633270264,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.792646586894989,
  "theta_neg_2_0p5_rmse_deg": 0.9968700408935547,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.025381565093994,
  "theta_neg_2_0p5_max_abs_err_deg": 4.191751956939697,
  "theta_neg_2_0p5_bias_deg": -0.6968851685523987,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.302223801612854,
  "theta_pos_0p5_2_rmse_deg": 1.5862716436386108,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5473713874816895,
  "theta_pos_0p5_2_max_abs_err_deg": 3.706416368484497,
  "theta_pos_0p5_2_bias_deg": 0.4228910207748413,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.37230845660737466,
  "loss_turn": 1.469950965099309,
  "loss_theta": 0.0004153346986269152,
  "loss_main_bundle_base": 0.37230845660737466,
  "loss_turn_bundle_base": 0.2939901971768623,
  "loss_theta_bundle_base": 0.0002876504005927905,
  "loss_main_bundle": 0.37230845660737466,
  "loss_turn_bundle": 0.2939901971768623,
  "loss_theta_bundle": 0.0002876504005927905,
  "loss_theta_flat": 0.0003577538152305341,
  "loss_theta_near_flat": 0.0013974037832367526,
  "loss_theta_error_excess": 0.00014163053863749906,
  "loss_theta_flat_excess": 0.00016729831907214148,
  "loss_theta_near_flat_excess": 0.0009996922673463457,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.204327419944642e-05,
  "loss_theta_small_neg": 0.00033480405967546494,
  "loss_theta_small_neg_excess": 7.383019021612684e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3691973945204073,
  "loss_false_turn_straight": 0.3207627517847957,
  "loss_transition_focal_raw": 1.2614433773154334,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.300244423728611,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
