function cfg = ModernTCN_default_config(root)
%MODERNTCN_DEFAULT_CONFIG 当前冻结的 ModernTCN 部署配置。
%
% 这里只保存当前闭环仿真使用的默认模型。需要临时测试其他 checkpoint 时，仍可在调用脚本中传入 cfg
% 覆盖 seed、dataset_file、run_tag 或 onnx_file。

if nargin < 1 || isempty(root)
    root = local_project_root();
end

cfg = struct();
cfg.seed = 21;
cfg.run_tag = 'modern_tcn_theta10_uniform_h0_v2_seed21';
cfg.dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat');
cfg.raw_train_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v2.mat');
cfg.onnx_file = fullfile(root, 'results', 'modern_tcn', cfg.run_tag, ...
    'modern_tcn_seed21.onnx');
cfg.reference_dir = fullfile(root, 'results', 'modern_tcn', cfg.run_tag);
cfg.pytorch_reference_file = fullfile(root, 'results', 'modern_tcn', cfg.run_tag, ...
    'modern_tcn_seed21_pytorch_reference.mat');

% Deployment-side theta conditioning for closed-loop scheduling. A concrete
% checkpoint must set these fields after the next dataset/model is selected.
cfg.theta_output_gain = 1.0;
cfg.theta_abs_limit = deg2rad(12.0);
cfg.theta_rate_limit = deg2rad(5.0);
cfg.theta_mpc_deadzone = deg2rad(2.0);
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
