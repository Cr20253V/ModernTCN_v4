# Transition-Rich v3 数据修订说明

## 当前 V2 不完善处

1. 原始训练母集只有 18 条短路径，V2 主要通过预处理阶段密集滑窗增加过渡样本，没有改变真实仿真路径的物理分布。
2. 坡度+转弯复合路径数量偏少，主要集中在 `slope_left_turn_combo`、`slope_right_turn_combo`、`downhill_turn_transition` 和 `challenge_steep_combo`。
3. 现有复合路径大多是先进入坡度平台，再进入转弯；坡度变化阶段和转弯变化阶段真正重叠的样本不足。
4. 负坡样本偏少。V2 测试集坡度窗口中正坡为 `223`，负坡为 `94`，坡度方向覆盖不均衡。
5. 连续变化坡度覆盖不足。已有 `bumpy_theta_local` 是局部正弦坡度，但 ramp、坡度反转、快慢坡度过渡没有系统覆盖。
6. V2 对 theta transition 使用 `theta_transition_weight=0.75`，这能降低模糊窗口影响，但也可能削弱模型学习坡度连续变化的能力。

## V3 修改目标

V3 的目标不是替换模型结构，而是先排除数据瓶颈：

- 增加坡度变化与转弯变化重叠的路径；
- 增加负坡+左/右转组合；
- 增加长 ramp、坡度反转、连续正弦坡度；
- 增加快/慢坡度过渡时间；
- 让 TCN/GRU 继续使用同一母集、同一 split、同一输入特征，保持公平比较。

## 已新增或修改的脚本

| 文件 | 作用 |
|---|---|
| `src/paths/gen_tcn_training_paths.m` | 保持默认 V1 行为，同时支持通过配置生成 V3 路径集合和自定义文件前缀。 |
| `src/paths/gen_tcn_training_paths_v3_transition_rich.m` | V3 路径入口，输出 `path_train_tcn_v3_*.mat`，不覆盖旧路径。 |
| `src/TCN/TCN_gen_train_data_v3_transition_rich.m` | V3 训练母集入口，输出 `TCN_train_data_v3_transition_rich_full.mat`。 |
| `src/TCN/TCN_prepare_dataset_v3_transition_rich.m` | V3 窗口化入口，输出 `TCN_dataset_v3_transition_rich.mat`。 |
| `src/TCN/run_TCN_GRU_transition_rich_v3_baseline.m` | V3 TCN/GRU 固定 seed baseline 入口。 |

## V3 路径新增重点

V3 在原有 18 条路径基础上追加以下类型：

- `v3_uphill_left/right_overlap_entry`
- `v3_downhill_left/right_overlap_entry`
- `v3_uphill_left_overlap_exit`
- `v3_downhill_right_overlap_exit`
- `v3_long_ramp_up_left_turn`
- `v3_long_ramp_down_right_turn`
- `v3_theta_reversal_s_curve`
- `v3_theta_sine_left/right_turn`
- `v3_fast_slope_step_left`
- `v3_slow_slope_step_right`
- `v3_speed_slope_turn_coupled`

这些路径会以 `path_train_tcn_v3_*.mat` 保存，因此不会覆盖 V2 使用过的 `path_train_tcn_*.mat`。

## V3 预处理差异

| 参数 | V2 | V3 |
|---|---:|---:|
| `transition_stride` | 16 | 12 |
| `transition_context_sec` | 1.00 | 1.50 |
| `theta_transition_range_deg` | 1.50 | 1.00 |
| `theta_transition_weight` | 0.75 | 1.00 |
| `main_ambiguous_weight` | 0.65 | 0.75 |
| `turn_ambiguous_weight` | 0.50 | 0.60 |

V3 对坡度连续变化窗口更敏感，并且不再降低 theta transition 的回归权重。

## 推荐手动运行顺序

```matlab
init_project;

% 1. 生成 V3 路径
run('src/paths/gen_tcn_training_paths_v3_transition_rich.m');

% 2. 运行 Simulink 生成 V3 连续训练母集
data = TCN_gen_train_data_v3_transition_rich();

% 3. 生成 V3 共享窗口化数据集
dataset = TCN_prepare_dataset_v3_transition_rich();

% 4. 固定 seed 复跑 TCN/GRU
seeds = [11 21 42 73 101];
for i = 1:numel(seeds)
    run_TCN_GRU_transition_rich_v3_baseline(seeds(i), i == 1, true);
end
```

如果第 3 步已经手动跑过，第 4 步也可以把 `i == 1` 改成 `false`，避免重复预处理。

## 复跑后重点观察

- V3 的 train/val/test 中正坡、负坡、坡度 transition 是否更均衡。
- TCN 的 `theta_mae_deg` 和 `slope_recall` 是否相对 V2 缩小与 GRU 的差距。
- TCN 是否继续保持 `acc_turn` 和 `acc_turn_transition` 优势。
- 如果 V3 数据充分后 TCN 仍明显落后 GRU 的坡度指标，再进入 ModernTCN-small。
