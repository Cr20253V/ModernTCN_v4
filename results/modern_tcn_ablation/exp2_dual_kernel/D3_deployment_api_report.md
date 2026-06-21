# D3 Deployment API Report

- pass: `1`
- checkpoint_restore: `build_model_from_checkpoint_dict` recognizes `small_dualkernel`
- onnx_meta_policy: export sidecar uses `<onnx_stem>_onnx_export.json`
- onnx_no_overwrite_policy: ONNX, PyTorch reference MAT, and export JSON all fail if present and `--no-overwrite` is set
- matlab_predictor_namespace: `small_dualkernel` maps to `modern_tcn_dualkernel_onnx_layers`
- matlab_consistency_namespace: `small_dualkernel` maps to `modern_tcn_dualkernel_onnx_layers`
- default_namespace_policy: `modern_tcn_onnx_layers` remains for baseline/default ONNX only

MATLAB/Simulink was not started in this node.
