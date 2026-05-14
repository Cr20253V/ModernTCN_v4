% =============================
% 文件名：test_GRU_workflow.m
% 版本号：V1.0
% 最后修改时间：2025-10-31
% 作者：LPV-MPC Project
% 功能描述：
%   测试GRU工况识别完整工作流
%   1. 验证训练后的模型是否可用
%   2. 测试单步推理 GRU_infer.m
%   3. 测试在线推理 GRU_state_classifier.m
%   4. 可视化结果
%
% 使用方法：
%   直接运行此脚本：run('test_GRU_workflow.m')
%
% 依赖：
%   - GRU_model.mat（由 GRU_train.m 生成）
%   - GRU_dataset_processed.mat（测试集）
%   - GRU_infer.m
%   - GRU_state_classifier.m
%   - parameters.m
% =============================

%% 清理环境
clear; clc; close all;

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
data_gru_dir = fullfile(root, 'data', 'gru');

fprintf('\n========================================\n');
fprintf('GRU工况识别工作流测试\n');
fprintf('========================================\n');

%% 1. 检查依赖文件
fprintf('\n[步骤1/5] 检查依赖文件...\n');

model_file = fullfile(data_models_dir, 'GRU_model.mat');
dataset_file = fullfile(data_gru_dir, 'GRU_dataset_processed.mat');
raw_file = fullfile(data_gru_dir, 'GRU_train_data_full.mat');

required_files = {
    model_file, ...
    dataset_file, ...
    'GRU_infer.m', ...
    'GRU_state_classifier.m', ...
    'parameters.m'
};

for i = 1:length(required_files)
    if ~exist(required_files{i}, 'file')
        error('缺少必要文件: %s', required_files{i});
    end
end

fprintf('  ✓ 所有依赖文件齐全\n');

%% 2. 加载模型和数据集
fprintf('\n[步骤2/5] 加载模型和数据集...\n');

load(model_file, 'model');
load(dataset_file, 'dataset');
params = parameters();

fprintf('  ✓ 模型加载成功\n');
fprintf('    特征维度: %d\n', size(model.scaler.mean, 2));
fprintf('    序列长度: %d\n', size(dataset.X_test, 2));
fprintf('    测试样本数: %d\n', size(dataset.X_test, 1));

%% 3. 测试单步推理（GRU_infer）
fprintf('\n[步骤3/5] 测试单步推理（GRU_infer）...\n');

% 取测试集的前10个样本
n_test_samples = min(10, size(dataset.X_test, 1));
test_results = struct();

for i = 1:n_test_samples
    % 提取样本
    x_seq = squeeze(dataset.X_test(i, :, :));  % [seq_len, feat_dim]
    y_main_true = dataset.y_main_test(i);
    y_turn_true = dataset.y_turn_test(i);
    y_theta_true = dataset.y_theta_test(i);
    
    % 推理
    [label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model);
    
    % 保存结果
    test_results(i).label_main_pred = label_main;
    test_results(i).label_main_true = y_main_true;
    test_results(i).label_turn_pred = label_turn;
    test_results(i).label_turn_true = y_turn_true;
    test_results(i).theta_hat = theta_hat;
    test_results(i).theta_true = y_theta_true;
    test_results(i).conf_main_name = conf.label_main_name;
    test_results(i).conf_turn_name = conf.label_turn_name;
end

% 计算准确率
acc_main = mean([test_results.label_main_pred] == [test_results.label_main_true]);
acc_turn = mean([test_results.label_turn_pred] == [test_results.label_turn_true]);

% 计算MAE（仅slope样本）
slope_idx = find([test_results.label_main_true] == 3);
if ~isempty(slope_idx)
    mae_theta = mean(abs([test_results(slope_idx).theta_hat] - [test_results(slope_idx).theta_true]));
else
    mae_theta = 0;
end

fprintf('  ✓ 单步推理测试完成\n');
fprintf('    主分类准确率: %.2f%% (%d/%d)\n', ...
    acc_main * 100, sum([test_results.label_main_pred] == [test_results.label_main_true]), n_test_samples);
fprintf('    转弯分类准确率: %.2f%% (%d/%d)\n', ...
    acc_turn * 100, sum([test_results.label_turn_pred] == [test_results.label_turn_true]), n_test_samples);
fprintf('    坡度角MAE: %.4f° (%.4f rad)\n', rad2deg(mae_theta), mae_theta);

% 打印部分结果
fprintf('\n  前5个样本推理结果:\n');
fprintf('  %-5s %-15s %-15s %-15s %-15s %-10s\n', ...
    'ID', '主分类(预测)', '主分类(真值)', '转弯(预测)', '转弯(真值)', 'θ(°)');
fprintf('  %s\n', repmat('-', 1, 85));
for i = 1:min(5, n_test_samples)
    fprintf('  %-5d %-15s %-15s %-15s %-15s %-10.2f\n', ...
        i, ...
        test_results(i).conf_main_name, ...
        model.class_labels_main{test_results(i).label_main_true}, ...
        test_results(i).conf_turn_name, ...
        model.class_labels_turn{test_results(i).label_turn_true + 2}, ...
        rad2deg(test_results(i).theta_hat));
end

%% 4. 测试在线推理（GRU_state_classifier）
fprintf('\n[步骤4/5] 测试在线推理（GRU_state_classifier）...\n');

% 加载一个完整的运行数据（用于测试在线推理）
load(raw_file, 'data');

% 选择第一个回合
run_data = data.runs(1);
N = length(run_data.t);

