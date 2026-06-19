# Stage 1 plantfix ModernTCN/GRU/TCN closed-loop comparison

- 输出文件：
  - ModernTCN: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\path_factory_logistics_showcase_theta10_v3\ModernTCN_v5_plantfix_out.mat`
  - GRU: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\path_factory_logistics_showcase_theta10_v3\GRU_v5_plantfix_out.mat`
  - TCN: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\path_factory_logistics_showcase_theta10_v3\TCN_v5_plantfix_out.mat`
  - LPV-MPC_theta0: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\path_factory_logistics_showcase_theta10_v3\lpvmpc_theta0_out.mat`
  - LPV-MPC_oracle_theta: `E:\Matlab\Simulink\S-Function_16\results\paper\agv_model_parameter_correction_workflow\09_closed_loop\path_factory_logistics_showcase_theta10_v3\lpvmpc_oracle_theta_out.mat`
- 展示路径文件：`E:\Matlab\Simulink\S-Function_16\data\paths\path_factory_logistics_showcase_theta10_v3.mat`

## 排序

排序采用名次和，数值越小越好。跟踪项包含横向/航向/速度/角速度/XY 误差；感知项包含坡度 MAE、主状态准确率和转向准确率；控制项包含控制增量、约束违规率和控制峰值。

| controller | tracking_rank_sum | perception_rank_sum | control_rank_sum | overall_rank_sum | overall_rank |
|---|---|---|---|---|---|
| ModernTCN | 6.0000 | 3.0000 | 4.0000 | 13.0000 | 1.0000 |
| GRU | 12.0000 | 6.0000 | 8.0000 | 26.0000 | 2.0000 |
| TCN | 18.0000 | 9.0000 | 12.0000 | 39.0000 | 3.0000 |
| LPV-MPC_theta0 | 24.0000 | 12.0000 | 16.0000 | 52.0000 | 4.0000 |
| LPV-MPC_oracle_theta | 30.0000 | 15.0000 | 20.0000 | 65.0000 | 5.0000 |

## 总体结果

| controller | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | xy_rmse | F_peak | omega_cmd_peak | j_du | viol_rate | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 0.2269 | 146.6837 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 0.2269 | 146.6837 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| TCN | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 0.2269 | 146.6837 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_theta0 | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 0.2269 | 146.6837 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_oracle_theta | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 0.2269 | 146.6837 | 2.686e-06 | 5.9227 | 0.0000 | NaN | 0.0000 | NaN | NaN |

## 处理用时统计

| controller | solve_time_p50_ms | solve_time_p95_ms | solve_time_p99_ms | solve_time_max_ms | timeout_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0066 | 0.0075 | 0.0077 | 0.0077 | 0.0000 |
| GRU | 0.0060 | 0.0069 | 0.0074 | 0.0075 | 0.0000 |
| TCN | 0.0060 | 0.0069 | 0.0101 | 0.0101 | 0.0000 |
| LPV-MPC_theta0 | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | NaN | NaN | NaN | NaN | NaN |

## 约束与饱和

| controller | F_sat595_pct | F_limit_hit_pct | omega_sat060_pct | omega_limit_hit_pct | viol_rate |
|---|---|---|---|---|---|
| ModernTCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| GRU | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| TCN | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| LPV-MPC_theta0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| LPV-MPC_oracle_theta | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 分区关键指标

| controller | zone | ey_rmse | ey_peak | epsi_rmse | ev_rmse | eomega_rmse | omega_cmd_peak | j_du | theta_mae_deg | theta_sched_mae_deg | main_acc_pct | turn_acc_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ModernTCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.3403 | 0.0000 | 0.0002388 | 252.2596 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| ModernTCN | receiving_aisle_right_entry | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | main_aisle_to_ramp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | extended_uphill_left_ramp_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | upper_pickup_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | slope_reversal_right_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | downhill_delivery_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | shipping_cross_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| ModernTCN | dock_approach_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | all | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | startup | 0.0000 | 0.0000 | 0.0000 | 0.3403 | 0.0000 | 0.0002388 | 252.2596 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| GRU | receiving_aisle_right_entry | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | main_aisle_to_ramp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | extended_uphill_left_ramp_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | upper_pickup_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | slope_reversal_right_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | downhill_delivery_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | shipping_cross_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| GRU | dock_approach_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | all | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| TCN | startup | 0.0000 | 0.0000 | 0.0000 | 0.3403 | 0.0000 | 0.0002388 | 252.2596 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| TCN | receiving_aisle_right_entry | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | main_aisle_to_ramp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | extended_uphill_left_ramp_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | upper_pickup_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | slope_reversal_right_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | downhill_delivery_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | shipping_cross_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| TCN | dock_approach_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | all | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 2.686e-06 | 5.9227 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_theta0 | startup | 0.0000 | 0.0000 | 0.0000 | 0.3403 | 0.0000 | 0.0002388 | 252.2596 | 0.0000 | 0.0000 | 100.0000 | 100.0000 |
| LPV-MPC_theta0 | receiving_aisle_right_entry | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | main_aisle_to_ramp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | extended_uphill_left_ramp_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | upper_pickup_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | slope_reversal_right_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | downhill_delivery_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | shipping_cross_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_theta0 | dock_approach_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | all | 0.0000 | 0.0000 | 0.0000 | 0.0610 | 0.0000 | 2.686e-06 | 5.9227 | NaN | 0.0000 | NaN | NaN |
| LPV-MPC_oracle_theta | startup | 0.0000 | 0.0000 | 0.0000 | 0.3403 | 0.0000 | 0.0002388 | 252.2596 | NaN | 0.0000 | NaN | NaN |
| LPV-MPC_oracle_theta | receiving_aisle_right_entry | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | main_aisle_to_ramp | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | extended_uphill_left_ramp_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | upper_pickup_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | slope_reversal_right_transfer | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | downhill_delivery_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | shipping_cross_aisle | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
| LPV-MPC_oracle_theta | dock_approach_straight | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN | NaN |
