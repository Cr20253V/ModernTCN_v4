# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73.pt`
- augment npz: ``
- best epoch: 27
- train seconds: 297.3

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
  "lambda_theta": 0.55,
  "lambda_theta_flat": 1.5,
  "lambda_theta_near_flat": 3.0,
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
  "select_theta_flat_p95_weight": 2.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 1.0,
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
| theta_mae_deg | 0.5137 |
| theta_flat_abs_p95_deg | 1.2363 |
| theta_flat_bias_deg | -0.2661 |
| theta_near_flat_abs_p95_deg | 1.4020 |
| theta_near_flat_bias_deg | -0.2281 |
| theta_flat_turn_abs_p95_deg | 0.9531 |
| flat_recall | 0.9867 |
| slope_recall | 0.9776 |
| slope_sign_acc | 0.9980 |

## Validation Best Metrics

```json
{
  "loss_total": 0.11420645911009494,
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
  "theta_mae_rad": 0.009781638160347939,
  "theta_mae_deg": 0.560446560382843,
  "uphill_recall": 0.9840546697038725,
  "downhill_recall": 0.9941972920696325,
  "slope_sign_acc": 0.9992831541218637,
  "theta_flat_mae_deg": 0.5662814378738403,
  "theta_flat_abs_p95_deg": 1.421379566192627,
  "theta_flat_bias_deg": -0.31264516711235046,
  "theta_flat_n": 1757.0,
  "theta_near_flat_mae_deg": 0.5329990983009338,
  "theta_near_flat_abs_p95_deg": 1.4422158002853394,
  "theta_near_flat_bias_deg": -0.29804179072380066,
  "theta_near_flat_n": 1574.0,
  "theta_flat_turn_mae_deg": 0.4016345143318176,
  "theta_flat_turn_abs_p95_deg": 1.1334880590438843,
  "theta_flat_turn_bias_deg": -0.2704263925552368,
  "theta_flat_turn_n": 518.0,
  "theta_slope_control_mae_deg": 0.560446560382843,
  "theta_slope_control_abs_p95_deg": 7.077264785766602,
  "theta_slope_control_bias_deg": -0.2616637051105499,
  "theta_slope_control_n": 1395.0
}
```
