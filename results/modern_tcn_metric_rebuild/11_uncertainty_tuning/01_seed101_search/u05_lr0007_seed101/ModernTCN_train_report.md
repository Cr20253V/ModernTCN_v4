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
| acc_main | 0.9628 |
| acc_turn | 0.5725 |
| acc_turn_pure | 0.5926 |
| acc_turn_transition | 0.4844 |
| main_confidence_mean | 0.9894 |
| main_low_conf_0p60_ratio | 0.0044 |
| main_low_conf_0p70_ratio | 0.0142 |
| turn_confidence_mean | 0.8238 |
| turn_low_conf_0p60_ratio | 0.1349 |
| turn_low_conf_0p70_ratio | 0.2582 |
| turn_right_recall | 0.5995 |
| turn_straight_recall | 0.5504 |
| turn_left_recall | 0.5966 |
| theta_mae_deg | 0.7839 |
| theta_abs_le_10_p95_abs_err_deg | 1.9900 |
| theta_neg_10_8_p95_abs_err_deg | 1.5326 |
| theta_pos_8_10_p95_abs_err_deg | 3.0427 |
| theta_abs_le_8_p95_abs_err_deg | 1.9274 |
| theta_neg_8_6_p95_abs_err_deg | 1.6721 |
| theta_pos_6_8_p95_abs_err_deg | 1.6579 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8709 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9443 |
| theta_flat_abs_p95_deg | 2.7769 |
| theta_flat_bias_deg | -0.7483 |
| theta_near_flat_abs_p95_deg | 2.2911 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.8110 |
| theta_flat_turn_abs_p95_deg | 2.2190 |
| flat_recall | 0.9563 |
| stall_recall | 0.6979 |
| slope_recall | 0.9738 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7477 |
| downhill_recall | 0.7985 |

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
    10,
    67,
    19
  ],
  [
    64,
    8,
    2678
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    479,
    192,
    128
  ],
  [
    389,
    1064,
    480
  ],
  [
    182,
    169,
    519
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.323159 |
| test_loss_turn_bundle_base | 0.323994 |
| test_loss_theta_bundle_base | 0.000225 |
| test_loss_transition_focal_raw | 1.458259 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.309704 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 385.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 16 | 0.5000 | 0.5466 |
| [0.60,0.70) | 35 | 0.4857 | 0.6500 |
| [0.70,0.80) | 21 | 0.4286 | 0.7546 |
| [0.80,0.90) | 45 | 0.5778 | 0.8635 |
| [0.90,1.00) | 3485 | 0.0212 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 486 | 0.5864 | 0.5233 |
| [0.60,0.70) | 444 | 0.5901 | 0.6475 |
| [0.70,0.80) | 485 | 0.4845 | 0.7479 |
| [0.80,0.90) | 552 | 0.4746 | 0.8483 |
| [0.90,1.00) | 1635 | 0.3034 | 0.9753 |


## 验证集最佳点

```json
{
  "loss_total": 0.6175112394583241,
  "acc_main": 0.9450608930987822,
  "acc_turn": 0.6346414073071719,
  "acc_turn_pure": 0.6460176991150443,
  "acc_turn_transition": 0.5807453416149069,
  "false_turn_straight": 0.42775467775467774,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.38095238095238093,
  "slope_recall": 0.9516021361815754,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9512937595129376,
    0.38095238095238093,
    0.9516021361815754
  ],
  "turn_right_recall": 0.6848341232227488,
  "turn_straight_recall": 0.5722453222453222,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6848341232227488,
    0.5722453222453222,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      578,
      212,
      54
    ],
    [
      395,
      1101,
      428
    ],
    [
      97,
      164,
      666
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
      16,
      26
    ],
    [
      133,
      12,
      2851
    ]
  ],
  "main_confidence_mean": 0.9714878208637507,
  "main_confidence_error_mean": 0.775993937327166,
  "main_low_conf_0p60_ratio": 0.04817320703653586,
  "main_low_conf_0p70_ratio": 0.05493910690121786,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 178,
      "error_rate": 0.449438202247191,
      "mean_confidence": 0.5489162652803845
    },
    {
      "bin": "[0.60,0.70)",
      "n": 25,
      "error_rate": 0.48,
      "mean_confidence": 0.642133940621949
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.5714285714285714,
      "mean_confidence": 0.7456946401890646
    },
    {
      "bin": "[0.80,0.90)",
      "n": 32,
      "error_rate": 0.28125,
      "mean_confidence": 0.8528976076217674
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3439,
      "error_rate": 0.026170398371619656,
      "mean_confidence": 0.9982363313370848
    }
  ],
  "turn_confidence_mean": 0.8484868536250951,
  "turn_confidence_error_mean": 0.7787909494420356,
  "turn_low_conf_0p60_ratio": 0.1442489851150203,
  "turn_low_conf_0p70_ratio": 0.227063599458728,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 533,
      "error_rate": 0.6228893058161351,
      "mean_confidence": 0.5296423805915914
    },
    {
      "bin": "[0.60,0.70)",
      "n": 306,
      "error_rate": 0.5032679738562091,
      "mean_confidence": 0.6492113222611805
    },
    {
      "bin": "[0.70,0.80)",
      "n": 358,
      "error_rate": 0.5027932960893855,
      "mean_confidence": 0.7512139048251663
    },
    {
      "bin": "[0.80,0.90)",
      "n": 453,
      "error_rate": 0.41280353200883,
      "mean_confidence": 0.850717199613444
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2045,
      "error_rate": 0.2430317848410758,
      "mean_confidence": 0.9779420055379889
    }
  ],
  "theta_mae_rad": 0.015331139788031578,
  "theta_mae_deg": 0.8784095644950867,
  "uphill_recall": 0.7752021563342318,
  "downhill_recall": 0.803670745272525,
  "slope_sign_acc": 0.9737202299479879,
  "theta_flat_mae_deg": 1.2290865182876587,
  "theta_flat_abs_p95_deg": 3.2659265995025635,
  "theta_flat_abs_max_deg": 10.61212158203125,
  "theta_flat_bias_deg": -0.26826396584510803,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5682151317596436,
  "theta_near_flat_abs_p95_deg": 3.4621407985687256,
  "theta_near_flat_abs_max_deg": 10.61212158203125,
  "theta_near_flat_bias_deg": -0.018927574157714844,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3258298635482788,
  "theta_flat_turn_abs_p95_deg": 3.49304461479187,
  "theta_flat_turn_abs_max_deg": 10.61212158203125,
  "theta_flat_turn_bias_deg": -0.6310063600540161,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8784095644950867,
  "theta_slope_control_abs_p95_deg": 9.361056327819824,
  "theta_slope_control_abs_max_deg": 13.808176040649414,
  "theta_slope_control_bias_deg": -0.46878287196159363,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8784095048904419,
  "theta_all_rmse_deg": 1.1940646171569824,
  "theta_all_p95_abs_err_deg": 2.4035274982452393,
  "theta_all_max_abs_err_deg": 10.11212158203125,
  "theta_all_bias_deg": -0.46878287196159363,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8015087246894836,
  "theta_active_abs_ge_2_rmse_deg": 1.0822750329971313,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0583157539367676,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.348686695098877,
  "theta_active_abs_ge_2_bias_deg": -0.5127550959587097,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9097847938537598,
  "theta_abs_le_8_rmse_deg": 1.23475182056427,
  "theta_abs_le_8_p95_abs_err_deg": 2.631765604019165,
  "theta_abs_le_8_max_abs_err_deg": 10.11212158203125,
  "theta_abs_le_8_bias_deg": -0.4685240387916565,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8784095048904419,
  "theta_abs_le_10_rmse_deg": 1.1940646171569824,
  "theta_abs_le_10_p95_abs_err_deg": 2.4035274982452393,
  "theta_abs_le_10_max_abs_err_deg": 10.11212158203125,
  "theta_abs_le_10_bias_deg": -0.46878287196159363,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.690412163734436,
  "theta_pos_8_10_rmse_deg": 0.8539769053459167,
  "theta_pos_8_10_p95_abs_err_deg": 1.5593490600585938,
  "theta_pos_8_10_max_abs_err_deg": 4.63770055770874,
  "theta_pos_8_10_bias_deg": -0.5232176780700684,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8026508092880249,
  "theta_neg_10_8_rmse_deg": 1.1372628211975098,
  "theta_neg_10_8_p95_abs_err_deg": 1.8380159139633179,
  "theta_neg_10_8_max_abs_err_deg": 5.348686695098877,
  "theta_neg_10_8_bias_deg": -0.4156092703342438,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6065489649772644,
  "theta_pos_6_8_rmse_deg": 0.8263370394706726,
  "theta_pos_6_8_p95_abs_err_deg": 1.7611364126205444,
  "theta_pos_6_8_max_abs_err_deg": 3.053257465362549,
  "theta_pos_6_8_bias_deg": -0.2555394470691681,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8669348359107971,
  "theta_neg_8_6_rmse_deg": 1.154380440711975,
  "theta_neg_8_6_p95_abs_err_deg": 2.055149555206299,
  "theta_neg_8_6_max_abs_err_deg": 5.156132698059082,
  "theta_neg_8_6_bias_deg": -0.633423924446106,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9971709251403809,
  "theta_neg_4_2_rmse_deg": 1.2000786066055298,
  "theta_neg_4_2_p95_abs_err_deg": 2.023078203201294,
  "theta_neg_4_2_max_abs_err_deg": 4.198434352874756,
  "theta_neg_4_2_bias_deg": -0.8236603140830994,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.975561261177063,
  "theta_neg_2_0p5_rmse_deg": 1.1296099424362183,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.7489720582962036,
  "theta_neg_2_0p5_max_abs_err_deg": 3.996490240097046,
  "theta_neg_2_0p5_bias_deg": -0.8819693326950073,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.076414942741394,
  "theta_pos_0p5_2_rmse_deg": 1.2480335235595703,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0011518001556396,
  "theta_pos_0p5_2_max_abs_err_deg": 3.951622486114502,
  "theta_pos_0p5_2_bias_deg": 0.2716051936149597,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3302897772866431,
  "loss_turn": 1.4345190572803173,
  "loss_theta": 0.00043434931430965664,
  "loss_main_bundle_base": 0.3302897772866431,
  "loss_turn_bundle_base": 0.2869038147597255,
  "loss_theta_bundle_base": 0.00031764320674741763,
  "loss_main_bundle": 0.3302897772866431,
  "loss_turn_bundle": 0.2869038147597255,
  "loss_theta_bundle": 0.00031764320674741763,
  "loss_theta_flat": 0.0005224355098858213,
  "loss_theta_near_flat": 0.0013711508518495725,
  "loss_theta_error_excess": 0.00013195943748654044,
  "loss_theta_flat_excess": 0.00023448343023422133,
  "loss_theta_near_flat_excess": 0.0009519509163323452,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.460843742241597e-05,
  "loss_theta_small_neg": 0.0004366269632253962,
  "loss_theta_small_neg_excess": 8.954724340012148e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.37644388300640175,
  "loss_false_turn_straight": 0.31676530162116995,
  "loss_transition_focal_raw": 1.2024250452508785,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.996255718226039,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
