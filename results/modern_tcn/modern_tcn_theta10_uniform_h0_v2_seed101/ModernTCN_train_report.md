# ModernTCN-small 第一阶段训练报告

## 固定约束

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
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
  "lambda_turn": 0.08,
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
    1.08,
    1.0,
    1.08
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.4,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.2,
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
| acc_main | 0.9743 |
| acc_turn | 0.8958 |
| acc_turn_pure | 0.9203 |
| acc_turn_transition | 0.7495 |
| main_confidence_mean | 0.9942 |
| main_low_conf_0p60_ratio | 0.0032 |
| main_low_conf_0p70_ratio | 0.0064 |
| turn_confidence_mean | 0.9498 |
| turn_low_conf_0p60_ratio | 0.0254 |
| turn_low_conf_0p70_ratio | 0.0576 |
| turn_right_recall | 0.8954 |
| turn_straight_recall | 0.8944 |
| turn_left_recall | 0.9003 |
| theta_mae_deg | 0.2820 |
| theta_abs_le_10_p95_abs_err_deg | 0.9187 |
| theta_neg_10_8_p95_abs_err_deg | 0.8238 |
| theta_pos_8_10_p95_abs_err_deg | 1.2384 |
| theta_abs_le_8_p95_abs_err_deg | 0.8596 |
| theta_neg_8_6_p95_abs_err_deg | 0.9741 |
| theta_pos_6_8_p95_abs_err_deg | 0.4828 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.8428 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2915 |
| theta_flat_abs_p95_deg | 2.1209 |
| theta_flat_bias_deg | 0.1820 |
| theta_near_flat_abs_p95_deg | 1.0127 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2824 |
| theta_flat_turn_abs_p95_deg | 0.7023 |
| flat_recall | 0.9577 |
| stall_recall | 0.6496 |
| slope_recall | 0.9920 |
| uphill_recall | 0.8078 |
| downhill_recall | 0.7794 |

- best_epoch: 108
- train_seconds: 449.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 12 | 0.5833 | 0.5380 |
| [0.60,0.70) | 12 | 0.5000 | 0.6493 |
| [0.70,0.80) | 18 | 0.4444 | 0.7535 |
| [0.80,0.90) | 20 | 0.4000 | 0.8571 |
| [0.90,1.00) | 3671 | 0.0183 | 0.9987 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 95 | 0.3895 | 0.5485 |
| [0.60,0.70) | 120 | 0.3417 | 0.6504 |
| [0.70,0.80) | 150 | 0.3533 | 0.7519 |
| [0.80,0.90) | 225 | 0.2800 | 0.8560 |
| [0.90,1.00) | 3143 | 0.0620 | 0.9895 |


## 验证集最佳点

