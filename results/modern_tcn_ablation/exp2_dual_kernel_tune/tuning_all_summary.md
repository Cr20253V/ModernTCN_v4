# exp2 dual_kernel tuning all-round summary

## Baseline and gate thresholds

- acc_main: baseline `0.9669627984453082`, gate `ge 0.9639627984453082`
- acc_turn: baseline `0.5788450860632982`, gate `ge 0.5738450860632982`
- acc_turn_transition: baseline `0.4977645305514158`, gate `ge 0.4977645305514158`
- theta_mae_deg: baseline `0.6793947815895081`, gate `le 0.6893947815895081`
- slope_recall: baseline `0.974909090909091`, gate `ge 0.9699090909090909`
- flat_recall: baseline `0.9695767195767195`, gate `ge 0.9595767195767195`
- stall_recall: baseline `0.71875`, gate `ge 0.66875`
- theta_edge_p95_abs_err: baseline `2.755056858062744`, gate `le 2.805056858062744`
- false_turn_straight: baseline `0.42369374030005175`, gate `le 0.43369374030005176`
- flat_peak_theta_error: baseline `5.335740089416504`, gate `le 5.585740089416504`

## Ranked candidates

| rank | round | run_tag | status | miss | gap | main | turn | turnT | theta | flat | stall | slope | edge_p95 | false_turn | flat_peak |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | round1 | `tune_r1_scale035_s7_seed21` | FAIL | 5 | 0.598347 | 0.965852 | 0.579400 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 0.980000 | 3.556906 | 0.413864 | 7.179438 |
| 2 | round1 | `tune_r1_theta_s7_seed21` | FAIL | 5 | 0.598347 | 0.965852 | 0.579400 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 0.980000 | 3.556906 | 0.413864 | 7.179438 |
| 3 | round2 | `tune_r2_edgeflat035_s7_seed21` | FAIL | 5 | 0.598347 | 0.965852 | 0.579400 | 0.494784 | 0.665343 | 0.955026 | 0.645833 | 0.980000 | 3.556906 | 0.413864 | 7.179438 |
| 4 | round1 | `tune_r1_s5_bal_seed21` | FAIL | 7 | 0.693310 | 0.963076 | 0.560522 | 0.490313 | 0.823587 | 0.960317 | 0.625000 | 0.975636 | 3.543658 | 0.490429 | 5.583386 |
| 5 | round2 | `tune_r2_mainstall035_s7_seed21` | FAIL | 7 | 1.165085 | 0.964464 | 0.557746 | 0.460507 | 0.828046 | 0.972222 | 0.614583 | 0.974545 | 3.839954 | 0.452147 | 7.644498 |
| 6 | round2 | `tune_r2_zero035_s7_seed21` | FAIL | 7 | 1.244894 | 0.970294 | 0.546641 | 0.482861 | 0.859132 | 0.981481 | 0.625000 | 0.979273 | 3.364393 | 0.541645 | 7.862486 |
| 7 | round1 | `tune_r1_scale025_s7_seed21` | FAIL | 7 | 1.441268 | 0.967518 | 0.556080 | 0.464978 | 0.906892 | 0.984127 | 0.614583 | 0.975273 | 4.843884 | 0.471288 | 6.336631 |
| 8 | round1 | `tune_r1_stall_s7_seed21` | FAIL | 8 | 1.514454 | 0.963631 | 0.548306 | 0.445604 | 0.945203 | 0.969577 | 0.625000 | 0.973818 | 3.504542 | 0.461976 | 9.014004 |
| 9 | round1 | `tune_r1_guard_s7_seed21` | FAIL | 7 | 1.582485 | 0.966408 | 0.567463 | 0.464978 | 0.999980 | 0.977513 | 0.625000 | 0.975273 | 3.880856 | 0.459390 | 8.639937 |
| 10 | round2 | `tune_r2_scale030_s7_seed21` | FAIL | 7 | 1.817661 | 0.966130 | 0.558023 | 0.464978 | 1.087994 | 0.969577 | 0.625000 | 0.977091 | 3.316625 | 0.450595 | 10.385401 |

## Best candidate diagnosis

- best_run: `tune_r1_scale035_s7_seed21`
- gate_status: `FAIL`
- gate_failures: acc_turn_transition 0.494784 >= 0.497765 failed; flat_recall 0.955026 >= 0.959577 failed; stall_recall 0.645833 >= 0.66875 failed; theta_edge_p95_abs_err 3.55691 <= 2.80506 failed; flat_peak_theta_error 7.17944 <= 5.58574 failed

## Decision

- decision: `STOP_NO_MULTISEED`
- reason: no seed21 candidate passed the offline gate; further multi-seed training would test instability rather than validate a candidate.
