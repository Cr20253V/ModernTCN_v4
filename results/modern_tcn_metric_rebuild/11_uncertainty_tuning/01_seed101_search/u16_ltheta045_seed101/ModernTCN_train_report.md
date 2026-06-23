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
  "lambda_theta": 0.45,
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
| acc_main | 0.9697 |
| acc_turn | 0.5847 |
| acc_turn_pure | 0.6012 |
| acc_turn_transition | 0.5127 |
| main_confidence_mean | 0.9893 |
| main_low_conf_0p60_ratio | 0.0072 |
| main_low_conf_0p70_ratio | 0.0150 |
| turn_confidence_mean | 0.8469 |
| turn_low_conf_0p60_ratio | 0.1358 |
| turn_low_conf_0p70_ratio | 0.2268 |
| turn_right_recall | 0.5745 |
| turn_straight_recall | 0.5810 |
| turn_left_recall | 0.6023 |
| theta_mae_deg | 0.6833 |
| theta_abs_le_10_p95_abs_err_deg | 1.8815 |
| theta_neg_10_8_p95_abs_err_deg | 1.4721 |
| theta_pos_8_10_p95_abs_err_deg | 2.6512 |
| theta_abs_le_8_p95_abs_err_deg | 1.7597 |
| theta_neg_8_6_p95_abs_err_deg | 2.0685 |
| theta_pos_6_8_p95_abs_err_deg | 1.5867 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8519 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4131 |
| theta_flat_abs_p95_deg | 2.4272 |
| theta_flat_bias_deg | -0.3194 |
| theta_near_flat_abs_p95_deg | 1.7873 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4041 |
| theta_flat_turn_abs_p95_deg | 1.7644 |
| flat_recall | 0.9590 |
| stall_recall | 0.7083 |
| slope_recall | 0.9818 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7626 |
| downhill_recall | 0.7951 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    725,
    0,
    31
  ],
  [
    10,
    68,
    18
  ],
  [
    40,
    10,
    2700
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    459,
    193,
    147
  ],
  [
    336,
    1123,
    474
  ],
  [
    138,
    208,
    524
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.351823 |
| test_loss_turn_bundle_base | 0.368683 |
| test_loss_theta_bundle_base | 0.000141 |
| test_loss_transition_focal_raw | 1.716366 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.804777 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 83
- train_seconds: 379.7

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 26 | 0.5000 | 0.5439 |
| [0.60,0.70) | 28 | 0.2500 | 0.6497 |
| [0.70,0.80) | 19 | 0.2632 | 0.7476 |
| [0.80,0.90) | 40 | 0.3500 | 0.8518 |
| [0.90,1.00) | 3489 | 0.0201 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 489 | 0.5890 | 0.5250 |
| [0.60,0.70) | 328 | 0.5701 | 0.6513 |
| [0.70,0.80) | 346 | 0.5202 | 0.7504 |
| [0.80,0.90) | 496 | 0.4819 | 0.8536 |
| [0.90,1.00) | 1943 | 0.3098 | 0.9765 |


## 验证集最佳点

```json
{
  "loss_total": 0.6935854940840291,
  "acc_main": 0.9426251691474966,
  "acc_turn": 0.6365358592692828,
  "acc_turn_pure": 0.6509341199606686,
  "acc_turn_transition": 0.5683229813664596,
  "false_turn_straight": 0.41528066528066526,
  "flat_recall": 0.9269406392694064,
  "stall_recall": 0.35714285714285715,
  "slope_recall": 0.9542723631508678,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9269406392694064,
    0.35714285714285715,
    0.9542723631508678
  ],
  "turn_right_recall": 0.6090047393364929,
  "turn_straight_recall": 0.5847193347193347,
  "turn_left_recall": 0.7691477885652643,
  "recall_turn": [
    0.6090047393364929,
    0.5847193347193347,
    0.7691477885652643
  ],
  "cm_turn": [
    [
      514,
      226,
      104
    ],
    [
      276,
      1125,
      523
    ],
    [
      46,
      168,
      713
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      609,
      0,
      48
    ],
    [
      0,
      15,
      27
    ],
    [
      126,
      11,
      2859
    ]
  ],
  "main_confidence_mean": 0.9703074932133897,
  "main_confidence_error_mean": 0.7718711315197233,
  "main_low_conf_0p60_ratio": 0.04736129905277402,
  "main_low_conf_0p70_ratio": 0.053585926928281465,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 175,
      "error_rate": 0.45714285714285713,
      "mean_confidence": 0.5042585507097161
    },
    {
      "bin": "[0.60,0.70)",
      "n": 23,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.6357519676590843
    },
    {
      "bin": "[0.70,0.80)",
      "n": 19,
      "error_rate": 0.47368421052631576,
      "mean_confidence": 0.7568812807379754
    },
    {
      "bin": "[0.80,0.90)",
      "n": 29,
      "error_rate": 0.3448275862068966,
      "mean_confidence": 0.8607202250946284
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3449,
      "error_rate": 0.029573789504204116,
      "mean_confidence": 0.9982826949641491
    }
  ],
  "turn_confidence_mean": 0.8589393764416567,
  "turn_confidence_error_mean": 0.7794456353147845,
  "turn_low_conf_0p60_ratio": 0.13423545331529094,
  "turn_low_conf_0p70_ratio": 0.20757780784844385,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 496,
      "error_rate": 0.655241935483871,
      "mean_confidence": 0.48660093305083124
    },
    {
      "bin": "[0.60,0.70)",
      "n": 271,
      "error_rate": 0.5092250922509225,
      "mean_confidence": 0.6510165839753157
    },
    {
      "bin": "[0.70,0.80)",
      "n": 273,
      "error_rate": 0.4725274725274725,
      "mean_confidence": 0.7531609617510044
    },
    {
      "bin": "[0.80,0.90)",
      "n": 414,
      "error_rate": 0.4782608695652174,
      "mean_confidence": 0.8531614099366843
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2241,
      "error_rate": 0.24676483712628292,
      "mean_confidence": 0.9804460832796019
    }
  ],
  "theta_mae_rad": 0.014125403016805649,
  "theta_mae_deg": 0.8093259334564209,
  "uphill_recall": 0.7795148247978436,
  "downhill_recall": 0.8125695216907676,
  "slope_sign_acc": 0.976731453599781,
  "theta_flat_mae_deg": 1.0562635660171509,
  "theta_flat_abs_p95_deg": 3.657986640930176,
  "theta_flat_abs_max_deg": 6.597120761871338,
  "theta_flat_bias_deg": 0.05719449371099472,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.341185212135315,
  "theta_near_flat_abs_p95_deg": 3.658020496368408,
  "theta_near_flat_abs_max_deg": 6.3752288818359375,
  "theta_near_flat_bias_deg": 0.4710887372493744,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9430428743362427,
  "theta_flat_turn_abs_p95_deg": 3.657986640930176,
  "theta_flat_turn_abs_max_deg": 6.3752288818359375,
  "theta_flat_turn_bias_deg": -0.030707161873579025,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8093259334564209,
  "theta_slope_control_abs_p95_deg": 9.411736488342285,
  "theta_slope_control_abs_max_deg": 13.009117126464844,
  "theta_slope_control_bias_deg": -0.1827402114868164,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8093259930610657,
  "theta_all_rmse_deg": 1.1607873439788818,
  "theta_all_p95_abs_err_deg": 2.548469066619873,
  "theta_all_max_abs_err_deg": 6.484654903411865,
  "theta_all_bias_deg": -0.1827401965856552,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.7551743984222412,
  "theta_active_abs_ge_2_rmse_deg": 1.0781238079071045,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.2731552124023438,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.484654903411865,
  "theta_active_abs_ge_2_bias_deg": -0.23535606265068054,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8431965112686157,
  "theta_abs_le_8_rmse_deg": 1.1892952919006348,
  "theta_abs_le_8_p95_abs_err_deg": 2.724532127380371,
  "theta_abs_le_8_max_abs_err_deg": 5.8752288818359375,
  "theta_abs_le_8_bias_deg": -0.18471203744411469,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8093259930610657,
  "theta_abs_le_10_rmse_deg": 1.1607873439788818,
  "theta_abs_le_10_p95_abs_err_deg": 2.548469066619873,
  "theta_abs_le_10_max_abs_err_deg": 6.484654903411865,
  "theta_abs_le_10_bias_deg": -0.1827401965856552,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5842646360397339,
  "theta_pos_8_10_rmse_deg": 0.8122344613075256,
  "theta_pos_8_10_p95_abs_err_deg": 1.5808590650558472,
  "theta_pos_8_10_max_abs_err_deg": 4.32553768157959,
  "theta_pos_8_10_bias_deg": -0.34533870220184326,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7500375509262085,
  "theta_neg_10_8_rmse_deg": 1.2152692079544067,
  "theta_neg_10_8_p95_abs_err_deg": 2.10658597946167,
  "theta_neg_10_8_max_abs_err_deg": 6.484654903411865,
  "theta_neg_10_8_bias_deg": -0.000549828982912004,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.561170220375061,
  "theta_pos_6_8_rmse_deg": 0.813720166683197,
  "theta_pos_6_8_p95_abs_err_deg": 1.612425684928894,
  "theta_pos_6_8_max_abs_err_deg": 3.3755569458007812,
  "theta_pos_6_8_bias_deg": -0.13308529555797577,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.005839228630066,
  "theta_neg_8_6_rmse_deg": 1.2959740161895752,
  "theta_neg_8_6_p95_abs_err_deg": 2.4455406665802,
  "theta_neg_8_6_max_abs_err_deg": 5.845477104187012,
  "theta_neg_8_6_bias_deg": -0.5927571058273315,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8232640027999878,
  "theta_neg_4_2_rmse_deg": 1.0632137060165405,
  "theta_neg_4_2_p95_abs_err_deg": 1.9438793659210205,
  "theta_neg_4_2_max_abs_err_deg": 5.311088562011719,
  "theta_neg_4_2_bias_deg": -0.42647117376327515,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8249487280845642,
  "theta_neg_2_0p5_rmse_deg": 1.036354899406433,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8438078165054321,
  "theta_neg_2_0p5_max_abs_err_deg": 3.8115527629852295,
  "theta_neg_2_0p5_bias_deg": -0.705940306186676,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9934569001197815,
  "theta_pos_0p5_2_rmse_deg": 1.3221994638442993,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.157986640930176,
  "theta_pos_0p5_2_max_abs_err_deg": 4.825148582458496,
  "theta_pos_0p5_2_bias_deg": 0.4094417691230774,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3886154159560739,
  "loss_turn": 1.5237051372760364,
  "loss_theta": 0.0004103735475095193,
  "loss_main_bundle_base": 0.3886154159560739,
  "loss_turn_bundle_base": 0.3047410323832774,
  "loss_theta_bundle_base": 0.00022905456319360595,
  "loss_main_bundle": 0.3886154159560739,
  "loss_turn_bundle": 0.3047410323832774,
  "loss_theta_bundle": 0.00022905456319360595,
  "loss_theta_flat": 0.0002314443900611432,
  "loss_theta_near_flat": 0.001098145785425186,
  "loss_theta_error_excess": 0.00012889331371614178,
  "loss_theta_flat_excess": 0.00010671043788701384,
  "loss_theta_near_flat_excess": 0.0007505782553800086,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00010168481594063745,
  "loss_theta_small_neg": 0.0003400230783552022,
  "loss_theta_small_neg_excess": 6.909973165842658e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.38422223870744565,
  "loss_false_turn_straight": 0.30652976665993664,
  "loss_transition_focal_raw": 1.4382447596493206,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.645725069579112,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
