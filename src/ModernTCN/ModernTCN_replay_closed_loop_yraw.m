function result = ModernTCN_replay_closed_loop_yraw(out_file, max_steps, cfg)
%MODERNTCN_REPLAY_CLOSED_LOOP_YRAW Replay logged y_raw through a ModernTCN wrapper.
%
% This diagnostic does not rerun or modify the Simulink model. It reuses
% diag.y_raw from an existing out.mat and calls the same
% ModernTCN_State_Classifier_sim(y_raw, reset) entry used by Simulink.
%
% Optional cfg fields:
%   seed      : default 21.
%   run_tag   : results/modern_tcn/<run_tag>/modern_tcn_seed<seed>.onnx.
%   onnx_file : explicit ONNX path, overrides run_tag.

if nargin < 1 || isempty(out_file)
    out_file = fullfile(local_project_root(), 'out.mat');
end
if nargin < 2 || isempty(max_steps)
    max_steps = 0;
end
if nargin < 3 || isempty(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = local_project_root();
cfg = local_normalize_cfg(root, cfg);
params = parameters();
assignin('base', 'params', params);
[had_sim_cfg, old_sim_cfg] = local_install_sim_cfg(cfg);
cleanup_cfg = onCleanup(@() local_restore_sim_cfg(had_sim_cfg, old_sim_cfg)); %#ok<NASGU>

S = load(out_file, 'logsout');
logs = S.logsout;

t = local_time(logs, 'diag.y_raw');
y_raw = local_data(logs, 'diag.y_raw');
theta_ground = local_resample(logs, 'diag.theta_ground', t);
omega_ref = local_resample(logs, 'diag.omega_ref', t);

if max_steps > 0
    n = min(max_steps, numel(t));
    t = t(1:n);
    y_raw = y_raw(1:n, :);
    theta_ground = theta_ground(1:n);
    omega_ref = omega_ref(1:n);
else
    n = numel(t);
end

theta_hat = nan(n, 1);
label_main = nan(n, 1);
label_turn = nan(n, 1);
conf_main = nan(n, 1);
label_main_raw = nan(n, 1);
label_turn_raw = nan(n, 1);
theta_hat_raw = nan(n, 1);
conf_turn = nan(n, 1);
main_prob = nan(n, 3);
turn_prob = nan(n, 3);
features = nan(n, 19);
features_norm = nan(n, 19);

ModernTCN_State_Classifier_sim(y_raw(1, :).', 1);
fprintf('[ModernTCN replay] steps=%d | out=%s\n', n, out_file);
fprintf('  onnx=%s\n', cfg.onnx_file);
for k = 1:n
    [theta_hat(k), label_main(k), label_turn(k), conf_main(k)] = ...
        ModernTCN_State_Classifier_sim(y_raw(k, :).', 0);
    debug_out = evalin('base', 'modern_tcn_out_temp');
    [label_main_raw(k), label_turn_raw(k), theta_hat_raw(k), conf_turn(k), ...
        main_prob(k, :), turn_prob(k, :), features(k, :), features_norm(k, :)] = ...
        local_debug_fields(debug_out);
    if mod(k, 1000) == 0 || k == n
        fprintf('  replayed %d/%d\n', k, n);
    end
end

truth02 = local_make_truth(theta_ground, omega_ref, 0.02);
truth05 = local_make_truth(theta_ground, omega_ref, 0.05);
zones = local_get_zones(root, t);
zone_names = fieldnames(zones);
rows = repmat(local_empty_zone_row(), numel(zone_names), 1);
for i = 1:numel(zone_names)
    name = zone_names{i};
    tr = zones.(name);
    mask = t >= tr(1) & t < tr(2);
    rows(i) = local_zone_row(name, tr, mask, theta_hat, theta_ground, ...
        label_main, label_turn, label_main_raw, label_turn_raw, conf_main, ...
        conf_turn, turn_prob, truth02, truth05, omega_ref);
end
zone_table = struct2table(rows);

out_dir = fullfile(root, 'results', 'modern_tcn', 'closed_loop_replay');
if exist(out_dir, 'dir') ~= 7
    mkdir(out_dir);
end
[~, base_name, ~] = fileparts(out_file);
report_tag = local_report_tag(cfg);
mat_file = fullfile(out_dir, sprintf('%s_modern_tcn_replay_%s.mat', base_name, report_tag));
report_file = fullfile(out_dir, sprintf('%s_modern_tcn_replay_%s_report.md', base_name, report_tag));

result = struct();
result.out_file = out_file;
result.cfg = cfg;
result.onnx_file = cfg.onnx_file;
result.zone_table = zone_table;
result.t = t;
result.theta_hat = theta_hat;
result.theta_hat_raw = theta_hat_raw;
result.label_main = label_main;
result.label_main_raw = label_main_raw;
result.label_turn = label_turn;
result.label_turn_raw = label_turn_raw;
result.conf_main = conf_main;
result.conf_turn = conf_turn;
result.main_prob = main_prob;
result.turn_prob = turn_prob;
result.features = features;
result.features_norm = features_norm;
result.theta_ground = theta_ground;
result.omega_ref = omega_ref;
result.truth02 = truth02;
result.truth05 = truth05;
result.mat_file = mat_file;
result.report_file = report_file;

save(mat_file, 'result');
local_write_report(report_file, result);

fprintf('[ModernTCN replay] report: %s\n', report_file);
disp(zone_table(:, {'zone','theta_mae_deg','main_acc_pct','turn_acc05_pct', ...
    'left_recall05_pct','left_raw_recall05_pct','pred_main_3_pct', ...
    'pred_turn_1_pct','pred_turn_raw_1_pct','left_prob_p90'}));
end

function cfg = local_normalize_cfg(root, cfg)
default_cfg = ModernTCN_default_config(root);
if ~isfield(cfg, 'seed') || isempty(cfg.seed)
    cfg.seed = default_cfg.seed;
end
if ~isfield(cfg, 'run_tag')
    cfg.run_tag = default_cfg.run_tag;
end
if ~isfield(cfg, 'onnx_file')
    cfg.onnx_file = '';
end
if ~isfield(cfg, 'dataset_file') || isempty(cfg.dataset_file)
    cfg.dataset_file = default_cfg.dataset_file;
end
if isempty(cfg.onnx_file)
    if ~isempty(cfg.run_tag)
        cfg.onnx_file = fullfile(root, 'results', 'modern_tcn', char(cfg.run_tag), ...
            sprintf('modern_tcn_seed%d.onnx', cfg.seed));
    else
        cfg.onnx_file = default_cfg.onnx_file;
    end
end
end

function [had_cfg, old_cfg] = local_install_sim_cfg(cfg)
had_cfg = evalin('base', 'exist(''modern_tcn_sim_cfg'', ''var'')==1');
if had_cfg
    old_cfg = evalin('base', 'modern_tcn_sim_cfg');
else
    old_cfg = [];
end
assignin('base', 'modern_tcn_sim_cfg', cfg);
end

function local_restore_sim_cfg(had_cfg, old_cfg)
if had_cfg
    assignin('base', 'modern_tcn_sim_cfg', old_cfg);
else
    evalin('base', 'clear modern_tcn_sim_cfg');
end
end

function [label_main_raw, label_turn_raw, theta_hat_raw, conf_turn, main_prob, turn_prob, features, features_norm] = ...
    local_debug_fields(debug_out)
label_main_raw = NaN;
label_turn_raw = NaN;
theta_hat_raw = NaN;
conf_turn = NaN;
main_prob = nan(1, 3);
turn_prob = nan(1, 3);
features = nan(1, 19);
features_norm = nan(1, 19);
if ~isstruct(debug_out)
    return;
end
if isfield(debug_out, 'label_main_raw'); label_main_raw = double(debug_out.label_main_raw); end
if isfield(debug_out, 'label_turn_raw'); label_turn_raw = double(debug_out.label_turn_raw); end
if isfield(debug_out, 'theta_hat_raw'); theta_hat_raw = double(debug_out.theta_hat_raw); end
if isfield(debug_out, 'conf_turn'); conf_turn = double(debug_out.conf_turn); end
if isfield(debug_out, 'main_prob')
    p = double(debug_out.main_prob(:)).';
    main_prob(1:min(3, numel(p))) = p(1:min(3, numel(p)));
end
if isfield(debug_out, 'turn_prob')
    p = double(debug_out.turn_prob(:)).';
    turn_prob(1:min(3, numel(p))) = p(1:min(3, numel(p)));
end
if isfield(debug_out, 'features')
    p = double(debug_out.features(:)).';
    features(1:min(19, numel(p))) = p(1:min(19, numel(p)));
end
if isfield(debug_out, 'features_norm')
    p = double(debug_out.features_norm(:)).';
    features_norm(1:min(19, numel(p))) = p(1:min(19, numel(p)));
end
end

function row = local_empty_zone_row()
row = struct('zone', "", 't0', NaN, 't1', NaN, ...
    'theta_mae_deg', NaN, 'theta_rmse_deg', NaN, 'theta_peak_deg', NaN, ...
    'theta_hat_min_deg', NaN, 'theta_hat_max_deg', NaN, ...
    'main_acc_pct', NaN, ...
    'turn_acc_pct', NaN, 'turn_acc02_pct', NaN, 'turn_acc05_pct', NaN, ...
    'turn_raw_acc05_pct', NaN, ...
    'left_recall02_pct', NaN, 'left_recall05_pct', NaN, ...
    'left_raw_recall05_pct', NaN, 'right_recall05_pct', NaN, ...
    'right_raw_recall05_pct', NaN, ...
    'true_main_1_pct', NaN, 'true_main_3_pct', NaN, ...
    'pred_main_1_pct', NaN, 'pred_main_2_pct', NaN, 'pred_main_3_pct', NaN, ...
    'true_turn_m1_pct', NaN, 'true_turn_0_pct', NaN, 'true_turn_1_pct', NaN, ...
    'true_turn05_m1_pct', NaN, 'true_turn05_0_pct', NaN, 'true_turn05_1_pct', NaN, ...
    'pred_turn_m1_pct', NaN, 'pred_turn_0_pct', NaN, 'pred_turn_1_pct', NaN, ...
    'pred_turn_raw_m1_pct', NaN, 'pred_turn_raw_0_pct', NaN, 'pred_turn_raw_1_pct', NaN, ...
    'left_prob_median', NaN, 'left_prob_p90', NaN, ...
    'straight_prob_median', NaN, 'conf_median', NaN, 'conf_p10', NaN, ...
    'omega_ref_min', NaN, 'omega_ref_max', NaN);
end

function row = local_zone_row(name, tr, mask, theta_hat, theta_ground, ...
    label_main, label_turn, label_main_raw, label_turn_raw, conf_main, ...
    conf_turn, turn_prob, truth02, truth05, omega_ref)
row = local_empty_zone_row();
row.zone = string(name);
row.t0 = tr(1);
row.t1 = tr(2);
if nnz(mask) < 2
    return;
end

th_err = theta_hat(mask) - theta_ground(mask);
lm = round(label_main(mask));
lt = round(label_turn(mask));
ltr = round(label_turn_raw(mask));
tm = truth05.main(mask);
tt02 = truth02.turn(mask);
tt05 = truth05.turn(mask);
prob = turn_prob(mask, :);

row.theta_mae_deg = rad2deg(mean(abs(th_err), 'omitnan'));
row.theta_rmse_deg = rad2deg(local_rms(th_err));
row.theta_peak_deg = rad2deg(max(abs(th_err)));
row.theta_hat_min_deg = rad2deg(min(theta_hat(mask)));
row.theta_hat_max_deg = rad2deg(max(theta_hat(mask)));
row.main_acc_pct = 100 * mean(lm == tm, 'omitnan');
row.turn_acc_pct = 100 * mean(lt == tt02, 'omitnan');
row.turn_acc02_pct = row.turn_acc_pct;
row.turn_acc05_pct = 100 * mean(lt == tt05, 'omitnan');
row.turn_raw_acc05_pct = 100 * mean(ltr == tt05, 'omitnan');
row.left_recall02_pct = local_recall_pct(lt, tt02, 1);
row.left_recall05_pct = local_recall_pct(lt, tt05, 1);
row.left_raw_recall05_pct = local_recall_pct(ltr, tt05, 1);
row.right_recall05_pct = local_recall_pct(lt, tt05, -1);
row.right_raw_recall05_pct = local_recall_pct(ltr, tt05, -1);
row.true_main_1_pct = 100 * mean(tm == 1, 'omitnan');
row.true_main_3_pct = 100 * mean(tm == 3, 'omitnan');
row.pred_main_1_pct = 100 * mean(lm == 1, 'omitnan');
row.pred_main_2_pct = 100 * mean(lm == 2, 'omitnan');
row.pred_main_3_pct = 100 * mean(lm == 3, 'omitnan');
row.true_turn_m1_pct = 100 * mean(tt02 == -1, 'omitnan');
row.true_turn_0_pct = 100 * mean(tt02 == 0, 'omitnan');
row.true_turn_1_pct = 100 * mean(tt02 == 1, 'omitnan');
row.true_turn05_m1_pct = 100 * mean(tt05 == -1, 'omitnan');
row.true_turn05_0_pct = 100 * mean(tt05 == 0, 'omitnan');
row.true_turn05_1_pct = 100 * mean(tt05 == 1, 'omitnan');
row.pred_turn_m1_pct = 100 * mean(lt == -1, 'omitnan');
row.pred_turn_0_pct = 100 * mean(lt == 0, 'omitnan');
row.pred_turn_1_pct = 100 * mean(lt == 1, 'omitnan');
row.pred_turn_raw_m1_pct = 100 * mean(ltr == -1, 'omitnan');
row.pred_turn_raw_0_pct = 100 * mean(ltr == 0, 'omitnan');
row.pred_turn_raw_1_pct = 100 * mean(ltr == 1, 'omitnan');
row.left_prob_median = median(prob(:, 3), 'omitnan');
row.left_prob_p90 = local_prctile(prob(:, 3), 90);
row.straight_prob_median = median(prob(:, 2), 'omitnan');
row.conf_median = median(conf_main(mask), 'omitnan');
row.conf_p10 = local_prctile(conf_main(mask), 10);
row.omega_ref_min = min(omega_ref(mask));
row.omega_ref_max = max(omega_ref(mask));

% Keep the raw main label read alive in reports if a future diagnostic needs it.
if all(~isfinite(label_main_raw(mask))) && all(~isfinite(conf_turn(mask)))
    return;
end
end

function truth = local_make_truth(theta_ground, omega_ref, omega_thresh)
truth = struct();
truth.main = ones(size(theta_ground));
truth.main(abs(theta_ground) > deg2rad(2.0)) = 3;
truth.turn = zeros(size(omega_ref));
truth.turn(omega_ref > omega_thresh) = 1;
truth.turn(omega_ref < -omega_thresh) = -1;
truth.omega_thresh = omega_thresh;
end

function zones = local_get_zones(root, t)
path_file = fullfile(root, 'data', 'paths', 'path_industrial_lite.mat');
if exist(path_file, 'file') == 2
    S = load(path_file, 'ref');
    if isfield(S, 'ref') && isfield(S.ref, 'meta') && isfield(S.ref.meta, 'zones')
        zones = S.ref.meta.zones;
        return;
    end
end
zones = struct();
zones.startup = [min(t), 10];
zones.golden_test = [10, 50];
zones.pure_turn = [50, 78];
zones.pure_slope = [78, 98];
zones.composite = [98, 118];
zones.closure = [118, max(t)];
end

function data = local_resample(logs, name, t)
ts = local_timeseries(logs, name);
data = squeeze(double(ts.Data));
if isvector(data)
    data = data(:);
else
    data = reshape(data, [], size(data, ndims(data)));
    data = data(:);
end
tt = double(ts.Time(:));
if numel(tt) ~= numel(data)
    data = squeeze(double(ts.Data));
    data = reshape(data, [], numel(tt)).';
end
if numel(tt) == numel(t) && max(abs(tt - t)) < 1e-12
    return;
end
data = interp1(tt, data, t, 'linear', 'extrap');
end

function data = local_data(logs, name)
ts = local_timeseries(logs, name);
data = squeeze(double(ts.Data));
end

function t = local_time(logs, name)
ts = local_timeseries(logs, name);
t = double(ts.Time(:));
end

function ts = local_timeseries(logs, name)
hit = [];
for i = 1:logs.numElements
    el = logs.getElement(i);
    if strcmp(el.Name, name)
        hit(end + 1) = i; %#ok<AGROW>
    end
end
if isempty(hit)
    error('ModernTCN:MissingLogSignal', 'logsout missing signal: %s', name);
end
ts = logs.getElement(hit(end)).Values;
end

function local_write_report(report_file, result)
fid = fopen(report_file, 'w');
if fid < 0
    warning('ModernTCN:ReportFailed', 'Cannot write report: %s', report_file);
    return;
end
cleanup = onCleanup(@() fclose(fid)); %#ok<NASGU>

fprintf(fid, '# ModernTCN y_raw Replay Diagnostic\n\n');
fprintf(fid, '- out file: `%s`\n', result.out_file);
fprintf(fid, '- onnx: `%s`\n', result.onnx_file);
fprintf(fid, '- turn truth thresholds: `0.02` and `0.05` rad/s; training labels use `0.05` rad/s.\n\n');
fprintf(fid, '| zone | theta MAE deg | main acc | turn acc 0.05 | left recall 0.05 | raw left recall 0.05 | pred main 3 | pred turn 1 | raw pred turn 1 | left p90 |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n');
T = result.zone_table;
for i = 1:height(T)
    fprintf(fid, '| %s | %.3f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.3f |\n', ...
        T.zone(i), T.theta_mae_deg(i), T.main_acc_pct(i), T.turn_acc05_pct(i), ...
        T.left_recall05_pct(i), T.left_raw_recall05_pct(i), T.pred_main_3_pct(i), ...
        T.pred_turn_1_pct(i), T.pred_turn_raw_1_pct(i), T.left_prob_p90(i));
end
fprintf(fid, '\n## Full Zone Table\n\n');
fprintf(fid, 'Saved in `%s` as `result.zone_table`.\n', result.mat_file);
end

function y = local_rms(x)
x = x(isfinite(x));
if isempty(x)
    y = NaN;
else
    y = sqrt(mean(x.^2));
end
end

function p = local_recall_pct(pred, truth, cls)
mask = truth == cls;
if ~any(mask)
    p = NaN;
else
    p = 100 * mean(pred(mask) == cls, 'omitnan');
end
end

function p = local_prctile(x, q)
x = x(isfinite(x));
if isempty(x)
    p = NaN;
else
    p = prctile(x, q);
end
end

function tag = local_report_tag(cfg)
if isfield(cfg, 'run_tag') && ~isempty(cfg.run_tag)
    tag = char(cfg.run_tag);
else
    tag = 'current_model';
end
tag = regexprep(tag, '[^A-Za-z0-9_\-]+', '_');
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
