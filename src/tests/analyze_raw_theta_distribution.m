% analyze_raw_theta_distribution.m
% 用途：快速查看“未预处理原始数据”与“预处理后数据集”中的坡度角分布，输出图像和命令行统计。
% 用法示例：
%   run('src/tests/analyze_raw_theta_distribution.m');
%   cfg = struct('data_file','data/gru/GRU_train_data_full.mat', ...
%                'dataset_file','data/gru/GRU_dataset_processed.mat', ...
%                'output_dir','results/gru/raw_theta', ...
%                'bin_width_deg',1.0, ...
%                'theta_limits_deg',[-12 12]);
%   analyze_raw_theta_distribution(cfg);

function analyze_raw_theta_distribution(cfg)
if nargin < 1 || isempty(cfg)
    cfg = struct();
end

root = project_root();
defaults = struct( ...
    'data_file', fullfile(root, 'data', 'gru', 'GRU_train_data_full.mat'), ...  % 原始未预处理数据
    'dataset_file', fullfile(root, 'data', 'gru', 'GRU_dataset_processed.mat'), ... % 预处理后的数据集
    'output_dir', fullfile(root, 'results', 'gru', 'raw_theta'), ...
    'bin_width_deg', 1.0, ...
    'theta_limits_deg', [] ...
);
cfg = apply_defaults(cfg, defaults);

if ~exist(cfg.output_dir, 'dir')
    mkdir(cfg.output_dir);
end

fprintf('\n[analyze_raw_theta_distribution] 加载原始数据: %s\n', cfg.data_file);
if ~exist(cfg.data_file, 'file')
    error('Data file not found: %s', cfg.data_file);
end
S = load(cfg.data_file, 'data');
data = S.data;

% 仅统计 slope 场景（原始数据），排除其他场景的 0° 样本干扰
all_theta = [];
scene_names = {}; scene_counts = [];
for k = 1:numel(data.runs)
    run = data.runs(k);
    if ~isfield(run, 'theta')
        error('Run %d missing field theta', k);
    end
    if ~isfield(run, 'scene') || ~strcmpi(run.scene, 'slope')
        continue;  % 只看 slope 场景
    end
    theta_k = run.theta(:);  % rad
    all_theta = [all_theta; theta_k]; %#ok<AGROW>
    s = run.scene;
    idx = find(strcmp(scene_names, s), 1);
    if isempty(idx)
        scene_names{end+1} = s; %#ok<AGROW>
        scene_counts(end+1) = numel(theta_k); %#ok<AGROW>
    else
        scene_counts(idx) = scene_counts(idx) + numel(theta_k);
    end
end

all_theta_deg = rad2deg(all_theta);
[edges, centers] = make_bin_edges(all_theta_deg, cfg.bin_width_deg, cfg.theta_limits_deg);

% 原始数据直方图
fig1 = figure('Name','theta_hist_raw','Position',[120 120 760 520]);
histogram(all_theta_deg, edges, 'FaceColor', [0.30 0.60 0.90]);
grid on;
xlabel('\theta [deg]'); ylabel('Count');
title(sprintf('Raw theta histogram | bin=%.2f deg | N=%d', cfg.bin_width_deg, numel(all_theta_deg)));
saveas(fig1, fullfile(cfg.output_dir, 'theta_hist_raw.png'));
close(fig1);

% 原始数据分箱计数与符号统计
bin_count = histcounts(all_theta_deg, edges);
summary.sign = [sum(all_theta_deg<0), sum(abs(all_theta_deg)<eps), sum(all_theta_deg>0)];
summary.total = numel(all_theta_deg);
summary.bin_edges = edges;
summary.bin_centers = centers;
summary.bin_count = bin_count;
summary.scene_names = scene_names;
summary.scene_counts = scene_counts;
summary.theta_min_deg = min(all_theta_deg);
summary.theta_max_deg = max(all_theta_deg);
save(fullfile(cfg.output_dir, 'theta_raw_summary.mat'), 'summary');

% 命令行输出统计
fprintf('  总样本数: %d\n', summary.total);
fprintf('  theta 最小/最大值 [deg]: %.3f / %.3f\n', summary.theta_min_deg, summary.theta_max_deg);
for i = 1:numel(scene_names)
    fprintf('  场景 %-22s : %d 样本\n', scene_names{i}, scene_counts(i));
end
fprintf('  按符号计数 [负,零,正]: [%d, %d, %d]\n', summary.sign(1), summary.sign(2), summary.sign(3));
print_bin_table(centers, bin_count, '原始数据分箱计数');

% 原始数据分箱柱状图
fig2 = figure('Name','theta_bin_counts_raw','Position',[140 140 820 520]);
bar(centers, bin_count, 0.9, 'FaceColor', [0.20 0.55 0.70]);
grid on;
xlabel('\theta bin center [deg]'); ylabel('Count');
title(sprintf('Bin counts | bin=%.2f deg | N=%d', cfg.bin_width_deg, numel(all_theta_deg)));
for i = 1:numel(centers)
    if bin_count(i) > 0
        text(centers(i), bin_count(i), sprintf('n=%d', bin_count(i)), ...
            'HorizontalAlignment','center', 'VerticalAlignment','bottom', 'FontSize',8);
    end
