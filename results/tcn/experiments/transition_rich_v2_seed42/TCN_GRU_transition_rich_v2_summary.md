# TCN/GRU Transition-Rich v2 Baseline

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- csv: `E:\Matlab\Simulink\S-Function_16\results\tcn\experiments\transition_rich_v2_seed42\TCN_GRU_transition_rich_v2_summary.csv`

| model | seed | epoch | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| TCN | 42 | 75 | 0.9380 | 0.8946 | 0.9197 | 0.7190 | 0.4861 | 0.9616 | 1.0000 | 0.8801 | 0.8520 | 0.9468 |
| GRU | 42 | 21 | 0.9277 | 0.8812 | 0.9091 | 0.6860 | 0.4687 | 0.9337 | 1.0000 | 0.8991 | 0.8744 | 0.9574 |
