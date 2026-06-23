# Uncertainty Seed101 Rerun Note

- run_tag: `uncertainty_seed101_rerun_20260622`
- source intent: regenerate a missing executable checkpoint for the E1 uncertainty weighting recipe.
- not a restored historical artifact: the original historical directory `uncertainty_seed101/` still has no `modern_tcn_seed101.pt`.
- training recipe: `loss_mode=uncertainty_weighting`, `seed=101`, `model_family=small`, `input_dim=22`, `seq_len=128`, `feature_contract=passive17_plus_all5`.
- checkpoint: `modern_tcn_seed101.pt`
- offline metrics match the historical `uncertainty_seed101` metrics in the nine decision metrics checked after training.

This rerun may be used as a new executable candidate for sandbox closed-loop testing, but it must not be relabeled as a restored original historical checkpoint.
