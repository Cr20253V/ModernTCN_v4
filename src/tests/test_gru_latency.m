% =============================
% 文件名：test_gru_latency.m
% 版本号：V1.1
% 最后修改时间：2025-11-26
% 作者：LPV-MPC Project
% 功能描述：
%   使用控制变量法 + 预设组合验证，对 GRU 在线识别中的
%   dwell_main / dwell_turn / tau_theta 三个延时敏感参数进行搜索，
%   输出综合评分排名与最优配置。
%
% 配置说明：
%   - cfg.model_file       ：GRU 模型文件 (默认 GRU_model.mat)
%   - cfg.raw_data_file    ：原始 run 数据 (默认 GRU_train_data_full.mat)
%   - cfg.results_dir      ：评估结果输出目录
%   - cfg.runs_per_mode    ：每种行驶模式抽取的 run 数量
%   - cfg.weights          ：综合得分权重 (准确率/延时/θMAE/抖动)
%
% 依赖脚本/数据：
%   - parameters.m（系统参数）
%   - GRU_model.mat（包含 seq_len/scaler 的训练模型）
%   - GRU_train_data_full.mat（在线评估所需 run）
%   - GRU_state_classifier.m / GRU_infer.m（在线推理封装）
%
% 使用方法：
%   >> test_gru_latency
%   运行结束后，Top5 排行及控制变量法最优结果将打印至命令行，
%   并保存至 cfg.results_dir/latency_summary_<timestamp>.mat。
%
% 约束/注意：
%   - 仅覆盖 GRU_state_classifier 中的驻留时间与 theta 低通参数；
%   - seq_len、特征滤波 (tau_diff/tau_accel_lp) 与数据集保持不变；
%   - 若需评估其它参数，应另行构建专用脚本。
% =============================

clear; clc;  % 清理环境，以免旧变量干扰评分

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
data_gru_dir = fullfile(root, 'data', 'gru');
default_results_dir = results_dir('gru/latency_eval');
fprintf('\n===============================================\n');
fprintf('GRU 延时评估 (test_gru_latency)\n');
fprintf('===============================================\n');

%% 配置
cfg = struct();
cfg.model_file        = fullfile(data_models_dir, 'GRU_model.mat');
cfg.raw_data_file     = fullfile(data_gru_dir, 'GRU_train_data_full.mat');
cfg.results_dir       = default_results_dir;
cfg.runs_per_mode     = 6;          % 每种行驶模式最多选取的 run 数
cfg.weights = struct( ...
    'acc_main', 1.0, ...            % 主分类准确率权重
    'acc_turn', 0.5, ...            % 转弯准确率权重
    'delay',    0.7, ...            % 延时惩罚系数 (单位 s)
    'theta',    0.2, ...            % θ MAE 惩罚系数 (单位 deg)
    'flips',    0.3 ...             % 标签抖动惩罚系数 (次/分钟)
);

if ~exist(cfg.results_dir,'dir')
    mkdir(cfg.results_dir);
end

%% 加载依赖与原始数据
fprintf('[1/6] 加载模型与数据...\n');
params = parameters();
model_data = load(cfg.model_file, 'model');
model = model_data.model;
raw = load(cfg.raw_data_file, 'data');
all_runs = raw.data.runs;
[selected_runs, selection_meta] = select_runs_for_latency(all_runs, cfg.runs_per_mode);
if isempty(selected_runs)
    error('未选到任何 run，请检查原始数据。');
end
fprintf('  - 选取 %d 条 run，覆盖 %d 种行驶模式\n', numel(selected_runs), selection_meta.num_modes);

timestamp = datestr(now,'yyyymmdd_HHMMSS');
variant_cache = containers.Map();   % key -> metrics
all_metrics = containers.Map();

%% 变体定义（包含控制变量序列与人工组合）
% 最优组合（来自上一轮评估）：
%   dwell_main = 0.20 s
%   dwell_turn = 0.40 s
%   tau_theta  = 0.15 s
baseline = struct('name','baseline','dwell_main',0.20,'dwell_turn',0.40,'tau_theta',0.15);
dwell_main_candidates = [0.20 0.25 0.30 0.40];
dwell_turn_candidates = [0.40 0.50];
tau_theta_candidates  = [0.15 0.20 0.40];
manual_combos = [ ...
    struct('name','combo_fast','dwell_main',0.25,'dwell_turn',0.40,'tau_theta',0.20); ...
    struct('name','combo_balanced','dwell_main',0.30,'dwell_turn',0.50,'tau_theta',0.20); ...
    struct('name','combo_aggressive','dwell_main',0.20,'dwell_turn',0.40,'tau_theta',0.15) ...
];

