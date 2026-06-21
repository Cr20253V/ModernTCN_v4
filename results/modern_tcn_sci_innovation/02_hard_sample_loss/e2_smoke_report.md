# E2 Smoke Report

- status: PASS
- high_loss_scale_detected: False
- formal_grid: primary_0.2_0.5
- theta_smooth_status: `disabled_contract_limited`

## Loss Scale

| run | base main | base turn | base theta | raw transition | weighted transition | transition/base turn | raw stall | weighted stall | stall/base main | warning |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| smoke_transition_focal | 0.829942 | 0.220348 | 0.022756 | 0.504785 | 0.100957 | 0.458171 | 1.428646 | 0.000000 | 0.000000 | False |
| smoke_stall_focal | 0.880856 | 0.228422 | 0.025589 | 0.576116 | 0.000000 | 0.000000 | 0.607819 | 0.121564 | 0.138006 | False |
| smoke_combo_focal | 0.880753 | 0.221383 | 0.025737 | 0.514246 | 0.102849 | 0.464577 | 0.608458 | 0.121692 | 0.138168 | False |

## Formal Runs Selected

- `fs_t02_s02_sm000_seed21`: transition=0.2, stall=0.2, smooth=0
- `fs_t05_s02_sm000_seed21`: transition=0.5, stall=0.2, smooth=0
- `fs_t02_s05_sm000_seed21`: transition=0.2, stall=0.5, smooth=0
- `fs_t05_s05_sm000_seed21`: transition=0.5, stall=0.5, smooth=0
