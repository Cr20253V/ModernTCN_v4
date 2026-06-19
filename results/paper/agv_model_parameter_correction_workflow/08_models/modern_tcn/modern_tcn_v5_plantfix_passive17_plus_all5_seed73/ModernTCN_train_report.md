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
| acc_main | 0.9650 |
| acc_turn | 0.5738 |
| acc_turn_pure | 0.5954 |
| acc_turn_transition | 0.4799 |
| main_confidence_mean | 0.9862 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0183 |
| turn_confidence_mean | 0.7453 |
| turn_low_conf_0p60_ratio | 0.2754 |
| turn_low_conf_0p70_ratio | 0.4309 |
| turn_right_recall | 0.6070 |
| turn_straight_recall | 0.5913 |
| turn_left_recall | 0.5046 |
| theta_mae_deg | 0.7123 |
| theta_abs_le_10_p95_abs_err_deg | 2.1703 |
| theta_neg_10_8_p95_abs_err_deg | 1.1765 |
| theta_pos_8_10_p95_abs_err_deg | 2.8365 |
| theta_abs_le_8_p95_abs_err_deg | 2.1530 |
| theta_neg_8_6_p95_abs_err_deg | 1.4588 |
| theta_pos_6_8_p95_abs_err_deg | 1.4703 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.6402 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.4225 |
| theta_flat_abs_p95_deg | 2.7790 |
| theta_flat_bias_deg | -0.4945 |
| theta_near_flat_abs_p95_deg | 2.0186 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3436 |
| theta_flat_turn_abs_p95_deg | 1.7421 |
| flat_recall | 0.9577 |
| stall_recall | 0.6250 |
| slope_recall | 0.9789 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7980 |

- best_epoch: 54
- train_seconds: 753.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.4167 | 0.5552 |
| [0.60,0.70) | 42 | 0.3095 | 0.6591 |
| [0.70,0.80) | 35 | 0.4000 | 0.7532 |
| [0.80,0.90) | 48 | 0.2292 | 0.8541 |
| [0.90,1.00) | 3453 | 0.0226 | 0.9974 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 992 | 0.5726 | 0.5151 |
| [0.60,0.70) | 560 | 0.4839 | 0.6471 |
| [0.70,0.80) | 515 | 0.4330 | 0.7512 |
| [0.80,0.90) | 516 | 0.3721 | 0.8489 |
| [0.90,1.00) | 1019 | 0.2758 | 0.9677 |


## 验证集最佳点

