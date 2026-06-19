function result = run_dual_modern_seed101_closed_loop(cfg)
%RUN_DUAL_MODERN_SEED101_CLOSED_LOOP Compare two ModernTCN seed101 baselines.
%
% This runner is workflow-local and intentionally does not overwrite the
% existing stage1 closed-loop results. It compares:
%   - ModernTCN slope-strong seed101
%   - ModernTCN turn-improved seed101 l020_tt25
%   - GRU full seed101
%   - TCN full seed101

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = local_cfg(cfg, 'node_dir', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '09_closed_loop', ...
    'dual_modern_seed101_full'));
if exist(node_dir, 'dir') ~= 7
    mkdir(node_dir);
end
cfg.stop_time_override = local_cfg(cfg, 'stop_time_override', []);
cfg.stop_on_error = local_cfg(cfg, 'stop_on_error', true);
cfg.include_theta0_oracle = local_cfg(cfg, 'include_theta0_oracle', false);
cfg.path_indices = local_cfg(cfg, 'path_indices', []);

models = local_models(root);
paths = local_paths(root);
if ~isempty(cfg.path_indices)
    path_indices = double(cfg.path_indices(:).');
    if any(path_indices < 1) || any(path_indices > numel(paths)) || any(path_indices ~= fix(path_indices))
        error('dual_modern_closed_loop:BadPathIndices', ...
            'cfg.path_indices must contain integer indices in [1, %d].', numel(paths));
    end
    paths = paths(path_indices);
end
preflight = local_preflight(root, paths, models);
mpc_candidate = local_load_mpc_candidate(local_maps_file(root));

result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.node_dir = node_dir;
result.cfg = cfg;
result.models = models;
result.paths = paths;
result.preflight = preflight;
result.mpc_candidate = mpc_candidate;
local_write_json(fullfile(node_dir, 'dual_modern_preflight.json'), preflight);
fprintf('[dual-modern closed-loop] output: %s\n', node_dir);
fprintf('[dual-modern closed-loop] paths=%d, stop_time_override=%s\n', ...
    numel(paths), mat2str(cfg.stop_time_override));

if ~preflight.pass
    result.status = 'preflight_failed';
    save(fullfile(node_dir, 'dual_modern_closed_loop_result.mat'), 'result', '-v7.3');
    error('dual_modern_closed_loop:PreflightFailed', 'Preflight failed.');
end

path_runs = local_run_all(root, node_dir, paths, models, cfg, mpc_candidate);
result.path_runs = path_runs;
writetable(path_runs, fullfile(node_dir, 'dual_modern_path_runs.csv'));

[summary_table, aggregate_table] = local_collect(path_runs);
result.summary_table = summary_table;
result.aggregate_table = aggregate_table;
if ~isempty(summary_table)
    writetable(summary_table, fullfile(node_dir, 'dual_modern_summary.csv'));
end
if ~isempty(aggregate_table)
    writetable(aggregate_table, fullfile(node_dir, 'dual_modern_aggregate.csv'));
end
local_write_report(node_dir, result);
result.status = 'done';
save(fullfile(node_dir, 'dual_modern_closed_loop_result.mat'), 'result', '-v7.3');
fprintf('[dual-modern closed-loop] done: %s\n', fullfile(node_dir, 'dual_modern_report.md'));
end

function models = local_models(root)
model_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models');
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');

models = struct();
models.dataset_file = dataset_file;
models.modern_slope = struct( ...
    'label', "ModernTCN_slope_seed101", ...
    'seed', 101, ...
    'dataset_file', dataset_file, ...
    'onnx_file', fullfile(model_dir, 'modern_tcn', ...
        'modern_tcn_v5_plantfix_passive17_plus_all5_seed101', ...
        'modern_tcn_seed101.onnx'), ...
    'run_tag', 'modern_tcn_v5_plantfix_passive17_plus_all5_seed101');
models.modern_turn = struct( ...
    'label', "ModernTCN_turn_l020_tt25_seed101", ...
    'seed', 101, ...
    'dataset_file', dataset_file, ...
    'onnx_file', fullfile(model_dir, 'modern_tcn', ...
        'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101', ...
        'modern_tcn_seed101.onnx'), ...
    'run_tag', 'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101');
models.gru = struct( ...
    'label', "GRU_seed101", ...
    'seed', 101, ...
    'dataset_file', dataset_file, ...
    'model_file', fullfile(model_dir, 'models', ...
        'GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat'), ...
    'meta_file', fullfile(model_dir, 'models', ...
        'GRU_meta_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat'));
models.tcn = struct( ...
    'label', "TCN_seed101", ...
    'seed', 101, ...
    'dataset_file', dataset_file, ...
    'model_file', fullfile(model_dir, 'models', ...
        'TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat'), ...
    'meta_file', fullfile(model_dir, 'models', ...
        'TCN_meta_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat'));
end

function paths = local_paths(root)
paths = { ...
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v3.mat'), ...
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat'), ...
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')};
end

function rows = local_run_all(root, node_dir, paths, models, cfg, mpc_candidate)
rows = repmat(local_path_row(), numel(paths), 1);
for i = 1:numel(paths)
    path_file = paths{i};
    [~, path_tag] = fileparts(path_file);
    fprintf('[dual-modern closed-loop] path %d/%d: %s\n', i, numel(paths), path_tag);
    path_dir = fullfile(node_dir, path_tag);
    if exist(path_dir, 'dir') ~= 7
        mkdir(path_dir);
    end
    rows(i).path_tag = string(path_tag);
    rows(i).path_file = string(path_file);
    rows(i).out_dir = string(path_dir);
    try
        sim_cfg = struct();
        sim_cfg.stop_time_override = cfg.stop_time_override;
        sim_cfg.params_override = parameters();
        if ~isempty(mpc_candidate)
            sim_cfg.mpc_runtime_override = mpc_candidate.runtime_override;
        end

        modern_slope_out = fullfile(path_dir, 'ModernTCN_slope_seed101_out.mat');
        modern_turn_out = fullfile(path_dir, 'ModernTCN_turn_l020_tt25_seed101_out.mat');
        gru_out = fullfile(path_dir, 'GRU_seed101_out.mat');
        tcn_out = fullfile(path_dir, 'TCN_seed101_out.mat');

        fprintf('[dual-modern closed-loop] start %s\n', models.modern_slope.label);
        t_controller = tic;
        local_run_modern(root, models.modern_slope, path_file, modern_slope_out, sim_cfg);
        fprintf('[dual-modern closed-loop] done %s in %.1fs\n', ...
            models.modern_slope.label, toc(t_controller));

        fprintf('[dual-modern closed-loop] start %s\n', models.modern_turn.label);
        t_controller = tic;
        local_run_modern(root, models.modern_turn, path_file, modern_turn_out, sim_cfg);
        fprintf('[dual-modern closed-loop] done %s in %.1fs\n', ...
            models.modern_turn.label, toc(t_controller));

        fprintf('[dual-modern closed-loop] start %s\n', models.gru.label);
        t_controller = tic;
        local_run_gru(root, models.gru, path_file, gru_out, sim_cfg);
        fprintf('[dual-modern closed-loop] done %s in %.1fs\n', ...
            models.gru.label, toc(t_controller));

        fprintf('[dual-modern closed-loop] start %s\n', models.tcn.label);
        t_controller = tic;
        local_run_tcn(root, models.tcn, path_file, tcn_out, sim_cfg);
        fprintf('[dual-modern closed-loop] done %s in %.1fs\n', ...
            models.tcn.label, toc(t_controller));

        extra_runs = struct('label', models.modern_turn.label, 'file', modern_turn_out);
        compare_tcn_gru_modern_closed_loop_out( ...
            modern_slope_out, gru_out, tcn_out, path_file, path_dir, ...
            models.modern_slope.label, extra_runs, ...
            'Dual ModernTCN seed101 plantfix closed-loop comparison', ...
            'dual_modern_closed_loop');

        rows(i).modern_slope_file = string(modern_slope_out);
        rows(i).modern_turn_file = string(modern_turn_out);
        rows(i).gru_file = string(gru_out);
        rows(i).tcn_file = string(tcn_out);
        rows(i).summary_file = string(fullfile(path_dir, 'dual_modern_closed_loop_summary.csv'));
        rows(i).rank_file = string(fullfile(path_dir, 'dual_modern_closed_loop_rank.csv'));
        rows(i).status = "ok";
        path_runs = struct2table(rows(1:i)); %#ok<NASGU>
        writetable(path_runs, fullfile(node_dir, 'dual_modern_path_runs_partial.csv'));
    catch ME
        rows(i).status = "error";
        rows(i).message = string(ME.message);
        if cfg.stop_on_error
            path_runs = struct2table(rows(1:i)); %#ok<NASGU>
            writetable(path_runs, fullfile(node_dir, 'dual_modern_path_runs_partial.csv'));
            rethrow(ME);
        end
    end
end
rows = struct2table(rows);
end

function local_run_modern(root, model_cfg, path_file, out_file, sim_cfg)
cfg = sim_cfg;
cfg.modern_tcn_sim_cfg = struct( ...
    'seed', model_cfg.seed, ...
    'run_tag', model_cfg.run_tag, ...
    'dataset_file', model_cfg.dataset_file, ...
    'onnx_file', model_cfg.onnx_file, ...
    'theta_output_gain', 1.0, ...
    'theta_abs_limit', deg2rad(12.0), ...
    'theta_rate_limit', deg2rad(5.0), ...
    'theta_mpc_deadzone', deg2rad(2.0));
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', path_file, out_file, cfg);
local_write_audit(out_file, 'modern_tcn', model_cfg, root, path_file);
end

function local_run_gru(root, model_cfg, path_file, out_file, sim_cfg)
S = load(model_cfg.model_file, 'model');
M = load(model_cfg.meta_file, 'meta');
assignin('base', 'gru_model', S.model);
assignin('base', 'gru_meta', M.meta);
cfg = sim_cfg;
cfg.gru_sim_cfg = struct( ...
    'seed', model_cfg.seed, ...
    'dataset_file', model_cfg.dataset_file, ...
    'model_file', model_cfg.model_file, ...
    'meta_file', model_cfg.meta_file, ...
    'theta_output_gain', 1.0, ...
    'theta_abs_limit', deg2rad(12.0), ...
    'theta_rate_limit', deg2rad(5.0), ...
    'theta_mpc_deadzone', deg2rad(2.0));
run_closed_loop_model_once('LPVMPC_AGV_simulink_GRU', path_file, out_file, cfg);
local_write_audit(out_file, 'gru', model_cfg, root, path_file);
end

function local_run_tcn(root, model_cfg, path_file, out_file, sim_cfg)
S = load(model_cfg.model_file, 'model');
M = load(model_cfg.meta_file, 'meta');
assignin('base', 'tcn_model', S.model);
assignin('base', 'tcn_meta', M.meta);
cfg = sim_cfg;
cfg.tcn_sim_cfg = struct( ...
    'seed', model_cfg.seed, ...
    'dataset_file', model_cfg.dataset_file, ...
    'model_file', model_cfg.model_file, ...
    'meta_file', model_cfg.meta_file, ...
    'theta_output_gain', 1.0, ...
    'theta_abs_limit', deg2rad(12.0), ...
    'theta_rate_limit', deg2rad(5.0), ...
    'theta_mpc_deadzone', deg2rad(2.0));
run_closed_loop_model_once('LPVMPC_AGV_simulink_TCN', path_file, out_file, cfg);
local_write_audit(out_file, 'tcn', model_cfg, root, path_file);
end

function preflight = local_preflight(root, paths, models)
plant = agv_plant_revision(parameters());
checks = struct();
checks.plant_revision = strcmp(plant.id, 'agv_physics_v2_plantfix');
checks.dataset = exist(models.dataset_file, 'file') == 2;
checks.modern_slope_onnx = exist(models.modern_slope.onnx_file, 'file') == 2;
checks.modern_turn_onnx = exist(models.modern_turn.onnx_file, 'file') == 2;
checks.gru_model = exist(models.gru.model_file, 'file') == 2 && exist(models.gru.meta_file, 'file') == 2;
checks.tcn_model = exist(models.tcn.model_file, 'file') == 2 && exist(models.tcn.meta_file, 'file') == 2;
checks.learned_shells = local_exists_model(root, 'LPVMPC_AGV_simulink_Modern_TCN') && ...
    local_exists_model(root, 'LPVMPC_AGV_simulink_GRU') && ...
    local_exists_model(root, 'LPVMPC_AGV_simulink_TCN');
checks.three_paths = all(cellfun(@(p) exist(p, 'file') == 2, paths));
checks.maps_candidate = exist(local_maps_file(root), 'file') == 2;
preflight = struct('checks', checks, 'pass', all(structfun(@(x) isequal(x, true), checks)));
end

function tf = local_exists_model(root, model_name)
path_in = fullfile(root, 'simulink', [model_name '.slx']);
tf = exist(path_in, 'file') == 2 || exist(path_in, 'file') == 4;
end

function maps_file = local_maps_file(root)
maps_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning', ...
    'maps_best_agv_physics_v2_plantfix_stage1.mat');
end

function mpc_candidate = local_load_mpc_candidate(maps_file)
if exist(maps_file, 'file') ~= 2
    mpc_candidate = [];
    return;
end
S = load(maps_file, 'maps_best', 'opts', 'db_file');
maps_best = S.maps_best;
if isfield(S, 'opts')
    opts = S.opts;
else
    opts = maps_best;
end
runtime_override = struct();
runtime_override.id = local_field_or_default(maps_best, 'id', 'stage1_plantfix_p0');
runtime_override.Np = local_field_or_default(opts, 'Np', local_field_or_default(maps_best, 'Np', 150));
runtime_override.Nc = local_field_or_default(opts, 'Nc', local_field_or_default(maps_best, 'Nc', 30));
runtime_override.Q = local_field_or_default(opts, 'Q', local_field_or_default(maps_best, 'Q', [100 100 15 3]));
runtime_override.R = local_field_or_default(opts, 'R', local_field_or_default(maps_best, 'R', [3e-5 3e-5]));
runtime_override.dR = local_field_or_default(opts, 'dR', local_field_or_default(maps_best, 'dR', [1e-3 1e-3]));
runtime_override.maps_template = maps_best;
if isfield(S, 'db_file') && ~isempty(S.db_file)
    runtime_override.db_file = S.db_file;
elseif isfield(maps_best, 'db_file') && ~isempty(maps_best.db_file)
    runtime_override.db_file = maps_best.db_file;
else
    workflow_dir = fileparts(fileparts(maps_file));
    runtime_override.db_file = fullfile(workflow_dir, '04_lpv_database', ...
        'lin_agv_db_agv_physics_v2_plantfix.mat');
end
mpc_candidate = struct('maps_file', maps_file, 'maps_best', maps_best, ...
    'runtime_override', runtime_override);
end

function [summary_table, aggregate_table] = local_collect(path_runs)
summary_table = table();
for i = 1:height(path_runs)
    if path_runs.status(i) ~= "ok" || exist(path_runs.summary_file(i), 'file') ~= 2
        continue;
    end
    T = readtable(path_runs.summary_file(i), 'TextType', 'string');
    T.path_tag = repmat(path_runs.path_tag(i), height(T), 1);
    summary_table = [summary_table; T]; %#ok<AGROW>
end
if isempty(summary_table)
    aggregate_table = table();
    return;
end
controllers = unique(summary_table.controller, 'stable');
rows = repmat(struct('controller', "", 'n_paths', 0, ...
    'ey_rmse_mean', NaN, 'ey_peak_worst', NaN, ...
    'xy_rmse_mean', NaN, 'j_du_mean', NaN, ...
    'rank_ey', NaN), numel(controllers), 1);
for i = 1:numel(controllers)
    mask = summary_table.controller == controllers(i);
    rows(i).controller = controllers(i);
    rows(i).n_paths = sum(mask);
    rows(i).ey_rmse_mean = mean(summary_table.ey_rmse(mask), 'omitnan');
    rows(i).ey_peak_worst = max(summary_table.ey_peak(mask), [], 'omitnan');
    rows(i).xy_rmse_mean = mean(summary_table.xy_rmse(mask), 'omitnan');
    rows(i).j_du_mean = mean(summary_table.j_du(mask), 'omitnan');
end
aggregate_table = sortrows(struct2table(rows), 'ey_rmse_mean');
aggregate_table.rank_ey = (1:height(aggregate_table))';
end

function row = local_path_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", ...
    'modern_slope_file', "", 'modern_turn_file', "", ...
    'gru_file', "", 'tcn_file', "", 'summary_file', "", ...
    'rank_file', "", 'status', "", 'message', "");
