# E2/E5 Repair Final Report

- generated_at: 2026-06-22T01:32:31
- repair_status: `PASS_CONTRACT_LIMITED`
- metric_rebuild_can_continue: True
- dataset_file: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`

## Answers

1. Current data supports continuous replay: False.
2. Original E2 is not full focal + smoothness because theta smoothness was disabled by contract; allowed use is focal-only.
3. Original E5 cannot enter formal control-oriented ranking because every scheduled metric depends on previous scheduled state and the old replay order is not auditable.
4. test_replay_manifest generated with rows: 0.
5. Baseline replay status: `not_run`.
6. E5 replay-fixed status: `not_run_contract_limited`.
7. E2 smooth-fixed status: `not_run_contract_limited`.
8. Candidates allowed into metric rebuild are governed by invalid_evidence_registry.csv.
9. Original E5 scheduled evidence is advisory_only; original E2 smoothness evidence is invalid/not_run.

## Metadata Levels

```json
{
  "train": "level0_invalid",
  "val": "level0_invalid",
  "test": "level0_invalid"
}
```

## Decision

```json
{
  "repair_status": "PASS_CONTRACT_LIMITED",
  "manifest_available": false,
  "reason": "current dataset does not expose auditable test replay continuity metadata",
  "test_metadata_level": "level0_invalid",
  "metric_rebuild_can_continue": true,
  "e5_replay_fixed_status": "not_run_contract_limited",
  "e2_smooth_fixed_status": "not_run_contract_limited"
}
```
