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
| acc_main | 0.9770 |
| acc_turn | 0.9087 |
| acc_turn_pure | 0.9287 |
| acc_turn_transition | 0.7888 |
| main_confidence_mean | 0.9955 |
| main_low_conf_0p60_ratio | 0.0024 |
| main_low_conf_0p70_ratio | 0.0051 |
| turn_confidence_mean | 0.9651 |
| turn_low_conf_0p60_ratio | 0.0182 |
| turn_low_conf_0p70_ratio | 0.0405 |
| turn_right_recall | 0.8659 |
| turn_straight_recall | 0.9209 |
| turn_left_recall | 0.9194 |
| theta_mae_deg | 0.2682 |
| theta_abs_le_10_p95_abs_err_deg | 0.8949 |
| theta_neg_10_8_p95_abs_err_deg | 0.9937 |
| theta_pos_8_10_p95_abs_err_deg | 0.7687 |
| theta_abs_le_8_p95_abs_err_deg | 0.9008 |
| theta_neg_8_6_p95_abs_err_deg | 0.7587 |
| theta_pos_6_8_p95_abs_err_deg | 0.4199 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.5108 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.3034 |
| theta_flat_abs_p95_deg | 2.3422 |
| theta_flat_bias_deg | 0.1596 |
| theta_near_flat_abs_p95_deg | 1.0666 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2606 |
| theta_flat_turn_abs_p95_deg | 1.0224 |
| flat_recall | 0.9564 |
| stall_recall | 0.6667 |
| slope_recall | 0.9951 |
| uphill_recall | 0.8123 |
| downhill_recall | 0.7799 |

- best_epoch: 173
- train_seconds: 583.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 9 | 0.3333 | 0.5517 |
| [0.60,0.70) | 10 | 0.4000 | 0.6462 |
| [0.70,0.80) | 12 | 0.4167 | 0.7404 |
| [0.80,0.90) | 20 | 0.2500 | 0.8517 |
| [0.90,1.00) | 3682 | 0.0187 | 0.9991 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 68 | 0.5000 | 0.5411 |
| [0.60,0.70) | 83 | 0.4096 | 0.6498 |
| [0.70,0.80) | 86 | 0.3256 | 0.7519 |
| [0.80,0.90) | 156 | 0.1987 | 0.8559 |
| [0.90,1.00) | 3340 | 0.0641 | 0.9922 |


## 验证集最佳点

