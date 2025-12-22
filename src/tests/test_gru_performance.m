% =============================
% 文件名：test_gru_performance.m
% 版本号：V1.0
% 最后修改时间：2025-11-24
% 作者：LPV-MPC Project
% 功能描述：
%   统一评估 GRU 工况识别模型在不同数据集切分（Train/Val/Test）
%   及真实 run 数据上的性能，输出分类/回归/延迟等综合指标。
%   在线阶段会按行驶模式自动抽取 cfg.runs_per_mode 条 run 进行评估。
% 使用方法：
%   >> test_gru_performance();
%   >> cfg = struct('results_dir','GRU_eval_seq64','runs_per_mode',8);
%   >> test_gru_performance(cfg);
% 输出：
%   - split_<name>_metrics.mat：离线集指标
%   - online_eval_<scene>.png：run 级别曲线
%   - GRU_eval_summary_<timestamp>.mat：指标汇总
% 依赖：
%   - GRU_model.mat / GRU_dataset_processed.mat / GRU_train_data_full.mat
%   - GRU_infer.m / GRU_state_classifier.m / parameters.m
% 备注：
%   - cfg 允许覆盖模型路径、run 索引、seq_len、是否绘图等
%   - 所有结果会写入 cfg.results_dir 便于版本对比
% =============================

function summary = test_gru_performance(cfg)

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
data_gru_dir = fullfile(root, 'data', 'gru');
default_results_dir = results_dir('gru/eval_reports');

if nargin < 1 || isempty(cfg)
    cfg = struct();
end

% 使用项目统一默认值补齐配置项
cfg = apply_defaults(cfg, struct( ...
    'model_file',          fullfile(data_models_dir, 'GRU_model.mat'), ...
    'dataset_file',        fullfile(data_gru_dir, 'GRU_dataset_processed.mat'), ...
    'raw_data_file',       fullfile(data_gru_dir, 'GRU_train_data_full.mat'), ...
    'results_dir',         default_results_dir, ...
    'num_offline_samples', inf, ...
    'run_indices',         [], ...
    'runs_per_mode',       10, ...
    'seq_len_override',    [], ...
    'enable_plots',        true ...
));

fprintf('\n===============================================\n');
fprintf('GRU 模型性能评估 (test_gru_performance)\n');
fprintf('===============================================\n');

%% 0. 依赖检查与输出目录准备
% 确保所有必需文件存在，避免运行过程中断
req_files = {cfg.model_file, cfg.dataset_file, cfg.raw_data_file, ...
    'GRU_infer.m', 'GRU_state_classifier.m', 'parameters.m'};
for i = 1:numel(req_files)
    if ~exist(req_files{i}, 'file')
        error('缺少必要文件: %s', req_files{i});
    end
end
if ~exist(cfg.results_dir, 'dir')
    mkdir(cfg.results_dir);
end

params = parameters();

%% 1. 加载模型与数据集
% 模型包含 seq_len/scaler 信息，数据集含 Train/Val/Test 切分
fprintf('\n[1/4] 加载模型和数据集...\n');
model = load(cfg.model_file, 'model');
model = model.model;
data = load(cfg.dataset_file, 'dataset');
dataset = data.dataset;

if isfield(model, 'seq_len')
    seq_len_model = model.seq_len;
else
    seq_len_model = size(dataset.X_train, 2);
end
if ~isempty(cfg.seq_len_override) && cfg.seq_len_override ~= seq_len_model
    warning('当前模型 seq_len=%d，与 cfg.seq_len_override=%d 不一致。请确认模型/数据是否与新 seq_len 匹配。', ...
        seq_len_model, cfg.seq_len_override);
end
seq_len = seq_len_model;
fprintf('  模型特征维度: %d, 序列长度: %d\n', size(model.scaler.mean, 2), seq_len);

%% 2. 离线评估：训练/验证/测试
% 针对三类切分分别统计分类准确率、混淆矩阵、坡度 MAE
splits = { ...
    struct('name','Train','X',dataset.X_train,'y_main',dataset.y_main_train,'y_turn',dataset.y_turn_train, ...
           'y_theta',dataset.y_theta_train,'mask_theta',dataset.mask_theta_train), ...
    struct('name','Val','X',dataset.X_val,'y_main',dataset.y_main_val,'y_turn',dataset.y_turn_val, ...
           'y_theta',dataset.y_theta_val,'mask_theta',dataset.mask_theta_val), ...
    struct('name','Test','X',dataset.X_test,'y_main',dataset.y_main_test,'y_turn',dataset.y_turn_test, ...
           'y_theta',dataset.y_theta_test,'mask_theta',dataset.mask_theta_test) ...
};

