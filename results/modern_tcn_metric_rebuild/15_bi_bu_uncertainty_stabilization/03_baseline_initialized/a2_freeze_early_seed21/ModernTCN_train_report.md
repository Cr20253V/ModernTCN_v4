# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `bounded_uncertainty`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=128, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## E2 hard-sample focal settings

- lambda_transition_focal: `0.0`
- lambda_stall_focal: `0.0`
- lambda_theta_smooth: `0.0`
- focal_gamma: `2.0`
- theta_smooth_mode: `off`
- theta_smooth_status: `disabled_contract_limited`

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
  "command_dropout_prob": 0.0,
  "command_dropout_start_index": -1,
  "command_dropout_feature_count": 0,
  "command_dropout_mode": "window_block",
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
  "lambda_theta_error_excess": 0.0,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.0,
  "lambda_theta_active_excess": 0.0,
  "lambda_theta_small_neg": 0.0,
  "lambda_theta_small_neg_excess": 0.0,
  "lambda_turn_release": 0.0,
  "lambda_false_turn_straight": 0.0,
  "lambda_transition_focal": 0.0,
  "lambda_stall_focal": 0.0,
  "lambda_theta_smooth": 0.0,
  "focal_gamma": 2.0,
  "theta_smooth_mode": "off",
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
    1.0,
    1.1,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_turn_lr_weight": 0.0,
  "select_turn_lr_target": 0.8,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.15,
  "select_theta_ref_deg": 5.0,
  "select_theta_p95_weight": 0.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 0.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 0.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.0,
  "select_theta_extreme_p95_target_deg": 1.0,
  "select_theta_edge_p95_weight": 0.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.0,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2,
  "freeze_mode": "early_blocks",
  "freeze_early_blocks": 3,
  "preserve_mode": "baseline",
  "lambda_preserve_main": 0.05,
  "lambda_preserve_turn": 0.05,
  "lambda_preserve_theta": 0.05,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9647 |
