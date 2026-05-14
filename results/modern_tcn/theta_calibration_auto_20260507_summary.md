# ModernTCN theta 校准自动化总结

## 最优候选

- run_tag: `modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21`
- seed: `21`
- 训练方式: `theta_head + --unfreeze-last-block`
- 权重: `theta_neg_weight=1.0`, `theta_pos_weight=1.0`
- loss: `lambda_theta=1.0`, `lambda_theta_flat=1.0`, `lambda_theta_near_flat=2.0`
- 已将 `src/ModernTCN/ModernTCN_default_config.m` 默认 run_tag 切到该候选。

## 关键结果

| 项目 | 当前版本 | 最优候选 |
|---|---:|---:|
| full-test theta MAE (deg) | 0.4868 | 0.4185 |
| full-test +6~+8 MAE (deg) | 1.1907 | 0.8249 |
| full-test -8~-6 MAE (deg) | 0.6535 | 0.5423 |
| test scatter R2 identity | 0.9712 | 0.9780 |
| sweep all MAE (deg) | 0.7721 | 0.5952 |
| sweep all RMSE (deg) | 1.0647 | 0.8515 |
| sweep all R2 identity | 0.9663 | 0.9785 |
| sweep \|theta\|<=8 MAE (deg) | n/a | 0.4657 |
| sweep \|theta\|<=8 P95 abs error (deg) | n/a | 1.0994 |

## 闭环对比

| controller | ey_rmse | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | j_du | theta_mae_deg | main_acc_pct | turn_acc_pct |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ModernTCN candidate | 0.0170 | 0.0417 | 0.0403 | 0.0106 | 0.7901 | 1.1890 | 0.6167 | 96.7133 | 80.8200 |
| GRU frozen | 0.0231 | 0.2063 | 0.0680 | 0.0201 | 3.3648 | 2.2471 | 0.4082 | 95.0643 | 76.9929 |

ModernTCN 候选在闭环跟踪、控制平滑性和分类准确率上继续优于冻结 GRU。相比当前冻结 ModernTCN 报告，`epsi_rmse`、`xy_rmse`、`j_du`、闭环 `theta_mae_deg` 也下降。

## 输出路径

- checkpoint: `results/modern_tcn/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/modern_tcn_seed21.pt`
- ONNX: `results/modern_tcn/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/modern_tcn_seed21.onnx`
- ONNXRuntime consistency: `results/modern_tcn/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/modern_tcn_seed21_onnxruntime_consistency.md`
- MATLAB full-test report: `results/modern_tcn/matlab_full_testset_modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/ModernTCN_v1_matlab_full_testset_report.md`
- test scatter: `results/paper/modern_tcn_theta_scatter/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/modern_tcn_theta_scatter.png`
- sweep full-range report: `results/paper/modern_tcn_theta_sweep_plot/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21/modern_tcn_theta_sweep_report.md`
- sweep ±8 paper figure: `results/paper/modern_tcn_theta_sweep_plot/modern_tcn_theta_calib_uflast_w1p0_lam100_f100_nf200_seed21_pm8/modern_tcn_theta_sweep_scatter.png`
- closed-loop report: `results/compare/modern_tcn_gru_closed_loop/modern_tcn_gru_closed_loop_theta_calib_uflast_report.md`
