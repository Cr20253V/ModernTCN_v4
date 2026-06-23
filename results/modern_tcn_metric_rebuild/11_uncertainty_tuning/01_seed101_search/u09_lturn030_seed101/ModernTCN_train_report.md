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
  "lambda_turn": 0.3,
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
| acc_main | 0.9736 |
| acc_turn | 0.5475 |
| acc_turn_pure | 0.5643 |
| acc_turn_transition | 0.4739 |
| main_confidence_mean | 0.9894 |
| main_low_conf_0p60_ratio | 0.0047 |
| main_low_conf_0p70_ratio | 0.0122 |
| turn_confidence_mean | 0.8324 |
| turn_low_conf_0p60_ratio | 0.1330 |
| turn_low_conf_0p70_ratio | 0.2435 |
| turn_right_recall | 0.6283 |
| turn_straight_recall | 0.4992 |
| turn_left_recall | 0.5805 |
| theta_mae_deg | 0.8291 |
| theta_abs_le_10_p95_abs_err_deg | 2.0164 |
| theta_neg_10_8_p95_abs_err_deg | 1.6557 |
| theta_pos_8_10_p95_abs_err_deg | 2.9237 |
| theta_abs_le_8_p95_abs_err_deg | 1.8945 |
| theta_neg_8_6_p95_abs_err_deg | 1.6020 |
| theta_pos_6_8_p95_abs_err_deg | 2.1695 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.8617 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.7654 |
| theta_flat_abs_p95_deg | 2.5140 |
| theta_flat_bias_deg | -0.0853 |
| theta_near_flat_abs_p95_deg | 1.8439 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1103 |
| theta_flat_turn_abs_p95_deg | 1.8168 |
| flat_recall | 0.9696 |
| stall_recall | 0.7083 |
| slope_recall | 0.9840 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7701 |
| downhill_recall | 0.7866 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    733,
    0,
    23
  ],
  [
    10,
    68,
    18
  ],
  [
    36,
    8,
    2706
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    502,
    164,
    133
  ],
  [
    460,
    965,
    508
  ],
  [
    208,
    157,
    505
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.303903 |
| test_loss_turn_bundle_base | 0.501547 |
| test_loss_theta_bundle_base | 0.000234 |
| test_loss_transition_focal_raw | 1.547867 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.395928 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 60
- train_seconds: 307.9

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 17 | 0.5882 | 0.5448 |
| [0.60,0.70) | 27 | 0.2593 | 0.6525 |
| [0.70,0.80) | 36 | 0.2778 | 0.7416 |
| [0.80,0.90) | 31 | 0.2258 | 0.8515 |
| [0.90,1.00) | 3491 | 0.0175 | 0.9979 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 479 | 0.6388 | 0.5220 |
| [0.60,0.70) | 398 | 0.5854 | 0.6552 |
| [0.70,0.80) | 455 | 0.6330 | 0.7499 |
| [0.80,0.90) | 538 | 0.5279 | 0.8533 |
| [0.90,1.00) | 1732 | 0.2997 | 0.9741 |


## 验证集最佳点

```json
{
  "loss_total": 0.805490752050454,
  "acc_main": 0.9480378890392422,
  "acc_turn": 0.6070365358592693,
  "acc_turn_pure": 0.6247132087840053,
  "acc_turn_transition": 0.5232919254658385,
  "false_turn_straight": 0.4797297297297297,
  "flat_recall": 0.9528158295281582,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9546061415220294,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9528158295281582,
    0.40476190476190477,
    0.9546061415220294
  ],
  "turn_right_recall": 0.6552132701421801,
  "turn_straight_recall": 0.5202702702702703,
  "turn_left_recall": 0.7432578209277239,
  "recall_turn": [
    0.6552132701421801,
    0.5202702702702703,
    0.7432578209277239
  ],
  "cm_turn": [
    [
      553,
      190,
      101
    ],
    [
      428,
      1001,
      495
    ],
    [
      93,
      145,
      689
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      626,
      0,
      31
    ],
    [
      0,
      17,
      25
    ],
    [
      125,
      11,
      2860
    ]
  ],
  "main_confidence_mean": 0.9714305641151121,
  "main_confidence_error_mean": 0.7807725106471266,
  "main_low_conf_0p60_ratio": 0.04844384303112314,
  "main_low_conf_0p70_ratio": 0.0530446549391069,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 179,
      "error_rate": 0.45251396648044695,
      "mean_confidence": 0.5647446470068086
    },
    {
      "bin": "[0.60,0.70)",
      "n": 17,
      "error_rate": 0.47058823529411764,
      "mean_confidence": 0.6517132981009857
    },
    {
      "bin": "[0.70,0.80)",
      "n": 27,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.7587993491769888
    },
    {
      "bin": "[0.80,0.90)",
      "n": 55,
      "error_rate": 0.18181818181818182,
      "mean_confidence": 0.8516812465249223
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3417,
      "error_rate": 0.024582967515364356,
      "mean_confidence": 0.9979331183894511
    }
  ],
  "turn_confidence_mean": 0.8443930361820865,
  "turn_confidence_error_mean": 0.7798693931932278,
  "turn_low_conf_0p60_ratio": 0.1456021650879567,
  "turn_low_conf_0p70_ratio": 0.22462787550744248,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 538,
      "error_rate": 0.6338289962825279,
      "mean_confidence": 0.4943850204717923
    },
    {
      "bin": "[0.60,0.70)",
      "n": 292,
      "error_rate": 0.476027397260274,
      "mean_confidence": 0.6496898172928959
    },
    {
      "bin": "[0.70,0.80)",
      "n": 348,
      "error_rate": 0.5057471264367817,
      "mean_confidence": 0.7513021828365348
    },
    {
      "bin": "[0.80,0.90)",
      "n": 465,
      "error_rate": 0.4881720430107527,
      "mean_confidence": 0.8515077104240739
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2052,
      "error_rate": 0.2772904483430799,
      "mean_confidence": 0.978040670592179
    }
  ],
  "theta_mae_rad": 0.01736968383193016,
  "theta_mae_deg": 0.9952095150947571,
  "uphill_recall": 0.784366576819407,
  "downhill_recall": 0.7986651835372637,
  "slope_sign_acc": 0.9693402682726526,
  "theta_flat_mae_deg": 1.0021617412567139,
  "theta_flat_abs_p95_deg": 3.481733798980713,
  "theta_flat_abs_max_deg": 6.764899730682373,
  "theta_flat_bias_deg": 0.46948328614234924,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.244089961051941,
  "theta_near_flat_abs_p95_deg": 3.484748363494873,
  "theta_near_flat_abs_max_deg": 6.764899730682373,
  "theta_near_flat_bias_deg": 0.7360888123512268,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.9928120374679565,
  "theta_flat_turn_abs_p95_deg": 3.481733798980713,
  "theta_flat_turn_abs_max_deg": 6.764899730682373,
  "theta_flat_turn_bias_deg": 0.20070180296897888,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.9952095150947571,
  "theta_slope_control_abs_p95_deg": 9.192492485046387,
  "theta_slope_control_abs_max_deg": 12.466035842895508,
  "theta_slope_control_bias_deg": -0.18058307468891144,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.9952095746994019,
  "theta_all_rmse_deg": 1.3469452857971191,
  "theta_all_p95_abs_err_deg": 2.9181065559387207,
  "theta_all_max_abs_err_deg": 7.926052570343018,
  "theta_all_bias_deg": -0.18058307468891144,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.9936849474906921,
  "theta_active_abs_ge_2_rmse_deg": 1.3292137384414673,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.528111457824707,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.926052570343018,
  "theta_active_abs_ge_2_bias_deg": -0.32313767075538635,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9922232031822205,
  "theta_abs_le_8_rmse_deg": 1.3652093410491943,
  "theta_abs_le_8_p95_abs_err_deg": 2.981733798980713,
  "theta_abs_le_8_max_abs_err_deg": 7.926052570343018,
  "theta_abs_le_8_bias_deg": -0.09913299232721329,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.9952095746994019,
  "theta_abs_le_10_rmse_deg": 1.3469452857971191,
  "theta_abs_le_10_p95_abs_err_deg": 2.9181065559387207,
  "theta_abs_le_10_max_abs_err_deg": 7.926052570343018,
  "theta_abs_le_10_bias_deg": -0.18058307468891144,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.184744119644165,
  "theta_pos_8_10_rmse_deg": 1.3426580429077148,
  "theta_pos_8_10_p95_abs_err_deg": 2.356210708618164,
  "theta_pos_8_10_max_abs_err_deg": 5.037555694580078,
  "theta_pos_8_10_bias_deg": -1.0405688285827637,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8278115391731262,
  "theta_neg_10_8_rmse_deg": 1.1850935220718384,
  "theta_neg_10_8_p95_abs_err_deg": 2.2282309532165527,
  "theta_neg_10_8_max_abs_err_deg": 6.225802421569824,
  "theta_neg_10_8_bias_deg": 0.0011253961129114032,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 1.037137508392334,
  "theta_pos_6_8_rmse_deg": 1.2130247354507446,
  "theta_pos_6_8_p95_abs_err_deg": 2.2360804080963135,
  "theta_pos_6_8_max_abs_err_deg": 3.5271761417388916,
  "theta_pos_6_8_bias_deg": -0.8071856498718262,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8269669413566589,
  "theta_neg_8_6_rmse_deg": 1.2218939065933228,
  "theta_neg_8_6_p95_abs_err_deg": 2.933687925338745,
  "theta_neg_8_6_max_abs_err_deg": 5.8102827072143555,
  "theta_neg_8_6_bias_deg": -0.0937478169798851,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.856492280960083,
  "theta_neg_4_2_rmse_deg": 1.1011626720428467,
  "theta_neg_4_2_p95_abs_err_deg": 2.26607084274292,
  "theta_neg_4_2_max_abs_err_deg": 4.065855503082275,
  "theta_neg_4_2_bias_deg": -0.08580838143825531,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6212690472602844,
  "theta_neg_2_0p5_rmse_deg": 0.8067265152931213,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.2253968715667725,
  "theta_neg_2_0p5_max_abs_err_deg": 4.181192874908447,
  "theta_neg_2_0p5_bias_deg": -0.05160844698548317,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.1448521614074707,
  "theta_pos_0p5_2_rmse_deg": 1.3826450109481812,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0736324787139893,
  "theta_pos_0p5_2_max_abs_err_deg": 3.9565818309783936,
  "theta_pos_0p5_2_bias_deg": 0.7598902583122253,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.3531107653461709,
  "loss_turn": 1.5067701025809261,
  "loss_theta": 0.0005525973890605603,
  "loss_main_bundle_base": 0.3531107653461709,
  "loss_turn_bundle_base": 0.45203105012844635,
  "loss_theta_bundle_base": 0.00034892166362469196,
  "loss_main_bundle": 0.3531107653461709,
  "loss_turn_bundle": 0.45203105012844635,
  "loss_theta_bundle": 0.00034892166362469196,
  "loss_theta_flat": 0.0001546859667840929,
  "loss_theta_near_flat": 0.001026671902177016,
  "loss_theta_error_excess": 0.000182636722661454,
  "loss_theta_flat_excess": 8.407628823360365e-05,
  "loss_theta_near_flat_excess": 0.0006976186372188496,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.0001729894504784411,
  "loss_theta_small_neg": 0.00036380882973559655,
  "loss_theta_small_neg_excess": 7.479664400577985e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4467170559424347,
  "loss_false_turn_straight": 0.35295501407009017,
  "loss_transition_focal_raw": 1.3847180157778873,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.72289701133345,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
