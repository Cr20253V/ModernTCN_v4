function manual_fill_baseline_lock()
%MANUAL_FILL_BASELINE_LOCK Fill missing baseline_lock_out.mat files for the 19-path extension flow.

root = local_project_root();
addpath(root);
addpath(genpath(fullfile(root, 'src')));
addpath(fullfile(root, 'simulink'));

dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
baseline_onnx = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn', ...
    'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101', ...
    'modern_tcn_seed101.onnx');

path_files = {
    fullfile(root, 'data', 'paths', 'agv_theta10_uniform_v2', 'agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16.mat')
    fullfile(root, 'data', 'paths', 'agv_theta10_uniform_v2', 'agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06.mat')
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v10.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_positive_slope_lr_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_positive_slope_factory_loop_190_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_flat_right_entry_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_uphill_left_overlap_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_downhill_right_reversal_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_downhill_straight_after_turn_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_uphill_straight_after_downhill_v1.mat')
    fullfile(root, 'data', 'paths', 'factory_targeted_eval', 'path_factory_target_final_flat_release_v1.mat')
};

out_files = {
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'agv_theta10_uniform_v2_036_short_bin06_m04p5_theta_edge_speed_R16', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'agv_theta10_uniform_v2_039_short_bin09_m01p5_right_R06', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_logistics_showcase_theta10_v10', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_closed_loop_sharp_turn_transition_theta10_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_closed_loop_long_updown_theta10_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_soft_updown_straight_turn_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_factory_flat_logistics_safe_190_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_flat_clean_s_turn_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_positive_slope_lr_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_modern_tcn_showcase_candidate_positive_slope_factory_loop_190_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_flat_right_entry_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_uphill_left_overlap_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_downhill_right_reversal_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_downhill_straight_after_turn_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_uphill_straight_after_downhill_v1', 'baseline_lock_out.mat')
    fullfile(root, 'results', 'modern_tcn_metric_rebuild', '05_sandbox_closed_loop_if_needed', '03_formal_validation', 'path_factory_target_final_flat_release_v1', 'baseline_lock_out.mat')
};

for i = 1:numel(path_files)
    path_file = path_files{i};
    out_file = out_files{i};
    out_dir = fileparts(out_file);
    if exist(path_file, 'file') ~= 2
        error('manual_fill_baseline_lock:MissingPath', 'Missing path file: %s', path_file);
    end
    if exist(baseline_onnx, 'file') ~= 2
        error('manual_fill_baseline_lock:MissingONNX', 'Missing baseline ONNX: %s', baseline_onnx);
    end
    if exist(dataset_file, 'file') ~= 2
        error('manual_fill_baseline_lock:MissingDataset', 'Missing dataset file: %s', dataset_file);
    end
    if exist(out_dir, 'dir') ~= 7
        mkdir(out_dir);
    end
    if exist(out_file, 'file') == 2
        fprintf('[baseline-fill] skip existing: %s\n', out_file);
        continue;
    end

    sim_cfg = struct();
    sim_cfg.params_override = parameters();
    modern_cfg = struct();
    modern_cfg.seed = 101;
    modern_cfg.run_tag = 'baseline_lock';
    modern_cfg.dataset_file = dataset_file;
    modern_cfg.onnx_file = baseline_onnx;
    sim_cfg.modern_tcn_sim_cfg = modern_cfg;

    fprintf('[baseline-fill] %d/%d %s -> %s\n', i, numel(path_files), path_file, out_file);
    run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', path_file, out_file, sim_cfg);
end

status_file = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '19_fair_10seed_selection_and_final_test_path_extension', '00_protocol_lock', ...
    'baseline_lock_fill_status.txt');
fid = fopen(status_file, 'w');
if fid >= 0
    cleanup = onCleanup(@() fclose(fid)); %#ok<NASGU>
    fprintf(fid, 'ok\n');
end
fprintf('[baseline-fill] done\n');
end

function root = local_project_root()
this_file = mfilename('fullpath');
this_dir = fileparts(this_file);
root = this_dir;
while exist(fullfile(root, 'init_project.m'), 'file') ~= 2
    parent_dir = fileparts(root);
    if strcmp(parent_dir, root)
        error('manual_fill_baseline_lock:ProjectRootNotFound', ...
            'Could not find init_project.m above %s.', this_dir);
    end
    root = parent_dir;
end
end
