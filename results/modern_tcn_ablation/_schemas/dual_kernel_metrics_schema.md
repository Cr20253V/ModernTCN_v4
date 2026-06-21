# Dual-kernel Metrics Schema

Offline required columns: acc_main, acc_turn, acc_turn_transition, theta_mae_deg, flat_recall, stall_recall, slope_recall, theta_edge_p95_abs_err, false_turn_straight, flat_peak_theta_error.

Boundary gate aliases:
- theta_edge_p95_abs_err = max(theta_neg_10_8_p95_abs_err_deg, theta_pos_8_10_p95_abs_err_deg)
- flat_peak_theta_error = theta_flat_abs_max_deg
- false_turn_straight = ratio of true-straight turn labels predicted as left/right

Closed-loop required columns: ey_rmse, xy_rmse, theta_mae_deg, main_acc_pct, turn_acc_pct, omega_cmd_rms, j_du or delta_u proxy, rank_ey.
