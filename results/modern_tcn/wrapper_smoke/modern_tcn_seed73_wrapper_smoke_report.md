# ModernTCN Wrapper Smoke Test

- seed: `73`
- pass: `1`
- tolerance: `1.0e-06`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73.onnx`
- reference: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_transition_rich_v3_kinTurnD_seed73\modern_tcn_seed73_matlab_full_testset_outputs.mat`

| max main abs error | max turn abs error | max theta abs error |
|---:|---:|---:|
| 0 | 0 | 0 |

## Checked Windows

| index | main | turn | theta deg | main confidence | turn confidence |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | -1 | 0.1839 | 1.0000 | 0.5563 |
| 2 | 3 | -1 | 3.9993 | 1.0000 | 0.9927 |
| 3 | 1 | 0 | 0.4297 | 1.0000 | 0.8210 |
| 16 | 1 | 0 | 0.0236 | 1.0000 | 0.7092 |
| 128 | 1 | -1 | -0.0195 | 1.0000 | 0.8349 |
| 512 | 1 | -1 | 0.4476 | 1.0000 | 0.9606 |
| 1024 | 1 | 0 | -0.0886 | 1.0000 | 0.6282 |
| 2048 | 3 | 1 | 4.5563 | 0.9999 | 0.9220 |
| 2849 | 3 | 0 | -3.6004 | 1.0000 | 0.9741 |
