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
| acc_main | 0.9520 |
| acc_turn | 0.5333 |
| acc_turn_pure | 0.5425 |
| acc_turn_transition | 0.4933 |
| main_confidence_mean | 0.9783 |
| main_low_conf_0p60_ratio | 0.0144 |
| main_low_conf_0p70_ratio | 0.0244 |
| turn_confidence_mean | 0.7145 |
| turn_low_conf_0p60_ratio | 0.3265 |
| turn_low_conf_0p70_ratio | 0.4911 |
| turn_right_recall | 0.5657 |
| turn_straight_recall | 0.4853 |
| turn_left_recall | 0.6103 |
| theta_mae_deg | 0.8211 |
| theta_abs_le_10_p95_abs_err_deg | 2.2389 |
| theta_neg_10_8_p95_abs_err_deg | 2.0367 |
| theta_pos_8_10_p95_abs_err_deg | 2.9538 |
| theta_abs_le_8_p95_abs_err_deg | 2.1622 |
| theta_neg_8_6_p95_abs_err_deg | 1.9259 |
| theta_pos_6_8_p95_abs_err_deg | 1.8108 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.6014 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.7535 |
| theta_flat_abs_p95_deg | 2.8532 |
| theta_flat_bias_deg | 0.4652 |
| theta_near_flat_abs_p95_deg | 1.5371 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.6163 |
| theta_flat_turn_abs_p95_deg | 1.5282 |
| flat_recall | 0.9259 |
| stall_recall | 0.6979 |
| slope_recall | 0.9680 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7374 |
| downhill_recall | 0.8127 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    700,
    0,
    56
  ],
  [
    10,
    67,
    19
  ],
  [
    51,
    37,
    2662
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    452,
    204,
    143
  ],
  [
    419,
    938,
    576
  ],
  [
    123,
    216,
    531
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.326484 |
| test_loss_turn_bundle_base | 0.228135 |
| test_loss_theta_bundle_base | 0.000282 |
| test_loss_transition_focal_raw | 0.854670 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.760546 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 28
- train_seconds: 197.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 52 | 0.5769 | 0.5498 |
| [0.60,0.70) | 36 | 0.3611 | 0.6537 |
| [0.70,0.80) | 52 | 0.3269 | 0.7587 |
| [0.80,0.90) | 102 | 0.1569 | 0.8606 |
| [0.90,1.00) | 3360 | 0.0289 | 0.9953 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1176 | 0.6037 | 0.5080 |
| [0.60,0.70) | 593 | 0.5228 | 0.6472 |
| [0.70,0.80) | 510 | 0.5471 | 0.7487 |
| [0.80,0.90) | 560 | 0.4054 | 0.8469 |
| [0.90,1.00) | 763 | 0.2031 | 0.9650 |


## 验证集最佳点

```json
{
  "loss_total": 0.4928946471182032,
  "acc_main": 0.9431664411366711,
  "acc_turn": 0.5607577807848444,
  "acc_turn_pure": 0.5742379547689282,
  "acc_turn_transition": 0.4968944099378882,
  "false_turn_straight": 0.5597713097713097,
  "flat_recall": 0.9573820395738204,
  "stall_recall": 0.5,
  "slope_recall": 0.9462616822429907,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9573820395738204,
    0.5,
    0.9462616822429907
  ],
  "turn_right_recall": 0.6729857819905213,
  "turn_straight_recall": 0.4402286902286902,
  "turn_left_recall": 0.7087378640776699,
  "recall_turn": [
    0.6729857819905213,
    0.4402286902286902,
    0.7087378640776699
  ],
  "cm_turn": [
    [
      568,
      165,
      111
    ],
    [
      552,
      847,
      525
    ],
    [
      107,
      163,
      657
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      629,
      0,
      28
    ],
    [
      1,
      21,
      20
    ],
    [
      128,
      33,
      2835
    ]
  ],
  "main_confidence_mean": 0.9762499920490739,
  "main_confidence_error_mean": 0.8548027844839287,
  "main_low_conf_0p60_ratio": 0.007848443843031122,
  "main_low_conf_0p70_ratio": 0.015696887686062245,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 29,
      "error_rate": 0.5172413793103449,
      "mean_confidence": 0.550299339412215
    },
    {
      "bin": "[0.60,0.70)",
      "n": 29,
      "error_rate": 0.4482758620689655,
      "mean_confidence": 0.6524605199703659
    },
    {
      "bin": "[0.70,0.80)",
      "n": 53,
      "error_rate": 0.2641509433962264,
      "mean_confidence": 0.763028378568667
    },
    {
      "bin": "[0.80,0.90)",
      "n": 237,
      "error_rate": 0.38396624472573837,
      "mean_confidence": 0.843666630507317
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3347,
      "error_rate": 0.023005676725425753,
      "mean_confidence": 0.9955106630429817
    }
  ],
  "turn_confidence_mean": 0.7393589519905444,
  "turn_confidence_error_mean": 0.682818695077965,
  "turn_low_conf_0p60_ratio": 0.29336941813261164,
  "turn_low_conf_0p70_ratio": 0.43599458728010826,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1084,
      "error_rate": 0.5922509225092251,
      "mean_confidence": 0.5128784517505905
    },
    {
      "bin": "[0.60,0.70)",
      "n": 527,
      "error_rate": 0.47248576850094876,
      "mean_confidence": 0.6508124107072353
    },
    {
      "bin": "[0.70,0.80)",
      "n": 520,
      "error_rate": 0.5038461538461538,
      "mean_confidence": 0.7502578195742842
    },
    {
      "bin": "[0.80,0.90)",
      "n": 568,
      "error_rate": 0.42077464788732394,
      "mean_confidence": 0.8492623359601325
    },
    {
      "bin": "[0.90,1.00)",
      "n": 996,
      "error_rate": 0.2319277108433735,
      "mean_confidence": 0.9643352133139811
    }
  ],
  "theta_mae_rad": 0.01640377752482891,
  "theta_mae_deg": 0.9398671388626099,
  "uphill_recall": 0.7681940700808625,
  "downhill_recall": 0.7997775305895439,
  "slope_sign_acc": 0.9507254311524774,
  "theta_flat_mae_deg": 1.2510452270507812,
  "theta_flat_abs_p95_deg": 3.1044230461120605,
  "theta_flat_abs_max_deg": 10.670374870300293,
  "theta_flat_bias_deg": 0.9987920522689819,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.8525632619857788,
  "theta_near_flat_abs_p95_deg": 4.238441467285156,
  "theta_near_flat_abs_max_deg": 10.670374870300293,
  "theta_near_flat_bias_deg": 1.7884396314620972,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.8967114686965942,
  "theta_flat_turn_abs_p95_deg": 7.257533073425293,
  "theta_flat_turn_abs_max_deg": 10.670374870300293,
  "theta_flat_turn_bias_deg": 1.809004545211792,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9398671388626099,
  "theta_slope_control_abs_p95_deg": 9.094107627868652,
  "theta_slope_control_abs_max_deg": 12.189894676208496,
  "theta_slope_control_bias_deg": 0.12412240356206894,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9398670792579651,
  "theta_all_rmse_deg": 1.3679308891296387,
  "theta_all_p95_abs_err_deg": 2.6043906211853027,
  "theta_all_max_abs_err_deg": 11.170373916625977,
  "theta_all_bias_deg": 0.12412241101264954,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8716280460357666,
  "theta_active_abs_ge_2_rmse_deg": 1.2262133359909058,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.517672538757324,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.347411632537842,
  "theta_active_abs_ge_2_bias_deg": -0.06768597662448883,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9853910803794861,
  "theta_abs_le_8_rmse_deg": 1.4265369176864624,
  "theta_abs_le_8_p95_abs_err_deg": 2.650343179702759,
  "theta_abs_le_8_max_abs_err_deg": 11.170373916625977,
  "theta_abs_le_8_bias_deg": 0.16572973132133484,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9398670792579651,
  "theta_abs_le_10_rmse_deg": 1.3679308891296387,
  "theta_abs_le_10_p95_abs_err_deg": 2.6043906211853027,
  "theta_abs_le_10_max_abs_err_deg": 11.170373916625977,
  "theta_abs_le_10_bias_deg": 0.12412241101264954,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7593727707862854,
  "theta_pos_8_10_rmse_deg": 1.0907686948776245,
  "theta_pos_8_10_p95_abs_err_deg": 2.032839298248291,
  "theta_pos_8_10_max_abs_err_deg": 6.217947959899902,
  "theta_pos_8_10_bias_deg": -0.5188136100769043,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7360690236091614,
  "theta_neg_10_8_rmse_deg": 1.0820157527923584,
  "theta_neg_10_8_p95_abs_err_deg": 2.2448456287384033,
  "theta_neg_10_8_max_abs_err_deg": 4.938076019287109,
  "theta_neg_10_8_bias_deg": 0.42409372329711914,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.811163604259491,
  "theta_pos_6_8_rmse_deg": 1.0860435962677002,
  "theta_pos_6_8_p95_abs_err_deg": 1.9153244495391846,
  "theta_pos_6_8_max_abs_err_deg": 4.010193347930908,
  "theta_pos_6_8_bias_deg": -0.40860700607299805,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8750331997871399,
  "theta_neg_8_6_rmse_deg": 1.192059874534607,
  "theta_neg_8_6_p95_abs_err_deg": 2.488291025161743,
  "theta_neg_8_6_max_abs_err_deg": 5.639864444732666,
  "theta_neg_8_6_bias_deg": -0.03788406774401665,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9332988262176514,
  "theta_neg_4_2_rmse_deg": 1.286067247390747,
  "theta_neg_4_2_p95_abs_err_deg": 2.6677799224853516,
  "theta_neg_4_2_max_abs_err_deg": 5.743505001068115,
  "theta_neg_4_2_bias_deg": 0.22495368123054504,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6779612302780151,
  "theta_neg_2_0p5_rmse_deg": 0.90146803855896,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5711381435394287,
  "theta_neg_2_0p5_max_abs_err_deg": 4.534961700439453,
  "theta_neg_2_0p5_bias_deg": 0.47905659675598145,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9530375599861145,
  "theta_pos_0p5_2_rmse_deg": 1.1967664957046509,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.7145119905471802,
  "theta_pos_0p5_2_max_abs_err_deg": 4.555881023406982,
  "theta_pos_0p5_2_bias_deg": 0.28666406869888306,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2708064817366,
  "loss_turn": 1.1085470390255299,
  "loss_theta": 0.0005703053156610866,
  "loss_main_bundle_base": 0.2708064817366,
  "loss_turn_bundle_base": 0.2217094115217258,
  "loss_theta_bundle_base": 0.00037875441262178394,
  "loss_main_bundle": 0.2708064817366,
  "loss_turn_bundle": 0.2217094115217258,
  "loss_theta_bundle": 0.00037875441262178394,
  "loss_theta_flat": 0.0003267363137059879,
  "loss_theta_near_flat": 0.0019012614549043134,
  "loss_theta_error_excess": 0.00022204807206184298,
  "loss_theta_flat_excess": 0.00013421886398796312,
  "loss_theta_near_flat_excess": 0.0014311200189901987,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014775729419097067,
  "loss_theta_small_neg": 0.0004990408342800775,
  "loss_theta_small_neg_excess": 0.00015631314569463384,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4833780550343742,
  "loss_false_turn_straight": 0.3674931936318884,
  "loss_transition_focal_raw": 0.7140592631370999,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.5479652476538583,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