| acc_turn | 0.6002 |
| acc_turn_pure | 0.6179 |
| acc_turn_transition | 0.5231 |
| main_confidence_mean | 0.9902 |
| main_low_conf_0p60_ratio | 0.0036 |
| main_low_conf_0p70_ratio | 0.0075 |
| turn_confidence_mean | 0.8292 |
| turn_low_conf_0p60_ratio | 0.1483 |
| turn_low_conf_0p70_ratio | 0.2640 |
| turn_right_recall | 0.5907 |
| turn_straight_recall | 0.6094 |
| turn_left_recall | 0.5885 |
| theta_mae_deg | 0.6692 |
| theta_abs_le_10_p95_abs_err_deg | 1.7166 |
| theta_neg_10_8_p95_abs_err_deg | 1.4401 |
| theta_pos_8_10_p95_abs_err_deg | 2.8893 |
| theta_abs_le_8_p95_abs_err_deg | 1.6923 |
| theta_neg_8_6_p95_abs_err_deg | 1.7176 |
| theta_pos_6_8_p95_abs_err_deg | 1.7314 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.2959 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4036 |
| theta_flat_abs_p95_deg | 2.3560 |
| theta_flat_bias_deg | -0.0173 |
| theta_near_flat_abs_p95_deg | 1.9660 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1502 |
| theta_flat_turn_abs_p95_deg | 2.0194 |
| flat_recall | 0.9537 |
| stall_recall | 0.6979 |
| slope_recall | 0.9771 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0833 |
| uphill_recall | 0.7563 |
| downhill_recall | 0.7963 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    0,
    35
  ],
  [
    8,
    67,
    21
  ],
  [
    58,
    5,
    2687
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    472,
    209,
    118
  ],
  [
    386,
    1178,
    369
  ],
  [
    172,
    186,
    512
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.361945 |
| test_loss_turn_bundle_base | 0.292641 |
| test_loss_theta_bundle_base | 0.000160 |
| test_loss_transition_focal_raw | 1.427567 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.811140 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 1
- train_seconds: 5.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 13 | 0.5385 | 0.5404 |
| [0.60,0.70) | 14 | 0.5000 | 0.6537 |
| [0.70,0.80) | 38 | 0.5000 | 0.7653 |
| [0.80,0.90) | 45 | 0.3778 | 0.8630 |
| [0.90,1.00) | 3492 | 0.0221 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 534 | 0.5243 | 0.5244 |
| [0.60,0.70) | 417 | 0.5923 | 0.6485 |
| [0.70,0.80) | 380 | 0.5000 | 0.7498 |
| [0.80,0.90) | 510 | 0.4373 | 0.8522 |
| [0.90,1.00) | 1761 | 0.2839 | 0.9750 |


## 验证集最佳点

```json
{
  "loss_total": 0.5770755905259769,
  "acc_main": 0.9485791610284168,
  "acc_turn": 0.627063599458728,
  "acc_turn_pure": 0.6411012782694199,
  "acc_turn_transition": 0.5605590062111802,
  "false_turn_straight": 0.43607068607068605,
  "flat_recall": 0.9558599695585996,
  "stall_recall": 0.47619047619047616,
  "slope_recall": 0.9536048064085447,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9558599695585996,
    0.47619047619047616,
    0.9536048064085447
  ],
  "turn_right_recall": 0.6812796208530806,
  "turn_straight_recall": 0.5639293139293139,
  "turn_left_recall": 0.7087378640776699,
  "recall_turn": [
    0.6812796208530806,
    0.5639293139293139,
    0.7087378640776699
  ],
  "cm_turn": [
    [
      575,
      214,
      55
    ],
    [
      403,
      1085,
      436
    ],
    [
      91,
      179,
      657
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
      0,
      20,
      22
    ],
    [
      133,
      6,
      2857
    ]
  ],
  "main_confidence_mean": 0.9689166687293386,
  "main_confidence_error_mean": 0.756903197867876,
  "main_low_conf_0p60_ratio": 0.052232746955345064,
  "main_low_conf_0p70_ratio": 0.0571041948579161,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 193,
      "error_rate": 0.43523316062176165,
      "mean_confidence": 0.5385545711623622
    },
    {
      "bin": "[0.60,0.70)",
      "n": 18,
      "error_rate": 0.5,
      "mean_confidence": 0.648219412212184
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7634413845488585
    },
    {
      "bin": "[0.80,0.90)",
      "n": 47,
      "error_rate": 0.2127659574468085,
      "mean_confidence": 0.8542759558358606
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3416,
      "error_rate": 0.022833723653395786,
      "mean_confidence": 0.9977619643738113
    }
  ],
  "turn_confidence_mean": 0.8408331503289374,
  "turn_confidence_error_mean": 0.7684337431572854,
  "turn_low_conf_0p60_ratio": 0.15426251691474965,
  "turn_low_conf_0p70_ratio": 0.2411366711772666,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 570,
      "error_rate": 0.631578947368421,
      "mean_confidence": 0.5061487362133514
    },
    {
      "bin": "[0.60,0.70)",
      "n": 321,
      "error_rate": 0.48909657320872274,
      "mean_confidence": 0.653049940301111
    },
    {
      "bin": "[0.70,0.80)",
      "n": 346,
      "error_rate": 0.44508670520231214,
      "mean_confidence": 0.7513917059365284
    },
    {
      "bin": "[0.80,0.90)",
      "n": 448,
      "error_rate": 0.46875,
      "mean_confidence": 0.8533473077815376
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2010,
      "error_rate": 0.2472636815920398,
      "mean_confidence": 0.9783400775358154
    }
  ],
  "theta_mae_rad": 0.014285760931670666,
  "theta_mae_deg": 0.8185137510299683,
  "uphill_recall": 0.7789757412398922,
  "downhill_recall": 0.8014460511679644,
  "slope_sign_acc": 0.9756364631809472,
  "theta_flat_mae_deg": 1.1257271766662598,
  "theta_flat_abs_p95_deg": 3.8302993774414062,
  "theta_flat_abs_max_deg": 7.930609703063965,
  "theta_flat_bias_deg": 0.4593295156955719,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.396920084953308,
  "theta_near_flat_abs_p95_deg": 3.850989580154419,
  "theta_near_flat_abs_max_deg": 7.930609703063965,
  "theta_near_flat_bias_deg": 0.68255615234375,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.047245740890503,
  "theta_flat_turn_abs_p95_deg": 3.8302993774414062,
  "theta_flat_turn_abs_max_deg": 7.930609703063965,
  "theta_flat_turn_bias_deg": 0.08089812844991684,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8185137510299683,
  "theta_slope_control_abs_p95_deg": 9.126331329345703,
  "theta_slope_control_abs_max_deg": 12.236664772033691,
  "theta_slope_control_bias_deg": 0.3292068839073181,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.818513810634613,
  "theta_all_rmse_deg": 1.2235455513000488,
  "theta_all_p95_abs_err_deg": 2.5849449634552,
  "theta_all_max_abs_err_deg": 7.430610179901123,
  "theta_all_bias_deg": 0.3292068839073181,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.751144289970398,
  "theta_active_abs_ge_2_rmse_deg": 1.117106556892395,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2672486305236816,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.966184616088867,
  "theta_active_abs_ge_2_bias_deg": 0.3006719946861267,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8597874045372009,
  "theta_abs_le_8_rmse_deg": 1.2659915685653687,
  "theta_abs_le_8_p95_abs_err_deg": 2.723856210708618,
  "theta_abs_le_8_max_abs_err_deg": 7.430610179901123,
  "theta_abs_le_8_bias_deg": 0.35890302062034607,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.818513810634613,
  "theta_abs_le_10_rmse_deg": 1.2235455513000488,
  "theta_abs_le_10_p95_abs_err_deg": 2.5849449634552,
  "theta_abs_le_10_max_abs_err_deg": 7.430610179901123,
  "theta_abs_le_10_bias_deg": 0.3292068839073181,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5440937876701355,
  "theta_pos_8_10_rmse_deg": 0.7226104736328125,
  "theta_pos_8_10_p95_abs_err_deg": 1.2316774129867554,
  "theta_pos_8_10_max_abs_err_deg": 3.6533091068267822,
  "theta_pos_8_10_bias_deg": -0.12541377544403076,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7464377880096436,
  "theta_neg_10_8_rmse_deg": 1.2607741355895996,
  "theta_neg_10_8_p95_abs_err_deg": 2.4223544597625732,
  "theta_neg_10_8_max_abs_err_deg": 6.966184616088867,
  "theta_neg_10_8_bias_deg": 0.5389719009399414,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5420584678649902,
  "theta_pos_6_8_rmse_deg": 0.7553209662437439,
  "theta_pos_6_8_p95_abs_err_deg": 1.4847043752670288,
  "theta_pos_6_8_max_abs_err_deg": 3.43595290184021,
  "theta_pos_6_8_bias_deg": 0.2337976098060608,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8132849335670471,
  "theta_neg_8_6_rmse_deg": 1.1925591230392456,
  "theta_neg_8_6_p95_abs_err_deg": 2.2773444652557373,
  "theta_neg_8_6_max_abs_err_deg": 6.157627582550049,
  "theta_neg_8_6_bias_deg": 0.09324310719966888,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7667927145957947,
  "theta_neg_4_2_rmse_deg": 1.0541036128997803,
  "theta_neg_4_2_p95_abs_err_deg": 2.183377742767334,
  "theta_neg_4_2_max_abs_err_deg": 3.9510459899902344,
  "theta_neg_4_2_bias_deg": 0.32332324981689453,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6167334318161011,
  "theta_neg_2_0p5_rmse_deg": 0.8737844228744507,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.9302208423614502,
  "theta_neg_2_0p5_max_abs_err_deg": 4.100710391998291,
  "theta_neg_2_0p5_bias_deg": -0.1554151475429535,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.404213309288025,
  "theta_pos_0p5_2_rmse_deg": 1.6618719100952148,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.3302993774414062,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9111275672912598,
  "theta_pos_0p5_2_bias_deg": 1.0006517171859741,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3112841760434704,
  "loss_turn": 1.3275624714943004,
  "loss_theta": 0.0004560783155406138,
  "loss_main_bundle_base": 0.3112841760434704,
  "loss_turn_bundle_base": 0.2655124986970215,
  "loss_theta_bundle_base": 0.00027891826946338755,
  "loss_main_bundle": 0.3112841760434704,
  "loss_turn_bundle": 0.2655124986970215,
  "loss_theta_bundle": 0.00027891826946338755,
  "loss_theta_flat": 0.0002339599118158423,
  "loss_theta_near_flat": 0.0013068451628048623,
  "loss_theta_error_excess": 0.0001649579120921513,
  "loss_theta_flat_excess": 0.0001310858236016461,
  "loss_theta_near_flat_excess": 0.0009290350089101714,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001265291206813411,
  "loss_theta_small_neg": 0.00033740793989343675,
  "loss_theta_small_neg_excess": 8.195742300515604e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4002958425004363,
  "loss_false_turn_straight": 0.3208025624690746,
  "loss_transition_focal_raw": 1.194334182461802,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.0923739563770964,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0,
  "preserve_loss": 0.00261217774823308
}
```
