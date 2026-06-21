# seq256 Builder Policy Audit

- generated_at: `2026-06-21 13:18:00`
- builder: `src/ModernTCN/run_next_round_22d_phase0_2.py`
- source raw data: `data/tcn/ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- baseline split source: `data/tcn/ModernTCN_shared_run_split_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- MATLAB/Simulink execution: `not used`

## Policy Status

- Reused the baseline run-level train/val/test IDs.
- Reused the documented window-start policy from `TCN_prepare_dataset.m`: steady stride, transition stride, transition context, current-window-end labels.
- Reimplemented documented split-level balancing order: theta balance, turn balance, theta rebalance, then split-local shuffle.
- Fitted the scaler on seq256 train windows only and applied it to val/test.
- Preserved `input_dim=22`, `feature_contract=passive17_plus_all5`, `horizon_steps=0`, and `label_time_policy=current_window_end`.

## Parity Boundary

A seq128 reconstruction check using the Python builder does not exactly reproduce the historical MATLAB dataset after split-level balancing. The residual differences are small but nonzero:

- train windows: Python `16550` vs baseline `16529`
- val windows: Python `3695` vs baseline `3695`
- test windows: Python `3602` vs baseline `3602`
- class/count differences remain in train and turn labels for val/test.

Likely cause: MATLAB `rng(..., 'twister')` / `randperm` selection order during split-level balancing is not bit-identical to NumPy RNG, even though the policy and seed offsets are mirrored.

## Decision

The seq256 dataset is accepted for Phase 2 validation as a Python-built dataset that reuses the baseline run split and documented preparation policy. It should not be described as a byte- or row-identical MATLAB `TCN_prepare_dataset.m` reproduction. Before paper-critical seq256 claims, either run the MATLAB builder with `reuse_split_file=true` in a separate approved node or keep this audit attached to the experiment evidence.
