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
  "lambda_turn": 0.22,
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
    1.45,
    0.75,
    1.45
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.8,
  "select_turn_weight": 0.62,
  "select_turn_transition_weight": 1.35,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.7,
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
| acc_main | 0.9620 |
| acc_turn | 0.5847 |
| acc_turn_pure | 0.6015 |
| acc_turn_transition | 0.5112 |
| main_confidence_mean | 0.9875 |
| main_low_conf_0p60_ratio | 0.0069 |
| main_low_conf_0p70_ratio | 0.0130 |
| turn_confidence_mean | 0.8195 |
| turn_low_conf_0p60_ratio | 0.1710 |
| turn_low_conf_0p70_ratio | 0.2773 |
| turn_right_recall | 0.6458 |
| turn_straight_recall | 0.5654 |
| turn_left_recall | 0.5713 |
| theta_mae_deg | 0.6268 |
| theta_abs_le_10_p95_abs_err_deg | 1.7539 |
| theta_neg_10_8_p95_abs_err_deg | 1.5187 |
| theta_pos_8_10_p95_abs_err_deg | 2.0985 |
| theta_abs_le_8_p95_abs_err_deg | 1.6990 |
| theta_neg_8_6_p95_abs_err_deg | 1.6824 |
| theta_pos_6_8_p95_abs_err_deg | 1.5005 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.9398 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7760 |
| theta_flat_abs_p95_deg | 2.7566 |
| theta_flat_bias_deg | 0.5803 |
| theta_near_flat_abs_p95_deg | 2.2990 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.6685 |
| theta_flat_turn_abs_p95_deg | 1.9003 |
| flat_recall | 0.9471 |
| stall_recall | 0.6354 |
| slope_recall | 0.9775 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.8002 |

- best_epoch: 65
- train_seconds: 912.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 25 | 0.4000 | 0.5367 |
| [0.60,0.70) | 22 | 0.4091 | 0.6521 |
| [0.70,0.80) | 27 | 0.3333 | 0.7444 |
| [0.80,0.90) | 67 | 0.4478 | 0.8560 |
| [0.90,1.00) | 3461 | 0.0228 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 616 | 0.5893 | 0.5183 |
| [0.60,0.70) | 383 | 0.5300 | 0.6488 |
| [0.70,0.80) | 423 | 0.4515 | 0.7494 |
| [0.80,0.90) | 480 | 0.4479 | 0.8510 |
| [0.90,1.00) | 1700 | 0.3082 | 0.9758 |


## 验证集最佳点

