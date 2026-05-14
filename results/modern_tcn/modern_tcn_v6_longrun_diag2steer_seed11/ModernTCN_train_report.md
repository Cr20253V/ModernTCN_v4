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
| acc_main | 0.9709 |
| acc_turn | 0.9207 |
| acc_turn_pure | 0.9383 |
| acc_turn_transition | 0.5806 |
| main_confidence_mean | 0.9859 |
| main_low_conf_0p60_ratio | 0.0048 |
| main_low_conf_0p70_ratio | 0.0143 |
| turn_confidence_mean | 0.9368 |
| turn_low_conf_0p60_ratio | 0.0211 |
| turn_low_conf_0p70_ratio | 0.0544 |
| turn_right_recall | 0.9298 |
| turn_straight_recall | 0.9393 |
| turn_left_recall | 0.8553 |
| theta_mae_deg | 1.9116 |
| theta_flat_abs_p95_deg | 9.1799 |
| theta_flat_bias_deg | -1.4257 |
| theta_near_flat_abs_p95_deg | 9.7972 |
| theta_near_flat_bias_deg | -1.3513 |
| theta_flat_turn_abs_p95_deg | 5.2272 |
| flat_recall | 0.9908 |
| stall_recall | 0.8269 |
| slope_recall | 0.9360 |
| uphill_recall | 0.8099 |
| downhill_recall | 0.7314 |

- best_epoch: 18
- train_seconds: 60.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 9 | 0.2222 | 0.5247 |
| [0.60,0.70) | 18 | 0.1667 | 0.6424 |
| [0.70,0.80) | 21 | 0.4762 | 0.7433 |
| [0.80,0.90) | 26 | 0.3077 | 0.8507 |
| [0.90,1.00) | 1818 | 0.0176 | 0.9963 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 40 | 0.5000 | 0.5269 |
| [0.60,0.70) | 63 | 0.4286 | 0.6561 |
| [0.70,0.80) | 117 | 0.1966 | 0.7573 |
| [0.80,0.90) | 204 | 0.1471 | 0.8563 |
| [0.90,1.00) | 1468 | 0.0341 | 0.9855 |


## 验证集最佳点

```json
{
  "loss_total": 0.3815892749175023,
  "acc_main": 0.9696663296258847,
  "acc_turn": 0.9246713852376137,
  "acc_turn_pure": 0.9470021413276232,
  "acc_turn_transition": 0.5454545454545454,
  "flat_recall": 0.9870395634379263,
  "stall_recall": 0.9090909090909091,
  "slope_recall": 0.92152466367713,
  "recall_main": [
    0.9870395634379263,
    0.9090909090909091,
    0.92152466367713
  ],
  "turn_right_recall": 0.9235127478753541,
  "turn_straight_recall": 0.9443016281062554,
  "turn_left_recall": 0.8755458515283843,
  "recall_turn": [
    0.9235127478753541,
    0.9443016281062554,
    0.8755458515283843
  ],
  "cm_turn": [
    [
      326,
      15,
      12
    ],
    [
      48,
      1102,
      17
    ],
    [
      6,
      51,
      401
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1447,
      10,
      9
    ],
    [
      5,
      60,
      1
    ],
    [
      35,
      0,
      411
    ]
  ],
  "main_confidence_mean": 0.9861580129545694,
  "main_confidence_error_mean": 0.8707057091062624,
  "main_low_conf_0p60_ratio": 0.010111223458038422,
  "main_low_conf_0p70_ratio": 0.01769464105156724,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 20,
      "error_rate": 0.35,
      "mean_confidence": 0.5376744095430829
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6452925654664131
    },
    {
      "bin": "[0.70,0.80)",
      "n": 12,
      "error_rate": 0.4166666666666667,
      "mean_confidence": 0.7487444612428352
    },
    {
      "bin": "[0.80,0.90)",
      "n": 19,
      "error_rate": 0.2631578947368421,
      "mean_confidence": 0.8470646604334522
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1912,
      "error_rate": 0.0198744769874477,
      "mean_confidence": 0.9963956646799847
    }
  ],
  "turn_confidence_mean": 0.9406086988910144,
  "turn_confidence_error_mean": 0.8251913036579889,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.04398382204246714,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.5135135135135135,
      "mean_confidence": 0.5315274461700119
    },
    {
      "bin": "[0.60,0.70)",
      "n": 50,
      "error_rate": 0.26,
      "mean_confidence": 0.6491357147460924
    },
    {
      "bin": "[0.70,0.80)",
      "n": 97,
      "error_rate": 0.21649484536082475,
      "mean_confidence": 0.7537421799052697
    },
    {
      "bin": "[0.80,0.90)",
      "n": 224,
      "error_rate": 0.15625,
      "mean_confidence": 0.8583112617184562
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1570,
      "error_rate": 0.038853503184713374,
      "mean_confidence": 0.9828191026019656
    }
  ],
  "theta_mae_rad": 0.02468201518058777,
  "theta_mae_deg": 1.414175271987915,
  "uphill_recall": 0.8498293515358362,
  "downhill_recall": 0.690677966101695,
  "slope_sign_acc": 0.25418410041841005,
  "theta_flat_mae_deg": 1.4354594945907593,
  "theta_flat_abs_p95_deg": 6.033270835876465,
  "theta_flat_bias_deg": -0.7433902025222778,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 1.4998013973236084,
  "theta_near_flat_abs_p95_deg": 6.202005386352539,
  "theta_near_flat_bias_deg": -0.6064676642417908,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 1.41650390625,
  "theta_flat_turn_abs_p95_deg": 5.127624988555908,
  "theta_flat_turn_bias_deg": -0.41097643971443176,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 1.414175271987915,
  "theta_slope_control_abs_p95_deg": 7.693970203399658,
  "theta_slope_control_bias_deg": -0.7620867490768433,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 1.414175271987915,
  "theta_abs_le_8_rmse_deg": 3.6460824012756348,
  "theta_abs_le_8_p95_abs_err_deg": 5.59003210067749,
  "theta_abs_le_8_bias_deg": -0.7620867490768433,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 1.414175271987915,
  "theta_abs_le_10_rmse_deg": 3.6460824012756348,
  "theta_abs_le_10_p95_abs_err_deg": 5.59003210067749,
  "theta_abs_le_10_bias_deg": -0.7620867490768433,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 1.0013993978500366,
  "theta_pos_6_8_rmse_deg": 1.3137811422348022,
  "theta_pos_6_8_p95_abs_err_deg": 2.7782881259918213,
  "theta_pos_6_8_bias_deg": -0.31419408321380615,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 1.0709891319274902,
  "theta_neg_8_6_rmse_deg": 1.3548873662948608,
  "theta_neg_8_6_p95_abs_err_deg": 2.2567830085754395,
  "theta_neg_8_6_bias_deg": -0.8065915107727051,
  "theta_neg_8_6_n": 47.0
}
```
