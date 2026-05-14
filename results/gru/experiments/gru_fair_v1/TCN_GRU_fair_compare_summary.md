# TCN vs GRU 公平对照表

- TCN 行使用当前交接文档记录的临时最优候选，不代表论文最终结果。
- GRU 行使用本次流水线 production_score 排序后的最佳候选。

| model | case | seed | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill | model file |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| TCN | staged_bestbase_inputstats_turn_lam050 | NaN | 0.9303 | 0.8989 | 0.9257 | 0.6341 | 0.7380 | 0.9585 | 0.7778 | 0.9012 | 0.9173 | 0.8276 | `data/models/TCN_model_staged_bestbase_v1_staged_bestbase_inputstats_turn_lam050.mat` |
| GRU | h96_l2_turn0p05_last_mean_inputstats | NaN | 0.9483 | 0.8831 | 0.9134 | 0.5854 | 0.4156 | 0.9623 | 0.6667 | 0.9568 | 0.9774 | 0.8621 | `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_fair_v1_h96_l2_turn0p05_last_mean_inputstats.mat` |
