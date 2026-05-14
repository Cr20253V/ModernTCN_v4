# TCN/GRU Transition-Rich v2 Baseline

- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\TCN_dataset_v2_transition_rich.mat`
- csv: `E:\Matlab\Simulink\S-Function_16\results\tcn\experiments\transition_rich_v2_seed101\TCN_GRU_transition_rich_v2_summary.csv`

| model | seed | epoch | main | turn | turn pure | turn trans | theta deg | flat | stall | slope | uphill | downhill |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| TCN | 101 | 71 | 0.9008 | 0.9019 | 0.9244 | 0.7438 | 0.6148 | 0.9529 | 1.0000 | 0.7823 | 0.7265 | 0.9149 |
| GRU | 101 | 49 | 0.9442 | 0.8915 | 0.9197 | 0.6942 | 0.3296 | 0.9459 | 0.9872 | 0.9306 | 0.9193 | 0.9574 |
