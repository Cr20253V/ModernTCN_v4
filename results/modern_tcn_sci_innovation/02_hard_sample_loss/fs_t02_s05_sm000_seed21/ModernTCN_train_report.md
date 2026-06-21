# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- loss_mode: `fixed`
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

- lambda_transition_focal: `0.2`
- lambda_stall_focal: `0.5`
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
  "lambda_transition_focal": 0.2,
  "lambda_stall_focal": 0.5,
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
| acc_main | 0.9553 |
| acc_turn | 0.4647 |
| acc_turn_pure | 0.4698 |
| acc_turn_transition | 0.4426 |
| main_confidence_mean | 0.9740 |
| main_low_conf_0p60_ratio | 0.0130 |
| main_low_conf_0p70_ratio | 0.0278 |
| turn_confidence_mean | 0.6606 |
| turn_low_conf_0p60_ratio | 0.4134 |
| turn_low_conf_0p70_ratio | 0.6086 |
| turn_right_recall | 0.5707 |
| turn_straight_recall | 0.4113 |
| turn_left_recall | 0.4862 |
| theta_mae_deg | 0.9158 |
| theta_abs_le_10_p95_abs_err_deg | 2.4069 |
| theta_neg_10_8_p95_abs_err_deg | 1.9214 |
| theta_pos_8_10_p95_abs_err_deg | 4.2516 |
| theta_abs_le_8_p95_abs_err_deg | 2.2486 |
| theta_neg_8_6_p95_abs_err_deg | 2.1375 |
| theta_pos_6_8_p95_abs_err_deg | 2.0849 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.0688 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.2772 |
| theta_flat_abs_p95_deg | 2.9843 |
| theta_flat_bias_deg | -0.4063 |
| theta_near_flat_abs_p95_deg | 2.4151 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.2746 |
| theta_flat_turn_abs_p95_deg | 2.2444 |
| flat_recall | 0.9537 |
| stall_recall | 0.6771 |
| slope_recall | 0.9655 |
| flat_as_stall_ratio | 0.0013 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7322 |
| downhill_recall | 0.8014 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    721,
    1,
    34
  ],
  [
    9,
    65,
    22
  ],
  [
    77,
    18,
    2655
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    456,
    232,
    111
  ],
  [
    533,
    795,
    605
  ],
  [
    205,
    242,
    423
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.284020 |
| test_loss_turn_bundle_base | 0.229694 |
| test_loss_theta_bundle_base | 0.000328 |
| test_loss_transition_focal_raw | 0.691217 |
| test_loss_transition_focal_weighted | 0.138243 |
| test_loss_stall_focal_raw | 2.720146 |
| test_loss_stall_focal_weighted | 1.360073 |
| test_loss_theta_smooth | 0.000000 |

- best_epoch: 38
- train_seconds: 246.6

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 47 | 0.4043 | 0.5517 |
| [0.60,0.70) | 53 | 0.3208 | 0.6554 |
| [0.70,0.80) | 66 | 0.1970 | 0.7607 |
| [0.80,0.90) | 108 | 0.2037 | 0.8540 |
| [0.90,1.00) | 3328 | 0.0270 | 0.9932 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1489 | 0.6185 | 0.4965 |
| [0.60,0.70) | 703 | 0.6259 | 0.6439 |
| [0.70,0.80) | 550 | 0.5309 | 0.7441 |
| [0.80,0.90) | 381 | 0.4199 | 0.8467 |
| [0.90,1.00) | 479 | 0.2401 | 0.9515 |


## 验证集最佳点

```json
{
  "loss_total": 1.5483016766456532,
  "acc_main": 0.9347767253044655,
  "acc_turn": 0.5499323410013531,
  "acc_turn_pure": 0.5552277941658472,
  "acc_turn_transition": 0.5248447204968945,
  "false_turn_straight": 0.5358627858627859,
  "flat_recall": 0.9604261796042618,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9365821094793058,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9604261796042618,
    0.40476190476190477,
    0.9365821094793058
  ],
  "turn_right_recall": 0.5971563981042654,
  "turn_straight_recall": 0.46413721413721415,
  "turn_left_recall": 0.6850053937432579,
  "recall_turn": [
    0.5971563981042654,
    0.46413721413721415,
    0.6850053937432579
  ],
  "cm_turn": [
    [
      504,
      185,
      155
    ],
    [
      408,
      893,
      623
    ],
    [
      121,
      171,
      635
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
      17,
      24
    ],
    [
      167,
      23,
      2806
    ]
  ],
  "main_confidence_mean": 0.9532875359684199,
  "main_confidence_error_mean": 0.7327624234332879,
  "main_low_conf_0p60_ratio": 0.056833558863328824,
  "main_low_conf_0p70_ratio": 0.06928281461434371,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 210,
      "error_rate": 0.4714285714285714,
      "mean_confidence": 0.5098188614155715
    },
    {
      "bin": "[0.60,0.70)",
      "n": 46,
      "error_rate": 0.41304347826086957,
      "mean_confidence": 0.654604471770438
    },
    {
      "bin": "[0.70,0.80)",
      "n": 62,
      "error_rate": 0.22580645161290322,
      "mean_confidence": 0.7516625483178665
    },
    {
      "bin": "[0.80,0.90)",
      "n": 108,
      "error_rate": 0.2777777777777778,
      "mean_confidence": 0.8543378474380396
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3269,
      "error_rate": 0.02416641174671153,
      "mean_confidence": 0.9930719220818555
    }
  ],
  "turn_confidence_mean": 0.6785509528515304,
  "turn_confidence_error_mean": 0.6239078524800546,
  "turn_low_conf_0p60_ratio": 0.3945872801082544,
  "turn_low_conf_0p70_ratio": 0.5539918809201624,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1458,
      "error_rate": 0.5631001371742113,
      "mean_confidence": 0.4865000691962452
    },
    {
      "bin": "[0.60,0.70)",
      "n": 589,
      "error_rate": 0.47198641765704585,
      "mean_confidence": 0.6508139881308238
    },
    {
      "bin": "[0.70,0.80)",
      "n": 535,
      "error_rate": 0.47102803738317756,
      "mean_confidence": 0.7479490785457759
    },
    {
      "bin": "[0.80,0.90)",
      "n": 454,
      "error_rate": 0.381057268722467,
      "mean_confidence": 0.8509243643988046
    },
    {
      "bin": "[0.90,1.00)",
      "n": 659,
      "error_rate": 0.2109256449165402,
      "mean_confidence": 0.9531514604403291
    }
  ],
  "theta_mae_rad": 0.019295116886496544,
  "theta_mae_deg": 1.105528712272644,
  "uphill_recall": 0.7525606469002696,
  "downhill_recall": 0.7986651835372637,
  "slope_sign_acc": 0.9614015877361073,
  "theta_flat_mae_deg": 1.3333736658096313,
  "theta_flat_abs_p95_deg": 4.211418628692627,
  "theta_flat_abs_max_deg": 9.518777847290039,
  "theta_flat_bias_deg": 0.6566357016563416,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.8478553295135498,
  "theta_near_flat_abs_p95_deg": 5.270644187927246,
  "theta_near_flat_abs_max_deg": 9.518777847290039,
  "theta_near_flat_bias_deg": 0.794566810131073,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.7425750494003296,
  "theta_flat_turn_abs_p95_deg": 6.231749534606934,
  "theta_flat_turn_abs_max_deg": 9.518777847290039,
  "theta_flat_turn_bias_deg": 0.40583887696266174,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 1.105528712272644,
  "theta_slope_control_abs_p95_deg": 9.487481117248535,
  "theta_slope_control_abs_max_deg": 13.705216407775879,
  "theta_slope_control_bias_deg": -0.14434611797332764,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 1.105528712272644,
  "theta_all_rmse_deg": 1.5057952404022217,
  "theta_all_p95_abs_err_deg": 3.0079238414764404,
  "theta_all_max_abs_err_deg": 10.018777847290039,
  "theta_all_bias_deg": -0.14434611797332764,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 1.055564045906067,
  "theta_active_abs_ge_2_rmse_deg": 1.3895611763000488,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.7878851890563965,
  "theta_active_abs_ge_2_max_abs_err_deg": 6.6992669105529785,
  "theta_active_abs_ge_2_bias_deg": -0.31999534368515015,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 1.1065491437911987,
  "theta_abs_le_8_rmse_deg": 1.522106409072876,
  "theta_abs_le_8_p95_abs_err_deg": 3.0079288482666016,
  "theta_abs_le_8_max_abs_err_deg": 10.018777847290039,
  "theta_abs_le_8_bias_deg": 0.00022330899082589895,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 1.105528712272644,
  "theta_abs_le_10_rmse_deg": 1.5057952404022217,
  "theta_abs_le_10_p95_abs_err_deg": 3.0079238414764404,
  "theta_abs_le_10_max_abs_err_deg": 10.018777847290039,
  "theta_abs_le_10_bias_deg": -0.14434611797332764,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 1.3409892320632935,
  "theta_pos_8_10_rmse_deg": 1.5859594345092773,
  "theta_pos_8_10_p95_abs_err_deg": 2.6216304302215576,
  "theta_pos_8_10_max_abs_err_deg": 6.043123245239258,
  "theta_pos_8_10_bias_deg": -1.247018575668335,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8573134541511536,
  "theta_neg_10_8_rmse_deg": 1.2629286050796509,
  "theta_neg_10_8_p95_abs_err_deg": 2.3719370365142822,
  "theta_neg_10_8_max_abs_err_deg": 5.812199592590332,
  "theta_neg_10_8_bias_deg": -0.2529057264328003,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.9893826842308044,
  "theta_pos_6_8_rmse_deg": 1.1852062940597534,
  "theta_pos_6_8_p95_abs_err_deg": 1.9687070846557617,
  "theta_pos_6_8_max_abs_err_deg": 3.4555671215057373,
  "theta_pos_6_8_bias_deg": -0.6910549998283386,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 1.1107087135314941,
  "theta_neg_8_6_rmse_deg": 1.430521011352539,
  "theta_neg_8_6_p95_abs_err_deg": 2.816282272338867,
  "theta_neg_8_6_max_abs_err_deg": 6.451869487762451,
  "theta_neg_8_6_bias_deg": -0.5253100991249084,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.8496084809303284,
  "theta_neg_4_2_rmse_deg": 1.0907676219940186,
  "theta_neg_4_2_p95_abs_err_deg": 2.2142090797424316,
  "theta_neg_4_2_max_abs_err_deg": 4.294529438018799,
  "theta_neg_4_2_bias_deg": -0.06113646551966667,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.5841837525367737,
  "theta_neg_2_0p5_rmse_deg": 0.7745269536972046,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.3945984840393066,
  "theta_neg_2_0p5_max_abs_err_deg": 3.3017513751983643,
  "theta_neg_2_0p5_bias_deg": 0.3950923979282379,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 1.4549095630645752,
  "theta_pos_0p5_2_rmse_deg": 1.794243335723877,
  "theta_pos_0p5_2_p95_abs_err_deg": 3.2937042713165283,
  "theta_pos_0p5_2_max_abs_err_deg": 3.989759922027588,
  "theta_pos_0p5_2_bias_deg": 1.0266828536987305,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.26017785340103955,
  "loss_turn": 1.0276852273811992,
  "loss_theta": 0.0006907801373032487,
  "loss_main_bundle_base": 0.26017785340103955,
  "loss_turn_bundle_base": 0.2055370478370354,
  "loss_theta_bundle_base": 0.00045963267539596346,
  "loss_main_bundle": 1.2160441232469634,
  "loss_turn_bundle": 0.33179792248025153,
  "loss_theta_bundle": 0.00045963267539596346,
  "loss_theta_flat": 0.00040141561266925834,
  "loss_theta_near_flat": 0.001880269716348857,
  "loss_theta_error_excess": 0.0002575696405358562,
  "loss_theta_flat_excess": 0.00020300668906244034,
  "loss_theta_near_flat_excess": 0.0014040034963133088,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00018655237264371023,
  "loss_theta_small_neg": 0.000362940502059375,
  "loss_theta_small_neg_excess": 7.643516666000062e-05,
  "loss_turn_release": 0.4065011539785078,
  "loss_false_turn_straight": 0.33987689286026807,
  "loss_transition_focal_raw": 0.6313043522576679,
  "loss_transition_focal_weighted": 0.12626087312890324,
  "loss_stall_focal_raw": 1.9117325928848954,
  "loss_stall_focal_weighted": 0.9558662964424477,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
