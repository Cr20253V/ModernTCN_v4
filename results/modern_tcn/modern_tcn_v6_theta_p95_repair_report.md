# ModernTCN V6 Theta P95 Repair Report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- hard target: total/near-flat/true-zero P95 <= `1.0 deg`

## GRU Baseline

| seed | main | turn | turnT | theta MAE | slope | uphill | downhill |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 73 | 0.9366 | 0.9096 | 0.5484 | 0.5556 | 0.9096 | 0.8099 | 0.7880 |

## Candidates

| pass | run_tag | score | main | turn | turnT | theta MAE | P95 | active P95 | neg4_2 MAE | neg4_2 P95 | flat P95 | near P95 | zero P95 | flat peak | slope | checkpoint |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | modern_tcn_v6_theta_p95_s42_tail_flat220_neg80_nogate_uf | 9.4927 | 0.9783 | 0.9382 | 0.6667 | 0.4524 | 1.9220 | 1.8312 | 1.0895 | 3.5870 | 1.9039 | 2.0872 | 2.1368 | 8.3808 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_tail_flat220_neg80_nogate_uf\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_gate_p1p0_f0p10_tail_neg80_uf | 5.3985 | 0.9783 | 0.9387 | 0.6667 | 0.3557 | 1.2881 | 2.3866 | 1.5154 | 3.4975 | 0.6979 | 0.7033 | 0.7098 | 1.7190 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p0_f0p10_tail_neg80_uf\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_gate_p0p25_f0p10_tail_neg80_uf | 5.0687 | 0.9773 | 0.9397 | 0.6882 | 0.2965 | 1.3244 | 2.5747 | 1.3154 | 3.6087 | 0.4347 | 0.4263 | 0.4268 | 1.8632 | 0.9416 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p0p25_f0p10_tail_neg80_uf\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_tail_neg120_uf | 5.0824 | 0.9778 | 0.9392 | 0.6667 | 0.3153 | 1.1843 | 2.3069 | 1.4185 | 3.6282 | 0.4667 | 0.4667 | 0.4797 | 2.5202 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p20_tail_neg120_uf\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_headonly_gate_p1p0_f0p15_tail | 6.6444 | 0.9783 | 0.9408 | 0.6989 | 0.5209 | 1.6448 | 3.3149 | 1.9142 | 4.2073 | 0.5245 | 0.5295 | 0.5358 | 3.6878 | 0.9473 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_headonly_gate_p1p0_f0p15_tail\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p35_neg200_mainhead | 6.7147 | 0.9773 | 0.9392 | 0.6774 | 0.3749 | 1.4599 | 2.0182 | 1.2447 | 3.7195 | 0.9658 | 0.9784 | 1.0466 | 5.1286 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p5_f0p35_neg200_mainhead\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_p95_s42_gate_p1p0_f0p35_neg200_mainhead | 6.2333 | 0.9773 | 0.9376 | 0.6667 | 0.4404 | 1.4058 | 2.1381 | 1.2558 | 3.0954 | 1.1223 | 1.1339 | 1.1355 | 2.8551 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_p95_s42_gate_p1p0_f0p35_neg200_mainhead\modern_tcn_seed42.pt` |

## Selected

- `modern_tcn_v6_theta_p95_s42_gate_p0p25_f0p10_tail_neg80_uf` score `5.0687`, P95 `1.3244 deg`, zero P95 `0.4268 deg`.
