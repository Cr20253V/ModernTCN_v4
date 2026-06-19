# AGV Model Parameter Correction / ModernTCN Follow-up Handoff

Last updated: 2026-06-19
Workspace: `E:\Matlab\Simulink\S-Function_16`

## 1. Current Goal

Current goal is to continue improving **ModernTCN only** on top of the repaired
`plantfix` pipeline. GRU and TCN are now used as fixed comparators.

The current trustworthy comparison is:

`ModernTCN > GRU > TCN` in the three-path closed-loop aggregate.

30D command-response optimization is now closed. The 30D branch was useful as a
diagnostic, but no 30D candidate beat the 22D plantfix champion in the promotion
criteria. See:

- `results/paper/agv_model_parameter_correction_workflow/30D_CMDRESP_EXPERIMENT_CLOSURE_20260619.md`

## 2. Frozen Physical Baseline

- Plant revision: `agv_physics_v2_plantfix`
- Dataset contract: `passive17_plus_all5`
- Input dimension: `22`
- Sequence length: `128`
- Split policy: run-level, no leakage
- Scaler policy: reuse dataset-side normalization only
- Feature policy: passive-only, no new inputs

Authoritative dataset:

- `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
- `data/tcn/CURRENT_ModernTCN_DATASET.json`

Manifest:

- `results/paper/agv_model_parameter_correction_workflow/CURRENT_RESULT_MANIFEST_20260617.md`

## 3. Training History

### ModernTCN

The best current ModernTCN branch is the turn-focused seed101 model:

- `turn_l020_tt25_tcm14_stw055_slrw060_seed101`

It came from the stage-1/stage-2 plantfix retraining loop:

- stage-1 smoke / full plantfix retraining
- stage-2 targeted search around:
  - `l018_tt22_bal`
  - `l020_tt25_bal`
  - `l022_tt28_turn`
  - `l020_tt30_lr`

The selected closed-loop champion is **not** the offline best candidate.
The offline-only best was:

- `ModernTCN_stage2_l020_tt30_lr_seed303`

but it degraded badly in closed loop, so do not replace the champion with it.

### GRU

GRU was retrained on the same plantfix dataset with seeds:

- `21`
- `73`
- `101`

Seed101 is the current GRU closed-loop baseline.

### TCN

TCN was retrained on the same plantfix dataset with seeds:

- `21`
- `73`
- `101`

Seed101 is the current TCN closed-loop baseline.

## 4. Training Configurations

### ModernTCN champion

Report:

- `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/ModernTCN_train_report.md`

Key config:

- `input_dim=22`
- `seq_len=128`
- `channels=64`
- `blocks=5`
- `kernel_size=31`
- `dropout=0.15`
- `lambda_turn=0.20`
- `lambda_theta=0.55`
- `lambda_theta_flat=0.12`
- `turn_transition_weight=2.5`
- `turn_class_multipliers=[1.4, 0.8, 1.4]`
- `select_turn_weight=0.55`
- `select_turn_transition_weight=1.20`
- `select_turn_lr_weight=0.60`
- `best_epoch=63`

### GRU seed101

Report:

- `results/paper/agv_model_parameter_correction_workflow/08_models/matlab_logs/full_gru_v5_plantfix_passive17_plus_all5_seed101/GRU_train_report.md`

Key config:

- `hidden_size=96`
- `num_layers=2`
- `dropout=0.20`
- `batch_size=128`
- `max_epochs=140`
- `lambda_turn=0.08`
- `lambda_theta=0.55`
- `lambda_theta_flat=0.12`
- `turn_class_multipliers=[1.08, 1.00, 1.08]`
- `turn_transition_weight=1.20`
- `select_turn_lr_weight=0.20`
- `best_epoch=48`

### TCN seed101

Report:

- `results/paper/agv_model_parameter_correction_workflow/08_models/matlab_logs/full_tcn_v5_plantfix_passive17_plus_all5_seed101/TCN_train_report.md`

Key config:

- `num_blocks=6`
- `num_filters=96`
- `kernel_size=3`
- `dropout=0.15`
- `batch_size=128`
- `best_metric=turn_priority`
- `turn_finetune_start_epoch=64`
- `turn_finetune_lambda_turn=0.50`
- `disable_other_losses=1`
- `turn_transition_weight=1.25`
- `best_epoch=74`

## 5. Offline Results

### ModernTCN champion

- `acc_main=0.96696`
- `acc_turn=0.57885`
- `acc_turn_transition=0.49776`
- `theta_mae_deg=0.67939`
- `theta_abs_le_10_p95_abs_err_deg=1.82747`
- `flat_recall=0.96958`
- `slope_recall=0.97491`

### GRU seed101

- `acc_main=0.96030`
- `acc_turn=0.53800`
- `acc_turn_transition=0.39340`
- `theta_mae_deg=0.71580`
- `theta_abs_le_10_p95_abs_err_deg=2.23520`

### TCN seed101

- `acc_main=0.74403`
- `acc_turn=0.54303`
- `acc_turn_transition=0.42474`
- `theta_mae_deg=0.86309`
- `theta_abs_le_10_p95_abs_err_deg=2.14177`

### ModernTCN stage-2 offline best

- `ModernTCN_stage2_l020_tt30_lr_seed303`
- offline score best in the search
- do **not** use as the main closed-loop champion

## 6. Closed-Loop Results

Closed-loop report:

- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/dual_modern_report.md`
- `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/dual_modern_aggregate.csv`

