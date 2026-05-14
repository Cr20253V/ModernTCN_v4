% analyze_bo_results.m
% 分析贝叶斯优化结果，判断参数区间设置是否合理
% 核心方法：加载 bo_history 中的完整评估历史 (XTrace)，而非仅分析 bestPoint
% 运行方法：在MATLAB命令窗口中执行此脚本

clear; clc;
fprintf('═══════════════════════════════════════════════════════════════\n');
fprintf('           贝叶斯优化参数区间分析 (基于完整历史)\n');
fprintf('═══════════════════════════════════════════════════════════════\n\n');

%% 定义参数边界（来自 Bayesian_Optimization.m）
phase1_bounds = struct(...
    'q_y',          [20, 50], ...
    'q_psi',        [15, 60], ...
    'q_v',          [3.0, 20], ...
    'q_omega',      [0.5, 4], ...
    'log10_r_F',    [-4.0, -1.0], ...
    'log10_r_omega',[-4.0, -2.0], ...
    'log10_rdF',    [-2.5, -1.0], ...
    'log10_rdw',    [-2.5, -1.0]);

phase2_bounds = struct(...
    'omega_threshold',    [0.08, 0.40], ...
    'q_y_gain_max',       [1.2, 3.0], ...
    'theta_threshold',    [0.02, 0.08], ...
    'q_v_gain_max',       [1.2, 2.5], ...
    'R_F_gain_max_uphill',[1.0, 1.8]);

%% 查找历史文件
script_dir = fileparts(mfilename('fullpath'));
history_dir = fullfile(script_dir, '..', '..', 'results', 'bo', 'history');

% 获取今天的日期字符串
today_str = datestr(now, 'yyyymmdd');
history_files = dir(fullfile(history_dir, sprintf('bo_history_%s*.mat', today_str)));

if isempty(history_files)
    % 如果今天没有，找最新的
    history_files = dir(fullfile(history_dir, 'bo_history_*.mat'));
end

if isempty(history_files)
    error('未找到任何贝叶斯优化历史文件！请先运行优化。');
end

fprintf('找到 %d 个历史文件:\n', length(history_files));
for i = 1:length(history_files)
    fprintf('  [%d] %s\n', i, history_files(i).name);
end

%% 让用户选择分析哪个文件
if length(history_files) == 1
    selected_idx = 1;
else
    fprintf('\n请输入要分析的文件编号 (默认最新: %d): ', length(history_files));
    user_input = input('');
    if isempty(user_input)
        selected_idx = length(history_files);
    else
        selected_idx = user_input;
    end
end

history_file = fullfile(history_dir, history_files(selected_idx).name);
fprintf('\n正在分析: %s\n\n', history_files(selected_idx).name);

%% 加载历史并分析
S = load(history_file);
if ~isfield(S, 'boResults')
    error('历史文件中未找到 boResults 变量！');
end

br = S.boResults;

% 提取完整评估历史
if isprop(br, 'XTrace') || isfield(br, 'XTrace')
    XTrace = br.XTrace;
    ObjectiveTrace = br.ObjectiveTrace;
else
    error('boResults 中未找到 XTrace（评估历史）！');
end

fprintf('═══════════════════════════════════════════════════════════════\n');
fprintf('                    评估历史统计\n');
fprintf('═══════════════════════════════════════════════════════════════\n');
fprintf('总评估次数: %d\n', height(XTrace));
fprintf('成功评估数: %d (J < 1e6)\n', sum(ObjectiveTrace < 1e6));
fprintf('失败评估数: %d (J >= 1e6)\n', sum(ObjectiveTrace >= 1e6));
fprintf('最优代价: %.4f\n\n', min(ObjectiveTrace));

%% 分析每个参数的分布和边界命中情况
varNames = XTrace.Properties.VariableNames;

% 根据变量名判断是 Phase 1 还是 Phase 2
if any(strcmp(varNames, 'q_y'))
    bounds = phase1_bounds;
    phase_name = 'Phase 1';
elseif any(strcmp(varNames, 'omega_threshold'))
    bounds = phase2_bounds;
    phase_name = 'Phase 2';
else
    error('无法识别优化阶段（变量名不匹配）');
end

