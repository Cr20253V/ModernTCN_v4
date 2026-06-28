function result = run_fair10_closed_loop(cfg)
%RUN_FAIR10_CLOSED_LOOP Manifest-driven closed-loop runner for fair 10-seed protocol.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();
node_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '19_fair_10seed_selection_and_final_test_path_extension');
path_split = local_cfg(cfg, 'path_split', 'validation_sentinel');
reuse_existing = logical(local_cfg(cfg, 'reuse_existing', true));
stop_time_override = local_cfg(cfg, 'stop_time_override', []);
disturbance_mode = local_cfg(cfg, 'disturbance_mode', 'hybrid');
disturbance_seed = local_cfg(cfg, 'disturbance_seed', 20260625);
disturbance_levels = local_cfg(cfg, 'disturbance_levels', [0 1 2]);

switch char(path_split)
    case 'validation_sentinel'
        manifest_file = local_cfg(cfg, 'manifest_file', fullfile(node_root, '04_validation_sentinel_closed_loop', 'sentinel_manifest.csv'));
        out_root = fullfile(node_root, '04_validation_sentinel_closed_loop');
        path_files = {
            fullfile(root, 'data', 'paths', 'agv_theta10_uniform_v2', 'agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat')
            fullfile(root, 'data', 'paths', 'agv_theta10_uniform_v2', 'agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat')
        };
    case 'final_test'
        manifest_file = local_cfg(cfg, 'manifest_file', fullfile(node_root, '05_seed_selection', 'selected_seed_decision.csv'));
        out_root = fullfile(node_root, '06_final_test_closed_loop');
        path_files = {
            fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v10.mat')
            fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
            fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
            fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1.mat')
            fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1.mat')
            fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_downhill_straight_after_turn_v1.mat')
        };
    case 'disturbance_validation'
        manifest_file = local_cfg(cfg, 'manifest_file', fullfile(node_root, '05_seed_selection', 'selected_seed_decision.csv'));
        out_root = fullfile(node_root, '07_disturbance_validation');
        path_files = {
            fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
            fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
        };
    otherwise
        error('run_fair10_closed_loop:BadPathSplit', 'Unsupported path_split: %s', char(path_split));
end

local_assert_file(manifest_file, 'manifest file');
if exist(out_root, 'dir') ~= 7
    mkdir(out_root);
end

switch char(path_split)
    case 'validation_sentinel'
        selected = local_read_manifest(manifest_file);
        selected = selected(strcmpi(string(selected.enter_validation_sentinel), "true") | strcmpi(string(selected.enter_validation_sentinel), "1"), :);
        required_cols = {'algorithm_id', 'seed', 'candidate_id', 'checkpoint_file', 'onnx_file', 'sample_file', 'summary_csv', 'history_csv', 'config_json', 'report_file'};
        local_require_columns(selected, required_cols, 'validation sentinel manifest');
    otherwise
        selected = local_read_manifest(manifest_file);
        selected = selected(strcmpi(string(selected.selection_status), "pass"), :);
        required_cols = {'algorithm_id', 'selected_seed', 'selected_candidate_id', 'checkpoint_file', 'onnx_file', 'sample_file', 'summary_csv', 'history_csv', 'config_json', 'report_file'};
        local_require_columns(selected, required_cols, 'selection manifest');
end

if height(selected) == 0
    error('run_fair10_closed_loop:NoSelectedCandidates', 'No selected candidates found for %s.', char(path_split));
end

