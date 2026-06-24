# Multi-seed Algorithm Comparison under Current v2 Metrics

## 结论

1. 当前同 contract 离线多 seed 可比集合不是完全一致的 `21/42/101`：
   - `ModernTCN_small_base`: seed `21/73/101`
   - `Uncertainty_weighted_ModernTCN_small`: seed `21/42/101`
   - `GRU_plantfix`: seed `21/73/101`
2. 按 v2 offline hard gate，完整可判定 pass 的是 `ModernTCN_small_base` 的 1/3、当前 `ModernTCN_small_champion_baseline` 的 reference pass、以及 `Uncertainty_weighted_ModernTCN_small` 的 1/3。`GRU_plantfix` 因训练报告缺少 `flat_peak_theta_error`，不能被判为 full offline pass；其中 seed21/73 还额外存在硬保护失败。
3. 当前已有三路径闭环 v2 结果中，最佳仍是 `uncertainty_seed101_rerun_20260622`，`J_control_current_v2=0.944117`；当前 frozen ModernTCN_small baseline 为 `J=1.0`。
4. 多 seed 稳定性角度，Uncertainty 还不能直接替代 ModernTCN_small：seed21/42 离线分别因 flat peak / edge theta 失败，闭环 J 也显著波动。更合理的定位仍是 seed101 anchor / paper innovation candidate，而不是 full replacement baseline。
5. GRU 的离线主任务表现不差，但当前闭环 seed101 的路径跟踪和控制代价远差于 ModernTCN_small / Uncertainty；并且缺少 plantfix 多 seed 闭环，所以不能作为当前最优。

## Offline v2 summary

| algorithm_group | seeds_available | offline_pass_count | offline_fail_count | offline_unavailable_count | best_seed_by_offline_score | best_offline_score_vs_baseline | median_offline_score_vs_baseline |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Uncertainty_weighted_ModernTCN_small | 21/42/101 | 1 | 2 | 0 | 101 | 0.970838817749306 | 1.07901896581399 |
| ModernTCN_small_base | 21/73/101 | 1 | 2 | 0 | 101 | 1.00914528585944 | 1.05146783283019 |
| GRU_plantfix | 21/73/101 | 0 | 2 | 1 | 101 | 1.06858365938923 | 1.10872679128676 |

## Offline seed-level details

| algorithm_group | variant_id | seed | offline_v2_status | hard_gate_failures | hard_gate_unavailable | offline_score_vs_baseline | acc_main | stall_recall | slope_recall | theta_edge_p95_abs_err | flat_peak_theta_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ModernTCN_small_base | plantfix_passive17_plus_all5_seed21 | 21 | fail | theta_edge_p95_abs_err_ratio=1.21467>1.05;flat_peak_theta_error_ratio=1.24187>1.15 | none | 1.08138457217925 | 0.972515269294836 | 0.697916666666667 | 0.986181818181818 | 3.34648656845093 | 6.62629556655884 |
| ModernTCN_small_base | plantfix_passive17_plus_all5_seed73 | 73 | fail | flat_peak_theta_error_ratio=1.17885>1.15 | none | 1.05146783283019 | 0.965019433647973 | 0.625 | 0.978909090909091 | 2.83646965026855 | 6.2900538444519 |
| ModernTCN_small_base | plantfix_passive17_plus_all5_seed101 | 101 | pass | none | none | 1.00914528585944 | 0.961132704053304 | 0.697916666666667 | 0.979636363636364 | 2.55618762969971 | 5.6189980506897 |
| ModernTCN_small_champion_baseline | turn_l020_tt25_tcm14_stw055_slrw060_seed101 | 101 | pass | reference | none | 1 | 0.966962798445308 | 0.71875 | 0.974909090909091 | 2.75505685806274 | 5.3357400894165 |
| Uncertainty_weighted_ModernTCN_small | uncertainty_anchor_same_recipe_seed21 | 21 | fail | flat_peak_theta_error_ratio=1.3324>1.15 | none | 1.09351261643159 | 0.960022209883398 | 0.6875 | 0.976727272727273 | 2.43688559532166 | 7.10931348800659 |
| Uncertainty_weighted_ModernTCN_small | uncertainty_anchor_same_recipe_seed42 | 42 | fail | theta_edge_p95_abs_err_ratio=1.24186>1.05 | none | 1.07901896581399 | 0.967240421987785 | 0.697916666666667 | 0.984 | 3.42140817642212 | 5.89323759078979 |
| Uncertainty_weighted_ModernTCN_small | uncertainty_seed101_rerun_20260622 | 101 | pass | none | none | 0.970838817749306 | 0.967518045530261 | 0.697916666666667 | 0.979272727272727 | 2.27067041397095 | 5.24426937103271 |
| GRU_plantfix | full_gru_v5_plantfix_passive17_plus_all5_seed21 | 21 | fail | stall_recall_drop=0.11455>0.1;theta_edge_p95_abs_err_ratio=1.2337>1.05 | flat_peak_theta_error | 1.10872679128676 | 0.9581 | 0.6042 | 0.9705 | 3.3989 | NaN |
| GRU_plantfix | full_gru_v5_plantfix_passive17_plus_all5_seed73 | 73 | fail | theta_edge_p95_abs_err_ratio=1.90493>1.05 | flat_peak_theta_error | 1.22191425694843 | 0.9589 | 0.6771 | 0.9749 | 5.2482 | NaN |
| GRU_plantfix | full_gru_v5_plantfix_passive17_plus_all5_seed101 | 101 | unavailable | none | flat_peak_theta_error | 1.06858365938923 | 0.9603 | 0.6354 | 0.9811 | 2.6859 | NaN |

