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
  "turn_transition_weight": 2.0,
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
| acc_main | 0.9617 |
| acc_turn | 0.5594 |
| acc_turn_pure | 0.5745 |
| acc_turn_transition | 0.4933 |
| main_confidence_mean | 0.9848 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0172 |
| turn_confidence_mean | 0.7764 |
| turn_low_conf_0p60_ratio | 0.2165 |
| turn_low_conf_0p70_ratio | 0.3584 |
| turn_right_recall | 0.5770 |
| turn_straight_recall | 0.5354 |
| turn_left_recall | 0.5966 |
| theta_mae_deg | 0.6440 |
| theta_abs_le_10_p95_abs_err_deg | 1.8489 |
| theta_neg_10_8_p95_abs_err_deg | 1.3447 |
| theta_pos_8_10_p95_abs_err_deg | 3.0391 |
| theta_abs_le_8_p95_abs_err_deg | 1.7254 |
| theta_neg_8_6_p95_abs_err_deg | 1.7720 |
| theta_pos_6_8_p95_abs_err_deg | 1.9519 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.4859 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9843 |
| theta_flat_abs_p95_deg | 2.6573 |
| theta_flat_bias_deg | 0.0193 |
| theta_near_flat_abs_p95_deg | 2.0555 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0198 |
| theta_flat_turn_abs_p95_deg | 2.0376 |
| flat_recall | 0.9563 |
| stall_recall | 0.7083 |
| slope_recall | 0.9720 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7483 |
| downhill_recall | 0.7951 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    723,
    0,
    33
  ],
  [
    9,
    68,
    19
  ],
  [
    69,
    8,
    2673
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    461,
    206,
    132
  ],
  [
    375,
    1035,
    523
  ],
  [
    178,
    173,
    519
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.338470 |
| test_loss_turn_bundle_base | 0.269307 |
| test_loss_theta_bundle_base | 0.000170 |
| test_loss_transition_focal_raw | 1.132810 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.743399 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 49
- train_seconds: 268.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.3333 | 0.5505 |
| [0.60,0.70) | 35 | 0.4571 | 0.6550 |
| [0.70,0.80) | 47 | 0.5957 | 0.7546 |
| [0.80,0.90) | 54 | 0.2778 | 0.8671 |
| [0.90,1.00) | 3439 | 0.0204 | 0.9965 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 780 | 0.6295 | 0.5159 |
| [0.60,0.70) | 511 | 0.5166 | 0.6498 |
| [0.70,0.80) | 504 | 0.4901 | 0.7493 |
| [0.80,0.90) | 552 | 0.4674 | 0.8499 |
| [0.90,1.00) | 1255 | 0.2606 | 0.9686 |


## 验证集最佳点

```json
{
  "loss_total": 0.5659248097823663,
  "acc_main": 0.9450608930987822,
  "acc_turn": 0.6138024357239513,
  "acc_turn_pure": 0.6306129137987545,
  "acc_turn_transition": 0.5341614906832298,
  "false_turn_straight": 0.461018711018711,
  "flat_recall": 0.9558599695585996,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9509345794392523,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.047619047619047616,
  "recall_main": [
    0.9558599695585996,
    0.35714285714285715,
    0.9509345794392523
  ],
  "turn_right_recall": 0.6516587677725119,
  "turn_straight_recall": 0.5389812889812889,
  "turn_left_recall": 0.7346278317152104,
  "recall_turn": [
    0.6516587677725119,
    0.5389812889812889,
    0.7346278317152104
  ],
  "cm_turn": [
    [
      550,
      229,
      65
    ],
    [
      425,
      1037,
      462
    ],
    [
      101,
      145,
      681
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      628,
      0,
      29
    ],
    [
      2,
      15,
      25
    ],
    [
      139,
      8,
      2849
    ]
  ],
  "main_confidence_mean": 0.961882517009369,
  "main_confidence_error_mean": 0.715200846260165,
  "main_low_conf_0p60_ratio": 0.0543978349120433,
  "main_low_conf_0p70_ratio": 0.0625169147496617,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 201,
      "error_rate": 0.46766169154228854,
      "mean_confidence": 0.4826803241752345
    },
    {
      "bin": "[0.60,0.70)",
      "n": 30,
      "error_rate": 0.36666666666666664,
      "mean_confidence": 0.6513305192773892
    },
    {
      "bin": "[0.70,0.80)",
      "n": 32,
      "error_rate": 0.3125,
      "mean_confidence": 0.7493493470027518
    },
    {
      "bin": "[0.80,0.90)",
      "n": 56,
      "error_rate": 0.19642857142857142,
      "mean_confidence": 0.8569547408873769
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3376,
      "error_rate": 0.022808056872037914,
      "mean_confidence": 0.996927901367978
    }
  ],
  "turn_confidence_mean": 0.7975438651113897,
  "turn_confidence_error_mean": 0.7222806121140921,
  "turn_low_conf_0p60_ratio": 0.19702300405953993,
  "turn_low_conf_0p70_ratio": 0.30690121786197566,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 728,
      "error_rate": 0.6153846153846154,
      "mean_confidence": 0.5042102733629159
    },
    {
      "bin": "[0.60,0.70)",
      "n": 406,
      "error_rate": 0.5197044334975369,
      "mean_confidence": 0.6499811283258362
    },
    {
      "bin": "[0.70,0.80)",
      "n": 467,
      "error_rate": 0.49036402569593146,
      "mean_confidence": 0.7528473350259774
    },
    {
      "bin": "[0.80,0.90)",
      "n": 612,
      "error_rate": 0.3709150326797386,
      "mean_confidence": 0.8530862987608065
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1482,
      "error_rate": 0.21052631578947367,
      "mean_confidence": 0.973210960984715
    }
  ],
  "theta_mae_rad": 0.014769713394343853,
  "theta_mae_deg": 0.8462421894073486,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.7992213570634038,
  "slope_sign_acc": 0.9616753353408157,
  "theta_flat_mae_deg": 1.2351900339126587,
  "theta_flat_abs_p95_deg": 3.990793466567993,
  "theta_flat_abs_max_deg": 9.925164222717285,
  "theta_flat_bias_deg": 0.5233755707740784,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6074436902999878,
  "theta_near_flat_abs_p95_deg": 4.278161525726318,
  "theta_near_flat_abs_max_deg": 9.925164222717285,
  "theta_near_flat_bias_deg": 0.7054585218429565,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2195764780044556,
  "theta_flat_turn_abs_p95_deg": 3.990793466567993,
  "theta_flat_turn_abs_max_deg": 9.925164222717285,
  "theta_flat_turn_bias_deg": -0.09989004582166672,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8462421894073486,
  "theta_slope_control_abs_p95_deg": 9.154685020446777,
  "theta_slope_control_abs_max_deg": 13.65852165222168,
  "theta_slope_control_bias_deg": 0.1638871729373932,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8462421894073486,
  "theta_all_rmse_deg": 1.2856611013412476,
  "theta_all_p95_abs_err_deg": 2.855557441711426,
  "theta_all_max_abs_err_deg": 9.425164222717285,
  "theta_all_bias_deg": 0.16388720273971558,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7609488368034363,
  "theta_active_abs_ge_2_rmse_deg": 1.1595760583877563,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2948079109191895,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.7523722648620605,
  "theta_active_abs_ge_2_bias_deg": 0.08505410701036453,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.885929524898529,
  "theta_abs_le_8_rmse_deg": 1.3398631811141968,
  "theta_abs_le_8_p95_abs_err_deg": 3.1385293006896973,
  "theta_abs_le_8_max_abs_err_deg": 9.425164222717285,
  "theta_abs_le_8_bias_deg": 0.20526087284088135,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8462421894073486,
  "theta_abs_le_10_rmse_deg": 1.2856611013412476,
  "theta_abs_le_10_p95_abs_err_deg": 2.855557441711426,
  "theta_abs_le_10_max_abs_err_deg": 9.425164222717285,
  "theta_abs_le_10_bias_deg": 0.16388720273971558,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5678219795227051,
  "theta_pos_8_10_rmse_deg": 0.7585891485214233,
  "theta_pos_8_10_p95_abs_err_deg": 1.4874271154403687,
  "theta_pos_8_10_max_abs_err_deg": 3.002131700515747,
  "theta_pos_8_10_bias_deg": -0.2839744985103607,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7917335629463196,
  "theta_neg_10_8_rmse_deg": 1.240145206451416,
  "theta_neg_10_8_p95_abs_err_deg": 2.444338798522949,
  "theta_neg_10_8_max_abs_err_deg": 6.7523722648620605,
  "theta_neg_10_8_bias_deg": 0.26739925146102905,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5483910441398621,
  "theta_pos_6_8_rmse_deg": 0.7756081223487854,
  "theta_pos_6_8_p95_abs_err_deg": 1.6856307983398438,
  "theta_pos_6_8_max_abs_err_deg": 3.4488561153411865,
  "theta_pos_6_8_bias_deg": -0.02231529727578163,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8286523222923279,
  "theta_neg_8_6_rmse_deg": 1.207310676574707,
  "theta_neg_8_6_p95_abs_err_deg": 2.269649028778076,
  "theta_neg_8_6_max_abs_err_deg": 6.147096157073975,
  "theta_neg_8_6_bias_deg": 0.06752178072929382,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7478381395339966,
  "theta_neg_4_2_rmse_deg": 1.014746069908142,
  "theta_neg_4_2_p95_abs_err_deg": 2.0108656883239746,
  "theta_neg_4_2_max_abs_err_deg": 4.136312484741211,
  "theta_neg_4_2_bias_deg": 0.11226378381252289,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8118289709091187,
  "theta_neg_2_0p5_rmse_deg": 1.0207240581512451,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.9297860860824585,
  "theta_neg_2_0p5_max_abs_err_deg": 3.8922035694122314,
  "theta_neg_2_0p5_bias_deg": 0.07238162308931351,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.313591718673706,
  "theta_pos_0p5_2_rmse_deg": 1.5848077535629272,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.490793466567993,
  "theta_pos_0p5_2_max_abs_err_deg": 3.662182569503784,
  "theta_pos_0p5_2_bias_deg": 1.0620455741882324,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3148025900891734,
  "loss_turn": 1.2539441995917542,
  "loss_theta": 0.0005035375257990549,
  "loss_main_bundle_base": 0.3148025900891734,
  "loss_turn_bundle_base": 0.2507888448738439,
  "loss_theta_bundle_base": 0.00033338497659375486,
  "loss_main_bundle": 0.3148025900891734,
  "loss_turn_bundle": 0.2507888448738439,
  "loss_theta_bundle": 0.00033338497659375486,
  "loss_theta_flat": 0.0002622194989120143,
  "loss_theta_near_flat": 0.001531603382975972,
  "loss_theta_error_excess": 0.00019870629704731274,
  "loss_theta_flat_excess": 0.00015091969932811347,
  "loss_theta_near_flat_excess": 0.0011275469405508532,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001503767263105187,
  "loss_theta_small_neg": 0.0003122157679684208,
  "loss_theta_small_neg_excess": 7.384301641204865e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.40023064047945045,
  "loss_false_turn_straight": 0.319471840227731,
  "loss_transition_focal_raw": 0.9864586661729825,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.3251764885950155,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
