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
| acc_main | 0.9796 |
| acc_turn | 0.8722 |
| acc_turn_pure | 0.8981 |
| acc_turn_transition | 0.7178 |
| main_confidence_mean | 0.9957 |
| main_low_conf_0p60_ratio | 0.0008 |
| main_low_conf_0p70_ratio | 0.0035 |
| turn_confidence_mean | 0.9160 |
| turn_low_conf_0p60_ratio | 0.0471 |
| turn_low_conf_0p70_ratio | 0.0978 |
| turn_right_recall | 0.8721 |
| turn_straight_recall | 0.8652 |
| turn_left_recall | 0.8934 |
| theta_mae_deg | 0.3281 |
| theta_abs_le_10_p95_abs_err_deg | 0.9201 |
| theta_neg_10_8_p95_abs_err_deg | 1.2732 |
| theta_pos_8_10_p95_abs_err_deg | 1.3413 |
| theta_abs_le_8_p95_abs_err_deg | 0.8539 |
| theta_neg_8_6_p95_abs_err_deg | 1.0920 |
| theta_pos_6_8_p95_abs_err_deg | 0.4867 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.7177 |
| theta_pos_0p5_2_p95_abs_err_deg | 0.9867 |
| theta_flat_abs_p95_deg | 2.1761 |
| theta_flat_bias_deg | 0.0425 |
| theta_near_flat_abs_p95_deg | 1.3054 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1348 |
| theta_flat_turn_abs_p95_deg | 0.8561 |
| flat_recall | 0.9630 |
| stall_recall | 0.6667 |
| slope_recall | 0.9969 |
| uphill_recall | 0.8123 |
| downhill_recall | 0.7805 |

- best_epoch: 68
- train_seconds: 336.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 3 | 1.0000 | 0.5357 |
| [0.60,0.70) | 10 | 0.2000 | 0.6536 |
| [0.70,0.80) | 15 | 0.5333 | 0.7640 |
| [0.80,0.90) | 19 | 0.3684 | 0.8505 |
| [0.90,1.00) | 3686 | 0.0152 | 0.9987 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 176 | 0.4943 | 0.5361 |
| [0.60,0.70) | 189 | 0.3439 | 0.6547 |
| [0.70,0.80) | 250 | 0.2400 | 0.7552 |
| [0.80,0.90) | 401 | 0.1696 | 0.8543 |
| [0.90,1.00) | 2717 | 0.0725 | 0.9827 |


## 验证集最佳点

