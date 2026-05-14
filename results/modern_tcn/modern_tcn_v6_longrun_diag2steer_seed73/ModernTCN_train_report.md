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
| acc_main | 0.9725 |
| acc_turn | 0.9308 |
| acc_turn_pure | 0.9455 |
| acc_turn_transition | 0.6452 |
| main_confidence_mean | 0.9907 |
| main_low_conf_0p60_ratio | 0.0042 |
| main_low_conf_0p70_ratio | 0.0116 |
| turn_confidence_mean | 0.9447 |
| turn_low_conf_0p60_ratio | 0.0254 |
| turn_low_conf_0p70_ratio | 0.0460 |
| turn_right_recall | 0.9088 |
| turn_straight_recall | 0.9566 |
| turn_left_recall | 0.8656 |
| theta_mae_deg | 1.1464 |
| theta_flat_abs_p95_deg | 5.2122 |
| theta_flat_bias_deg | -0.5779 |
| theta_near_flat_abs_p95_deg | 5.9879 |
| theta_near_flat_bias_deg | -0.4793 |
| theta_flat_turn_abs_p95_deg | 3.6997 |
| flat_recall | 0.9924 |
| stall_recall | 0.8846 |
| slope_recall | 0.9322 |
| uphill_recall | 0.8127 |
| downhill_recall | 0.7208 |

- best_epoch: 29
- train_seconds: 80.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 8 | 0.3750 | 0.5415 |
| [0.60,0.70) | 14 | 0.5000 | 0.6555 |
| [0.70,0.80) | 14 | 0.2857 | 0.7612 |
| [0.80,0.90) | 12 | 0.0833 | 0.8669 |
| [0.90,1.00) | 1844 | 0.0201 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 48 | 0.3750 | 0.5474 |
| [0.60,0.70) | 39 | 0.4872 | 0.6489 |
| [0.70,0.80) | 79 | 0.1519 | 0.7578 |
| [0.80,0.90) | 201 | 0.0697 | 0.8490 |
| [0.90,1.00) | 1525 | 0.0446 | 0.9871 |


## 验证集最佳点

```json
{
  "loss_total": 0.4690763991932536,
  "acc_main": 0.9701718907987866,
  "acc_turn": 0.9261880687563195,
  "acc_turn_pure": 0.9480728051391863,
  "acc_turn_transition": 0.5545454545454546,
  "flat_recall": 0.990450204638472,
  "stall_recall": 0.9090909090909091,
  "slope_recall": 0.9125560538116592,
  "recall_main": [
    0.990450204638472,
    0.9090909090909091,
    0.9125560538116592
  ],
  "turn_right_recall": 0.9263456090651558,
  "turn_straight_recall": 0.9468723221936589,
  "turn_left_recall": 0.8733624454148472,
  "recall_turn": [
    0.9263456090651558,
    0.9468723221936589,
    0.8733624454148472
  ],
  "cm_turn": [
    [
      327,
      16,
      10
    ],
    [
      42,
      1105,
      20
    ],
    [
      5,
      53,
      400
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1452,
      5,
      9
    ],
    [
      6,
      60,
      0
    ],
    [
      39,
      0,
      407
    ]
  ],
  "main_confidence_mean": 0.9940066106577572,
  "main_confidence_error_mean": 0.9297184865558102,
  "main_low_conf_0p60_ratio": 0.0025278058645096056,
  "main_low_conf_0p70_ratio": 0.00455005055611729,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 5,
      "error_rate": 0.2,
      "mean_confidence": 0.5259437421650108
    },
    {
      "bin": "[0.60,0.70)",
      "n": 4,
      "error_rate": 1.0,
      "mean_confidence": 0.6443406044730234
    },
    {
      "bin": "[0.70,0.80)",
      "n": 7,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7670548083538071
    },
    {
      "bin": "[0.80,0.90)",
      "n": 17,
      "error_rate": 0.4117647058823529,
      "mean_confidence": 0.8482356928667022
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1945,
      "error_rate": 0.02262210796915167,
      "mean_confidence": 0.9980198479769234
    }
  ],
  "turn_confidence_mean": 0.9452892593823492,
  "turn_confidence_error_mean": 0.8225814097611683,
  "turn_low_conf_0p60_ratio": 0.023255813953488372,
  "turn_low_conf_0p70_ratio": 0.04903943377148635,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 46,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.5392925937377102
    },
    {
      "bin": "[0.60,0.70)",
      "n": 51,
      "error_rate": 0.37254901960784315,
      "mean_confidence": 0.645877551727019
    },
    {
      "bin": "[0.70,0.80)",
      "n": 95,
      "error_rate": 0.1368421052631579,
      "mean_confidence": 0.7576797916242609
    },
    {
      "bin": "[0.80,0.90)",
      "n": 164,
      "error_rate": 0.17682926829268292,
      "mean_confidence": 0.8595442987018209
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1622,
      "error_rate": 0.03884093711467324,
      "mean_confidence": 0.9858755212187856
    }
  ],
  "theta_mae_rad": 0.01874096877872944,
  "theta_mae_deg": 1.0737783908843994,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.6822033898305084,
  "slope_sign_acc": 0.25889121338912136,
  "theta_flat_mae_deg": 1.0491257905960083,
  "theta_flat_abs_p95_deg": 4.7495622634887695,
  "theta_flat_bias_deg": -0.5045086145401001,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 1.1361020803451538,
  "theta_near_flat_abs_p95_deg": 5.802237033843994,
  "theta_near_flat_bias_deg": -0.34427863359451294,
  "theta_near_flat_n": 1472.0,
  "theta_flat_turn_mae_deg": 1.0929696559906006,
  "theta_flat_turn_abs_p95_deg": 2.7647008895874023,
  "theta_flat_turn_bias_deg": -0.5416505932807922,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 1.0737783908843994,
  "theta_slope_control_abs_p95_deg": 7.092069625854492,
  "theta_slope_control_bias_deg": -0.48470988869667053,
  "theta_slope_control_n": 1912.0,
  "theta_abs_le_8_mae_deg": 1.073778510093689,
  "theta_abs_le_8_rmse_deg": 2.3180344104766846,
  "theta_abs_le_8_p95_abs_err_deg": 4.200875282287598,
  "theta_abs_le_8_bias_deg": -0.48470988869667053,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 1.073778510093689,
  "theta_abs_le_10_rmse_deg": 2.3180344104766846,
  "theta_abs_le_10_p95_abs_err_deg": 4.200875282287598,
  "theta_abs_le_10_bias_deg": -0.48470988869667053,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.7286309003829956,
  "theta_pos_6_8_rmse_deg": 1.7668789625167847,
  "theta_pos_6_8_p95_abs_err_deg": 1.947351336479187,
  "theta_pos_6_8_bias_deg": 0.48214131593704224,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.6907050609588623,
  "theta_neg_8_6_rmse_deg": 0.8022173047065735,
  "theta_neg_8_6_p95_abs_err_deg": 1.3969972133636475,
  "theta_neg_8_6_bias_deg": -0.02168158069252968,
  "theta_neg_8_6_n": 47.0
}
```