% 获取场景类型（兼容不同版本的meta字段）
if isfield(run_data.meta, 'path_type')
    scene_name = run_data.meta.path_type;
elseif isfield(run_data.meta, 'scene')
    scene_name = run_data.meta.scene;
else
    scene_name = '未知';
end

fprintf('  测试场景: %s\n', scene_name);
fprintf('  仿真时长: %.2f s\n', run_data.t(end));
fprintf('  采样点数: %d\n', N);

% 初始化分类器
state = GRU_state_classifier('init', params, model);

% 在线循环
online_results = struct();
online_results.t = run_data.t;
online_results.label_main = zeros(N, 1);
online_results.label_turn = zeros(N, 1);
online_results.theta_hat = zeros(N, 1);
online_results.label_main_true = run_data.label_main;
online_results.label_turn_true = run_data.label_turn;
online_results.theta_true = run_data.theta;

fprintf('  开始在线推理...\n');
for t = 1:N
    % 当前时刻的原始输出
    y_raw_t = run_data.y_raw(t, :)';  % [31×1]
    
    % 更新分类器
    [state, out] = GRU_state_classifier('update', state, y_raw_t);
    
    % 保存结果
    online_results.label_main(t) = out.label_main;
    online_results.label_turn(t) = out.label_turn;
    online_results.theta_hat(t) = out.theta_hat;
end

fprintf('  ✓ 在线推理完成\n');

% 计算性能（跳过序列未满的初始阶段）
% 序列长度优先从model获取，否则从数据集维度获取
if isfield(model, 'seq_len')
    seq_len = model.seq_len;
else
    seq_len = size(dataset.X_test, 2);  % [n_samples, seq_len, feat_dim]
end
start_idx = seq_len + 1;

acc_main_online = mean(online_results.label_main(start_idx:end) == ...
                       online_results.label_main_true(start_idx:end));
acc_turn_online = mean(online_results.label_turn(start_idx:end) == ...
                       online_results.label_turn_true(start_idx:end));

% 坡度角MAE（仅slope样本）
slope_idx_online = find(online_results.label_main_true(start_idx:end) == 3);
if ~isempty(slope_idx_online)
    mae_theta_online = mean(abs(online_results.theta_hat(start_idx + slope_idx_online - 1) - ...
                                 online_results.theta_true(start_idx + slope_idx_online - 1)));
else
    mae_theta_online = 0;
end

fprintf('    主分类准确率: %.2f%%\n', acc_main_online * 100);
fprintf('    转弯分类准确率: %.2f%%\n', acc_turn_online * 100);
fprintf('    坡度角MAE: %.4f°\n', rad2deg(mae_theta_online));

%% 5. 可视化在线推理结果
fprintf('\n[步骤5/5] 可视化在线推理结果...\n');

fig = figure('Position', [100, 100, 1400, 800]);

% 子图1：主分类
subplot(3, 1, 1);
hold on;
plot(online_results.t, online_results.label_main_true, 'k-', 'LineWidth', 2, 'DisplayName', '真值');
plot(online_results.t, online_results.label_main, 'r--', 'LineWidth', 1.5, 'DisplayName', '预测');
xlabel('时间 [s]');
ylabel('主分类');
title(sprintf('主分类识别（准确率: %.2f%%）', acc_main_online * 100));
legend('Location', 'best');
grid on;
ylim([0.5, 3.5]);
yticks(1:3);
yticklabels({'flat', 'stall', 'slope'});

% 子图2：转弯状态
subplot(3, 1, 2);
hold on;
plot(online_results.t, online_results.label_turn_true, 'k-', 'LineWidth', 2, 'DisplayName', '真值');
plot(online_results.t, online_results.label_turn, 'b--', 'LineWidth', 1.5, 'DisplayName', '预测');
xlabel('时间 [s]');
ylabel('转弯状态');
title(sprintf('转弯状态识别（准确率: %.2f%%）', acc_turn_online * 100));
legend('Location', 'best');
grid on;
ylim([-1.5, 1.5]);
yticks(-1:1);
yticklabels({'right', 'straight', 'left'});

% 子图3：坡度角估计
subplot(3, 1, 3);
hold on;
plot(online_results.t, rad2deg(online_results.theta_true), 'k-', 'LineWidth', 2, 'DisplayName', '真值');
plot(online_results.t, rad2deg(online_results.theta_hat), 'g--', 'LineWidth', 1.5, 'DisplayName', '估计');
xlabel('时间 [s]');
ylabel('坡度角 [°]');
title(sprintf('坡度角估计（MAE: %.4f°）', rad2deg(mae_theta_online)));
legend('Location', 'best');
grid on;

% 保存图像
saveas(fig, 'GRU_logs/test_online_inference.png');
fprintf('  ✓ 可视化图像已保存至: GRU_logs/test_online_inference.png\n');

%% 总结
fprintf('\n========================================\n');
fprintf('测试完成！\n');
fprintf('========================================\n');
fprintf('单步推理性能:\n');
fprintf('  - 主分类准确率: %.2f%%\n', acc_main * 100);
fprintf('  - 转弯分类准确率: %.2f%%\n', acc_turn * 100);
fprintf('  - 坡度角MAE: %.4f°\n', rad2deg(mae_theta));
fprintf('\n在线推理性能:\n');
fprintf('  - 主分类准确率: %.2f%%\n', acc_main_online * 100);
fprintf('  - 转弯分类准确率: %.2f%%\n', acc_turn_online * 100);
fprintf('  - 坡度角MAE: %.4f°\n', rad2deg(mae_theta_online));
fprintf('\n所有测试通过！✓\n');