```json
{
  "loss_total": 0.3684342003239669,
  "acc_main": 0.9477672530446549,
  "acc_turn": 0.6186738836265223,
  "acc_turn_pure": 0.6273352999016716,
  "acc_turn_transition": 0.577639751552795,
  "flat_recall": 0.9604261796042618,
  "stall_recall": 0.2619047619047619,
  "slope_recall": 0.9546061415220294,
  "recall_main": [
    0.9604261796042618,
    0.2619047619047619,
    0.9546061415220294
  ],
  "turn_right_recall": 0.6267772511848341,
  "turn_straight_recall": 0.6008316008316008,
  "turn_left_recall": 0.6483279395900755,
  "recall_turn": [
    0.6267772511848341,
    0.6008316008316008,
    0.6483279395900755
  ],
  "cm_turn": [
    [
      529,
      210,
      105
    ],
    [
      348,
      1156,
      420
    ],
    [
      88,
      238,
      601
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      631,
      0,
      26
    ],
    [
      1,
      11,
      30
    ],
    [
      133,
      3,
      2860
    ]
  ],
  "main_confidence_mean": 0.9822009721722139,
  "main_confidence_error_mean": 0.863074490243351,
  "main_low_conf_0p60_ratio": 0.0035182679296346412,
  "main_low_conf_0p70_ratio": 0.008119079837618403,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 13,
      "error_rate": 0.6153846153846154,
      "mean_confidence": 0.5537136081443428
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.35294117647058826,
      "mean_confidence": 0.6476314297147824
    },
    {
      "bin": "[0.70,0.80)",
      "n": 37,
      "error_rate": 0.32432432432432434,
      "mean_confidence": 0.7517225836679627
    },
    {
      "bin": "[0.80,0.90)",
      "n": 207,
      "error_rate": 0.42995169082125606,
      "mean_confidence": 0.8182240837907734
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3421,
      "error_rate": 0.0228003507746273,
      "mean_confidence": 0.9979065945702713
    }
  ],
  "turn_confidence_mean": 0.7611892341738096,
  "turn_confidence_error_mean": 0.6813822535836802,
  "turn_low_conf_0p60_ratio": 0.2679296346414073,
  "turn_low_conf_0p70_ratio": 0.3899864682002706,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 990,
      "error_rate": 0.598989898989899,
      "mean_confidence": 0.5060872560371908
    },
    {
      "bin": "[0.60,0.70)",
      "n": 451,
      "error_rate": 0.4611973392461197,
      "mean_confidence": 0.6511827681925669
    },
    {
      "bin": "[0.70,0.80)",
      "n": 493,
      "error_rate": 0.40162271805273836,
      "mean_confidence": 0.7490376818372443
    },
    {
      "bin": "[0.80,0.90)",
      "n": 520,
      "error_rate": 0.325,
      "mean_confidence": 0.8492455338184062
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1241,
      "error_rate": 0.19419822723609992,
      "mean_confidence": 0.9726036693063876
    }
  ],
  "theta_mae_rad": 0.01405459363013506,
  "theta_mae_deg": 0.8052688241004944,
  "uphill_recall": 0.7805929919137466,
  "downhill_recall": 0.7997775305895439,
  "slope_sign_acc": 0.9753627155762387,
  "theta_flat_mae_deg": 1.1416915655136108,
  "theta_flat_abs_p95_deg": 3.0545175075531006,
  "theta_flat_abs_max_deg": 7.468991756439209,
  "theta_flat_bias_deg": 0.19631575047969818,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5489410161972046,
  "theta_near_flat_abs_p95_deg": 4.384131908416748,
  "theta_near_flat_abs_max_deg": 7.468991756439209,
  "theta_near_flat_bias_deg": 0.8971349596977234,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.3551709651947021,
  "theta_flat_turn_abs_p95_deg": 4.429324150085449,
  "theta_flat_turn_abs_max_deg": 7.468991756439209,
  "theta_flat_turn_bias_deg": 0.7083152532577515,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8052688241004944,
  "theta_slope_control_abs_p95_deg": 9.643709182739258,
  "theta_slope_control_abs_max_deg": 12.483777046203613,
  "theta_slope_control_bias_deg": 0.01766626536846161,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8052688837051392,
  "theta_all_rmse_deg": 1.1693010330200195,
  "theta_all_p95_abs_err_deg": 2.486107110977173,
  "theta_all_max_abs_err_deg": 7.968991279602051,
  "theta_all_bias_deg": 0.017666269093751907,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7314938902854919,
  "theta_active_abs_ge_2_rmse_deg": 1.0523335933685303,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.055493116378784,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.385671615600586,
  "theta_active_abs_ge_2_bias_deg": -0.021510206162929535,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.845572829246521,
  "theta_abs_le_8_rmse_deg": 1.191818118095398,
  "theta_abs_le_8_p95_abs_err_deg": 2.5497984886169434,
  "theta_abs_le_8_max_abs_err_deg": 7.968991279602051,
  "theta_abs_le_8_bias_deg": -0.031293462961912155,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8052688837051392,
  "theta_abs_le_10_rmse_deg": 1.1693010330200195,
  "theta_abs_le_10_p95_abs_err_deg": 2.486107110977173,
  "theta_abs_le_10_max_abs_err_deg": 7.968991279602051,
  "theta_abs_le_10_bias_deg": 0.017666269093751907,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5999628305435181,
  "theta_pos_8_10_rmse_deg": 0.9782715439796448,
  "theta_pos_8_10_p95_abs_err_deg": 2.0788795948028564,
  "theta_pos_8_10_max_abs_err_deg": 5.757197380065918,
  "theta_pos_8_10_bias_deg": 0.2480776458978653,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6711347699165344,
  "theta_neg_10_8_rmse_deg": 1.1541948318481445,
  "theta_neg_10_8_p95_abs_err_deg": 1.9845237731933594,
  "theta_neg_10_8_max_abs_err_deg": 7.385671615600586,
  "theta_neg_10_8_bias_deg": 0.1999223679304123,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.7998435497283936,
  "theta_pos_6_8_rmse_deg": 1.0985054969787598,
  "theta_pos_6_8_p95_abs_err_deg": 1.9580633640289307,
  "theta_pos_6_8_max_abs_err_deg": 4.9880571365356445,
  "theta_pos_6_8_bias_deg": -0.10774262249469757,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7403455972671509,
  "theta_neg_8_6_rmse_deg": 1.0677176713943481,
  "theta_neg_8_6_p95_abs_err_deg": 2.132138967514038,
  "theta_neg_8_6_max_abs_err_deg": 7.2283616065979,
  "theta_neg_8_6_bias_deg": -0.054360657930374146,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8104938864707947,
  "theta_neg_4_2_rmse_deg": 1.1090036630630493,
  "theta_neg_4_2_p95_abs_err_deg": 2.1542811393737793,
  "theta_neg_4_2_max_abs_err_deg": 5.28123140335083,
  "theta_neg_4_2_bias_deg": -0.4139518439769745,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8872130513191223,
  "theta_neg_2_0p5_rmse_deg": 1.0969116687774658,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8395230770111084,
  "theta_neg_2_0p5_max_abs_err_deg": 5.238942623138428,
  "theta_neg_2_0p5_bias_deg": -0.7599159479141235,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9132276773452759,
  "theta_pos_0p5_2_rmse_deg": 1.152083158493042,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.89145028591156,
  "theta_pos_0p5_2_max_abs_err_deg": 4.4982075691223145,
  "theta_pos_0p5_2_bias_deg": 0.24357132613658905,
  "theta_pos_0p5_2_n": 163.0
}
```
