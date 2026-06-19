# Stage 1 Plantfix Execution Summary

- date: 2026-06-15
- plant revision: `agv_physics_v2_plantfix`
- feature contract: `passive17_plus_all5`
- input_dim: `22`

## Completed

1. Plant revision freeze
   - Added `src/core/agv_plant_revision.m`.
   - Captures current stiffness, yaw damping, and beta damping policy.

2. Open-loop smoke
   - Report: `03_open_loop/stage1_open_loop_smoke_report.md`
   - Result: pass.
   - Cases: straight/turn, flat/slope; no NaN/Inf and bounded beta/omega.

3. Full v5 raw + dataset rebuild
   - Raw: `data/tcn/ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
   - Dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
   - Contract: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`
   - Runs: 102/102 complete, zero failed runs.
   - Windows: train 16529, val 3695, test 3602.
   - `CURRENT_ModernTCN_DATASET.json` now points to the v5 plantfix dataset.

4. Versioned LPV DB + MPC candidate
   - LPV DB: `04_lpv_database/lin_agv_db_agv_physics_v2_plantfix.mat`
   - MPC maps: `06_mpc_retuning/maps_best_agv_physics_v2_plantfix_stage1.mat`
   - Canonical `data/models/lin_agv_db.mat` and `data/models/maps_best.mat` were not intentionally overwritten by these Stage 1 runners.
   - LPV rebuild completed 4125/4125 grid points, with 0 unstable points.
   - Note: low-speed extreme grid points still emit near-singular warnings; keep this as an MPC/LPV validation risk.

5. Model smoke retraining + ONNX checks
   - ModernTCN smoke: seed 21, 20 epochs, checkpoint and ONNX generated.
   - GRU smoke: seed 101, 20 epochs, status trained.
   - TCN smoke: seed 21, 20 epochs, status trained.
   - ONNXRuntime consistency: pass.
   - MATLAB ONNX consistency: pass.
   - Report: `08_models/stage1_model_retraining_report.md`

6. Closed-loop smoke
   - Smoke horizon: 1.0 s.
   - Paths: all three Stage 1 paths.
   - Controllers: ModernTCN, GRU, TCN, theta0, oracle-ref.
   - Runtime provenance verified in log: versioned LPV DB, `stage1_plantfix_p0` runtime MPC override, and v5 learned-model configs.
   - Log: `09_closed_loop/stage1_closed_loop_smoke_1s.log`
   - Report: `09_closed_loop/stage1_closed_loop_report.md`
   - The smoke ranking is not a final result; at 1 s it mainly verifies wiring and provenance.

## Important Fixes Made During Execution

- `TCN_gen_train_data.m` now stamps raw data with `plant_revision` and skips neural model preload for data generation.
- `TCN_prepare_dataset.m` now carries `plant_revision` into dataset metadata and contract JSON.
- `build_agv_theta10_uniform_dataset.m` now respects `max_paths` with manifest paths and forwards split controls.
- `preloadfcn_gru.m` now supports `mpc_runtime_override`, runtime DB selection, and external `tcn_sim_cfg`.
- `preloadfcn_v2.m` now supports runtime DB selection for theta0/oracle baselines.
- `run_closed_loop_model_once.m` now injects `tcn_sim_cfg` before model preload.
- Stage 1 closed-loop runner now separates smoke/full model artifacts and injects versioned MPC/DB provenance.
- ModernTCN training wrapper now writes a marker so a future full run will not accidentally reuse the 20-epoch smoke checkpoint.

## Remaining Full-Result Steps

Run these only when ready for a long job.

```powershell
python results\paper\agv_model_parameter_correction_workflow\08_models\run_stage1_plantfix_train.py --mode full --no-skip-existing --device auto
python results\paper\agv_model_parameter_correction_workflow\08_models\run_stage1_plantfix_train.py --mode onnx
matlab -batch "init_project; addpath(fullfile(project_root(),'results','paper','agv_model_parameter_correction_workflow','09_closed_loop')); result=run_stage1_closed_loop_validation(struct('mode','preflight'));"
matlab -batch "init_project; addpath(fullfile(project_root(),'results','paper','agv_model_parameter_correction_workflow','09_closed_loop')); result=run_stage1_closed_loop_validation(struct('mode','full'));"
```

Expected cost: MATLAB GRU/TCN smoke used about 37 minutes for 20 epochs total; the original 140-epoch, 3-seed full MATLAB training is likely many hours.

## Interpretation Boundary

This run establishes the corrected, physically self-consistent data and smoke-validated deployment pipeline. It does not yet establish the final ModernTCN vs GRU vs TCN paper ranking, because the final 3-seed training and full-route closed-loop evaluation are still pending.
