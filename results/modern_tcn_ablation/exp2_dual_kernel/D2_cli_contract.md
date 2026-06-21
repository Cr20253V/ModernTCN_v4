# D2 CLI Contract

- pass: `1`
- train_script: `src/ModernTCN/train_modern_tcn.py`
- model_family: `small_dualkernel`
- default_output_root: `results/modern_tcn_ablation/exp2_dual_kernel`
- default_dataset_for_dualkernel: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- required_cli: `--model-family small_dualkernel --large-kernel --small-kernel --dual-branch-scale --small-branch-init --output-root --run-tag --no-overwrite`
- smoke_cli_supported: `--dry-run --limit-train --limit-val --limit-test`
- run_metadata: `config.json`, `config.md`, `git_hash.txt`, `dataset_contract_copy.json`, `feature_names.txt`, `metrics_val.csv`, `metrics_test.csv`
- no_overwrite_policy: non-empty output directories fail before training starts.

The default MATLAB deployment config is not edited; candidate deployment must pass explicit ONNX and dataset paths.
