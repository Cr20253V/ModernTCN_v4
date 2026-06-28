# Probe closed-loop: path_factory_target_final_flat_release_v1

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_factory_target_final_flat_release_v1\baseline_lock_out.mat`
  - modern_fixed_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_final_flat_release_v1\modern_fixed_seed101_out.mat`
  - uncertainty_weighted_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\19_fair_10seed_selection_and_final_test_path_extension\tmp_path_probe\path_factory_target_final_flat_release_v1\uncertainty_weighted_seed101_out.mat`
- 展示路径文件：`E:/Matlab/Simulink/S-Function_16/data/paths/factory_targeted_eval/path_factory_target_final_flat_release_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 9.0000 | 4.0000 | 4.0000 | 17.0000 | 1.0000 |
| uncertainty_weighted_seed101 | 11.0000 | 6.0000 | 10.0000 | 27.0000 | 2.0000 |
| modern_fixed_seed101 | 16.0000 | 8.0000 | 10.0000 | 34.0000 | 3.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0346 | 0.0627 | 0.0398 | 0.0366 | 0.0128 | 0.7606 | 162.9948 | 0.1452 | 1.5223 | 0.0000 | 0.6102 | 0.6636 | 93.9004 | 57.7431 |
| modern_fixed_seed101 | 0.0505 | 0.0881 | 0.0465 | 0.0411 | 0.0099 | 0.7785 | 181.5223 | 0.9730 | 2.0816 | 0.0000 | 0.6912 | 0.6899 | 69.8068 | 51.4741 |
| uncertainty_weighted_seed101 | 0.0410 | 0.0816 | 0.0409 | 0.0366 | 0.0105 | 0.6956 | 169.7014 | 0.9711 | 3.2312 | 0.0000 | 0.5835 | 0.6146 | 82.3450 | 30.6676 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0278 | 0.0469 | 0.0543 | 0.3258 | 0.0000 |
| modern_fixed_seed101 | 0.0209 | 0.0227 | 0.0239 | 0.2440 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0210 | 0.0228 | 0.0245 | 0.2512 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| modern_fixed_seed101 | 0.0000 | 0.0000 | 0.3389 | 0.0000 | 0.0000 |
| uncertainty_weighted_seed101 | 0.0000 | 0.0000 | 0.2372 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0346 | 0.0627 | 0.0398 | 0.0366 | 0.0128 | 0.1452 | 1.5223 | 0.6102 | 0.6636 | 93.9004 | 57.7431 |
| ModernTCN | all | 0.0343 | 0.0627 | 0.0395 | 0.0738 | 0.0126 | 0.1452 | 10.4289 | 0.6004 | 0.6529 | 94.0000 | 58.4333 |
| modern_fixed_seed101 | all | 0.0505 | 0.0881 | 0.0465 | 0.0411 | 0.0099 | 0.9730 | 2.0816 | 0.6912 | 0.6899 | 69.8068 | 51.4741 |
| modern_fixed_seed101 | all | 0.0501 | 0.0881 | 0.0461 | 0.0761 | 0.0098 | 0.9730 | 10.9791 | 0.6800 | 0.6787 | 70.3333 | 52.2667 |
| uncertainty_weighted_seed101 | all | 0.0410 | 0.0816 | 0.0409 | 0.0366 | 0.0105 | 0.9711 | 3.2312 | 0.5835 | 0.6146 | 82.3450 | 30.6676 |
| uncertainty_weighted_seed101 | all | 0.0407 | 0.0816 | 0.0406 | 0.0738 | 0.0104 | 0.9711 | 12.1100 | 0.5740 | 0.6046 | 82.6333 | 31.8333 |
