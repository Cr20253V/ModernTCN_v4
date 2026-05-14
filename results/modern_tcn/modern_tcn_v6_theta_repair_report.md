# ModernTCN V6 Theta Repair Report

- base checkpoint: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_longrun_diag2steer_seed42\modern_tcn_seed42.pt`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_v6_longrun_diag2steer.mat`
- theta target: `0.750 deg`

## Baselines

| model | seed | main | turn | turnT | theta deg | slope |
|---|---:|---:|---:|---:|---:|---:|
| ModernTCN v6 base | 42 | 0.9778 | 0.9334 | 0.6344 | 1.1564 | 0.9529 |
| GRU v6 baseline | 73 | 0.9366 | 0.9096 | 0.5484 | 0.5556 | 0.9096 |

## Candidates

| pass | run_tag | main | turn | turnT | theta deg | err p95 | flat p95 | near-flat p95 | flat bias | slope | checkpoint |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | modern_tcn_v6_theta_repair_s42_lam100_f100_nf200_w1p0_unfreeze | 0.9767 | 0.9355 | 0.6237 | 0.9055 | nan | 3.9650 | 4.1157 | 0.0765 | 0.9397 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam100_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam075_f100_nf200_w1p0_unfreeze | 0.9752 | 0.9345 | 0.6344 | 1.3560 | nan | 5.5191 | 6.4300 | -0.0037 | 0.9416 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam075_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze | 0.9783 | 0.9408 | 0.6989 | 0.4906 | nan | 2.0334 | 2.1599 | -0.0701 | 0.9473 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam120_f100_nf200_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam100_f150_nf300_w1p0_unfreeze | 0.9783 | 0.9392 | 0.6882 | 0.4717 | 1.9841 | 1.9229 | 2.0810 | -0.1025 | 0.9454 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam100_f150_nf300_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam100_f400_nf800_w1p0_unfreeze | 0.9773 | 0.9387 | 0.6559 | 0.5101 | 2.2557 | 2.0906 | 2.2106 | -0.0622 | 0.9435 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam100_f400_nf800_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam080_f600_nf1200_w1p0_unfreeze | 0.9757 | 0.9371 | 0.6452 | 0.5942 | 2.5321 | 2.1139 | 2.1632 | -0.0412 | 0.9416 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam080_f600_nf1200_w1p0_unfreeze\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam060_f800_nf1600_w1p0_headonly | 0.9778 | 0.9334 | 0.6344 | 0.7620 | 3.1818 | 1.7540 | 1.9903 | -0.0626 | 0.9529 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam060_f800_nf1600_w1p0_headonly\modern_tcn_seed42.pt` |
| 0 | modern_tcn_v6_theta_repair_s42_lam100_f100_nf200_w1p0_headonly | 0.9778 | 0.9334 | 0.6344 | 0.5601 | 2.1578 | 1.9359 | 2.2979 | -0.1104 | 0.9529 | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v6_theta_repair_s42_lam100_f100_nf200_w1p0_headonly\modern_tcn_seed42.pt` |

## Selected

- `modern_tcn_v6_theta_repair_s42_lam100_f100_nf200_w1p0_unfreeze` with theta MAE `0.9055 deg`, main `0.9767`, turn `0.9355`, slope recall `0.9397`.
