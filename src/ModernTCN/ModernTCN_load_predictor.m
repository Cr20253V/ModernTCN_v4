function predictor = ModernTCN_load_predictor(seed, onnx_file)
%MODERNTCN_LOAD_PREDICTOR 加载一个 ModernTCN ONNX 模型，返回在线推理句柄。
%
% 功能说明：
%   本函数是后续 Simulink 接入前的 MATLAB 在线推理入口。它只负责把指定
%   seed 的 ONNX 文件导入为 dlnetwork，并记录标签映射、输入窗口尺寸等信息。
%   真正的单窗口推理由 ModernTCN_predict_window 完成。
%
% 用法：
%   init_project;
%   addpath(fullfile(project_root(), 'src', 'ModernTCN'));
%   predictor = ModernTCN_load_predictor();
%
% 输入：
%   seed      : 可选，默认 21。默认定位当前推荐的 V4 theta-head B 候选。
%   onnx_file : 可选，自定义 ONNX 路径。为空时按 seed 自动定位。
%
% 输出：
%   predictor : 结构体，包含 net、seed、onnx_file、input_size 和标签映射。

root = local_project_root();
default_cfg = ModernTCN_default_config(root);
if nargin < 1 || isempty(seed)
    seed = default_cfg.seed;
end

if nargin < 2 || isempty(onnx_file)
    if seed == default_cfg.seed
        onnx_file = default_cfg.onnx_file;
    else
        onnx_file = fullfile(root, 'results', 'modern_tcn', default_cfg.run_tag, ...
            sprintf('modern_tcn_seed%d.onnx', seed));
    end
end

if exist(onnx_file, 'file') ~= 2
    error('ModernTCN:MissingONNX', '找不到 ONNX 文件: %s', onnx_file);
end

% MATLAB ONNX importer 会为部分算子生成 custom layer。这里把生成位置固定
% 在 src/ModernTCN/generated_layers，避免污染项目根目录。
layer_root = fullfile(root, 'src', 'ModernTCN', 'generated_layers');
if exist(layer_root, 'dir') ~= 7
    mkdir(layer_root);
end
addpath(layer_root);

old_dir = pwd;
cleanup = onCleanup(@() cd(old_dir));
cd(layer_root);
net = importNetworkFromONNX(onnx_file, Namespace="modern_tcn_onnx_layers");

predictor = struct();
predictor.seed = seed;
predictor.onnx_file = string(onnx_file);
predictor.layer_root = string(layer_root);
predictor.net = net;
predictor.input_size = [128 19];              % [time, feature]
predictor.onnx_input_size = [1 128 19];       % [batch, time, feature]
predictor.main_labels = [1 2 3];              % 1=flat, 2=stall, 3=slope
predictor.turn_labels = [-1 0 1];             % -1=right, 0=straight, 1=left
predictor.theta_unit = "rad";
predictor.theta_output_unit = "deg";
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
