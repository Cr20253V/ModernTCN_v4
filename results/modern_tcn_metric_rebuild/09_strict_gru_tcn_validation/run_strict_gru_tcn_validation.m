function result = run_strict_gru_tcn_validation(cfg)
%RUN_STRICT_GRU_TCN_VALIDATION Re-run GRU/TCN on the frozen formal path set.
%
% This node compares GRU and TCN under the same path set and closed-loop
% execution shell used by the Window 2 formal validation. The baseline output
% is reused from Window 2 formal validation because it is already the frozen
% reference run for the same paths.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();

node_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '09_strict_gru_tcn_validation');
baseline_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '05_sandbox_closed_loop_if_needed', '03_formal_validation');
if exist(node_root, 'dir') ~= 7
    mkdir(node_root);
end

path_files = local_cfg(cfg, 'path_files', local_default_path_files(root));
if isstring(path_files)
    path_files = cellstr(path_files);
elseif ischar(path_files)
    path_files = {path_files};
end
stop_time_override = local_cfg(cfg, 'stop_time_override', []);
reuse_existing = logical(local_cfg(cfg, 'reuse_existing', false));

gru_cfg = local_gru_cfg(root);
tcn_cfg = local_tcn_cfg(root);
local_assert_file(gru_cfg.dataset_file, 'GRU dataset');
local_assert_file(gru_cfg.model_file, 'GRU model');
local_assert_file(gru_cfg.meta_file, 'GRU meta');
local_assert_file(tcn_cfg.dataset_file, 'TCN dataset');
local_assert_file(tcn_cfg.model_file, 'TCN model');
local_assert_file(tcn_cfg.meta_file, 'TCN meta');

rows = repmat(local_empty_row(), numel(path_files), 1);
for p = 1:numel(path_files)
    path_file = path_files{p};
    local_assert_file(path_file, 'path file');
    [~, path_tag] = fileparts(path_file);
    path_dir = fullfile(node_root, path_tag);
    if exist(path_dir, 'dir') ~= 7
        mkdir(path_dir);
    end

    baseline_file = fullfile(baseline_root, path_tag, 'baseline_lock_out.mat');
    local_assert_file(baseline_file, 'Window 2 baseline output');

    gru_out = fullfile(path_dir, 'GRU_seed101_out.mat');
    tcn_out = fullfile(path_dir, 'TCN_seed101_out.mat');

    fprintf('[strict GRU/TCN] path %d/%d: %s\n', p, numel(path_files), path_tag);

    if ~(reuse_existing && exist(gru_out, 'file') == 2)
        sim_cfg = local_sim_cfg(stop_time_override);
        sim_cfg.gru_sim_cfg = gru_cfg;
        run_closed_loop_model_once('LPVMPC_AGV_simulink_GRU', ...
            path_file, gru_out, sim_cfg);
    end

    if ~(reuse_existing && exist(tcn_out, 'file') == 2)
        sim_cfg = local_sim_cfg(stop_time_override);
        sim_cfg.tcn_sim_cfg = tcn_cfg;
        run_closed_loop_model_once('LPVMPC_AGV_simulink_TCN', ...
            path_file, tcn_out, sim_cfg);
    end

    compare_tcn_gru_modern_closed_loop_out( ...
        baseline_file, gru_out, tcn_out, path_file, path_dir, ...
        "baseline_lock", [], ...
        sprintf('Strict GRU/TCN validation: %s', path_tag), ...
        'strict_gru_tcn');

    rows(p).path_tag = string(path_tag);
    rows(p).path_file = string(path_file);
    rows(p).out_dir = string(path_dir);
    rows(p).baseline_file = string(baseline_file);
    rows(p).gru_file = string(gru_out);
    rows(p).tcn_file = string(tcn_out);
    rows(p).summary_file = string(fullfile(path_dir, 'strict_gru_tcn_summary.csv'));
    rows(p).rank_file = string(fullfile(path_dir, 'strict_gru_tcn_rank.csv'));
    rows(p).report_file = string(fullfile(path_dir, 'strict_gru_tcn_report.md'));
    rows(p).status = "ok";
end

