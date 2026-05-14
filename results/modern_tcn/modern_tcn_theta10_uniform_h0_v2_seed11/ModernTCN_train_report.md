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
| acc_main | 0.9794 |
| acc_turn | 0.8931 |
| acc_turn_pure | 0.9162 |
| acc_turn_transition | 0.7551 |
| main_confidence_mean | 0.9957 |
| main_low_conf_0p60_ratio | 0.0024 |
| main_low_conf_0p70_ratio | 0.0051 |
| turn_confidence_mean | 0.9607 |
| turn_low_conf_0p60_ratio | 0.0246 |
| turn_low_conf_0p70_ratio | 0.0485 |
| turn_right_recall | 0.9004 |
| turn_straight_recall | 0.8976 |
| turn_left_recall | 0.8716 |
| theta_mae_deg | 0.2700 |
| theta_abs_le_10_p95_abs_err_deg | 0.8306 |
| theta_neg_10_8_p95_abs_err_deg | 0.7964 |
| theta_pos_8_10_p95_abs_err_deg | 1.1338 |
| theta_abs_le_8_p95_abs_err_deg | 0.7966 |
| theta_neg_8_6_p95_abs_err_deg | 0.8227 |
| theta_pos_6_8_p95_abs_err_deg | 0.5044 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.5325 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2155 |
| theta_flat_abs_p95_deg | 2.1047 |
| theta_flat_bias_deg | 0.0387 |
| theta_near_flat_abs_p95_deg | 1.0166 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1510 |
| theta_flat_turn_abs_p95_deg | 0.8673 |
| flat_recall | 0.9670 |
| stall_recall | 0.6154 |
| slope_recall | 0.9976 |
| uphill_recall | 0.8049 |
| downhill_recall | 0.7864 |

- best_epoch: 135
- train_seconds: 535.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 9 | 0.7778 | 0.5416 |
| [0.60,0.70) | 10 | 0.5000 | 0.6381 |
| [0.70,0.80) | 11 | 0.1818 | 0.7432 |
| [0.80,0.90) | 16 | 0.5625 | 0.8385 |
| [0.90,1.00) | 3687 | 0.0146 | 0.9992 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 92 | 0.5217 | 0.5421 |
| [0.60,0.70) | 89 | 0.4944 | 0.6554 |
| [0.70,0.80) | 95 | 0.4421 | 0.7528 |
| [0.80,0.90) | 175 | 0.2286 | 0.8568 |
| [0.90,1.00) | 3282 | 0.0686 | 0.9922 |


## 验证集最佳点

