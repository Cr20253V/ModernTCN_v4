function [J, report] = evaluate_bo_point(X, params, db, options)
%EVALUATE_BO_POINT 评估单个 BO 参数点，复现优化时的目标函数计算。
%
%   [J, report] = evaluate_bo_point(X, params, db, options)
%
%   用途
%   - 用于“复评/一致性检查”：在不重新运行 bayesopt 的前提下，给定一个候选点 X，
%     以与 Bayesian_Optimization.m 中 objective_wrapper 尽量一致的流程构造控制器，
%     然后调用 Cost_Function 计算代价 J。
%   - 典型调用方：tools/check_bo_consistency.m。
%
%   输入
%   - X      : table 或 struct。通常是 bayesopt 的 bestPoint。
%              需要包含（至少）这些字段/变量名：
%              q_y, q_psi, q_v, q_omega,
%              log10_r_F, log10_r_omega, log10_rdF, log10_rdw。
%              其他字段会覆盖 frozen 默认值（见下方 frozen）。
%   - params : 工程参数结构体（由上层脚本/项目初始化提供）。
%   - db     : 线性化/插值数据库（lin_agv_grid 的输出）。若传入 []/empty，
%              本函数会生成一个小网格并调用 lin_agv_grid 自动构建（可能较慢）。
%   - options: 可选 struct。
%              * options.path_file : 路径 MAT 文件（会写入 cfg.path_file）
%              * options.zones     : 分段/路段定义（会写入 cfg.zones）
%              * options.scenes    : 场景权重 struct，覆盖默认 scenes。
%
%   输出
%   - J      : 标量代价（越小越好）。
%   - report : Cost_Function 产生的详细分解报告（包含各子项与统计）。
%
%   注意事项
%   - 本函数内部维护了一组 frozen 参数，目标是与 Bayesian_Optimization.m 保持一致。
%     如果你更新了优化脚本里的 frozen/地图逻辑，建议同步更新这里以保证复评一致。
%   - 若出现“同一点多次复评结果波动”，通常来自并行/求解器/初始化差异；
%     请用 tools/check_bo_consistency.m 做统计，而不要只看单次结果。

if nargin < 4
    options = struct();
end

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');

% 冻结参数（与 Bayesian_Optimization.m 保持一致）
frozen = struct();
frozen.alpha_Q = 0.5;
frozen.beta_Q = 0.5;
frozen.alpha_R = 0.5;
frozen.beta_R = 0.5;
frozen.alpha_dR = 0.5;
frozen.beta_dR = 0.5;
frozen.scale_umin_lo = 1.0;
frozen.scale_umin_hi = 1.0;
frozen.scale_umax_lo = 1.0;
frozen.scale_umax_hi = 1.0;
frozen.tau = 0.35;
frozen.omega_threshold = 0.15;
frozen.q_y_gain_max = 1.0;
frozen.theta_threshold = 0.04;
frozen.q_v_gain_max = 1.0;
frozen.transition_width = 0.03;
frozen.theta_transition_width = 0.02;
frozen.R_F_gain_max_uphill = 1.0;
frozen.R_F_gain_max_downhill = 1.0;
frozen.dR_F_gain_max_uphill = 1.0;
frozen.dR_F_gain_max_downhill = 1.0;

if isfield(options, 'path_file'), frozen.path_file = options.path_file; end
if isfield(options, 'zones'), frozen.zones = options.zones; end

% 合并 X -> P
P = frozen;
if istable(X)
    var_names = X.Properties.VariableNames;
    for i = 1:length(var_names)
        vn = var_names{i};
        P.(vn) = X.(vn);
    end
elseif isstruct(X)
    fn = fieldnames(X);
    for i = 1:length(fn)
        P.(fn{i}) = X.(fn{i});
    end
else
    error('X 必须是 table 或 struct');
end

% cfg
cfg = struct();
cfg.tau = P.tau;
if isfield(P, 'path_file'), cfg.path_file = P.path_file; end
if isfield(P, 'zones'), cfg.zones = P.zones; end

Q0 = [P.q_y, P.q_psi, P.q_v, P.q_omega];
R0 = [10^(P.log10_r_F), 10^(P.log10_r_omega)];
dR0= [10^(P.log10_rdF), 10^(P.log10_rdw)];

alpha_Q_val = min(P.alpha_Q, P.beta_Q);
beta_Q_val  = max(P.alpha_Q, P.beta_Q);
alpha_R_val = min(P.alpha_R, P.beta_R);
beta_R_val  = max(P.alpha_R, P.beta_R);
alpha_dR_val= min(P.alpha_dR, P.beta_dR);
beta_dR_val = max(P.alpha_dR, P.beta_dR);

alpha_Q = repmat(alpha_Q_val, 1, 4);
beta_Q  = repmat(beta_Q_val, 1, 4);
alpha_R = repmat(alpha_R_val, 1, 2);
beta_R  = repmat(beta_R_val, 1, 2);
alpha_dR= repmat(alpha_dR_val, 1, 2);
beta_dR = repmat(beta_dR_val, 1, 2);

