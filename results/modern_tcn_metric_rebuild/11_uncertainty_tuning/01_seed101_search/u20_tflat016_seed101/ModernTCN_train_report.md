# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `uncertainty_weighting`
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
  "lambda_theta_flat": 0.16,
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
    1.4,
    0.8,
    1.4
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 2.5,
  "select_turn_weight": 0.55,
  "select_turn_transition_weight": 1.2,
  "select_turn_transition_target": 0.82,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.88,
  "select_turn_lr_weight": 0.6,
  "select_turn_lr_target": 0.88,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
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
| acc_main | 0.9714 |
| acc_turn | 0.5702 |
| acc_turn_pure | 0.5902 |
| acc_turn_transition | 0.4829 |
| main_confidence_mean | 0.9889 |
| main_low_conf_0p60_ratio | 0.0083 |
| main_low_conf_0p70_ratio | 0.0144 |
| turn_confidence_mean | 0.8111 |
| turn_low_conf_0p60_ratio | 0.1816 |
| turn_low_conf_0p70_ratio | 0.2976 |
| turn_right_recall | 0.5620 |
| turn_straight_recall | 0.5722 |
| turn_left_recall | 0.5736 |
| theta_mae_deg | 0.6946 |
| theta_abs_le_10_p95_abs_err_deg | 1.9649 |
| theta_neg_10_8_p95_abs_err_deg | 1.2367 |
| theta_pos_8_10_p95_abs_err_deg | 3.6885 |
| theta_abs_le_8_p95_abs_err_deg | 1.7690 |
| theta_neg_8_6_p95_abs_err_deg | 1.4401 |
| theta_pos_6_8_p95_abs_err_deg | 1.8935 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3418 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7660 |
| theta_flat_abs_p95_deg | 2.3883 |
| theta_flat_bias_deg | -0.1096 |
| theta_near_flat_abs_p95_deg | 1.4143 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.0182 |
| theta_flat_turn_abs_p95_deg | 1.3714 |
| flat_recall | 0.9735 |
| stall_recall | 0.7083 |
| slope_recall | 0.9800 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7575 |
| downhill_recall | 0.7911 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    736,
    0,
    20
  ],
  [
    9,
    68,
    19
  ],
  [
    49,
    6,
    2695
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    449,
    215,
    135
  ],
  [
    349,
    1106,
    478
  ],
  [
    180,
    191,
    499
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.315853 |
| test_loss_turn_bundle_base | 0.310638 |
| test_loss_theta_bundle_base | 0.000201 |
| test_loss_transition_focal_raw | 1.342863 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.535649 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 63
- train_seconds: 316.2

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 30 | 0.4000 | 0.5373 |
| [0.60,0.70) | 22 | 0.3182 | 0.6450 |
| [0.70,0.80) | 14 | 0.2857 | 0.7446 |
| [0.80,0.90) | 39 | 0.3333 | 0.8588 |
| [0.90,1.00) | 3497 | 0.0192 | 0.9973 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 654 | 0.6086 | 0.5236 |
| [0.60,0.70) | 418 | 0.5502 | 0.6488 |
| [0.70,0.80) | 434 | 0.5184 | 0.7499 |
| [0.80,0.90) | 512 | 0.4590 | 0.8529 |
| [0.90,1.00) | 1584 | 0.2904 | 0.9758 |


## 验证集最佳点

```json
{
  "loss_total": 0.5862990919243499,
  "acc_main": 0.9512855209742895,
  "acc_turn": 0.6292286874154263,
  "acc_turn_pure": 0.6424123238282531,
  "acc_turn_transition": 0.5667701863354038,
  "false_turn_straight": 0.4371101871101871,
  "flat_recall": 0.974124809741248,
  "stall_recall": 0.4523809523809524,
  "slope_recall": 0.9532710280373832,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.974124809741248,
    0.4523809523809524,
    0.9532710280373832
  ],
  "turn_right_recall": 0.6149289099526066,
  "turn_straight_recall": 0.5628898128898129,
  "turn_left_recall": 0.7799352750809061,
  "recall_turn": [
    0.6149289099526066,
    0.5628898128898129,
    0.7799352750809061
  ],
  "cm_turn": [
    [
      519,
      208,
      117
    ],
    [
      309,
      1083,
      532
    ],
    [
      33,
      171,
      723
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      640,
      0,
      17
    ],
    [
      0,
      19,
      23
    ],
    [
      132,
      8,
      2856
    ]
  ],
  "main_confidence_mean": 0.9692542372578254,
  "main_confidence_error_mean": 0.7438245407259321,
  "main_low_conf_0p60_ratio": 0.04871447902571042,
  "main_low_conf_0p70_ratio": 0.05412719891745602,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 180,
      "error_rate": 0.46111111111111114,
      "mean_confidence": 0.5099125589485122
    },
    {
      "bin": "[0.60,0.70)",
      "n": 20,
      "error_rate": 0.25,
      "mean_confidence": 0.6637271751876994
    },
    {
      "bin": "[0.70,0.80)",
      "n": 28,
      "error_rate": 0.2857142857142857,
      "mean_confidence": 0.7578832690913455
    },
    {
      "bin": "[0.80,0.90)",
      "n": 25,
      "error_rate": 0.12,
      "mean_confidence": 0.8505138890664375
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3442,
      "error_rate": 0.023532829750145264,
      "mean_confidence": 0.9976327785566415
    }
  ],
  "turn_confidence_mean": 0.8306997459577202,
  "turn_confidence_error_mean": 0.7533283888311838,
  "turn_low_conf_0p60_ratio": 0.16129905277401896,
  "turn_low_conf_0p70_ratio": 0.2522327469553451,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 596,
      "error_rate": 0.6325503355704698,
      "mean_confidence": 0.500671822310228
    },
    {
      "bin": "[0.60,0.70)",
      "n": 336,
      "error_rate": 0.5535714285714286,
      "mean_confidence": 0.6480094819765092
    },
    {
      "bin": "[0.70,0.80)",
      "n": 390,
      "error_rate": 0.41794871794871796,
      "mean_confidence": 0.7513769969554909
    },
    {
      "bin": "[0.80,0.90)",
      "n": 473,
      "error_rate": 0.35517970401691334,
      "mean_confidence": 0.8529927107037135
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1900,
      "error_rate": 0.2505263157894737,
      "mean_confidence": 0.9772638885775135
    }
  ],
  "theta_mae_rad": 0.014869026839733124,
  "theta_mae_deg": 0.8519324660301208,
  "uphill_recall": 0.7768194070080863,
  "downhill_recall": 0.796440489432703,
  "slope_sign_acc": 0.9709827539009034,
  "theta_flat_mae_deg": 1.1248730421066284,
  "theta_flat_abs_p95_deg": 4.013633728027344,
  "theta_flat_abs_max_deg": 10.606053352355957,
  "theta_flat_bias_deg": 0.1603797972202301,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.4061869382858276,
  "theta_near_flat_abs_p95_deg": 3.8856067657470703,
  "theta_near_flat_abs_max_deg": 10.606053352355957,
  "theta_near_flat_bias_deg": 0.5471107959747314,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.2018412351608276,
  "theta_flat_turn_abs_p95_deg": 4.260828971862793,
  "theta_flat_turn_abs_max_deg": 10.606053352355957,
  "theta_flat_turn_bias_deg": -0.30793410539627075,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8519324660301208,
  "theta_slope_control_abs_p95_deg": 9.293607711791992,
  "theta_slope_control_abs_max_deg": 13.428163528442383,
  "theta_slope_control_bias_deg": -0.24843759834766388,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8519324660301208,
  "theta_all_rmse_deg": 1.2431849241256714,
  "theta_all_p95_abs_err_deg": 2.6359434127807617,
  "theta_all_max_abs_err_deg": 10.106053352355957,
  "theta_all_bias_deg": -0.24843759834766388,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7920786738395691,
  "theta_active_abs_ge_2_rmse_deg": 1.1099520921707153,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2541141510009766,
  "theta_active_abs_ge_2_max_abs_err_deg": 5.749337196350098,
  "theta_active_abs_ge_2_bias_deg": -0.33808815479278564,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8901702165603638,
  "theta_abs_le_8_rmse_deg": 1.2920454740524292,
  "theta_abs_le_8_p95_abs_err_deg": 2.7048137187957764,
  "theta_abs_le_8_max_abs_err_deg": 10.106053352355957,
  "theta_abs_le_8_bias_deg": -0.2439081370830536,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8519324660301208,
  "theta_abs_le_10_rmse_deg": 1.2431849241256714,
  "theta_abs_le_10_p95_abs_err_deg": 2.6359434127807617,
  "theta_abs_le_10_max_abs_err_deg": 10.106053352355957,
  "theta_abs_le_10_bias_deg": -0.24843759834766388,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7416985034942627,
  "theta_pos_8_10_rmse_deg": 0.9592287540435791,
  "theta_pos_8_10_p95_abs_err_deg": 1.914297342300415,
  "theta_pos_8_10_max_abs_err_deg": 4.640852928161621,
  "theta_pos_8_10_bias_deg": -0.5601338744163513,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6386660933494568,
  "theta_neg_10_8_rmse_deg": 1.0618585348129272,
  "theta_neg_10_8_p95_abs_err_deg": 2.179368019104004,
  "theta_neg_10_8_max_abs_err_deg": 5.703782081604004,
  "theta_neg_10_8_bias_deg": 0.030102133750915527,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.753738522529602,
  "theta_pos_6_8_rmse_deg": 0.9803649187088013,
  "theta_pos_6_8_p95_abs_err_deg": 1.9474457502365112,
  "theta_pos_6_8_max_abs_err_deg": 3.1121644973754883,
  "theta_pos_6_8_bias_deg": -0.45636191964149475,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8771610260009766,
  "theta_neg_8_6_rmse_deg": 1.2376348972320557,
  "theta_neg_8_6_p95_abs_err_deg": 2.4313488006591797,
  "theta_neg_8_6_max_abs_err_deg": 5.269914150238037,
  "theta_neg_8_6_bias_deg": -0.17467652261257172,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8143376111984253,
  "theta_neg_4_2_rmse_deg": 1.108121395111084,
  "theta_neg_4_2_p95_abs_err_deg": 1.947948932647705,
  "theta_neg_4_2_max_abs_err_deg": 4.600007057189941,
  "theta_neg_4_2_bias_deg": -0.49484944343566895,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.9487756490707397,
  "theta_neg_2_0p5_rmse_deg": 1.3963621854782104,
  "theta_neg_2_0p5_p95_abs_err_deg": 2.910824775695801,
  "theta_neg_2_0p5_max_abs_err_deg": 4.739150047302246,
  "theta_neg_2_0p5_bias_deg": -0.32731443643569946,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0154850482940674,
  "theta_pos_0p5_2_rmse_deg": 1.3501965999603271,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.18582820892334,
  "theta_pos_0p5_2_max_abs_err_deg": 4.4632744789123535,
  "theta_pos_0p5_2_bias_deg": 0.2629324793815613,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3105635600096479,
  "loss_turn": 1.3771377438298742,
  "loss_theta": 0.0004707915005362334,
  "loss_main_bundle_base": 0.3105635600096479,
  "loss_turn_bundle_base": 0.2754275520696369,
  "loss_theta_bundle_base": 0.00030797476518246397,
  "loss_main_bundle": 0.3105635600096479,
  "loss_turn_bundle": 0.2754275520696369,
  "loss_theta_bundle": 0.00030797476518246397,
  "loss_theta_flat": 0.00018926176280298376,
  "loss_theta_near_flat": 0.001422494023544298,
  "loss_theta_error_excess": 0.0001644236913092021,
  "loss_theta_flat_excess": 9.71251782694746e-05,
  "loss_theta_near_flat_excess": 0.0010719001698981925,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010536371199231398,
  "loss_theta_small_neg": 0.00037472502417302867,
  "loss_theta_small_neg_excess": 0.00010137927536669922,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.3929528506989408,
  "loss_false_turn_straight": 0.3091149237384977,
  "loss_transition_focal_raw": 1.235225198733468,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.177088668808881,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
