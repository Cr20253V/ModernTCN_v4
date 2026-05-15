# ModernTCN ONNXRuntime Latency Benchmark

- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.onnx`
- dataset: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`
- provider: `CPUExecutionProvider`
- batch size: `1`
- warmup: `200`
- repeat: `5000`

| metric | value (ms) |
|---|---:|
| mean_ms | 0.380407 |
| p50_ms | 0.3659 |
| p95_ms | 0.450725 |
| p99_ms | 0.600001 |
| max_ms | 1.8839 |