```json
{
  "loss_total": 0.2952053064604029,
  "acc_main": 0.971614883007288,
  "acc_turn": 0.8181818181818182,
  "acc_turn_pure": 0.8431641518061271,
  "acc_turn_transition": 0.6880952380952381,
  "flat_recall": 0.9469548133595285,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.9795221843003413,
  "recall_main": [
    0.9469548133595285,
    0.8936170212765957,
    0.9795221843003413
  ],
  "turn_right_recall": 0.7884615384615384,
  "turn_straight_recall": 0.8361162646876933,
  "turn_left_recall": 0.789272030651341,
  "recall_turn": [
    0.7884615384615384,
    0.8361162646876933,
    0.789272030651341
  ],
  "cm_turn": [
    [
      369,
      57,
      42
    ],
    [
      149,
      1352,
      116
    ],
    [
      24,
      86,
      412
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      482,
      0,
      27
    ],
    [
      5,
      42,
      0
    ],
    [
      36,
      6,
      2009
    ]
  ],
  "main_confidence_mean": 0.9940267107524476,
  "main_confidence_error_mean": 0.9073838551748002,
  "main_low_conf_0p60_ratio": 0.0030686612965093976,
  "main_low_conf_0p70_ratio": 0.006904487917146145,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 8,
      "error_rate": 0.625,
      "mean_confidence": 0.5476631000318901
    },
    {
      "bin": "[0.60,0.70)",
      "n": 10,
      "error_rate": 0.6,
      "mean_confidence": 0.6447303703907754
    },
    {
      "bin": "[0.70,0.80)",
      "n": 9,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.7544991250386053
    },
    {
      "bin": "[0.80,0.90)",
      "n": 18,
      "error_rate": 0.2222222222222222,
      "mean_confidence": 0.8585526198678515
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2562,
      "error_rate": 0.02185792349726776,
      "mean_confidence": 0.9985771222265803
    }
  ],
  "turn_confidence_mean": 0.9434251236157117,
  "turn_confidence_error_mean": 0.8812843538205203,
  "turn_low_conf_0p60_ratio": 0.02915228231683928,
  "turn_low_conf_0p70_ratio": 0.06635980053701572,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 76,
      "error_rate": 0.4342105263157895,
      "mean_confidence": 0.5412603036652089
    },
    {
      "bin": "[0.60,0.70)",
      "n": 97,
      "error_rate": 0.44329896907216493,
      "mean_confidence": 0.6470982591514917
    },
    {
      "bin": "[0.70,0.80)",
      "n": 130,
      "error_rate": 0.3769230769230769,
      "mean_confidence": 0.7540716139274949
    },
    {
      "bin": "[0.80,0.90)",
      "n": 179,
      "error_rate": 0.3016759776536313,
      "mean_confidence": 0.8594744270649239
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2125,
      "error_rate": 0.1388235294117647,
      "mean_confidence": 0.9899904709622185
    }
  ],
  "theta_mae_rad": 0.004079559352248907,
  "theta_mae_deg": 0.23374152183532715,
  "uphill_recall": 0.7790519877675841,
  "downhill_recall": 0.8123003194888179,
  "slope_sign_acc": 0.984765625,
  "theta_flat_mae_deg": 0.25834769010543823,
  "theta_flat_abs_p95_deg": 1.8569960594177246,
  "theta_flat_abs_max_deg": 3.068234920501709,
  "theta_flat_bias_deg": 0.04302302375435829,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.3996959626674652,
  "theta_near_flat_abs_p95_deg": 2.049255847930908,
  "theta_near_flat_abs_max_deg": 6.424135208129883,
  "theta_near_flat_bias_deg": 0.19422636926174164,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.2555282711982727,
  "theta_flat_turn_abs_p95_deg": 0.9881909489631653,
  "theta_flat_turn_abs_max_deg": 2.36600399017334,
  "theta_flat_turn_bias_deg": 0.1627560704946518,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.23374152183532715,
  "theta_slope_control_abs_p95_deg": 9.23804759979248,
  "theta_slope_control_abs_max_deg": 10.447540283203125,
  "theta_slope_control_bias_deg": -0.022429784759879112,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.23374152183532715,
  "theta_all_rmse_deg": 0.396517813205719,
  "theta_all_p95_abs_err_deg": 0.6944842338562012,
  "theta_all_max_abs_err_deg": 3.9682350158691406,
  "theta_all_bias_deg": -0.022429784759879112,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.2276349514722824,
  "theta_active_abs_ge_2_rmse_deg": 0.36959969997406006,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.6670597195625305,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.2733285427093506,
  "theta_active_abs_ge_2_bias_deg": -0.038673315197229385,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.22164106369018555,
  "theta_abs_le_8_rmse_deg": 0.38410264253616333,
  "theta_abs_le_8_p95_abs_err_deg": 0.631521463394165,
  "theta_abs_le_8_max_abs_err_deg": 3.9682350158691406,
  "theta_abs_le_8_bias_deg": -0.010776548646390438,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.23374152183532715,
  "theta_abs_le_10_rmse_deg": 0.396517813205719,
  "theta_abs_le_10_p95_abs_err_deg": 0.6944842338562012,
  "theta_abs_le_10_max_abs_err_deg": 3.9682350158691406,
  "theta_abs_le_10_bias_deg": -0.022429784759879112,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.28098464012145996,
  "theta_pos_8_10_rmse_deg": 0.3953201472759247,
  "theta_pos_8_10_p95_abs_err_deg": 0.8774875402450562,
  "theta_pos_8_10_max_abs_err_deg": 1.527359962463379,
  "theta_pos_8_10_bias_deg": -0.22551828622817993,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.27948951721191406,
  "theta_neg_10_8_rmse_deg": 0.4784209728240967,
  "theta_neg_10_8_p95_abs_err_deg": 0.9504434466362,
  "theta_neg_10_8_max_abs_err_deg": 3.093952178955078,
  "theta_neg_10_8_bias_deg": 0.07579859346151352,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.18531478941440582,
  "theta_pos_6_8_rmse_deg": 0.22300635278224945,
  "theta_pos_6_8_p95_abs_err_deg": 0.4227737486362457,
  "theta_pos_6_8_max_abs_err_deg": 0.5870662331581116,
  "theta_pos_6_8_bias_deg": -0.14055338501930237,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.21794669330120087,
  "theta_neg_8_6_rmse_deg": 0.462356299161911,
  "theta_neg_8_6_p95_abs_err_deg": 0.9856271743774414,
  "theta_neg_8_6_max_abs_err_deg": 2.2499589920043945,
  "theta_neg_8_6_bias_deg": 0.1109670028090477,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.19948531687259674,
  "theta_neg_4_2_rmse_deg": 0.2651808261871338,
  "theta_neg_4_2_p95_abs_err_deg": 0.5031687021255493,
  "theta_neg_4_2_max_abs_err_deg": 1.2089049816131592,
  "theta_neg_4_2_bias_deg": 0.011650143191218376,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.4009557068347931,
  "theta_neg_2_0p5_rmse_deg": 0.7550092339515686,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3210861682891846,
  "theta_neg_2_0p5_max_abs_err_deg": 3.9682350158691406,
  "theta_neg_2_0p5_bias_deg": 0.07879946380853653,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.14309808611869812,
  "theta_pos_0p5_2_rmse_deg": 0.19425052404403687,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.3991648852825165,
  "theta_pos_0p5_2_max_abs_err_deg": 0.930639922618866,
  "theta_pos_0p5_2_bias_deg": 0.014627093449234962,
  "theta_pos_0p5_2_n": 168.0
}
```
