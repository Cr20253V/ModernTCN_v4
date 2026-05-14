# ModernTCN-small v1 5-Seed 冻结报告

- Generated: 2026-05-02 20:41:29
- Freeze name: `ModernTCN-small v1`
- Dataset: `data/tcn/TCN_dataset_v3_transition_rich.mat`
- Seeds: `11, 21, 42, 73, 101`
- Split/scaler: 使用 MAT 文件已有 run-level split 与归一化后 X，不重划分、不重拟合。
- Deployment chain: PyTorch -> ONNX -> ONNXRuntime -> MATLAB imported dlnetwork。

## 判定结论

- `acc_main`、`flat_recall`、`slope_recall` 稳定超过最终推荐目标，说明 v1 已修复 staged TCN 的 flat/slope 主工况边界崩塌。
- `acc_turn_transition` 均值低于 0.77，未达到最终推荐目标，也低于 TCN staged baseline。
- `theta_mae_deg` 均值高于 0.43，未达到最终推荐目标，也弱于 GRU strong baseline。
- 5 个 seed 的 ONNXRuntime 与 MATLAB 一致性均通过，当前 v1 可以作为冻结的离线模型版本。

## 5-Seed 指标

| metric | mean | std | min | max | target | pass |
|---|---:|---:|---:|---:|---:|---:|
| acc_main | 0.9631 | 0.0036 | 0.9589 | 0.9670 | >= 0.9300 | 1 |
| acc_turn | 0.9068 | 0.0148 | 0.8912 | 0.9224 |  |  |
| acc_turn_pure | 0.9299 | 0.0121 | 0.9171 | 0.9466 |  |  |
| acc_turn_transition | 0.7560 | 0.0422 | 0.7109 | 0.8170 | >= 0.7700 | 0 |
| theta_mae_deg | 0.4604 | 0.1253 | 0.3132 | 0.6312 | <= 0.4300 | 0 |
| flat_recall | 0.9474 | 0.0069 | 0.9365 | 0.9547 | >= 0.9000 | 1 |
| stall_recall | 0.8615 | 0.0335 | 0.8146 | 0.8927 |  |  |
| slope_recall | 0.9911 | 0.0034 | 0.9853 | 0.9944 | >= 0.9400 | 1 |
| uphill_recall | 0.9904 | 0.0048 | 0.9828 | 0.9954 |  |  |
| downhill_recall | 0.9921 | 0.0037 | 0.9875 | 0.9964 |  |  |

## Per-Seed 指标

| seed | epoch | main | turn | turnT | theta deg | flat | stall | slope | uphill | downhill |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 37 | 0.9589 | 0.8912 | 0.7215 | 0.6312 | 0.9481 | 0.8390 | 0.9853 | 0.9828 | 0.9893 |
| 21 | 50 | 0.9670 | 0.8940 | 0.7109 | 0.4381 | 0.9514 | 0.8878 | 0.9916 | 0.9908 | 0.9929 |
| 42 | 76 | 0.9596 | 0.9224 | 0.7639 | 0.3838 | 0.9365 | 0.8732 | 0.9916 | 0.9897 | 0.9946 |
| 73 | 77 | 0.9656 | 0.9217 | 0.8170 | 0.3132 | 0.9464 | 0.8927 | 0.9923 | 0.9954 | 0.9875 |
| 101 | 56 | 0.9645 | 0.9049 | 0.7666 | 0.5354 | 0.9547 | 0.8146 | 0.9944 | 0.9931 | 0.9964 |

## Baseline 对照

| metric | ModernTCN v1 mean/std | GRU mean/std | TCN staged mean/std | TCN calibrated upper bound |
|---|---:|---:|---:|---:|
| acc_main | 0.9631 / 0.0036 | 0.9400 / 0.0050 | 0.9052 / 0.0350 | 0.9442 |
| acc_turn | 0.9068 / 0.0148 | 0.8875 / 0.0104 | 0.9063 / 0.0027 | 0.9077 |
| acc_turn_transition | 0.7560 / 0.0422 | 0.6870 / 0.0381 | 0.7830 / 0.0115 | 0.7851 |
| theta_mae_deg | 0.4604 / 0.1253 | 0.4195 / 0.0653 | 0.4490 / 0.0846 | 0.3998 |
| flat_recall | 0.9474 / 0.0069 | 0.9070 / 0.0086 | 0.8594 / 0.0523 | 0.9233 |
| stall_recall | 0.8615 / 0.0335 | 0.9161 / 0.0275 | 0.9688 / 0.0168 | 0.9756 |
| slope_recall | 0.9911 / 0.0034 | 0.9715 / 0.0066 | 0.9350 / 0.0458 | 0.9574 |
| uphill_recall | 0.9904 / 0.0048 | 0.9623 / 0.0065 | 0.9104 / 0.0511 | 0.9564 |
| downhill_recall | 0.9921 / 0.0037 | 0.9857 / 0.0079 | 0.9732 / 0.0389 | 0.9589 |

## 三方一致性

| seed | ONNXRuntime pass | MATLAB pass | MATLAB report |
|---:|---:|---:|---|
| 11 | 1 | 1 | `results\modern_tcn\transition_rich_v3_seed11\modern_tcn_seed11_matlab_consistency.md` |
| 21 | 1 | 1 | `results\modern_tcn\transition_rich_v3_seed21\modern_tcn_seed21_matlab_consistency.md` |
| 42 | 1 | 1 | `results\modern_tcn\transition_rich_v3_seed42\modern_tcn_seed42_matlab_consistency.md` |
| 73 | 1 | 1 | `results\modern_tcn\transition_rich_v3_seed73\modern_tcn_seed73_matlab_consistency.md` |
| 101 | 1 | 1 | `results\modern_tcn\transition_rich_v3_seed101\modern_tcn_seed101_matlab_consistency.md` |

## 冻结产物

- `results/modern_tcn/ModernTCN_v1_5seed_per_seed.csv`
- `results/modern_tcn/ModernTCN_v1_5seed_summary.csv`
- `results/modern_tcn/ModernTCN_v1_baseline_comparison.csv`
- `results/modern_tcn/ModernTCN_v1_freeze_manifest.json`
- `results/modern_tcn/ModernTCN_v1_5seed_report.md`

## 下一步建议

1. 保留 v1 作为冻结基线，用于论文中的 ModernTCN-small v1 对照。
2. 若继续优化，开启 ModernTCN v2，只做小范围定向修正：提高 `turn_transition_weight`、`lambda_turn` 和 `lambda_theta`，并提高选模分数中 turn-transition/theta 权重。
3. 进入 Simulink 前，先写 MATLAB 离线全 test set 推理脚本，验证标签映射、softmax 后处理和全量测试集指标与 Python 一致。
