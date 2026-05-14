# TCN / GRU / PG-TCN 当前消融汇总

- CSV: `E:\Matlab\Simulink\S-Function_16\results\tcn\experiments\ablation_summary_current\TCN_GRU_PG_ablation_summary.csv`
- 结论: 当前主线保留 staged TCN；GRU 作为公平对照；PG-TCN 作为消融实验，不作为主线模型。

| model | role | case | type | seed | n | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill | decision |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| TCN | main | staged_bestbase_inputstats_turn_lam050 | frozen_single | NaN | 1 | 0.9303 | 0.8989 | 0.9257 | 0.6341 | 0.7380 | 0.9585 | 0.7778 | 0.9012 | 0.9173 | 0.8276 | mainline temporary best |
| GRU | fair_baseline | h96_l2_turn0p05_last_mean_inputstats | grid_best_single | NaN | 1 | 0.9483 | 0.8831 | 0.9134 | 0.5854 | 0.4156 | 0.9623 | 0.6667 | 0.9568 | 0.9774 | 0.8621 | GRU temporary best |
| PG-TCN | ablation | best_single_phy0p005 | single | 21 | 1 | 0.9281 | 0.8787 | 0.9059 | 0.6098 | 0.9926 | 0.9547 | 0.7778 | 0.9012 | 0.9173 | 0.8276 | ablation only |
| PG-TCN | ablation | mean_phy0p005_seed5 | mean | NaN | 5 | 0.9043 | 0.8876 | 0.9163 | 0.6049 | 1.3224 | 0.9298 | 0.7778 | 0.8765 | 0.8842 | 0.8414 | ablation only; not mainline |
| TCN-control | ablation | mean_phy0_seed5 | mean | NaN | 5 | 0.9231 | 0.8858 | 0.9144 | 0.6049 | 1.1271 | 0.9479 | 0.7556 | 0.9012 | 0.9158 | 0.8345 | ablation only; not mainline |
