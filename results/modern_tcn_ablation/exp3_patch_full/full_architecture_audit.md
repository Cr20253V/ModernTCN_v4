# D1 ModernTCNFull Architecture Audit

- pass: `1`
- source: `src/ModernTCN/modern_tcn_model.py`
- initialization: `random initialization only; no checkpoint load in training path`

| config | tokens | dims | stage_blocks | large_kernels | small_kernels | ffn_ratio | layer_scale | params |
|---|---:|---|---|---|---|---:|---:|---:|
| `full128_light` | 29 | `8,16` | `1,1` | `15,9` | `5,3` | 2 | 0.01 | 171223 |
| `full128_mid` | 29 | `16,32` | `1,1` | `15,9` | `5,3` | 2 | 0.01 | 391279 |
| `full128_densepatch` | 61 | `16,32` | `1,1` | `15,9` | `5,3` | 2 | 0.01 | 391151 |
