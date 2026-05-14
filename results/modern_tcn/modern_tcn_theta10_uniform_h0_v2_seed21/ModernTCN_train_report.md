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
| acc_main | 0.9807 |
| acc_turn | 0.9022 |
| acc_turn_pure | 0.9234 |
| acc_turn_transition | 0.7757 |
| main_confidence_mean | 0.9953 |
| main_low_conf_0p60_ratio | 0.0024 |
| main_low_conf_0p70_ratio | 0.0054 |
| turn_confidence_mean | 0.9687 |
| turn_low_conf_0p60_ratio | 0.0177 |
| turn_low_conf_0p70_ratio | 0.0335 |
| turn_right_recall | 0.8770 |
| turn_straight_recall | 0.9209 |
| turn_left_recall | 0.8743 |
| theta_mae_deg | 0.2519 |
| theta_abs_le_10_p95_abs_err_deg | 0.8194 |
| theta_neg_10_8_p95_abs_err_deg | 0.6371 |
| theta_pos_8_10_p95_abs_err_deg | 0.7922 |
| theta_abs_le_8_p95_abs_err_deg | 0.8332 |
| theta_neg_8_6_p95_abs_err_deg | 0.5743 |
| theta_pos_6_8_p95_abs_err_deg | 0.3607 |
| theta_neg_2_0p5_p95_abs_err_deg | 0.6320 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.2936 |
| theta_flat_abs_p95_deg | 2.2232 |
| theta_flat_bias_deg | 0.0800 |
| theta_near_flat_abs_p95_deg | 1.2417 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.2034 |
| theta_flat_turn_abs_p95_deg | 0.6040 |
| flat_recall | 0.9657 |
| stall_recall | 0.6923 |
| slope_recall | 0.9965 |
| uphill_recall | 0.8106 |
| downhill_recall | 0.7805 |

- best_epoch: 158
- train_seconds: 584.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 9 | 0.1111 | 0.5409 |
| [0.60,0.70) | 11 | 0.4545 | 0.6631 |
| [0.70,0.80) | 10 | 0.5000 | 0.7569 |
| [0.80,0.90) | 25 | 0.2800 | 0.8473 |
| [0.90,1.00) | 3678 | 0.0147 | 0.9991 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 66 | 0.5758 | 0.5484 |
| [0.60,0.70) | 59 | 0.6102 | 0.6521 |
| [0.70,0.80) | 91 | 0.3956 | 0.7547 |
| [0.80,0.90) | 135 | 0.2519 | 0.8579 |
| [0.90,1.00) | 3382 | 0.0653 | 0.9926 |


## 验证集最佳点