split_reports = cell(numel(splits), 1);
for i = 1:numel(splits)
    split_reports{i} = evaluate_split(splits{i}, model, cfg.num_offline_samples);
    save(fullfile(cfg.results_dir, sprintf('split_%s_metrics.mat', lower(splits{i}.name))), 'split_reports');
end

%% 3. 在线评估：按行驶模式分组抽样
% 每种模式最多抽取 cfg.runs_per_mode 条 run，衡量驻留/滤波后的表现
fprintf('\n[3/4] 在线评估（按行驶模式分组）...\n');
raw_data = load(cfg.raw_data_file, 'data');
runs = raw_data.data.runs;
total_runs = numel(runs);
if total_runs == 0
    warning('原始 run 数据为空，跳过在线评估。');
end

% 候选索引：若用户提供 run_indices，则先筛选；否则使用全部 run
candidate_idx = 1:total_runs;
if ~isempty(cfg.run_indices)
    user_idx = unique(cfg.run_indices);
    user_idx = user_idx(user_idx >= 1 & user_idx <= total_runs);
    if isempty(user_idx)
        warning('cfg.run_indices 未匹配到有效 run，将回退到全部数据。');
    else
        candidate_idx = user_idx;
    end
end

% 统计候选样本对应的行驶模式
mode_labels = cell(numel(candidate_idx), 1);
for n = 1:numel(candidate_idx)
    mode_labels{n} = get_scene_name(runs(candidate_idx(n)));
end
unique_modes = unique(mode_labels);

all_online_reports = {};
mode_entries = struct('mode', {}, 'indices', {}, 'reports', {});
for m = 1:numel(unique_modes)
    mode = unique_modes{m};
    mode_mask = strcmp(mode_labels, mode);
    mode_idx = candidate_idx(mode_mask);
    if isempty(mode_idx)
        continue;
    end
    select_count = min(cfg.runs_per_mode, numel(mode_idx));
    selected_idx = mode_idx(1:select_count);
    fprintf('  模式 %-15s: 选择 %2d/%2d 条 run\n', mode, select_count, numel(mode_idx));
    mode_reports = cell(select_count, 1);
    for j = 1:select_count
        idx = selected_idx(j);
        mode_reports{j} = evaluate_run(runs(idx), model, params, seq_len, cfg.enable_plots, cfg.results_dir);
        all_online_reports{end+1,1} = mode_reports{j}; %#ok<AGROW>
    end
    mode_entries(end+1) = struct('mode', mode, 'indices', selected_idx, 'reports', {mode_reports}); %#ok<AGROW>
end

if isempty(all_online_reports)
    warning('未选择到任何 run 进行在线评估，请检查数据或配置。');
end


%% 4. 汇总并保存
% 将离线/在线结果融合，便于 seq_len 或 retrain 对比
fprintf('\n[4/4] 汇总指标并保存...\n');
summary = build_summary(split_reports, all_online_reports, mode_entries, seq_len);
summary.config = cfg;
summary.timestamp = datestr(now, 'yyyy-mm-dd_HHMMSS');
save(fullfile(cfg.results_dir, sprintf('GRU_eval_summary_%s.mat', summary.timestamp)), 'summary');

fprintf('\n评估完成，关键指标：\n');
print_summary(summary);

end

%% ======================================================================
function rpt = evaluate_split(split, model, sample_limit)
% 针对单个数据集切分执行离线推理，输出分类/回归指标
name = split.name;
X = split.X;
y_main = split.y_main;
y_turn = split.y_turn;
y_theta = split.y_theta;
mask_theta = split.mask_theta;
num_samples = size(X, 1);
if isfinite(sample_limit)
    num_samples = min(num_samples, sample_limit);
end
fprintf('  [%s] 样本数: %d\n', name, num_samples);

pred_main = zeros(num_samples, 1);
pred_turn = zeros(num_samples, 1);
pred_theta = zeros(num_samples, 1);
conf_main = zeros(num_samples, 1);

for i = 1:num_samples
    seq = squeeze(X(i, :, :));
    % 单条序列送入 GRU_infer，获得三任务输出与置信度
    [label_main, label_turn, theta_hat, conf] = GRU_infer(seq, model);
    pred_main(i) = label_main;
    pred_turn(i) = label_turn;
    pred_theta(i) = theta_hat;
    conf_main(i) = max(conf.conf_main);
end

metrics_main = classification_metrics(y_main(1:num_samples), pred_main, {'flat','slip','stall','slope'});
metrics_turn = classification_metrics(y_turn(1:num_samples) + 2, pred_turn + 2, {'right','straight','left'});

% 坡度 MAE 仅对 slope 样本
theta_idx = find(mask_theta(1:num_samples) > 0);
if isempty(theta_idx)
    mae_theta = NaN;
else
    mae_theta = mean(abs(pred_theta(theta_idx) - y_theta(theta_idx)));