%% 基线评估：记录默认参数的表现
fprintf('\n[2/6] 评估基线参数...\n');
[metrics, variant_cache] = eval_variant_with_cache(baseline, params, model, selected_runs, cfg, variant_cache);
all_metrics(metrics.key) = metrics;
control_variant = baseline;
control_metrics = metrics;
fprintf('  baseline score = %.3f (AccMain=%.3f, Delay=%.3f s)\n', control_metrics.score, control_metrics.acc_main, control_metrics.delay_combined);

%% 控制变量法：仅改变 dwell_main，锁定其余参数
fprintf('\n[3/6] 控制变量法 - 扫描 dwell_main ...\n');
[control_variant, control_metrics, variant_cache, all_metrics] = sweep_parameter('dwell_main', ...
    dwell_main_candidates, control_variant, params, model, selected_runs, cfg, variant_cache, all_metrics);
fprintf('  best dwell_main=%.2f s (score=%.3f)\n', control_variant.dwell_main, control_metrics.score);

%% 控制变量法：仅改变 dwell_turn
fprintf('\n[4/6] 控制变量法 - 扫描 dwell_turn ...\n');
[control_variant, control_metrics, variant_cache, all_metrics] = sweep_parameter('dwell_turn', ...
    dwell_turn_candidates, control_variant, params, model, selected_runs, cfg, variant_cache, all_metrics);
fprintf('  best dwell_turn=%.2f s (score=%.3f)\n', control_variant.dwell_turn, control_metrics.score);

%% 控制变量法：仅改变 tau_theta
fprintf('\n[5/6] 控制变量法 - 扫描 tau_theta ...\n');
[control_variant, control_metrics, variant_cache, all_metrics] = sweep_parameter('tau_theta', ...
    tau_theta_candidates, control_variant, params, model, selected_runs, cfg, variant_cache, all_metrics);
fprintf('  best tau_theta=%.2f s (score=%.3f)\n', control_variant.tau_theta, control_metrics.score);
control_best = control_metrics;

%% 手工组合验证：捕捉潜在参数耦合
fprintf('\n[6/6] 评估手工组合...\n');
for i = 1:numel(manual_combos)
    combo = manual_combos(i);
    [combo_metrics, variant_cache] = eval_variant_with_cache(combo, params, model, selected_runs, cfg, variant_cache);
    combo_metrics.tag = sprintf('manual:%s', combo.name);
    all_metrics(combo_metrics.key) = combo_metrics;
end

%% 汇总排行榜并输出 Top5
scoreboard = collect_metrics(all_metrics);
[~, order] = sort([scoreboard.score], 'descend');
scoreboard = scoreboard(order);

fprintf('\n===============================================\n');
fprintf('评估完成，Top 5 方案如下 (score 越大越好)：\n');
fprintf('%-16s %-7s %-7s %-7s | Score  AccMain AccTurn  Delay  θMAE  Flips/min\n', 'Variant', 'd_main', 'd_turn', 'tauθ');
fprintf('%s\n', repmat('-',1,86));
for i = 1:min(5, numel(scoreboard))
    m = scoreboard(i);
    fprintf('%-16s %-7.2f %-7.2f %-7.2f | %5.3f   %5.3f  %5.3f  %5.3f  %5.3f    %5.2f\n', ...
        m.tag, m.variant.dwell_main, m.variant.dwell_turn, m.variant.tau_theta, ...
        m.score, m.acc_main, m.acc_turn, m.delay_combined, m.theta_mae_deg, m.flip_rate_per_min);
end

fprintf('\n控制变量法最优：%s (score=%.3f)\n', control_best.tag, control_best.score);
fprintf('  - dwell_main=%.2f s, dwell_turn=%.2f s, tau_theta=%.2f s\n', ...
    control_best.variant.dwell_main, control_best.variant.dwell_turn, control_best.variant.tau_theta);

summary_file = fullfile(cfg.results_dir, sprintf('latency_summary_%s.mat', timestamp));
save(summary_file, 'scoreboard', 'cfg', 'selection_meta', 'control_best');
fprintf('\n已保存评估结果至 %s\n', summary_file);

