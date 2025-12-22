% =============================
% 文件名：test_gru_filter_constants.m
% 版本号：V1.0
% 最后修改时间：2025-11-26
% 作者：LPV-MPC Project
% 功能描述：
%   在手动修改 GRU 输入侧一阶低通 (tau_accel_lp) 与差分滤波 (tau_diff)
%   时间常数后，快速对在线推理性能做一次离线 run 级评估。
%   该脚本不会自动改写数据集/模型，只会基于当前模型覆写 scaler
%   中的滤波时间常数，然后调用 GRU_state_classifier 计算指标。
%
% 使用方法：
%   1. 根据需要在 "配置" 区域填写 override 数值（单位：秒）。
%      如果留空 ([])，脚本会直接采用当前模型中的时间常数。
%   2. 运行本脚本：>> test_gru_filter_constants
%   3. 评估结果会打印在命令行，并保存到 cfg.results_dir。
%
% 注意事项：
%   - 如需彻底生效，应在修改完时间常数后重新执行
%     GRU_prepare_dataset → GRU_train.m，以便 scaler / 模型内的数值同步。
%   - 本脚本仅用于实验性对比，覆盖范围为 `cfg.runs_per_mode`
%     指定的每种行驶模式样本，运行代价可控。
% =============================

clear; clc;

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
data_gru_dir = fullfile(root, 'data', 'gru');
default_results_dir = results_dir('gru/filter_constant_eval');
fprintf('\n===============================================\n');
fprintf('GRU 滤波时间常数评估 (test_gru_filter_constants)\n');
fprintf('===============================================\n');

%% 配置
cfg = struct();
cfg.model_file            = fullfile(data_models_dir, 'GRU_model.mat');
cfg.raw_data_file         = fullfile(data_gru_dir, 'GRU_train_data_full.mat');
cfg.results_dir           = default_results_dir;
cfg.runs_per_mode         = 10;        % 每个行驶模式抽取的 run 数量
cfg.tau_accel_lp_override = [];        % 例如 0.30（秒）；为空则使用模型值
cfg.tau_diff_override     = [];        % 例如 0.25（秒）；为空则使用模型值
cfg.save_timeseries       = false;     % 若需调试可开启，保存预测/真值轨迹

if ~exist(cfg.results_dir,'dir')
    mkdir(cfg.results_dir);
end

%% 加载模型、数据并应用 override
fprintf('[1/4] 加载模型与数据...\n');
params = parameters();
model_data = load(cfg.model_file, 'model');
model = model_data.model;
raw = load(cfg.raw_data_file, 'data');
all_runs = raw.data.runs;

if ~isempty(cfg.tau_accel_lp_override)
    model.scaler.tau_accel_lp = cfg.tau_accel_lp_override;
    fprintf('  - 覆写 tau_accel_lp = %.3f s\n', model.scaler.tau_accel_lp);
elseif isfield(model.scaler, 'tau_accel_lp')
    fprintf('  - 使用模型中的 tau_accel_lp = %.3f s\n', model.scaler.tau_accel_lp);
else
    warning('model.scaler 缺少 tau_accel_lp（将 fallback 至 0.4s）');
end

if ~isempty(cfg.tau_diff_override)
    model.scaler.tau_diff = cfg.tau_diff_override;
    fprintf('  - 覆写 tau_diff = %.3f s\n', model.scaler.tau_diff);
elseif isfield(model.scaler, 'tau_diff')
    fprintf('  - 使用模型中的 tau_diff = %.3f s\n', model.scaler.tau_diff);
else
    warning('model.scaler 缺少 tau_diff（将 fallback 至 0.3s）');
end

[selected_runs, selection_meta] = select_runs_for_filter_eval(all_runs, cfg.runs_per_mode);
if isempty(selected_runs)
    error('未选到任何 run，请检查原始数据。');
end
fprintf('  - 选取 %d 条 run，覆盖 %d 种行驶模式\n', numel(selected_runs), selection_meta.num_modes);

%% 逐 run 仿真与统计
fprintf('\n[2/4] 逐 run 仿真...\n');
run_stats = arrayfun(@(r) simulate_run(r, params, model, cfg), selected_runs);

%% 聚合指标
fprintf('\n[3/4] 聚合指标...\n');
metrics = aggregate_metrics(run_stats);
print_metrics_table(metrics);

%% 保存结果
fprintf('\n[4/4] 保存结果...\n');
timestamp = datestr(now,'yyyymmdd_HHMMSS');
summary = struct();
summary.cfg = cfg;
summary.metrics = metrics;
summary.selection_meta = selection_meta;
summary.run_stats = run_stats;
summary.model_scaler = model.scaler;
summary_file = fullfile(cfg.results_dir, sprintf('filter_eval_%s.mat', timestamp));
save(summary_file, '-struct', 'summary');
fprintf('  ✓ 已保存至 %s\n', summary_file);

fprintf('\n评估完成。可结合不同的 tau_* override 数值多次运行本脚本，比较输出指标。\n');

