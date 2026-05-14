function [state, out] = ModernTCN_state_classifier(action, varargin)
%MODERNTCN_STATE_CLASSIFIER ModernTCN 在线工况识别状态机。
%
% 功能说明：
%   本函数从每个仿真步的 34 维 y_raw 中提取与 ModernTCN_dataset_v4_industrial
%   完全一致的 19 维可观测特征，使用该数据集内保存的 scaler 做归一化，
%   维护 128 步滑动窗口，然后调用当前推荐 ModernTCN ONNX predictor 推理。
%
% 设计边界：
%   1. 本函数只用于 MATLAB/Simulink 仿真，不用于代码生成部署。
%   2. 输入是原始 y_raw 单帧，不是已经归一化的 [128,19] 窗口。
%   3. theta_hat 先作为诊断输出；第一阶段不建议直接接入 RhoFilter。
%
% 用法：
%   params = parameters();
%   state = ModernTCN_state_classifier('init', params);
%   [state, out] = ModernTCN_state_classifier('update', state, y_raw_t);

switch lower(action)
    case 'init'
        if nargin < 2
            error('ModernTCN:init', '初始化需要提供 params。');
        end
        cfg = struct();
        if nargin >= 3 && isstruct(varargin{2})
            cfg = varargin{2};
        end
        state = local_init(varargin{1}, cfg);
        out = [];

    case 'update'
        if nargin < 3
            error('ModernTCN:update', '更新需要提供 state 和 y_raw_t。');
        end
        [state, out] = local_update(varargin{1}, varargin{2});

    otherwise
        error('ModernTCN:BadAction', '未知操作: %s，应为 init 或 update。', action);
end
end

function state = local_init(params, cfg)
root = local_project_root();
default_cfg = ModernTCN_default_config(root);

if ~isfield(cfg, 'seed') || isempty(cfg.seed)
    cfg.seed = default_cfg.seed;
end
if ~isfield(cfg, 'dataset_file') || isempty(cfg.dataset_file)
    cfg.dataset_file = default_cfg.dataset_file;
end
if (~isfield(cfg, 'run_tag') || isempty(cfg.run_tag)) && (~isfield(cfg, 'onnx_file') || isempty(cfg.onnx_file))
    cfg.run_tag = default_cfg.run_tag;
end
if ~isfield(cfg, 'theta_output_gain') || isempty(cfg.theta_output_gain)
    cfg.theta_output_gain = local_field_or_default(default_cfg, 'theta_output_gain', 1.0);
end
if ~isfield(cfg, 'theta_abs_limit') || isempty(cfg.theta_abs_limit)
    cfg.theta_abs_limit = local_field_or_default(default_cfg, 'theta_abs_limit', inf);
end
if ~isfield(cfg, 'theta_rate_limit') || isempty(cfg.theta_rate_limit)
    cfg.theta_rate_limit = local_field_or_default(default_cfg, 'theta_rate_limit', inf);
end
if ~isfield(cfg, 'theta_mpc_deadzone') || isempty(cfg.theta_mpc_deadzone)
    cfg.theta_mpc_deadzone = local_field_or_default(default_cfg, 'theta_mpc_deadzone', deg2rad(2.0));
end
onnx_file = '';
if isfield(cfg, 'onnx_file') && ~isempty(cfg.onnx_file)
    onnx_file = char(cfg.onnx_file);
elseif isfield(cfg, 'run_tag') && ~isempty(cfg.run_tag)
    onnx_file = fullfile(root, 'results', 'modern_tcn', char(cfg.run_tag), ...
        sprintf('modern_tcn_seed%d.onnx', cfg.seed));
end

if exist(cfg.dataset_file, 'file') ~= 2
    error('ModernTCN:MissingDataset', '找不到 ModernTCN 数据集: %s', cfg.dataset_file);
end

S = load(cfg.dataset_file, 'dataset');
dataset = S.dataset;
scaler = dataset.scaler;

state = struct();
state.params = params;
state.Ts = local_field_or_default(params, 'Ts', 0.01);
state.seed = cfg.seed;
state.dataset_file = cfg.dataset_file;
state.onnx_file = onnx_file;
state.scaler = scaler;
state.feat_names = dataset.feat_names;
state.seq_len = local_field_or_default(dataset.meta, 'seq_len', 128);
state.feat_dim = numel(scaler.mean);
state.buffer = zeros(state.seq_len, state.feat_dim, 'single');
state.buffer_count = 0;

