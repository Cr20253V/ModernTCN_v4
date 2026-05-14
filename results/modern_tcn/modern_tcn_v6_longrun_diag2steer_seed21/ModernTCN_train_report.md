# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=19]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## 配置

```json
{
  "input_dim": 19,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "dropout": 0.15,
  "expansion": 2,
  "readout_input_stats": true,
  "turn_head_source": "full",
  "turn_feature_indices": [
    1,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    16
  ],
  "lambda_turn": 0.05,
  "lambda_theta": 0.35,
  "lambda_theta_flat": 0.2,
  "lambda_theta_near_flat": 0.0,
  "theta_near_flat_deg": 0.5,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.0,
    1.0,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9662 |
| acc_turn | 0.9276 |
| acc_turn_pure | 0.9433 |
| acc_turn_transition | 0.6237 |
| main_confidence_mean | 0.9881 |
| main_low_conf_0p60_ratio | 0.0042 |
| main_low_conf_0p70_ratio | 0.0111 |
| turn_confidence_mean | 0.9536 |
| turn_low_conf_0p60_ratio | 0.0201 |
| turn_low_conf_0p70_ratio | 0.0465 |
| turn_right_recall | 0.9298 |
| turn_straight_recall | 0.9459 |
| turn_left_recall | 0.8682 |
| theta_mae_deg | 1.0383 |
| theta_flat_abs_p95_deg | 4.1397 |
| theta_flat_bias_deg | 0.1783 |
| theta_near_flat_abs_p95_deg | 4.8549 |
| theta_near_flat_bias_deg | 0.2127 |
| theta_flat_turn_abs_p95_deg | 2.8722 |
| flat_recall | 0.9771 |
| stall_recall | 0.8846 |
| slope_recall | 0.9473 |
| uphill_recall | 0.8237 |
| downhill_recall | 0.7314 |

- best_epoch: 39
- train_seconds: 94.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 8 | 0.6250 | 0.5650 |
| [0.60,0.70) | 13 | 0.6923 | 0.6411 |
| [0.70,0.80) | 11 | 0.2727 | 0.7643 |
| [0.80,0.90) | 35 | 0.2571 | 0.8591 |
| [0.90,1.00) | 1825 | 0.0208 | 0.9962 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 38 | 0.4474 | 0.5509 |
| [0.60,0.70) | 50 | 0.3400 | 0.6453 |
| [0.70,0.80) | 77 | 0.2857 | 0.7583 |
| [0.80,0.90) | 93 | 0.2043 | 0.8585 |
| [0.90,1.00) | 1634 | 0.0379 | 0.9871 |


## 验证集最佳点

```json
{
  "loss_total": 0.4069914986559306,
  "acc_main": 0.9686552072800809,
  "acc_turn": 0.9307381193124368,
  "acc_turn_pure": 0.9518201284796574,
  "acc_turn_transition": 0.5727272727272728,
  "flat_recall": 0.9877216916780355,
  "stall_recall": 0.8939393939393939,
  "slope_recall": 0.9170403587443946,
  "recall_main": [
    0.9877216916780355,
    0.8939393939393939,
    0.9170403587443946
  ],
  "turn_right_recall": 0.9376770538243626,
  "turn_straight_recall": 0.9434447300771208,
  "turn_left_recall": 0.8930131004366813,
  "recall_turn": [
    0.9376770538243626,
    0.9434447300771208,
    0.8930131004366813
  ],
  "cm_turn": [
    [
      331,
      13,
      9
    ],
    [
      47,
      1101,
      19
    ],
    [
      2,
      47,
      409
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1448,
      1,
      17
    ],
    [
      5,
      59,
      2
    ],
    [
      36,
      1,
      409
    ]
  ],
  "main_confidence_mean": 0.9890309029524331,
  "main_confidence_error_mean": 0.9094842077192884,
  "main_low_conf_0p60_ratio": 0.008594539939332659,
  "main_low_conf_0p70_ratio": 0.014661274014155713,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 17,
      "error_rate": 0.23529411764705882,
      "mean_confidence": 0.5413656539240366
    },
    {
      "bin": "[0.60,0.70)",
      "n": 12,
      "error_rate": 0.25,
      "mean_confidence": 0.6533667090888787
    },
    {
      "bin": "[0.70,0.80)",
      "n": 14,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7432842091777293
    },
    {
      "bin": "[0.80,0.90)",
      "n": 21,
      "error_rate": 0.19047619047619047,
      "mean_confidence": 0.8596831065585736
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1914,
      "error_rate": 0.023510971786833857,
      "mean_confidence": 0.998328205458683
    }
  ],
  "turn_confidence_mean": 0.952316281271193,
  "turn_confidence_error_mean": 0.8434572557151756,
  "turn_low_conf_0p60_ratio": 0.024266936299292215,
  "turn_low_conf_0p70_ratio": 0.04499494438827098,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 48,
      "error_rate": 0.4375,
      "mean_confidence": 0.538982589692773
    },
    {
      "bin": "[0.60,0.70)",
      "n": 41,
      "error_rate": 0.24390243902439024,
      "mean_confidence": 0.6473568570394312
    },
    {
      "bin": "[0.70,0.80)",
      "n": 74,
      "error_rate": 0.17567567567567569,
      "mean_confidence": 0.7607306384660606
    },
    {
      "bin": "[0.80,0.90)",
      "n": 136,
      "error_rate": 0.16176470588235295,
      "mean_confidence": 0.8628652169743899
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1679,
      "error_rate": 0.04228707564026206,
      "mean_confidence": 0.9872692508371321
    }
  ],
  "theta_mae_rad": 0.015619223937392235,
  "theta_mae_deg": 0.8949155807495117,
  "uphill_recall": 0.8395904436860068,
  "downhill_recall": 0.6949152542372882,
  "slope_sign_acc": 0.24790794979079497,
  "theta_flat_mae_deg": 0.8632842898368835,
  "theta_flat_abs_p95_deg": 3.0722897052764893,
  "theta_flat_bias_deg": -0.08177754282951355,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.8909524083137512,
  "theta_near_flat_abs_p95_deg": 3.264249801635742,
  "theta_near_flat_bias_deg": -0.045704394578933716,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 0.938228964805603,
  "theta_flat_turn_abs_p95_deg": 2.68554425239563,
  "theta_flat_turn_bias_deg": -0.4272702634334564,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.8949155807495117,
  "theta_slope_control_abs_p95_deg": 5.679596424102783,
  "theta_slope_control_bias_deg": -0.09041894972324371,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 0.8949155807495117,
  "theta_abs_le_8_rmse_deg": 1.6201711893081665,
  "theta_abs_le_8_p95_abs_err_deg": 3.168809175491333,
  "theta_abs_le_8_bias_deg": -0.09041894227266312,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.8949155807495117,
  "theta_abs_le_10_rmse_deg": 1.6201711893081665,
  "theta_abs_le_10_p95_abs_err_deg": 3.168809175491333,
  "theta_abs_le_10_bias_deg": -0.09041894227266312,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7137492895126343,
  "theta_pos_6_8_rmse_deg": 0.853964626789093,
  "theta_pos_6_8_p95_abs_err_deg": 1.5744818449020386,
  "theta_pos_6_8_bias_deg": -0.4447973668575287,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.617564857006073,
  "theta_neg_8_6_rmse_deg": 0.8179137706756592,
  "theta_neg_8_6_p95_abs_err_deg": 1.5919907093048096,
  "theta_neg_8_6_bias_deg": -0.5336816906929016,
  "theta_neg_8_6_n": 47.0
}
```
