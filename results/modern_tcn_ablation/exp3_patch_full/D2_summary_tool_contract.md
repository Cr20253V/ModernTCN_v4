# D2 exp3 Tool Contract

- tool: `results/modern_tcn_ablation/exp3_tools.py`
- run_glob: `results/modern_tcn_ablation/exp3_patch_full/full128_*_seed*/modern_tcn_full_seed*_summary.csv`
- excluded_legacy_assertion: `required before best-run selection`
- no_seq256: `true; this tool does not create seq_len=256 data or scripts`
- outputs: `patch_full_offline_summary.csv`, `patch_full_offline_summary.md`, `best_run_selection.md`, `promote_decision.json`
