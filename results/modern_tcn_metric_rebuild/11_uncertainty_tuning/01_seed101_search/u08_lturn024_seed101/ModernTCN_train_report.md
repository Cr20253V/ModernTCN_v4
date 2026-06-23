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
| acc_main | 0.9664 |
| acc_turn | 0.5830 |
| acc_turn_pure | 0.6001 |
| acc_turn_transition | 0.5082 |
| main_confidence_mean | 0.9897 |
| main_low_conf_0p60_ratio | 0.0050 |
| main_low_conf_0p70_ratio | 0.0133 |
| turn_confidence_mean | 0.8457 |
| turn_low_conf_0p60_ratio | 0.1288 |
| turn_low_conf_0p70_ratio | 0.2271 |
| turn_right_recall | 0.6383 |
| turn_straight_recall | 0.5763 |
| turn_left_recall | 0.5471 |
| theta_mae_deg | 0.6103 |
| theta_abs_le_10_p95_abs_err_deg | 1.6454 |
| theta_neg_10_8_p95_abs_err_deg | 1.1572 |
| theta_pos_8_10_p95_abs_err_deg | 2.3194 |
| theta_abs_le_8_p95_abs_err_deg | 1.6160 |
| theta_neg_8_6_p95_abs_err_deg | 1.4466 |
| theta_pos_6_8_p95_abs_err_deg | 1.5005 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6597 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4861 |
| theta_flat_abs_p95_deg | 2.6075 |
| theta_flat_bias_deg | 0.3013 |
| theta_near_flat_abs_p95_deg | 1.7437 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3578 |
| theta_flat_turn_abs_p95_deg | 1.3882 |
| flat_recall | 0.9709 |
| stall_recall | 0.6979 |
| slope_recall | 0.9745 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7511 |
| downhill_recall | 0.7900 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    734,
    0,
    22
  ],
  [
    11,
    67,
    18
  ],
  [
    61,
    9,
    2680
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    510,
    179,
    110
  ],
  [
    434,
    1114,
    385
  ],
  [
    196,
    198,
    476
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.339754 |
| test_loss_turn_bundle_base | 0.422459 |
| test_loss_theta_bundle_base | 0.000144 |
| test_loss_transition_focal_raw | 1.559737 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.738365 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 383.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 18 | 0.4444 | 0.5472 |
| [0.60,0.70) | 30 | 0.6333 | 0.6505 |
| [0.70,0.80) | 25 | 0.3600 | 0.7550 |
| [0.80,0.90) | 38 | 0.4211 | 0.8523 |
| [0.90,1.00) | 3491 | 0.0198 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 464 | 0.6185 | 0.5091 |
| [0.60,0.70) | 354 | 0.6045 | 0.6527 |
| [0.70,0.80) | 384 | 0.4896 | 0.7505 |
| [0.80,0.90) | 448 | 0.4799 | 0.8540 |
| [0.90,1.00) | 1952 | 0.3064 | 0.9776 |


## 验证集最佳点

```json
{
  "loss_total": 0.7738901963091993,
  "acc_main": 0.9437077131258458,
  "acc_turn": 0.635723951285521,
  "acc_turn_pure": 0.6463454605047525,
  "acc_turn_transition": 0.5854037267080745,
  "false_turn_straight": 0.420997920997921,
  "flat_recall": 0.9406392694063926,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9526034712950601,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9406392694063926,
    0.35714285714285715,
    0.9526034712950601
  ],
  "turn_right_recall": 0.7037914691943128,
  "turn_straight_recall": 0.579002079002079,
  "turn_left_recall": 0.6914778856526429,
  "recall_turn": [
    0.7037914691943128,
    0.579002079002079,
    0.6914778856526429
  ],
  "cm_turn": [
    [
      594,
      202,
      48
    ],
    [
      416,
      1114,
      394
    ],
    [
      114,
      172,
      641
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
      0,
      15,
      27
    ],
    [
      132,
      10,
      2854
    ]
  ],
  "main_confidence_mean": 0.9697363639718314,
  "main_confidence_error_mean": 0.772475424082909,
  "main_low_conf_0p60_ratio": 0.05196211096075778,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 192,
      "error_rate": 0.4427083333333333,
      "mean_confidence": 0.5438921270656437
    },
    {
      "bin": "[0.60,0.70)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.6534194362144602
    },
    {
      "bin": "[0.70,0.80)",
      "n": 22,
      "error_rate": 0.3181818181818182,
      "mean_confidence": 0.7512174416324503
    },
    {
      "bin": "[0.80,0.90)",
      "n": 41,
      "error_rate": 0.4146341463414634,
      "mean_confidence": 0.857007251694427
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3421,
      "error_rate": 0.026308097047646885,
      "mean_confidence": 0.9981495253305621
    }
  ],
  "turn_confidence_mean": 0.8634771590986616,
  "turn_confidence_error_mean": 0.7900567753241787,
  "turn_low_conf_0p60_ratio": 0.11880920162381597,
  "turn_low_conf_0p70_ratio": 0.19512855209742896,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 439,
      "error_rate": 0.6400911161731208,
      "mean_confidence": 0.4900185220022675
    },
    {
      "bin": "[0.60,0.70)",
      "n": 282,
      "error_rate": 0.5035460992907801,
      "mean_confidence": 0.649270796320343
    },
    {
      "bin": "[0.70,0.80)",
      "n": 286,
      "error_rate": 0.5384615384615384,
      "mean_confidence": 0.7529083199711273
    },
    {
      "bin": "[0.80,0.90)",
      "n": 461,
      "error_rate": 0.4837310195227766,
      "mean_confidence": 0.8546617592149747
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2227,
      "error_rate": 0.24517287831162998,
      "mean_confidence": 0.9802446145659528
    }
  ],
  "theta_mae_rad": 0.012854119762778282,
  "theta_mae_deg": 0.7364867925643921,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.8075639599555061,
  "slope_sign_acc": 0.9742677251574049,
  "theta_flat_mae_deg": 0.9554251432418823,
  "theta_flat_abs_p95_deg": 3.6688456535339355,
  "theta_flat_abs_max_deg": 6.625912666320801,
  "theta_flat_bias_deg": 0.6144497990608215,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.2788779735565186,
  "theta_near_flat_abs_p95_deg": 3.732668399810791,
  "theta_near_flat_abs_max_deg": 6.625912666320801,
  "theta_near_flat_bias_deg": 0.852855384349823,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9161973595619202,
  "theta_flat_turn_abs_p95_deg": 3.6688337326049805,
  "theta_flat_turn_abs_max_deg": 6.625912666320801,
  "theta_flat_turn_bias_deg": 0.30215388536453247,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7364867925643921,
  "theta_slope_control_abs_p95_deg": 9.441045761108398,
  "theta_slope_control_abs_max_deg": 11.53140640258789,
  "theta_slope_control_bias_deg": 0.2332683503627777,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7364867925643921,
  "theta_all_rmse_deg": 1.136405110359192,
  "theta_all_p95_abs_err_deg": 2.989122152328491,
  "theta_all_max_abs_err_deg": 7.02564811706543,
  "theta_all_bias_deg": 0.23326832056045532,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6884752511978149,
  "theta_active_abs_ge_2_rmse_deg": 1.0601297616958618,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.429612159729004,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.02564811706543,
  "theta_active_abs_ge_2_bias_deg": 0.14967812597751617,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7655760645866394,
  "theta_abs_le_8_rmse_deg": 1.1740238666534424,
  "theta_abs_le_8_p95_abs_err_deg": 3.084829330444336,
  "theta_abs_le_8_max_abs_err_deg": 7.02564811706543,
  "theta_abs_le_8_bias_deg": 0.29391831159591675,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7364867925643921,
  "theta_abs_le_10_rmse_deg": 1.136405110359192,
  "theta_abs_le_10_p95_abs_err_deg": 2.989122152328491,
  "theta_abs_le_10_max_abs_err_deg": 7.02564811706543,
  "theta_abs_le_10_bias_deg": 0.23326832056045532,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5293095707893372,
  "theta_pos_8_10_rmse_deg": 0.7154492139816284,
  "theta_pos_8_10_p95_abs_err_deg": 1.3770945072174072,
  "theta_pos_8_10_max_abs_err_deg": 3.5272622108459473,
  "theta_pos_8_10_bias_deg": -0.12962917983531952,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6996941566467285,
  "theta_neg_10_8_rmse_deg": 1.1596484184265137,
  "theta_neg_10_8_p95_abs_err_deg": 2.334089517593384,
  "theta_neg_10_8_max_abs_err_deg": 6.209161281585693,
  "theta_neg_10_8_bias_deg": 0.08630423247814178,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.49041473865509033,
  "theta_pos_6_8_rmse_deg": 0.7734767198562622,
  "theta_pos_6_8_p95_abs_err_deg": 1.655380129814148,
  "theta_pos_6_8_max_abs_err_deg": 3.648224115371704,
  "theta_pos_6_8_bias_deg": 0.12620685994625092,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7463863492012024,
  "theta_neg_8_6_rmse_deg": 1.1068484783172607,
  "theta_neg_8_6_p95_abs_err_deg": 2.409442901611328,
  "theta_neg_8_6_max_abs_err_deg": 5.74945592880249,
  "theta_neg_8_6_bias_deg": -0.004540873691439629,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6652306914329529,
  "theta_neg_4_2_rmse_deg": 0.9624156355857849,
  "theta_neg_4_2_p95_abs_err_deg": 1.8913729190826416,
  "theta_neg_4_2_max_abs_err_deg": 6.225461483001709,
  "theta_neg_4_2_bias_deg": -0.029337521642446518,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.45791032910346985,
  "theta_neg_2_0p5_rmse_deg": 0.6986054182052612,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0306367874145508,
  "theta_neg_2_0p5_max_abs_err_deg": 4.5563740730285645,
  "theta_neg_2_0p5_bias_deg": 0.09240452945232391,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1835461854934692,
  "theta_pos_0p5_2_rmse_deg": 1.4261404275894165,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.1688337326049805,
  "theta_pos_0p5_2_max_abs_err_deg": 4.761659622192383,
  "theta_pos_0p5_2_bias_deg": 1.063742756843567,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.4083266409388737,
  "loss_turn": 1.5221039194215458,
  "loss_theta": 0.00039343507193263333,
  "loss_main_bundle_base": 0.4083266409388737,
  "loss_turn_bundle_base": 0.3653049278646425,
  "loss_theta_bundle_base": 0.00025863569450069405,
  "loss_main_bundle": 0.4083266409388737,
  "loss_turn_bundle": 0.3653049278646425,
  "loss_theta_bundle": 0.00025863569450069405,
  "loss_theta_flat": 0.00019529191011510014,
  "loss_theta_near_flat": 0.0010612024257403165,
  "loss_theta_error_excess": 0.00014205087841606884,
  "loss_theta_flat_excess": 9.859291784626668e-05,
  "loss_theta_near_flat_excess": 0.0007436706204690715,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00011708831098888457,
  "loss_theta_small_neg": 0.00027582674212905,
  "loss_theta_small_neg_excess": 7.634880026137325e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.36831663707435053,
  "loss_false_turn_straight": 0.31558804456371414,
  "loss_transition_focal_raw": 1.3687405391700858,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.543234527271335,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