Three paths:

- `path_factory_logistics_showcase_theta10_v3`
- `path_closed_loop_long_updown_theta10_v1`
- `path_closed_loop_sharp_turn_transition_theta10_v1`

### Closed-loop aggregate

| controller | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | rank_ey |
|---|---:|---:|---:|---:|---:|
| ModernTCN_turn_l020_tt25_seed101 | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 1 |
| GRU | 0.939034 | 8.40855 | 4.85317 | 659.981 | 3 |
| TCN | 5.26379 | 27.6947 | 9.04896 | 1029.16 | 4 |

### ModernTCN closed-loop per-path highlights

- `path_factory_logistics_showcase_theta10_v3`
  - `ey_rmse=0.0273817`
  - `theta_mae_deg=0.444974`
  - `main_acc_pct=98.1901`
  - `turn_acc_pct=67.0519`
- `path_closed_loop_long_updown_theta10_v1`
  - `ey_rmse=0.0336777`
  - `theta_mae_deg=0.705796`
  - `main_acc_pct=91.1055`
  - `turn_acc_pct=47.7591`
- `path_closed_loop_sharp_turn_transition_theta10_v1`
  - `ey_rmse=0.0271049`
  - `theta_mae_deg=0.433332`
  - `main_acc_pct=94.9913`
  - `turn_acc_pct=48.1460`

## 7. MPC / LPV / Closed-Loop Controller Baseline

Current plantfix controller support is aligned to the repaired plant and the
P0 oracle-style tuning:

- `Np=150`
- `Nc=30`
- `Q=[100, 100, 15, 3]`
- `R=[3e-5, 3e-5]`
- `dR=[1e-3, 1e-3]`

Relevant code paths:

- `src/core/UpdatePlantModel.m`
- `src/core/UpdatePlantModel_gru.m`
- `src/core/parameters.m`
- `src/core/state_eq.m`
- `src/core/state_eq_ref.m`
- `src/lpv/lin_agv_at_point.m`
- `src/mpc/Cost_Function.m`
- `src/Compare/run_closed_loop_model_once.m`
- `src/Compare/compare_tcn_gru_modern_closed_loop_out.m`

## 8. Cleanup State

Old exploration branches have been archived under:

- `archive/obsolete_experiments_20260617/`

Do not auto-restore command-response / weak-combo / showcase branches unless
they are explicitly needed again.

The working tree still contains many tracked source diffs that are part of the
current plantfix result. Do not use a blanket revert or hard reset.

## 9. Next Conversation Recommendation

Do not continue the 30D command-response branch unless the user explicitly
reopens it as a larger data-generation redesign. The completed 30D checks were:

- full 30D `cmdresp_lite_v1`
- fixed online `u_cmd` lag alignment
- command sign / phase audit
- 24D `cmdresp_lag1_only_v1`
- 30D command-feature dropout

Final 30D decision: `NO_PROMOTION`. The 22D champion remains authoritative.

If continuing ModernTCN work later, start from the 22D plantfix branch. Good
follow-up directions:

1. Try a narrower ModernTCN seed sweep around the current champion.
2. Try a small `turn_transition_weight` / `select_turn_*` refinement sweep.
3. Keep GRU/TCN frozen as comparators.
4. Keep the current plantfix dataset and closed-loop shell unchanged unless a
   new plant/data mismatch is found.
