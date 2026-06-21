# exp3 patch_full rescue

本目录只保存 `exp3_patch_full` 在 D6 失败后的单 seed 挽救试验。

硬边界：

- 只使用 22D plantfix dataset：`data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat`
- 不读取旧 ModernTCNFull / weakcombo / stage2 结果作为证据。
- 所有 run 从随机初始化开始，不 warm-start，不 fine-tune。
- 不导出 ONNX，不运行 MATLAB/Simulink，不写入 closed-loop compare。
- 若单 seed 未达到 D6 基本门槛，不进入 9-run。

Rescue 顺序：

1. `full128_light_theta_select_seed21`: 只增强 selection score 的 theta/edge/flat peak 权重。
2. `full128_light_theta_loss_seed21`: 增强 theta loss 和负坡权重。
3. `full128_densepatch_theta_select_seed21`: 使用 dense patch，同时增强 selection score。
4. `full128_densepatch_theta_loss_seed21`: 仅当前三个方向仍有希望但未过 gate 时执行。
