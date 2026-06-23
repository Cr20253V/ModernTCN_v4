function result = run_e4_mode_theta_flatreg001_rerun_closed_loop()
%RUN_E4_MODE_THETA_FLATREG001_RERUN_CLOSED_LOOP Sandbox closed-loop check.
%
% This script evaluates the retrained E4 candidate
% `mode_theta_detach_flatreg001_seed21_rerun_20260622` against the locked
% baseline on the default sharp-turn transition path. All outputs stay under
% the rerun directory; the historical flatreg001 run directory is not touched.

init_project();
root = project_root();

run_tag = 'mode_theta_detach_flatreg001_seed21_rerun_20260622';
run_dir = fullfile(root, 'results', 'modern_tcn_sci_innovation', ...
    '04_mode_conditioned_theta', run_tag);
out_root = fullfile(root, 'results', 'modern_tcn_sci_innovation', ...
    '04_mode_conditioned_theta', 'e4_cl_001r_20260622');

path_file = fullfile(root, 'data', 'paths', ...
    'path_closed_loop_sharp_turn_transition_theta10_v1.mat');
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');

baseline_onnx = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn', ...
    'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101', ...
    'modern_tcn_seed101.onnx');
candidate_onnx = fullfile(run_dir, 'onnx_sandbox', ...
    'mode_theta_detach_flatreg001_seed21_rerun_20260622.onnx');

must_exist(path_file, 'path file');
must_exist(dataset_file, 'dataset file');
must_exist(baseline_onnx, 'baseline ONNX');
must_exist(candidate_onnx, 'candidate ONNX');

if exist(out_root, 'dir') ~= 7
    mkdir(out_root);
end

baseline_out = fullfile(out_root, 'base_out.mat');
candidate_out = fullfile(out_root, 'cand_out.mat');
file_prefix = 'e4_001r';
expected_outputs = {baseline_out, candidate_out, ...
    fullfile(out_root, [file_prefix '_summary.csv']), ...
    fullfile(out_root, [file_prefix '_zones.csv']), ...
    fullfile(out_root, [file_prefix '_rank.csv']), ...
    fullfile(out_root, [file_prefix '_compare.mat']), ...
    fullfile(out_root, [file_prefix '_report.md']), ...
    fullfile(out_root, 'status.json'), ...
    fullfile(out_root, 'result.mat')};
for i = 1:numel(expected_outputs)
    if exist(expected_outputs{i}, 'file') == 2
        error('e4_mode_theta_rerun:NoOverwrite', ...
            'Closed-loop output already exists: %s', expected_outputs{i});
    end
end

baseline_info = struct();
baseline_info.seed = 101;
baseline_info.run_tag = 'baseline_lock_seed101';
baseline_info.dataset_file = dataset_file;
baseline_info.onnx_file = baseline_onnx;

candidate_info = struct();
candidate_info.seed = 21;
candidate_info.run_tag = run_tag;
candidate_info.dataset_file = dataset_file;
candidate_info.onnx_file = candidate_onnx;

fprintf('[E4 rerun sandbox] baseline closed-loop\n');
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
    path_file, baseline_out, local_sim_cfg(baseline_info));

fprintf('[E4 rerun sandbox] candidate closed-loop\n');
run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
    path_file, candidate_out, local_sim_cfg(candidate_info));

extra_runs = struct('label', string(run_tag), 'file', candidate_out);
compare_result = compare_tcn_gru_modern_closed_loop_out( ...
    baseline_out, '__skip_gru__', '__skip_tcn__', path_file, out_root, ...
    "baseline_lock_seed101", extra_runs, ...
    'E4 mode-conditioned theta flatreg001 rerun sandbox closed-loop screening', ...
    file_prefix);

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.scope = 'E4 sandbox-only rerun closed-loop';
result.rerun_candidate = run_tag;
result.path_file = path_file;
result.dataset_file = dataset_file;
result.run_dir = run_dir;
result.out_root = out_root;
result.baseline_onnx = baseline_onnx;
result.candidate_onnx = candidate_onnx;
result.baseline_out = baseline_out;
result.candidate_out = candidate_out;
result.compare_result = compare_result;
result.summary_file = compare_result.summary_file;
result.zone_file = compare_result.zone_file;
result.rank_file = compare_result.rank_file;
result.report_file = compare_result.report_file;
result.status_file = fullfile(out_root, 'status.json');
result.mat_file = fullfile(out_root, 'result.mat');
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
status.dataset_file = result.dataset_file;
status.run_dir = result.run_dir;
status.out_root = result.out_root;
status.baseline_onnx = result.baseline_onnx;
status.candidate_onnx = result.candidate_onnx;
status.baseline_out = result.baseline_out;
status.candidate_out = result.candidate_out;
status.summary_file = result.summary_file;
status.zone_file = result.zone_file;
status.rank_file = result.rank_file;
status.report_file = result.report_file;
status.formal_validation = false;
status.formal_compare_write = false;
status.original_flatreg001_overwritten = false;
end

function must_exist(path, label)
if exist(path, 'file') ~= 2
    error('e4_mode_theta_rerun:MissingFile', ...
        'Missing %s: %s', label, path);
end
end
