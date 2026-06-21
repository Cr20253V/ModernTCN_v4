# ModernTCN-small 第一阶段训练报告

## 固定约束

- model_family: `small`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256.mat`
- vehicle: `diagonal_dual_steer_drive_agv`; active=`LF,RR`; passive=`RF,LR`
- feature_policy: `keep_current_algorithm_inputs_unchanged`
- label_time_policy: `current_window_end`, horizon_steps=0
- split: 使用 MAT 文件已有 run-level split，不重划分。
- scaler: 使用 MAT 文件已有归一化后 X，不重新拟合。
- confidence_policy: `derive_classification_confidence_from_softmax_and_export`
- input: `[batch, time=256, feature=22]`
- output: `logits_main`, `logits_turn`, `theta_hat`

## 配置

```json
{
  "input_dim": 22,
  "seq_len": 256,
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
  "lambda_theta_error_excess": 0.0,
  "lambda_theta_flat_excess": 0.0,
  "lambda_theta_near_flat_excess": 0.0,
  "lambda_theta_true_zero_excess": 0.0,
  "lambda_theta_active_excess": 0.0,
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
  "select_turn_left_target": 0.8,
  "select_turn_lr_weight": 0.0,
  "select_turn_lr_target": 0.8,
  "select_stall_weight": 0.0,
  "select_stall_target": 0.7,
  "select_theta_weight": 0.3,
  "select_theta_ref_deg": 5.0,
  "select_theta_p95_weight": 0.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 0.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 0.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 0.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 0.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 0.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_extreme_p95_weight": 0.0,
  "select_theta_extreme_p95_target_deg": 1.0,
  "select_theta_edge_p95_weight": 0.0,
  "select_theta_edge_p95_target_deg": 1.2,
  "select_theta_small_nonzero_p95_weight": 0.0,
  "select_theta_small_nonzero_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## 测试集指标

| metric | value |
|---|---:|
| acc_main | 0.9593 |
| acc_turn | 0.6086 |
| acc_turn_pure | 0.6411 |
| acc_turn_transition | 0.5415 |
| main_confidence_mean | 0.9862 |
| main_low_conf_0p60_ratio | 0.0081 |
| main_low_conf_0p70_ratio | 0.0152 |
| turn_confidence_mean | 0.7647 |
| turn_low_conf_0p60_ratio | 0.2269 |
| turn_low_conf_0p70_ratio | 0.3817 |
| turn_right_recall | 0.6224 |
| turn_straight_recall | 0.5898 |
| turn_left_recall | 0.6359 |
| theta_mae_deg | 0.8205 |
| theta_abs_le_10_p95_abs_err_deg | 2.2954 |
| theta_neg_10_8_p95_abs_err_deg | 2.3239 |
| theta_pos_8_10_p95_abs_err_deg | 4.1758 |
| theta_abs_le_8_p95_abs_err_deg | 2.1438 |
| theta_neg_8_6_p95_abs_err_deg | 1.9098 |
| theta_pos_6_8_p95_abs_err_deg | 1.9717 |
| theta_neg_2_0p5_p95_abs_err_deg | 2.4268 |
| theta_pos_0p5_2_p95_abs_err_deg | 1.8057 |
| theta_flat_abs_p95_deg | 2.7290 |
| theta_flat_bias_deg | 0.0295 |
| theta_near_flat_abs_p95_deg | 1.6775 |
| theta_true_zero_abs_p95_deg | nan |
| theta_near_flat_bias_deg | -0.0891 |
| theta_flat_turn_abs_p95_deg | 1.3061 |
| flat_recall | 0.9051 |
| stall_recall | 0.6279 |
| slope_recall | 0.9835 |
| uphill_recall | 0.7729 |
| downhill_recall | 0.8249 |

- best_epoch: 27
- train_seconds: 291.8

## 置信度分桶

### main

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 30 | 0.5667 | 0.5359 |
| [0.60,0.70) | 26 | 0.3462 | 0.6467 |
| [0.70,0.80) | 30 | 0.3667 | 0.7553 |
| [0.80,0.90) | 50 | 0.3800 | 0.8612 |
| [0.90,1.00) | 3548 | 0.0265 | 0.9962 |

### turn

| confidence bin | n | error rate | mean confidence |
|---|---:|---:|---:|
| [0.00,0.60) | 836 | 0.5311 | 0.5102 |
| [0.60,0.70) | 570 | 0.4807 | 0.6505 |
| [0.70,0.80) | 529 | 0.3837 | 0.7521 |
| [0.80,0.90) | 598 | 0.3846 | 0.8507 |
| [0.90,1.00) | 1151 | 0.2528 | 0.9672 |


## 验证集最佳点

```json
{
  "loss_total": 0.3965774105786994,
  "acc_main": 0.942504157757187,
  "acc_turn": 0.6274649560465669,
  "acc_turn_pure": 0.6609993060374739,
  "acc_turn_transition": 0.5546345139412208,
  "false_turn_straight": 0.4251968503937008,
  "flat_recall": 0.9232839838492598,
  "stall_recall": 0.5238095238095238,
  "slope_recall": 0.9518107476635514,
  "recall_main": [
    0.9232839838492598,
    0.5238095238095238,
    0.9518107476635514
  ],
  "turn_right_recall": 0.6909650924024641,
  "turn_straight_recall": 0.5748031496062992,
  "turn_left_recall": 0.6756505576208178,
  "recall_turn": [
    0.6909650924024641,
    0.5748031496062992,
    0.6756505576208178
  ],
  "cm_turn": [
    [
      673,
      239,
      62
    ],
    [
      526,
      1241,
      392
    ],
    [
      149,
      200,
      727
    ]
  ],
  "n_turn_transition": 1327,
  "n_turn_pure": 2882,
  "cm_main": [
    [
      686,
      0,
      57
    ],
    [
      0,
      22,
      20
    ],
    [
      164,
      1,
      3259
    ]
  ],
  "main_confidence_mean": 0.9621966177156819,
  "main_confidence_error_mean": 0.6984191364906802,
  "main_low_conf_0p60_ratio": 0.05203136136849608,
  "main_low_conf_0p70_ratio": 0.060109289617486336,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 219,
      "error_rate": 0.5251141552511416,
      "mean_confidence": 0.48243761902056737
    },
    {
      "bin": "[0.60,0.70)",
      "n": 34,
      "error_rate": 0.5882352941176471,
      "mean_confidence": 0.6499500741576041
    },
    {
      "bin": "[0.70,0.80)",
      "n": 40,
      "error_rate": 0.275,
      "mean_confidence": 0.7496109063996389
    },
    {
      "bin": "[0.80,0.90)",
      "n": 58,
      "error_rate": 0.22413793103448276,
      "mean_confidence": 0.8478014892890653
    },
    {
      "bin": "[0.90,1.00)",
      "n": 3858,
      "error_rate": 0.021513737687921204,
      "mean_confidence": 0.9961058839408219
    }
  ],
  "turn_confidence_mean": 0.7857658925208313,
  "turn_confidence_error_mean": 0.7086555199706746,
  "turn_low_conf_0p60_ratio": 0.2195295794725588,
  "turn_low_conf_0p70_ratio": 0.33380850558327396,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 924,
      "error_rate": 0.5768398268398268,
      "mean_confidence": 0.5040956578473768
    },
    {
      "bin": "[0.60,0.70)",
      "n": 481,
      "error_rate": 0.48440748440748443,
      "mean_confidence": 0.6504107378185927
    },
    {
      "bin": "[0.70,0.80)",
      "n": 502,
      "error_rate": 0.4362549800796813,
      "mean_confidence": 0.7511136096517734
    },
    {
      "bin": "[0.80,0.90)",
      "n": 670,
      "error_rate": 0.37910447761194027,
      "mean_confidence": 0.8553389081748465
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1632,
      "error_rate": 0.20159313725490197,
      "mean_confidence": 0.9672307526691925
    }
  ],
  "theta_mae_rad": 0.017748745158314705,
  "theta_mae_deg": 1.0169280767440796,
  "uphill_recall": 0.7749408983451537,
  "downhill_recall": 0.8172514619883041,
  "slope_sign_acc": 0.9695224382049437,
  "theta_flat_mae_deg": 1.2675358057022095,
  "theta_flat_abs_p95_deg": 4.047972679138184,
  "theta_flat_abs_max_deg": 15.019281387329102,
  "theta_flat_bias_deg": 0.6799855828285217,
  "theta_flat_n": 743.0,
  "theta_near_flat_mae_deg": 1.6135947704315186,
  "theta_near_flat_abs_p95_deg": 4.213877201080322,
  "theta_near_flat_abs_max_deg": 15.019281387329102,
  "theta_near_flat_bias_deg": 1.1339691877365112,
  "theta_near_flat_n": 374.0,
  "theta_true_zero_mae_deg": NaN,
  "theta_true_zero_abs_p95_deg": NaN,
  "theta_true_zero_abs_max_deg": NaN,
  "theta_true_zero_bias_deg": NaN,
  "theta_true_zero_n": 0.0,
  "theta_flat_turn_mae_deg": 1.373759388923645,
  "theta_flat_turn_abs_p95_deg": 4.536999702453613,
  "theta_flat_turn_abs_max_deg": 13.103106498718262,
  "theta_flat_turn_bias_deg": 1.0660213232040405,
  "theta_flat_turn_n": 189.0,
  "theta_slope_control_mae_deg": 1.0169280767440796,
  "theta_slope_control_abs_p95_deg": 9.478200912475586,
  "theta_slope_control_abs_max_deg": 15.019281387329102,
  "theta_slope_control_bias_deg": 0.1360403448343277,
  "theta_slope_control_n": 4167.0,
  "theta_all_mae_deg": 1.0169281959533691,
  "theta_all_rmse_deg": 1.5073338747024536,
  "theta_all_p95_abs_err_deg": 3.3230981826782227,
  "theta_all_max_abs_err_deg": 15.519281387329102,
  "theta_all_bias_deg": 0.1360403448343277,
  "theta_all_n": 4167.0,
  "theta_active_abs_ge_2_mae_deg": 0.9625469446182251,
  "theta_active_abs_ge_2_rmse_deg": 1.3397330045700073,
  "theta_active_abs_ge_2_p95_abs_err_deg": 2.9930286407470703,
  "theta_active_abs_ge_2_max_abs_err_deg": 8.475651741027832,
  "theta_active_abs_ge_2_bias_deg": 0.0180054921656847,
  "theta_active_abs_ge_2_n": 3424.0,
  "theta_abs_le_8_mae_deg": 1.0597535371780396,
  "theta_abs_le_8_rmse_deg": 1.563319444656372,
  "theta_abs_le_8_p95_abs_err_deg": 3.373159170150757,
  "theta_abs_le_8_max_abs_err_deg": 15.519281387329102,
  "theta_abs_le_8_bias_deg": 0.1368052363395691,
  "theta_abs_le_8_n": 3369.0,
  "theta_abs_le_10_mae_deg": 1.0169281959533691,
  "theta_abs_le_10_rmse_deg": 1.5073338747024536,
  "theta_abs_le_10_p95_abs_err_deg": 3.3230981826782227,
  "theta_abs_le_10_max_abs_err_deg": 15.519281387329102,
  "theta_abs_le_10_bias_deg": 0.1360403448343277,
  "theta_abs_le_10_n": 4167.0,
  "theta_pos_8_10_mae_deg": 0.7728036642074585,
  "theta_pos_8_10_rmse_deg": 1.0882354974746704,
  "theta_pos_8_10_p95_abs_err_deg": 2.343592882156372,
  "theta_pos_8_10_max_abs_err_deg": 5.529020309448242,
  "theta_pos_8_10_bias_deg": -0.10433918982744217,
  "theta_pos_8_10_n": 399.0,
  "theta_neg_10_8_mae_deg": 0.8994522094726562,
  "theta_neg_10_8_rmse_deg": 1.3814107179641724,
  "theta_neg_10_8_p95_abs_err_deg": 2.962873935699463,
  "theta_neg_10_8_max_abs_err_deg": 7.254898548126221,
  "theta_neg_10_8_bias_deg": 0.36996135115623474,
  "theta_neg_10_8_n": 399.0,
  "theta_pos_6_8_mae_deg": 0.9124329090118408,
  "theta_pos_6_8_rmse_deg": 1.2470930814743042,
  "theta_pos_6_8_p95_abs_err_deg": 2.438340663909912,
  "theta_pos_6_8_max_abs_err_deg": 5.234602451324463,
  "theta_pos_6_8_bias_deg": -0.0768040344119072,
  "theta_pos_6_8_n": 472.0,
  "theta_neg_8_6_mae_deg": 1.0008081197738647,
  "theta_neg_8_6_rmse_deg": 1.3725460767745972,
  "theta_neg_8_6_p95_abs_err_deg": 2.945582866668701,
  "theta_neg_8_6_max_abs_err_deg": 6.435029983520508,
  "theta_neg_8_6_bias_deg": -0.21013496816158295,
  "theta_neg_8_6_n": 437.0,
  "theta_neg_4_2_mae_deg": 0.9346522688865662,
  "theta_neg_4_2_rmse_deg": 1.244888186454773,
  "theta_neg_4_2_p95_abs_err_deg": 2.475304126739502,
  "theta_neg_4_2_max_abs_err_deg": 8.475651741027832,
  "theta_neg_4_2_bias_deg": -0.3888087570667267,
  "theta_neg_4_2_n": 406.0,
  "theta_neg_2_0p5_mae_deg": 0.749087929725647,
  "theta_neg_2_0p5_rmse_deg": 0.9007601141929626,
  "theta_neg_2_0p5_p95_abs_err_deg": 1.6153161525726318,
  "theta_neg_2_0p5_max_abs_err_deg": 3.431262731552124,
  "theta_neg_2_0p5_bias_deg": 0.03563268110156059,
  "theta_neg_2_0p5_n": 202.0,
  "theta_pos_0p5_2_mae_deg": 1.162607192993164,
  "theta_pos_0p5_2_rmse_deg": 1.5398119688034058,
  "theta_pos_0p5_2_p95_abs_err_deg": 2.5479719638824463,
  "theta_pos_0p5_2_max_abs_err_deg": 5.517758369445801,
  "theta_pos_0p5_2_bias_deg": 0.5310330390930176,
  "theta_pos_0p5_2_n": 179.0
}
```
