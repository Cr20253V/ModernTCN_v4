# Uncertainty tuning Top5: path_closed_loop_sharp_turn_transition_theta10_v1

- 输出文件：
  - baseline_lock: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\05_sandbox_closed_loop_if_needed\03_formal_validation\path_closed_loop_sharp_turn_transition_theta10_v1\baseline_lock_out.mat`
  - u06_lr0013_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\u06_lr0013_seed101_out.mat`
  - u04_lwlr0030_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\u04_lwlr0030_seed101_out.mat`
  - u17_ltheta050_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\u17_ltheta050_seed101_out.mat`
  - u23_turn_protect_mix_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\u23_turn_protect_mix_seed101_out.mat`
  - u18_ltheta065_seed101: `E:\Matlab\Simulink\S-Function_16\results\modern_tcn_metric_rebuild\11_uncertainty_tuning\04_closed_loop_top5\01_closed_loop_runs\path_closed_loop_sharp_turn_transition_theta10_v1\u18_ltheta065_seed101_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_closed_loop_sharp_turn_transition_theta10_v1.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| u23_turn_protect_mix_seed101 | 11.0000 | 14.0000 | 10.0000 | 35.0000 | 1.0000 |
| u17_ltheta050_seed101 | 16.0000 | 10.0000 | 12.0000 | 38.0000 | 2.0000 |
| u18_ltheta065_seed101 | 14.0000 | 12.0000 | 18.0000 | 44.0000 | 3.0000 |
| u04_lwlr0030_seed101 | 24.0000 | 9.0000 | 13.0000 | 46.0000 | 4.0000 |
| u06_lr0013_seed101 | 30.0000 | 8.0000 | 16.0000 | 54.0000 | 5.0000 |
| baseline_lock | 31.0000 | 10.0000 | 15.0000 | 56.0000 | 6.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 0.5137 | 224.7044 | 1.3509 | 5.3237 | 0.0000 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| u06_lr0013_seed101 | 0.0459 | 0.1252 | 0.0507 | 0.0323 | 0.0277 | 0.6359 | 228.6977 | 1.3646 | 2.6240 | 0.0000 | 0.5326 | 0.6487 | 95.4378 | 46.5347 |
| u04_lwlr0030_seed101 | 0.0319 | 0.0818 | 0.0311 | 0.0385 | 0.0192 | 0.3863 | 226.3172 | 0.1601 | 3.5246 | 0.0000 | 0.5616 | 0.6866 | 91.3221 | 55.8144 |
| u17_ltheta050_seed101 | 0.0337 | 0.0846 | 0.0266 | 0.0347 | 0.0139 | 0.3136 | 222.9726 | 0.1835 | 2.8513 | 0.0000 | 0.6150 | 0.7123 | 91.5550 | 65.3659 |
| u23_turn_protect_mix_seed101 | 0.0255 | 0.0521 | 0.0283 | 0.0356 | 0.0167 | 0.3089 | 221.8494 | 0.3068 | 2.2806 | 0.0000 | 0.6024 | 0.7725 | 90.6426 | 53.9701 |
| u18_ltheta065_seed101 | 0.0277 | 0.0588 | 0.0304 | 0.0332 | 0.0175 | 0.3091 | 230.1017 | 0.3976 | 2.5352 | 0.0000 | 0.6026 | 0.7147 | 91.3415 | 55.4261 |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0209 | 0.0226 | 0.0239 | 0.2452 | 0.0000 |
| u06_lr0013_seed101 | 0.0214 | 0.0236 | 0.0318 | 0.2499 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0214 | 0.0240 | 0.0323 | 0.2769 | 0.0000 |
| u17_ltheta050_seed101 | 0.0213 | 0.0244 | 0.0331 | 0.2622 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0214 | 0.0243 | 0.0332 | 0.2661 | 0.0000 |
| u18_ltheta065_seed101 | 0.0214 | 0.0241 | 0.0319 | 0.2471 | 0.0000 |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| baseline_lock | 0.0000 | 0.0000 | 0.0777 | 0.0000 | 0.0000 |
| u06_lr0013_seed101 | 0.0000 | 0.0000 | 0.0582 | 0.0000 | 0.0000 |
| u04_lwlr0030_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u17_ltheta050_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u23_turn_protect_mix_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| u18_ltheta065_seed101 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline_lock | all | 0.0406 | 0.1269 | 0.0416 | 0.0356 | 0.0219 | 1.3509 | 5.3237 | 0.6002 | 0.7126 | 94.1371 | 48.8449 |
| baseline_lock | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| baseline_lock | uphill_left_transition | 0.0371 | 0.0676 | 0.0542 | 0.0372 | 0.0259 | 0.1441 | 0.9621 | 0.5676 | 0.7060 | 93.9444 | 63.6111 |
| baseline_lock | downhill_right_transition | 0.0200 | 0.0391 | 0.0304 | 0.0299 | 0.0229 | 0.1301 | 3.4855 | 0.5232 | 0.6685 | 96.6000 | 36.9500 |
| baseline_lock | flat_left_exit | 0.0722 | 0.1269 | 0.0421 | 0.0451 | 0.0147 | 1.3509 | 18.4221 | 1.0234 | 1.0628 | 87.5000 | 28.2000 |
| u06_lr0013_seed101 | all | 0.0459 | 0.1252 | 0.0507 | 0.0323 | 0.0277 | 1.3646 | 2.6240 | 0.5326 | 0.6487 | 95.4378 | 46.5347 |
| u06_lr0013_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u06_lr0013_seed101 | uphill_left_transition | 0.0440 | 0.0763 | 0.0634 | 0.0444 | 0.0309 | 0.1771 | 0.6618 | 0.8289 | 0.9165 | 95.2778 | 56.0556 |
| u06_lr0013_seed101 | downhill_right_transition | 0.0319 | 0.0525 | 0.0445 | 0.0254 | 0.0285 | 0.1788 | 3.3205 | 0.4633 | 0.6430 | 97.2000 | 39.2000 |
| u06_lr0013_seed101 | flat_left_exit | 0.0732 | 0.1252 | 0.0451 | 0.0183 | 0.0247 | 1.3646 | 5.3753 | 0.3245 | 0.4059 | 90.6000 | 25.4000 |
| u04_lwlr0030_seed101 | all | 0.0319 | 0.0818 | 0.0311 | 0.0385 | 0.0192 | 0.1601 | 3.5246 | 0.5616 | 0.6866 | 91.3221 | 55.8144 |
| u04_lwlr0030_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u04_lwlr0030_seed101 | uphill_left_transition | 0.0281 | 0.0535 | 0.0459 | 0.0408 | 0.0218 | 0.1423 | 0.8343 | 0.6359 | 0.7291 | 92.8889 | 72.3889 |
| u04_lwlr0030_seed101 | downhill_right_transition | 0.0160 | 0.0322 | 0.0168 | 0.0341 | 0.0197 | 0.1601 | 7.5115 | 0.4721 | 0.6242 | 98.0500 | 40.3000 |
| u04_lwlr0030_seed101 | flat_left_exit | 0.0575 | 0.0818 | 0.0253 | 0.0461 | 0.0163 | 0.1523 | 1.3219 | 0.8043 | 0.9757 | 72.0000 | 41.6000 |
| u17_ltheta050_seed101 | all | 0.0337 | 0.0846 | 0.0266 | 0.0347 | 0.0139 | 0.1835 | 2.8513 | 0.6150 | 0.7123 | 91.5550 | 65.3659 |
| u17_ltheta050_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u17_ltheta050_seed101 | uphill_left_transition | 0.0264 | 0.0541 | 0.0413 | 0.0422 | 0.0185 | 0.1548 | 0.6819 | 0.8349 | 0.9457 | 95.1111 | 71.3333 |
| u17_ltheta050_seed101 | downhill_right_transition | 0.0217 | 0.0478 | 0.0137 | 0.0344 | 0.0132 | 0.1835 | 5.8695 | 0.6432 | 0.7624 | 95.1000 | 60.1500 |
| u17_ltheta050_seed101 | flat_left_exit | 0.0606 | 0.0846 | 0.0140 | 0.0208 | 0.0060 | 0.1452 | 1.4108 | 0.3788 | 0.4418 | 75.1000 | 53.0000 |
| u23_turn_protect_mix_seed101 | all | 0.0255 | 0.0521 | 0.0283 | 0.0356 | 0.0167 | 0.3068 | 2.2806 | 0.6024 | 0.7725 | 90.6426 | 53.9701 |
| u23_turn_protect_mix_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u23_turn_protect_mix_seed101 | uphill_left_transition | 0.0264 | 0.0520 | 0.0428 | 0.0369 | 0.0199 | 0.1449 | 1.3529 | 0.6192 | 0.8399 | 93.8333 | 69.7778 |
| u23_turn_protect_mix_seed101 | downhill_right_transition | 0.0181 | 0.0360 | 0.0184 | 0.0356 | 0.0162 | 0.1757 | 3.8580 | 0.6662 | 0.8243 | 95.2500 | 40.2500 |
| u23_turn_protect_mix_seed101 | flat_left_exit | 0.0379 | 0.0521 | 0.0124 | 0.0364 | 0.0138 | 0.3068 | 1.2861 | 0.6562 | 0.8184 | 72.4000 | 36.9000 |
| u18_ltheta065_seed101 | all | 0.0277 | 0.0588 | 0.0304 | 0.0332 | 0.0175 | 0.3976 | 2.5352 | 0.6026 | 0.7147 | 91.3415 | 55.4261 |
| u18_ltheta065_seed101 | startup | 0.0000 | 0.0000 | 0.0000 | 0.1753 | 0.0000 | 0.0002457 | 66.3593 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| u18_ltheta065_seed101 | uphill_left_transition | 0.0294 | 0.0588 | 0.0455 | 0.0410 | 0.0204 | 0.2103 | 1.2739 | 0.8172 | 0.9439 | 94.0556 | 70.5556 |
| u18_ltheta065_seed101 | downhill_right_transition | 0.0239 | 0.0497 | 0.0200 | 0.0325 | 0.0159 | 0.1962 | 4.6062 | 0.6195 | 0.7674 | 96.0500 | 36.9000 |
| u18_ltheta065_seed101 | flat_left_exit | 0.0355 | 0.0561 | 0.0154 | 0.0185 | 0.0179 | 0.3976 | 1.2436 | 0.3938 | 0.4478 | 74.0000 | 49.7000 |