```json
{
  "loss_total": 0.6677317672395254,
  "acc_main": 0.9382949932341001,
  "acc_turn": 0.6346414073071719,
  "acc_turn_pure": 0.6492953130121272,
  "acc_turn_transition": 0.5652173913043478,
  "flat_recall": 0.943683409436834,
  "stall_recall": 0.23809523809523808,
  "slope_recall": 0.9469292389853138,
  "recall_main": [
    0.943683409436834,
    0.23809523809523808,
    0.9469292389853138
  ],
  "turn_right_recall": 0.7251184834123223,
  "turn_straight_recall": 0.5748440748440748,
  "turn_left_recall": 0.6763754045307443,
  "recall_turn": [
    0.7251184834123223,
    0.5748440748440748,
    0.6763754045307443
  ],
  "cm_turn": [
    [
      612,
      179,
      53
    ],
    [
      456,
      1106,
      362
    ],
    [
      113,
      187,
      627
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      620,
      0,
      37
    ],
    [
      9,
      10,
      23
    ],
    [
      153,
      6,
      2837
    ]
  ],
  "main_confidence_mean": 0.9675070232915477,
  "main_confidence_error_mean": 0.7732919414008197,
  "main_low_conf_0p60_ratio": 0.05331529093369418,
  "main_low_conf_0p70_ratio": 0.06359945872801083,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 197,
      "error_rate": 0.467005076142132,
      "mean_confidence": 0.5896435781095484
    },
    {
      "bin": "[0.60,0.70)",
      "n": 38,
      "error_rate": 0.42105263157894735,
      "mean_confidence": 0.6460203159002922
    },
    {
      "bin": "[0.70,0.80)",
      "n": 34,
      "error_rate": 0.4117647058823529,
      "mean_confidence": 0.7535680760570235
    },
    {
      "bin": "[0.80,0.90)",
      "n": 59,
      "error_rate": 0.3389830508474576,
      "mean_confidence": 0.8539793592323922
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3367,
      "error_rate": 0.025542025542025542,
      "mean_confidence": 0.9973934652182437
    }
  ],
  "turn_confidence_mean": 0.837111128192922,
  "turn_confidence_error_mean": 0.7647036576308657,
  "turn_low_conf_0p60_ratio": 0.18051420838971582,
  "turn_low_conf_0p70_ratio": 0.260893098782138,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 667,
      "error_rate": 0.6101949025487257,
      "mean_confidence": 0.5227303701452568
    },
    {
      "bin": "[0.60,0.70)",
      "n": 297,
      "error_rate": 0.4107744107744108,
      "mean_confidence": 0.6504914111291399
    },
    {
      "bin": "[0.70,0.80)",
      "n": 321,
      "error_rate": 0.4984423676012461,
      "mean_confidence": 0.7511857353727323
    },
    {
      "bin": "[0.80,0.90)",
      "n": 398,
      "error_rate": 0.40954773869346733,
      "mean_confidence": 0.8501959558123662
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2012,
      "error_rate": 0.24751491053677932,
      "mean_confidence": 0.9799999509009133
    }
  ],
  "theta_mae_rad": 0.013084783218801022,
  "theta_mae_deg": 0.7497028112411499,
  "uphill_recall": 0.7735849056603774,
  "downhill_recall": 0.800333704115684,
  "slope_sign_acc": 0.9592116068984397,
  "theta_flat_mae_deg": 1.139713168144226,
  "theta_flat_abs_p95_deg": 3.9343996047973633,
  "theta_flat_abs_max_deg": 7.651749610900879,
  "theta_flat_bias_deg": 0.7492735385894775,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6013224124908447,
  "theta_near_flat_abs_p95_deg": 4.158894062042236,
  "theta_near_flat_abs_max_deg": 7.651749610900879,
  "theta_near_flat_bias_deg": 1.149903655052185,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2045313119888306,
  "theta_flat_turn_abs_p95_deg": 3.9343996047973633,
  "theta_flat_turn_abs_max_deg": 7.651749610900879,
  "theta_flat_turn_bias_deg": 0.4301914572715759,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7497028112411499,
  "theta_slope_control_abs_p95_deg": 9.259808540344238,
  "theta_slope_control_abs_max_deg": 11.977361679077148,
  "theta_slope_control_bias_deg": 0.19833770394325256,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7497028112411499,
  "theta_all_rmse_deg": 1.1880284547805786,
  "theta_all_p95_abs_err_deg": 2.6943628787994385,
  "theta_all_max_abs_err_deg": 7.562887191772461,
  "theta_all_bias_deg": 0.19833770394325256,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6641765236854553,
  "theta_active_abs_ge_2_rmse_deg": 1.0555429458618164,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2239444255828857,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.562887191772461,
  "theta_active_abs_ge_2_bias_deg": 0.07752168923616409,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7798556089401245,
  "theta_abs_le_8_rmse_deg": 1.2297672033309937,
  "theta_abs_le_8_p95_abs_err_deg": 2.840944528579712,
  "theta_abs_le_8_max_abs_err_deg": 7.429628372192383,
  "theta_abs_le_8_bias_deg": 0.2859724760055542,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7497028112411499,
  "theta_abs_le_10_rmse_deg": 1.1880284547805786,
  "theta_abs_le_10_p95_abs_err_deg": 2.6943628787994385,
  "theta_abs_le_10_max_abs_err_deg": 7.562887191772461,
  "theta_abs_le_10_bias_deg": 0.19833770394325256,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5756253004074097,
  "theta_pos_8_10_rmse_deg": 0.718731701374054,
  "theta_pos_8_10_p95_abs_err_deg": 1.2915433645248413,
  "theta_pos_8_10_max_abs_err_deg": 3.595661163330078,
  "theta_pos_8_10_bias_deg": -0.3756222724914551,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6701878905296326,
  "theta_neg_10_8_rmse_deg": 1.2095110416412354,
  "theta_neg_10_8_p95_abs_err_deg": 2.2162744998931885,
  "theta_neg_10_8_max_abs_err_deg": 7.562887191772461,
  "theta_neg_10_8_bias_deg": 0.03644287586212158,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.49563243985176086,
  "theta_pos_6_8_rmse_deg": 0.7222220301628113,
  "theta_pos_6_8_p95_abs_err_deg": 1.3955776691436768,
  "theta_pos_6_8_max_abs_err_deg": 3.851468324661255,
  "theta_pos_6_8_bias_deg": -0.013486447744071484,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.659162163734436,
  "theta_neg_8_6_rmse_deg": 1.0478529930114746,
  "theta_neg_8_6_p95_abs_err_deg": 1.8756110668182373,
  "theta_neg_8_6_max_abs_err_deg": 7.322230339050293,
  "theta_neg_8_6_bias_deg": 0.03858104720711708,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6710960865020752,
  "theta_neg_4_2_rmse_deg": 0.9664947390556335,
  "theta_neg_4_2_p95_abs_err_deg": 2.1412670612335205,
  "theta_neg_4_2_max_abs_err_deg": 4.94354772567749,
  "theta_neg_4_2_bias_deg": -0.010122298263013363,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.596052885055542,
  "theta_neg_2_0p5_rmse_deg": 0.8687776923179626,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5630379915237427,
  "theta_neg_2_0p5_max_abs_err_deg": 4.9265336990356445,
  "theta_neg_2_0p5_bias_deg": 0.23268994688987732,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1766531467437744,
  "theta_pos_0p5_2_rmse_deg": 1.504047155380249,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.4343996047973633,
  "theta_pos_0p5_2_max_abs_err_deg": 4.585083484649658,
  "theta_pos_0p5_2_bias_deg": 0.9053946733474731,
  "theta_pos_0p5_2_n": 163.0
}
```
