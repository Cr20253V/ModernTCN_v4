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
  "temporal_padding": "causal",
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
| acc_main | 0.9772 |
| acc_turn | 0.8840 |
| acc_turn_pure | 0.9078 |
| acc_turn_transition | 0.7421 |
| main_confidence_mean | 0.9942 |
| main_low_conf_0p60_ratio | 0.0029 |
| main_low_conf_0p70_ratio | 0.0072 |
| turn_confidence_mean | 0.9472 |
| turn_low_conf_0p60_ratio | 0.0303 |
| turn_low_conf_0p70_ratio | 0.0627 |
| turn_right_recall | 0.8967 |
| turn_straight_recall | 0.8652 |
| turn_left_recall | 0.9262 |
| theta_mae_deg | 0.2918 |
| theta_abs_le_10_p95_abs_err_deg | 0.8860 |
| theta_neg_10_8_p95_abs_err_deg | 0.8642 |
| theta_pos_8_10_p95_abs_err_deg | 0.9415 |
| theta_abs_le_8_p95_abs_err_deg | 0.8827 |
| theta_neg_8_6_p95_abs_err_deg | 1.0275 |
| theta_pos_6_8_p95_abs_err_deg | 0.4794 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.8284 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4169 |
| theta_flat_abs_p95_deg | 2.2895 |
| theta_flat_bias_deg | 0.0248 |
| theta_near_flat_abs_p95_deg | 1.0059 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1560 |
| theta_flat_turn_abs_p95_deg | 0.7848 |
| flat_recall | 0.9590 |
| stall_recall | 0.6325 |
| slope_recall | 0.9962 |
| uphill_recall | 0.8123 |
| downhill_recall | 0.7805 |

- best_epoch: 97
- train_seconds: 431.1

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 11 | 0.5455 | 0.5513 |
| [0.60,0.70) | 16 | 0.5000 | 0.6550 |
| [0.70,0.80) | 12 | 0.3333 | 0.7520 |
| [0.80,0.90) | 28 | 0.1786 | 0.8528 |
| [0.90,1.00) | 3666 | 0.0169 | 0.9989 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 113 | 0.6195 | 0.5401 |
| [0.60,0.70) | 121 | 0.3802 | 0.6469 |
| [0.70,0.80) | 143 | 0.3287 | 0.7479 |
| [0.80,0.90) | 232 | 0.2328 | 0.8549 |
| [0.90,1.00) | 3124 | 0.0691 | 0.9895 |


## 验证集最佳点

