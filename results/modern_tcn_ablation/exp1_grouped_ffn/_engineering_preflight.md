# Exp1 grouped_ffn Engineering Preflight

- baseline snapshot: `PASS`
- baseline metrics snapshot: `PASS`
- default config action: `no global default edit`; closed-loop candidates must pass `modern_tcn_sim_cfg.onnx_file` explicitly
- model import/forward: `PASS` for `small`, `small_gffn`, and `full`
- baseline small checkpoint restore: `PASS`
- small_gffn dry-run: `PASS`
- smoke train/save: `PASS`
- no_overwrite protection: `PASS`

Evidence:

- `results/modern_tcn_ablation/_baseline_snapshot/baseline_identity.md`
- `results/modern_tcn_ablation/_baseline_snapshot/baseline_summary.md`
- `results/modern_tcn_ablation/_baseline_snapshot/default_path_alignment_report.md`
- `results/modern_tcn_ablation/exp1_grouped_ffn/_engineering_preflight/baseline_small_regression.md`
- `results/modern_tcn_ablation/exp1_grouped_ffn/_smoke/gffn_d4_k31_seed21_smoke/config.json`
- `results/modern_tcn_ablation/exp1_grouped_ffn/_smoke/gffn_d4_k31_seed21_smoke/metrics_test.csv`