## Current closed-loop v2 results

| algorithm_group | variant_id | seed | J_control_current_v2 | closed_loop_v2_status | closed_loop_v2_failures | ey_rmse_mean | xy_rmse_mean | epsi_rmse_mean | j_du_mean | omega_cmd_rms_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Uncertainty_weighted_ModernTCN_small | uncertainty_seed101_rerun_20260622 | 101 | 0.94411711953914 | pass | none | 0.0296269727303799 | 0.553890709479584 | 0.0379209992142139 | 4.68786764219691 | 0.0710415972600494 |
| ModernTCN_small_champion_baseline | turn_l020_tt25_tcm14_stw055_slrw060_seed101 | 101 | 1 | pass | reference | 0.0340541598964198 | 0.600747319384481 | 0.0395281150431306 | 4.73336252454802 | 0.0725761346213963 |
| Uncertainty_weighted_ModernTCN_small | uncertainty_anchor_same_recipe_seed21 | 21 | 1.13638158707013 | pass | none | 0.0465832825836547 | 0.55813879940855 | 0.047221060932995 | 5.29839329683462 | 0.0777235748578882 |
| Uncertainty_weighted_ModernTCN_small | uncertainty_anchor_same_recipe_seed42 | 42 | 11.9154967909798 | pass | none | 0.256449583915538 | 3.66591952530886 | 0.116475958937402 | 187.59045166008 | 0.244318660915203 |
| GRU_plantfix | full_gru_v5_plantfix_passive17_plus_all5_seed101 | 101 | 14.2610395101703 | pass | none | 0.705279721691159 | 1.90536420591849 | 0.148761770616854 | 183.81009723165 | 0.350302402102523 |

## Historical ModernTCN turn-champion multi-seed closed-loop

这个表只用于理解 ModernTCN turn champion 的历史 seed 波动。它以同一文件中的 `ModernTCN_turn_seed101_champion` 为 local reference，不和 current v2 `J_control` 混排。

| controller | seed | J_control_vs_historical_champion | ey_rmse_mean | xy_rmse_mean | epsi_rmse_mean | j_du_mean | omega_cmd_rms_mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ModernTCN_turn_seed101_champion | 101 | 1 | 0.0293881212343404 | 0.599794482657117 | 0.0385927891357143 | 3.6807764852036 | 0.0713431735945118 |
| ModernTCN_turn_seed303_multiseed | 303 | 1.27952447294865 | 0.0294623008936542 | 0.628339829047264 | 0.0434454082417661 | 8.12496026717823 | 0.0723679088180799 |
| ModernTCN_turn_seed101_multiseed | 101 | 1.29370208815488 | 0.040415590389661 | 0.527667871849468 | 0.0381920343266275 | 7.68622455854488 | 0.081024719017315 |
| ModernTCN_turn_seed202_multiseed | 202 | 19.3899854482782 | 0.25128876728378 | 3.66289036789894 | 0.110479510804208 | 279.339923361196 | 0.252415961793254 |

## Legacy GRU theta10_v2 evidence

旧 `GRU_theta10_v2` 确实有 seed `21/42/73/101`，但它不是当前 plantfix passive17_plus_all5 contract，因此只记录为 excluded evidence，不能和当前 baseline / uncertainty 正式排名。

| algorithm_group | case_name | seed | acc_main | acc_turn | theta_mae_deg | theta_edge_p95_abs_err | official_use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRU_theta10_v2_legacy | inputstats_hidden96_l2 | 21 | 0.971872488615055 | 0.756763996785427 | 0.534570988629751 | 1.75040653856066 | excluded_old_contract |
| GRU_theta10_v2_legacy | inputstats_hidden96_l2 | 42 | 0.975087061344763 | 0.764532547548888 | 0.321725410608268 | 1.00929924531197 | excluded_old_contract |
| GRU_theta10_v2_legacy | inputstats_hidden96_l2 | 73 | 0.979641039378516 | 0.775783552102866 | 0.277451756346473 | 0.657308262764836 | excluded_old_contract |
| GRU_theta10_v2_legacy | inputstats_hidden96_l2 | 101 | 0.976694347709617 | 0.768015001339405 | 0.260056371896385 | 0.723894671913472 | excluded_old_contract |

## Output files

- Evidence inventory: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/00_evidence_inventory/evidence_inventory.csv`
- Parameter table: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/00_evidence_inventory/algorithm_parameter_table.csv`
- Offline seed-level comparison: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/01_offline_v2/multiseed_offline_v2.csv`
- Offline algorithm summary: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/01_offline_v2/algorithm_offline_summary.csv`
- Current closed-loop v2 comparison: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/02_closed_loop_v2/current_closed_loop_v2_existing.csv`
- Historical ModernTCN multiseed closed-loop: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/02_closed_loop_v2/historical_modern_tcn_multiseed_closed_loop.csv`
- Report: `results/modern_tcn_metric_rebuild/13_multiseed_algorithm_comparison/03_report/multiseed_algorithm_comparison_report.md`

## Method notes

- 缺失值没有用 0 或 baseline 回填。
- `flat_peak_theta_error` 对 GRU plantfix 报告不可用，因此 GRU full offline hard pass 只能是 `unavailable` 或 `fail`，不能强行 pass。
- Current v2 `J_control` 采用 `ey_rmse / xy_rmse / epsi_rmse / j_du / omega_cmd_rms` 相对 baseline 的平均比值；越低越好。
- Historical ModernTCN multiseed 闭环是独立历史证据，避免和 current v2 strict validation 混排。
