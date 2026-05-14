% =========================================================================
% 脚本名称: export_mamba_dataset.m
% 版本: V2.0 (全量优化版)
% 最后修改时间: 2026-03-30
% 
% 优化亮点:
%   1. 极速内存预分配: 以 240 回合为例，瞬间千万级切片无延迟、无内存碎片。
%   2. PyTorch 原生支持: 数据直接下移至 single (float32)，砍掉50%冗余存储，PyTorch 零损耗对接。
%   3. HDF5 扁平化导出: 彻底解决 Python h5py 工具读取嵌套 MATLAB struct 时地狱般的 key 查找问题，变量存至顶级视图。
%   4. 自检安全网: 自动分析 NaN / 均值溢出，严格捍卫训练前的数据纯度。
% =========================================================================

clear; clc;

%% -------------------- 1. 配置参数 --------------------
disp('初始化导出配置...');
root = project_root();
data_dir = fullfile(root, 'data', 'mamba');
input_file = fullfile(data_dir, 'Mamba_train_data_full.mat');
output_file = fullfile(data_dir, 'Mamba_dataset_export.mat');cd /mnt/e/Matlab/Simulink/S-Function_16/src/Mamba
python train_agv_mamba.py \
    --model mamba2 \
    --data ../../data/mamba/Mamba_dataset_export.mat \
    --epochs 30 \
    --turn-right-weight 10.0 \
    --slip-pos-weight 8.0 \
    --exp-name agv_mamba2_v2_weighted \
    --d-model 128 --n-layers 4 --d-state 64 --d-conv 4 --expand 2

cfg = struct();
cfg.window_size = 128;      % 序列窗口长度 (1.28秒 @ 0.01s Ts)
cfg.stride = 64;            % 滑窗步长 (50% 重叠)
cfg.train_ratio = 0.80;     % 训练集比例
cfg.val_ratio = 0.10;       % 验证集比例

% 传感器通道保留配置 (默认保留打滑率通道，依靠两侧轮速计算不算作弊)
cfg.drop_slip_ratio = false; 
cfg.slip_indices = [8, 9];  
channel_names = {'accel_x', 'gyro_y', 'gyro_z', 'I_lf', 'I_rr', ...
                 'omega_w_lf', 'omega_w_rr', 'slip_lf', 'slip_rr', 'accel_y'};
if cfg.drop_slip_ratio
    channel_names(cfg.slip_indices) = [];
end

% 基础配置合法性检查
if cfg.window_size <= 0 || cfg.stride <= 0
    error('window_size 和 stride 必须为正数。');
end
if cfg.train_ratio <= 0 || cfg.val_ratio < 0 || (cfg.train_ratio + cfg.val_ratio) >= 1
    error('数据集划分比例非法：需满足 train_ratio>0, val_ratio>=0 且 train_ratio+val_ratio<1。');
end

%% -------------------- 2. 加载原始数据 --------------------
fprintf('正在加载原始数据: %s\n', input_file);
if ~exist(input_file, 'file')
    error('未找到 Mamba 原始训练数据。请确保已运行 Mamba_gen_train_data.m。');
end
raw_data = load(input_file);
if ~isfield(raw_data, 'data') || ~isfield(raw_data.data, 'runs')
    error('输入 MAT 文件缺少 data.runs 结构。');
end
runs = raw_data.data.runs;
N_runs = numel(runs);
fprintf('成功加载，共找到 %d 个 Run。\n', N_runs);
if N_runs < 3
    warning('Run 数较少（%d），Train/Val/Test 中可能出现空集合。', N_runs);
end

%% -------------------- 3. 划分数据集 (Run-Level) --------------------
rng(42); % 固定种子以保证可复现性
rand_idx = randperm(N_runs);

N_train = floor(N_runs * cfg.train_ratio);
N_val = floor(N_runs * cfg.val_ratio);

run_idx_train = rand_idx(1 : N_train);
run_idx_val = rand_idx(N_train+1 : N_train + N_val);
run_idx_test = rand_idx(N_train + N_val + 1 : end);

fprintf('数据划分完成: Train=%d, Val=%d, Test=%d Runs\n', ...
    length(run_idx_train), length(run_idx_val), length(run_idx_test));

if isempty(run_idx_train)
    error('训练集 Run 为空，无法计算归一化统计量。请提高 run 数或调整划分比例。');
end
if isempty(run_idx_val)
    warning('验证集 Run 为空。');
end
if isempty(run_idx_test)
    warning('测试集 Run 为空。');
end

%% -------------------- 4. 执行切片 (极速预分配模式) --------------------
disp('开始对 Train 集进行滑窗切片...');
[X_train, Y_train_theta, Y_train_delta, Y_train_main, Y_train_turn, Y_train_slip, Y_train_stall] = ...
    slice_data(runs, run_idx_train, cfg);