end

rpt = struct();
rpt.name = name;
rpt.num_samples = num_samples;
rpt.metrics_main = metrics_main;
rpt.metrics_turn = metrics_turn;
rpt.mae_theta = mae_theta;
rpt.avg_confidence = mean(conf_main);

fprintf('    主分类准确率: %.2f%% | MAE_theta: %.3f deg\n', metrics_main.accuracy*100, rad2deg(mae_theta));
end

%% ======================================================================
function rpt = evaluate_run(run_data, model, params, seq_len, enable_plots, results_dir)
% 真实 run 数据评估：调用在线分类器，统计准确率/延迟并可视化
state = GRU_state_classifier('init', params, model);
N = size(run_data.y_raw, 1);
out_main = zeros(N,1);
out_turn = zeros(N,1);
out_theta = zeros(N,1);
for k = 1:N
    y = run_data.y_raw(k, :)';
    % 逐样本更新在线分类器内部状态
    [state, out] = GRU_state_classifier('update', state, y);
    out_main(k) = out.label_main;
    out_turn(k) = out.label_turn;
    out_theta(k) = out.theta_hat;
end

truth_main = run_data.label_main;
truth_turn = run_data.label_turn;
truth_theta = run_data.theta;
time = run_data.t;
start_idx = min(N, seq_len + 1);

rpt = struct();
rpt.scene = get_scene_name(run_data);
rpt.duration = time(end);
rpt.acc_main = mean(out_main(start_idx:end) == truth_main(start_idx:end));
rpt.acc_turn = mean(out_turn(start_idx:end) == truth_turn(start_idx:end));
slope_mask = truth_main(start_idx:end) == 4;
if any(slope_mask)
    slope_idx = find(slope_mask) + start_idx - 1;
    rpt.mae_theta = mean(abs(out_theta(slope_idx) - truth_theta(slope_idx)));
else
    rpt.mae_theta = NaN;
end

% 检测延迟：真值首次进入 slope 与预测首次进入 slope 的时间差
truth_slope_idx = find(truth_main == 4, 1, 'first');
pred_slope_idx = find(out_main == 4, 1, 'first');
if ~isempty(truth_slope_idx) && ~isempty(pred_slope_idx)
    rpt.slope_delay = time(pred_slope_idx) - time(truth_slope_idx);
else
    rpt.slope_delay = NaN;
end

if enable_plots
    fig = figure('Name', sprintf('GRU在线评估-%s', rpt.scene), 'Position', [100 100 1200 800]);
    tiledlayout(3,1,'Padding','compact');
    % 主分类对比
    nexttile; hold on; grid on;
    plot(time, truth_main, 'k','LineWidth',2);
    plot(time, out_main, 'r--','LineWidth',1.2);
    yticks(1:4); yticklabels({'flat','slip','stall','slope'});
    ylabel('主分类'); title(sprintf('%s | 主分类准确率 %.2f%%', rpt.scene, rpt.acc_main*100));
    % 转弯分类对比
    nexttile; hold on; grid on;
    plot(time, truth_turn, 'k','LineWidth',2);
    plot(time, out_turn, 'b--','LineWidth',1.2);
    yticks(-1:1); yticklabels({'right','straight','left'});
    ylabel('转弯'); title(sprintf('转弯准确率 %.2f%%', rpt.acc_turn*100));
    % 坡度角估计曲线
    nexttile; hold on; grid on;
    plot(time, rad2deg(truth_theta), 'k','LineWidth',2);
    plot(time, rad2deg(out_theta), 'g--','LineWidth',1.2);
    ylabel('\theta [deg]'); xlabel('时间 [s]');
    title(sprintf('坡度估计 MAE %.3f deg | 延迟 %.2f s', rad2deg(rpt.mae_theta), rpt.slope_delay));
    saveas(fig, fullfile(results_dir, sprintf('online_eval_%s.png', rpt.scene)));
    close(fig);
end

end

%% ======================================================================
function metrics = classification_metrics(y_true, y_pred, class_names)
% 统一计算准确率、精确率、召回率、F1 以及混淆矩阵
cm = confusionmat(y_true(:), y_pred(:));
num_classes = size(cm,1);
precision = zeros(num_classes,1);
recall = zeros(num_classes,1);
f1 = zeros(num_classes,1);
for c = 1:num_classes
    tp = cm(c,c);
    fp = sum(cm(:,c)) - tp;
    fn = sum(cm(c,:)) - tp;
    precision(c) = tp / max(tp + fp, eps);
    recall(c) = tp / max(tp + fn, eps);
    f1(c) = 2 * precision(c) * recall(c) / max(precision(c) + recall(c), eps);
