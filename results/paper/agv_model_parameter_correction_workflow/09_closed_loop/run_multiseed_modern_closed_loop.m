function result = run_multiseed_modern_closed_loop(cfg)
%RUN_MULTISEED_MODERN_CLOSED_LOOP Compare ModernTCN l020_tt25 seed candidates.
%
% Workflow-local runner. It compares the current closed-loop champion
% seed101 against multiseed retrains seed101/202/303 without overwriting
% previous dual-model closed-loop results.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = local_cfg(cfg, 'node_dir', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '09_closed_loop', ...
    'modern_multiseed_l020_tt25_full'));
if exist(node_dir, 'dir') ~= 7
    mkdir(node_dir);
end
cfg.stop_time_override = local_cfg(cfg, 'stop_time_override', []);
cfg.stop_on_error = local_cfg(cfg, 'stop_on_error', true);
cfg.path_indices = local_cfg(cfg, 'path_indices', []);
cfg.file_prefix = local_cfg(cfg, 'file_prefix', 'modern_multiseed_closed_loop');
cfg.resume_existing = logical(local_cfg(cfg, 'resume_existing', false));
cfg.short_output_files = logical(local_cfg(cfg, 'short_output_files', false));
cfg.report_title = local_cfg(cfg, 'report_title', ...
    'ModernTCN l020 tt25 multiseed closed-loop comparison');

