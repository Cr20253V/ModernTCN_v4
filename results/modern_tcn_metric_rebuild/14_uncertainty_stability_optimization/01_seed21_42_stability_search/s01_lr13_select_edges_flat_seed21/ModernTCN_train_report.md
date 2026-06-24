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
  "select_stall_weight": 0.2,
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
  "select_theta_flat_peak_weight": 1.0,
  "select_theta_flat_peak_target_deg": 5.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.6,
  "select_theta_extreme_p95_target_deg": 1.2,
  "select_theta_edge_p95_weight": 1.2,
  "select_theta_edge_p95_target_deg": 1.15,
  "select_theta_small_nonzero_p95_weight": 0.8,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.3,
  "select_theta_flat_bias_target_deg": 0.15
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9731 |
| acc_turn | 0.5866 |
| acc_turn_pure | 0.6012 |
| acc_turn_transition | 0.5231 |
| main_confidence_mean | 0.9881 |
| main_low_conf_0p60_ratio | 0.0097 |
| main_low_conf_0p70_ratio | 0.0153 |
| turn_confidence_mean | 0.8403 |
| turn_low_conf_0p60_ratio | 0.1319 |
| turn_low_conf_0p70_ratio | 0.2340 |
| turn_right_recall | 0.6345 |
| turn_straight_recall | 0.5551 |
| turn_left_recall | 0.6126 |
| theta_mae_deg | 0.6389 |
| theta_abs_le_10_p95_abs_err_deg | 1.7105 |
| theta_neg_10_8_p95_abs_err_deg | 1.2054 |
| theta_pos_8_10_p95_abs_err_deg | 2.6754 |
| theta_abs_le_8_p95_abs_err_deg | 1.6687 |
| theta_neg_8_6_p95_abs_err_deg | 1.6103 |
| theta_pos_6_8_p95_abs_err_deg | 1.2881 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.7128 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8339 |
| theta_flat_abs_p95_deg | 2.5788 |
| theta_flat_bias_deg | -0.5897 |
| theta_near_flat_abs_p95_deg | 1.7683 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.3961 |
| theta_flat_turn_abs_p95_deg | 1.5169 |
| flat_recall | 0.9577 |
| stall_recall | 0.7083 |
| slope_recall | 0.9865 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7735 |
| downhill_recall | 0.7923 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    724,
    0,
    32
  ],
  [
    10,
    68,
    18
  ],
  [
    31,
    6,
    2713
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    507,
    183,
    109
  ],
  [
    402,
    1073,
    458
  ],
  [
    150,
    187,
    533
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.298928 |
| test_loss_turn_bundle_base | 0.330133 |
| test_loss_theta_bundle_base | 0.000163 |
| test_loss_transition_focal_raw | 1.583204 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 3.387289 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 74
- train_seconds: 345.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 35 | 0.3714 | 0.5418 |
| [0.60,0.70) | 20 | 0.4000 | 0.6512 |
| [0.70,0.80) | 27 | 0.4815 | 0.7582 |
| [0.80,0.90) | 48 | 0.3125 | 0.8547 |
| [0.90,1.00) | 3472 | 0.0138 | 0.9982 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 475 | 0.6379 | 0.5233 |
| [0.60,0.70) | 368 | 0.5136 | 0.6494 |
| [0.70,0.80) | 384 | 0.5078 | 0.7502 |
| [0.80,0.90) | 521 | 0.4683 | 0.8513 |
| [0.90,1.00) | 1854 | 0.3010 | 0.9749 |


## 验证集最佳点

```json
{
  "loss_total": 0.5949123035425746,
  "acc_main": 0.9504736129905278,
  "acc_turn": 0.6408660351826793,
  "acc_turn_pure": 0.655850540806293,
  "acc_turn_transition": 0.5698757763975155,
  "false_turn_straight": 0.4267151767151767,
  "flat_recall": 0.9512937595129376,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9559412550066756,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.0,
  "recall_main": [
    0.9512937595129376,
    0.5476190476190477,
    0.9559412550066756
  ],
  "turn_right_recall": 0.7132701421800948,
  "turn_straight_recall": 0.5732848232848233,
  "turn_left_recall": 0.7152103559870551,
  "recall_turn": [
    0.7132701421800948,
    0.5732848232848233,
    0.7152103559870551
  ],
  "cm_turn": [
    [
      602,
      213,
      29
    ],
    [
      476,
      1103,
      345
    ],
    [
      107,
      157,
      663
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      625,
      0,
      32
    ],
    [
      0,
      23,
      19
    ],
    [
      125,
      7,
      2864
    ]
  ],
  "main_confidence_mean": 0.9746860626576249,
  "main_confidence_error_mean": 0.7854174354236015,
  "main_low_conf_0p60_ratio": 0.0037889039242219214,
  "main_low_conf_0p70_ratio": 0.05466847090663058,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 14,
      "error_rate": 0.5,
      "mean_confidence": 0.5623247038326825
    },
    {
      "bin": "[0.60,0.70)",
      "n": 188,
      "error_rate": 0.46808510638297873,
      "mean_confidence": 0.6310321777327719
    },
    {
      "bin": "[0.70,0.80)",
      "n": 20,
      "error_rate": 0.4,
      "mean_confidence": 0.7452760099497132
    },
    {
      "bin": "[0.80,0.90)",
      "n": 45,
      "error_rate": 0.17777777777777778,
      "mean_confidence": 0.853228966609898
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3428,
      "error_rate": 0.021003500583430573,
      "mean_confidence": 0.9981498198821662
    }
  ],
  "turn_confidence_mean": 0.8573452506077269,
  "turn_confidence_error_mean": 0.7933877353983517,
  "turn_low_conf_0p60_ratio": 0.14370771312584574,
  "turn_low_conf_0p70_ratio": 0.22354533152909337,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 531,
      "error_rate": 0.5856873822975518,
      "mean_confidence": 0.5396093937965332
    },
    {
      "bin": "[0.60,0.70)",
      "n": 295,
      "error_rate": 0.4745762711864407,
      "mean_confidence": 0.6499439799113724
    },
    {
      "bin": "[0.70,0.80)",
      "n": 291,
      "error_rate": 0.5395189003436426,
      "mean_confidence": 0.7509193475778597
    },
    {
      "bin": "[0.80,0.90)",
      "n": 422,
      "error_rate": 0.4194312796208531,
      "mean_confidence": 0.8537078056454764
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2156,
      "error_rate": 0.25139146567717996,
      "mean_confidence": 0.979054923324763
    }
  ],
  "theta_mae_rad": 0.01390785165131092,
  "theta_mae_deg": 0.7968611717224121,
  "uphill_recall": 0.7854447439353099,
  "downhill_recall": 0.800333704115684,
  "slope_sign_acc": 0.9720777443197371,
  "theta_flat_mae_deg": 1.2867097854614258,
  "theta_flat_abs_p95_deg": 4.31822395324707,
  "theta_flat_abs_max_deg": 6.904168605804443,
  "theta_flat_bias_deg": 0.28266531229019165,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.6445670127868652,
  "theta_near_flat_abs_p95_deg": 4.822113513946533,
  "theta_near_flat_abs_max_deg": 6.904168605804443,
  "theta_near_flat_bias_deg": 0.8280633091926575,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.320338249206543,
  "theta_flat_turn_abs_p95_deg": 5.209555149078369,
  "theta_flat_turn_abs_max_deg": 6.904168605804443,
  "theta_flat_turn_bias_deg": 0.5065307021141052,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7968611717224121,
  "theta_slope_control_abs_p95_deg": 9.335357666015625,
  "theta_slope_control_abs_max_deg": 11.801667213439941,
  "theta_slope_control_bias_deg": -0.009806191548705101,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7968611717224121,
  "theta_all_rmse_deg": 1.2121586799621582,
  "theta_all_p95_abs_err_deg": 2.7734577655792236,
  "theta_all_max_abs_err_deg": 7.404168605804443,
  "theta_all_bias_deg": -0.009806190617382526,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6894410848617554,
  "theta_active_abs_ge_2_rmse_deg": 1.0028390884399414,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0414624214172363,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.1022233963012695,
  "theta_active_abs_ge_2_bias_deg": -0.07394297420978546,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.8416163325309753,
  "theta_abs_le_8_rmse_deg": 1.2625237703323364,
  "theta_abs_le_8_p95_abs_err_deg": 2.8182239532470703,
  "theta_abs_le_8_max_abs_err_deg": 7.404168605804443,
  "theta_abs_le_8_bias_deg": 0.01979987509548664,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7968611717224121,
  "theta_abs_le_10_rmse_deg": 1.2121586799621582,
  "theta_abs_le_10_p95_abs_err_deg": 2.7734577655792236,
  "theta_abs_le_10_max_abs_err_deg": 7.404168605804443,
  "theta_abs_le_10_bias_deg": -0.009806190617382526,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5224854350090027,
  "theta_pos_8_10_rmse_deg": 0.7467935681343079,
  "theta_pos_8_10_p95_abs_err_deg": 1.5884308815002441,
  "theta_pos_8_10_max_abs_err_deg": 4.577327251434326,
  "theta_pos_8_10_bias_deg": -0.23220811784267426,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.6951108574867249,
  "theta_neg_10_8_rmse_deg": 1.1558735370635986,
  "theta_neg_10_8_p95_abs_err_deg": 1.851457118988037,
  "theta_neg_10_8_max_abs_err_deg": 7.1022233963012695,
  "theta_neg_10_8_bias_deg": -0.035508893430233,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5813785195350647,
  "theta_pos_6_8_rmse_deg": 0.8308176398277283,
  "theta_pos_6_8_p95_abs_err_deg": 1.5991442203521729,
  "theta_pos_6_8_max_abs_err_deg": 3.8725974559783936,
  "theta_pos_6_8_bias_deg": -0.11271049827337265,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.6852442622184753,
  "theta_neg_8_6_rmse_deg": 1.0438430309295654,
  "theta_neg_8_6_p95_abs_err_deg": 2.101072072982788,
  "theta_neg_8_6_max_abs_err_deg": 6.96802282333374,
  "theta_neg_8_6_bias_deg": -0.1741020530462265,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6507102251052856,
  "theta_neg_4_2_rmse_deg": 0.8933756947517395,
  "theta_neg_4_2_p95_abs_err_deg": 1.8354772329330444,
  "theta_neg_4_2_max_abs_err_deg": 4.45918083190918,
  "theta_neg_4_2_bias_deg": -0.27835991978645325,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.7838903665542603,
  "theta_neg_2_0p5_rmse_deg": 0.9621286392211914,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.8326183557510376,
  "theta_neg_2_0p5_max_abs_err_deg": 3.6957242488861084,
  "theta_neg_2_0p5_bias_deg": -0.6367368698120117,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.3397860527038574,
  "theta_pos_0p5_2_rmse_deg": 1.6955327987670898,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.8182239532470703,
  "theta_pos_0p5_2_max_abs_err_deg": 3.8194057941436768,
  "theta_pos_0p5_2_bias_deg": 0.5057262778282166,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.32224280835811114,
  "loss_turn": 1.3618136314319822,
  "loss_theta": 0.0004475626003290798,
  "loss_main_bundle_base": 0.32224280835811114,
  "loss_turn_bundle_base": 0.272362732157333,
  "loss_theta_bundle_base": 0.0003067564384801331,
  "loss_main_bundle": 0.32224280835811114,
  "loss_turn_bundle": 0.272362732157333,
  "loss_theta_bundle": 0.0003067564384801331,
  "loss_theta_flat": 0.00036053790077434777,
  "loss_theta_near_flat": 0.0017340666470174579,
  "loss_theta_error_excess": 0.00017034667778000265,
  "loss_theta_flat_excess": 0.00018021815500765393,
  "loss_theta_near_flat_excess": 0.0012868621989615837,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 8.815120647208329e-05,
  "loss_theta_small_neg": 0.00023913001991349685,
  "loss_theta_small_neg_excess": 5.136846992957843e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4159154145014302,
  "loss_false_turn_straight": 0.31883366675757585,
  "loss_transition_focal_raw": 1.1455007613431134,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 3.3725070843125255,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
