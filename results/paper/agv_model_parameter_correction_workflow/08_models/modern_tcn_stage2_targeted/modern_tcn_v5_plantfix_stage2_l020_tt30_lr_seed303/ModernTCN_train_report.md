# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

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
    1.5,
    0.75,
    1.5
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
  "select_turn_weight": 0.6,
  "select_turn_transition_weight": 1.45,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.8,
  "select_turn_lr_target": 0.88,
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
| acc_main | 0.9667 |
| acc_turn | 0.6074 |
| acc_turn_pure | 0.6169 |
| acc_turn_transition | 0.5663 |
| main_confidence_mean | 0.9885 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0117 |
| turn_confidence_mean | 0.8104 |
| turn_low_conf_0p60_ratio | 0.1952 |
| turn_low_conf_0p70_ratio | 0.3115 |
| turn_right_recall | 0.5269 |
| turn_straight_recall | 0.6684 |
| turn_left_recall | 0.5460 |
| theta_mae_deg | 0.7080 |
| theta_abs_le_10_p95_abs_err_deg | 1.9131 |
| theta_neg_10_8_p95_abs_err_deg | 1.4962 |
| theta_pos_8_10_p95_abs_err_deg | 2.8260 |
| theta_abs_le_8_p95_abs_err_deg | 1.8491 |
| theta_neg_8_6_p95_abs_err_deg | 1.6901 |
| theta_pos_6_8_p95_abs_err_deg | 1.8044 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.5058 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.9274 |
| theta_flat_abs_p95_deg | 2.6644 |
| theta_flat_bias_deg | 0.1929 |
| theta_near_flat_abs_p95_deg | 1.9394 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.3431 |
| theta_flat_turn_abs_p95_deg | 1.8030 |
| flat_recall | 0.9656 |
| stall_recall | 0.6354 |
| slope_recall | 0.9785 |
| uphill_recall | 0.7586 |
| downhill_recall | 0.7911 |

- best_epoch: 66
- train_seconds: 918.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.5000 | 0.5604 |
| [0.60,0.70) | 18 | 0.6111 | 0.6584 |
| [0.70,0.80) | 29 | 0.3448 | 0.7548 |
| [0.80,0.90) | 58 | 0.2414 | 0.8529 |
| [0.90,1.00) | 3473 | 0.0210 | 0.9974 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 703 | 0.5263 | 0.5172 |
| [0.60,0.70) | 419 | 0.5131 | 0.6533 |
| [0.70,0.80) | 370 | 0.4459 | 0.7519 |
| [0.80,0.90) | 442 | 0.4367 | 0.8529 |
| [0.90,1.00) | 1668 | 0.2824 | 0.9753 |


## 验证集最佳点