%% 辅助函数
function [metrics, cache] = eval_variant_with_cache(variant, params, model, runs, cfg, cache)
    % 带缓存的变体评估，避免重复仿真相同组合
    key = variant_key(variant);
    if isKey(cache, key)
        metrics = cache(key);
        return;
    end
    run_stats = arrayfun(@(r) simulate_and_score_run(r, params, model, variant), runs);
    metrics = aggregate_metrics(run_stats, variant, cfg);
    metrics.key = key;
    metrics.tag = variant.name;
    cache(key) = metrics;
end

function [best_variant, best_metrics, cache, metrics_map] = sweep_parameter(param_name, values, base_variant, params, model, runs, cfg, cache, metrics_map)
    % 对单个参数做一维扫描，返回得分最高的组合
    best_variant = base_variant;
    best_metrics = [];
    best_score = -inf;
    for v = values
        variant = base_variant;
        variant.(param_name) = v;
        variant.name = sprintf('%s_%s%.2f', base_variant.name, param_name, v);
        [metrics, cache] = eval_variant_with_cache(variant, params, model, runs, cfg, cache);
        metrics.tag = sprintf('sweep:%s', param_name);
        metrics_map(metrics.key) = metrics;
        if metrics.score > best_score
            best_score = metrics.score;
            best_variant = variant;
            best_metrics = metrics;
        end
    end
end

function stats = simulate_and_score_run(run, params, model, variant)
    % 针对单条 run 调用在线推理，采集预测轨迹并计算指标
    state = GRU_state_classifier('init', params, model);
    state = apply_variant_overrides(state, variant);
    seq_len_effective = state.seq_len;
    N = size(run.y_raw,1);
    pred_main = zeros(N,1);
    pred_turn = zeros(N,1);
    pred_theta = zeros(N,1);
    for k = 1:N
        y = run.y_raw(k,:)';
        [state, out] = GRU_state_classifier('update', state, y);
        pred_main(k) = out.label_main;
        pred_turn(k) = out.label_turn;
        pred_theta(k) = out.theta_hat;
    end
    stats.seq_len = seq_len_effective;
    stats.time = run.t;
    stats.truth_main = run.label_main;
    stats.truth_turn = run.label_turn;
    stats.truth_theta = run.theta;
    stats.pred_main = pred_main;
    stats.pred_turn = pred_turn;
    stats.pred_theta = pred_theta;
    stats = compute_run_metrics(stats);
end

function state = apply_variant_overrides(state, variant)
    % 将变体中的 dwell_main/dwell_turn/tau_theta 覆盖到 state
    if isfield(variant,'dwell_main')
        state.dwell_main = variant.dwell_main;
        state.dwell_main_steps = max(1, round(state.dwell_main / state.Ts));
    end
    if isfield(variant,'dwell_turn')
        state.dwell_turn = variant.dwell_turn;
        state.dwell_turn_steps = max(1, round(state.dwell_turn / state.Ts));
    end
    if isfield(variant,'tau_theta')
        state.tau_theta = variant.tau_theta;
        state.alpha_theta = state.Ts / (state.tau_theta + state.Ts);
    end
end

function stats = compute_run_metrics(sim)
    % 针对单条 run 的预测与真值，计算准确率、延时、抖动等指标
    time = sim.time;
    N = numel(time);
    start_idx = min(N, sim.seq_len + 1);
    idx = start_idx:N;
    if isempty(idx)
        idx = 1:N;
    end
    duration = time(end) - time(idx(1));
    stats.acc_main = mean(sim.pred_main(idx) == sim.truth_main(idx));
    stats.acc_turn = mean(sim.pred_turn(idx) == sim.truth_turn(idx));
    slope_mask = (sim.truth_main(idx) == 4);
    if any(slope_mask)
        stats.theta_mae = mean(abs(sim.pred_theta(idx(slope_mask)) - sim.truth_theta(idx(slope_mask))));
    else
        stats.theta_mae = NaN;
    end
    stats.delay_slope = compute_delay(sim.truth_main, sim.pred_main, time, 4);
    stats.delay_slip  = compute_delay(sim.truth_main, sim.pred_main, time, 2);
    stats.delay_turn  = compute_delay(sim.truth_turn, sim.pred_turn, time, 1); % left turn
    if isempty(idx) || numel(idx)<2
        stats.flip_rate = 0;
    else
        flips = sum(sim.pred_main(idx(2:end)) ~= sim.pred_main(idx(1:end-1)));
        stats.flip_rate = flips / max(duration, eps);
    end
