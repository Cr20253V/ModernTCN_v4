# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\transition_rich_v3_theta_head_D_online_aug_seed73\modern_tcn_seed73.pt`
- augment npz: `data\tcn\ModernTCN_theta_online_aug_industrial_lite_v2_seed73.npz`
- best epoch: 37
- train seconds: 395.8

## Config

```json
{
  "input_dim": 19,
  "seq_len": 128,
  "channels": 64,
  "blocks": 5,
  "kernel_size": 31,
  "dropout": 0.15,
  "expansion": 2,
  "readout_input_stats": true,
  "turn_head_source": "kinematic_stats",
  "turn_feature_indices": [
    1,
    4,
    5,
    6,
    7,
    9,
    10,
    11,
    16
  ],
  "lambda_turn": 0.1,
  "lambda_theta": 1.0,
  "lambda_theta_flat": 8.0,
  "lambda_theta_near_flat": 16.0,
  "theta_near_flat_deg": 0.5,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.2,
    0.8,
    1.2
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 2.0,
  "theta_pos_weight": 1.0,
  "turn_transition_weight": 1.5,
  "select_turn_weight": 0.5,
  "select_turn_transition_weight": 1.5,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 1.0,
  "select_turn_left_target": 0.85,
  "select_theta_flat_p95_weight": 6.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 2.0,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9752 |
| acc_turn | 0.7894 |
| acc_turn_transition | 0.5944 |
| turn_left_recall | 0.9596 |
| theta_mae_deg | 0.7192 |
| theta_flat_abs_p95_deg | 0.9692 |
| theta_flat_bias_deg | 0.0078 |
| theta_near_flat_abs_p95_deg | 0.9692 |
| theta_near_flat_bias_deg | 0.0291 |
| theta_flat_turn_abs_p95_deg | 0.6469 |
| flat_recall | 0.9867 |
| slope_recall | 0.9776 |
| slope_sign_acc | 1.0000 |

## Validation Best Metrics

```json
{
  "loss_total": 0.11481795700074494,
  "acc_main": 0.9836544074722708,
  "acc_turn": 0.819614711033275,
  "acc_turn_pure": 0.8491600959890299,
  "acc_turn_transition": 0.650294695481336,
  "flat_recall": 0.983494593056346,
  "stall_recall": 0.9635036496350365,
  "slope_recall": 0.9878136200716846,
  "recall_main": [
    0.983494593056346,
    0.9635036496350365,
    0.9878136200716846
  ],
  "turn_right_recall": 0.8610271903323263,
  "turn_straight_recall": 0.7482758620689656,
  "turn_left_recall": 0.9795640326975477,
  "recall_turn": [
    0.8610271903323263,
    0.7482758620689656,
    0.9795640326975477
  ],
  "cm_turn": [
    [
      570,
      69,
      23
    ],
    [
      230,
      1519,
      281
    ],
    [
      0,
      15,
      719
    ]
  ],
  "n_turn_transition": 509,
  "n_turn_pure": 2917,
  "cm_main": [
    [
      1728,
      5,
      24
    ],
    [
      8,
      264,
      2
    ],
    [
      10,
      7,
      1378
    ]
  ],
  "theta_mae_rad": 0.012977580539882183,
  "theta_mae_deg": 0.7435605525970459,
  "uphill_recall": 0.9840546697038725,
  "downhill_recall": 0.9941972920696325,
  "slope_sign_acc": 0.9992831541218637,
  "theta_flat_mae_deg": 0.3557378649711609,
  "theta_flat_abs_p95_deg": 1.1291614770889282,
  "theta_flat_bias_deg": 0.06979215890169144,
  "theta_flat_n": 1757.0,
  "theta_near_flat_mae_deg": 0.2716495990753174,
  "theta_near_flat_abs_p95_deg": 1.1058756113052368,
  "theta_near_flat_bias_deg": 0.06402169167995453,
  "theta_near_flat_n": 1574.0,
  "theta_flat_turn_mae_deg": 0.2207704484462738,
  "theta_flat_turn_abs_p95_deg": 0.7656033039093018,
  "theta_flat_turn_bias_deg": 0.002774427877739072,
  "theta_flat_turn_n": 518.0,
  "theta_slope_control_mae_deg": 0.7435605525970459,
  "theta_slope_control_abs_p95_deg": 6.432328701019287,
  "theta_slope_control_bias_deg": -0.0719335675239563,
  "theta_slope_control_n": 1395.0
}
```
