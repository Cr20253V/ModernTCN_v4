# Window 2 Rerun Sandbox Preflight

- scope: sandbox-only closed-loop screening
- formal validation: not executed
- historical Class B IDs remain unchanged; rerun IDs are registered as new executable sandbox candidates
- selected candidates: uncertainty_seed101_rerun_20260622, mode_theta_detach_flatreg001_seed21_rerun_20260622
- all selected ready: True
- baseline ONNX: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`

## Candidate Readiness

| order | candidate | source historical candidate | export | onnxruntime | ready | boundary |
|---:|---|---|---|---|---:|---|
| 1 | `uncertainty_seed101_rerun_20260622` | `uncertainty_seed101` | reused_existing | reused_existing | 1 | new executable rerun; not a restored historical uncertainty_seed101 checkpoint |
| 2 | `mode_theta_detach_flatreg001_seed21_rerun_20260622` | `mode_theta_detach_flatreg001_seed21` | reused_existing | reused_existing | 1 | new executable rerun; not a restored historical mode_theta_detach_flatreg001_seed21 checkpoint |