```json
{
  "loss_total": 0.26185183967833414,
  "acc_main": 0.9612581511315689,
  "acc_turn": 0.7786728039892596,
  "acc_turn_pure": 0.8084133516232281,
  "acc_turn_transition": 0.6238095238095238,
  "flat_recall": 0.9115913555992141,
  "stall_recall": 0.8936170212765957,
  "slope_recall": 0.9751340809361287,
  "recall_main": [
    0.9115913555992141,
    0.8936170212765957,
    0.9751340809361287
  ],
  "turn_right_recall": 0.7649572649572649,
  "turn_straight_recall": 0.7860235003092146,
  "turn_left_recall": 0.7681992337164751,
  "recall_turn": [
    0.7649572649572649,
    0.7860235003092146,
    0.7681992337164751
  ],
  "cm_turn": [
    [
      358,
      77,
      33
    ],
    [
      177,
      1271,
      169
    ],
    [
      28,
      93,
      401
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      464,
      0,
      45
    ],
    [
      5,
      42,
      0
    ],
    [
      48,
      3,
      2000
    ]
  ],
  "main_confidence_mean": 0.9892925967646713,
  "main_confidence_error_mean": 0.858425815959864,
  "main_low_conf_0p60_ratio": 0.00728807057920982,
  "main_low_conf_0p70_ratio": 0.01304181051016494,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 19,
      "error_rate": 0.5789473684210527,
      "mean_confidence": 0.545312509045987
    },
    {
      "bin": "[0.60,0.70)",
      "n": 15,
      "error_rate": 0.7333333333333333,
      "mean_confidence": 0.6497396469276019
    },
    {
      "bin": "[0.70,0.80)",
      "n": 26,
      "error_rate": 0.38461538461538464,
      "mean_confidence": 0.7550488773529442
    },
    {
      "bin": "[0.80,0.90)",
      "n": 26,
      "error_rate": 0.5,
      "mean_confidence": 0.8517273604179765
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2521,
      "error_rate": 0.022213407378024592,
      "mean_confidence": 0.9984936871113314
    }
  ],
  "turn_confidence_mean": 0.898597103278205,
  "turn_confidence_error_mean": 0.8239350638606334,
  "turn_low_conf_0p60_ratio": 0.05715381664748753,
  "turn_low_conf_0p70_ratio": 0.12696586114307634,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 149,
      "error_rate": 0.4563758389261745,
      "mean_confidence": 0.5403405760498772
    },
    {
      "bin": "[0.60,0.70)",
      "n": 182,
      "error_rate": 0.4230769230769231,
      "mean_confidence": 0.653078671624348
    },
    {
      "bin": "[0.70,0.80)",
      "n": 209,
      "error_rate": 0.430622009569378,
      "mean_confidence": 0.7512512067898788
    },
    {
      "bin": "[0.80,0.90)",
      "n": 334,
      "error_rate": 0.2844311377245509,
      "mean_confidence": 0.8545343449450654
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1733,
      "error_rate": 0.1425274091171379,
      "mean_confidence": 0.9814458227054131
    }
  ],
  "theta_mae_rad": 0.005258292891085148,
  "theta_mae_deg": 0.3012779653072357,
  "uphill_recall": 0.7767584097859327,
  "downhill_recall": 0.8218849840255591,
  "slope_sign_acc": 0.983203125,
  "theta_flat_mae_deg": 0.3119441270828247,
  "theta_flat_abs_p95_deg": 1.9866689443588257,
  "theta_flat_abs_max_deg": 3.508300542831421,
  "theta_flat_bias_deg": 0.11499324440956116,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.4058672785758972,
  "theta_near_flat_abs_p95_deg": 1.7616701126098633,
  "theta_near_flat_abs_max_deg": 5.531498432159424,
  "theta_near_flat_bias_deg": 0.17572715878486633,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.3492700159549713,
  "theta_flat_turn_abs_p95_deg": 1.355159044265747,
  "theta_flat_turn_abs_max_deg": 1.9721028804779053,
  "theta_flat_turn_bias_deg": 0.15895453095436096,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.3012779653072357,
  "theta_slope_control_abs_p95_deg": 9.239545822143555,
  "theta_slope_control_abs_max_deg": 10.733413696289062,
  "theta_slope_control_bias_deg": -0.07691532373428345,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.30127793550491333,
  "theta_all_rmse_deg": 0.44553038477897644,
  "theta_all_p95_abs_err_deg": 0.7554437518119812,
  "theta_all_max_abs_err_deg": 3.837855815887451,
  "theta_all_bias_deg": -0.07691532373428345,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.2986309230327606,
  "theta_active_abs_ge_2_rmse_deg": 0.42555779218673706,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.7335900068283081,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.0341532230377197,
  "theta_active_abs_ge_2_bias_deg": -0.12454158067703247,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.2759959399700165,
  "theta_abs_le_8_rmse_deg": 0.4160991907119751,
  "theta_abs_le_8_p95_abs_err_deg": 0.69501793384552,
  "theta_abs_le_8_max_abs_err_deg": 3.837855815887451,
  "theta_abs_le_8_bias_deg": -0.05248008668422699,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.30127793550491333,
  "theta_abs_le_10_rmse_deg": 0.44553038477897644,
  "theta_abs_le_10_p95_abs_err_deg": 0.7554437518119812,
  "theta_abs_le_10_max_abs_err_deg": 3.837855815887451,
  "theta_abs_le_10_bias_deg": -0.07691532373428345,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.3972155749797821,
  "theta_pos_8_10_rmse_deg": 0.47582122683525085,
  "theta_pos_8_10_p95_abs_err_deg": 0.7745920419692993,
  "theta_pos_8_10_max_abs_err_deg": 2.3005406856536865,
  "theta_pos_8_10_bias_deg": -0.34270697832107544,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.3993624746799469,
  "theta_neg_10_8_rmse_deg": 0.5988024473190308,
  "theta_neg_10_8_p95_abs_err_deg": 1.2054742574691772,
  "theta_neg_10_8_max_abs_err_deg": 2.7130868434906006,
  "theta_neg_10_8_bias_deg": -0.015455784276127815,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.3752005696296692,
  "theta_pos_6_8_rmse_deg": 0.445026695728302,
  "theta_pos_6_8_p95_abs_err_deg": 0.7990390062332153,
  "theta_pos_6_8_max_abs_err_deg": 1.8870919942855835,
  "theta_pos_6_8_bias_deg": -0.24649304151535034,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.2575574219226837,
  "theta_neg_8_6_rmse_deg": 0.454351007938385,
  "theta_neg_8_6_p95_abs_err_deg": 0.7255169749259949,
  "theta_neg_8_6_max_abs_err_deg": 1.9554638862609863,
  "theta_neg_8_6_bias_deg": 0.03717760741710663,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.2151750773191452,
  "theta_neg_4_2_rmse_deg": 0.2959613800048828,
  "theta_neg_4_2_p95_abs_err_deg": 0.6204772591590881,
  "theta_neg_4_2_max_abs_err_deg": 1.202146053314209,
  "theta_neg_4_2_bias_deg": -0.07493875175714493,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.41613972187042236,
  "theta_neg_2_0p5_rmse_deg": 0.7581876516342163,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2023768424987793,
  "theta_neg_2_0p5_max_abs_err_deg": 3.837855815887451,
  "theta_neg_2_0p5_bias_deg": 0.11759229004383087,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.23471076786518097,
  "theta_pos_0p5_2_rmse_deg": 0.30510959029197693,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.49495747685432434,
  "theta_pos_0p5_2_max_abs_err_deg": 1.736328125,
  "theta_pos_0p5_2_bias_deg": 0.1736467033624649,
  "theta_pos_0p5_2_n": 168.0
}
```
