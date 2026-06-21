# Phase 3A seq256 small seed21 Exploratory Screening

## Decision

- decision: `NO_PROMOTION`
- next_allowed_step: `STOP seq256 small; no seed expansion, no deployment`
- dataset_status: `exploratory_python_builder`
- matlab_parity_required_before_promotion: `true`
- seed21_screening_only: `true`
- not_replacement_for_seed101_champion: `true`
- ONNX/MATLAB/Simulink/closed-loop: `not executed`

## Scope Boundary

- This run uses seq256 data built by the Python builder and keeps the builder audit attached.
- The seq128 champion is seed101; this seed21 result is only a continue/stop screen.
- No k51, loss tuning, seed42/101 expansion, ONNX export, MATLAB, Simulink, or closed-loop was executed.

## Evidence

- preflight: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_preflight_report.md`
- recipe parity: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_recipe_parity.csv`
- train command: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_train_command.txt`
- candidate summary: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_seq256_small_seed21_summary.csv`
- gate matrix: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_gate_matrix.csv`
- decision json: `results/modern_tcn_next_round_22d/03_seq256_small_baseline/phase3A_seed21/phase3A_decision.json`
- dataset audit: `results/modern_tcn_next_round_22d/02_seq256_dataset/seq256_builder_policy_audit.md`

## Candidate Metrics

- acc_main: `0.9592833876221498`
- acc_turn: `0.6085776330076005`
- acc_turn_transition: `0.5415282392026578`
- theta_mae_deg: `0.8204795122146606`
- flat_recall: `0.9050802139037433`
- stall_recall: `0.627906976744186`
- slope_recall: `0.9835087719298246`
- theta_edge_p95_abs_err: `4.175807476043701`
- flat_peak_theta_error: `6.42245626449585`
- false_turn_straight: `0.41015018125323666`

## Gate Matrix

| metric | op | threshold | candidate | passed |
|---|---|---:|---:|---:|
| `acc_main` | `>=` | 0.963962798445 | 0.959283387622 | 0 |
| `acc_turn` | `>=` | 0.573845086063 | 0.608577633008 | 1 |
| `acc_turn_transition` | `>=` | 0.497764530551 | 0.541528239203 | 1 |
| `theta_mae_deg` | `<=` | 0.68939478159 | 0.820479512215 | 0 |
| `flat_recall` | `>=` | 0.959576719577 | 0.905080213904 | 0 |
| `stall_recall` | `>=` | 0.66875 | 0.627906976744 | 0 |
| `slope_recall` | `>=` | 0.969909090909 | 0.98350877193 | 1 |
| `theta_edge_p95_abs_err` | `<=` | 2.80505685806 | 4.17580747604 | 0 |

## Isolation Check

| path | file_count_changed | latest_mtime_changed |
|---|---:|---:|
| `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_ablation` | 0 | 0 |
| `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101` | 0 | 0 |
| `E:\Matlab\Simulink\S-Function_16\results\compare` | 0 | 0 |
| `E:\Matlab\Simulink\S-Function_16\src\ModernTCN\generated_layers` | 0 | 0 |
