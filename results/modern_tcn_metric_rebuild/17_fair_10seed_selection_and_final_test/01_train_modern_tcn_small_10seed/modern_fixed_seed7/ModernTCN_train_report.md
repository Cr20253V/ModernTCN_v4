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
  "select_theta_flat_bias_target_deg": 0.15,
  "freeze_mode": "none",
  "freeze_early_blocks": 3,
  "preserve_mode": "none",
  "lambda_preserve_main": 0.0,
  "lambda_preserve_turn": 0.0,
  "lambda_preserve_theta": 0.0,
  "s_range": 0.25,
  "lambda_s_prior": 0.01
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9661 |
| acc_turn | 0.6061 |
| acc_turn_pure | 0.6230 |
| acc_turn_transition | 0.5320 |
| main_confidence_mean | 0.9917 |
| main_low_conf_0p60_ratio | 0.0042 |
| main_low_conf_0p70_ratio | 0.0094 |
| turn_confidence_mean | 0.8189 |
| turn_low_conf_0p60_ratio | 0.1752 |
| turn_low_conf_0p70_ratio | 0.2776 |
| turn_right_recall | 0.5532 |
| turn_straight_recall | 0.6239 |
| turn_left_recall | 0.6149 |
| theta_mae_deg | 0.6027 |
| theta_abs_le_10_p95_abs_err_deg | 1.5144 |
| theta_neg_10_8_p95_abs_err_deg | 1.4232 |
| theta_pos_8_10_p95_abs_err_deg | 3.2802 |
| theta_abs_le_8_p95_abs_err_deg | 1.3786 |
| theta_neg_8_6_p95_abs_err_deg | 1.5867 |
| theta_pos_6_8_p95_abs_err_deg | 1.1773 |
| theta_neg_2_0p5_p95_abs_err_deg | 1.3323 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.4452 |
| theta_flat_abs_p95_deg | 2.2798 |
| theta_flat_bias_deg | -0.4072 |
| theta_near_flat_abs_p95_deg | 1.6201 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.4165 |
| theta_flat_turn_abs_p95_deg | 1.5804 |
| flat_recall | 0.9405 |
| stall_recall | 0.6979 |
| slope_recall | 0.9825 |
| flat_as_stall_ratio | 0.0000 |
| stall_as_flat_ratio | 0.0938 |
| uphill_recall | 0.7626 |
| downhill_recall | 0.8042 |

## 混淆矩阵

### main: rows truth flat/stall/slope, columns pred flat/stall/slope

```json
[
  [
    711,
    0,
    45
  ],
  [
    9,
    67,
    20
  ],
  [
    41,
    7,
    2702
  ]
]
```

### turn: rows truth right/straight/left, columns pred right/straight/left

```json
[
  [
    442,
    216,
    141
  ],
  [
    301,
    1206,
    426
  ],
  [
    122,
    213,
    535
  ]
]
```

## Loss scale

| component | value |
|---|---:|
| test_loss_main_bundle_base | 0.377725 |
| test_loss_turn_bundle_base | 0.118684 |
| test_loss_theta_bundle_base | 0.000150 |
| test_loss_transition_focal_raw | 1.434005 |
| test_loss_transition_focal_weighted | 0.000000 |
| test_loss_stall_focal_raw | 4.276696 |
| test_loss_stall_focal_weighted | 0.000000 |
| test_loss_theta_smooth | 0.000000 |
| test_loss_flat_theta_expert_reg | 0.000000 |
| test_loss_flat_theta_expert_reg_weighted | 0.000000 |

- best_epoch: 93
- train_seconds: 1236.4

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 15 | 0.5333 | 0.5310 |
| [0.60,0.70) | 19 | 0.4737 | 0.6452 |
| [0.70,0.80) | 15 | 0.4667 | 0.7622 |
| [0.80,0.90) | 39 | 0.4103 | 0.8595 |
| [0.90,1.00) | 3514 | 0.0233 | 0.9980 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 631 | 0.5008 | 0.5168 |
| [0.60,0.70) | 369 | 0.4932 | 0.6471 |
| [0.70,0.80) | 408 | 0.5147 | 0.7563 |
| [0.80,0.90) | 510 | 0.4549 | 0.8511 |
| [0.90,1.00) | 1684 | 0.2844 | 0.9752 |


## 验证集最佳点