end
saveas(fig2, fullfile(cfg.output_dir, 'theta_bin_counts_raw.png'));
close(fig2);

fprintf('Figures and summary saved to: %s\n', cfg.output_dir);

%% ---------------- 预处理后数据集（slope-only） ----------------
fprintf('\n[analyze_raw_theta_distribution] 加载预处理数据集: %s\n', cfg.dataset_file);
if ~exist(cfg.dataset_file, 'file')
    warning('dataset_file 不存在，跳过预处理数据统计: %s', cfg.dataset_file);
    return;
end
Ds = load(cfg.dataset_file, 'dataset');
ds = Ds.dataset;

% 只统计 slope 样本（mask_theta=1），合并 train/val/test
y_theta_deg = rad2deg([ds.y_theta_train(:); ds.y_theta_val(:); ds.y_theta_test(:)]);
mask_theta = [ds.mask_theta_train(:); ds.mask_theta_val(:); ds.mask_theta_test(:)];
slope_theta_deg = y_theta_deg(mask_theta > 0);
[edges_p, centers_p] = make_bin_edges(slope_theta_deg, cfg.bin_width_deg, cfg.theta_limits_deg);
bin_count_p = histcounts(slope_theta_deg, edges_p);

fig3 = figure('Name','theta_hist_processed','Position',[160 160 760 520]);
histogram(slope_theta_deg, edges_p, 'FaceColor', [0.35 0.65 0.85]);
grid on;
xlabel('\theta [deg]'); ylabel('Count');
title(sprintf('Processed (slope-only) theta histogram | bin=%.2f deg | N=%d', cfg.bin_width_deg, numel(slope_theta_deg)));
saveas(fig3, fullfile(cfg.output_dir, 'theta_hist_processed.png'));
close(fig3);

fig4 = figure('Name','theta_bin_counts_processed','Position',[180 180 820 520]);
bar(centers_p, bin_count_p, 0.9, 'FaceColor', [0.22 0.58 0.72]);
grid on;
xlabel('\theta bin center [deg]'); ylabel('Count');
title(sprintf('Processed bin counts (slope-only) | bin=%.2f deg | N=%d', cfg.bin_width_deg, numel(slope_theta_deg)));
for i = 1:numel(centers_p)
    if bin_count_p(i) > 0
        text(centers_p(i), bin_count_p(i), sprintf('n=%d', bin_count_p(i)), ...
            'HorizontalAlignment','center', 'VerticalAlignment','bottom', 'FontSize',8);
    end
end
saveas(fig4, fullfile(cfg.output_dir, 'theta_bin_counts_processed.png'));
close(fig4);

summary_p = struct();
summary_p.total = numel(slope_theta_deg);
summary_p.bin_edges = edges_p;
summary_p.bin_centers = centers_p;
summary_p.bin_count = bin_count_p;
summary_p.theta_min_deg = min(slope_theta_deg);
summary_p.theta_max_deg = max(slope_theta_deg);
summary_p.sign = [sum(slope_theta_deg<0), sum(abs(slope_theta_deg)<eps), sum(slope_theta_deg>0)];
save(fullfile(cfg.output_dir, 'theta_processed_summary.mat'), 'summary_p');

fprintf('  slope-only 样本数: %d\n', summary_p.total);
fprintf('  theta 最小/最大值 [deg]: %.3f / %.3f\n', summary_p.theta_min_deg, summary_p.theta_max_deg);
fprintf('  按符号计数 [负,零,正]: [%d, %d, %d]\n', summary_p.sign(1), summary_p.sign(2), summary_p.sign(3));
print_bin_table(centers_p, bin_count_p, '预处理后 slope-only 分箱计数');

fprintf('Processed figures and summary saved to: %s\n', cfg.output_dir);
end

%% Helpers
function cfg = apply_defaults(cfg, defaults)
fields = fieldnames(defaults);
for i = 1:numel(fields)
    f = fields{i};
    if ~isfield(cfg, f) || isempty(cfg.(f))
        cfg.(f) = defaults.(f);
    end
end
end

function [edges, centers] = make_bin_edges(values_deg, bin_width_deg, manual_limits)
if isempty(values_deg)
    edges = [0 1];
    centers = 0.5;
    return;
end
if isempty(manual_limits)
    min_v = min(values_deg);
    max_v = max(values_deg);
else
    min_v = manual_limits(1);
    max_v = manual_limits(2);
end
min_edge = floor(min_v / bin_width_deg) * bin_width_deg;
max_edge = ceil(max_v / bin_width_deg) * bin_width_deg;
edges = min_edge:bin_width_deg:max_edge;
if numel(edges) < 2
    edges = [min_edge, min_edge + bin_width_deg];
end
centers = edges(1:end-1) + bin_width_deg / 2;
end

function print_bin_table(centers, counts, title_str)
% 命令行输出分箱计数表，便于快速查看覆盖情况
fprintf('  %s\n', title_str);
fprintf('    bin_center_deg    count\n');
for i = 1:numel(centers)
    if counts(i) > 0
        fprintf('    %8.2f          %5d\n', centers(i), counts(i));
    end
end
end
