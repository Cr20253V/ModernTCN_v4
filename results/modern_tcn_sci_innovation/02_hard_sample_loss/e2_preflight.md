# E2 Engineering Preflight

- status: PASS
- scope: E2 / 02_hard_sample_loss only; no ONNX; no MATLAB/Simulink.
- method label: hard-sample focal only
- theta_smooth_status: `disabled_contract_limited`
- dataset input: `[batch,128,22]`
- feature_contract: `passive17_plus_all5`
- compare note: old compare directory exists but is not touched
- zero_loss_equivalence_verified: True
- no_overwrite_guard_verified: True

## Baseline Reference

- source: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101_summary.csv`
- acc_main: 0.9669627984453082
- acc_turn: 0.5788450860632982
- acc_turn_transition: 0.4977645305514158
- theta_mae_deg: 0.6793947815895081
- flat_recall: 0.9695767195767195
- stall_recall: 0.71875
- slope_recall: 0.974909090909091
- theta_edge_p95_abs_err: 2.755056858062744
- flat_peak_theta_error: 5.335740089416504

## Theta Smoothness Audit

```json
{
  "train": {
    "n_windows": 16529,
    "unique_runs": 71,
    "contiguous_segments": 16115,
    "run_reappears": true
  },
  "val": {
    "n_windows": 3695,
    "unique_runs": 15,
    "contiguous_segments": 3242,
    "run_reappears": true
  },
  "test": {
    "n_windows": 3602,
    "unique_runs": 16,
    "contiguous_segments": 3174,
    "run_reappears": true
  },
  "theta_smooth_status": "disabled_contract_limited",
  "reason": "run_id exists, but windows are not ordered as contiguous same-run sequences and no window/order index is available"
}
```

## Planned Formal Runs

- `fs_t02_s02_sm000_seed21`: lambda_transition=0.2, lambda_stall=0.2, lambda_smooth=0
- `fs_t05_s02_sm000_seed21`: lambda_transition=0.5, lambda_stall=0.2, lambda_smooth=0
- `fs_t02_s05_sm000_seed21`: lambda_transition=0.2, lambda_stall=0.5, lambda_smooth=0
- `fs_t05_s05_sm000_seed21`: lambda_transition=0.5, lambda_stall=0.5, lambda_smooth=0

## Smoke Loss Scale

| run | transition/base_turn | stall/base_main | warning |
|---|---:|---:|---|
| smoke_transition_focal | 0.458171 | 0.000000 | False |
| smoke_stall_focal | 0.000000 | 0.138006 | False |
| smoke_combo_focal | 0.464577 | 0.138168 | False |
