function result = run_uncertainty_seed101_rerun_closed_loop()
%RUN_UNCERTAINTY_SEED101_RERUN_CLOSED_LOOP Run one sandbox closed-loop check.
%
% This evaluates the E1 rerun candidate
% `uncertainty_seed101_rerun_20260622` against the locked baseline on the
% default sandbox path. Outputs stay under metric_rebuild sandbox only.

init_project();
root = project_root();

out_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '05_sandbox_closed_loop_if_needed', '02_uncertainty_seed101_rerun_20260622');
path_file = fullfile(root, 'data', 'paths', ...
    'path_closed_loop_sharp_turn_transition_theta10_v1.mat');
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');

baseline_onnx = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn', ...
    'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101', ...
    'modern_tcn_seed101.onnx');
candidate_onnx = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '05_sandbox_closed_loop_if_needed', '00_exported_onnx', ...
    'uncertainty_seed101_rerun_20260622', ...
    'uncertainty_seed101_rerun_20260622.onnx');

must_exist(path_file, 'path file');
must_exist(dataset_file, 'dataset file');
must_exist(baseline_onnx, 'baseline ONNX');
must_exist(candidate_onnx, 'candidate ONNX');

if exist(out_root, 'dir') ~= 7
    mkdir(out_root);
end

baseline_out = fullfile(out_root, 'baseline_lock_out.mat');
candidate_out = fullfile(out_root, 'uncertainty_seed101_rerun_20260622_out.mat');
summary_file = fullfile(out_root, 'uncertainty_seed101_rerun_summary.csv');
if exist(baseline_out, 'file') == 2 || exist(candidate_out, 'file') == 2 || exist(summary_file, 'file') == 2
    error('uncertainty_rerun:NoOverwrite', ...
        'Closed-loop output already exists in %s; refusing to overwrite.', out_root);
end

baseline_info = struct();
baseline_info.seed = 101;
baseline_info.run_tag = 'baseline_lock';
baseline_info.dataset_file = dataset_file;
baseline_info.onnx_file = baseline_onnx;

candidate_info = struct();
candidate_info.seed = 101;
candidate_info.run_tag = 'uncertainty_seed101_rerun_20260622';
candidate_info.dataset_file = dataset_file;
candidate_info.onnx_file = candidate_onnx;

fprintf('[uncertainty rerun sandbox] baseline closed-loop\n');
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
    path_file, baseline_out, local_sim_cfg(baseline_info));

fprintf('[uncertainty rerun sandbox] candidate closed-loop\n');
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
    path_file, candidate_out, local_sim_cfg(candidate_info));

extra_runs = struct('label', "uncertainty_seed101_rerun_20260622", ...
    'file', candidate_out);
compare_result = compare_tcn_gru_modern_closed_loop_out( ...
    baseline_out, '__skip_gru__', '__skip_tcn__', path_file, out_root, ...
    "baseline_lock", extra_runs, ...
    'Uncertainty seed101 rerun sandbox closed-loop screening', ...
    'uncertainty_seed101_rerun');

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.scope = 'sandbox-only rerun closed-loop';
result.rerun_candidate = 'uncertainty_seed101_rerun_20260622';
result.path_file = path_file;
result.out_root = out_root;
result.baseline_out = baseline_out;
result.candidate_out = candidate_out;
result.compare_result = compare_result;
result.summary_file = compare_result.summary_file;
result.rank_file = compare_result.rank_file;
result.report_file = compare_result.report_file;
result.status_file = fullfile(out_root, 'uncertainty_seed101_rerun_status.json');
result.mat_file = fullfile(out_root, 'uncertainty_seed101_rerun_result.mat');
save(result.mat_file, 'result', '-v7.3');
fid = fopen(result.status_file, 'w');
if fid >= 0
    cleanup = onCleanup(@() fclose(fid));
    fprintf(fid, '%s\n', jsonencode(local_status(result), PrettyPrint=true));
    delete(cleanup);
end
end

function sim_cfg = local_sim_cfg(info)
sim_cfg = struct();
sim_cfg.params_override = parameters();
modern_cfg = struct();
modern_cfg.seed = double(info.seed);
modern_cfg.run_tag = char(info.run_tag);
modern_cfg.dataset_file = char(info.dataset_file);
modern_cfg.onnx_file = char(info.onnx_file);
sim_cfg.modern_tcn_sim_cfg = modern_cfg;
end

function status = local_status(result)
status = struct();
status.timestamp = result.timestamp;
status.scope = result.scope;
status.rerun_candidate = result.rerun_candidate;
status.path_file = result.path_file;
status.out_root = result.out_root;
status.baseline_out = result.baseline_out;
status.candidate_out = result.candidate_out;
status.summary_file = result.summary_file;
status.rank_file = result.rank_file;
status.report_file = result.report_file;
status.formal_validation = false;
status.formal_compare_write = false;
end

function must_exist(path, label)
if exist(path, 'file') ~= 2
    error('uncertainty_rerun:MissingFile', 'Missing %s: %s', label, path);
end
end