end

function delay = compute_delay(truth_signal, pred_signal, time, target_label)
    % 计算指定标签首次出现的时间差，若缺失则返回 NaN
    truth_idx = find(truth_signal == target_label, 1, 'first');
    pred_idx  = find(pred_signal == target_label, 1, 'first');
    if isempty(truth_idx) || isempty(pred_idx)
        delay = NaN;
    else
        delay = time(pred_idx) - time(truth_idx);
    end
end

function metrics = aggregate_metrics(run_stats, variant, cfg)
    % 将多条 run 的结果取平均，并给出综合得分
    fields = {'acc_main','acc_turn','theta_mae','delay_slope','delay_slip','delay_turn','flip_rate'};
    aggregated = struct();
    for i = 1:numel(fields)
        f = fields{i};
        values = [run_stats.(f)];
        aggregated.(f) = mean(values, 'omitnan');
    end
    metrics = aggregated;
    metrics.variant = variant;
    metrics.theta_mae_deg = rad2deg(metrics.theta_mae);
    metrics.flip_rate_per_min = metrics.flip_rate * 60;
    metrics.delay_combined = mean([metrics.delay_slope, metrics.delay_slip], 'omitnan');
    if isnan(metrics.delay_combined)
        metrics.delay_combined = 0;
    end
    metrics.score = compute_score(metrics, cfg.weights);
end

function score = compute_score(m, w)
    % 根据设定权重计算综合得分，越大越好
    score = w.acc_main * m.acc_main + ...
            w.acc_turn * m.acc_turn - ...
            w.delay    * max(m.delay_combined, 0) - ...
            w.theta    * max(m.theta_mae_deg, 0) - ...
            w.flips    * max(m.flip_rate_per_min, 0);
end

function key = variant_key(v)
    % 构造缓存键，确保不同组合唯一
    key = sprintf('dm%.3f_dt%.3f_tt%.3f', v.dwell_main, v.dwell_turn, v.tau_theta);
end

function scoreboard = collect_metrics(metrics_map)
    % 将 map 中的结构转为数组，便于排序
    keys = metrics_map.keys;
    vals = cellfun(@(k) metrics_map(k), keys, 'UniformOutput', false);
    scoreboard = [vals{:}];
end

function [selected_runs, meta] = select_runs_for_latency(runs, per_mode)
    % 按行驶模式均匀抽样，保证各类场景均有覆盖
    num_runs = numel(runs);
    mode_names = cell(num_runs,1);
    for i = 1:num_runs
        mode_names{i} = get_scene_name(runs(i));
    end
    unique_modes = unique(mode_names);
    idx_list = [];
    for m = 1:numel(unique_modes)
        mask = strcmp(mode_names, unique_modes{m});
        mode_idx = find(mask);
        take = mode_idx(1:min(per_mode, numel(mode_idx)));
        idx_list = [idx_list; take(:)]; %#ok<AGROW>
    end
    idx_list = unique(idx_list);
    selected_runs = runs(idx_list);
    meta = struct('indices', idx_list, 'num_modes', numel(unique_modes));
end

function name = get_scene_name(source)
    % 递归解析 run 元数据中的场景名称，兼容多种字段
    default_name = 'run_unknown';
    name = default_name;
    text = extract_scene_text(source);
    if ~isempty(text)
        name = text;
        return;
    end
    if ~isstruct(source)
        return;
    end
    fields = {'scene','path_type','scene_name','mode'};
    for i = 1:numel(fields)
        if isfield(source, fields{i})
            text = extract_scene_text(source.(fields{i}));
            if ~isempty(text)
                name = text;
                return;
            end
        end
    end
    nested = {'meta','path_params'};
    for i = 1:numel(nested)
        if isfield(source, nested{i})
            name = get_scene_name(source.(nested{i}));
            if ~strcmp(name, default_name)
                return;
            end
        end
    end
end

function text = extract_scene_text(value)
    % 提取字符串表示，兼容 char/string/cellstr
    text = '';
    if ischar(value)
        text = strtrim(value);
    elseif isstring(value) && isscalar(value)
        text = strtrim(char(value));
    elseif iscell(value) && numel(value)==1
        text = extract_scene_text(value{1});
    end
end