```json
{
  "loss_total": 0.26077965597540287,
  "acc_main": 0.9696969696969697,
  "acc_turn": 0.8247027234369007,
  "acc_turn_pure": 0.8500228623685414,
  "acc_turn_transition": 0.6928571428571428,
  "flat_recall": 0.9449901768172888,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.977571916138469,
  "recall_main": [
    0.9449901768172888,
    0.8936170212765957,
    0.977571916138469
  ],
  "turn_right_recall": 0.782051282051282,
  "turn_straight_recall": 0.8484848484848485,
  "turn_left_recall": 0.789272030651341,
  "recall_turn": [
    0.782051282051282,
    0.8484848484848485,
    0.789272030651341
  ],
  "cm_turn": [
    [
      366,
      80,
      22
    ],
    [
      141,
      1372,
      104
    ],
    [
      18,
      92,
      412
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      481,
      0,
      28
    ],
    [
      4,
      42,
      1
    ],
    [
      39,
      7,
      2005
    ]
  ],
  "main_confidence_mean": 0.9919646331511178,
  "main_confidence_error_mean": 0.8767425535642571,
  "main_low_conf_0p60_ratio": 0.004986574606827772,
  "main_low_conf_0p70_ratio": 0.010356731875719217,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 13,
      "error_rate": 0.5384615384615384,
      "mean_confidence": 0.5368150656911103
    },
    {
      "bin": "[0.60,0.70)",
      "n": 14,
      "error_rate": 0.6428571428571429,
      "mean_confidence": 0.651132985706779
    },
    {
      "bin": "[0.70,0.80)",
      "n": 13,
      "error_rate": 0.23076923076923078,
      "mean_confidence": 0.7503050960357899
    },
    {
      "bin": "[0.80,0.90)",
      "n": 21,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.8529293907945963
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2546,
      "error_rate": 0.020031421838177535,
      "mean_confidence": 0.9985435418365801
    }
  ],
  "turn_confidence_mean": 0.9396791194603573,
  "turn_confidence_error_mean": 0.8717858559403038,
  "turn_low_conf_0p60_ratio": 0.04181051016494054,
  "turn_low_conf_0p70_ratio": 0.07403145377828922,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 109,
      "error_rate": 0.4036697247706422,
      "mean_confidence": 0.539175275297083
    },
    {
      "bin": "[0.60,0.70)",
      "n": 84,
      "error_rate": 0.4642857142857143,
      "mean_confidence": 0.6496179039647063
    },
    {
      "bin": "[0.70,0.80)",
      "n": 111,
      "error_rate": 0.35135135135135137,
      "mean_confidence": 0.7514715111204686
    },
    {
      "bin": "[0.80,0.90)",
      "n": 186,
      "error_rate": 0.3387096774193548,
      "mean_confidence": 0.8522551425165191
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2117,
      "error_rate": 0.12848370335380255,
      "mean_confidence": 0.9893588385688659
    }
  ],
  "theta_mae_rad": 0.0051992773078382015,
  "theta_mae_deg": 0.2978966236114502,
  "uphill_recall": 0.7759938837920489,
  "downhill_recall": 0.8130990415335463,
  "slope_sign_acc": 0.973828125,
  "theta_flat_mae_deg": 0.3292733430862427,
  "theta_flat_abs_p95_deg": 1.9933762550354004,
  "theta_flat_abs_max_deg": 2.4246573448181152,
  "theta_flat_bias_deg": 0.26774972677230835,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.4829232096672058,
  "theta_near_flat_abs_p95_deg": 1.4535337686538696,
  "theta_near_flat_abs_max_deg": 5.77808952331543,
  "theta_near_flat_bias_deg": 0.3917752504348755,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.39269185066223145,
  "theta_flat_turn_abs_p95_deg": 1.3083560466766357,
  "theta_flat_turn_abs_max_deg": 1.4637465476989746,
  "theta_flat_turn_bias_deg": 0.33674681186676025,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.2978966236114502,
  "theta_slope_control_abs_p95_deg": 9.282870292663574,
  "theta_slope_control_abs_max_deg": 10.139668464660645,
  "theta_slope_control_bias_deg": 0.034598998725414276,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.2978966236114502,
  "theta_all_rmse_deg": 0.45985811948776245,
  "theta_all_p95_abs_err_deg": 0.8758522272109985,
  "theta_all_max_abs_err_deg": 3.3246572017669678,
  "theta_all_bias_deg": 0.034598998725414276,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.2901098132133484,
  "theta_active_abs_ge_2_rmse_deg": 0.4519384205341339,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.8730514049530029,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.309502601623535,
  "theta_active_abs_ge_2_bias_deg": -0.023262400180101395,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.29646769165992737,
  "theta_abs_le_8_rmse_deg": 0.44565194845199585,
  "theta_abs_le_8_p95_abs_err_deg": 0.86008620262146,
  "theta_abs_le_8_max_abs_err_deg": 3.3246572017669678,
  "theta_abs_le_8_bias_deg": 0.04865672439336777,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.2978966236114502,
  "theta_abs_le_10_rmse_deg": 0.45985811948776245,
  "theta_abs_le_10_p95_abs_err_deg": 0.8758522272109985,
  "theta_abs_le_10_max_abs_err_deg": 3.3246572017669678,
  "theta_abs_le_10_bias_deg": 0.034598998725414276,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.3066406846046448,
  "theta_pos_8_10_rmse_deg": 0.48522019386291504,
  "theta_pos_8_10_p95_abs_err_deg": 0.9018470048904419,
  "theta_pos_8_10_max_abs_err_deg": 2.345447063446045,
  "theta_pos_8_10_bias_deg": -0.2408154159784317,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.30044135451316833,
  "theta_neg_10_8_rmse_deg": 0.5327366590499878,
  "theta_neg_10_8_p95_abs_err_deg": 1.0932096242904663,
  "theta_neg_10_8_max_abs_err_deg": 3.309502601623535,
  "theta_neg_10_8_bias_deg": 0.18056219816207886,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.35342058539390564,
  "theta_pos_6_8_rmse_deg": 0.4410220682621002,
  "theta_pos_6_8_p95_abs_err_deg": 0.8511930704116821,
  "theta_pos_6_8_max_abs_err_deg": 1.2589912414550781,
  "theta_pos_6_8_bias_deg": -0.3044532239437103,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.27372831106185913,
  "theta_neg_8_6_rmse_deg": 0.5121215581893921,
  "theta_neg_8_6_p95_abs_err_deg": 1.3510968685150146,
  "theta_neg_8_6_max_abs_err_deg": 2.2095115184783936,
  "theta_neg_8_6_bias_deg": 0.19676871597766876,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.2547961473464966,
  "theta_neg_4_2_rmse_deg": 0.3209015727043152,
  "theta_neg_4_2_p95_abs_err_deg": 0.6511117219924927,
  "theta_neg_4_2_max_abs_err_deg": 1.0813342332839966,
  "theta_neg_4_2_bias_deg": 0.19555681943893433,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.36640629172325134,
  "theta_neg_2_0p5_rmse_deg": 0.6769067049026489,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.327232003211975,
  "theta_neg_2_0p5_max_abs_err_deg": 3.3246572017669678,
  "theta_neg_2_0p5_bias_deg": 0.3206374943256378,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.27219676971435547,
  "theta_pos_0p5_2_rmse_deg": 0.3320096433162689,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.6076510548591614,
  "theta_pos_0p5_2_max_abs_err_deg": 0.9034512639045715,
  "theta_pos_0p5_2_bias_deg": 0.23841072618961334,
  "theta_pos_0p5_2_n": 168.0
}
```
