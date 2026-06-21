# grouped_ffn Targeted Tuning Report

## Decision

- decision: `NO_PROMOTION`
- stop_node: `tuning_seed21_screen`
- multi_seed_validation: `not_executed`
- onnx_matlab_closed_loop: `not_executed`
- reason: targeted tuning did not produce a seed21 candidate that improves the original grouped_ffn best balance; no tuned run passed the offline gate.

## Fixed Contract

- dataset: `plantfix passive17_plus_all5`
- input_dim: `22`
- seq_len: `128`
- baseline champion: `turn_l020_tt25_tcm14_stw055_slrw060_seed101`
- output isolation: `results/modern_tcn_ablation/exp1_grouped_ffn_tune/`

## Baseline And Original Best

| run | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline champion | 0.966963 | 0.578845 | 0.497765 | 0.679395 | 0.969577 | 0.718750 | 0.974909 |
| original gffn best `gffn_d4_k51_seed21` | 0.963631 | 0.568573 | 0.506706 | 0.626342 | 0.968254 | 0.635417 | 0.973818 |

Original grouped_ffn strength is transition and theta: `acc_turn_transition` and `theta_mae_deg` beat baseline. The weakness is overall turn and main/stall balance: `acc_turn`, `acc_main`, and especially `stall_recall` miss the offline gate.

## Tuning Rationale

The grouped_ffn block separates temporal, variable-wise FFN, and channel-wise FFN residuals. Current results suggest it can model transition/theta dynamics, but it is less robust on global class balance and straight/stall discrimination. Tuning therefore focused on:

- preserving the `d4,k51` transition/theta advantage;
- increasing main/stall selection pressure without overcorrecting;
- improving turn recall through `lambda_turn`, `turn_transition_weight`, and turn class multipliers;
- checking whether intermediate capacity/kernel settings improve the tradeoff.

## Tuning Rounds

Round 1, loss/selection stress test:

- `tune_r1_stallw_seed21`: stronger stall/main selection pressure.
- `tune_r1_turnheavy_seed21`: stronger turn loss and turn selection pressure.
- `tune_r1_classbal_seed21`: stronger main class balance and reduced theta pressure.
- `tune_r1_lowtheta_seed21`: lower theta weight to free capacity for classification.

Result: all four degraded the original transition/theta balance, and none improved stall recall enough to matter.

Round 2, mild recipe tuning around original best:

- `tune_r2_mildstall_seed21`: mild stall selection, `dropout=0.18`.
- `tune_r2_lrslow_seed21`: lower `lr=0.0007`, mild stall selection.
- `tune_r2_lowdrop_seed21`: lower dropout and mild stall selection.

Result: `tune_r2_lrslow_seed21` improved `acc_main` to `0.969184`, but lost transition/theta performance and still missed `acc_turn`, `acc_turn_transition`, `theta_mae_deg`, and `stall_recall` gates.

Round 3, capacity/kernel check:

- `tune_r3_d5_k51_seed21`: larger `dmodel=5`, `kernel=51`.
- `tune_r3_d4_k41_seed21`: intermediate `kernel=41`.

Result: both were worse than original `d4,k51` on transition/theta and turn.

## Tuned Seed21 Results

| run | acc_main | acc_turn | acc_turn_transition | theta_mae_deg | flat_recall | stall_recall | slope_recall |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tune_r2_lrslow_seed21` | 0.969184 | 0.559134 | 0.476900 | 0.727756 | 0.980159 | 0.635417 | 0.977818 |
| `tune_r1_turnheavy_seed21` | 0.960577 | 0.542199 | 0.466468 | 0.774954 | 0.947090 | 0.635417 | 0.975636 |
| `tune_r1_stallw_seed21` | 0.966408 | 0.517768 | 0.439642 | 0.867703 | 0.966931 | 0.635417 | 0.977818 |
| `tune_r3_d5_k51_seed21` | 0.963076 | 0.490561 | 0.435171 | 1.088906 | 0.981481 | 0.614583 | 0.970182 |
| `tune_r1_classbal_seed21` | 0.963354 | 0.518323 | 0.421759 | 1.175514 | 0.980159 | 0.635417 | 0.970182 |
| `tune_r2_mildstall_seed21` | 0.961410 | 0.535813 | 0.417288 | 0.877343 | 0.939153 | 0.635417 | 0.978909 |
| `tune_r2_lowdrop_seed21` | 0.959745 | 0.524708 | 0.406855 | 0.892806 | 0.976190 | 0.645833 | 0.966182 |
| `tune_r3_d4_k41_seed21` | 0.959467 | 0.486674 | 0.393443 | 1.121957 | 0.974868 | 0.635417 | 0.966545 |
| `tune_r1_lowtheta_seed21` | 0.950028 | 0.486396 | 0.377049 | 1.043335 | 0.984127 | 0.635417 | 0.951636 |

## Conclusion

The useful grouped_ffn signal remains the original `d4,k51` recipe: it can improve transition and theta, but this advantage is fragile. Targeted tuning showed a consistent tradeoff: increasing classification/stall pressure recovers parts of `acc_main` or slope behavior, but it collapses transition/theta and does not fix stall recall. Increasing capacity or using an intermediate kernel also does not help.

Because no tuned seed21 candidate is better than the original grouped_ffn best, multi-seed validation would mostly quantify a weaker recipe. The tuning run therefore stops before multi-seed, ONNX, MATLAB, and closed-loop.

## Evidence

- original summary: `results/modern_tcn_ablation/exp1_grouped_ffn/grouped_ffn_offline_summary.csv`
- tuning summary: `results/modern_tcn_ablation/exp1_grouped_ffn_tune/grouped_ffn_offline_summary.csv`
- tuning best selection: `results/modern_tcn_ablation/exp1_grouped_ffn_tune/best_run_selection.md`
- tuning logs: `results/modern_tcn_ablation/exp1_grouped_ffn_tune/_logs/`
