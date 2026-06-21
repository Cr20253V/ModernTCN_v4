# exp2 dual_kernel tuning round1 summary

## Baseline

- acc_main: `0.9669627984453082`
- acc_turn: `0.5788450860632982`
- acc_turn_transition: `0.4977645305514158`
- theta_mae_deg: `0.6793947815895081`
- flat_recall: `0.9695767195767195`
- stall_recall: `0.71875`
- slope_recall: `0.974909090909091`
- theta_edge_p95_abs_err: `2.755056858062744`
- false_turn_straight: `0.42369374030005175`
- flat_peak_theta_error: `5.335740089416504`

## Ranked candidates

| rank | run_tag | status | miss | gap | main | turnT | theta | flat | stall | slope | edge_p95 | false_turn | flat_peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `tune_r1_scale035_s7_seed21` | FAIL | 5 | 0.598347 | 0.965852 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 0.980000 | 3.556906 | 0.413864 | 7.179438 |
| 2 | `tune_r1_theta_s7_seed21` | FAIL | 5 | 0.598347 | 0.965852 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 0.980000 | 3.556906 | 0.413864 | 7.179438 |
| 3 | `tune_r1_s5_bal_seed21` | FAIL | 7 | 0.693310 | 0.963076 | 0.490313 | 0.823587 | 0.960317 | 0.625000 | 0.975636 | 3.543658 | 0.490429 | 5.583386 |
| 4 | `tune_r1_scale025_s7_seed21` | FAIL | 7 | 1.441268 | 0.967518 | 0.464978 | 0.906892 | 0.984127 | 0.614583 | 0.975273 | 4.843884 | 0.471288 | 6.336631 |
| 5 | `tune_r1_stall_s7_seed21` | FAIL | 8 | 1.514454 | 0.963631 | 0.445604 | 0.945203 | 0.969577 | 0.625000 | 0.973818 | 3.504542 | 0.461976 | 9.014004 |
| 6 | `tune_r1_guard_s7_seed21` | FAIL | 7 | 1.582485 | 0.966408 | 0.464978 | 0.999980 | 0.977513 | 0.625000 | 0.975273 | 3.880856 | 0.459390 | 8.639937 |

## Gate failures

- `tune_r1_scale035_s7_seed21`: acc_turn_transition 0.494784 >= 0.497765 failed; flat_recall 0.955026 >= 0.959577 failed; stall_recall 0.645833 >= 0.66875 failed; theta_edge_p95_abs_err 3.55691 <= 2.80506 failed; flat_peak_theta_error 7.17944 <= 5.58574 failed
- `tune_r1_theta_s7_seed21`: acc_turn_transition 0.494784 >= 0.497765 failed; flat_recall 0.955026 >= 0.959577 failed; stall_recall 0.645833 >= 0.66875 failed; theta_edge_p95_abs_err 3.55691 <= 2.80506 failed; flat_peak_theta_error 7.17944 <= 5.58574 failed
- `tune_r1_s5_bal_seed21`: acc_main 0.963076 >= 0.963963 failed; acc_turn 0.560522 >= 0.573845 failed; acc_turn_transition 0.490313 >= 0.497765 failed; theta_mae_deg 0.823587 <= 0.689395 failed; stall_recall 0.625 >= 0.66875 failed; theta_edge_p95_abs_err 3.54366 <= 2.80506 failed; false_turn_straight 0.490429 <= 0.433694 failed
- `tune_r1_scale025_s7_seed21`: acc_turn 0.55608 >= 0.573845 failed; acc_turn_transition 0.464978 >= 0.497765 failed; theta_mae_deg 0.906892 <= 0.689395 failed; stall_recall 0.614583 >= 0.66875 failed; theta_edge_p95_abs_err 4.84388 <= 2.80506 failed; false_turn_straight 0.471288 <= 0.433694 failed; flat_peak_theta_error 6.33663 <= 5.58574 failed
- `tune_r1_stall_s7_seed21`: acc_main 0.963631 >= 0.963963 failed; acc_turn 0.548306 >= 0.573845 failed; acc_turn_transition 0.445604 >= 0.497765 failed; theta_mae_deg 0.945203 <= 0.689395 failed; stall_recall 0.625 >= 0.66875 failed; theta_edge_p95_abs_err 3.50454 <= 2.80506 failed; false_turn_straight 0.461976 <= 0.433694 failed; flat_peak_theta_error 9.014 <= 5.58574 failed
- `tune_r1_guard_s7_seed21`: acc_turn 0.567463 >= 0.573845 failed; acc_turn_transition 0.464978 >= 0.497765 failed; theta_mae_deg 0.99998 <= 0.689395 failed; stall_recall 0.625 >= 0.66875 failed; theta_edge_p95_abs_err 3.88086 <= 2.80506 failed; false_turn_straight 0.45939 <= 0.433694 failed; flat_peak_theta_error 8.63994 <= 5.58574 failed
