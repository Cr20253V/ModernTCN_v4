# E3 Smoke Report

- status: PASS
- no ONNX export: True
- no MATLAB/Simulink closed-loop: True

| check | status | detail |
|---|---|---|
| `small_dry_run` | `dry_run_ok` | `dry_run forward ok` |
| `small_physics_group_gate_dry_run` | `dry_run_ok` | `dry_run forward ok` |
| `baseline_checkpoint_regression` | `PASS` | `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt` |
| `no_overwrite_probe` | `PASS` | `existing non-empty dir rejected` |
| `gate_stats_probe` | `PASS` | `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\03_physics_group_gate\_smoke\gate_stats_probe\physics_gate_statistics.json` |
