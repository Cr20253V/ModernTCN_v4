# D6 Formal Single-seed Gate

- run_tag: `full128_light_seed21`
- pass: `0`
- summary: `results/modern_tcn_ablation/exp3_patch_full/full128_light_seed21/modern_tcn_full_seed21_summary.csv`
- initialization: `random initialization; no checkpoint load path is present in train_modern_tcn.py formal training args`
- acc_main: `0.9508606329816769`
- acc_turn: `0.5577456968350916`
- acc_turn_transition: `0.43219076005961254`
- theta_mae_deg: `2.198178768157959`
- stall_recall: `0.65625`

## Failures

- theta_mae_deg 2.19818 <= 1.2 failed