```json
{
  "loss_total": 0.6487459641348202,
  "acc_main": 0.9361299052774019,
  "acc_turn": 0.6381596752368065,
  "acc_turn_pure": 0.6492953130121272,
  "acc_turn_transition": 0.5854037267080745,
  "flat_recall": 0.923896499238965,
  "stall_recall": 0.2619047619047619,
  "slope_recall": 0.94826435246996,
  "recall_main": [
    0.923896499238965,
    0.2619047619047619,
    0.94826435246996
  ],
  "turn_right_recall": 0.6445497630331753,
  "turn_straight_recall": 0.6330561330561331,
  "turn_left_recall": 0.6429341963322546,
  "recall_turn": [
    0.6445497630331753,
    0.6330561330561331,
    0.6429341963322546
  ],
  "cm_turn": [
    [
      544,
      247,
      53
    ],
    [
      350,
      1218,
      356
    ],
    [
      63,
      268,
      596
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      607,
      0,
      50
    ],
    [
      6,
      11,
      25
    ],
    [
      143,
      12,
      2841
    ]
  ],
  "main_confidence_mean": 0.9674460544901459,
  "main_confidence_error_mean": 0.7865728785989591,
  "main_low_conf_0p60_ratio": 0.008660351826792964,
  "main_low_conf_0p70_ratio": 0.06549391069012178,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 32,
      "error_rate": 0.4375,
      "mean_confidence": 0.56238411124406
    },
    {
      "bin": "[0.60,0.70)",
      "n": 210,
      "error_rate": 0.4666666666666667,
      "mean_confidence": 0.6162632748280799
    },
    {
      "bin": "[0.70,0.80)",
      "n": 37,
      "error_rate": 0.32432432432432434,
      "mean_confidence": 0.7428823608359121
    },
    {
      "bin": "[0.80,0.90)",
      "n": 50,
      "error_rate": 0.36,
      "mean_confidence": 0.8545309904424373
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3366,
      "error_rate": 0.027926322043969103,
      "mean_confidence": 0.9973524644071098
    }
  ],
  "turn_confidence_mean": 0.8312692435834138,
  "turn_confidence_error_mean": 0.7613581284144841,
  "turn_low_conf_0p60_ratio": 0.16535859269282815,
  "turn_low_conf_0p70_ratio": 0.25953991880920163,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 611,
      "error_rate": 0.6055646481178396,
      "mean_confidence": 0.49610226797112866
    },
    {
      "bin": "[0.60,0.70)",
      "n": 348,
      "error_rate": 0.4511494252873563,
      "mean_confidence": 0.6508964802647492
    },
    {
      "bin": "[0.70,0.80)",
      "n": 350,
      "error_rate": 0.38,
      "mean_confidence": 0.7492060387061799
    },
    {
      "bin": "[0.80,0.90)",
      "n": 432,
      "error_rate": 0.39351851851851855,
      "mean_confidence": 0.8520721427895501
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1954,
      "error_rate": 0.259467758444217,
      "mean_confidence": 0.9782968858474786
    }
  ],
  "theta_mae_rad": 0.014557684771716595,
  "theta_mae_deg": 0.8340938687324524,
  "uphill_recall": 0.7714285714285715,
  "downhill_recall": 0.8120133481646273,
  "slope_sign_acc": 0.9753627155762387,
  "theta_flat_mae_deg": 1.136113166809082,
  "theta_flat_abs_p95_deg": 3.6261239051818848,
  "theta_flat_abs_max_deg": 7.474027156829834,
  "theta_flat_bias_deg": 0.6082332134246826,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.480380654335022,
  "theta_near_flat_abs_p95_deg": 4.079928398132324,
  "theta_near_flat_abs_max_deg": 7.474027156829834,
  "theta_near_flat_bias_deg": 0.8659668564796448,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.1175559759140015,
  "theta_flat_turn_abs_p95_deg": 3.62494158744812,
  "theta_flat_turn_abs_max_deg": 7.474027156829834,
  "theta_flat_turn_bias_deg": 0.2523173689842224,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8340938687324524,
  "theta_slope_control_abs_p95_deg": 9.157699584960938,
  "theta_slope_control_abs_max_deg": 11.70093059539795,
  "theta_slope_control_bias_deg": -0.12107927352190018,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8340939283370972,
  "theta_all_rmse_deg": 1.1733582019805908,
  "theta_all_p95_abs_err_deg": 2.494511365890503,
  "theta_all_max_abs_err_deg": 6.974027156829834,
  "theta_all_bias_deg": -0.12107928097248077,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7678633332252502,
  "theta_active_abs_ge_2_rmse_deg": 1.0556237697601318,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.103250503540039,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.292661666870117,
  "theta_active_abs_ge_2_bias_deg": -0.2810119390487671,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8363433480262756,
  "theta_abs_le_8_rmse_deg": 1.1879065036773682,
  "theta_abs_le_8_p95_abs_err_deg": 2.6522605419158936,
  "theta_abs_le_8_max_abs_err_deg": 6.974027156829834,
  "theta_abs_le_8_bias_deg": -0.041606370359659195,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8340939283370972,
  "theta_abs_le_10_rmse_deg": 1.1733582019805908,
  "theta_abs_le_10_p95_abs_err_deg": 2.494511365890503,
  "theta_abs_le_10_max_abs_err_deg": 6.974027156829834,
  "theta_abs_le_10_bias_deg": -0.12107928097248077,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.9096771478652954,
  "theta_pos_8_10_rmse_deg": 1.0653899908065796,
  "theta_pos_8_10_p95_abs_err_deg": 1.9085252285003662,
  "theta_pos_8_10_max_abs_err_deg": 4.084928035736084,
  "theta_pos_8_10_bias_deg": -0.7797043323516846,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7380605936050415,
  "theta_neg_10_8_rmse_deg": 1.153395652770996,
  "theta_neg_10_8_p95_abs_err_deg": 2.1444249153137207,
  "theta_neg_10_8_max_abs_err_deg": 6.292661666870117,
  "theta_neg_10_8_bias_deg": -0.12738719582557678,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8044406175613403,
  "theta_pos_6_8_rmse_deg": 0.9797008037567139,
  "theta_pos_6_8_p95_abs_err_deg": 1.8502223491668701,
  "theta_pos_6_8_max_abs_err_deg": 2.8181581497192383,
  "theta_pos_6_8_bias_deg": -0.5681248903274536,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6431146264076233,
  "theta_neg_8_6_rmse_deg": 0.9875314235687256,
  "theta_neg_8_6_p95_abs_err_deg": 1.8842705488204956,
  "theta_neg_8_6_max_abs_err_deg": 6.081831932067871,
  "theta_neg_8_6_bias_deg": -0.1606002002954483,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7228212356567383,
  "theta_neg_4_2_rmse_deg": 0.9941627979278564,
  "theta_neg_4_2_p95_abs_err_deg": 1.8784960508346558,
  "theta_neg_4_2_max_abs_err_deg": 5.278310775756836,
  "theta_neg_4_2_bias_deg": -0.32899585366249084,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6141223907470703,
  "theta_neg_2_0p5_rmse_deg": 0.8107908964157104,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4887231588363647,
  "theta_neg_2_0p5_max_abs_err_deg": 4.5260772705078125,
  "theta_neg_2_0p5_bias_deg": 0.027024900540709496,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.32708740234375,
  "theta_pos_0p5_2_rmse_deg": 1.5762866735458374,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.6421895027160645,
  "theta_pos_0p5_2_max_abs_err_deg": 4.009298801422119,
  "theta_pos_0p5_2_bias_deg": 1.076027750968933,
  "theta_pos_0p5_2_n": 163.0
}
```