path_table = struct2table(rows);
path_runs_file = fullfile(node_root, 'strict_gru_tcn_path_runs.csv');
writetable(path_table, path_runs_file);

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.node_root = node_root;
result.baseline_root = baseline_root;
result.gru_cfg = gru_cfg;
result.tcn_cfg = tcn_cfg;
result.path_table = path_table;
result.path_runs_file = path_runs_file;
result.mat_file = fullfile(node_root, 'strict_gru_tcn_validation_result.mat');
result.summary_file = fullfile(node_root, 'strict_gru_tcn_execution_summary.md');
save(result.mat_file, 'result', '-v7.3');
local_write_summary(result);

fprintf('[strict GRU/TCN] path runs: %s\n', result.path_runs_file);
fprintf('[strict GRU/TCN] summary:   %s\n', result.summary_file);
end

function path_files = local_default_path_files(root)
path_files = {
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v3.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
};
end

function cfg = local_sim_cfg(stop_time_override)
cfg = struct();
if ~isempty(stop_time_override)
    cfg.stop_time_override = stop_time_override;
end
cfg.params_override = parameters();
end

function cfg = local_gru_cfg(root)
cfg = struct();
cfg.seed = 101;
cfg.case_name = 'inputstats_hidden96_l2';
cfg.run_tag = 'full_gru_v5_plantfix_passive17_plus_all5_seed101';
cfg.dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
cfg.model_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'models', ...
    'GRU_model_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat');
cfg.meta_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'models', ...
    'GRU_meta_full_gru_v5_plantfix_passive17_plus_all5_seed101.mat');
cfg.report_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'matlab_logs', ...
    'full_gru_v5_plantfix_passive17_plus_all5_seed101', ...
    'GRU_train_report.md');
end

function cfg = local_tcn_cfg(root)
cfg = struct();
cfg.seed = 101;
cfg.case_name = 'tcn96_rawtheta_sym';
cfg.run_tag = 'full_tcn_v5_plantfix_passive17_plus_all5_seed101';
cfg.dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
cfg.model_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'models', ...
    'TCN_model_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat');
cfg.meta_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'models', ...
    'TCN_meta_full_tcn_v5_plantfix_passive17_plus_all5_seed101.mat');
cfg.report_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'matlab_logs', ...
    'full_tcn_v5_plantfix_passive17_plus_all5_seed101', ...
    'TCN_train_report.md');
cfg.theta_output_gain = 1.0;
cfg.theta_abs_limit = deg2rad(12.0);
cfg.theta_rate_limit = deg2rad(5.0);
cfg.theta_mpc_deadzone = deg2rad(2.0);
end

function value = local_cfg(cfg, name, default_value)
if isstruct(cfg) && isfield(cfg, name) && ~isempty(cfg.(name))
    value = cfg.(name);
else
    value = default_value;
end
end

function local_assert_file(file, label)
if exist(file, 'file') ~= 2 && exist(file, 'file') ~= 4
    error('strict_gru_tcn:MissingFile', 'Missing %s: %s', label, file);
end
end

function row = local_empty_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", ...
    'baseline_file', "", 'gru_file', "", 'tcn_file', "", ...
    'summary_file', "", 'rank_file', "", 'report_file', "", ...
    'status', "");
end

function local_write_summary(result)
fid = fopen(result.summary_file, 'w');
if fid < 0
    warning('strict_gru_tcn:SummaryWriteFailed', ...
        'Cannot write summary: %s', result.summary_file);
    return;
end
cleanup = onCleanup(@() fclose(fid));

fprintf(fid, '# Strict GRU/TCN Validation Execution Summary\n\n');
fprintf(fid, '- scope: strict same-path closed-loop validation for GRU and TCN\n');
fprintf(fid, '- baseline source: `%s`\n', result.baseline_root);
fprintf(fid, '- GRU model: `%s`\n', result.gru_cfg.model_file);
fprintf(fid, '- TCN model: `%s`\n', result.tcn_cfg.model_file);
fprintf(fid, '- path runs: `%s`\n\n', result.path_runs_file);
fprintf(fid, '## Outputs\n\n');
fprintf(fid, '| path | status | summary | report |\n');
fprintf(fid, '|---|---|---|---|\n');
for i = 1:height(result.path_table)
    fprintf(fid, '| `%s` | %s | `%s` | `%s` |\n', ...
        result.path_table.path_tag(i), result.path_table.status(i), ...
        result.path_table.summary_file(i), result.path_table.report_file(i));
end
fprintf(fid, '\n');
fprintf(fid, 'Aggregated metric decisions are generated by the Python summarizer for this node.\n');
end
