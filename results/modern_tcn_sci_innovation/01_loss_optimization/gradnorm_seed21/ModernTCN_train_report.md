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
| acc_main | 0.9697 |
| acc_turn | 0.4881 |
| acc_turn_pure | 0.5070 |
| acc_turn_transition | 0.4054 |
| main_confidence_mean | 0.9815 |
| main_low_conf_0p60_ratio | 0.0103 |
| main_low_conf_0p70_ratio | 0.0205 |
| turn_confidence_mean | 0.7114 |
| turn_low_conf_0p60_ratio | 0.3201 |
| turn_low_conf_0p70_ratio | 0.4981 |
| turn_right_recall | 0.6320 |
| turn_straight_recall | 0.4149 |
| turn_left_recall | 0.5184 |
| theta_mae_deg | 0.8419 |
| theta_abs_le_10_p95_abs_err_deg | 2.3141 |
| theta_neg_10_8_p95_abs_err_deg | 2.2901 |
| theta_pos_8_10_p95_abs_err_deg | 4.0993 |
| theta_abs_le_8_p95_abs_err_deg | 2.1880 |
| theta_neg_8_6_p95_abs_err_deg | 1.9385 |
| theta_pos_6_8_p95_abs_err_deg | 1.8977 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4339 |
| theta_pos_0p5_2_p95_abs_err_deg | 2.0487 |
| theta_flat_abs_p95_deg | 3.0591 |
| theta_flat_bias_deg | 0.1325 |
| theta_near_flat_abs_p95_deg | 2.0891 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | 0.1211 |
| theta_flat_turn_abs_p95_deg | 1.9482 |
| flat_recall | 0.9669 |
| stall_recall | 0.6667 |
| slope_recall | 0.9811 |
| uphill_recall | 0.7597 |
| downhill_recall | 0.7934 |

- best_epoch: 25
- train_seconds: 320.0

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 37 | 0.2973 | 0.5566 |
| [0.60,0.70) | 37 | 0.2432 | 0.6476 |
| [0.70,0.80) | 38 | 0.2895 | 0.7482 |
| [0.80,0.90) | 74 | 0.2027 | 0.8591 |
| [0.90,1.00) | 3416 | 0.0184 | 0.9950 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 1153 | 0.6496 | 0.5127 |
| [0.60,0.70) | 641 | 0.6131 | 0.6490 |
| [0.70,0.80) | 597 | 0.4757 | 0.7495 |
| [0.80,0.90) | 506 | 0.4862 | 0.8469 |
| [0.90,1.00) | 705 | 0.2440 | 0.9634 |


## 验证集最佳点

