# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `gradnorm`
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
| acc_main | 0.9661 |
| acc_turn | 0.5736 |
| acc_turn_pure | 0.5865 |
| acc_turn_transition | 0.5171 |
| main_confidence_mean | 0.9880 |
| main_low_conf_0p60_ratio | 0.0067 |
| main_low_conf_0p70_ratio | 0.0119 |
| turn_confidence_mean | 0.8096 |
| turn_low_conf_0p60_ratio | 0.1855 |
| turn_low_conf_0p70_ratio | 0.2937 |
| turn_right_recall | 0.6095 |
| turn_straight_recall | 0.5556 |
| turn_left_recall | 0.5805 |
| theta_mae_deg | 0.7578 |
| theta_abs_le_10_p95_abs_err_deg | 2.0587 |
| theta_neg_10_8_p95_abs_err_deg | 2.1766 |
| theta_pos_8_10_p95_abs_err_deg | 2.8559 |
| theta_abs_le_8_p95_abs_err_deg | 1.9826 |
| theta_neg_8_6_p95_abs_err_deg | 2.1739 |
| theta_pos_6_8_p95_abs_err_deg | 1.9116 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.7128 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.6837 |
| theta_flat_abs_p95_deg | 2.9544 |
| theta_flat_bias_deg | 0.0323 |
| theta_near_flat_abs_p95_deg | 1.4705 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1486 |
| theta_flat_turn_abs_p95_deg | 1.3943 |
| flat_recall | 0.9616 |
| stall_recall | 0.6979 |
| slope_recall | 0.9767 |
| uphill_recall | 0.7557 |
| downhill_recall | 0.7928 |

- best_epoch: 58
- train_seconds: 531.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 24 | 0.4583 | 0.5466 |
| [0.60,0.70) | 19 | 0.4211 | 0.6472 |
| [0.70,0.80) | 32 | 0.1875 | 0.7542 |
| [0.80,0.90) | 47 | 0.2979 | 0.8532 |
| [0.90,1.00) | 3480 | 0.0239 | 0.9969 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 668 | 0.5898 | 0.5141 |
| [0.60,0.70) | 390 | 0.5821 | 0.6517 |
| [0.70,0.80) | 444 | 0.5248 | 0.7531 |
| [0.80,0.90) | 500 | 0.5040 | 0.8527 |
| [0.90,1.00) | 1600 | 0.2687 | 0.9737 |


## 验证集最佳点

