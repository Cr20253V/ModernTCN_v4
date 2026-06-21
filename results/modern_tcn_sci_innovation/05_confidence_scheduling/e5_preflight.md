# E5 Confidence Scheduling Preflight

- status: PASS
- scope: E5 offline scheduling safety screen only; no training/export/formal compare
- baseline checkpoint: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.pt`
- baseline ONNX: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\08_models\modern_tcn\modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101\modern_tcn_seed101.onnx`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- sandbox root: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_sci_innovation\06_closed_loop_validation\sandbox`
- model_family: `small`
- source: `baseline_small`
- loss_mode: `fixed`
- input_dim: 22
- seq_len: 128
- feature_contract: `passive17_plus_all5`
- matlab E5 default enable: False
- no training: True
- no ONNX export: True
- no baseline overwrite: True
- no formal compare write: True

## Baseline References

- acc_main: 0.966963
- acc_turn: 0.578845
- acc_turn_transition: 0.497765
- theta_mae_deg: 0.679395
- flat_peak_theta_error: 5.335740
- theta_edge_p95_abs_err: 2.755057

## Replay Order Audit

```json
{
  "n_windows": 3602,
  "n_unique_run_id": 16,
  "n_contiguous_segments": 3174,
  "run_ids_are_contiguous": false,
  "n_noncontiguous_run_id": 16,
  "sample_noncontiguous_run_id": {
    "2.0": 487,
    "3.0": 508,
    "9.0": 492,
    "12.0": 483,
    "22.0": 130,
    "27.0": 110,
    "33.0": 101,
    "38.0": 89,
    "40.0": 96,
    "41.0": 95
  },
  "advisory_step_metrics": true,
  "note": "step and smoothness metrics are advisory when run_id is interleaved"
}
```