end

function local_write_audit(out_file, kind, model_cfg, root, path_file)
audit = model_cfg;
audit.kind = kind;
audit.path_file = path_file;
audit.root = root;
audit.plant_revision = 'agv_physics_v2_plantfix';
audit.created_at = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
local_write_json(strrep(out_file, '.mat', '_model_audit.json'), audit);
end

function local_write_report(node_dir, result)
report_file = fullfile(node_dir, 'dual_modern_report.md');
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Dual ModernTCN Seed101 Closed-Loop Report\n\n');
fprintf(fid, '- generated: `%s`\n', result.timestamp);
fprintf(fid, '- output_dir: `%s`\n', node_dir);
fprintf(fid, '- dataset: `%s`\n', result.models.dataset_file);
fprintf(fid, '- ModernTCN slope ONNX: `%s`\n', result.models.modern_slope.onnx_file);
fprintf(fid, '- ModernTCN turn ONNX: `%s`\n', result.models.modern_turn.onnx_file);
fprintf(fid, '- GRU model: `%s`\n', result.models.gru.model_file);
fprintf(fid, '- TCN model: `%s`\n\n', result.models.tcn.model_file);

if isfield(result, 'aggregate_table') && ~isempty(result.aggregate_table)
    fprintf(fid, '## Aggregate\n\n');
    local_write_table_md(fid, result.aggregate_table);