```json
{
  "loss_total": 0.31255780610262685,
  "acc_main": 0.9677790563866513,
  "acc_turn": 0.8308400460299195,
  "acc_turn_pure": 0.8545953360768176,
  "acc_turn_transition": 0.7071428571428572,
  "flat_recall": 0.9076620825147348,
  "stall_recall": 0.9148936170212766,
  "slope_recall": 0.9839102876645539,
  "recall_main": [
    0.9076620825147348,
    0.9148936170212766,
    0.9839102876645539
  ],
  "turn_right_recall": 0.75,
  "turn_straight_recall": 0.860235003092146,
  "turn_left_recall": 0.8122605363984674,
  "recall_turn": [
    0.75,
    0.860235003092146,
    0.8122605363984674
  ],
  "cm_turn": [
    [
      351,
      85,
      32
    ],
    [
      105,
      1391,
      121
    ],
    [
      34,
      64,
      424
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      462,
      1,
      46
    ],
    [
      4,
      43,
      0
    ],
    [
      30,
      3,
      2018
    ]
  ],
  "main_confidence_mean": 0.9939872838447422,
  "main_confidence_error_mean": 0.911783081598197,
  "main_low_conf_0p60_ratio": 0.0038358266206367474,
  "main_low_conf_0p70_ratio": 0.006137322593018795,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 10,
      "error_rate": 0.5,
      "mean_confidence": 0.53224383010105
    },
    {
      "bin": "[0.60,0.70)",
      "n": 6,
      "error_rate": 0.8333333333333334,
      "mean_confidence": 0.6441243257321564
    },
    {
      "bin": "[0.70,0.80)",
      "n": 9,
      "error_rate": 0.4444444444444444,
      "mean_confidence": 0.7500551241406437
    },
    {
      "bin": "[0.80,0.90)",
      "n": 26,
      "error_rate": 0.3076923076923077,
      "mean_confidence": 0.8531008268548165
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2556,
      "error_rate": 0.024256651017214397,
      "mean_confidence": 0.9989070998092131
    }
  ],
  "turn_confidence_mean": 0.9467635777515637,
  "turn_confidence_error_mean": 0.8779238195077615,
  "turn_low_conf_0p60_ratio": 0.02838511699271193,
  "turn_low_conf_0p70_ratio": 0.06444188722669736,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 74,
      "error_rate": 0.4594594594594595,
      "mean_confidence": 0.5401387686977189
    },
    {
      "bin": "[0.60,0.70)",
      "n": 94,
      "error_rate": 0.4574468085106383,
      "mean_confidence": 0.6535689285018013
    },
    {
      "bin": "[0.70,0.80)",
      "n": 107,
      "error_rate": 0.38317757009345793,
      "mean_confidence": 0.7489893896756095
    },
    {
      "bin": "[0.80,0.90)",
      "n": 173,
      "error_rate": 0.30057803468208094,
      "mean_confidence": 0.8507598055849533
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2159,
      "error_rate": 0.12552107457156092,
      "mean_confidence": 0.9909604390801475
    }
  ],
  "theta_mae_rad": 0.00435176445171237,
  "theta_mae_deg": 0.24933771789073944,
  "uphill_recall": 0.7912844036697247,
  "downhill_recall": 0.8218849840255591,
  "slope_sign_acc": 0.98359375,
  "theta_flat_mae_deg": 0.28865471482276917,
  "theta_flat_abs_p95_deg": 1.9599807262420654,
  "theta_flat_abs_max_deg": 3.5392603874206543,
  "theta_flat_bias_deg": 0.15950629115104675,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.4211116135120392,
  "theta_near_flat_abs_p95_deg": 2.02339506149292,
  "theta_near_flat_abs_max_deg": 5.504773139953613,
  "theta_near_flat_bias_deg": 0.26933711767196655,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.36660870909690857,
  "theta_flat_turn_abs_p95_deg": 1.0337848663330078,
  "theta_flat_turn_abs_max_deg": 2.109945297241211,
  "theta_flat_turn_bias_deg": 0.3277069628238678,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.24933771789073944,
  "theta_slope_control_abs_p95_deg": 9.356292724609375,
  "theta_slope_control_abs_max_deg": 10.168055534362793,
  "theta_slope_control_bias_deg": 0.021658524870872498,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.24933774769306183,
  "theta_all_rmse_deg": 0.38692280650138855,
  "theta_all_p95_abs_err_deg": 0.7092292904853821,
  "theta_all_max_abs_err_deg": 3.5104455947875977,
  "theta_all_bias_deg": 0.021658524870872498,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.23958036303520203,
  "theta_active_abs_ge_2_rmse_deg": 0.36741873621940613,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.7018715143203735,
  "theta_active_abs_ge_2_max_abs_err_deg": 3.5104455947875977,
  "theta_active_abs_ge_2_bias_deg": -0.012551377527415752,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.25120359659194946,
  "theta_abs_le_8_rmse_deg": 0.386941134929657,
  "theta_abs_le_8_p95_abs_err_deg": 0.6683838367462158,
  "theta_abs_le_8_max_abs_err_deg": 3.5104455947875977,
  "theta_abs_le_8_bias_deg": 0.04195105656981468,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.24933774769306183,
  "theta_abs_le_10_rmse_deg": 0.38692280650138855,
  "theta_abs_le_10_p95_abs_err_deg": 0.7092292904853821,
  "theta_abs_le_10_max_abs_err_deg": 3.5104455947875977,
  "theta_abs_le_10_bias_deg": 0.021658524870872498,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.24238619208335876,
  "theta_pos_8_10_rmse_deg": 0.34469249844551086,
  "theta_pos_8_10_p95_abs_err_deg": 0.7451223731040955,
  "theta_pos_8_10_max_abs_err_deg": 1.4346226453781128,
  "theta_pos_8_10_bias_deg": -0.1924305558204651,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.2419826090335846,
  "theta_neg_10_8_rmse_deg": 0.42130887508392334,
  "theta_neg_10_8_p95_abs_err_deg": 0.8442039489746094,
  "theta_neg_10_8_max_abs_err_deg": 2.876800060272217,
  "theta_neg_10_8_bias_deg": 0.06670250743627548,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.2883118987083435,
  "theta_pos_6_8_rmse_deg": 0.36787644028663635,
  "theta_pos_6_8_p95_abs_err_deg": 0.7550666928291321,
  "theta_pos_6_8_max_abs_err_deg": 1.5381333827972412,
  "theta_pos_6_8_bias_deg": -0.2139796018600464,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.2327261120080948,
  "theta_neg_8_6_rmse_deg": 0.4534708857536316,
  "theta_neg_8_6_p95_abs_err_deg": 0.9121302962303162,
  "theta_neg_8_6_max_abs_err_deg": 2.1491811275482178,
  "theta_neg_8_6_bias_deg": 0.14265137910842896,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.20126232504844666,
  "theta_neg_4_2_rmse_deg": 0.2654760181903839,
  "theta_neg_4_2_p95_abs_err_deg": 0.5961486101150513,
  "theta_neg_4_2_max_abs_err_deg": 1.0551071166992188,
  "theta_neg_4_2_bias_deg": 0.11774425953626633,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.32668477296829224,
  "theta_neg_2_0p5_rmse_deg": 0.610142171382904,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.0008676052093506,
  "theta_neg_2_0p5_max_abs_err_deg": 3.2095530033111572,
  "theta_neg_2_0p5_bias_deg": 0.1535559892654419,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.24741753935813904,
  "theta_pos_0p5_2_rmse_deg": 0.320264995098114,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.5719219446182251,
  "theta_pos_0p5_2_max_abs_err_deg": 1.7672878503799438,
  "theta_pos_0p5_2_bias_deg": 0.18986640870571136,
  "theta_pos_0p5_2_n": 168.0
}
```