scale_umin_lo = [P.scale_umin_lo, P.scale_umin_lo];
scale_umin_hi = [P.scale_umin_hi, P.scale_umin_hi];
scale_umax_lo = [P.scale_umax_lo, P.scale_umax_lo];
scale_umax_hi = [P.scale_umax_hi, P.scale_umax_hi];

% db fallback
if isempty(db)
    grid.V_grid = linspace(0.1, 1.2, 7)';
    grid.W_grid = linspace(-1.2, 1.2, 7)';
    grid.T_grid = linspace(-0.2, 0.2, 7)';
    lin_opts = struct('coord','path','disc','zoh','keep_E',true, ...
        'export_mat', fullfile(data_models_dir, 'plant_grid_test.mat'));
    db = lin_agv_grid(params, grid, lin_opts);
end

% 构造控制器（与 objective_wrapper 同步）
base_opts = struct(...
    'Q',[10,15,2,1], ...
    'R',[1e-3,1e-3], ...
    'dR',[1e-2,1e-2], ...
    'umin',[-600; -1.2], ...
    'umax',[600; 1.2], ...
    'dumin',[-400; -0.9], ...
    'dumax',[400; 0.9]);
base_ctrl = mpc_setup_single_interp(db, base_opts);

ctrl = struct();
ctrl.db = base_ctrl.db;
ctrl.opts = base_ctrl.opts;
ctrl.maps = base_ctrl.maps;
ctrl.meta = base_ctrl.meta;

plant_base = base_ctrl.mpcobj.Model.Plant;
Ts = base_ctrl.mpcobj.Ts;
Np = base_ctrl.mpcobj.PredictionHorizon;
Nc = base_ctrl.mpcobj.ControlHorizon;
ctrl.mpcobj = mpc(plant_base, Ts, Np, Nc);

ctrl.mpcobj.Weights.OutputVariables = base_ctrl.opts.Q;
ctrl.mpcobj.Weights.ManipulatedVariables = base_ctrl.opts.R;
ctrl.mpcobj.Weights.ManipulatedVariablesRate = base_ctrl.opts.dR;

for i = 1:2
    ctrl.mpcobj.MV(i).Min = base_ctrl.mpcobj.MV(i).Min;
    ctrl.mpcobj.MV(i).Max = base_ctrl.mpcobj.MV(i).Max;
    ctrl.mpcobj.MV(i).RateMin = base_ctrl.mpcobj.MV(i).RateMin;
    ctrl.mpcobj.MV(i).RateMax = base_ctrl.mpcobj.MV(i).RateMax;
end
for i = 1:4
    ctrl.mpcobj.OV(i).Min = base_ctrl.mpcobj.OV(i).Min;
    ctrl.mpcobj.OV(i).Max = base_ctrl.mpcobj.OV(i).Max;
    if isfinite(base_ctrl.mpcobj.OV(i).MinECR)
        ctrl.mpcobj.OV(i).MinECR = base_ctrl.mpcobj.OV(i).MinECR;
    end
    if isfinite(base_ctrl.mpcobj.OV(i).MaxECR)
        ctrl.mpcobj.OV(i).MaxECR = base_ctrl.mpcobj.OV(i).MaxECR;
    end
end

ctrl.maps.Q_range = [Q0*0.5; Q0*1.5];
ctrl.maps.R_range = [R0*0.5; R0*1.5];
ctrl.maps.dR_range= [dR0*0.5; dR0*1.5];
ctrl.maps.alpha_Q = alpha_Q; ctrl.maps.beta_Q = beta_Q;
ctrl.maps.alpha_R = alpha_R; ctrl.maps.beta_R = beta_R;
ctrl.maps.alpha_dR= alpha_dR; ctrl.maps.beta_dR = beta_dR;
ctrl.maps.scale_umin_lo = scale_umin_lo; ctrl.maps.scale_umin_hi = scale_umin_hi;
ctrl.maps.scale_umax_lo = scale_umax_lo; ctrl.maps.scale_umax_hi = scale_umax_hi;
ctrl.maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
ctrl.maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];
ctrl.maps.tau = P.tau;
ctrl.maps.omega_threshold          = P.omega_threshold;
ctrl.maps.transition_width        = P.transition_width;
ctrl.maps.q_y_gain_max           = P.q_y_gain_max;
ctrl.maps.theta_threshold        = P.theta_threshold;
ctrl.maps.theta_transition_width = P.theta_transition_width;
ctrl.maps.q_v_gain_max           = P.q_v_gain_max;
ctrl.maps.R_F_gain_max_uphill    = P.R_F_gain_max_uphill;
ctrl.maps.R_F_gain_max_downhill  = P.R_F_gain_max_downhill;
ctrl.maps.dR_F_gain_max_uphill   = P.dR_F_gain_max_uphill;
ctrl.maps.dR_F_gain_max_downhill = P.dR_F_gain_max_downhill;

cfg.ctrl = ctrl;
cfg.ctrl_maps = ctrl.maps;

if isfield(options,'scenes')
    scenes = options.scenes;
else
    scenes = struct('startup',0.05,'golden_test',0.20,'pure_turn',0.25,'pure_slope',0.20,'composite',0.25,'closure',0.05);
end

[J, report] = Cost_Function(params, db, cfg, scenes);
end