end

if isfield(result, 'summary_table') && ~isempty(result.summary_table)
    fprintf(fid, '\n## Per-Path Summary\n\n');
    keep = {'controller','path_tag','ey_rmse','ey_peak','xy_rmse','theta_mae_deg','main_acc_pct','turn_acc_pct'};
    keep = keep(ismember(keep, result.summary_table.Properties.VariableNames));
    local_write_table_md(fid, result.summary_table(:, keep));
end
end

function local_write_table_md(fid, T)
vars = T.Properties.VariableNames;
fprintf(fid, '| %s |\n', strjoin(vars, ' | '));
fprintf(fid, '|%s|\n', strjoin(repmat({'---'}, 1, numel(vars)), '|'));
for i = 1:height(T)
    vals = cell(1, numel(vars));
    for j = 1:numel(vars)
        v = T{i, j};
        if isnumeric(v)
            vals{j} = sprintf('%.6g', v);
        elseif isstring(v) || ischar(v)
            vals{j} = char(string(v));
        else
            vals{j} = char(string(v));
        end
    end
    fprintf(fid, '| %s |\n', strjoin(vals, ' | '));
end
fprintf(fid, '\n');
end

function local_write_json(path_in, data)
fid = fopen(path_in, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s', jsonencode(data, PrettyPrint=true));
end

function value = local_cfg(cfg, name, default_value)
if isstruct(cfg) && isfield(cfg, name) && ~isempty(cfg.(name))
    value = cfg.(name);
else
    value = default_value;
end
end

function value = local_field_or_default(s, name, default_value)
if isstruct(s) && isfield(s, name) && ~isempty(s.(name))
    value = s.(name);
else
    value = default_value;
end
end
