# Closed-Loop Robustness Benchmark

- timestamp: `2026-05-15 16:38:41`
- output root: `E:\Matlab\Simulink\S-Function_16\results\compare\robustness_closed_loop`
- controllers: `ModernTCN, GRU, TCN`
- disturbance levels: `[0 1 2]`

## Aggregate By Disturbance

| d | controller | cases | rank mean | worst rank | ey rmse | xy rmse | j_du | viol | main acc | turn acc |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | ModernTCN | 2 | 1.000 | 1 | 0.035547 | 0.33155 | 19.67 | 0 | 94.568 | 78.235 |
| 0 | GRU | 2 | 2.000 | 2 | 0.041256 | 0.57156 | 1.5143 | 0 | 89.053 | 69.129 |
| 0 | TCN | 2 | 3.000 | 3 | 0.055196 | 0.92733 | 353.04 | 0 | 73.549 | 77.220 |
| 1 | ModernTCN | 2 | 1.000 | 1 | 0.061824 | 1.288 | 205.78 | 0 | 84.975 | 71.221 |
| 1 | GRU | 2 | 2.500 | 3 | 0.076476 | 1.3874 | 307.31 | 0 | 89.673 | 51.411 |
| 1 | TCN | 2 | 2.500 | 3 | 0.068626 | 1.4244 | 669.08 | 0 | 43.461 | 63.497 |
| 2 | ModernTCN | 2 | 1.000 | 1 | 0.081916 | 1.6587 | 709.76 | 0 | 82.777 | 70.645 |
| 2 | GRU | 2 | 2.000 | 2 | 0.11699 | 1.8842 | 292.18 | 0 | 90.121 | 50.970 |
| 2 | TCN | 2 | 3.000 | 3 | 0.09565 | 1.8597 | 1101.8 | 0 | 34.236 | 64.094 |

## ModernTCN Check

- ModernTCN better than both GRU and TCN by per-case overall rank: `6/6` cases.