```json
{
  "loss_total": 0.2912874761147201,
  "acc_main": 0.9739163789796701,
  "acc_turn": 0.7997698504027618,
  "acc_turn_pure": 0.8271604938271605,
  "acc_turn_transition": 0.6571428571428571,
  "flat_recall": 0.9174852652259332,
  "stall_recall": 0.8723404255319149,
  "slope_recall": 0.9902486591906388,
  "recall_main": [
    0.9174852652259332,
    0.8723404255319149,
    0.9902486591906388
  ],
  "turn_right_recall": 0.8034188034188035,
  "turn_straight_recall": 0.79282622139765,
  "turn_left_recall": 0.8180076628352491,
  "recall_turn": [
    0.8034188034188035,
    0.79282622139765,
    0.8180076628352491
  ],
  "cm_turn": [
    [
      376,
      77,
      15
    ],
    [
      175,
      1282,
      160
    ],
    [
      30,
      65,
      427
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      467,
      0,
      42
    ],
    [
      5,
      41,
      1
    ],
    [
      18,
      2,
      2031
    ]
  ],
  "main_confidence_mean": 0.9902826599697077,
  "main_confidence_error_mean": 0.8581699766056851,
  "main_low_conf_0p60_ratio": 0.006137322593018795,
  "main_low_conf_0p70_ratio": 0.012658227848101266,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 16,
      "error_rate": 0.375,
      "mean_confidence": 0.5567188752119108
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.5294117647058824,
      "mean_confidence": 0.6470230268926359
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.23809523809523808,
      "mean_confidence": 0.7544994289888758
    },
    {
      "bin": "[0.80,0.90)",
      "n": 22,
      "error_rate": 0.5,
      "mean_confidence": 0.8429768691087062
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2531,
      "error_rate": 0.014618727775582773,
      "mean_confidence": 0.9985657929479671
    }
  ],
  "turn_confidence_mean": 0.9303290015781931,
  "turn_confidence_error_mean": 0.8499517822789655,
  "turn_low_conf_0p60_ratio": 0.04334484081319524,
  "turn_low_conf_0p70_ratio": 0.0805523590333717,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 113,
      "error_rate": 0.5132743362831859,
      "mean_confidence": 0.5387700764293178
    },
    {
      "bin": "[0.60,0.70)",
      "n": 97,
      "error_rate": 0.5463917525773195,
      "mean_confidence": 0.6487883730109075
    },
    {
      "bin": "[0.70,0.80)",
      "n": 152,
      "error_rate": 0.3618421052631579,
      "mean_confidence": 0.7489721104670429
    },
    {
      "bin": "[0.80,0.90)",
      "n": 219,
      "error_rate": 0.3744292237442922,
      "mean_confidence": 0.8539153321255528
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2026,
      "error_rate": 0.13524185587364265,
      "mean_confidence": 0.9875138192345959
    }
  ],
  "theta_mae_rad": 0.004807768855243921,
  "theta_mae_deg": 0.27546486258506775,
  "uphill_recall": 0.8042813455657493,
  "downhill_recall": 0.8154952076677316,
  "slope_sign_acc": 0.983984375,
  "theta_flat_mae_deg": 0.27185943722724915,
  "theta_flat_abs_p95_deg": 1.9032926559448242,
  "theta_flat_abs_max_deg": 2.8432888984680176,
  "theta_flat_bias_deg": 0.06583502143621445,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.35813185572624207,
  "theta_near_flat_abs_p95_deg": 1.7083877325057983,
  "theta_near_flat_abs_max_deg": 6.158154010772705,
  "theta_near_flat_bias_deg": 0.1188477948307991,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.2813605070114136,
  "theta_flat_turn_abs_p95_deg": 1.0578029155731201,
  "theta_flat_turn_abs_max_deg": 2.320734977722168,
  "theta_flat_turn_bias_deg": 0.1139795333147049,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.27546486258506775,
  "theta_slope_control_abs_p95_deg": 9.351214408874512,
  "theta_slope_control_abs_max_deg": 11.553901672363281,
  "theta_slope_control_bias_deg": 0.03627289459109306,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.27546483278274536,
  "theta_all_rmse_deg": 0.42046719789505005,
  "theta_all_p95_abs_err_deg": 0.7401711940765381,
  "theta_all_max_abs_err_deg": 3.74328875541687,
  "theta_all_bias_deg": 0.036272890865802765,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.27635958790779114,
  "theta_active_abs_ge_2_rmse_deg": 0.4107288122177124,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.7336698770523071,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.588928699493408,
  "theta_active_abs_ge_2_bias_deg": 0.028936414048075676,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.2734529376029968,
  "theta_abs_le_8_rmse_deg": 0.4186230003833771,
  "theta_abs_le_8_p95_abs_err_deg": 0.7333085536956787,
  "theta_abs_le_8_max_abs_err_deg": 3.74328875541687,
  "theta_abs_le_8_bias_deg": 0.0495910719037056,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.27546483278274536,
  "theta_abs_le_10_rmse_deg": 0.42046719789505005,
  "theta_abs_le_10_p95_abs_err_deg": 0.7401711940765381,
  "theta_abs_le_10_max_abs_err_deg": 3.74328875541687,
  "theta_abs_le_10_bias_deg": 0.036272890865802765,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.2568262219429016,
  "theta_pos_8_10_rmse_deg": 0.3652917444705963,
  "theta_pos_8_10_p95_abs_err_deg": 0.7236632108688354,
  "theta_pos_8_10_max_abs_err_deg": 1.7624675035476685,
  "theta_pos_8_10_bias_deg": -0.15553361177444458,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.3069913983345032,
  "theta_neg_10_8_rmse_deg": 0.4766988754272461,
  "theta_neg_10_8_p95_abs_err_deg": 0.9509981870651245,
  "theta_neg_10_8_max_abs_err_deg": 2.749831438064575,
  "theta_neg_10_8_bias_deg": 0.11215135455131531,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.2517414093017578,
  "theta_pos_6_8_rmse_deg": 0.34821614623069763,
  "theta_pos_6_8_p95_abs_err_deg": 0.7597317099571228,
  "theta_pos_6_8_max_abs_err_deg": 1.4185144901275635,
  "theta_pos_6_8_bias_deg": -0.16317036747932434,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.37198829650878906,
  "theta_neg_8_6_rmse_deg": 0.5627216696739197,
  "theta_neg_8_6_p95_abs_err_deg": 1.2290581464767456,
  "theta_neg_8_6_max_abs_err_deg": 2.3531785011291504,
  "theta_neg_8_6_bias_deg": 0.36435672640800476,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.25709840655326843,
  "theta_neg_4_2_rmse_deg": 0.3170921802520752,
  "theta_neg_4_2_p95_abs_err_deg": 0.5849327445030212,
  "theta_neg_4_2_max_abs_err_deg": 0.9435877799987793,
  "theta_neg_4_2_bias_deg": 0.12764321267604828,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.3374248445034027,
  "theta_neg_2_0p5_rmse_deg": 0.6638918519020081,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0377203226089478,
  "theta_neg_2_0p5_max_abs_err_deg": 3.74328875541687,
  "theta_neg_2_0p5_bias_deg": 0.19465994834899902,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.22351376712322235,
  "theta_pos_0p5_2_rmse_deg": 0.293241024017334,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.5713293552398682,
  "theta_pos_0p5_2_max_abs_err_deg": 0.9218733310699463,
  "theta_pos_0p5_2_bias_deg": 0.018533702939748764,
  "theta_pos_0p5_2_n": 168.0
}
```