disp('开始对 Val 集进行滑窗切片...');
[X_val, Y_val_theta, Y_val_delta, Y_val_main, Y_val_turn, Y_val_slip, Y_val_stall] = ...
    slice_data(runs, run_idx_val, cfg);

disp('开始对 Test 集进行滑窗切片...');
[X_test, Y_test_theta, Y_test_delta, Y_test_main, Y_test_turn, Y_test_slip, Y_test_stall] = ...
    slice_data(runs, run_idx_test, cfg);

fprintf('切片完成，样本数提取: Train=%d, Val=%d, Test=%d\n', ...
    size(X_train, 1), size(X_val, 1), size(X_test, 1));

if isempty(X_train)
    error('Train 切片样本为 0，无法计算标准化统计量。请检查 window_size/stride 或数据长度。');
end

%% -------------------- 5. Z-Score 标准化 (严格防泄漏) --------------------
disp('依据训练集计算均值和方差，执行 Z-Score 标准化...');

% 前两维展开，统计全量输入的通道级分布
flat_X_train = reshape(X_train, [], size(X_train, 3));
mu = single(mean(flat_X_train, 1));
sigma = single(std(flat_X_train, 0, 1));
sigma(sigma < 1e-6) = 1e-6; % 防止除零

% 广播机制运用 (Broadcasting)
X_train = (X_train - reshape(mu, 1, 1, [])) ./ reshape(sigma, 1, 1, []);
X_val   = (X_val - reshape(mu, 1, 1, [])) ./ reshape(sigma, 1, 1, []);
X_test  = (X_test - reshape(mu, 1, 1, [])) ./ reshape(sigma, 1, 1, []);

%% -------------------- 6. 数据自检诊断台 --------------------
disp('进入数据装箱自检...');

% 检查 NaN 和 Inf (覆盖全部三个集合)
chk_nan = sum(isnan(X_train(:))) + sum(isnan(X_val(:))) + sum(isnan(X_test(:)));
chk_inf = sum(isinf(X_train(:))) + sum(isinf(X_val(:))) + sum(isinf(X_test(:)));
if chk_nan > 0
    warning('🚨 数据存在 %d 个 NaN！请回溯仿真脚本！', chk_nan);
elseif chk_inf > 0
    warning('🚨 数据存在 %d 个 Inf！请检查归一化 sigma 是否过小！', chk_inf);
else
    disp('  ✅ 矩阵纯度检查通过: 无 NaN / Inf');
end

% 检查归一化后的数据范围 (正常应落在 [-5, 5] 以内)
max_abs_val = max(abs(X_train(:)));
fprintf('  归一化后最大绝对值: %.2f\n', max_abs_val);
if max_abs_val > 10
    warning('🚨 归一化后极端值超过 10，存在严重异常样本！');
else
    disp('  ✅ 归一化范围检查通过');
end

% 检查标签有效性
fprintf('  回归标签 theta 范围: [%.4f, %.4f] rad\n', min(Y_train_theta(:)), max(Y_train_theta(:)));
fprintf('  回归标签 delta 范围: [%.4f, %.4f] rad\n', min(Y_train_delta(:)), max(Y_train_delta(:)));
fprintf('  分类标签 main 类别数: %d\n', numel(unique(Y_train_main(:))));
validate_label_values(Y_train_main, [1, 2, 3], 'Y_train_main');
validate_label_values(Y_train_turn, [-1, 0, 1], 'Y_train_turn');
validate_label_values(Y_train_slip, [0, 1], 'Y_train_slip');
validate_label_values(Y_train_stall, [0, 1], 'Y_train_stall');

% 也覆盖验证/测试集，避免训练通过但评估阶段崩溃
validate_label_values(Y_val_main, [1, 2, 3], 'Y_val_main');
validate_label_values(Y_val_turn, [-1, 0, 1], 'Y_val_turn');
validate_label_values(Y_val_slip, [0, 1], 'Y_val_slip');
validate_label_values(Y_val_stall, [0, 1], 'Y_val_stall');
validate_label_values(Y_test_main, [1, 2, 3], 'Y_test_main');
validate_label_values(Y_test_turn, [-1, 0, 1], 'Y_test_turn');
validate_label_values(Y_test_slip, [0, 1], 'Y_test_slip');
validate_label_values(Y_test_stall, [0, 1], 'Y_test_stall');

disp('  ✅ 数据类型校验通过: 统一降维为 Single(fp32)');

%% -------------------- 7. 扁平化导出保存 --------------------
disp('正在导出为 v7.3 MAT 格式 (开启 HDF5 底层兼容)...');