%% =====================================================================
function [selected_runs, meta] = select_runs_for_filter_eval(runs, per_mode)
% 与 test_gru_latency 同理念：尽量覆盖不同场景
    if per_mode <= 0
        selected_runs = runs;
        meta.num_modes = numel(unique({runs.scene}));
        return;
    end
    groups = struct();
    for i = 1:numel(runs)
        scene = get_scene_name(runs(i));
        if ~isfield(groups, scene)
            groups.(scene) = [];
        end
        groups.(scene) = [groups.(scene), i];
    end
    scenes = fieldnames(groups);
    selected_idx = [];
    for i = 1:numel(scenes)
        idx = groups.(scenes{i});
        take = min(numel(idx), per_mode);
        selected_idx = [selected_idx, idx(1:take)]; %#ok<AGROW>
    end
    selected_runs = runs(selected_idx);
    meta.num_modes = numel(scenes);
end

function name = get_scene_name(run)
    name = 'unknown';
    if isfield(run,'scene') && ~isempty(run.scene)
        name = run.scene;
    elseif isfield(run,'meta') && isfield(run.meta,'scene')
        name = run.meta.scene;
    end
end

function stats = simulate_run(run, params, model, cfg)
% 复用 GRU_state_classifier 的 init/update，返回关键指标
    state = GRU_state_classifier('init', params, model);
    N = size(run.y_raw, 1);
    out_main = zeros(N,1);
    out_turn = zeros(N,1);
    out_theta = zeros(N,1);
    for k = 1:N
        y = run.y_raw(k,:)';
        [state, out] = GRU_state_classifier('update', state, y);
        out_main(k) = out.label_main;
        out_turn(k) = out.label_turn;
        out_theta(k) = out.theta_hat;
    end
    stats.scene = get_scene_name(run);
    stats.time = run.t;
    stats.truth_main = run.label_main;
    stats.truth_turn = run.label_turn;
    stats.truth_theta = run.theta;
    stats.pred_main = out_main;
    stats.pred_turn = out_turn;
    stats.pred_theta = out_theta;
    stats.seq_len = state.seq_len;
    stats = compute_metrics(stats);
    if cfg.save_timeseries
        stats.timeseries = struct('time', stats.time, ...
            'pred_main', out_main, 'truth_main', run.label_main, ...
            'pred_turn', out_turn, 'truth_turn', run.label_turn, ...
            'pred_theta', out_theta, 'truth_theta', run.theta);
    end
end

function stats = compute_metrics(sim)
    time = sim.time;
    N = numel(time);
    start_idx = min(N, sim.seq_len + 1);
    idx = start_idx:N;
    if isempty(idx)
        idx = 1:N;
    end
    duration = time(idx(end)) - time(idx(1));
    stats = struct();
    stats.scene = sim.scene;
    stats.acc_main = mean(sim.pred_main(idx) == sim.truth_main(idx));
    stats.acc_turn = mean(sim.pred_turn(idx) == sim.truth_turn(idx));
    slope_mask = sim.truth_main(idx) == 4;
    if any(slope_mask)
        stats.theta_mae = mean(abs(sim.pred_theta(idx(slope_mask)) - sim.truth_theta(idx(slope_mask))));
    else
        stats.theta_mae = NaN;
    end
    stats.delay_slope = compute_delay(sim.truth_main, sim.pred_main, time, 4);
    stats.delay_slip  = compute_delay(sim.truth_main, sim.pred_main, time, 2);
    stats.delay_turn  = compute_delay(sim.truth_turn, sim.pred_turn, time, 1);
    if numel(idx) < 2
        stats.flip_rate = 0;
    else
        flips = sum(sim.pred_main(idx(2:end)) ~= sim.pred_main(idx(1:end-1)));
        stats.flip_rate = flips / max(duration, eps);
    end
end

function delay = compute_delay(truth_signal, pred_signal, time, label)
    truth_idx = find(truth_signal == label, 1, 'first');
    pred_idx  = find(pred_signal == label, 1, 'first');
    if isempty(truth_idx) || isempty(pred_idx)
        delay = NaN;
    else
        delay = time(pred_idx) - time(truth_idx);
    end
end

function metrics = aggregate_metrics(run_stats)
    fields = {'acc_main','acc_turn','theta_mae','delay_slope','delay_slip','delay_turn','flip_rate'};
    metrics = struct();
    for i = 1:numel(fields)
        f = fields{i};
        values = [run_stats.(f)];
        metrics.(f) = mean(values, 'omitnan');
    end
    metrics.theta_mae_deg = rad2deg(metrics.theta_mae);
    metrics.flip_rate_per_min = metrics.flip_rate * 60;
end

function print_metrics_table(m)
    fprintf('\n=== 滤波参数评估指标 ===\n');
    fprintf('主分类准确率   : %.3f\n', m.acc_main);
    fprintf('转弯准确率     : %.3f\n', m.acc_turn);
    fprintf('θ MAE (deg)     : %.3f\n', m.theta_mae_deg);
    fprintf('Slope 延迟 (s) : %.3f\n', m.delay_slope);
    fprintf('Slip 延迟 (s)  : %.3f\n', m.delay_slip);
    fprintf('Turn 延迟 (s)  : %.3f\n', m.delay_turn);
    fprintf('抖动 (次/分钟) : %.2f\n', m.flip_rate_per_min);
end
