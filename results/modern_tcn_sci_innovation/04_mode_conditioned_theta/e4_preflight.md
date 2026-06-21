# E4 Engineering Preflight

- status: PASS
- scope: E4 / 04_mode_conditioned_theta only; no ONNX; no MATLAB/Simulink.
- base strategy: `small + fixed loss` from frozen baseline.
- model_family: `small_mode_theta`
- formal runs: `flatreg000`, `flatreg001`, `flatreg003`, seed21 only.
- dataset input: `[batch,128,22]`
- feature_contract: `passive17_plus_all5`
- baseline checkpoint: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt`

## Baseline Reference

- acc_main: 0.9669627984453082
- acc_turn: 0.5788450860632982
- acc_turn_transition: 0.4977645305514158
- theta_mae_deg: 0.6793948411941528
- flat_recall: 0.9695767195767195
- stall_recall: 0.71875
- slope_recall: 0.974909090909091
- theta_edge_p95_abs_err: 2.755056858062744
- flat_peak_theta_error: 5.335740089416504

## Baseline E4-Aligned Theta Metrics

```json
{
  "by_true_main": {
    "flat": {
      "label": "flat",
      "n": 756,
      "mae_deg": 0.6804766654968262,
      "p95_abs_err_deg": 1.7982949018478394,
      "bias_deg": -0.47606202960014343
    },
    "stall": {
      "label": "stall",
      "n": 96,
      "mae_deg": 4.951716899871826,
      "p95_abs_err_deg": 7.779551982879639,
      "bias_deg": 4.951716899871826
    },
    "slope": {
      "label": "slope",
      "n": 2750,
      "mae_deg": 0.6790974140167236,
      "p95_abs_err_deg": 1.8383079767227173,
      "bias_deg": -0.19112996757030487
    }
  },
  "by_pred_main": {
    "flat": {
      "label": "flat",
      "n": 807,
      "mae_deg": 0.7682332992553711,
      "p95_abs_err_deg": 1.9465569257736206,
      "bias_deg": -0.42551910877227783
    },
    "stall": {
      "label": "stall",
      "n": 73,
      "mae_deg": 4.691384792327881,
      "p95_abs_err_deg": 7.671703815460205,
      "bias_deg": 4.6120524406433105
    },
    "slope": {
      "label": "slope",
      "n": 2722,
      "mae_deg": 0.6961379647254944,
      "p95_abs_err_deg": 1.8977285623550415,
      "bias_deg": -0.14821141958236694
    }
  },
  "by_theta_bin": {
    "near_zero_abs_le_0p5": {
      "label": "near_zero_abs_le_0p5",
      "n": 278,
      "mae_deg": 0.7597319483757019,
      "p95_abs_err_deg": 1.9942437410354614,
      "bias_deg": -0.5854495763778687
    },
    "small_neg_2_0p5": {
      "label": "small_neg_2_0p5",
      "n": 207,
      "mae_deg": 0.6102249622344971,
      "p95_abs_err_deg": 1.5686184167861938,
      "bias_deg": -0.40880438685417175
    },
    "small_pos_0p5_2": {
      "label": "small_pos_0p5_2",
      "n": 284,
      "mae_deg": 0.8294838666915894,
      "p95_abs_err_deg": 2.05415678024292,
      "bias_deg": -0.18968431651592255
    },
    "mid_neg_8_2": {
      "label": "mid_neg_8_2",
      "n": 1055,
      "mae_deg": 0.8056600093841553,
      "p95_abs_err_deg": 2.101637601852417,
      "bias_deg": -0.17582005262374878
    },
    "mid_pos_2_8": {
      "label": "mid_pos_2_8",
      "n": 1067,
      "mae_deg": 0.7620978355407715,
      "p95_abs_err_deg": 2.3689565658569336,
      "bias_deg": 0.12854918837547302
    },
    "edge_neg_10_8": {
      "label": "edge_neg_10_8",
      "n": 373,
      "mae_deg": 0.7125639915466309,
      "p95_abs_err_deg": 1.600038766860962,
      "bias_deg": 0.07767274975776672
    },
    "edge_pos_8_10": {
      "label": "edge_pos_8_10",
      "n": 338,
      "mae_deg": 1.051216959953308,
      "p95_abs_err_deg": 3.623901128768921,
      "bias_deg": -0.2649156451225281
    }
  },
  "acc_main": 0.9669627984453082,
  "acc_turn": 0.5788450860632982,
  "acc_turn_transition": 0.4977645305514158,
  "theta_mae_deg": 0.6793948411941528,
  "flat_recall": 0.9695767195767195,
  "stall_recall": 0.71875,
  "slope_recall": 0.974909090909091,
  "theta_neg_10_8_p95_abs_err_deg": 1.3394129276275635,
  "theta_pos_8_10_p95_abs_err_deg": 2.7550570964813232,
  "theta_flat_abs_max_deg": 5.335739612579346
}
```
