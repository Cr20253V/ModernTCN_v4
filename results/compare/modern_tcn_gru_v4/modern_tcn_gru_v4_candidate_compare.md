# ModernTCN vs GRU V4 Candidate Compare

- ModernTCN summary: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21_summary.csv`
- GRU per-seed summary: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\GRU_v4_industrial_existing_meta_summary.csv`
- GRU group summary: `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\GRU_v4_industrial_existing_meta_group_summary.csv`

| model | candidate | seed | n | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill | flat->slope | artifact |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ModernTCN | modern_tcn_v4_turn_focus_A_theta_head_B_seed21 | 21 | 1 | 0.9867 | 0.9529 | 0.9819 | 0.7624 | 0.4868 | 0.9876 | 0.9721 | 0.9890 | 0.9944 | 0.9840 | NaN | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx` |
| GRU | inputstats_hidden96 | 101 | 1 | 0.9709 | 0.9447 | 0.9774 | 0.7295 | 0.3278 | 0.9659 | 0.9778 | 0.9778 | 0.9763 | 0.9792 | 0.0288 | `E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_v4_industrial_inputstats_hidden96_seed101.mat` |
| GRU | inputstats_hidden96_5seed_mean | mean | 5 | 0.9684 | 0.9420 | 0.9743 | 0.7295 | 0.3611 | 0.9643 | 0.9768 | 0.9734 | 0.9677 | 0.9786 | 0.0301 | `E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_v4_industrial\GRU_v4_industrial_existing_meta_summary.csv` |

## Reading

- ModernTCN remains the better classifier on this V4 test split, especially main state and turn transition.
- GRU seed101 is the best GRU deployment candidate because it has the best main/turn scores and lowest theta MAE among the five seeds.
- GRU has lower theta MAE than the current ModernTCN deployment candidate, so it is still a useful regression baseline.
