# Seed Failure Diagnosis

## Seed-level summary

| seed | failure_type | closed_loop_transfer_risk | offline_v2_score | acc_main | stall_recall | slope_recall | theta_edge_p95_abs_err | flat_peak_theta_error | J_control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 21 | edge_and_flat_drift | high | 1.09351261643159 | 0.960022209883398 | 0.6875 | 0.976727272727273 | 2.43688559532166 | 7.10931348800659 | 1.14311774157566 |
| 42 | edge_and_flat_drift | high | 1.07901896581399 | 0.967240421987785 | 0.697916666666667 | 0.984 | 3.42140817642212 | 5.89323759078979 | 1.17496689656309 |
| 101 | success_pattern_seed101 | moderate | 0.970838817749306 | 0.967518045530261 | 0.697916666666667 | 0.979272727272727 | 2.27067041397095 | 5.24426937103271 | 0.94411711953914 |

## Classification

- failure_type_seed21: `edge_and_flat_drift`
- failure_type_seed42: `edge_and_flat_drift`
- success_pattern_seed101: `success_pattern_seed101`
- closed_loop_transfer_risk: `high`
