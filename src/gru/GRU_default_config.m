function cfg = GRU_default_config(root)
%GRU_DEFAULT_CONFIG Current frozen GRU deployment artifact.

if nargin < 1 || isempty(root)
    root = local_project_root();
end

cfg = struct();
cfg.seed = 101;
cfg.case_name = 'inputstats_hidden96_l2';
cfg.run_tag = 'gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101';
cfg.dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat');
cfg.raw_train_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v2.mat');
cfg.model_file = fullfile(root, 'data', 'models', ...
    'GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat');
cfg.meta_file = fullfile(root, 'data', 'models', ...
    'GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat');
cfg.summary_file = fullfile(root, 'results', 'gru', 'train_logs_theta10_uniform_h0_v2', ...
    'GRU_theta10_v2_multi_seed_summary.csv');
cfg.group_summary_file = fullfile(root, 'results', 'gru', 'train_logs_theta10_uniform_h0_v2', ...
    'GRU_theta10_v2_group_summary.csv');
cfg.report_file = fullfile(root, 'results', 'gru', 'train_logs_theta10_uniform_h0_v2', ...
    sprintf('%s_seed%d', cfg.case_name, cfg.seed), 'GRU_train_report.md');
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
