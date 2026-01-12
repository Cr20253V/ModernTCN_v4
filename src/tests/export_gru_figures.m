% export_gru_figures.m
% Phase 0 quick diagnostics for slope-only subset:
%   1) theta_true histogram (check bin coverage / discretization)
%   2) binned MAE by theta_true bins

function export_gru_figures(cfg)

if nargin < 1 || isempty(cfg)
    cfg = struct();
end

root = project_root();
defaults = struct( ...
    'model_file',   fullfile(root, 'data', 'models', 'GRU_model.mat'), ...
    'dataset_file', fullfile(root, 'data', 'gru', 'GRU_dataset_processed.mat'), ...
    'output_dir',   fullfile(root, 'results', 'gru', 'diagnostics'), ...
    'bin_width_deg', 1.0, ...            % 1 deg bins by default (set 0.5 if needed)
    'theta_limits_deg', [] ...           % optional [min max] for bin edges
);
cfg = apply_defaults(cfg, defaults);

if ~exist(cfg.output_dir, 'dir')
    mkdir(cfg.output_dir);
end

fprintf('\n[export_gru_figures] Loading model and dataset...\n');
model_data = load(cfg.model_file, 'model');
dataset_data = load(cfg.dataset_file, 'dataset');
model = model_data.model;
dataset = dataset_data.dataset;

% slope-only subset
X = dataset.X_test;
y_theta = dataset.y_theta_test;           % radians
mask_theta = dataset.mask_theta_test;     % slope samples marked as 1
slope_idx = find(mask_theta > 0);
if isempty(slope_idx)
    warning('No slope samples in test set. Nothing to export.');
    return;
end

true_theta_deg = rad2deg(y_theta(slope_idx));
pred_theta_deg = zeros(numel(slope_idx), 1);

fprintf('  Inference on %d slope samples...\n', numel(slope_idx));
for k = 1:numel(slope_idx)
    seq = squeeze(X(slope_idx(k), :, :));
    [~, ~, theta_hat] = GRU_infer(seq, model);
    pred_theta_deg(k) = rad2deg(theta_hat);
end

err_deg = pred_theta_deg - true_theta_deg;
mae_deg = mean(abs(err_deg));
pos_mae = mean(abs(err_deg(true_theta_deg > 0)));
neg_mae = mean(abs(err_deg(true_theta_deg < 0)));

fprintf('  Overall slope-only MAE: %.4f deg\n', mae_deg);
fprintf('  Positive-slope MAE:     %.4f deg\n', pos_mae);
fprintf('  Negative-slope MAE:     %.4f deg\n', neg_mae);

[edges, centers] = make_bin_edges(true_theta_deg, cfg.bin_width_deg, cfg.theta_limits_deg);

%% Figure 1: theta_true histogram
fig1 = figure('Name','theta_true_hist','Position',[100 100 640 520]);
histogram(true_theta_deg, edges, 'FaceColor', [0.30 0.60 0.90]);
grid on;
xlabel('\theta_{true} [deg]'); ylabel('Count');
title(sprintf('theta_{true} histogram | bin=%.2f deg | N=%d', cfg.bin_width_deg, numel(true_theta_deg)));
saveas(fig1, fullfile(cfg.output_dir, 'theta_true_hist.png'));
close(fig1);

%% Figure 2: binned MAE by theta_true
bin_mae = nan(size(centers));
bin_count = zeros(size(centers));
for i = 1:numel(centers)
    in_bin = true_theta_deg >= edges(i) & true_theta_deg < edges(i+1);
    bin_count(i) = sum(in_bin);
    if bin_count(i) > 0
        bin_mae(i) = mean(abs(err_deg(in_bin)));
    end
end

fig2 = figure('Name','theta_binned_mae','Position',[120 120 720 520]);
bar(centers, bin_mae, 0.9, 'FaceColor', [0.20 0.55 0.70]);
grid on;
xlabel('\theta_{true} bin center [deg]'); ylabel('MAE [deg]');
title(sprintf('Binned MAE | bin=%.2f deg | overall MAE=%.3f deg', cfg.bin_width_deg, mae_deg));