% 与 TCN_prepare_dataset.m 保持一致：训练数据跳过起始 1s 后再建窗。
state.skip_initial_sec = local_field_or_default(dataset.meta, 'skip_initial_sec', 1.0);
state.skip_initial_steps = round(state.skip_initial_sec / state.Ts);
state.step = 0;

% 特征提取参数。字段来自 TCN scaler，缺省值与 TCN_prepare_dataset.m 一致。
state.tau_accel_lp = local_field_or_default(scaler, 'tau_accel_lp', 0.4);
state.tau_diff = local_field_or_default(scaler, 'tau_diff', 0.3);
state.tau_pitch = local_field_or_default(scaler, 'tau_pitch', 2.0);
state.alpha_accel = state.Ts / (state.tau_accel_lp + state.Ts);
state.alpha_diff = state.Ts / (state.tau_diff + state.Ts);
state.lambda_pitch = exp(-state.Ts / state.tau_pitch);

% 特征递推状态。首个有效样本按离线 local_lowpass/local_leaky_integral 的
% 初值约定初始化，避免在线/离线开头一段不一致。
state.feature_started = false;
state.v_hat_prev = 0.0;
state.dv_hat_dt_prev = 0.0;
state.accel_x_lp_prev = 0.0;
state.pitch_angle_est_prev = 0.0;

% 标签驻留时间。ModernTCN 的 offline 指标较稳，但 Simulink 中单步更新仍需
% 抑制边界跳变，先沿用 GRU 侧成熟参数。
state.dwell_main = 0.20;
state.dwell_turn = 0.40;
state.dwell_main_steps = max(1, round(state.dwell_main / state.Ts));
state.dwell_turn_steps = max(1, round(state.dwell_turn / state.Ts));
state.label_main_current = 1;
state.label_turn_current = 0;
state.label_main_candidate = 1;
state.label_turn_candidate = 0;
state.label_main_stable_count = 0;
state.label_turn_stable_count = 0;
state.conf_main_current = 1.0;
state.conf_turn_current = 1.0;

% theta raw/conditioned output remains a model estimate. MPC scheduling can
% use theta_hat_for_mpc, which applies the deployment deadzone outside the
% learned regressor.
state.tau_theta = 0.15;
state.alpha_theta = state.Ts / (state.tau_theta + state.Ts);
state.theta_hat_current = 0.0;
state.theta_mpc_deadzone = double(cfg.theta_mpc_deadzone);
state.theta_output_gain = double(cfg.theta_output_gain);
state.theta_abs_limit = double(cfg.theta_abs_limit);
state.theta_rate_limit = double(cfg.theta_rate_limit);
state.theta_hat_output_prev = 0.0;

% 19 维特征对应的 y_raw 索引，与 TCN_prepare_dataset.m 的 local_extract_runs 一致。
state.feat_indices = struct();
state.feat_indices.accel_x = 9;
state.feat_indices.gyro_y = 10;
state.feat_indices.gyro_z = 11;
state.feat_indices.I_lf = 12;
state.feat_indices.I_rr = 13;
state.feat_indices.omega_wheel_lf = 17;
state.feat_indices.omega_wheel_rr = 18;
state.feat_indices.delta_lf = 6;
state.feat_indices.delta_rr = 7;
state.eps = 1e-8;

% ONNX predictor 只在初始化时加载一次，避免每个仿真步重复导入网络。
if isempty(state.onnx_file)
    state.predictor = ModernTCN_load_predictor(state.seed);
else
    state.predictor = ModernTCN_load_predictor(state.seed, state.onnx_file);
end
state.is_ready = true;
end

function [state, out] = local_update(state, y_raw_t)
state.step = state.step + 1;

if isempty(y_raw_t) || numel(y_raw_t) < 18
    out = local_default_output(state, 'y_raw 维度不足');
    return;
end

% 与训练预处理保持一致：跳过起始 transient，跳过期间不更新特征滤波状态。
if state.step <= state.skip_initial_steps
    out = local_default_output(state, 'skip_initial_sec 内输出默认值');
    return;
