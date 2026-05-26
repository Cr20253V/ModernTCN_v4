# Table Data Source Log

| Table | Field | Source | Note |
|---|---|---|---|
| Table 1 | vehicle parameters | `src/core/parameters.m` | Parsed params.* assignments. |
| Table 2 | sampling time | `src/core/parameters.m` | Parsed params.Ts. |
| Table 3 | dataset contract | `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json` | Loaded JSON contract. |
| Table 2 | MPC defaults and constraints | `src/mpc/mpc_setup_single_interp.m` | Parsed opts.* defaults. |
| Table 4 | GRU metadata | `data/models/GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat` | Loaded MATLAB metadata via scipy.io.loadmat. |
| Table 4 | TCN metadata | `data/models/TCN_meta_tcn_theta10_uniform_h0_v2_tcn96_rawtheta_sym_seed21.mat` | Loaded MATLAB metadata via scipy.io.loadmat. |
| Table 4 | ModernTCN trainable parameters | `results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt` | Loaded PyTorch checkpoint and counted model_state tensors. |
| Table 4 | GRU parameter count | `computed` | Computed from GRU_train.m architecture and GRU metadata shapes. |
| Table 4 | TCN parameter count | `computed` | Computed from TCN_train.m architecture and TCN metadata shapes. |
| Table 5 | baseline definitions | `results/paper/Latex/paper_v1.tex` | Definition table aligned with existing manuscript text. |
| Table 6 | main route summary | `results/compare/lpvmpc_theta_baseline/path_factory_logistics_showcase_theta10_v3/tcn_gru_modern_lpvmpc_theta_baseline_summary.csv` | Loaded CSV data. |
| Table 6 | Fig. 8 smoothness summary | `src/pic&table/fig08_control_smoothness_metric_summary.csv` | Loaded CSV data. |
| Table 6 | Fig. 7 scheduled-slope manifest | `src/pic&table/fig07_scheduled_slope_source_manifest.csv` | Loaded CSV data. |
| Table 6 | scheduled slope index | `src/pic&table/generate_fig7_scheduled_slope.py` | Uses Python rho[:, 2], labeled rho_f[:,3], i.e. MATLAB rho_f(:,3), the third channel theta_f. |
| Table 7 | multi-route aggregate | `results/compare/multipath_closed_loop/multipath_closed_loop_aggregate.csv` | Loaded CSV data. |
| Table 8 | robustness aggregate | `results/compare/robustness_closed_loop/robustness_closed_loop_aggregate.csv` | Loaded CSV data. |
| Table 9 | Fig. 10 metric source | `src/pic&table/fig10_offline_closed_loop_mismatch_metric_source_data.csv` | Loaded CSV data. |
| Table 10 | computational timing summary | `results/compare/realtime_benchmark/realtime_summary.csv` | Loaded CSV data. |
| Table 10 | runtime platform metadata | `results/compare/realtime_benchmark/realtime_onnx_runtime_metadata.json` | Loaded JSON contract. |

## Table 6 Scheduled-Slope Index Check

- Fig. 7 source script reads `signals.rho_f` and uses Python `rho[:, 2]`.
- Because Python uses zero-based indexing, `rho[:, 2]` is the third channel.
- The script labels the diagnostic as `rho_f[:,3]`, matching MATLAB `rho_f(:,3)`.
- Project documentation describes `rho_f=[v_f; omega_f; theta_f]`, so the third channel is the conditioned scheduled slope used by LPV-MPC.
- Therefore Table 6 should use `theta_sched_mae_deg` derived from `rho_f(:,3)` in MATLAB notation, not `rho_f(:,2)`.
