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
  "lambda_theta": 0.6,
  "lambda_theta_flat": 0.12,
  "theta_flat_loss_mode": "near_zero",
  "theta_flat_zero_tol_deg": 0.3,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 0.05,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.1,
  "lambda_theta_active_excess": 0.05,
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
  "theta_neg_weight": 1.1,
  "theta_pos_weight": 1.35,
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
  "select_theta_flat_peak_weight": 0.6,
  "select_theta_flat_peak_target_deg": 5.2,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.5,
  "select_theta_edge_p95_target_deg": 1.1,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9586 |
| acc_turn | 0.5919 |
| acc_turn_pure | 0.6141 |
| acc_turn_transition | 0.4948 |
| main_confidence_mean | 0.9876 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8456 |
| turn_low_conf_0p60_ratio | 0.1369 |
| turn_low_conf_0p70_ratio | 0.2296 |
| turn_right_recall | 0.6108 |
| turn_straight_recall | 0.5913 |
| turn_left_recall | 0.5759 |
| theta_mae_deg | 0.6111 |
| theta_abs_le_10_p95_abs_err_deg | 1.6449 |
| theta_neg_10_8_p95_abs_err_deg | 1.4932 |
| theta_pos_8_10_p95_abs_err_deg | 2.4949 |
| theta_abs_le_8_p95_abs_err_deg | 1.5611 |
| theta_neg_8_6_p95_abs_err_deg | 1.5192 |
| theta_pos_6_8_p95_abs_err_deg | 1.4883 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5059 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4363 |
| theta_flat_abs_p95_deg | 2.3913 |
| theta_flat_bias_deg | -0.1901 |
| theta_near_flat_abs_p95_deg | 1.5253 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0933 |
| theta_flat_turn_abs_p95_deg | 1.4780 |
| flat_recall | 0.9497 |
| stall_recall | 0.6667 |
| slope_recall | 0.9713 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7523 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    718,
    1,
    37
  ],
  [
    9,
    64,
    23
  ],
  [
    66,
    13,
    2671
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    488,
    188,
    123
  ],
  [
    360,
    1143,
    430
  ],
  [
    169,
    200,
    501
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.359710 |
| test_loss_turn_bundle_base | 0.359127 |
| test_loss_theta_bundle_base | 0.000172 |
| test_loss_transition_focal_raw | 1.640350 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.821404 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 75
- train_seconds: 347.3

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.4815 | 0.5431 |
| [0.60,0.70) | 22 | 0.5909 | 0.6479 |
| [0.70,0.80) | 41 | 0.5610 | 0.7554 |
| [0.80,0.90) | 47 | 0.4255 | 0.8541 |
| [0.90,1.00) | 3465 | 0.0231 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 493 | 0.5822 | 0.5197 |
| [0.60,0.70) | 334 | 0.5569 | 0.6485 |
| [0.70,0.80) | 376 | 0.5293 | 0.7521 |
| [0.80,0.90) | 442 | 0.4548 | 0.8534 |
| [0.90,1.00) | 1957 | 0.3051 | 0.9775 |

## seed42 进入三 seed 判定

- pass: `0`
- acc_turn_transition >= 0.7500 未满足，实际 0.4948

## 验证集最佳点

```json
{
  "loss_total": 0.6467028513167643,
  "acc_main": 0.9447902571041948,
  "acc_turn": 0.6327469553450609,
  "acc_turn_pure": 0.644706653556211,
  "acc_turn_transition": 0.5760869565217391,
  "false_turn_straight": 0.4303534303534304,
  "flat_recall": 0.958904109589041,
  "stall_recall": 0.42857142857142855,
  "slope_recall": 0.9489319092122831,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.047619047619047616,
  "recall_main": [
    0.958904109589041,
    0.42857142857142855,
    0.9489319092122831
  ],
  "turn_right_recall": 0.6504739336492891,
  "turn_straight_recall": 0.5696465696465697,
  "turn_left_recall": 0.7475728155339806,
  "recall_turn": [
    0.6504739336492891,
    0.5696465696465697,
    0.7475728155339806
  ],
  "cm_turn": [
    [
      549,
      203,
      92
    ],
    [
      354,
      1096,
      474
    ],
    [
      64,
      170,
      693
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      630,
      0,
      27
    ],
    [
      2,
      18,
      22
    ],
    [
      140,
      13,
      2843
    ]
  ],
  "main_confidence_mean": 0.9697838354662576,
  "main_confidence_error_mean": 0.766705238214046,
  "main_low_conf_0p60_ratio": 0.0516914749661705,
  "main_low_conf_0p70_ratio": 0.05629228687415426,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 191,
      "error_rate": 0.4607329842931937,
      "mean_confidence": 0.5434983313828963
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.29411764705882354,
      "mean_confidence": 0.6562892044030235
    },
    {
      "bin": "[0.70,0.80)",
      "n": 31,
      "error_rate": 0.3548387096774194,
      "mean_confidence": 0.7590077584697016
    },
    {
      "bin": "[0.80,0.90)",
      "n": 42,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.8614871035354151
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3414,
      "error_rate": 0.025190392501464556,
      "mean_confidence": 0.9984400923895105
    }
  ],
  "turn_confidence_mean": 0.8547629862252023,
  "turn_confidence_error_mean": 0.7744514716084019,
  "turn_low_conf_0p60_ratio": 0.13667117726657646,
  "turn_low_conf_0p70_ratio": 0.21190798376184034,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 505,
      "error_rate": 0.6376237623762376,
      "mean_confidence": 0.49567379293987823
    },
    {
      "bin": "[0.60,0.70)",
      "n": 278,
      "error_rate": 0.5935251798561151,
      "mean_confidence": 0.6514572732588644
    },
    {
      "bin": "[0.70,0.80)",
      "n": 311,
      "error_rate": 0.5144694533762058,
      "mean_confidence": 0.7553828650659682
    },
    {
      "bin": "[0.80,0.90)",
      "n": 445,
      "error_rate": 0.44719101123595506,
      "mean_confidence": 0.8476352161724963
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2156,
      "error_rate": 0.237012987012987,
      "mean_confidence": 0.9808938332417638
    }
  ],
  "theta_mae_rad": 0.012680008076131344,
  "theta_mae_deg": 0.7265108823776245,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.7947719688542826,
  "slope_sign_acc": 0.970161511086778,
  "theta_flat_mae_deg": 0.9987037181854248,
  "theta_flat_abs_p95_deg": 3.4118292331695557,
  "theta_flat_abs_max_deg": 7.697288990020752,
  "theta_flat_bias_deg": 0.3667108714580536,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.387885332107544,
  "theta_near_flat_abs_p95_deg": 3.6852269172668457,
  "theta_near_flat_abs_max_deg": 7.697288990020752,
  "theta_near_flat_bias_deg": 0.6800330281257629,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1331499814987183,
  "theta_flat_turn_abs_p95_deg": 3.90324330329895,
  "theta_flat_turn_abs_max_deg": 7.697288990020752,
  "theta_flat_turn_bias_deg": 0.19838586449623108,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7265108823776245,
  "theta_slope_control_abs_p95_deg": 9.43956470489502,
  "theta_slope_control_abs_max_deg": 12.018728256225586,
  "theta_slope_control_bias_deg": 0.12531182169914246,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7265108227729797,
  "theta_all_rmse_deg": 1.1239992380142212,
  "theta_all_p95_abs_err_deg": 2.207307815551758,
  "theta_all_max_abs_err_deg": 8.197288513183594,
  "theta_all_bias_deg": 0.12531180679798126,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6668210625648499,
  "theta_active_abs_ge_2_rmse_deg": 1.030180811882019,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.9846631288528442,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.766404628753662,
  "theta_active_abs_ge_2_bias_deg": 0.07237483561038971,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7623545527458191,
  "theta_abs_le_8_rmse_deg": 1.1406314373016357,
  "theta_abs_le_8_p95_abs_err_deg": 2.3411941528320312,
  "theta_abs_le_8_max_abs_err_deg": 8.197288513183594,
  "theta_abs_le_8_bias_deg": 0.11443132907152176,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7265108227729797,
  "theta_abs_le_10_rmse_deg": 1.1239992380142212,
  "theta_abs_le_10_p95_abs_err_deg": 2.207307815551758,
  "theta_abs_le_10_max_abs_err_deg": 8.197288513183594,
  "theta_abs_le_10_bias_deg": 0.12531180679798126,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4385800361633301,
  "theta_pos_8_10_rmse_deg": 0.7466396689414978,
  "theta_pos_8_10_p95_abs_err_deg": 1.585632562637329,
  "theta_pos_8_10_max_abs_err_deg": 4.683372974395752,
  "theta_pos_8_10_bias_deg": 0.07030072063207626,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7143878936767578,
  "theta_neg_10_8_rmse_deg": 1.2887755632400513,
  "theta_neg_10_8_p95_abs_err_deg": 1.9646100997924805,
  "theta_neg_10_8_max_abs_err_deg": 7.766404628753662,
  "theta_neg_10_8_bias_deg": 0.2738679051399231,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5883160829544067,
  "theta_pos_6_8_rmse_deg": 0.8993887305259705,
  "theta_pos_6_8_p95_abs_err_deg": 1.7598600387573242,
  "theta_pos_6_8_max_abs_err_deg": 4.24772834777832,
  "theta_pos_6_8_bias_deg": 0.09448818862438202,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6982920169830322,
  "theta_neg_8_6_rmse_deg": 1.0622801780700684,
  "theta_neg_8_6_p95_abs_err_deg": 1.9134939908981323,
  "theta_neg_8_6_max_abs_err_deg": 7.099449157714844,
  "theta_neg_8_6_bias_deg": 0.22364066541194916,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6567471027374268,
  "theta_neg_4_2_rmse_deg": 0.9744074940681458,
  "theta_neg_4_2_p95_abs_err_deg": 1.771499514579773,
  "theta_neg_4_2_max_abs_err_deg": 6.299619197845459,
  "theta_neg_4_2_bias_deg": -0.09288395196199417,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5763353109359741,
  "theta_neg_2_0p5_rmse_deg": 0.779032289981842,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.401319980621338,
  "theta_neg_2_0p5_max_abs_err_deg": 3.9224958419799805,
  "theta_neg_2_0p5_bias_deg": -0.24114498496055603,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0033427476882935,
  "theta_pos_0p5_2_rmse_deg": 1.2477182149887085,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9118292331695557,
  "theta_pos_0p5_2_max_abs_err_deg": 4.578224182128906,
  "theta_pos_0p5_2_bias_deg": 0.7764468193054199,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.32796971001870256,
  "loss_turn": 1.5922963920239666,
  "loss_theta": 0.00037748828581981713,
  "loss_main_bundle_base": 0.32796971001870256,
  "loss_turn_bundle_base": 0.31845928457173667,
  "loss_theta_bundle_base": 0.000273855279474828,
  "loss_main_bundle": 0.32796971001870256,
  "loss_turn_bundle": 0.31845928457173667,
  "loss_theta_bundle": 0.000273855279474828,
  "loss_theta_flat": 0.0002937508315435615,
  "loss_theta_near_flat": 0.0011454977560158269,
  "loss_theta_error_excess": 0.00013603407892991482,
  "loss_theta_flat_excess": 0.00013368344287285948,
  "loss_theta_near_flat_excess": 0.0008026253713385601,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010620981119859823,
  "loss_theta_small_neg": 0.00028492623668526965,
  "loss_theta_small_neg_excess": 8.743709365677225e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3967097384842549,
  "loss_false_turn_straight": 0.32131512419941943,
  "loss_transition_focal_raw": 1.3105657479759805,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.621755676531792,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