% annotate sample count per bin
for i = 1:numel(centers)
    if bin_count(i) > 0 && ~isnan(bin_mae(i))
        text(centers(i), bin_mae(i), sprintf('n=%d', bin_count(i)), ...
            'HorizontalAlignment','center', 'VerticalAlignment','bottom', 'FontSize',9);
    end
end

saveas(fig2, fullfile(cfg.output_dir, 'theta_binned_mae.png'));
close(fig2);

fprintf('Figures saved to: %s\n', cfg.output_dir);
end

%% =====================================================================
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
end% export_gru_figures.m
% 离线评估并导出图表（无需重新训练）：
%  - 主工况三分类混淆矩阵
%  - 转弯三分类混淆矩阵
%  - 坡度回归散点一致性图（真值 vs 预测）
%  - 坡度回归误差分布（直方图 + CDF）
%
% 用法：
%   >> export_gru_figures();
%   >> cfg = struct('model_file','data/models/GRU_model.mat', ...
%                   'dataset_file','data/gru/GRU_dataset_processed.mat', ...
%                   'output_dir','results/gru/train_logs');
%   >> export_gru_figures(cfg);
%
% 依赖：
%   - GRU_model.mat（包含 dlnetwork、scaler、seq_len 等）
%   - GRU_dataset_processed.mat（含 Train/Val/Test 切分与 mask_theta）
%   - GRU_infer.m / project_root.m
%
function export_gru_figures(cfg)

if nargin < 1 || isempty(cfg)
    cfg = struct();
end

%% =====================================================================
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

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
data_gru_dir    = fullfile(root, 'data', 'gru');
output_default  = fullfile(root, 'results', 'gru', 'train_logs');

cfg = apply_defaults(cfg, struct( ...
    'model_file',   fullfile(data_models_dir, 'GRU_model.mat'), ...
    'dataset_file', fullfile(data_gru_dir, 'GRU_dataset_processed.mat'), ...
    'output_dir',   output_default ...
));

if ~exist(cfg.output_dir, 'dir')
    mkdir(cfg.output_dir);
end

fprintf('\n[export_gru_figures] 加载模型与数据集...\n');
model_data = load(cfg.model_file, 'model');
dataset_data = load(cfg.dataset_file, 'dataset');
model = model_data.model;
dataset = dataset_data.dataset;

% 取测试集
X = dataset.X_test;
y_main = dataset.y_main_test;
y_turn = dataset.y_turn_test;
y_theta = dataset.y_theta_test;
mask_theta = dataset.mask_theta_test; % slope 样本=1

num_samples = size(X, 1);
fprintf('  测试样本数: %d, 序列长度: %d, 特征维: %d\n', num_samples, size(X,2), size(X,3));

pred_main = zeros(num_samples, 1);
pred_turn = zeros(num_samples, 1);
pred_theta = zeros(num_samples, 1);

for i = 1:num_samples
    seq = squeeze(X(i, :, :));
    [label_main, label_turn, theta_hat] = GRU_infer(seq, model); %#ok<*ASGLU>
    pred_main(i) = label_main;
    pred_turn(i) = label_turn;
    pred_theta(i) = theta_hat;
end

%% 混淆矩阵（主工况）
labels_main = unique([y_main(:); pred_main(:)]);
main_names = guess_main_names(labels_main);
cm_main = confusionmat(y_main, pred_main, 'Order', labels_main);
save_confusion(cm_main, labels_main, main_names, '主工况混淆矩阵', fullfile(cfg.output_dir, 'confusion_main.png'));

%% 混淆矩阵（转弯）
labels_turn = unique([y_turn(:); pred_turn(:)]);
turn_names = guess_turn_names(labels_turn);
cm_turn = confusionmat(y_turn, pred_turn, 'Order', labels_turn);
save_confusion(cm_turn, labels_turn, turn_names, '转弯状态混淆矩阵', fullfile(cfg.output_dir, 'confusion_turn.png'));

