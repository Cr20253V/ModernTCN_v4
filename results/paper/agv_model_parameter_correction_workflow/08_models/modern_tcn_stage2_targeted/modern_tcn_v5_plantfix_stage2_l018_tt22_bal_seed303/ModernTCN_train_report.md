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
  "lambda_turn": 0.18,
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
    1.35,
    0.85,
    1.35
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.2,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.25,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.55,
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
| acc_main | 0.9570 |
| acc_turn | 0.5883 |
| acc_turn_pure | 0.5995 |
| acc_turn_transition | 0.5395 |
| main_confidence_mean | 0.9893 |
| main_low_conf_0p60_ratio | 0.0075 |
| main_low_conf_0p70_ratio | 0.0136 |
| turn_confidence_mean | 0.8219 |
| turn_low_conf_0p60_ratio | 0.1669 |
| turn_low_conf_0p70_ratio | 0.2835 |
| turn_right_recall | 0.5519 |
| turn_straight_recall | 0.6022 |
| turn_left_recall | 0.5908 |
| theta_mae_deg | 0.6762 |
| theta_abs_le_10_p95_abs_err_deg | 1.8961 |
| theta_neg_10_8_p95_abs_err_deg | 1.5728 |
| theta_pos_8_10_p95_abs_err_deg | 2.6464 |
| theta_abs_le_8_p95_abs_err_deg | 1.7942 |
| theta_neg_8_6_p95_abs_err_deg | 1.9648 |
| theta_pos_6_8_p95_abs_err_deg | 1.8374 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6504 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6725 |
| theta_flat_abs_p95_deg | 2.4194 |
| theta_flat_bias_deg | -0.1691 |
| theta_near_flat_abs_p95_deg | 1.9051 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3160 |
| theta_flat_turn_abs_p95_deg | 1.6714 |
| flat_recall | 0.9299 |
| stall_recall | 0.6458 |
| slope_recall | 0.9753 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.8042 |

- best_epoch: 70
- train_seconds: 859.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 27 | 0.6296 | 0.5511 |
| [0.60,0.70) | 22 | 0.7727 | 0.6433 |
| [0.70,0.80) | 19 | 0.5263 | 0.7560 |
| [0.80,0.90) | 40 | 0.3250 | 0.8510 |
| [0.90,1.00) | 3494 | 0.0280 | 0.9977 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 601 | 0.5657 | 0.5252 |
| [0.60,0.70) | 420 | 0.5095 | 0.6496 |
| [0.70,0.80) | 406 | 0.5419 | 0.7515 |
| [0.80,0.90) | 430 | 0.4698 | 0.8530 |
| [0.90,1.00) | 1745 | 0.2905 | 0.9743 |


## 验证集最佳点

