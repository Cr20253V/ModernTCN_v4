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
  "lambda_turn": 0.24,
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
  "main_neg_slope_weight": 2.4,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 3.0,
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
| acc_main | 0.9597 |
| acc_turn | 0.5075 |
| acc_turn_pure | 0.5230 |
| acc_turn_transition | 0.4396 |
| main_confidence_mean | 0.9773 |
| main_low_conf_0p60_ratio | 0.0105 |
| main_low_conf_0p70_ratio | 0.0250 |
| turn_confidence_mean | 0.7075 |
| turn_low_conf_0p60_ratio | 0.3415 |
| turn_low_conf_0p70_ratio | 0.5189 |
| turn_right_recall | 0.6421 |
| turn_straight_recall | 0.4661 |
| turn_left_recall | 0.4759 |
| theta_mae_deg | 1.0428 |
| theta_abs_le_10_p95_abs_err_deg | 3.2472 |
| theta_neg_10_8_p95_abs_err_deg | 6.0184 |
| theta_pos_8_10_p95_abs_err_deg | 5.1915 |
| theta_abs_le_8_p95_abs_err_deg | 2.8932 |
| theta_neg_8_6_p95_abs_err_deg | 2.0228 |
| theta_pos_6_8_p95_abs_err_deg | 3.7721 |
| theta_neg_2_0p5_p95_abs_err_deg | 3.2394 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.7311 |
| theta_flat_abs_p95_deg | 3.6940 |
| theta_flat_bias_deg | -0.1819 |
| theta_near_flat_abs_p95_deg | 1.8107 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.1140 |
| theta_flat_turn_abs_p95_deg | 1.7460 |
| flat_recall | 0.9550 |
| stall_recall | 0.6562 |
| slope_recall | 0.9716 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.1042 |
| uphill_recall | 0.7448 |
| downhill_recall | 0.7985 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    722,
    0,
    34
  ],
  [
    10,
    63,
    23
  ],
  [
    68,
    10,
    2672
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    513,
    201,
    85
  ],
  [
    589,
    901,
    443
  ],
  [
    268,
    188,
    414
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.256361 |
| test_loss_turn_bundle_base | 0.268466 |
| test_loss_theta_bundle_base | 0.000468 |
| test_loss_transition_focal_raw | 0.783989 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 2.848664 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 25
- train_seconds: 185.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 38 | 0.5000 | 0.5602 |
| [0.60,0.70) | 52 | 0.5769 | 0.6581 |
| [0.70,0.80) | 50 | 0.2400 | 0.7614 |
| [0.80,0.90) | 114 | 0.0965 | 0.8569 |
| [0.90,1.00) | 3348 | 0.0218 | 0.9943 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1230 | 0.6163 | 0.5186 |
| [0.60,0.70) | 639 | 0.5603 | 0.6497 |
| [0.70,0.80) | 560 | 0.5214 | 0.7519 |
| [0.80,0.90) | 503 | 0.4414 | 0.8527 |
| [0.90,1.00) | 670 | 0.2149 | 0.9636 |


## 验证集最佳点

```json
{
  "loss_total": 0.510734431524238,
  "acc_main": 0.9447902571041948,
  "acc_turn": 0.577807848443843,
  "acc_turn_pure": 0.5935758767617175,
  "acc_turn_transition": 0.5031055900621118,
  "false_turn_straight": 0.48544698544698545,
  "flat_recall": 0.928462709284627,
  "stall_recall": 0.5476190476190477,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.928462709284627,
    0.5476190476190477,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6682464454976303,
  "turn_straight_recall": 0.5145530145530145,
  "turn_left_recall": 0.6267529665587918,
  "recall_turn": [
    0.6682464454976303,
    0.5145530145530145,
    0.6267529665587918
  ],
  "cm_turn": [
    [
      564,
      231,
      49
    ],
    [
      512,
      990,
      422
    ],
    [
      172,
      174,
      581
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      610,
      0,
      47
    ],
    [
      1,
      23,
      18
    ],
    [
      133,
      5,
      2858
    ]
  ],
  "main_confidence_mean": 0.9697485559747366,
  "main_confidence_error_mean": 0.8218517455318469,
  "main_low_conf_0p60_ratio": 0.008930987821380243,
  "main_low_conf_0p70_ratio": 0.018944519621109608,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 33,
      "error_rate": 0.30303030303030304,
      "mean_confidence": 0.5526289674947145
    },
    {
      "bin": "[0.60,0.70)",
      "n": 37,
      "error_rate": 0.3783783783783784,
      "mean_confidence": 0.6588088610201208
    },
    {
      "bin": "[0.70,0.80)",
      "n": 234,
      "error_rate": 0.405982905982906,
      "mean_confidence": 0.7581199755165253
    },
    {
      "bin": "[0.80,0.90)",
      "n": 83,
      "error_rate": 0.24096385542168675,
      "mean_confidence": 0.8569468695730292
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3308,
      "error_rate": 0.019649334945586457,
      "mean_confidence": 0.9951878978525253
    }
  ],
  "turn_confidence_mean": 0.710659676585957,
  "turn_confidence_error_mean": 0.6448287644523003,
  "turn_low_conf_0p60_ratio": 0.33802435723951285,
  "turn_low_conf_0p70_ratio": 0.48200270635994585,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1249,
      "error_rate": 0.5628502802241794,
      "mean_confidence": 0.4856042028529946
    },
    {
      "bin": "[0.60,0.70)",
      "n": 532,
      "error_rate": 0.4924812030075188,
      "mean_confidence": 0.6469732664911295
    },
    {
      "bin": "[0.70,0.80)",
      "n": 526,
      "error_rate": 0.47718631178707227,
      "mean_confidence": 0.749023211344401
    },
    {
      "bin": "[0.80,0.90)",
      "n": 518,
      "error_rate": 0.35135135135135137,
      "mean_confidence": 0.8527389863689343
    },
    {
      "bin": "[0.90,1.00)",
      "n": 870,
      "error_rate": 0.18620689655172415,
      "mean_confidence": 0.9649115790139962
    }
  ],
  "theta_mae_rad": 0.01812654733657837,
  "theta_mae_deg": 1.0385745763778687,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.8109010011123471,
  "slope_sign_acc": 0.9447029838488913,
  "theta_flat_mae_deg": 1.1169716119766235,
  "theta_flat_abs_p95_deg": 2.7533226013183594,
  "theta_flat_abs_max_deg": 10.198771476745605,
  "theta_flat_bias_deg": 0.25403210520744324,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.5490376949310303,
  "theta_near_flat_abs_p95_deg": 3.870823860168457,
  "theta_near_flat_abs_max_deg": 10.198771476745605,
  "theta_near_flat_bias_deg": 0.962521493434906,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.5674463510513306,
  "theta_flat_turn_abs_p95_deg": 4.864991664886475,
  "theta_flat_turn_abs_max_deg": 10.198771476745605,
  "theta_flat_turn_bias_deg": 0.7669327855110168,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.0385745763778687,
  "theta_slope_control_abs_p95_deg": 9.69272518157959,
  "theta_slope_control_abs_max_deg": 12.263114929199219,
  "theta_slope_control_bias_deg": -0.4175685942173004,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.0385746955871582,
  "theta_all_rmse_deg": 1.43197762966156,
  "theta_all_p95_abs_err_deg": 2.864722967147827,
  "theta_all_max_abs_err_deg": 10.698771476745605,
  "theta_all_bias_deg": -0.4175685942173004,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.0213828086853027,
  "theta_active_abs_ge_2_rmse_deg": 1.3972545862197876,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.915849208831787,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.994523048400879,
  "theta_active_abs_ge_2_bias_deg": -0.5648455023765564,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.0845935344696045,
  "theta_abs_le_8_rmse_deg": 1.4849629402160645,
  "theta_abs_le_8_p95_abs_err_deg": 2.987330436706543,
  "theta_abs_le_8_max_abs_err_deg": 10.698771476745605,
  "theta_abs_le_8_bias_deg": -0.4415675401687622,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.0385746955871582,
  "theta_abs_le_10_rmse_deg": 1.43197762966156,
  "theta_abs_le_10_p95_abs_err_deg": 2.864722967147827,
  "theta_abs_le_10_max_abs_err_deg": 10.698771476745605,
  "theta_abs_le_10_bias_deg": -0.4175685942173004,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.7285267114639282,
  "theta_pos_8_10_rmse_deg": 0.9781567454338074,
  "theta_pos_8_10_p95_abs_err_deg": 1.7369999885559082,
  "theta_pos_8_10_max_abs_err_deg": 5.834730625152588,
  "theta_pos_8_10_bias_deg": -0.36339351534843445,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.962359607219696,
  "theta_neg_10_8_rmse_deg": 1.3593987226486206,
  "theta_neg_10_8_p95_abs_err_deg": 2.8493893146514893,
  "theta_neg_10_8_max_abs_err_deg": 6.85081148147583,
  "theta_neg_10_8_bias_deg": -0.26844698190689087,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.8700087666511536,
  "theta_pos_6_8_rmse_deg": 1.1174060106277466,
  "theta_pos_6_8_p95_abs_err_deg": 2.183450698852539,
  "theta_pos_6_8_max_abs_err_deg": 4.130857944488525,
  "theta_pos_6_8_bias_deg": -0.3386009633541107,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.1946204900741577,
  "theta_neg_8_6_rmse_deg": 1.5812512636184692,
  "theta_neg_8_6_p95_abs_err_deg": 3.363478899002075,
  "theta_neg_8_6_max_abs_err_deg": 6.579420566558838,
  "theta_neg_8_6_bias_deg": -0.8505749106407166,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 1.1987313032150269,
  "theta_neg_4_2_rmse_deg": 1.6109638214111328,
  "theta_neg_4_2_p95_abs_err_deg": 3.279890537261963,
  "theta_neg_4_2_max_abs_err_deg": 5.322887420654297,
  "theta_neg_4_2_bias_deg": -0.8854771852493286,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6885993480682373,
  "theta_neg_2_0p5_rmse_deg": 0.8901068568229675,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.4485238790512085,
  "theta_neg_2_0p5_max_abs_err_deg": 4.785062313079834,
  "theta_neg_2_0p5_bias_deg": -0.0891302153468132,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.0177072286605835,
  "theta_pos_0p5_2_rmse_deg": 1.2036582231521606,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.0867693424224854,
  "theta_pos_0p5_2_max_abs_err_deg": 3.590789794921875,
  "theta_pos_0p5_2_bias_deg": -0.425127238035202,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.2706515895981589,
  "loss_turn": 0.9986163670219814,
  "loss_theta": 0.0006247190485899973,
  "loss_main_bundle_base": 0.2706515895981589,
  "loss_turn_bundle_base": 0.23966792174621268,
  "loss_theta_bundle_base": 0.00041491407990053606,
  "loss_main_bundle": 0.2706515895981589,
  "loss_turn_bundle": 0.23966792174621268,
  "loss_theta_bundle": 0.00041491407990053606,
  "loss_theta_flat": 0.0003201474885063067,
  "loss_theta_near_flat": 0.001170381051311786,
  "loss_theta_error_excess": 0.00023361202337273746,
  "loss_theta_flat_excess": 0.00011942367348666379,
  "loss_theta_near_flat_excess": 0.0008042986392729105,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00021220292237238185,
  "loss_theta_small_neg": 0.0007903240678431176,
  "loss_theta_small_neg_excess": 0.0003004603173283807,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4317322906041178,
  "loss_false_turn_straight": 0.3436250568484744,
  "loss_transition_focal_raw": 0.6298997087633497,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 2.9022730333859883,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