end

[features, state] = local_extract_features(double(y_raw_t(:)), state);
if any(~isfinite(features))
    out = local_default_output(state, '特征含 NaN/Inf');
    return;
end

state.buffer(1:end-1, :) = state.buffer(2:end, :);
state.buffer(end, :) = single(features);
state.buffer_count = min(state.buffer_count + 1, state.seq_len);

if state.buffer_count < state.seq_len
    out = local_default_output(state, '滑动窗口未填满');
    out.features = double(features(:));
    out.features_norm = double(((features(:).' - double(state.scaler.mean)) ./ ...
        (double(state.scaler.std) + state.eps)).');
    return;
end

X_norm = (double(state.buffer) - double(state.scaler.mean)) ./ ...
    (double(state.scaler.std) + state.eps);

try
    pred = ModernTCN_predict_window(state.predictor, single(X_norm));
catch ME
    warning('ModernTCN:InferenceFailed', 'ModernTCN 推理失败: %s', ME.message);
    out = local_default_output(state, 'ModernTCN 推理失败');
    return;
end

label_main_raw = double(pred.main_state);
label_turn_raw = double(pred.turn_state);
conf_main_raw = double(pred.main_confidence);
conf_turn_raw = double(pred.turn_confidence);
theta_hat_raw = double(pred.theta_hat_rad);

[state.label_main_current, state.label_main_candidate, state.label_main_stable_count] = ...
    local_apply_dwell(label_main_raw, state.label_main_current, ...
    state.label_main_candidate, state.label_main_stable_count, state.dwell_main_steps);

[state.label_turn_current, state.label_turn_candidate, state.label_turn_stable_count] = ...
    local_apply_dwell(label_turn_raw, state.label_turn_current, ...
    state.label_turn_candidate, state.label_turn_stable_count, state.dwell_turn_steps);

state.conf_main_current = conf_main_raw;
state.conf_turn_current = conf_turn_raw;
state.theta_hat_current = state.alpha_theta * theta_hat_raw + ...
    (1 - state.alpha_theta) * state.theta_hat_current;

theta_hat_out = local_apply_theta_conditioning(state.theta_hat_current, state);
theta_hat_for_mpc = local_apply_theta_mpc_deadzone(theta_hat_out, state);
state.theta_hat_output_prev = theta_hat_out;

out = struct();
out.label_main = state.label_main_current;
out.label_turn = state.label_turn_current;
out.theta_hat = theta_hat_out;
out.theta_hat_for_mpc = theta_hat_for_mpc;
out.conf_main = state.conf_main_current;
out.conf_turn = state.conf_turn_current;
out.label_main_raw = label_main_raw;
out.label_turn_raw = label_turn_raw;
out.theta_hat_raw = theta_hat_raw;
out.main_prob = double(pred.main_prob(:));
out.turn_prob = double(pred.turn_prob(:));
out.features = double(features(:));
out.features_norm = double(X_norm(end, :).');
out.debug = struct();
out.debug.step = state.step;
out.debug.buffer_count = state.buffer_count;
out.debug.ready = true;
out.debug.did_predict = true;
out.debug.skip_initial_steps = state.skip_initial_steps;
out.debug.feature_contract = 'GRU_compatible_observable_19';
out.debug.theta_output_gain = state.theta_output_gain;
out.debug.theta_abs_limit = state.theta_abs_limit;
out.debug.theta_rate_limit = state.theta_rate_limit;
out.debug.theta_mpc_deadzone = state.theta_mpc_deadzone;
out.debug.note = 'ModernTCN online output';
end

function [features, state] = local_extract_features(y_raw, state)
params = state.params;
Ts = state.Ts;
r = local_field_or_default(params, 'wheel_radius', 0.1);
W = local_field_or_default(params, 'W', 1.0);

accel_x = y_raw(state.feat_indices.accel_x);
gyro_y = y_raw(state.feat_indices.gyro_y);
gyro_z = y_raw(state.feat_indices.gyro_z);
I_lf = y_raw(state.feat_indices.I_lf);
I_rr = y_raw(state.feat_indices.I_rr);
omega_wheel_lf = y_raw(state.feat_indices.omega_wheel_lf);
omega_wheel_rr = y_raw(state.feat_indices.omega_wheel_rr);
delta_lf = y_raw(state.feat_indices.delta_lf);
delta_rr = y_raw(state.feat_indices.delta_rr);

v_hat = r * (omega_wheel_lf + omega_wheel_rr) / 2;
if ~state.feature_started
    dv_raw = 0.0;
    dv_hat_dt = 0.0;
    accel_x_lp = accel_x;
    pitch_angle_est = 0.0;
    state.feature_started = true;
else
    dv_raw = (v_hat - state.v_hat_prev) / Ts;
    dv_hat_dt = state.alpha_diff * dv_raw + ...
        (1 - state.alpha_diff) * state.dv_hat_dt_prev;
    accel_x_lp = state.alpha_accel * accel_x + ...
        (1 - state.alpha_accel) * state.accel_x_lp_prev;
    pitch_angle_est = state.lambda_pitch * state.pitch_angle_est_prev + gyro_y * Ts;
end

state.v_hat_prev = v_hat;
state.dv_hat_dt_prev = dv_hat_dt;
state.accel_x_lp_prev = accel_x_lp;
state.pitch_angle_est_prev = pitch_angle_est;

ws_imbalance = abs(omega_wheel_lf - omega_wheel_rr);
I_sum = abs(I_lf) + abs(I_rr);
I_diff_signed = I_lf - I_rr;
I_diff_abs = abs(I_lf) - abs(I_rr);
kappa_proxy = (tan(delta_lf) - tan(delta_rr)) / W;
accel_per_current = accel_x_lp / max(I_sum, 0.1);

features = [accel_x, gyro_z, I_lf, I_rr, omega_wheel_lf, omega_wheel_rr, ...
    delta_lf, delta_rr, gyro_y, v_hat, dv_hat_dt, ws_imbalance, ...
    I_sum, I_diff_signed, I_diff_abs, accel_x_lp, kappa_proxy, ...
    accel_per_current, pitch_angle_est];
end

function [current, candidate, count] = local_apply_dwell(raw_label, current, candidate, count, required_count)
if raw_label == candidate
    count = count + 1;
    if count >= required_count
        current = raw_label;
    end
else
    candidate = raw_label;
    count = 1;
end
end

function theta_hat = local_apply_theta_conditioning(theta_hat, state)
theta_hat = state.theta_output_gain * theta_hat;

if isfinite(state.theta_abs_limit) && state.theta_abs_limit > 0
    theta_hat = min(max(theta_hat, -state.theta_abs_limit), state.theta_abs_limit);
end

if isfinite(state.theta_rate_limit) && state.theta_rate_limit > 0
    max_step = state.theta_rate_limit * state.Ts;
    theta_delta = theta_hat - state.theta_hat_output_prev;
    theta_delta = min(max(theta_delta, -max_step), max_step);
    theta_hat = state.theta_hat_output_prev + theta_delta;
end
end

function theta_hat = local_apply_theta_mpc_deadzone(theta_hat, state)
theta_abs = abs(theta_hat);
if theta_abs <= state.theta_mpc_deadzone
    theta_hat = 0.0;
end
end

function out = local_default_output(state, note)
out = struct();
out.label_main = state.label_main_current;
out.label_turn = state.label_turn_current;
out.theta_hat = state.theta_hat_current;
out.theta_hat_for_mpc = local_apply_theta_mpc_deadzone(state.theta_hat_current, state);
out.conf_main = state.conf_main_current;
out.conf_turn = state.conf_turn_current;
out.label_main_raw = state.label_main_current;
out.label_turn_raw = state.label_turn_current;
out.theta_hat_raw = state.theta_hat_current;
out.main_prob = [1; 0; 0];
out.turn_prob = [0; 1; 0];
out.features = nan(19, 1);
out.features_norm = nan(19, 1);
out.debug = struct();
out.debug.step = state.step;
out.debug.buffer_count = state.buffer_count;
out.debug.ready = state.buffer_count >= state.seq_len;
out.debug.did_predict = false;
out.debug.skip_initial_steps = state.skip_initial_steps;
out.debug.note = note;
end

function v = local_field_or_default(s, field_name, default_value)
if isstruct(s) && isfield(s, field_name) && ~isempty(s.(field_name))
    v = s.(field_name);
else
    v = default_value;
end
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
