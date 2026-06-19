# 30D Command-Response ModernTCN Experiment Closure

Date: 2026-06-19
Workspace: `E:\Matlab\Simulink\S-Function_16`

## Decision

Stop further optimization of the 30D command-response ModernTCN branch.

The current paper-ready ModernTCN result remains the 22D plantfix champion:

- model: `ModernTCN_22d_turn_l020_tt25_seed101_champion`
- feature contract: `passive17_plus_all5`
- input_dim: `22`
- plant revision: `agv_physics_v2_plantfix`
- closed-loop aggregate: `ey_rmse_mean=0.0293881`, `ey_peak_worst=0.0852651`, `xy_rmse_mean=0.599794`, `j_du_mean=3.68078`

No 30D candidate should replace this model.

## Work Completed

1. Built the 30D `cmdresp_lite_v1` feature branch from the existing v5 plantfix raw dataset.
   Added eight online-available historical command features:
   `F_cmd_lag1`, `omega_cmd_lag1`, `dF_cmd_lag1`, `domega_cmd_lag1`,
   `F_cmd_mean_0p2s`, `F_cmd_std_0p2s`, `omega_cmd_mean_0p2s`,
   `omega_cmd_std_0p2s`.

2. Built and manually checked the Simulink test shell:
   `LPVMPC_AGV_simulink_Modern_TCN_30Dtest.slx`.

3. Fixed the online command-history alignment by passing already-lagged MPC commands
   into the command-response feature extractor during closed-loop simulation.

4. Audited command sign / phase behavior. The training raw command signs do not align
   with turn labels as cleanly as closed-loop MPC commands, so the issue is not only
   a one-step lag bug.

5. Ran three 30D-family checks:
   - full 30D `cmdresp_lite_v1`
   - 24D `cmdresp_lag1_only_v1`
   - 30D `cmdresp_dropout_v1` with `command_dropout_prob=0.35`

## Closed-Loop Evidence

### 22D Champion Baseline

| controller | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | rank_ey |
|---|---:|---:|---:|---:|---:|
| 22D champion | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 1 |

### Best Full 30D After Lag Fix

Best 30D full candidate:
`ModernTCN_30d_cmdresp_l020_tt30_lr_seed303`

| ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean |
|---:|---:|---:|---:|
| 0.0314936 | 0.104009 | 0.375985 | 3.90409 |

It improved `xy_rmse_mean`, but missed the main `ey_rmse_mean` and
`ey_peak_worst` closed-loop criteria.

### 24D Lag1-Only Ablation

Best 24D lag1-only candidate:
`ModernTCN_24d_cmdresp_lag1_l022_tt28_turn_seed101`

| ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean |
|---:|---:|---:|---:|
| 0.038966 | 0.164780 | 0.447844 | 9.42284 |

The lag1-only ablation did not fix the problem. The other selected lag1-only
candidate failed badly in closed loop.

### 30D Command Dropout

Best dropout candidate:
`ModernTCN_30d_cmdresp_dropout_p35_l022_tt28_turn_seed101`

| controller | ey_rmse_mean | ey_peak_worst | xy_rmse_mean | j_du_mean | turn_acc_mean |
|---|---:|---:|---:|---:|---:|
| 22D champion | 0.0293881 | 0.0852651 | 0.599794 | 3.68078 | 54.319 |
| 30D dropout best | 0.0299767 | 0.154851 | 0.410367 | 7.11791 | 43.8505 |

Dropout brought `ey_rmse_mean` close to the 22D champion and improved
`xy_rmse_mean`, but it worsened peak lateral error, control smoothness, and
turn recognition. It is therefore not promotable.

## Root-Cause Summary

Adding command features made the model more dependent on MPC command patterns.
Those command patterns are not distributed the same way in the offline training
raw data and in closed-loop simulation, especially around turn labels and
transition zones. The added variables are online-legal signals, but they create
a shortcut: the model can learn command-response correlations that look good
offline yet are brittle when the controller behavior changes in closed loop.

The evidence says the degradation is not caused by a single implementation bug:

- one-step command lag was fixed, but 30D still did not beat 22D;
- lag1-only command features did not recover the result;
- command dropout reduced shortcut dependence but damaged turn recognition and
  control smoothness.

## Practical Conclusion

Do not keep iterating on 30D command-response in the current paper branch.

If this idea is reopened later, it should not start from small loss-weight tweaks.
The likely useful restart would need a redesigned data-generation loop that
matches closed-loop MPC command distributions, or a separate robustness objective
that explicitly penalizes command shortcut dependence. That is a larger branch,
not a cleanup-level follow-up.

## Cleanup Note

After recording this conclusion, the 30D-only dataset scripts, command-response
training grids, closed-loop runner scripts, exported candidate models, diagnostic
outputs, and the temporary `LPVMPC_AGV_simulink_Modern_TCN_30Dtest.slx` model
were removed from the active worktree. The retained artifact for this branch is
this closure note only.
