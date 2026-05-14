# Transition-Rich v3 TCN 自动参数筛选流程

## 入口

使用：

```matlab
run_TCN_v3_auto_param_screen(struct('stage','probe'));
run_TCN_v3_auto_param_screen(struct('stage','confirm'));
run_TCN_v3_auto_param_screen(struct('stage','validate'));
run_TCN_v3_auto_param_screen(struct('stage','full'));
```

输出目录：

```text
results/tcn/experiments/transition_rich_v3_auto_screen
```

每个阶段都会生成：

- `TCN_v3_auto_<stage>_summary.csv`
- `TCN_v3_auto_<stage>_summary.md`

如果对应模型的 meta 文件已经存在，默认会直接读取并跳过训练。需要强制重训时加：

```matlab
run_TCN_v3_auto_param_screen(struct('stage','probe','force',true));
```

## 阶段说明

### 1. probe

只跑 seed42 的短训练，用来快速筛掉明显不行的配置。

默认候选：

- `sqrt_mild_ref`
- `base_comp_t025`
- `base_comp_t035`
- `base_comp_t060`
- `base_comp_flat120`

运行：

```matlab
init_project;
run_TCN_v3_auto_param_screen(struct('stage','probe'));
```

probe 默认设置：

- `max_epochs = 45`
- 不跑 turn finetune
- 不组合 base/turn best
- 主要看 `acc_main`、`flat_recall`、`slope_recall`、`theta_mae_deg`

### 2. confirm

自动读取 probe summary，选择 score 最低的前 `top_k=2` 个配置，用 seeds `[42 101]` 完整训练。

运行：

```matlab
run_TCN_v3_auto_param_screen(struct('stage','confirm'));
```

如果想手动指定配置：

```matlab
run_TCN_v3_auto_param_screen(struct( ...
    'stage','confirm', ...
    'configs',{{'base_comp_t035','base_comp_t060'}}));
```

### 3. validate

自动读取 confirm summary，选择最优配置，用 seed73 验证。

```matlab
run_TCN_v3_auto_param_screen(struct('stage','validate'));
```

### 4. full

自动读取 validate summary，如果不存在则读取 confirm summary，选择最优配置，用五个 seeds 完整训练：

```matlab
run_TCN_v3_auto_param_screen(struct('stage','full'));
```

默认 seeds：

```matlab
[11 21 42 73 101]
```

## 评分逻辑

分数越低越好。自动筛选重点惩罚：

- `acc_main` 低；
- `flat_recall < 0.90`；
- `slope_recall < 0.90`；
- `theta_mae_deg` 大；
- 完整训练阶段额外惩罚 `acc_turn_transition < 0.75`。

候选配置会先优先从 pass 的配置中选；如果没有配置 pass，则选择 score 最低者，避免流程中断。

## 推荐执行

为了控制耗时，按阶段跑：

```matlab
init_project;
run_TCN_v3_auto_param_screen(struct('stage','probe'));
```

看 `TCN_v3_auto_probe_summary.csv` 后再跑：

```matlab
run_TCN_v3_auto_param_screen(struct('stage','confirm'));
```

如果 confirm 有配置满足：

- `acc_main >= 0.90`
- `flat_recall >= 0.90`
- `slope_recall >= 0.88`
- `turnT >= 0.75`
- `theta_mae_deg <= 0.70`

再跑 validate/full。

## 内存建议

函数每个训练结束后会执行：

```matlab
close all;
reset(gpuDevice);
```

如果仍然出现内存不足，建议每个阶段单独重启 MATLAB 后再运行下一阶段。
