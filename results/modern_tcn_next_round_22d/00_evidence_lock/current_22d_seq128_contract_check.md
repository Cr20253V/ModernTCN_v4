# Current 22D seq128 Contract Check

- generated_at: `2026-06-21 13:15:17`
- status: `PASS`
- dataset: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- contract_json: `data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5_contract.json`

| field | expected | observed |
|---|---:|---:|
| input_dim | 22 | 22 |
| seq_len | 128 | 128 |
| feature_contract | passive17_plus_all5 | passive17_plus_all5 |
| plant_revision | agv_physics_v2_plantfix | agv_physics_v2_plantfix |
| horizon_steps | 0 | 0 |
| label_time_policy | current_window_end | current_window_end |

The frozen seq128 baseline contract is valid for Phase 1 diagnosis.