```json
{
  "loss_total": 0.43305938594718746,
  "acc_main": 0.9480378890392422,
  "acc_turn": 0.6408660351826793,
  "acc_turn_pure": 0.6578171091445427,
  "acc_turn_transition": 0.5605590062111802,
  "false_turn_straight": 0.38253638253638256,
  "flat_recall": 0.9558599695585996,
  "stall_recall": 0.40476190476190477,
  "slope_recall": 0.9539385847797063,
  "flat_as_stall_ratio": 0.0,
  "stall_as_flat_ratio": 0.023809523809523808,
  "recall_main": [
    0.9558599695585996,
    0.40476190476190477,
    0.9539385847797063
  ],
  "turn_right_recall": 0.6149289099526066,
  "turn_straight_recall": 0.6174636174636174,
  "turn_left_recall": 0.7130528586839266,
  "recall_turn": [
    0.6149289099526066,
    0.6174636174636174,
    0.7130528586839266
  ],
  "cm_turn": [
    [
      519,
      256,
      69
    ],
    [
      285,
      1188,
      451
    ],
    [
      46,
      220,
      661
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
      1,
      17,
      24
    ],
    [
      122,
      16,
      2858
    ]
  ],
  "main_confidence_mean": 0.9683731867395331,
  "main_confidence_error_mean": 0.7432510379162661,
  "main_low_conf_0p60_ratio": 0.05115020297699594,
  "main_low_conf_0p70_ratio": 0.05602165087956698,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 189,
      "error_rate": 0.455026455026455,
      "mean_confidence": 0.5000424001241506
    },
    {
      "bin": "[0.60,0.70)",
      "n": 18,
      "error_rate": 0.3333333333333333,
      "mean_confidence": 0.6516054356927362
    },
    {
      "bin": "[0.70,0.80)",
      "n": 18,
      "error_rate": 0.2222222222222222,
      "mean_confidence": 0.7525189487555126
    },
    {
      "bin": "[0.80,0.90)",
      "n": 31,
      "error_rate": 0.3548387096774194,
      "mean_confidence": 0.8584329054883433
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3439,
      "error_rate": 0.02471648735097412,
      "mean_confidence": 0.9978904484992449
    }
  ],
  "turn_confidence_mean": 0.8411539008512959,
  "turn_confidence_error_mean": 0.7749068465422452,
  "turn_low_conf_0p60_ratio": 0.1496617050067659,
  "turn_low_conf_0p70_ratio": 0.23355886332882272,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 553,
      "error_rate": 0.5678119349005425,
      "mean_confidence": 0.48789914539438306
    },
    {
      "bin": "[0.60,0.70)",
      "n": 310,
      "error_rate": 0.567741935483871,
      "mean_confidence": 0.6490092259579084
    },
    {
      "bin": "[0.70,0.80)",
      "n": 330,
      "error_rate": 0.45151515151515154,
      "mean_confidence": 0.7524896657507072
    },
    {
      "bin": "[0.80,0.90)",
      "n": 457,
      "error_rate": 0.4026258205689278,
      "mean_confidence": 0.8500609766666879
    },
    {
      "bin": "[0.90,1.00)",
      "n": 2045,
      "error_rate": 0.24645476772616137,
      "mean_confidence": 0.9781237751398939
    }
  ],
  "theta_mae_rad": 0.012553850188851357,
  "theta_mae_deg": 0.7192825675010681,
  "uphill_recall": 0.7800539083557951,
  "downhill_recall": 0.8008898776418243,
  "slope_sign_acc": 0.9753627155762387,
  "theta_flat_mae_deg": 0.9232357740402222,
  "theta_flat_abs_p95_deg": 3.4647016525268555,
  "theta_flat_abs_max_deg": 5.481860637664795,
  "theta_flat_bias_deg": 0.13921542465686798,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.1517094373703003,
  "theta_near_flat_abs_p95_deg": 3.4647603034973145,
  "theta_near_flat_abs_max_deg": 6.644147872924805,
  "theta_near_flat_bias_deg": 0.4183795750141144,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 0.7815299034118652,
  "theta_flat_turn_abs_p95_deg": 3.4647016525268555,
  "theta_flat_turn_abs_max_deg": 3.4647016525268555,
  "theta_flat_turn_bias_deg": 0.04798862338066101,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.7192825675010681,
  "theta_slope_control_abs_p95_deg": 9.030226707458496,
  "theta_slope_control_abs_max_deg": 13.627239227294922,
  "theta_slope_control_bias_deg": -0.0271441750228405,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.7192825675010681,
  "theta_all_rmse_deg": 1.0627124309539795,
  "theta_all_p95_abs_err_deg": 2.375411033630371,
  "theta_all_max_abs_err_deg": 7.306053161621094,
  "theta_all_bias_deg": -0.0271441787481308,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.6745572090148926,
  "theta_active_abs_ge_2_rmse_deg": 1.0079158544540405,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.0695347785949707,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.306053161621094,
  "theta_active_abs_ge_2_bias_deg": -0.06362557411193848,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.7270352244377136,
  "theta_abs_le_8_rmse_deg": 1.0733345746994019,
  "theta_abs_le_8_p95_abs_err_deg": 2.498664379119873,
  "theta_abs_le_8_max_abs_err_deg": 7.306053161621094,
  "theta_abs_le_8_bias_deg": -0.0564018152654171,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.7192825675010681,
  "theta_abs_le_10_rmse_deg": 1.0627124309539795,
  "theta_abs_le_10_p95_abs_err_deg": 2.375411033630371,
  "theta_abs_le_10_max_abs_err_deg": 7.306053161621094,
  "theta_abs_le_10_bias_deg": -0.0271441787481308,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.5923213958740234,
  "theta_pos_8_10_rmse_deg": 0.7889318466186523,
  "theta_pos_8_10_p95_abs_err_deg": 1.2857489585876465,
  "theta_pos_8_10_max_abs_err_deg": 4.543820858001709,
  "theta_pos_8_10_bias_deg": -0.32230132818222046,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.7824636697769165,
  "theta_neg_10_8_rmse_deg": 1.204980492591858,
  "theta_neg_10_8_p95_abs_err_deg": 2.012632131576538,
  "theta_neg_10_8_max_abs_err_deg": 6.934577941894531,
  "theta_neg_10_8_bias_deg": 0.5221015810966492,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.5981826186180115,
  "theta_pos_6_8_rmse_deg": 0.8652662634849548,
  "theta_pos_6_8_p95_abs_err_deg": 1.8305822610855103,
  "theta_pos_6_8_max_abs_err_deg": 3.9648597240448,
  "theta_pos_6_8_bias_deg": -0.22169478237628937,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.7489953637123108,
  "theta_neg_8_6_rmse_deg": 1.1220781803131104,
  "theta_neg_8_6_p95_abs_err_deg": 2.006772756576538,
  "theta_neg_8_6_max_abs_err_deg": 7.306053161621094,
  "theta_neg_8_6_bias_deg": 0.09173455089330673,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.6052461266517639,
  "theta_neg_4_2_rmse_deg": 0.9005560874938965,
  "theta_neg_4_2_p95_abs_err_deg": 1.7184159755706787,
  "theta_neg_4_2_max_abs_err_deg": 4.369545936584473,
  "theta_neg_4_2_bias_deg": -0.2880653142929077,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.6683340668678284,
  "theta_neg_2_0p5_rmse_deg": 0.8485124707221985,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.5561484098434448,
  "theta_neg_2_0p5_max_abs_err_deg": 3.4784042835235596,
  "theta_neg_2_0p5_bias_deg": -0.333198606967926,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.9642322659492493,
  "theta_pos_0p5_2_rmse_deg": 1.2260887622833252,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.9647016525268555,
  "theta_pos_0p5_2_max_abs_err_deg": 3.709888219833374,
  "theta_pos_0p5_2_bias_deg": 0.3816843330860138,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.31394649473030284,
  "loss_turn": 1.4860129741596433,
  "loss_theta": 0.0003441125646306653,
  "loss_main_bundle_base": 0.31394649473030284,
  "loss_turn_bundle_base": 0.11888103515353352,
  "loss_theta_bundle_base": 0.0002318531281018002,
  "loss_main_bundle": 0.31394649473030284,
  "loss_turn_bundle": 0.11888103515353352,
  "loss_theta_bundle": 0.0002318531281018002,
  "loss_theta_flat": 0.00022670005014795099,
  "loss_theta_near_flat": 0.0008359844680889402,
  "loss_theta_error_excess": 0.00011019399092285056,
  "loss_theta_flat_excess": 0.0001029119238848836,
  "loss_theta_near_flat_excess": 0.0005407901142653915,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 9.87750858644084e-05,
  "loss_theta_small_neg": 0.0002447878524121678,
  "loss_theta_small_neg_excess": 6.83108523392896e-05,
  "loss_flat_theta_expert_reg": 0.0,
  "loss_flat_theta_expert_reg_weighted": 0.0,
  "loss_turn_release": 0.4108477261053532,
  "loss_false_turn_straight": 0.2964194579601933,
  "loss_transition_focal_raw": 1.2841179534772735,
  "loss_transition_focal_weighted": 0.0,
  "loss_stall_focal_raw": 4.101655365945792,
  "loss_stall_focal_weighted": 0.0,
  "loss_theta_smooth": 0.0,
  "theta_smooth_status": 0.0
}
```
