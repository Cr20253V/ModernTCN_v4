# E3 Engineering Preflight

- status: PASS
- scope: E3 / 03_physics_group_gate only; no ONNX; no MATLAB/Simulink.
- model_family: `small_physics_group_gate`
- loss_mode: `fixed`
- E1/E2 loss explicitly disabled: transition_focal=0, stall_focal=0, theta_smooth=0, theta_smooth_mode=off
- dataset input: `[batch,128,22]`
- feature_contract: `passive17_plus_all5`
- residual_group: `empty`
- baseline checkpoint regression target: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt`

## Baseline Reference

- acc_main: 0.9669627984453082
- acc_turn: 0.5788450860632982
- acc_turn_transition: 0.4977645305514158
- theta_mae_deg: 0.6793947815895081
- flat_recall: 0.9695767195767195
- stall_recall: 0.71875
- slope_recall: 0.974909090909091
- theta_edge_p95_abs_err: 2.755056858062744
- flat_peak_theta_error: 5.335740089416504