end
metrics = struct();
metrics.accuracy = sum(diag(cm)) / sum(cm(:));
metrics.confusion = cm;
metrics.precision = precision;
metrics.recall = recall;
metrics.f1 = f1;
metrics.class_names = class_names(:)';
end

%% ======================================================================
function summary = build_summary(split_reports, online_reports, online_by_mode, seq_len)
% 聚合离线/在线指标，用于最终对比展示
summary = struct();
summary.seq_len = seq_len;
summary.offline = split_reports;
summary.online = online_reports;
summary.online_by_mode = online_by_mode;
summary.mean_acc_main = mean(cellfun(@(r) r.metrics_main.accuracy, split_reports));
summary.mean_mae_theta = mean(cellfun(@(r) r.mae_theta, split_reports));
if isempty(online_reports)
    summary.mean_online_delay = NaN;
else
    summary.mean_online_delay = mean(cellfun(@(r) r.slope_delay, online_reports), 'omitnan');
end
end

%% ======================================================================
function print_summary(summary)
% 终端输出核心指标，方便快速查看
fprintf('  - 平均主分类准确率（Train/Val/Test）：%.2f%%\n', summary.mean_acc_main*100);
fprintf('  - 平均离线坡度 MAE：%.3f deg\n', rad2deg(summary.mean_mae_theta));
if isnan(summary.mean_online_delay)
    fprintf('  - 平均在线坡度识别延迟：NaN（本次未选择到含坡度的 run） (seq_len=%.0f)\n', summary.seq_len);
else
    fprintf('  - 平均在线坡度识别延迟：%.2f s (seq_len=%.0f)\n', summary.mean_online_delay, summary.seq_len);
end
print_mode_breakdown(summary.online_by_mode);
end

%% ======================================================================
function print_mode_breakdown(mode_entries)
% 输出按行驶模式分组的在线评估结果
if isempty(mode_entries)
    fprintf('  - 未选择任何行驶模式样本，跳过在线分组统计。\n');
    return;
end

fprintf('\n  行驶模式分组指标：\n');
for i = 1:numel(mode_entries)
    reports_cell = mode_entries(i).reports;
    if isempty(reports_cell)
        continue;
    end
    reports = [reports_cell{:}];
    acc_main = mean(arrayfun(@(r) r.acc_main, reports));
    acc_turn = mean(arrayfun(@(r) r.acc_turn, reports));
    mae_theta = mean(arrayfun(@(r) r.mae_theta, reports), 'omitnan');
    delay = mean(arrayfun(@(r) r.slope_delay, reports), 'omitnan');
    fprintf('    - %-15s | 样本:%2d | 主分类:%.2f%%%% | 转弯:%.2f%%%% | θ MAE:%.3f deg | 延迟:%s\n', ...
        mode_entries(i).mode, numel(reports), acc_main*100, acc_turn*100, rad2deg(mae_theta), format_delay(delay));
end
end

function txt = format_delay(delay)
if isnan(delay)
    txt = 'NaN';
else
    txt = sprintf('%.2f s', delay);
end
end

%% ======================================================================
function name = get_scene_name(source)
% 从 run/元数据中解析场景名称，兼容嵌套结构与不同字段命名
default_name = 'run_unknown';
name = default_name;

if nargin == 0 || isempty(source)
    return;
end

% 直接传入字符串时立即返回
direct_text = extract_scene_text(source);
if ~isempty(direct_text)
    name = direct_text;
    return;
end

if ~isstruct(source)
    return;
end

text_fields = {'scene','path_type','scene_name','mode'};
for i = 1:numel(text_fields)
    field = text_fields{i};
    if isfield(source, field)
        candidate = extract_scene_text(source.(field));
        if ~isempty(candidate)
            name = candidate;
            return;
        end
    end
end

% 递归查找常见嵌套字段
nested_fields = {'meta','path_params'};
for i = 1:numel(nested_fields)
    field = nested_fields{i};
    if isfield(source, field)
        candidate = get_scene_name(source.(field));
        if ~strcmp(candidate, default_name)
            name = candidate;
            return;
        end
    end
end

end

function text = extract_scene_text(value)
% 统一提取字符串表示，兼容 char/string/cellstr
text = '';
if ischar(value)
    text = strtrim(value);
elseif isstring(value) && isscalar(value)
    text = strtrim(char(value));
elseif iscell(value) && numel(value) == 1
    text = extract_scene_text(value{1});
end

if isstring(text)
    text = char(text);
end

if isempty(text)
    text = '';
end
end

%% ======================================================================
function cfg = apply_defaults(cfg, defaults)
% 递归填充缺省配置项，保持主逻辑简洁
fields = fieldnames(defaults);
for i = 1:numel(fields)
    f = fields{i};
    if ~isfield(cfg, f) || isempty(cfg.(f))
        cfg.(f) = defaults.(f);
    end
end
end
