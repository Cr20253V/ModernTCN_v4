# exp1_grouped_ffn Handoff

## Final Decision

`NO_PROMOTION`.

在当前 22D plantfix ModernTCN-small 替换目标下，`grouped_ffn` 可以判定为不继续推进。不要进入 ONNX、MATLAB 一致性、closed-loop preflight 或 Simulink 闭环验证。

## Fixed Baseline

- plant revision: `agv_physics_v2_plantfix`
- feature contract: `passive17_plus_all5`
- input_dim: `22`
- seq_len: `128`
- current champion: `turn_l020_tt25_tcm14_stw055_slrw060_seed101`
- champion model dir: `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/`

Baseline offline metrics:

| metric | value |
|---|---:|
| acc_main | 0.966963 |
| acc_turn | 0.578845 |
| acc_turn_transition | 0.497765 |
| theta_mae_deg | 0.679395 |
| flat_recall | 0.969577 |
| stall_recall | 0.718750 |
| slope_recall | 0.974909 |

## What Was Implemented

Engineering support added during exp1:

- `small_gffn` model family.
- `ModernTCNGroupedConfig`, `ModernTCNGroupedBlock`, `ModernTCNGroupedSmall`.
- isolated training CLI support for `--model-family small_gffn`, `--output-root`, `--run-tag`, `--no-overwrite`.
- run metadata: `config.json`, `config.md`, `git_hash.txt`, `dataset_contract_copy.json`, `feature_names.txt`, `metrics_val.csv`, `metrics_test.csv`, reports.
- grouped ONNX namespace handling for future use: `modern_tcn_gffn_onnx_layers`.
- ONNXRuntime latency helper.
- baseline snapshot and schema tools under `results/modern_tcn_ablation/`.

Additional tuning support added after the first offline stop:

- CLI exposure for class-balance knobs: `main_class_multipliers`, `main_class_weight_method`, `turn_class_weight_method`, `main_neg_slope_weight`, `main_pos_slope_weight`.
- default-off validation selection terms: `select_stall_weight`, `select_stall_target`.

## Run Evidence

Original exp1:

- runs: 12
- directory: `results/modern_tcn_ablation/exp1_grouped_ffn/`
- summary: `grouped_ffn_offline_summary.csv`
- final report: `grouped_ffn_final_report.md`
- decision JSON: `promote_decision.json`
- best original candidate: `gffn_d4_k51_seed21`

Original best metrics:

| run | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gffn_d4_k51_seed21` | 0.963631 | 0.568573 | 0.506706 | 0.626342 | 0.968254 | 0.635417 | 0.973818 |

Failure reason:

- `acc_turn_transition` and `theta_mae_deg` were better than baseline.
- `acc_main`, `acc_turn`, and especially `stall_recall` missed the offline gate.
- no original run passed offline promotion gate.

Targeted tuning:

- runs: 9 seed21 screening runs
- directory: `results/modern_tcn_ablation/exp1_grouped_ffn_tune/`
- report: `grouped_ffn_tuning_report.md`
- decision JSON: `tune_decision.json`
- best tuned candidate: `tune_r2_lrslow_seed21`

Best tuned metrics:

| run | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tune_r2_lrslow_seed21` | 0.969184 | 0.559134 | 0.476900 | 0.727756 | 0.980159 | 0.635417 | 0.977818 |

Tuning result:

- targeted stall/turn/class-balance tuning did not fix `stall_recall`.
- stronger classification pressure degraded transition/theta.
- lower learning rate improved `acc_main` but lost transition/theta.
- `dmodel=5,k51` and `d4,k41` capacity/kernel checks were worse than original `d4,k51`.
- no tuned seed21 candidate was worth multi-seed validation.

## Final Interpretation

For this task, grouped_ffn's useful signal is local: it can improve transition and theta. The tradeoff is not acceptable for the current replacement goal because the current champion's value depends on stable global turn/main/stall behavior. Attempts to recover classification/stall performance collapse the transition/theta advantage.

Conclusion should be stated narrowly:

`grouped_ffn 在当前 22D plantfix ModernTCN-small 替换目标下 NO_PROMOTION；该结构可改善局部 transition/theta 指标，但不能稳定通过整体离线 gate，不建议进入 ONNX/MATLAB/closed-loop。`

This does not prove grouped FFN is universally invalid. It means it should not remain a priority for the current ablation sequence.

## Do Not Continue

- Do not spend more runs on `small_gffn` loss-weight tuning under the same structure.
- Do not export grouped_ffn ONNX.
- Do not run MATLAB generated layers for grouped_ffn.
- Do not run closed-loop for grouped_ffn.
- Do not replace current default ModernTCN-small.

## Recommended Next Step

Start exp2 in a fresh isolated branch/directory, reusing the exp1 engineering support:

- baseline snapshot
- no-overwrite output isolation
- unified metadata/config saving
- metrics schema
- summary writer
- explicit ONNX/MATLAB path policy if a candidate reaches later gates
- closed-loop short-path preflight policy

The frozen comparison anchor remains the 22D plantfix champion listed above.