models = local_models(root, cfg);
paths = local_paths(root);
if ~isempty(cfg.path_indices)
    path_indices = double(cfg.path_indices(:).');
    if any(path_indices < 1) || any(path_indices > numel(paths)) || any(path_indices ~= fix(path_indices))
        error('modern_multiseed_closed_loop:BadPathIndices', ...
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
local_write_json(fullfile(node_dir, 'modern_multiseed_preflight.json'), preflight);

fprintf('[modern multiseed closed-loop] output: %s\n', node_dir);
fprintf('[modern multiseed closed-loop] paths=%d, stop_time_override=%s\n', ...
    numel(paths), mat2str(cfg.stop_time_override));

if ~preflight.pass
    result.status = 'preflight_failed';
    save(fullfile(node_dir, 'modern_multiseed_closed_loop_result.mat'), 'result', '-v7.3');
    error('modern_multiseed_closed_loop:PreflightFailed', 'Preflight failed.');
end

path_runs = local_run_all(root, node_dir, paths, models, cfg, mpc_candidate);
result.path_runs = path_runs;
writetable(path_runs, fullfile(node_dir, 'modern_multiseed_path_runs.csv'));

[summary_table, aggregate_table] = local_collect(path_runs);
result.summary_table = summary_table;
result.aggregate_table = aggregate_table;
if ~isempty(summary_table)
    writetable(summary_table, fullfile(node_dir, 'modern_multiseed_summary.csv'));
end
if ~isempty(aggregate_table)
    writetable(aggregate_table, fullfile(node_dir, 'modern_multiseed_aggregate.csv'));
end
result.status = 'done';
local_write_report(node_dir, result);
save(fullfile(node_dir, 'modern_multiseed_closed_loop_result.mat'), 'result', '-v7.3');
fprintf('[modern multiseed closed-loop] done: %s\n', fullfile(node_dir, 'modern_multiseed_report.md'));
end

function models = local_models(root, cfg)
manifest_file = local_cfg(cfg, 'model_manifest_file', '');
if ~isempty(manifest_file)
    models = local_models_from_manifest(root, manifest_file);
    return;
end
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
champion_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn', ...
    'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101');
candidate_root = fullfile(root, 'results', 'modern_tcn', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn');

models = struct();
models.dataset_file = dataset_file;
models.runs = [ ...
    local_model("ModernTCN_turn_seed101_champion", 101, ...
        fullfile(champion_dir, 'modern_tcn_seed101.onnx'), ...
        'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101', dataset_file), ...
    local_model("ModernTCN_turn_seed101_multiseed", 101, ...
        fullfile(candidate_root, 'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed101', ...
        'modern_tcn_seed101.onnx'), ...
        'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed101', dataset_file), ...
    local_model("ModernTCN_turn_seed202_multiseed", 202, ...
        fullfile(candidate_root, 'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed202', ...
        'modern_tcn_seed202.onnx'), ...
        'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed202', dataset_file), ...
    local_model("ModernTCN_turn_seed303_multiseed", 303, ...
        fullfile(candidate_root, 'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed303', ...
        'modern_tcn_seed303.onnx'), ...
        'modern_tcn_v5_plantfix_turn_l020_tt25_multiseed_seed303', dataset_file)];
end

function models = local_models_from_manifest(root, manifest_file)
manifest_file = local_abs_path(root, manifest_file);
raw = fileread(manifest_file);
M = jsondecode(raw);
dataset_file = local_abs_path(root, M.dataset_file);
if ~isfield(M, 'runs') || numel(M.runs) < 3
    error('modern_multiseed_closed_loop:BadManifest', ...
        'Manifest must contain at least three runs: champion plus two candidates.');
end
models = struct();
models.dataset_file = dataset_file;
models.manifest_file = manifest_file;
run_items = M.runs;
models.runs = repmat(local_model("", 0, "", "", dataset_file), 1, numel(run_items));
for i = 1:numel(run_items)
    if iscell(run_items)
        run = run_items{i};
    else
        run = run_items(i);
    end
    models.runs(i) = local_model( ...
        local_string_field(run, 'label'), ...
        local_numeric_field(run, 'seed'), ...
        local_abs_path(root, local_string_field(run, 'onnx_file')), ...
        local_string_field(run, 'run_tag'), ...
        local_run_dataset_file(root, run, dataset_file), ...
        local_run_model_name(run, local_string_field(run, 'label'), ...
        local_run_dataset_file(root, run, dataset_file)));
end
end

function dataset_file = local_run_dataset_file(root, run, default_dataset_file)
dataset_file = default_dataset_file;
if isfield(run, 'dataset_file') && ~isempty(run.dataset_file)
    dataset_file = local_abs_path(root, local_string_field(run, 'dataset_file'));
end
end

function model_name = local_run_model_name(run, label, dataset_file)
if isfield(run, 'model_name') && ~isempty(run.model_name)
    model_name = char(string(run.model_name));
    return;
end

label_l = lower(char(string(label)));
dataset_l = lower(char(string(dataset_file)));
if contains(label_l, '30d') || contains(label_l, 'cmdresp') || ...
        contains(dataset_l, 'cmdresp_lite_v1') || contains(dataset_l, 'cmdresp_lag1_only_v1')
    model_name = 'LPVMPC_AGV_simulink_Modern_TCN_30Dtest';
else
    model_name = 'LPVMPC_AGV_simulink_Modern_TCN';
end
end

function model_cfg = local_model(label, seed, onnx_file, run_tag, dataset_file, model_name)
if nargin < 6 || isempty(model_name)
    model_name = local_run_model_name(struct(), label, dataset_file);
end
model_cfg = struct( ...
    'label', string(label), ...
    'seed', seed, ...
    'dataset_file', dataset_file, ...
    'onnx_file', onnx_file, ...
    'run_tag', run_tag, ...
    'model_name', char(model_name));
end

function path_out = local_abs_path(root, path_in)
path_out = char(string(path_in));
if isempty(path_out)
    return;
end
if ispc
    is_abs = numel(path_out) >= 2 && path_out(2) == ':';
else
    is_abs = startsWith(path_out, filesep);
end
if ~is_abs
    path_out = fullfile(root, path_out);
end
end

function value = local_string_field(s, name)
if isfield(s, name)
    value = string(s.(name));
else
    value = "";
end
end

function value = local_numeric_field(s, name)
if isfield(s, name)
    value = double(s.(name));
else
    value = NaN;
end
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
    fprintf('[modern multiseed closed-loop] path %d/%d: %s\n', i, numel(paths), path_tag);
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

        run_files = strings(1, numel(models.runs));
        for j = 1:numel(models.runs)
            model_cfg = models.runs(j);
            out_file = local_output_file(path_dir, model_cfg, j, cfg);
            if cfg.resume_existing && local_closed_loop_output_complete(out_file)
                fprintf('[modern multiseed closed-loop] reuse %s\n', model_cfg.label);
            else
                if cfg.resume_existing && exist(out_file, 'file') == 2
                    fprintf('[modern multiseed closed-loop] rerun incomplete %s\n', model_cfg.label);
                end
                fprintf('[modern multiseed closed-loop] start %s\n', model_cfg.label);
                t_controller = tic;
                local_run_modern(root, model_cfg, path_file, out_file, sim_cfg);
                fprintf('[modern multiseed closed-loop] done %s in %.1fs\n', ...
                    model_cfg.label, toc(t_controller));
            end
            run_files(j) = string(out_file);
        end

        extra_runs = struct('label', {}, 'file', {});
        for j = 4:numel(models.runs)
            extra_runs(end + 1) = struct('label', models.runs(j).label, ...
                'file', run_files(j)); %#ok<AGROW>
        end
        compare_tcn_gru_modern_closed_loop_out( ...
            run_files(1), run_files(2), run_files(3), path_file, path_dir, ...
            models.runs(1).label, extra_runs, ...
            cfg.report_title, cfg.file_prefix);
        local_relabel_compare_outputs(path_dir, cfg.file_prefix, ...
            models.runs, run_files, path_file);

        rows(i).champion_file = run_files(1);
        rows(i).candidate1_file = run_files(2);
        rows(i).candidate2_file = run_files(3);
        rows(i).extra_files = strjoin(run_files(4:end), ';');
        rows(i).summary_file = string(fullfile(path_dir, [char(cfg.file_prefix) '_summary.csv']));
        rows(i).rank_file = string(fullfile(path_dir, [char(cfg.file_prefix) '_rank.csv']));
        rows(i).status = "ok";
        path_runs = struct2table(rows(1:i)); %#ok<NASGU>
        writetable(path_runs, fullfile(node_dir, 'modern_multiseed_path_runs_partial.csv'));
    catch ME
        rows(i).status = "error";
        rows(i).message = string(ME.message);
        if cfg.stop_on_error
            path_runs = struct2table(rows(1:i)); %#ok<NASGU>
            writetable(path_runs, fullfile(node_dir, 'modern_multiseed_path_runs_partial.csv'));
            rethrow(ME);
        end
    end
end
rows = struct2table(rows);
end

function out_file = local_output_file(path_dir, model_cfg, run_index, cfg)
if cfg.short_output_files
    out_file = fullfile(path_dir, sprintf('m%02d_out.mat', run_index));
else
    out_file = fullfile(path_dir, char(model_cfg.label) + "_out.mat");
end
end

function tf = local_closed_loop_output_complete(out_file)
tf = false;
if exist(out_file, 'file') ~= 2
    return;
end
d = dir(out_file);
if isempty(d) || d.bytes == 0
    return;
end
try
    vars = whos('-file', out_file);
catch
    return;
end
names = string({vars.name});
tf = any(names == "logsout");
end

function local_run_modern(root, model_cfg, path_file, out_file, sim_cfg)
cfg = sim_cfg;
u_cmd_already_lagged = local_model_uses_lagged_cmd_input(model_cfg);
cfg.modern_tcn_sim_cfg = struct( ...
    'seed', model_cfg.seed, ...
    'run_tag', model_cfg.run_tag, ...
    'dataset_file', model_cfg.dataset_file, ...
    'onnx_file', model_cfg.onnx_file, ...
    'theta_output_gain', 1.0, ...
    'theta_abs_limit', deg2rad(12.0), ...
    'theta_rate_limit', deg2rad(5.0), ...
    'theta_mpc_deadzone', deg2rad(2.0), ...
    'u_cmd_already_lagged', u_cmd_already_lagged);
run_closed_loop_model_once(model_cfg.model_name, path_file, out_file, cfg);
local_write_audit(out_file, 'modern_tcn', model_cfg, root, path_file, ...
    cfg.modern_tcn_sim_cfg);
end

function tf = local_model_uses_lagged_cmd_input(model_cfg)
label_l = lower(char(string(model_cfg.label)));
dataset_l = lower(char(string(model_cfg.dataset_file)));
model_l = lower(char(string(model_cfg.model_name)));
tf = contains(model_l, '30dtest') || contains(label_l, '30d') || ...
    contains(label_l, 'cmdresp') || contains(dataset_l, 'cmdresp_lite_v1') || ...
    contains(dataset_l, 'cmdresp_lag1_only_v1');
end

function preflight = local_preflight(root, paths, models)
plant = agv_plant_revision(parameters());
checks = struct();
checks.plant_revision = strcmp(plant.id, 'agv_physics_v2_plantfix');
checks.dataset = exist(models.dataset_file, 'file') == 2;
for i = 1:numel(models.runs)
    key = matlab.lang.makeValidName(char("onnx_" + models.runs(i).label));
    checks.(key) = exist(models.runs(i).onnx_file, 'file') == 2;
end
checks.learned_shell = local_exists_model(root, 'LPVMPC_AGV_simulink_Modern_TCN');
checks.three_paths = all(cellfun(@(p) exist(p, 'file') == 2, paths));
checks.maps_candidate = exist(local_maps_file(root), 'file') == 2;
for i = 1:numel(models.runs)
    key = matlab.lang.makeValidName(char("model_" + models.runs(i).label));
    checks.(key) = local_exists_model(root, models.runs(i).model_name);
end
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
    if path_runs.status(i) ~= "ok"
        continue;
    end
    f = char(path_runs.summary_file(i));
    if exist(f, 'file') ~= 2
        continue;
    end
    T = readtable(f, 'TextType', 'string');
    T.path_tag = repmat(path_runs.path_tag(i), height(T), 1);
    summary_table = [summary_table; T]; %#ok<AGROW>
end
if isempty(summary_table)
    aggregate_table = table();
    return;
end
controllers = unique(summary_table.controller, 'stable');
rows = repmat(local_aggregate_row(), numel(controllers), 1);
for i = 1:numel(controllers)
    mask = summary_table.controller == controllers(i);
    sub = summary_table(mask, :);
    rows(i).controller = controllers(i);
    rows(i).n_paths = height(sub);
    rows(i).ey_rmse_mean = mean(sub.ey_rmse, 'omitnan');
    rows(i).ey_peak_worst = max(sub.ey_peak, [], 'omitnan');
    rows(i).xy_rmse_mean = mean(sub.xy_rmse, 'omitnan');
    rows(i).j_du_mean = mean(sub.j_du, 'omitnan');
    rows(i).theta_mae_mean = mean(sub.theta_mae_deg, 'omitnan');
    rows(i).main_acc_mean = mean(sub.main_acc_pct, 'omitnan');
    rows(i).turn_acc_mean = mean(sub.turn_acc_pct, 'omitnan');
end
aggregate_table = struct2table(rows);
aggregate_table.rank_ey = tiedrank(aggregate_table.ey_rmse_mean);
aggregate_table = sortrows(aggregate_table, {'rank_ey', 'xy_rmse_mean', 'j_du_mean'});
end

function row = local_path_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", ...
    'champion_file', "", 'candidate1_file', "", 'candidate2_file', "", ...
    'extra_files', "", 'summary_file', "", 'rank_file', "", ...
    'status', "pending", 'message', "");
end

function row = local_aggregate_row()
row = struct('controller', "", 'n_paths', 0, 'ey_rmse_mean', NaN, ...
    'ey_peak_worst', NaN, 'xy_rmse_mean', NaN, 'j_du_mean', NaN, ...
    'theta_mae_mean', NaN, 'main_acc_mean', NaN, 'turn_acc_mean', NaN);
end

function local_write_audit(out_file, kind, model_cfg, root, path_file, sim_model_cfg)
audit = struct();
audit.kind = kind;
audit.label = char(model_cfg.label);
audit.seed = model_cfg.seed;
audit.dataset_file = model_cfg.dataset_file;
audit.onnx_file = model_cfg.onnx_file;
audit.run_tag = model_cfg.run_tag;
audit.simulink_model = model_cfg.model_name;
audit.path_file = path_file;
audit.created_at = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
audit.project_root = root;
if nargin >= 6
    audit.modern_tcn_sim_cfg = sim_model_cfg;
end
local_write_json(strrep(out_file, '_out.mat', '_model_audit.json'), audit);
end

function local_relabel_compare_outputs(path_dir, file_prefix, runs, run_files, path_file)
label_map = containers.Map({'GRU', 'TCN'}, {char(runs(2).label), char(runs(3).label)});
for suffix = ["summary", "zones", "rank"]
    file = fullfile(path_dir, sprintf('%s_%s.csv', file_prefix, suffix));
    if exist(file, 'file') ~= 2
        continue;
    end
    T = readtable(file, 'TextType', 'string');
    if ismember('controller', T.Properties.VariableNames)
        for i = 1:height(T)
            key = char(T.controller(i));
            if isKey(label_map, key)
                T.controller(i) = string(label_map(key));
            end
        end
    end
    writetable(T, file);
end
report_file = fullfile(path_dir, sprintf('%s_report.md', file_prefix));
summary_file = fullfile(path_dir, sprintf('%s_summary.csv', file_prefix));
rank_file = fullfile(path_dir, sprintf('%s_rank.csv', file_prefix));
zone_file = fullfile(path_dir, sprintf('%s_zones.csv', file_prefix));
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# %s\n\n', strrep(char(file_prefix), '_', ' '));
fprintf(fid, '- path_file: `%s`\n', path_file);
fprintf(fid, '- output_dir: `%s`\n\n', path_dir);
fprintf(fid, '## Run Files\n\n');
for i = 1:numel(runs)
    fprintf(fid, '- %s: `%s`\n', runs(i).label, run_files(i));
end
if exist(rank_file, 'file') == 2
    fprintf(fid, '\n## Rank\n\n');
    local_write_table_md(fid, readtable(rank_file, 'TextType', 'string'));
end
if exist(summary_file, 'file') == 2
    fprintf(fid, '\n## Summary\n\n');
    local_write_table_md(fid, readtable(summary_file, 'TextType', 'string'));
end
if exist(zone_file, 'file') == 2
    fprintf(fid, '\n## Zones\n\n');
    local_write_table_md(fid, readtable(zone_file, 'TextType', 'string'));
end
end

function local_write_report(node_dir, result)
report_file = fullfile(node_dir, 'modern_multiseed_report.md');
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# ModernTCN l020 tt25 Multiseed Closed-Loop Report\n\n');
fprintf(fid, '- generated: `%s`\n', result.timestamp);
fprintf(fid, '- output_dir: `%s`\n', node_dir);
fprintf(fid, '- dataset: `%s`\n\n', result.models.dataset_file);
fprintf(fid, '## Models\n\n');
for i = 1:numel(result.models.runs)
    fprintf(fid, '- %s: `%s`\n', result.models.runs(i).label, result.models.runs(i).onnx_file);
end
if isfield(result, 'aggregate_table') && ~isempty(result.aggregate_table)
    fprintf(fid, '\n## Aggregate\n\n');
    local_write_table_md(fid, result.aggregate_table);
end
if isfield(result, 'summary_table') && ~isempty(result.summary_table)
    keep = {'controller', 'path_tag', 'ey_rmse', 'ey_peak', 'xy_rmse', ...
        'theta_mae_deg', 'main_acc_pct', 'turn_acc_pct'};
    fprintf(fid, '\n## Per-Path Summary\n\n');
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
        if iscell(v); v = v{1}; end
        if isstring(v) || ischar(v)
            vals{j} = char(string(v));
        elseif isnumeric(v)
            vals{j} = sprintf('%.6g', v);
        elseif islogical(v)
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
if isfield(cfg, name) && ~isempty(cfg.(name))
    value = cfg.(name);
else
    value = default_value;
end
end

function value = local_field_or_default(s, name, default_value)
if isstruct(s) && isfield(s, name)
    value = s.(name);
else
    value = default_value;
end
end