```json
{
  "loss_total": 0.5994253778651215,
  "acc_main": 0.9461434370771312,
  "acc_turn": 0.6503382949932341,
  "acc_turn_pure": 0.6653556211078335,
  "acc_turn_transition": 0.5791925465838509,
  "flat_recall": 0.9558599695585996,
  "stall_recall": 0.23809523809523808,
  "slope_recall": 0.9539385847797063,
  "recall_main": [
    0.9558599695585996,
    0.23809523809523808,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6196682464454977,
  "turn_straight_recall": 0.6309771309771309,
  "turn_left_recall": 0.7184466019417476,
  "recall_turn": [
    0.6196682464454977,
    0.6309771309771309,
    0.7184466019417476
  ],
  "cm_turn": [
    [
      523,
      231,
      90
    ],
    [
      275,
      1214,
      435
    ],
    [
      42,
      219,
      666
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      628,
      0,
      29
    ],
    [
      5,
      10,
      27
    ],
    [
      129,
      9,
      2858
    ]
  ],
  "main_confidence_mean": 0.9682509994012253,
  "main_confidence_error_mean": 0.7352531210345742,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.05602165087956698,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.48677248677248675,
      "mean_confidence": 0.5031239637520329
    },
    {
      "bin": "[0.60,0.70)",
      "n": 18,
      "error_rate": 0.3888888888888889,
      "mean_confidence": 0.6535566670756991
    },
    {
      "bin": "[0.70,0.80)",
      "n": 24,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.7503979324337736
    },
    {
      "bin": "[0.80,0.90)",
      "n": 32,
      "error_rate": 0.4375,
      "mean_confidence": 0.8539646373181371
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3432,
      "error_rate": 0.022727272727272728,
      "mean_confidence": 0.9981050626044403
    }
  ],
  "turn_confidence_mean": 0.8493644945549745,
  "turn_confidence_error_mean": 0.7752033666651178,
  "turn_low_conf_0p60_ratio": 0.15290933694181327,
  "turn_low_conf_0p70_ratio": 0.2368064952638701,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 565,
      "error_rate": 0.6300884955752213,
      "mean_confidence": 0.5341458253135292
    },
    {
      "bin": "[0.60,0.70)",
      "n": 310,
      "error_rate": 0.4645161290322581,
      "mean_confidence": 0.6482777531933873
    },
    {
      "bin": "[0.70,0.80)",
      "n": 347,
      "error_rate": 0.42939481268011526,
      "mean_confidence": 0.7526254762428543
    },
    {
      "bin": "[0.80,0.90)",
      "n": 386,
      "error_rate": 0.3911917098445596,
      "mean_confidence": 0.855309881056155
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2087,
      "error_rate": 0.23574508864398658,
      "mean_confidence": 0.9795556579993245
    }
  ],
  "theta_mae_rad": 0.014746000058948994,
  "theta_mae_deg": 0.8448835015296936,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9728989871338626,
  "theta_flat_mae_deg": 1.1407042741775513,
  "theta_flat_abs_p95_deg": 4.158107280731201,
  "theta_flat_abs_max_deg": 9.098775863647461,
  "theta_flat_bias_deg": 0.12224523723125458,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5699706077575684,
  "theta_near_flat_abs_p95_deg": 4.1585774421691895,
  "theta_near_flat_abs_max_deg": 9.098775863647461,
  "theta_near_flat_bias_deg": 0.3980616629123688,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.16968834400177,
  "theta_flat_turn_abs_p95_deg": 4.158107280731201,
  "theta_flat_turn_abs_max_deg": 9.098775863647461,
  "theta_flat_turn_bias_deg": -0.4119257926940918,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8448835015296936,
  "theta_slope_control_abs_p95_deg": 9.225253105163574,
  "theta_slope_control_abs_max_deg": 11.369906425476074,
  "theta_slope_control_bias_deg": 0.3109067380428314,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8448835015296936,
  "theta_all_rmse_deg": 1.256862998008728,
  "theta_all_p95_abs_err_deg": 2.8099231719970703,
  "theta_all_max_abs_err_deg": 8.598776817321777,
  "theta_all_bias_deg": 0.3109067678451538,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7800121903419495,
  "theta_active_abs_ge_2_rmse_deg": 1.1296882629394531,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2234363555908203,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.708399295806885,
  "theta_active_abs_ge_2_bias_deg": 0.35227882862091064,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8754022717475891,
  "theta_abs_le_8_rmse_deg": 1.2827881574630737,
  "theta_abs_le_8_p95_abs_err_deg": 3.064868450164795,
  "theta_abs_le_8_max_abs_err_deg": 8.598776817321777,
  "theta_abs_le_8_bias_deg": 0.29712504148483276,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8448835015296936,
  "theta_abs_le_10_rmse_deg": 1.256862998008728,
  "theta_abs_le_10_p95_abs_err_deg": 2.8099231719970703,
  "theta_abs_le_10_max_abs_err_deg": 8.598776817321777,
  "theta_abs_le_10_bias_deg": 0.3109067678451538,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.4869672656059265,
  "theta_pos_8_10_rmse_deg": 0.6495682597160339,
  "theta_pos_8_10_p95_abs_err_deg": 1.358154058456421,
  "theta_pos_8_10_max_abs_err_deg": 2.9670250415802,
  "theta_pos_8_10_bias_deg": 0.03602803125977516,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.949270486831665,
  "theta_neg_10_8_rmse_deg": 1.4822874069213867,
  "theta_neg_10_8_p95_abs_err_deg": 2.8305323123931885,
  "theta_neg_10_8_max_abs_err_deg": 7.708399295806885,
  "theta_neg_10_8_bias_deg": 0.7078220844268799,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5660730600357056,
  "theta_pos_6_8_rmse_deg": 0.8399108648300171,
  "theta_pos_6_8_p95_abs_err_deg": 1.685238242149353,
  "theta_pos_6_8_max_abs_err_deg": 4.208929538726807,
  "theta_pos_6_8_bias_deg": 0.12678855657577515,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.9141197800636292,
  "theta_neg_8_6_rmse_deg": 1.2341539859771729,
  "theta_neg_8_6_p95_abs_err_deg": 2.246553897857666,
  "theta_neg_8_6_max_abs_err_deg": 7.383626937866211,
  "theta_neg_8_6_bias_deg": 0.5779156684875488,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6766910552978516,
  "theta_neg_4_2_rmse_deg": 0.9396957159042358,
  "theta_neg_4_2_p95_abs_err_deg": 1.8350462913513184,
  "theta_neg_4_2_max_abs_err_deg": 5.322578430175781,
  "theta_neg_4_2_bias_deg": 0.16834639012813568,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6638124585151672,
  "theta_neg_2_0p5_rmse_deg": 0.9142392873764038,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6728098392486572,
  "theta_neg_2_0p5_max_abs_err_deg": 5.101937770843506,
  "theta_neg_2_0p5_bias_deg": -0.3175835907459259,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1210224628448486,
  "theta_pos_0p5_2_rmse_deg": 1.531103491783142,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.658107042312622,
  "theta_pos_0p5_2_max_abs_err_deg": 5.261331081390381,
  "theta_pos_0p5_2_bias_deg": 0.44000694155693054,
  "theta_pos_0p5_2_n": 163.0
}
```
