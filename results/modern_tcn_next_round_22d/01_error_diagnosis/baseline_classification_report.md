# Baseline seq128 Classification Report

Frozen baseline checkpoint and current seq128 test set were used. No baseline retraining was performed.

## Main Classes

| class | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| flat | 0.908302 | 0.969577 | 0.937940 | 756 |
| stall | 0.945205 | 0.718750 | 0.816568 | 96 |
| slope | 0.984938 | 0.974909 | 0.979898 | 2750 |

## Turn Classes

| class | precision | recall | f1 | support |
|---|---:|---:|---:|---:|
| right | 0.436997 | 0.612015 | 0.509906 | 799 |
| straight | 0.750168 | 0.576306 | 0.651843 | 1933 |
| left | 0.482966 | 0.554023 | 0.516060 | 870 |

## Core Metrics

- acc_main: `0.966963`
- acc_turn: `0.578845`
- acc_turn_transition: `0.497765`
- theta_mae_deg: `0.679494`
- flat_recall: `0.969577`
- stall_recall: `0.718750`
- slope_recall: `0.974909`
