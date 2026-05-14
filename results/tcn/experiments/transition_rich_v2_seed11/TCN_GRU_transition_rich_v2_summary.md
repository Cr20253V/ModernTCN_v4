# TCN/GRU Transition-Rich v2 Baseline

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- csv: `E:\Matlab\Simulink\S-Function_16\results\tcn\experiments\transition_rich_v2_seed11\TCN_GRU_transition_rich_v2_summary.csv`

| model | seed | epoch | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| TCN | 11 | 78 | 0.8554 | 0.9143 | 0.9374 | 0.7521 | 0.4277 | 0.9337 | 1.0000 | 0.6782 | 0.5785 | 0.9149 |
| GRU | 11 | 35 | 0.9349 | 0.8781 | 0.9185 | 0.5950 | 0.4407 | 0.9354 | 0.9744 | 0.9243 | 0.9103 | 0.9574 |