```json
{
  "loss_total": 0.2685217440334096,
  "acc_main": 0.9766014576141159,
  "acc_turn": 0.8270042194092827,
  "acc_turn_pure": 0.8491083676268861,
  "acc_turn_transition": 0.7119047619047619,
  "flat_recall": 0.9489194499017681,
  "stall_recall": 0.9361702127659575,
  "slope_recall": 0.984397854705022,
  "recall_main": [
    0.9489194499017681,
    0.9361702127659575,
    0.984397854705022
  ],
  "turn_right_recall": 0.7799145299145299,
  "turn_straight_recall": 0.8441558441558441,
  "turn_left_recall": 0.8160919540229885,
  "recall_turn": [
    0.7799145299145299,
    0.8441558441558441,
    0.8160919540229885
  ],
  "cm_turn": [
    [
      365,
      74,
      29
    ],
    [
      127,
      1365,
      125
    ],
    [
      19,
      77,
      426
    ]
  ],
  "n_turn_transition": 420,
  "n_turn_pure": 2187,
  "cm_main": [
    [
      483,
      0,
      26
    ],
    [
      3,
      44,
      0
    ],
    [
      29,
      3,
      2019
    ]
  ],
  "main_confidence_mean": 0.9922840638032082,
  "main_confidence_error_mean": 0.9107919802141997,
  "main_low_conf_0p60_ratio": 0.0023014959723820483,
  "main_low_conf_0p70_ratio": 0.009589566551591868,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 6,
      "error_rate": 0.16666666666666666,
      "mean_confidence": 0.5270272889234424
    },
    {
      "bin": "[0.60,0.70)",
      "n": 19,
      "error_rate": 0.3684210526315789,
      "mean_confidence": 0.6561620783842912
    },
    {
      "bin": "[0.70,0.80)",
      "n": 21,
      "error_rate": 0.19047619047619047,
      "mean_confidence": 0.7605675029246005
    },
    {
      "bin": "[0.80,0.90)",
      "n": 20,
      "error_rate": 0.35,
      "mean_confidence": 0.8465431787463373
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2541,
      "error_rate": 0.01652892561983471,
      "mean_confidence": 0.9989580991640215
    }
  ],
  "turn_confidence_mean": 0.9511314373068405,
  "turn_confidence_error_mean": 0.8848313293239072,
  "turn_low_conf_0p60_ratio": 0.03452243958573072,
  "turn_low_conf_0p70_ratio": 0.06405830456463368,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 90,
      "error_rate": 0.5222222222222223,
      "mean_confidence": 0.5427805824149844
    },
    {
      "bin": "[0.60,0.70)",
      "n": 77,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.6540237612597382
    },
    {
      "bin": "[0.70,0.80)",
      "n": 70,
      "error_rate": 0.44285714285714284,
      "mean_confidence": 0.7471392028389419
    },
    {
      "bin": "[0.80,0.90)",
      "n": 144,
      "error_rate": 0.2708333333333333,
      "mean_confidence": 0.8516384414420672
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2226,
      "error_rate": 0.13522012578616352,
      "mean_confidence": 0.9907699439614562
    }
  ],
  "theta_mae_rad": 0.003965418785810471,
  "theta_mae_deg": 0.22720174491405487,
  "uphill_recall": 0.7836391437308868,
  "downhill_recall": 0.8146964856230032,
  "slope_sign_acc": 0.989453125,
  "theta_flat_mae_deg": 0.2174038141965866,
  "theta_flat_abs_p95_deg": 1.8140497207641602,
  "theta_flat_abs_max_deg": 2.7483766078948975,
  "theta_flat_bias_deg": 0.11808016896247864,
  "theta_flat_n": 509.0,
  "theta_near_flat_mae_deg": 0.33203622698783875,
  "theta_near_flat_abs_p95_deg": 1.4986138343811035,
  "theta_near_flat_abs_max_deg": 5.271884441375732,
  "theta_near_flat_bias_deg": 0.19061267375946045,
  "theta_near_flat_n": 212.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.23146045207977295,
  "theta_flat_turn_abs_p95_deg": 0.932413637638092,
  "theta_flat_turn_abs_max_deg": 1.5366806983947754,
  "theta_flat_turn_bias_deg": 0.13291394710540771,
  "theta_flat_turn_n": 94.0,
  "theta_slope_control_mae_deg": 0.22720174491405487,
  "theta_slope_control_abs_p95_deg": 9.4476900100708,
  "theta_slope_control_abs_max_deg": 10.106236457824707,
  "theta_slope_control_bias_deg": 0.024743255227804184,
  "theta_slope_control_n": 2560.0,
  "theta_all_mae_deg": 0.22720174491405487,
  "theta_all_rmse_deg": 0.36415982246398926,
  "theta_all_p95_abs_err_deg": 0.626933217048645,
  "theta_all_max_abs_err_deg": 2.9658844470977783,
  "theta_all_bias_deg": 0.024743253365159035,
  "theta_all_n": 2560.0,
  "theta_active_abs_ge_2_mae_deg": 0.22963331639766693,
  "theta_active_abs_ge_2_rmse_deg": 0.3650057315826416,
  "theta_active_abs_ge_2_p95_abs_err_deg": 0.6323550939559937,
  "theta_active_abs_ge_2_max_abs_err_deg": 2.9658844470977783,
  "theta_active_abs_ge_2_bias_deg": 0.0015796798979863524,
  "theta_active_abs_ge_2_n": 2051.0,
  "theta_abs_le_8_mae_deg": 0.22276100516319275,
  "theta_abs_le_8_rmse_deg": 0.3555343449115753,
  "theta_abs_le_8_p95_abs_err_deg": 0.6159305572509766,
  "theta_abs_le_8_max_abs_err_deg": 2.8939270973205566,
  "theta_abs_le_8_bias_deg": 0.05174380913376808,
  "theta_abs_le_8_n": 2031.0,
  "theta_abs_le_10_mae_deg": 0.22720174491405487,
  "theta_abs_le_10_rmse_deg": 0.36415982246398926,
  "theta_abs_le_10_p95_abs_err_deg": 0.626933217048645,
  "theta_abs_le_10_max_abs_err_deg": 2.9658844470977783,
  "theta_abs_le_10_bias_deg": 0.024743253365159035,
  "theta_abs_le_10_n": 2560.0,
  "theta_pos_8_10_mae_deg": 0.27189189195632935,
  "theta_pos_8_10_rmse_deg": 0.38345715403556824,
  "theta_pos_8_10_p95_abs_err_deg": 0.7172014117240906,
  "theta_pos_8_10_max_abs_err_deg": 1.7105149030685425,
  "theta_pos_8_10_bias_deg": -0.17281639575958252,
  "theta_pos_8_10_n": 251.0,
  "theta_neg_10_8_mae_deg": 0.21929503977298737,
  "theta_neg_10_8_rmse_deg": 0.4061262309551239,
  "theta_neg_10_8_p95_abs_err_deg": 0.5491976737976074,
  "theta_neg_10_8_max_abs_err_deg": 2.9658844470977783,
  "theta_neg_10_8_bias_deg": 0.005855991505086422,
  "theta_neg_10_8_n": 278.0,
  "theta_pos_6_8_mae_deg": 0.2776012420654297,
  "theta_pos_6_8_rmse_deg": 0.36882710456848145,
  "theta_pos_6_8_p95_abs_err_deg": 0.799138069152832,
  "theta_pos_6_8_max_abs_err_deg": 1.1959089040756226,
  "theta_pos_6_8_bias_deg": -0.152593731880188,
  "theta_pos_6_8_n": 241.0,
  "theta_neg_8_6_mae_deg": 0.2756602466106415,
  "theta_neg_8_6_rmse_deg": 0.5338074564933777,
  "theta_neg_8_6_p95_abs_err_deg": 1.0158432722091675,
  "theta_neg_8_6_max_abs_err_deg": 2.7443058490753174,
  "theta_neg_8_6_bias_deg": 0.20470699667930603,
  "theta_neg_8_6_n": 251.0,
  "theta_neg_4_2_mae_deg": 0.20217351615428925,
  "theta_neg_4_2_rmse_deg": 0.2578577697277069,
  "theta_neg_4_2_p95_abs_err_deg": 0.4966929852962494,
  "theta_neg_4_2_max_abs_err_deg": 0.8502150774002075,
  "theta_neg_4_2_bias_deg": 0.009564227424561977,
  "theta_neg_4_2_n": 198.0,
  "theta_neg_2_0p5_mae_deg": 0.2532781958580017,
  "theta_neg_2_0p5_rmse_deg": 0.5182327032089233,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.1159058809280396,
  "theta_neg_2_0p5_max_abs_err_deg": 2.8939270973205566,
  "theta_neg_2_0p5_bias_deg": 0.19435307383537292,
  "theta_neg_2_0p5_n": 138.0,
  "theta_pos_0p5_2_mae_deg": 0.1782468557357788,
  "theta_pos_0p5_2_rmse_deg": 0.2283606082201004,
  "theta_pos_0p5_2_p95_abs_err_deg": 0.4243556559085846,
  "theta_pos_0p5_2_max_abs_err_deg": 0.976404070854187,
  "theta_pos_0p5_2_bias_deg": 0.10418562591075897,
  "theta_pos_0p5_2_n": 168.0
}
```
