function result = probe_candidate_path_rank(path_file)
%PROBE_CANDIDATE_PATH_RANK Run a narrow closed-loop probe on one path.

root = local_project_root();
init_project();
addpath(root);
addpath(genpath(fullfile(root, 'src')));
addpath(fullfile(root, 'simulink'));
if nargin < 1 || exist(path_file, 'file') ~= 2
    error('probe_candidate_path_rank:MissingPath', 'Missing path file: %s', path_file);
end

selected_csv = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '18_fair_10seed_selection_and_final_test_recut_recipe', '05_seed_selection', ...
    'selected_seed_decision.csv');
if exist(selected_csv, 'file') ~= 2
    error('probe_candidate_path_rank:MissingSelectedCSV', 'Missing selected_seed_decision.csv: %s', selected_csv);
end

opts = detectImportOptions(selected_csv, 'TextType', 'string', 'Delimiter', ',');
opts.VariableNamingRule = 'preserve';
T = readtable(selected_csv, opts);
fixed = T(T.("algorithm_id") == "modern_fixed", :);
uw = T(T.("algorithm_id") == "uncertainty_weighted", :);
if isempty(fixed) || isempty(uw)
    error('probe_candidate_path_rank:MissingSelectedRows', 'Missing selected rows in %s', selected_csv);
end

[~, path_tag] = fileparts(path_file);
baseline_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation');
baseline_out = local_baseline_out(baseline_root, path_tag);

probe_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '19_fair_10seed_selection_and_final_test_path_extension', 'tmp_path_probe', path_tag);
if exist(probe_root, 'dir') ~= 7
    mkdir(probe_root);
end

modern_fixed_out = fullfile(probe_root, 'modern_fixed_seed101_out.mat');
uw_out = fullfile(probe_root, 'uncertainty_weighted_seed101_out.mat');

run_one(fixed, modern_fixed_out, path_file);
run_one(uw, uw_out, path_file);

extra_runs = struct('label', {'modern_fixed_seed101', 'uncertainty_weighted_seed101'}, ...
    'file', {modern_fixed_out, uw_out});
compare_tcn_gru_modern_closed_loop_out( ...
    baseline_out, '__skip_gru__', '__skip_tcn__', path_file, probe_root, ...
    'ModernTCN', extra_runs, sprintf('Probe closed-loop: %s', path_tag), 'probe');

rank_file = fullfile(probe_root, 'probe_rank.csv');
rank_table = readtable(rank_file, 'TextType', 'string');
result = struct();
result.path_tag = string(path_tag);
result.probe_root = string(probe_root);
result.rank_file = string(rank_file);
result.rank_table = rank_table;
disp(rank_table);
end

function run_one(row, out_file, path_file)
if exist(out_file, 'file') == 2
    return;
end
cfg = struct();
cfg.params_override = parameters();
modern_cfg = struct();
modern_cfg.seed = double(row.("selected_seed"));
modern_cfg.run_tag = char(row.("selected_candidate_id"));
modern_cfg.dataset_file = fullfile(local_project_root(), 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
modern_cfg.onnx_file = char(row.("onnx_file"));
modern_cfg.checkpoint_file = char(row.("checkpoint_file"));
modern_cfg.sample_file = char(row.("sample_file"));
modern_cfg.candidate_id = char(row.("selected_candidate_id"));
cfg.modern_tcn_sim_cfg = modern_cfg;
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', path_file, out_file, cfg);
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
error('probe_candidate_path_rank:MissingBaselineOut', 'Missing baseline output for path %s', path_tag);
end

function root = local_project_root()
this_file = mfilename('fullpath');
this_dir = fileparts(this_file);
root = this_dir;
while exist(fullfile(root, 'init_project.m'), 'file') ~= 2
    parent_dir = fileparts(root);
    if strcmp(parent_dir, root)
        error('probe_candidate_path_rank:ProjectRootNotFound', ...
            'Could not find init_project.m above %s.', this_dir);
    end
    root = parent_dir;
end
end