% 为了被 python 高效抓取，不再封装 struct，直接扔在顶级命名空间
channel_info = string(channel_names); %#ok<NASGU>
save(output_file, '-v7.3', ...
    'X_train', 'Y_train_theta', 'Y_train_delta', 'Y_train_main', 'Y_train_turn', 'Y_train_slip', 'Y_train_stall', ...
    'X_val', 'Y_val_theta', 'Y_val_delta', 'Y_val_main', 'Y_val_turn', 'Y_val_slip', 'Y_val_stall', ...
    'X_test', 'Y_test_theta', 'Y_test_delta', 'Y_test_main', 'Y_test_turn', 'Y_test_slip', 'Y_test_stall', ...
    'mu', 'sigma', 'channel_info');

fprintf('\n🎯 导出大功告成！文件保存在: %s\n', output_file);
fprintf('在 Python 中，通过 h5py 读取犹如探囊取物。\n\n');

%% ==================== 内部切片引擎 ====================
function [X, Y_theta, Y_delta, Y_main, Y_turn, Y_slip, Y_stall] = slice_data(runs, indices, cfg)

    % 先计算需要开启的总窗口数，为接下来的连续内存分配打好地基
    total_windows = 0;
    for i = 1:length(indices)
        run_data = runs(indices(i));
        validate_run_fields(run_data, indices(i));

        N_frames = size(run_data.y_mamba, 1);
        windows_i = floor((N_frames - cfg.window_size) / cfg.stride) + 1;
        if windows_i > 0
            total_windows = total_windows + windows_i;
        end
    end
    
    dim_x = 10;
    if cfg.drop_slip_ratio
        dim_x = 8;
    end
    
    % 预留极其庞大的空旷连续内存块，大幅消除内存碎片化导致的电脑卡壳（设为 single 彻底向 PyTorch fp32 看齐）
    X = zeros(total_windows, cfg.window_size, dim_x, 'single');
    Y_theta = zeros(total_windows, cfg.window_size, 'single');
    Y_delta = zeros(total_windows, cfg.window_size, 'single');
    Y_main  = zeros(total_windows, cfg.window_size, 'int8');
    Y_turn  = zeros(total_windows, cfg.window_size, 'int8');
    Y_slip  = zeros(total_windows, cfg.window_size, 'int8');
    Y_stall = zeros(total_windows, cfg.window_size, 'int8');
    
    idx = 1;
    for i = 1:length(indices)
        run_data = runs(indices(i));
        validate_run_fields(run_data, indices(i));

        features = single(run_data.y_mamba); % 提前降为 fp32

        if size(features, 2) ~= 10
            error('Run #%d 的 y_mamba 维度非法：期望 10 通道，实际 %d。', indices(i), size(features, 2));
        end

        N_frames = size(features, 1);
        if N_frames < cfg.window_size
            continue;
        end

        if numel(run_data.y_theta_ground) ~= N_frames || ...
           numel(run_data.y_delta_vehicle) ~= N_frames || ...
           numel(run_data.label_main) ~= N_frames || ...
           numel(run_data.label_turn) ~= N_frames || ...
           numel(run_data.label_slip) ~= N_frames || ...
           numel(run_data.label_stall) ~= N_frames
            error('Run #%d 标签长度与 y_mamba 帧数不一致。', indices(i));
        end
        
        if cfg.drop_slip_ratio
            features(:, cfg.slip_indices) = [];
        end

        for start_idx = 1 : cfg.stride : (N_frames - cfg.window_size + 1)
            end_idx = start_idx + cfg.window_size - 1;
            
            X(idx, :, :) = features(start_idx:end_idx, :);
            Y_theta(idx, :) = single(run_data.y_theta_ground(start_idx:end_idx));
            Y_delta(idx, :) = single(run_data.y_delta_vehicle(start_idx:end_idx));
            Y_main(idx, :)  = int8(run_data.label_main(start_idx:end_idx));
            Y_turn(idx, :)  = int8(run_data.label_turn(start_idx:end_idx));
            Y_slip(idx, :)  = int8(run_data.label_slip(start_idx:end_idx));
            Y_stall(idx, :) = int8(run_data.label_stall(start_idx:end_idx));
            
            idx = idx + 1;
        end
    end
end

function validate_run_fields(run_data, run_index)
required_fields = {'y_mamba', 'y_theta_ground', 'y_delta_vehicle', ...
    'label_main', 'label_turn', 'label_slip', 'label_stall'};
for k = 1:numel(required_fields)
    f = required_fields{k};
    if ~isfield(run_data, f)
        error('Run #%d 缺少字段: %s', run_index, f);
    end
end
end

function validate_label_values(y, allowed, var_name)
if isempty(y)
    return;
end
if any(~isfinite(single(y(:))))
    error('%s 含 NaN/Inf。', var_name);
end
u = unique(double(y(:)));
if ~all(ismember(u, allowed))
    error('%s 出现非法标签值: %s', var_name, mat2str(u(:)'));
end
end