```json
{
  "loss_total": 0.46050679151356944,
  "acc_main": 0.9491204330175913,
  "acc_turn": 0.5580514208389716,
  "acc_turn_pure": 0.5722713864306784,
  "acc_turn_transition": 0.4906832298136646,
  "false_turn_straight": 0.5826403326403327,
  "flat_recall": 0.9482496194824962,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9552736982643525,
  "recall_main": [
    0.9482496194824962,
    0.5238095238095238,
    0.9552736982643525
  ],
  "turn_right_recall": 0.7428909952606635,
  "turn_straight_recall": 0.41735966735966734,
  "turn_left_recall": 0.6817691477885652,
  "recall_turn": [
    0.7428909952606635,
    0.41735966735966734,
    0.6817691477885652
  ],
  "cm_turn": [
    [
      627,
      155,
      62
    ],
    [
      677,
      803,
      444
    ],
    [
      176,
      119,
      632
    ]
  ],
  "n_turn_transition": 644,
  "n_turn_pure": 3051,
  "cm_main": [
    [
      623,
      0,
      34
    ],
    [
      0,
      22,
      20
    ],
    [
      127,
      7,
      2862
    ]
  ],
  "main_confidence_mean": 0.9766557206533549,
  "main_confidence_error_mean": 0.8616578120084974,
  "main_low_conf_0p60_ratio": 0.005412719891745603,
  "main_low_conf_0p70_ratio": 0.014343707713125846,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 20,
      "error_rate": 0.4,
      "mean_confidence": 0.5627305078479926
    },
    {
      "bin": "[0.60,0.70)",
      "n": 33,
      "error_rate": 0.21212121212121213,
      "mean_confidence": 0.6482064279849155
    },
    {
      "bin": "[0.70,0.80)",
      "n": 47,
      "error_rate": 0.2765957446808511,
      "mean_confidence": 0.7527851162952602
    },
    {
      "bin": "[0.80,0.90)",
      "n": 236,
      "error_rate": 0.3898305084745763,
      "mean_confidence": 0.8317410592037463
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3359,
      "error_rate": 0.02024412027389104,
      "mean_confidence": 0.9956611119665743
    }
  ],
  "turn_confidence_mean": 0.707740500272133,
  "turn_confidence_error_mean": 0.6302767745172884,
  "turn_low_conf_0p60_ratio": 0.3469553450608931,
  "turn_low_conf_0p70_ratio": 0.49174560216508795,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 1282,
      "error_rate": 0.641185647425897,
      "mean_confidence": 0.4916939600059906
    },
    {
      "bin": "[0.60,0.70)",
      "n": 535,
      "error_rate": 0.4654205607476635,
      "mean_confidence": 0.6462199480643113
    },
    {
      "bin": "[0.70,0.80)",
      "n": 503,
      "error_rate": 0.3856858846918489,
      "mean_confidence": 0.7475820187049215
    },
    {
      "bin": "[0.80,0.90)",
      "n": 546,
      "error_rate": 0.41208791208791207,
      "mean_confidence": 0.8493912597648428
    },
    {
      "bin": "[0.90,1.00)",
      "n": 829,
      "error_rate": 0.17249698431845598,
      "mean_confidence": 0.9640777277723346
    }
  ],
  "theta_mae_rad": 0.015548886731266975,
  "theta_mae_deg": 0.8908855319023132,
  "uphill_recall": 0.7827493261455526,
  "downhill_recall": 0.8031145717463849,
  "slope_sign_acc": 0.9542841500136874,
  "theta_flat_mae_deg": 1.1292587518692017,
  "theta_flat_abs_p95_deg": 2.7047815322875977,
  "theta_flat_abs_max_deg": 9.469922065734863,
  "theta_flat_bias_deg": 0.7802691459655762,
  "theta_flat_n": 657.0,
  "theta_near_flat_mae_deg": 1.7079126834869385,
  "theta_near_flat_abs_p95_deg": 5.433930397033691,
  "theta_near_flat_abs_max_deg": 9.469922065734863,
  "theta_near_flat_bias_deg": 1.500777006149292,
  "theta_near_flat_n": 323.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.5319502353668213,
  "theta_flat_turn_abs_p95_deg": 5.339526176452637,
  "theta_flat_turn_abs_max_deg": 9.469922065734863,
  "theta_flat_turn_bias_deg": 1.3389859199523926,
  "theta_flat_turn_n": 165.0,
  "theta_slope_control_mae_deg": 0.8908855319023132,
  "theta_slope_control_abs_p95_deg": 9.387767791748047,
  "theta_slope_control_abs_max_deg": 12.680880546569824,
  "theta_slope_control_bias_deg": 0.17080920934677124,
  "theta_slope_control_n": 3653.0,
  "theta_all_mae_deg": 0.8908855319023132,
  "theta_all_rmse_deg": 1.284388780593872,
  "theta_all_p95_abs_err_deg": 2.6082868576049805,
  "theta_all_max_abs_err_deg": 9.969921112060547,
  "theta_all_bias_deg": 0.17080920934677124,
  "theta_all_n": 3653.0,
  "theta_active_abs_ge_2_mae_deg": 0.8386120200157166,
  "theta_active_abs_ge_2_rmse_deg": 1.195960283279419,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.514296054840088,
  "theta_active_abs_ge_2_max_abs_err_deg": 7.081138610839844,
  "theta_active_abs_ge_2_bias_deg": 0.0371592752635479,
  "theta_active_abs_ge_2_n": 2996.0,
  "theta_abs_le_8_mae_deg": 0.9258970022201538,
  "theta_abs_le_8_rmse_deg": 1.3267685174942017,
  "theta_abs_le_8_p95_abs_err_deg": 2.6959309577941895,
  "theta_abs_le_8_max_abs_err_deg": 9.969921112060547,
  "theta_abs_le_8_bias_deg": 0.18239040672779083,
  "theta_abs_le_8_n": 2953.0,
  "theta_abs_le_10_mae_deg": 0.8908855319023132,
  "theta_abs_le_10_rmse_deg": 1.284388780593872,
  "theta_abs_le_10_p95_abs_err_deg": 2.6082868576049805,
  "theta_abs_le_10_max_abs_err_deg": 9.969921112060547,
  "theta_abs_le_10_bias_deg": 0.17080920934677124,
  "theta_abs_le_10_n": 3653.0,
  "theta_pos_8_10_mae_deg": 0.6214279532432556,
  "theta_pos_8_10_rmse_deg": 0.8868059515953064,
  "theta_pos_8_10_p95_abs_err_deg": 1.6250656843185425,
  "theta_pos_8_10_max_abs_err_deg": 5.755409240722656,
  "theta_pos_8_10_bias_deg": -0.0170562993735075,
  "theta_pos_8_10_n": 353.0,
  "theta_neg_10_8_mae_deg": 0.8670510053634644,
  "theta_neg_10_8_rmse_deg": 1.2593979835510254,
  "theta_neg_10_8_p95_abs_err_deg": 2.468205213546753,
  "theta_neg_10_8_max_abs_err_deg": 6.12591028213501,
  "theta_neg_10_8_bias_deg": 0.2633662223815918,
  "theta_neg_10_8_n": 347.0,
  "theta_pos_6_8_mae_deg": 0.6706947684288025,
  "theta_pos_6_8_rmse_deg": 0.9394864439964294,
  "theta_pos_6_8_p95_abs_err_deg": 1.857049822807312,
  "theta_pos_6_8_max_abs_err_deg": 4.071826457977295,
  "theta_pos_6_8_bias_deg": 0.042910799384117126,
  "theta_pos_6_8_n": 410.0,
  "theta_neg_8_6_mae_deg": 0.8468774557113647,
  "theta_neg_8_6_rmse_deg": 1.1923166513442993,
  "theta_neg_8_6_p95_abs_err_deg": 2.1716315746307373,
  "theta_neg_8_6_max_abs_err_deg": 6.845780372619629,
  "theta_neg_8_6_bias_deg": -0.12905412912368774,
  "theta_neg_8_6_n": 379.0,
  "theta_neg_4_2_mae_deg": 0.9383450746536255,
  "theta_neg_4_2_rmse_deg": 1.3213016986846924,
  "theta_neg_4_2_p95_abs_err_deg": 2.5285699367523193,
  "theta_neg_4_2_max_abs_err_deg": 6.303370952606201,
  "theta_neg_4_2_bias_deg": -0.11216669529676437,
  "theta_neg_4_2_n": 364.0,
  "theta_neg_2_0p5_mae_deg": 0.8119699358940125,
  "theta_neg_2_0p5_rmse_deg": 1.013266682624817,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.669870138168335,
  "theta_neg_2_0p5_max_abs_err_deg": 4.467861175537109,
  "theta_neg_2_0p5_bias_deg": 0.4247609078884125,
  "theta_neg_2_0p5_n": 183.0,
  "theta_pos_0p5_2_mae_deg": 0.7471646070480347,
  "theta_pos_0p5_2_rmse_deg": 0.9877654314041138,
  "theta_pos_0p5_2_p95_abs_err_deg": 1.8568083047866821,
  "theta_pos_0p5_2_max_abs_err_deg": 4.781594276428223,
  "theta_pos_0p5_2_bias_deg": 0.18567965924739838,
  "theta_pos_0p5_2_n": 163.0,
  "loss_main": 0.27241560061019876,
  "loss_turn": 0.9387111659301633,
  "loss_theta": 0.0005024826334013083,
  "loss_main_bundle": 0.27241560061019876,
  "loss_turn_bundle": 0.18774223554682828,
  "loss_theta_bundle": 0.00034895699921143477,
  "loss_theta_flat": 0.0004105218177811269,
  "loss_theta_near_flat": 0.0013408616642657976,
  "loss_theta_error_excess": 0.00018166220175963731,
  "loss_theta_flat_excess": 0.00019768610551089454,
  "loss_theta_near_flat_excess": 0.0009292992765741757,
  "loss_theta_true_zero_excess": 0.0,
  "loss_theta_active_excess": 0.00014245819306871898,
  "loss_theta_small_neg": 0.0005290086170518582,
  "loss_theta_small_neg_excess": 0.00018271991593915408,
  "loss_turn_release": 0.4740654433451099,
  "loss_false_turn_straight": 0.3669724325688508
}
```
