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
| acc_main | 0.9559 |
| acc_turn | 0.5666 |
| acc_turn_pure | 0.5759 |
| acc_turn_transition | 0.5261 |
| main_confidence_mean | 0.9852 |
| main_low_conf_0p60_ratio | 0.0039 |
| main_low_conf_0p70_ratio | 0.0108 |
| turn_confidence_mean | 0.7815 |
| turn_low_conf_0p60_ratio | 0.2215 |
| turn_low_conf_0p70_ratio | 0.3434 |
| turn_right_recall | 0.5569 |
| turn_straight_recall | 0.5246 |
| turn_left_recall | 0.6690 |
| theta_mae_deg | 0.7047 |
| theta_abs_le_10_p95_abs_err_deg | 2.1137 |
| theta_neg_10_8_p95_abs_err_deg | 1.6670 |
| theta_pos_8_10_p95_abs_err_deg | 3.7122 |
| theta_abs_le_8_p95_abs_err_deg | 1.9665 |
| theta_neg_8_6_p95_abs_err_deg | 1.2921 |
| theta_pos_6_8_p95_abs_err_deg | 1.8879 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6770 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6860 |
| theta_flat_abs_p95_deg | 2.9073 |
| theta_flat_bias_deg | 0.1566 |
| theta_near_flat_abs_p95_deg | 1.8471 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2689 |
| theta_flat_turn_abs_p95_deg | 1.5182 |
| flat_recall | 0.9511 |
| stall_recall | 0.6458 |
| slope_recall | 0.9680 |
| uphill_recall | 0.7420 |
| downhill_recall | 0.7968 |

- best_epoch: 46
- train_seconds: 662.5

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 14 | 0.6429 | 0.5391 |
| [0.60,0.70) | 25 | 0.5200 | 0.6537 |
| [0.70,0.80) | 43 | 0.3488 | 0.7454 |
| [0.80,0.90) | 84 | 0.2143 | 0.8555 |
| [0.90,1.00) | 3436 | 0.0303 | 0.9956 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 798 | 0.5514 | 0.5142 |
| [0.60,0.70) | 439 | 0.5672 | 0.6510 |
| [0.70,0.80) | 504 | 0.5615 | 0.7506 |
| [0.80,0.90) | 541 | 0.4750 | 0.8501 |
| [0.90,1.00) | 1320 | 0.2515 | 0.9701 |


## 验证集最佳点

