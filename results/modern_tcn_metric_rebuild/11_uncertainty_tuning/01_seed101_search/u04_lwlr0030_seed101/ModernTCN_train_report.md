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
| acc_main | 0.9659 |
| acc_turn | 0.5505 |
| acc_turn_pure | 0.5684 |
| acc_turn_transition | 0.4724 |
| main_confidence_mean | 0.9853 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0142 |
| turn_confidence_mean | 0.7618 |
| turn_low_conf_0p60_ratio | 0.2399 |
| turn_low_conf_0p70_ratio | 0.3878 |
| turn_right_recall | 0.6170 |
| turn_straight_recall | 0.4713 |
| turn_left_recall | 0.6655 |
| theta_mae_deg | 0.3928 |
| theta_abs_le_10_p95_abs_err_deg | 1.0325 |
| theta_neg_10_8_p95_abs_err_deg | 0.8891 |
| theta_pos_8_10_p95_abs_err_deg | 1.7507 |
| theta_abs_le_8_p95_abs_err_deg | 0.9728 |
| theta_neg_8_6_p95_abs_err_deg | 0.9280 |
| theta_pos_6_8_p95_abs_err_deg | 1.0145 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.9734 |
| theta_pos_0p5_2_p95_abs_err_deg | 0.9732 |
| theta_flat_abs_p95_deg | 2.1636 |
| theta_flat_bias_deg | 0.0059 |
| theta_near_flat_abs_p95_deg | 1.1704 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0804 |
| theta_flat_turn_abs_p95_deg | 0.9859 |
| flat_recall | 0.9577 |
| stall_recall | 0.7083 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1146 |
| uphill_recall | 0.7563 |
| downhill_recall | 0.7946 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    724,
    0,
    32
  ],
  [
    11,
    68,
    17
  ],
  [
    55,
    8,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    493,
    167,
    139
  ],
  [
    403,
    911,
    619
  ],
  [
    156,
    135,
    579
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.300480 |
| test_loss_turn_bundle_base | 0.252900 |
| test_loss_theta_bundle_base | 0.000067 |
| test_loss_transition_focal_raw | 0.928141 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.297564 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 378.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.4583 | 0.5544 |
| [0.60,0.70) | 27 | 0.5556 | 0.6556 |
| [0.70,0.80) | 34 | 0.3824 | 0.7506 |
| [0.80,0.90) | 76 | 0.2632 | 0.8529 |
| [0.90,1.00) | 3441 | 0.0186 | 0.9962 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 864 | 0.5914 | 0.5209 |
| [0.60,0.70) | 533 | 0.5291 | 0.6504 |
| [0.70,0.80) | 550 | 0.5400 | 0.7491 |
| [0.80,0.90) | 541 | 0.4104 | 0.8515 |
| [0.90,1.00) | 1114 | 0.2756 | 0.9646 |


## 验证集最佳点

```json
{
  "loss_total": 0.4888067018517945,
  "acc_main": 0.9453315290933694,
  "acc_turn": 0.5975642760487144,
  "acc_turn_pure": 0.615535889872173,
  "acc_turn_transition": 0.5124223602484472,
  "false_turn_straight": 0.5161122661122661,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.3333333333333333,
  "slope_recall": 0.9526034712950601,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9512937595129376,
    0.3333333333333333,
    0.9526034712950601
  ],
  "turn_right_recall": 0.5995260663507109,
  "turn_straight_recall": 0.4838877338877339,
  "turn_left_recall": 0.8317152103559871,
  "recall_turn": [
    0.5995260663507109,
    0.4838877338877339,
    0.8317152103559871
  ],
  "cm_turn": [
    [
      506,
      185,
      153
    ],
    [
      345,
      931,
      648
    ],
    [
      55,
      101,
      771
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      625,
      0,
      32
    ],
    [
      0,
      14,
      28
    ],
    [
      133,
      9,
      2854
    ]
  ],
  "main_confidence_mean": 0.9670198592104704,
  "main_confidence_error_mean": 0.7416088415295686,
  "main_low_conf_0p60_ratio": 0.053585926928281465,
  "main_low_conf_0p70_ratio": 0.06035182679296346,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 198,
      "error_rate": 0.5,
      "mean_confidence": 0.5533997781349667
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.44,
      "mean_confidence": 0.6495981550613663
    },
    {
      "bin": "[0.70,0.80)",
      "n": 26,
      "error_rate": 0.23076923076923078,
      "mean_confidence": 0.7560433259000059
    },
    {
      "bin": "[0.80,0.90)",
      "n": 45,
      "error_rate": 0.17777777777777778,
      "mean_confidence": 0.8516756876261198
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3401,
      "error_rate": 0.022934431049691267,
      "mean_confidence": 0.9965724014756998
    }
  ],
  "turn_confidence_mean": 0.7876414567338182,
  "turn_confidence_error_mean": 0.7155470828561504,
  "turn_low_conf_0p60_ratio": 0.18998646820027063,
  "turn_low_conf_0p70_ratio": 0.318809201623816,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 702,
      "error_rate": 0.613960113960114,
      "mean_confidence": 0.48860983132696567
    },
    {
      "bin": "[0.60,0.70)",
      "n": 476,
      "error_rate": 0.5336134453781513,
      "mean_confidence": 0.6520475004932429
    },
    {
      "bin": "[0.70,0.80)",
      "n": 512,
      "error_rate": 0.48046875,
      "mean_confidence": 0.7495385323080815
    },
    {
      "bin": "[0.80,0.90)",
      "n": 582,
      "error_rate": 0.4020618556701031,
      "mean_confidence": 0.8516299821743374
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1423,
      "error_rate": 0.22628250175685172,
      "mean_confidence": 0.9680562843555467
    }
  ],
  "theta_mae_rad": 0.009241684339940548,
  "theta_mae_deg": 0.5295094847679138,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9819326580892417,
  "theta_flat_mae_deg": 0.885239839553833,
  "theta_flat_abs_p95_deg": 3.6642019748687744,
  "theta_flat_abs_max_deg": 11.384815216064453,
  "theta_flat_bias_deg": 0.2779514193534851,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.295045256614685,
  "theta_near_flat_abs_p95_deg": 4.2299017906188965,
  "theta_near_flat_abs_max_deg": 11.384815216064453,
  "theta_near_flat_bias_deg": 0.6442930698394775,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9535643458366394,
  "theta_flat_turn_abs_p95_deg": 4.711789131164551,
  "theta_flat_turn_abs_max_deg": 11.384815216064453,
  "theta_flat_turn_bias_deg": -0.12923729419708252,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.5295094847679138,
  "theta_slope_control_abs_p95_deg": 9.165738105773926,
  "theta_slope_control_abs_max_deg": 11.384815216064453,
  "theta_slope_control_bias_deg": -0.03401082754135132,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.5295094847679138,
  "theta_all_rmse_deg": 0.9369490146636963,
  "theta_all_p95_abs_err_deg": 2.12247371673584,
  "theta_all_max_abs_err_deg": 10.884815216064453,
  "theta_all_bias_deg": -0.03401083126664162,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.45150047540664673,
  "theta_active_abs_ge_2_rmse_deg": 0.7136679887771606,
  "theta_active_abs_ge_2_p95_abs_err_deg": 1.3879185914993286,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.0436577796936035,
  "theta_active_abs_ge_2_bias_deg": -0.10242176800966263,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.548237144947052,
  "theta_abs_le_8_rmse_deg": 0.9824512600898743,
  "theta_abs_le_8_p95_abs_err_deg": 2.164194345474243,
  "theta_abs_le_8_max_abs_err_deg": 10.884815216064453,
  "theta_abs_le_8_bias_deg": -0.024350212886929512,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.5295094847679138,
  "theta_abs_le_10_rmse_deg": 0.9369490146636963,
  "theta_abs_le_10_p95_abs_err_deg": 2.12247371673584,
  "theta_abs_le_10_max_abs_err_deg": 10.884815216064453,
  "theta_abs_le_10_bias_deg": -0.03401083126664162,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.40686070919036865,
  "theta_pos_8_10_rmse_deg": 0.570047914981842,
  "theta_pos_8_10_p95_abs_err_deg": 1.235175609588623,
  "theta_pos_8_10_max_abs_err_deg": 2.6769776344299316,
  "theta_pos_8_10_bias_deg": -0.21423305571079254,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.49490487575531006,
  "theta_neg_10_8_rmse_deg": 0.8349297642707825,
  "theta_neg_10_8_p95_abs_err_deg": 1.2694356441497803,
  "theta_neg_10_8_max_abs_err_deg": 6.0436577796936035,
  "theta_neg_10_8_bias_deg": 0.0671149417757988,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.38746657967567444,
  "theta_pos_6_8_rmse_deg": 0.7004154920578003,
  "theta_pos_6_8_p95_abs_err_deg": 1.331355333328247,
  "theta_pos_6_8_max_abs_err_deg": 3.6644747257232666,
  "theta_pos_6_8_bias_deg": -0.04694535955786705,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.46847397089004517,
  "theta_neg_8_6_rmse_deg": 0.6859229803085327,
  "theta_neg_8_6_p95_abs_err_deg": 1.3960013389587402,
  "theta_neg_8_6_max_abs_err_deg": 4.07855224609375,
  "theta_neg_8_6_bias_deg": -0.19854478538036346,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.5508283972740173,
  "theta_neg_4_2_rmse_deg": 0.8154549598693848,
  "theta_neg_4_2_p95_abs_err_deg": 1.5371849536895752,
  "theta_neg_4_2_max_abs_err_deg": 4.701025485992432,
  "theta_neg_4_2_bias_deg": -0.33154773712158203,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5101537108421326,
  "theta_neg_2_0p5_rmse_deg": 0.722021222114563,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5743921995162964,
  "theta_neg_2_0p5_max_abs_err_deg": 3.6004879474639893,
  "theta_neg_2_0p5_bias_deg": -0.3120613992214203,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.768807053565979,
  "theta_pos_0p5_2_rmse_deg": 1.172482967376709,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.164194345474243,
  "theta_pos_0p5_2_max_abs_err_deg": 4.264864444732666,
  "theta_pos_0p5_2_bias_deg": 0.5336524844169617,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.259431024551069,
  "loss_turn": 1.1459912324951853,
  "loss_theta": 0.0002674423477798952,
  "loss_main_bundle_base": 0.259431024551069,
  "loss_turn_bundle_base": 0.22919824989222706,
  "loss_theta_bundle_base": 0.0001774326127910349,
  "loss_main_bundle": 0.259431024551069,
  "loss_turn_bundle": 0.22919824989222706,
  "loss_theta_bundle": 0.0001774326127910349,
  "loss_theta_flat": 0.00017625376291176306,
  "loss_theta_near_flat": 0.0014645743303515109,
  "loss_theta_error_excess": 0.00010630756514827457,
  "loss_theta_flat_excess": 9.358595301011805e-05,
  "loss_theta_near_flat_excess": 0.0011247567237003206,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 3.8734845627973256e-05,
  "loss_theta_small_neg": 0.00019993130645383256,
  "loss_theta_small_neg_excess": 4.683053875294432e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.46256593031876786,
  "loss_false_turn_straight": 0.354026673514401,
  "loss_transition_focal_raw": 0.8864298360434856,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.1732257837190194,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
