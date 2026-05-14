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
| acc_main | 0.9730 |
| acc_turn | 0.9323 |
| acc_turn_pure | 0.9466 |
| acc_turn_transition | 0.6559 |
| main_confidence_mean | 0.9950 |
| main_low_conf_0p60_ratio | 0.0042 |
| main_low_conf_0p70_ratio | 0.0058 |
| turn_confidence_mean | 0.9522 |
| turn_low_conf_0p60_ratio | 0.0227 |
| turn_low_conf_0p70_ratio | 0.0455 |
| turn_right_recall | 0.9404 |
| turn_straight_recall | 0.9516 |
| turn_left_recall | 0.8656 |
| theta_mae_deg | 1.4446 |
| theta_flat_abs_p95_deg | 7.3057 |
| theta_flat_bias_deg | 0.7624 |
| theta_near_flat_abs_p95_deg | 9.1849 |
| theta_near_flat_bias_deg | 0.8501 |
| theta_flat_turn_abs_p95_deg | 3.2301 |
| flat_recall | 0.9969 |
| stall_recall | 0.8654 |
| slope_recall | 0.9247 |
| uphill_recall | 0.8209 |
| downhill_recall | 0.6820 |

- best_epoch: 44
- train_seconds: 96.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 8 | 0.2500 | 0.5545 |
| [0.60,0.70) | 3 | 0.0000 | 0.6573 |
| [0.70,0.80) | 5 | 0.4000 | 0.7452 |
| [0.80,0.90) | 7 | 0.4286 | 0.8577 |
| [0.90,1.00) | 1869 | 0.0235 | 0.9986 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 43 | 0.3953 | 0.5511 |
| [0.60,0.70) | 43 | 0.3256 | 0.6565 |
| [0.70,0.80) | 62 | 0.2419 | 0.7558 |
| [0.80,0.90) | 153 | 0.1307 | 0.8523 |
| [0.90,1.00) | 1591 | 0.0390 | 0.9883 |


## 验证集最佳点

```json
{
  "loss_total": 0.40047581311545066,
  "acc_main": 0.974721941354904,
  "acc_turn": 0.9317492416582407,
  "acc_turn_pure": 0.9518201284796574,
  "acc_turn_transition": 0.5909090909090909,
  "flat_recall": 0.9918144611186903,
  "stall_recall": 0.9090909090909091,
  "slope_recall": 0.9282511210762332,
  "recall_main": [
    0.9918144611186903,
    0.9090909090909091,
    0.9282511210762332
  ],
  "turn_right_recall": 0.943342776203966,
  "turn_straight_recall": 0.9494430162810625,
  "turn_left_recall": 0.8777292576419214,
  "recall_turn": [
    0.943342776203966,
    0.9494430162810625,
    0.8777292576419214
  ],
  "cm_turn": [
    [
      333,
      15,
      5
    ],
    [
      43,
      1108,
      16
    ],
    [
      4,
      52,
      402
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1454,
      6,
      6
    ],
    [
      5,
      60,
      1
    ],
    [
      32,
      0,
      414
    ]
  ],
  "main_confidence_mean": 0.994822318726753,
  "main_confidence_error_mean": 0.9185437119338202,
  "main_low_conf_0p60_ratio": 0.003033367037411527,
  "main_low_conf_0p70_ratio": 0.006066734074823054,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 6,
      "error_rate": 0.5,
      "mean_confidence": 0.5475136222841795
    },
    {
      "bin": "[0.60,0.70)",
      "n": 6,
      "error_rate": 0.5,
      "mean_confidence": 0.6520629611375949
    },
    {
      "bin": "[0.70,0.80)",
      "n": 9,
      "error_rate": 0.2222222222222222,
      "mean_confidence": 0.7802212908265067
    },
    {
      "bin": "[0.80,0.90)",
      "n": 9,
      "error_rate": 0.5555555555555556,
      "mean_confidence": 0.8641535068572266
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1948,
      "error_rate": 0.018993839835728953,
      "mean_confidence": 0.998850982423939
    }
  ],
  "turn_confidence_mean": 0.9540632929570733,
  "turn_confidence_error_mean": 0.8393136285843956,
  "turn_low_conf_0p60_ratio": 0.017189079878665317,
  "turn_low_conf_0p70_ratio": 0.03640040444893832,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 34,
      "error_rate": 0.5,
      "mean_confidence": 0.5394179897485429
    },
    {
      "bin": "[0.60,0.70)",
      "n": 38,
      "error_rate": 0.3157894736842105,
      "mean_confidence": 0.6498999949890455
    },
    {
      "bin": "[0.70,0.80)",
      "n": 66,
      "error_rate": 0.25757575757575757,
      "mean_confidence": 0.7625322077822366
    },
    {
      "bin": "[0.80,0.90)",
      "n": 179,
      "error_rate": 0.1452513966480447,
      "mean_confidence": 0.8521797140969031
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1661,
      "error_rate": 0.037928958458759786,
      "mean_confidence": 0.988099631228828
    }
  ],
  "theta_mae_rad": 0.020162135362625122,
  "theta_mae_deg": 1.155205249786377,
  "uphill_recall": 0.8430034129692833,
  "downhill_recall": 0.7076271186440678,
  "slope_sign_acc": 0.24790794979079497,
  "theta_flat_mae_deg": 1.1555289030075073,
  "theta_flat_abs_p95_deg": 3.773350954055786,
  "theta_flat_bias_deg": 0.5177584290504456,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 1.1880806684494019,
  "theta_near_flat_abs_p95_deg": 4.59082555770874,
  "theta_near_flat_bias_deg": 0.5801288485527039,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 1.0336624383926392,
  "theta_flat_turn_abs_p95_deg": 2.8527164459228516,
  "theta_flat_turn_bias_deg": 0.3248565196990967,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 1.155205249786377,
  "theta_slope_control_abs_p95_deg": 5.647519111633301,
  "theta_slope_control_bias_deg": 0.49352338910102844,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 1.155205249786377,
  "theta_abs_le_8_rmse_deg": 2.8385043144226074,
  "theta_abs_le_8_p95_abs_err_deg": 3.461005687713623,
  "theta_abs_le_8_bias_deg": 0.49352341890335083,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 1.155205249786377,
  "theta_abs_le_10_rmse_deg": 2.8385043144226074,
  "theta_abs_le_10_p95_abs_err_deg": 3.461005687713623,
  "theta_abs_le_10_bias_deg": 0.49352341890335083,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 1.0953582525253296,
  "theta_pos_6_8_rmse_deg": 1.2332053184509277,
  "theta_pos_6_8_p95_abs_err_deg": 2.228229284286499,
  "theta_pos_6_8_bias_deg": -0.8761202096939087,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 1.439180850982666,
  "theta_neg_8_6_rmse_deg": 1.615347981452942,
  "theta_neg_8_6_p95_abs_err_deg": 2.6046979427337646,
  "theta_neg_8_6_bias_deg": 1.4389629364013672,
  "theta_neg_8_6_n": 47.0
}
```
