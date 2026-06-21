# D0 Baseline Preflight

- pass: `1`
- git_hash_now: `b0217f9149e8616a4a276cab48820373acaed963`
- snapshot_git_hash: `b0217f9149e8616a4a276cab48820373acaed963`
- plant_revision: `agv_physics_v2_plantfix`
- feature_contract: `passive17_plus_all5`
- input_dim: `22`
- seq_len: `128`
- train/val/test windows: `16529/3695/3602`
- dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- contract: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
- baseline_checkpoint: `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/modern_tcn_seed101.pt`
- baseline_onnx: `results/paper/agv_model_parameter_correction_workflow/08_models/modern_tcn/modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101/modern_tcn_seed101.onnx`
- closed_loop_baseline: `results/paper/agv_model_parameter_correction_workflow/09_closed_loop/dual_modern_seed101_full/`
- matlab_default_points_to_old_baseline: `1`

## Feature Names

1. `gyro_z`
2. `I_lf`
3. `I_rr`
4. `omega_wheel_lf`
5. `omega_wheel_rr`
6. `delta_lf`
7. `delta_rr`
8. `v_hat`
9. `dv_hat_dt`
10. `ws_imbalance`
11. `I_sum`
12. `I_diff_signed`
13. `I_diff_abs`
14. `kappa_proxy`
15. `accel_per_current`
16. `dv_hat_dt_lp`
17. `accel_x_wheel`
18. `I_drive_signed`
19. `current_per_accel`
20. `drive_load_proxy`
21. `a_hp`
22. `yaw_consistency_error`
