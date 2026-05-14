# ModernTCN 当前训练数据说明

本说明用于冻结当前 ModernTCN 使用的数据链路，避免 `data/tcn` 目录里多个历史数据集混在一起后误用。

## 当前权威数据集

当前 ModernTCN 默认使用：

- 窗口化数据集：`data/tcn/TCN_dataset_v3_transition_rich_clean_turn_aug.mat`
- scaler：`data/tcn/TCN_scaler_v3_transition_rich_clean_turn_aug.mat`
- run-level split：`data/tcn/TCN_GRU_shared_run_split_v3_transition_rich_clean_turn_aug.mat`
- 路径清单：`data/paths/path_train_tcn_v3_manifest.csv`
- 机器可读清单：`data/tcn/CURRENT_ModernTCN_DATASET.json`

当前冻结模型：

- `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.onnx`
- `results/modern_tcn/transition_rich_v3_theta_head_E_online_aug_seed73/modern_tcn_seed73.pt`

## V4 主训练集入口

V4 industrial 是下一轮 ModernTCN 主训练集入口，目前作为候选训练链路，不替换上面的 V3 冻结数据集。它把 clean-turn 样本直接放进路径生成阶段，不再额外维护一份 clean-turn 增强母集。

简化后的链路为：

```text
data/paths/path_modern_tcn_v4_*.mat
-> data/tcn/ModernTCN_train_data_v4_industrial.mat
-> data/tcn/ModernTCN_dataset_v4_industrial.mat
```

对应脚本：

- 路径生成：`src/paths/gen_modern_tcn_paths_v4_industrial.m`
- 一键构建入口：`src/ModernTCN/build_modern_tcn_dataset_v4_industrial.m`

主训练集覆盖范围：

- 速度：`0.8, 0.9, 1.0, 1.1 m/s`
- 平地 clean-turn 半径：`6-12 m`，左右方向成对生成
- 直线坡度：`-8:-1, 1:8 deg`
- 坡度-转弯重叠：entry、middle、exit 三类，坡度 `±3-±6 deg`
- 结构样本：平地 S 弯、坡度反转 S 弯

预期路径数量约为 `188` 条；完整连续仿真默认每条路径 `4` 次，因此会生成约 `752` 条 run。这个步骤会比较耗时，默认构建函数只生成路径，不自动跑完整 Simulink 数据采样。

常用命令：

```matlab
init_project;
outputs = build_modern_tcn_dataset_v4_industrial();
```

完整生成母集和窗口数据集：

```matlab
init_project;
cfg = struct('generate_train_data', true, 'prepare_dataset', true);
outputs = build_modern_tcn_dataset_v4_industrial(cfg);
```

V4 数据集训练 ModernTCN：

```powershell
python src\ModernTCN\train_modern_tcn.py --seed 42 --dataset-file data\tcn\ModernTCN_dataset_v4_industrial.mat --run-tag modern_tcn_v4_industrial_seed42
```

## 生成流程

1. 生成固定参考路径：
   - 脚本：`src/paths/gen_tcn_training_paths_v3_transition_rich.m`
   - 产物：`data/paths/path_train_tcn_v3_*.mat`
   - 清单：`data/paths/path_train_tcn_v3_manifest.csv`

2. 用 `GRU_DataGen` 对每条路径做连续仿真：
   - 脚本：`src/TCN/TCN_gen_train_data_v3_transition_rich.m`
   - 产物：`data/tcn/TCN_train_data_v3_transition_rich_full.mat`
   - 默认每条路径 `4` 次仿真。

3. 补充 clean-turn 增强样本：
   - 产物：`data/tcn/TCN_train_data_v3_clean_turn_aug.mat`
   - 合并产物：`data/tcn/TCN_train_data_v3_transition_rich_clean_turn_aug_full.mat`

4. 滑窗、归一化、run-level split：
   - 脚本：`src/TCN/TCN_prepare_dataset_v3_transition_rich.m`
   - 最终产物：`data/tcn/TCN_dataset_v3_transition_rich_clean_turn_aug.mat`

## 每条路径四次仿真的含义

四次仿真不改变参考路径几何。也就是说：

- `v_ref` 不变；
- `omega_ref` 不变；
- `theta_ref` 不变；
- `X_ref/Y_ref/psi_ref` 不变；
- 平地转弯路径的参考转弯半径 `R = v_ref / abs(omega_ref)` 不变。

四次仿真的变化来自连续数据生成阶段：

- 噪声是否开启；
- 噪声强度，当前 V3 clean-turn-aug 配置为 clean ratio `0.25`，噪声倍率在 `1.0` 和 `1.5` 中随机；
- 随机噪声种子；
- 动态事件类型：`slip`、`load_change`、`stall`；
- 动态事件窗口位置、持续时间、强度；
- 可能额外添加第二个动态事件。

因此，四次重复主要提升传感噪声、载荷、打滑、堵转扰动鲁棒性，不会扩展转向半径、曲率、坡度形状或速度曲线分布。

## 后续扩展原则

若目标是覆盖更多真实工业工况，优先改路径层，而不是只增加每条路径重复次数。

推荐路径层扩展：

- 增加更多左/右转半径族，建议半径 `6-12 m`，边界样本不低于 `5 m`；
- 增加 `v_ref=0.8-1.1 m/s` 的速度族；
- 增加 `theta_ref=+1~+8 deg` 和 `-1~-8 deg` 的直线坡度族；
- 增加坡度与转弯重叠的 entry、middle、exit 三类样本；
- 增加 S 弯、仓储通道连续弯、长直线入坡、坡顶/坡底过渡；
- 每类路径左右方向都要成对出现，避免方向偏置。

论文绘图需要的 `-10~10 deg`、`0.1 deg` 坡度密集样本后续单独生成，不混进主训练集，避免训练母集体量膨胀和坡度分布过度偏置。

推荐仿真生成层扩展：

- 保留每条路径至少一次 clean run；
- 增加噪声、载荷变化、打滑、堵转扰动；
- 可以少量引入质量、滚阻、摩擦系数变化，但必须记录到 run meta；
- 不要在仿真生成阶段直接改 `omega_ref/theta_ref/v_ref`，除非同步重建 `X_ref/Y_ref/psi_ref` 和标签。

## 历史或非当前数据

以下文件保留用于回溯，不作为当前 ModernTCN 默认训练数据：

- `data/tcn/TCN_dataset_v3_transition_rich.mat`
- `data/tcn/TCN_dataset_v2_transition_rich.mat`
- `data/tcn/TCN_dataset_processed.mat`
- `data/tcn/TCN_dataset_processed_turn_tail_tmp.mat`
- `data/tcn/TCN_train_data_full.mat`
- `data/tcn/TCN_train_data_smoke.mat`
- `data/tcn/TCN_train_data_v3_smoke.mat`