baseline_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation');
rows = repmat(local_empty_row(), numel(path_files), 1);
for p = 1:numel(path_files)
    path_file = path_files{p};
    local_assert_file(path_file, 'path file');
    [~, path_tag] = fileparts(path_file);
    path_dir = fullfile(out_root, path_tag);
    if exist(path_dir, 'dir') ~= 7
        mkdir(path_dir);
    end
    baseline_out = local_baseline_out(baseline_root, path_tag);
    local_assert_file(baseline_out, 'baseline output');

    extra_runs = struct('label', {}, 'file', {});
    candidate_files = strings(height(selected), 1);
    for i = 1:height(selected)
        if strcmp(char(path_split), 'validation_sentinel')
            candidate_id = char(selected.candidate_id(i));
            seed = double(selected.seed(i));
            checkpoint_file = char(selected.checkpoint_file(i));
            onnx_file = char(selected.onnx_file(i));
            sample_file = char(selected.sample_file(i));
        else
            candidate_id = char(selected.selected_candidate_id(i));
            seed = double(selected.selected_seed(i));
            checkpoint_file = char(selected.checkpoint_file(i));
            onnx_file = char(selected.onnx_file(i));
            sample_file = char(selected.sample_file(i));
        end
        candidate_out = fullfile(path_dir, sprintf('%s_out.mat', candidate_id));
        cfg_one = struct();
        if ~isempty(stop_time_override)
            cfg_one.stop_time_override = stop_time_override;
        end
        cfg_one.params_override = parameters();
        modern_cfg = struct();
        modern_cfg.seed = seed;
        modern_cfg.run_tag = candidate_id;
        modern_cfg.dataset_file = fullfile(root, 'data', 'tcn', 'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
        modern_cfg.onnx_file = onnx_file;
        modern_cfg.checkpoint_file = checkpoint_file;
        modern_cfg.sample_file = sample_file;
        modern_cfg.candidate_id = candidate_id;
        cfg_one.modern_tcn_sim_cfg = modern_cfg;
        if strcmp(char(path_split), 'disturbance_validation')
            cfg_one.robustness_case = struct('disturbance_mode', disturbance_mode, 'disturbance_seed', disturbance_seed, 'disturbance_level', NaN);
        end
        if ~(reuse_existing && local_output_complete(candidate_out))
            run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', path_file, candidate_out, cfg_one);
        end
        extra_runs(end+1) = struct('label', string(candidate_id), 'file', candidate_out); %#ok<AGROW>
        candidate_files(i) = string(candidate_out);
    end

    compare_label = 'ModernTCN';
    report_title = sprintf('Fair 10-seed closed-loop: %s', path_tag);
    prefix = char(path_split);
    compare_tcn_gru_modern_closed_loop_out( ...
        baseline_out, '__skip_gru__', '__skip_tcn__', path_file, path_dir, ...
        compare_label, extra_runs, report_title, prefix);

    rows(p).path_tag = string(path_tag);
    rows(p).path_file = string(path_file);
    rows(p).out_dir = string(path_dir);
    rows(p).baseline_file = string(baseline_out);
    rows(p).candidate_files = strjoin(candidate_files, ';');
    rows(p).summary_file = string(fullfile(path_dir, [prefix '_summary.csv']));
    rows(p).rank_file = string(fullfile(path_dir, [prefix '_rank.csv']));
    rows(p).report_file = string(fullfile(path_dir, [prefix '_report.md']));
    rows(p).status = "ok";
end

path_table = struct2table(rows);
writetable(path_table, fullfile(out_root, sprintf('%s_path_runs.csv', char(path_split))));
result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.node_root = node_root;
result.out_root = out_root;
result.path_split = path_split;
result.path_table = path_table;
result.summary_file = fullfile(out_root, sprintf('%s_execution_summary.md', char(path_split)));
result.mat_file = fullfile(out_root, sprintf('%s_result.mat', char(path_split)));
save(result.mat_file, 'result', '-v7.3');
local_write_summary(result);
end

function T = local_read_manifest(path)
opts = detectImportOptions(path, 'TextType', 'string', 'Delimiter', ',');
opts.VariableNamingRule = 'preserve';
T = readtable(path, opts);
end

function local_require_columns(T, required_cols, label)
vars = string(T.Properties.VariableNames);
missing = required_cols(~ismember(required_cols, vars));
if ~isempty(missing)
    error('run_fair10_closed_loop:MissingColumns', '%s missing columns: %s', label, strjoin(missing, ', '));
end
end

function baseline_out = local_baseline_out(baseline_root, path_tag)
candidate = fullfile(baseline_root, path_tag, 'baseline_lock_out.mat');
if exist(candidate, 'file') == 2
    baseline_out = candidate;
    return;
end
fallback = fullfile(baseline_root, path_tag, 'window2_formal_out.mat');
if exist(fallback, 'file') == 2
    baseline_out = fallback;
    return;
end
error('run_fair10_closed_loop:MissingBaselineOut', 'Missing baseline output for path %s', path_tag);
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
    error('run_fair10_closed_loop:MissingFile', 'Missing %s: %s', label, file);
end
end

function tf = local_output_complete(out_file)
tf = false;
if exist(out_file, 'file') ~= 2
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

function row = local_empty_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", 'baseline_file', "", 'candidate_files', "", 'summary_file', "", 'rank_file', "", 'report_file', "", 'status', "");
end

function local_write_summary(result)
fid = fopen(result.summary_file, 'w', 'n', 'UTF-8');
if fid < 0
    return;
end
cleanup = onCleanup(@() fclose(fid)); %#ok<NASGU>
fprintf(fid, '# Fair 10-Seed Closed-Loop Execution Summary\n\n');
fprintf(fid, '- timestamp: `%s`\n', result.timestamp);
fprintf(fid, '- path split: `%s`\n', char(result.path_split));
fprintf(fid, '- output root: `%s`\n\n', result.out_root);
fprintf(fid, '| path | status | summary | report |\n');
fprintf(fid, '|---|---|---|---|\n');
for i = 1:height(result.path_table)
    fprintf(fid, '| `%s` | %s | `%s` | `%s` |\n', result.path_table.path_tag(i), result.path_table.status(i), result.path_table.summary_file(i), result.path_table.report_file(i));
end
end
