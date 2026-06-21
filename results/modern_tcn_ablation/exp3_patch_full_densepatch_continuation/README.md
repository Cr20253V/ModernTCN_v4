# exp3 patch_full densepatch continuation

本目录保存 `exp3_patch_full_rescue` 之后的窄范围 densepatch-only continuation。

硬边界：

- 只使用 22D plantfix dataset：`data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 只测试 `patch_size=8, patch_stride=2, dims=16,32, stage_blocks=1,1`。
- 所有 run 从随机初始化开始，不 warm-start，不 fine-tune。
- 不导出 ONNX，不运行 MATLAB/Simulink，不写 closed-loop 或 compare 目录。
- 所有输出必须在本目录下，使用 `--no_overwrite`。

执行策略：

1. C1 先跑 seed21：在 R3 `densepatch + selector-only` 基础上只加入 `select_stall_weight`，目标是在保住 transition/theta/edge 的同时改善 stall。
2. C1 若仍明显不过 gate，则停止，不扩 seed。
3. C1 若接近或通过 gate，再扩展 seed42/101 做稳定性检查。
