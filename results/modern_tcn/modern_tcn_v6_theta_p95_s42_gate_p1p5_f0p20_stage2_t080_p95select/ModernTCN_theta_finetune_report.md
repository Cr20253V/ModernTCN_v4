# ModernTCN theta-head fine-tune report

- base checkpoint: `results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_tail_neg120_uf\modern_tcn_seed42.pt`
- augment npz: ``
- best epoch: 37
- train seconds: 110.9

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
  "turn_head_source": "full",
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
  "lambda_turn": 0.05,
  "lambda_theta": 1.0,
  "lambda_theta_flat": 2.0,
  "lambda_theta_near_flat": 8.0,
  "theta_near_flat_deg": 0.5,
  "lambda_theta_error_excess": 40.0,
  "lambda_theta_flat_excess": 260.0,
  "lambda_theta_near_flat_excess": 320.0,
  "lambda_theta_true_zero_excess": 380.0,
  "lambda_theta_active_excess": 90.0,
  "lambda_theta_small_neg": 18.0,
  "lambda_theta_small_neg_excess": 180.0,
  "theta_excess_target_deg": 0.8,
  "theta_flat_excess_target_deg": 0.35,
  "theta_true_zero_tol_deg": 0.0001,
  "theta_small_neg_min_deg": -4.0,
  "theta_small_neg_max_deg": -2.0,
  "theta_gate_mode": "main_slope_prob",
  "theta_gate_power": 1.5,
  "theta_gate_floor": 0.2,
  "main_class_multipliers": [
    1.2,
    1.0,
    0.95
  ],
  "turn_class_multipliers": [
    1.0,
    1.0,
    1.0
  ],
  "main_class_weight_method": "sqrt_inverse",
  "turn_class_weight_method": "sqrt_inverse",
  "main_neg_slope_weight": 2.0,
  "main_pos_slope_weight": 1.0,
  "theta_neg_weight": 1.8,
  "theta_pos_weight": 1.2,
  "turn_transition_weight": 1.0,
  "select_turn_weight": 0.3,
  "select_turn_transition_weight": 1.0,
  "select_turn_transition_target": 0.75,
  "select_turn_left_weight": 0.0,
  "select_turn_left_target": 0.8,
  "select_theta_weight": 0.1,
  "select_theta_ref_deg": 1.0,
  "select_theta_p95_weight": 80.0,
  "select_theta_p95_target_deg": 1.0,
  "select_theta_flat_p95_weight": 20.0,
  "select_theta_flat_p95_target_deg": 1.0,
  "select_theta_near_flat_p95_weight": 20.0,
  "select_theta_near_flat_p95_target_deg": 1.0,
  "select_theta_true_zero_p95_weight": 20.0,
  "select_theta_true_zero_p95_target_deg": 1.0,
  "select_theta_flat_peak_weight": 3.0,
  "select_theta_flat_peak_target_deg": 3.0,
  "select_theta_small_neg_p95_weight": 2.0,
  "select_theta_small_neg_p95_target_deg": 1.0,
  "select_theta_flat_bias_weight": 0.5,
  "select_theta_flat_bias_target_deg": 0.2
}
```

## Test Metrics

| metric | value |
|---|---:|
| acc_main | 0.9773 |
| acc_turn | 0.9387 |
| acc_turn_transition | 0.6667 |
| turn_left_recall | 0.8760 |
| theta_mae_deg | 0.2440 |
| theta_abs_le_8_mae_deg | 0.2440 |
| theta_abs_le_8_p95_abs_err_deg | 0.9925 |
| theta_abs_le_8_max_abs_err_deg | 4.5364 |
| theta_abs_le_10_mae_deg | 0.2440 |
| theta_abs_le_10_p95_abs_err_deg | 0.9925 |
| theta_pos_6_8_mae_deg | 0.3376 |
| theta_pos_6_8_p95_abs_err_deg | 1.1750 |
| theta_pos_6_8_bias_deg | -0.1030 |
| theta_neg_8_6_mae_deg | 0.2768 |
| theta_neg_8_6_p95_abs_err_deg | 0.6796 |
| theta_neg_8_6_bias_deg | -0.0891 |
| theta_active_abs_ge_2_mae_deg | 0.4366 |
| theta_active_abs_ge_2_p95_abs_err_deg | 2.3568 |
| theta_neg_4_2_mae_deg | 1.2241 |
| theta_neg_4_2_p95_abs_err_deg | 3.7753 |
| theta_neg_4_2_bias_deg | 0.9395 |
| theta_flat_abs_p95_deg | 0.3982 |
| theta_flat_abs_max_deg | 2.6375 |
| theta_flat_bias_deg | -0.0517 |
| theta_near_flat_abs_p95_deg | 0.3853 |
| theta_near_flat_abs_max_deg | 2.6375 |
| theta_near_flat_bias_deg | -0.0439 |
| theta_true_zero_abs_p95_deg | 0.3889 |
| theta_true_zero_abs_max_deg | 2.6375 |
| theta_true_zero_bias_deg | -0.0434 |
| theta_flat_turn_abs_p95_deg | 0.3009 |
| flat_recall | 0.9947 |
| slope_recall | 0.9416 |
| slope_sign_acc | 0.3304 |

## Validation Best Metrics

```json
{
  "loss_total": 0.6751704314239587,
  "acc_main": 0.9732052578361982,
  "acc_turn": 0.9332659251769464,
  "acc_turn_pure": 0.9491434689507494,
  "acc_turn_transition": 0.6636363636363637,
  "flat_recall": 0.9938608458390177,
  "stall_recall": 0.8787878787878788,
  "slope_recall": 0.9192825112107623,
  "recall_main": [
    0.9938608458390177,
    0.8787878787878788,
    0.9192825112107623
  ],
  "turn_right_recall": 0.9036827195467422,
  "turn_straight_recall": 0.9571550985432733,
  "turn_left_recall": 0.8951965065502183,
  "recall_turn": [
    0.9036827195467422,
    0.9571550985432733,
    0.8951965065502183
  ],
  "cm_turn": [
    [
      319,
      24,
      10
    ],
    [
      32,
      1117,
      18
    ],
    [
      1,
      47,
      410
    ]
  ],
  "n_turn_transition": 110,
  "n_turn_pure": 1868,
  "cm_main": [
    [
      1457,
      3,
      6
    ],
    [
      5,
      58,
      3
    ],
    [
      35,
      1,
      410
    ]
  ],
  "main_confidence_mean": 0.9980621684668882,
  "main_confidence_error_mean": 0.9664685374827553,
  "main_low_conf_0p60_ratio": 0.0,
  "main_low_conf_0p70_ratio": 0.0005055611729019212,
  "main_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 0,
      "error_rate": NaN,
      "mean_confidence": NaN
    },
    {
      "bin": "[0.60,0.70)",
      "n": 1,
      "error_rate": 1.0,
      "mean_confidence": 0.6431820967985341
    },
    {
      "bin": "[0.70,0.80)",
      "n": 7,
      "error_rate": 0.42857142857142855,
      "mean_confidence": 0.7424038129983555
    },
    {
      "bin": "[0.80,0.90)",
      "n": 6,
      "error_rate": 0.5,
      "mean_confidence": 0.86258492446572
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1964,
      "error_rate": 0.023421588594704685,
      "mean_confidence": 0.9995679485198186
    }
  ],
  "turn_confidence_mean": 0.9570422954244866,
  "turn_confidence_error_mean": 0.8497580184476624,
  "turn_low_conf_0p60_ratio": 0.01870576339737108,
  "turn_low_conf_0p70_ratio": 0.04398382204246714,
  "turn_confidence_bins": [
    {
      "bin": "[0.00,0.60)",
      "n": 37,
      "error_rate": 0.35135135135135137,
      "mean_confidence": 0.5458349192675257
    },
    {
      "bin": "[0.60,0.70)",
      "n": 50,
      "error_rate": 0.36,
      "mean_confidence": 0.657250211734435
    },
    {
      "bin": "[0.70,0.80)",
      "n": 59,
      "error_rate": 0.2033898305084746,
      "mean_confidence": 0.7563471172100384
    },
    {
      "bin": "[0.80,0.90)",
      "n": 124,
      "error_rate": 0.1532258064516129,
      "mean_confidence": 0.8543159737387546
    },
    {
      "bin": "[0.90,1.00)",
      "n": 1708,
      "error_rate": 0.040983606557377046,
      "mean_confidence": 0.9891168601235458
    }
  ],
  "theta_mae_rad": 0.004412941634654999,
  "theta_mae_deg": 0.25284290313720703,
  "uphill_recall": 0.8464163822525598,
  "downhill_recall": 0.6864406779661016,
  "slope_sign_acc": 0.25993723849372385,
  "theta_flat_mae_deg": 0.15470685064792633,
  "theta_flat_abs_p95_deg": 0.3746573328971863,
  "theta_flat_abs_max_deg": 3.9871580600738525,
  "theta_flat_bias_deg": -0.06586059927940369,
  "theta_flat_n": 1466.0,
  "theta_near_flat_mae_deg": 0.13781781494617462,
  "theta_near_flat_abs_p95_deg": 0.3939310312271118,
  "theta_near_flat_abs_max_deg": 4.533351898193359,
  "theta_near_flat_bias_deg": -0.0599588043987751,
  "theta_near_flat_n": 1472.0,
  "theta_true_zero_mae_deg": 0.13558036088943481,
  "theta_true_zero_abs_p95_deg": 0.391534686088562,
  "theta_true_zero_abs_max_deg": 4.533351898193359,
  "theta_true_zero_bias_deg": -0.05761800706386566,
  "theta_true_zero_n": 1433.0,
  "theta_flat_turn_mae_deg": 0.11056257039308548,
  "theta_flat_turn_abs_p95_deg": 0.31741100549697876,
  "theta_flat_turn_abs_max_deg": 0.9723886847496033,
  "theta_flat_turn_bias_deg": -0.06670243293046951,
  "theta_flat_turn_n": 463.0,
  "theta_slope_control_mae_deg": 0.25284290313720703,
  "theta_slope_control_abs_p95_deg": 5.714850902557373,
  "theta_slope_control_abs_max_deg": 7.233187198638916,
  "theta_slope_control_bias_deg": -0.010623980313539505,
  "theta_slope_control_n": 1912.0,
  "theta_all_mae_deg": 0.2528429329395294,
  "theta_all_rmse_deg": 0.5805630087852478,
  "theta_all_p95_abs_err_deg": 0.9106712937355042,
  "theta_all_max_abs_err_deg": 4.295966148376465,
  "theta_all_bias_deg": -0.010623977519571781,
  "theta_all_n": 1912.0,
  "theta_active_abs_ge_2_mae_deg": 0.5754157900810242,
  "theta_active_abs_ge_2_rmse_deg": 1.0502040386199951,
  "theta_active_abs_ge_2_p95_abs_err_deg": 3.010718822479248,
  "theta_active_abs_ge_2_max_abs_err_deg": 4.295966148376465,
  "theta_active_abs_ge_2_bias_deg": 0.17093853652477264,
  "theta_active_abs_ge_2_n": 446.0,
  "theta_abs_le_8_mae_deg": 0.2528429329395294,
  "theta_abs_le_8_rmse_deg": 0.5805630087852478,
  "theta_abs_le_8_p95_abs_err_deg": 0.9106712937355042,
  "theta_abs_le_8_max_abs_err_deg": 4.295966148376465,
  "theta_abs_le_8_bias_deg": -0.010623977519571781,
  "theta_abs_le_8_n": 1912.0,
  "theta_abs_le_10_mae_deg": 0.2528429329395294,
  "theta_abs_le_10_rmse_deg": 0.5805630087852478,
  "theta_abs_le_10_p95_abs_err_deg": 0.9106712937355042,
  "theta_abs_le_10_max_abs_err_deg": 4.295966148376465,
  "theta_abs_le_10_bias_deg": -0.010623977519571781,
  "theta_abs_le_10_n": 1912.0,
  "theta_pos_6_8_mae_deg": 0.5022589564323425,
  "theta_pos_6_8_rmse_deg": 0.6294741034507751,
  "theta_pos_6_8_p95_abs_err_deg": 0.9467576742172241,
  "theta_pos_6_8_max_abs_err_deg": 2.1621146202087402,
  "theta_pos_6_8_bias_deg": -0.42280104756355286,
  "theta_pos_6_8_n": 50.0,
  "theta_neg_8_6_mae_deg": 0.27922123670578003,
  "theta_neg_8_6_rmse_deg": 0.3326435685157776,
  "theta_neg_8_6_p95_abs_err_deg": 0.6582224369049072,
  "theta_neg_8_6_max_abs_err_deg": 0.8014402389526367,
  "theta_neg_8_6_bias_deg": -0.14606665074825287,
  "theta_neg_8_6_n": 47.0,
  "theta_neg_4_2_mae_deg": 0.9561603665351868,
  "theta_neg_4_2_rmse_deg": 1.6565791368484497,
  "theta_neg_4_2_p95_abs_err_deg": 3.5742876529693604,
  "theta_neg_4_2_max_abs_err_deg": 4.295966148376465,
  "theta_neg_4_2_bias_deg": 0.7340680360794067,
  "theta_neg_4_2_n": 145.0
}
```