fprintf('═══════════════════════════════════════════════════════════════\n');
fprintf('              %s 参数分布分析\n', phase_name);
fprintf('═══════════════════════════════════════════════════════════════\n\n');

% 边界命中阈值：距边界 5% 范围内视为命中
boundary_threshold = 0.05;

fprintf('%-20s %10s %10s %10s | %8s %8s | %12s\n', ...
    '参数名', '最小值', '最大值', '最优值', '下界', '上界', '边界命中率');
fprintf('%s\n', repmat('-', 1, 95));

boundary_issues = {};

for i = 1:length(varNames)
    vn = varNames{i};
    vals = XTrace.(vn);
    
    if ~isfield(bounds, vn)
        continue;  % 跳过未定义边界的变量
    end
    
    b = bounds.(vn);
    range = b(2) - b(1);
    
    % 计算边界命中比例
    hits_lower = sum(vals < b(1) + boundary_threshold * range);
    hits_upper = sum(vals > b(2) - boundary_threshold * range);
    hit_rate_lower = hits_lower / length(vals) * 100;
    hit_rate_upper = hits_upper / length(vals) * 100;
    total_hit_rate = (hits_lower + hits_upper) / length(vals) * 100;
    
    % 找到最优解对应的参数值
    [~, best_idx] = min(ObjectiveTrace);
    best_val = vals(best_idx);
    
    % 状态判定
    status = '';
    if hit_rate_lower > 20
        status = sprintf('⚠️ 下界%.0f%%', hit_rate_lower);
        boundary_issues{end+1} = sprintf('%s: %.0f%% 采样点命中下界，建议降低下界', vn, hit_rate_lower);
    elseif hit_rate_upper > 20
        status = sprintf('⚠️ 上界%.0f%%', hit_rate_upper);
        boundary_issues{end+1} = sprintf('%s: %.0f%% 采样点命中上界，建议提高上界', vn, hit_rate_upper);
    else
        status = '✓ 正常';
    end
    
    fprintf('%-20s %10.4f %10.4f %10.4f | %8.4f %8.4f | %s\n', ...
        vn, min(vals), max(vals), best_val, b(1), b(2), status);
end

%% 汇总问题
fprintf('\n═══════════════════════════════════════════════════════════════\n');
fprintf('                    诊断结论\n');
fprintf('═══════════════════════════════════════════════════════════════\n');

if isempty(boundary_issues)
    fprintf('✅ 所有参数区间设置合理，无边界命中问题。\n');
else
    fprintf('⚠️ 发现 %d 个参数区间问题:\n\n', length(boundary_issues));
    for i = 1:length(boundary_issues)
        fprintf('  %d. %s\n', i, boundary_issues{i});
    end
    fprintf('\n建议: 根据上述诊断调整 Bayesian_Optimization.m 中的变量边界。\n');
end

%% 可视化（可选）
fprintf('\n是否绘制参数分布直方图? (y/n，默认n): ');
user_plot = input('', 's');
if strcmpi(user_plot, 'y')
    n_vars = length(varNames);
    cols = ceil(sqrt(n_vars));
    rows = ceil(n_vars / cols);
    
    figure('Name', sprintf('%s 参数分布', phase_name), 'Position', [100,100,1200,800]);
    for i = 1:length(varNames)
        vn = varNames{i};
        if ~isfield(bounds, vn), continue; end
        
        subplot(rows, cols, i);
        vals = XTrace.(vn);
        b = bounds.(vn);
        
        histogram(vals, 20, 'FaceColor', [0.3 0.6 0.9]);
        hold on;
        xline(b(1), 'r--', 'LineWidth', 2, 'Label', '下界');
        xline(b(2), 'r--', 'LineWidth', 2, 'Label', '上界');
        
        [~, best_idx] = min(ObjectiveTrace);
        xline(vals(best_idx), 'g-', 'LineWidth', 2, 'Label', '最优');
        
        title(strrep(vn, '_', '\_'));
        xlabel('参数值');
        ylabel('采样次数');
        grid on;
    end
    sgtitle(sprintf('%s 参数采样分布 (共%d次评估)', phase_name, height(XTrace)));
end

fprintf('\n═══════════════════════════════════════════════════════════════\n');
fprintf('                    分析完成\n');
fprintf('═══════════════════════════════════════════════════════════════\n');