```json
{
  "loss_total": 0.5769545536563909,
  "acc_main": 0.9496617050067659,
  "acc_turn": 0.6129905277401895,
  "acc_turn_pure": 0.6296296296296297,
  "acc_turn_transition": 0.5341614906832298,
  "false_turn_straight": 0.4553014553014553,
  "flat_recall": 0.9710806697108066,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9526034712950601,
  "recall_main": [
    0.9710806697108066,
    0.40476190476190477,
    0.9526034712950601
  ],
  "turn_right_recall": 0.6113744075829384,
  "turn_straight_recall": 0.5446985446985447,
  "turn_left_recall": 0.756202804746494,
  "recall_turn": [
    0.6113744075829384,
    0.5446985446985447,
    0.756202804746494
  ],
  "cm_turn": [
    [
      516,
      206,
      122
    ],
    [
      344,
      1048,
      532
    ],
    [
      52,
      174,
      701
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      638,
      0,
      19
    ],
    [
      0,
      17,
      25
    ],
    [
      131,
      11,
      2854
    ]
  ],
  "main_confidence_mean": 0.9717425196907298,
  "main_confidence_error_mean": 0.7840408763922027,
  "main_low_conf_0p60_ratio": 0.005683355886332882,
  "main_low_conf_0p70_ratio": 0.056833558863328824,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 21,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.5540472587553903
    },
    {
      "bin": "[0.60,0.70)",
      "n": 189,
      "error_rate": 0.455026455026455,
      "mean_confidence": 0.6143229718731109
    },
    {
      "bin": "[0.70,0.80)",
      "n": 29,
      "error_rate": 0.20689655172413793,
      "mean_confidence": 0.7528302587783631
    },
    {
      "bin": "[0.80,0.90)",
      "n": 46,
      "error_rate": 0.08695652173913043,
      "mean_confidence": 0.8598702302432448
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3410,
      "error_rate": 0.02375366568914956,
      "mean_confidence": 0.9974957384292092
    }
  ],
  "turn_confidence_mean": 0.8260839547743408,
  "turn_confidence_error_mean": 0.7439369787118445,
  "turn_low_conf_0p60_ratio": 0.17185385656292287,
  "turn_low_conf_0p70_ratio": 0.2660351826792963,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 635,
      "error_rate": 0.6519685039370079,
      "mean_confidence": 0.49161662716052734
    },
    {
      "bin": "[0.60,0.70)",
      "n": 348,
      "error_rate": 0.5229885057471264,
      "mean_confidence": 0.6487457863273265
    },
    {
      "bin": "[0.70,0.80)",
      "n": 368,
      "error_rate": 0.4945652173913043,
      "mean_confidence": 0.7509702180742239
    },
    {
      "bin": "[0.80,0.90)",
      "n": 433,
      "error_rate": 0.44803695150115475,
      "mean_confidence": 0.8520468756138129
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1911,
      "error_rate": 0.23966509680795395,
      "mean_confidence": 0.9780987878651226
    }
  ],
  "theta_mae_rad": 0.014912007376551628,
  "theta_mae_deg": 0.8543950319290161,
  "uphill_recall": 0.7784366576819407,
  "downhill_recall": 0.7947719688542826,
  "slope_sign_acc": 0.9690665206679442,
  "theta_flat_mae_deg": 1.0391572713851929,
  "theta_flat_abs_p95_deg": 3.5536348819732666,
  "theta_flat_abs_max_deg": 9.03331470489502,
  "theta_flat_bias_deg": 0.27302879095077515,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.3501856327056885,
  "theta_near_flat_abs_p95_deg": 3.573729991912842,
  "theta_near_flat_abs_max_deg": 9.03331470489502,
  "theta_near_flat_bias_deg": 0.6623795628547668,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.0758073329925537,
  "theta_flat_turn_abs_p95_deg": 3.553419589996338,
  "theta_flat_turn_abs_max_deg": 9.03331470489502,
  "theta_flat_turn_bias_deg": 0.14588887989521027,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8543950319290161,
  "theta_slope_control_abs_p95_deg": 9.258766174316406,
  "theta_slope_control_abs_max_deg": 12.164198875427246,
  "theta_slope_control_bias_deg": 0.14421552419662476,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8543950319290161,
  "theta_all_rmse_deg": 1.2367209196090698,
  "theta_all_p95_abs_err_deg": 2.68123197555542,
  "theta_all_max_abs_err_deg": 8.53331470489502,
  "theta_all_bias_deg": 0.14421552419662476,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.813878059387207,
  "theta_active_abs_ge_2_rmse_deg": 1.1607507467269897,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.4629287719726562,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.2531514167785645,
  "theta_active_abs_ge_2_bias_deg": 0.115967757999897,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8596567511558533,
  "theta_abs_le_8_rmse_deg": 1.2492502927780151,
  "theta_abs_le_8_p95_abs_err_deg": 2.727473258972168,
  "theta_abs_le_8_max_abs_err_deg": 8.53331470489502,
  "theta_abs_le_8_bias_deg": 0.11701318621635437,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8543950319290161,
  "theta_abs_le_10_rmse_deg": 1.2367209196090698,
  "theta_abs_le_10_p95_abs_err_deg": 2.68123197555542,
  "theta_abs_le_10_max_abs_err_deg": 8.53331470489502,
  "theta_abs_le_10_bias_deg": 0.14421552419662476,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6786664724349976,
  "theta_pos_8_10_rmse_deg": 0.859712541103363,
  "theta_pos_8_10_p95_abs_err_deg": 1.534179449081421,
  "theta_pos_8_10_max_abs_err_deg": 4.4070515632629395,
  "theta_pos_8_10_bias_deg": -0.1308528631925583,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.988384485244751,
  "theta_neg_10_8_rmse_deg": 1.4382104873657227,
  "theta_neg_10_8_p95_abs_err_deg": 2.337923526763916,
  "theta_neg_10_8_max_abs_err_deg": 7.2531514167785645,
  "theta_neg_10_8_bias_deg": 0.6555343270301819,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6014984250068665,
  "theta_pos_6_8_rmse_deg": 0.8343108296394348,
  "theta_pos_6_8_p95_abs_err_deg": 1.8350907564163208,
  "theta_pos_6_8_max_abs_err_deg": 3.1445095539093018,
  "theta_pos_6_8_bias_deg": -0.011643419042229652,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.0584367513656616,
  "theta_neg_8_6_rmse_deg": 1.396810531616211,
  "theta_neg_8_6_p95_abs_err_deg": 2.7712695598602295,
  "theta_neg_8_6_max_abs_err_deg": 6.910549163818359,
  "theta_neg_8_6_bias_deg": 0.44558024406433105,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.7508589625358582,
  "theta_neg_4_2_rmse_deg": 1.0672322511672974,
  "theta_neg_4_2_p95_abs_err_deg": 2.389714241027832,
  "theta_neg_4_2_max_abs_err_deg": 4.795162200927734,
  "theta_neg_4_2_bias_deg": -0.09166720509529114,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7900243997573853,
  "theta_neg_2_0p5_rmse_deg": 1.0387221574783325,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8374974727630615,
  "theta_neg_2_0p5_max_abs_err_deg": 4.4765801429748535,
  "theta_neg_2_0p5_bias_deg": -0.17154546082019806,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9593915939331055,
  "theta_pos_0p5_2_rmse_deg": 1.3222095966339111,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.543483018875122,
  "theta_pos_0p5_2_max_abs_err_deg": 4.651890754699707,
  "theta_pos_0p5_2_bias_deg": 0.31388387084007263,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2912490653249666,
  "loss_turn": 1.4269592277413292,
  "loss_theta": 0.0004658426295654629,
  "loss_main_bundle": 0.2912490653249666,
  "loss_turn_bundle": 0.285391847021041,
  "loss_theta_bundle": 0.0003136432756599245,
  "loss_theta_flat": 0.0003065080650126201,
  "loss_theta_near_flat": 0.0011987941902312318,
  "loss_theta_error_excess": 0.00015872172964516277,
  "loss_theta_flat_excess": 0.00014012247212615535,
  "loss_theta_near_flat_excess": 0.0008536267352034621,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001271276477639562,
  "loss_theta_small_neg": 0.00034761204109691,
  "loss_theta_small_neg_excess": 9.236427665000003e-05,
  "loss_turn_release": 0.42005048309514587,
  "loss_false_turn_straight": 0.3157689749629959
}
```
