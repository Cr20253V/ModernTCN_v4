# D1 Model API Report

- pass: `1`
- model_family: `small_dualkernel`
- config_class: `ModernTCNDualKernelConfig`
- block_class: `ModernTCNDualKernelBlock`
- model_class: `ModernTCNDualKernelSmall`
- input_shape: `[2,128,22]`
- output_shapes: `[(2,3),(2,3),(2,1)]`
- large_branch: `depthwise Conv1d, groups=channels, same padding`
- small_branch: `depthwise Conv1d, groups=channels, same padding`
- temporal_merge: `(large_branch(x) + small_branch(x)) * dual_branch_scale`
- dual_branch_scale_default: `0.5`
- small_branch_init_default: `default`
- shared_temporal_bn: `1`
- layer_scale_init_default: `1e-2`
- baseline_small_regression: `pass`

No changes were made to the default `ModernTCNSmall` block construction.
