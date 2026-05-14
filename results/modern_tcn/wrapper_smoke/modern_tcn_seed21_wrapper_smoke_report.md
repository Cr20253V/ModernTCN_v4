# ModernTCN Wrapper Smoke Test

- seed: `21`
- pass: `1`
- tolerance: `1.0e-06`
- onnx: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21.onnx`
- reference: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn\matlab_full_testset_modern_tcn_v4_turn_focus_A_theta_head_B_seed21\modern_tcn_seed21_matlab_full_testset_outputs.mat`

| max main abs error | max turn abs error | max theta abs error |
|---:|---:|---:|
| 0 | 0 | 0 |

## Checked Windows

| index | main | turn | theta deg | main confidence | turn confidence |
|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 0 | 2.9670 | 1.0000 | 1.0000 |
| 2 | 1 | 0 | -0.0463 | 1.0000 | 0.8349 |
| 3 | 1 | 0 | -0.0804 | 1.0000 | 1.0000 |
| 16 | 1 | 0 | -0.0172 | 0.9998 | 0.9835 |
| 128 | 1 | 0 | -0.0687 | 0.9999 | 0.9909 |
| 512 | 1 | 0 | 1.1887 | 0.9910 | 1.0000 |
| 1024 | 3 | 0 | -2.6531 | 1.0000 | 1.0000 |
| 2048 | 1 | -1 | -0.1952 | 1.0000 | 0.9775 |
| 2849 | 1 | 0 | 0.9216 | 0.9992 | 1.0000 |