```json
{
  "loss_total": 0.5801391962255289,
  "acc_main": 0.9442489851150203,
  "acc_turn": 0.6259810554803789,
  "acc_turn_pure": 0.6394624713208784,
  "acc_turn_transition": 0.562111801242236,
  "flat_recall": 0.9665144596651446,
  "stall_recall": 0.30952380952380953,
  "slope_recall": 0.94826435246996,
  "recall_main": [
    0.9665144596651446,
    0.30952380952380953,
    0.94826435246996
  ],
  "turn_right_recall": 0.6907582938388626,
  "turn_straight_recall": 0.5265072765072765,
  "turn_left_recall": 0.7734627831715211,
  "recall_turn": [
    0.6907582938388626,
    0.5265072765072765,
    0.7734627831715211
  ],
  "cm_turn": [
    [
      583,
      167,
      94
    ],
    [
      398,
      1013,
      513
    ],
    [
      77,
      133,
      717
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      635,
      0,
      22
    ],
    [
      5,
      13,
      24
    ],
    [
      149,
      6,
      2841
    ]
  ],
  "main_confidence_mean": 0.9662522632270787,
  "main_confidence_error_mean": 0.7671216542286925,
  "main_low_conf_0p60_ratio": 0.05006765899864682,
  "main_low_conf_0p70_ratio": 0.05737483085250338,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 185,
      "error_rate": 0.4594594594594595,
      "mean_confidence": 0.5521896758837845
    },
    {
      "bin": "[0.60,0.70)",
      "n": 27,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.6324821725847691
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.2222222222222222,
      "mean_confidence": 0.7528664277321137
    },
    {
      "bin": "[0.80,0.90)",
      "n": 73,
      "error_rate": 0.2602739726027397,
      "mean_confidence": 0.8542923607331486
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3383,
      "error_rate": 0.024830032515518772,
      "mean_confidence": 0.9956781755966538
    }
  ],
  "turn_confidence_mean": 0.8107579052828786,
  "turn_confidence_error_mean": 0.7503868946435287,
  "turn_low_conf_0p60_ratio": 0.17347767253044655,
  "turn_low_conf_0p70_ratio": 0.29039242219215156,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 641,
      "error_rate": 0.5585023400936038,
      "mean_confidence": 0.5045389283957973
    },
    {
      "bin": "[0.60,0.70)",
      "n": 432,
      "error_rate": 0.46296296296296297,
      "mean_confidence": 0.64979660539409
    },
    {
      "bin": "[0.70,0.80)",
      "n": 452,
      "error_rate": 0.4446902654867257,
      "mean_confidence": 0.749424469610191
    },
    {
      "bin": "[0.80,0.90)",
      "n": 514,
      "error_rate": 0.3968871595330739,
      "mean_confidence": 0.8521299104226853
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1656,
      "error_rate": 0.2530193236714976,
      "mean_confidence": 0.9751776806565319
    }
  ],
  "theta_mae_rad": 0.014082370325922966,
  "theta_mae_deg": 0.8068603277206421,
  "uphill_recall": 0.7757412398921832,
  "downhill_recall": 0.7919911012235817,
  "slope_sign_acc": 0.9679715302491103,
  "theta_flat_mae_deg": 1.0474138259887695,
  "theta_flat_abs_p95_deg": 3.88291072845459,
  "theta_flat_abs_max_deg": 6.888908863067627,
  "theta_flat_bias_deg": 0.6387314796447754,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.378182291984558,
  "theta_near_flat_abs_p95_deg": 4.198488235473633,
  "theta_near_flat_abs_max_deg": 6.428531646728516,
  "theta_near_flat_bias_deg": 1.0307445526123047,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9034156203269958,
  "theta_flat_turn_abs_p95_deg": 3.88291072845459,
  "theta_flat_turn_abs_max_deg": 5.799920082092285,
  "theta_flat_turn_bias_deg": 0.4330110251903534,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8068603277206421,
  "theta_slope_control_abs_p95_deg": 9.369370460510254,
  "theta_slope_control_abs_max_deg": 12.143047332763672,
  "theta_slope_control_bias_deg": 0.04273369908332825,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8068603873252869,
  "theta_all_rmse_deg": 1.1992464065551758,
  "theta_all_p95_abs_err_deg": 2.625786781311035,
  "theta_all_max_abs_err_deg": 8.72496509552002,
  "theta_all_bias_deg": 0.04273369535803795,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7541088461875916,
  "theta_active_abs_ge_2_rmse_deg": 1.0890239477157593,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.1776609420776367,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.72496509552002,
  "theta_active_abs_ge_2_bias_deg": -0.08796408772468567,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8223461508750916,
  "theta_abs_le_8_rmse_deg": 1.214761734008789,
  "theta_abs_le_8_p95_abs_err_deg": 2.8326568603515625,
  "theta_abs_le_8_max_abs_err_deg": 7.397377014160156,
  "theta_abs_le_8_bias_deg": 0.10669850558042526,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8068603873252869,
  "theta_abs_le_10_rmse_deg": 1.1992464065551758,
  "theta_abs_le_10_p95_abs_err_deg": 2.625786781311035,
  "theta_abs_le_10_max_abs_err_deg": 8.72496509552002,
  "theta_abs_le_10_bias_deg": 0.04273369535803795,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6711716055870056,
  "theta_pos_8_10_rmse_deg": 0.8391994833946228,
  "theta_pos_8_10_p95_abs_err_deg": 1.628462314605713,
  "theta_pos_8_10_max_abs_err_deg": 2.9371237754821777,
  "theta_pos_8_10_bias_deg": -0.36037373542785645,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8131097555160522,
  "theta_neg_10_8_rmse_deg": 1.3660448789596558,
  "theta_neg_10_8_p95_abs_err_deg": 2.6213176250457764,
  "theta_neg_10_8_max_abs_err_deg": 8.72496509552002,
  "theta_neg_10_8_bias_deg": -0.09153472632169724,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6050900816917419,
  "theta_pos_6_8_rmse_deg": 0.8472057580947876,
  "theta_pos_6_8_p95_abs_err_deg": 1.7243409156799316,
  "theta_pos_6_8_max_abs_err_deg": 3.99257493019104,
  "theta_pos_6_8_bias_deg": -0.13231100142002106,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7595206499099731,
  "theta_neg_8_6_rmse_deg": 1.1154865026474,
  "theta_neg_8_6_p95_abs_err_deg": 2.024585008621216,
  "theta_neg_8_6_max_abs_err_deg": 7.397377014160156,
  "theta_neg_8_6_bias_deg": -0.23416855931282043,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6823538541793823,
  "theta_neg_4_2_rmse_deg": 0.910836935043335,
  "theta_neg_4_2_p95_abs_err_deg": 1.8061429262161255,
  "theta_neg_4_2_max_abs_err_deg": 4.239141941070557,
  "theta_neg_4_2_bias_deg": -0.10713290423154831,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7297616600990295,
  "theta_neg_2_0p5_rmse_deg": 0.9481222629547119,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.554114580154419,
  "theta_neg_2_0p5_max_abs_err_deg": 5.180195331573486,
  "theta_neg_2_0p5_bias_deg": 0.3454630672931671,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.014308214187622,
  "theta_pos_0p5_2_rmse_deg": 1.4248591661453247,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.38291072845459,
  "theta_pos_0p5_2_max_abs_err_deg": 5.116936206817627,
  "theta_pos_0p5_2_bias_deg": 0.48697590827941895,
  "theta_pos_0p5_2_n": 163.0
}
```
