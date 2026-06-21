# seq256 Dataset Validation

- generated_at: `2026-06-21 13:16:15`
- status: `PASS`
- dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256.mat`
- contract: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_seq256_contract.json`
- source train data: `data/tcn/ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- split source reused: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- scaler policy: `fit_train_only_apply_val_test_online`
- no split leakage: `1`
- builder policy audit: `results/modern_tcn_next_round_22d/02_seq256_dataset/seq256_builder_policy_audit.md`

| split | windows | unique_runs |
|---|---:|---:|
| train | 18210 | 71 |
| val | 4209 | 15 |
| test | 3684 | 16 |

Validation passed for the Python-built seq256 chain. It reuses the baseline run split and documented preparation policy, but does not claim row-identical MATLAB RNG parity; see the builder policy audit. Phase 3 training remains deferred and requires a separate seed21 screening plan.