%% 坡度回归评估
slope_idx = find(mask_theta > 0);
if isempty(slope_idx)
    warning('测试集中没有坡度样本，跳过坡度回归图。');
    return;
end
true_theta = y_theta(slope_idx);
pred_theta_slope = pred_theta(slope_idx);
mae_deg = rad2deg(mean(abs(pred_theta_slope - true_theta)));

% 图1：散点 + y=x 参考线
fig1 = figure('Name','theta_scatter','Position',[100 100 640 520]);
scatter(rad2deg(true_theta), rad2deg(pred_theta_slope), 12, 'filled', 'MarkerFaceAlpha', 0.35); hold on; grid on;
minv = min([rad2deg(true_theta); rad2deg(pred_theta_slope)]);
maxv = max([rad2deg(true_theta); rad2deg(pred_theta_slope)]);
plot([minv maxv],[minv maxv],'k--','LineWidth',1.2);
xlabel('\theta_{true} [deg]'); ylabel('\theta_{pred} [deg]');
title(sprintf('坡度回归散点 | MAE = %.3f deg', mae_deg));
saveas(fig1, fullfile(cfg.output_dir, 'theta_scatter.png'));
close(fig1);

% 图2：误差直方图 + CDF
err_deg = rad2deg(pred_theta_slope - true_theta);
fig2 = figure('Name','theta_error','Position',[100 100 720 520]);
tiledlayout(1,2,'Padding','compact','TileSpacing','compact');
nexttile; histogram(err_deg, 40, 'Normalization','pdf', 'FaceColor',[0.2 0.6 0.8]); grid on;
xlabel('误差 (pred - true) [deg]'); ylabel('PDF');
title('坡度回归误差分布');
nexttile; [f,x] = ecdf(err_deg); plot(x, f, 'LineWidth',1.5); grid on;
xlabel('误差 (pred - true) [deg]'); ylabel('CDF');
title(sprintf('误差CDF | MAE = %.3f deg', mae_deg));
saveas(fig2, fullfile(cfg.output_dir, 'theta_error_hist_cdf.png'));
close(fig2);

fprintf('图表已保存到: %s\n', cfg.output_dir);
end

%% =====================================================================
function names = guess_main_names(labels)
% 推测主工况类名（兼容 3 类或 4 类旧版）
names = cell(size(labels));
for i = 1:numel(labels)
    switch labels(i)
        case 1, names{i} = 'flat';
        case 2, names{i} = 'stall'; % 或堵转
        case 3, names{i} = 'slope';
        case 4, names{i} = 'slope'; % 旧版编号
        otherwise, names{i} = sprintf('class%d', labels(i));
    end
end
end

function names = guess_turn_names(labels)
% 推测转弯类名（通常 -1/0/1 => right/straight/left）
names = cell(size(labels));
for i = 1:numel(labels)
    switch labels(i)
        case -1, names{i} = 'right';
        case 0,  names{i} = 'straight';
        case 1,  names{i} = 'left';
        otherwise, names{i} = sprintf('class%d', labels(i));
    end
end
end

function save_confusion(cm, labels, names, title_str, out_file)
fig = figure('Name', title_str, 'Position', [100 100 560 460]);
imagesc(cm);
% 自定义配色：低值为浅米色，高值为蓝色，接近示例配色
base_colors = [0.95 0.88 0.85;   % 浅米色
               0.26 0.54 0.77];  % 蓝色
cmap = interp1([0 1], base_colors, linspace(0,1,256));
colormap(cmap);
axis equal tight; colorbar;
num_classes = numel(labels);
set(gca, 'XTick', 1:num_classes, 'XTickLabel', names, 'YTick', 1:num_classes, 'YTickLabel', names);
xlabel('预测'); ylabel('真值'); title(title_str);
for i = 1:num_classes
    for j = 1:num_classes
        text(j, i, num2str(cm(i,j)), 'HorizontalAlignment','center','FontSize',10);
    end
end
saveas(fig, out_file);
close(fig);
end
