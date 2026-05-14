function out = ModernTCN_online_step(y_raw, reset, seed, request_predict)
%MODERNTCN_ONLINE_STEP 从单帧 y_raw 在线更新 ModernTCN 状态并按需推理。
%
% 功能说明：
%   该函数是 ModernTCN 接入 Simulink 前的核心在线封装。它的输入不是
%   已经归一化的 [128,19] 窗口，而是仿真模型每个采样周期输出的一帧
%   y_raw。函数内部会：
%     1. 从 y_raw 提取与当前推荐 ModernTCN 数据集一致的 19 维特征；
%     2. 使用数据集内保存的 TCN scaler 做归一化；
%     3. 维护 128 步滑动窗口；
%     4. 调用当前推荐 ModernTCN ONNX predictor，输出分类、置信度和 theta_hat。
%
% 输入：
%   y_raw           : 当前时刻 AGV 输出，至少 18 维；闭环模型中实际为 [34,1]。
%   reset           : 非 0 时重置在线状态。
%   seed            : 可选，默认 21。
%   request_predict : 可选。
%                     []  = 按 cfg.infer_period_steps 自动决定是否推理；
%                     true  = 本步强制推理；
%                     false = 本步只更新滑窗，不调用 ONNX。
%
% 输出：
%   out : 结构体，字段包括 label_main、label_turn、theta_hat_rad、conf_main、
%         buffer_count、ready、did_predict 等。函数也会把最近一次输出写入
%         base workspace 的 modern_tcn_online_last_out，便于 Simulink 薄封装读取。

if nargin < 1
    y_raw = [];
end
if nargin < 2 || isempty(reset)
    reset = 0;
end
if nargin < 3 || isempty(seed)
    default_cfg = ModernTCN_default_config(local_project_root());
    seed = default_cfg.seed;
end
if nargin < 4
    request_predict = [];
end

persistent state

if reset ~= 0 || isempty(state) || ~isfield(state, 'seed') || state.seed ~= seed
    state = local_init_state(seed);
end

out = local_default_output(state);

if isempty(y_raw)
    local_publish_output(out);
    return;
end
if numel(y_raw) < 18
    out.debug.warning = "y_raw 维度不足，至少需要前 18 维。";
    local_publish_output(out);
    return;
end

[feature_raw, state] = local_extract_feature(double(y_raw(:)), state);
feature_norm = (feature_raw - state.scaler_mean) ./ (state.scaler_std + state.eps);

% 滚动维护 [128,19] 归一化窗口。模型训练时使用的就是这个归一化窗口。
state.buffer(1:end-1, :) = state.buffer(2:end, :);
state.buffer(end, :) = single(feature_norm);
state.buffer_count = min(state.buffer_count + 1, state.seq_len);
state.step = state.step + 1;

out = local_default_output(state);
out.feature_raw = feature_raw;
out.feature_norm = feature_norm;

if state.buffer_count < state.seq_len
    out.debug.warning = "窗口未满，保持默认输出。";
    state.last_out = out;
    local_publish_output(out);
    return;
end

do_predict = local_should_predict(state, request_predict);
if do_predict
    pred = ModernTCN_predict_window(state.predictor, state.buffer);
    out = local_output_from_prediction(state, pred);
    out.feature_raw = feature_raw;
    out.feature_norm = feature_norm;
    out.did_predict = true;
    state.last_out = out;
else
    out = state.last_out;
    out.step = state.step;
    out.buffer_count = state.buffer_count;
    out.ready = true;
    out.did_predict = false;
end

local_publish_output(out);
end

function state = local_init_state(seed)
% 初始化在线状态。注意：这里读取的是 TCN/ModernTCN 数据集 scaler，不是 GRU scaler。
root = local_project_root();
default_cfg = ModernTCN_default_config(root);
dataset_file = default_cfg.dataset_file;
if exist(dataset_file, 'file') ~= 2
    error('ModernTCN:MissingDataset', '找不到数据集: %s', dataset_file);
end

S = load(dataset_file, 'dataset');
dataset = S.dataset;
cfg = local_read_sim_cfg(seed);

params = parameters();
state = struct();
state.seed = seed;
state.params = params;
state.Ts = dataset.meta.Ts;
state.seq_len = dataset.meta.seq_len;
state.feat_dim = numel(dataset.scaler.mean);
state.buffer = zeros(state.seq_len, state.feat_dim, 'single');
state.buffer_count = 0;
state.step = 0;
state.eps = 1e-8;

state.scaler_mean = double(dataset.scaler.mean(:).');
state.scaler_std = double(dataset.scaler.std(:).');
state.tau_accel_lp = dataset.scaler.tau_accel_lp;
state.tau_diff = dataset.scaler.tau_diff;
state.tau_pitch = dataset.scaler.tau_pitch;
state.alpha_diff = state.Ts / (state.tau_diff + state.Ts);
state.alpha_accel = state.Ts / (state.tau_accel_lp + state.Ts);
state.lambda_pitch = exp(-state.Ts / state.tau_pitch);

state.has_feature_prev = false;
state.v_hat_prev = 0.0;
state.dv_hat_dt_prev = 0.0;
state.accel_x_lp_prev = 0.0;
state.pitch_angle_est_prev = 0.0;

state.infer_period_steps = cfg.infer_period_steps;
state.predictor = ModernTCN_load_predictor(seed);
state.last_out = local_default_output(state);
end

function cfg = local_read_sim_cfg(seed)
% 允许用户在 base workspace 里用 modern_tcn_sim_cfg 覆写仿真配置。
cfg = struct();
cfg.seed = seed;
cfg.infer_period_steps = 5;  % 默认每 0.05s 推理一次，降低闭环仿真开销。
try
    if evalin('base', 'exist(''modern_tcn_sim_cfg'', ''var'') == 1')
        user_cfg = evalin('base', 'modern_tcn_sim_cfg');
        if isstruct(user_cfg)
            if isfield(user_cfg, 'infer_period_steps') && ~isempty(user_cfg.infer_period_steps)
                cfg.infer_period_steps = max(1, round(double(user_cfg.infer_period_steps)));
            end
        end
    end
catch
    % base workspace 不可用时保留默认配置。
end
end

function [feature_raw, state] = local_extract_feature(y_raw, state)
% 复刻 TCN_prepare_dataset 中的 GRU_compatible_observable_19 特征契约。
p = state.params;
r = p.wheel_radius;
W = p.W;

accel_x = y_raw(9);
gyro_y = y_raw(10);
gyro_z = y_raw(11);
I_lf = y_raw(12);
I_rr = y_raw(13);
omega_wheel_lf = y_raw(17);
omega_wheel_rr = y_raw(18);
delta_lf = y_raw(6);
delta_rr = y_raw(7);

v_hat = r * (omega_wheel_lf + omega_wheel_rr) / 2;
if ~state.has_feature_prev
    % 离线数据预处理在每个 run 的第一个有效样本处使用 dv_raw=0、
    % accel_x_lp=accel_x、pitch_angle_est=0。这里保持相同初值，避免
    % 在线窗口与训练窗口出现开头偏移。
    dv_hat_dt = 0.0;
    accel_x_lp = accel_x;
    pitch_angle_est = 0.0;
    state.has_feature_prev = true;
else
    dv_raw = (v_hat - state.v_hat_prev) / state.Ts;
    dv_hat_dt = state.alpha_diff * dv_raw + (1 - state.alpha_diff) * state.dv_hat_dt_prev;
    accel_x_lp = state.alpha_accel * accel_x + (1 - state.alpha_accel) * state.accel_x_lp_prev;
    pitch_angle_est = state.lambda_pitch * state.pitch_angle_est_prev + gyro_y * state.Ts;
end

ws_imbalance = abs(omega_wheel_lf - omega_wheel_rr);
I_sum = abs(I_lf) + abs(I_rr);
I_diff_signed = I_lf - I_rr;
I_diff_abs = abs(I_lf) - abs(I_rr);
kappa_proxy = (tan(delta_lf) - tan(delta_rr)) / W;
accel_per_current = accel_x_lp / max(I_sum, 0.1);

state.v_hat_prev = v_hat;
state.dv_hat_dt_prev = dv_hat_dt;
state.accel_x_lp_prev = accel_x_lp;
state.pitch_angle_est_prev = pitch_angle_est;

feature_raw = [accel_x, gyro_z, I_lf, I_rr, omega_wheel_lf, omega_wheel_rr, ...
    delta_lf, delta_rr, gyro_y, v_hat, dv_hat_dt, ws_imbalance, ...
    I_sum, I_diff_signed, I_diff_abs, accel_x_lp, kappa_proxy, ...
    accel_per_current, pitch_angle_est];
end

function tf = local_should_predict(state, request_predict)
if isempty(request_predict)
    tf = mod(state.step - state.seq_len, state.infer_period_steps) == 0;
else
    tf = logical(request_predict);
end
end

function out = local_output_from_prediction(state, pred)
out = struct();
out.seed = state.seed;
out.step = state.step;
out.buffer_count = state.buffer_count;
out.ready = state.buffer_count >= state.seq_len;
out.did_predict = false;
out.label_main = double(pred.main_state);
out.label_turn = double(pred.turn_state);
out.theta_hat_rad = double(pred.theta_hat_rad);
out.theta_hat_deg = double(pred.theta_hat_deg);
out.conf_main = double(pred.main_confidence);
out.conf_turn = double(pred.turn_confidence);
out.main_prob = double(pred.main_prob(:));
out.turn_prob = double(pred.turn_prob(:));
out.logits_main = single(pred.logits_main(:).');
out.logits_turn = single(pred.logits_turn(:).');
out.X_window_norm = state.buffer;
out.debug = struct();
out.debug.infer_period_steps = state.infer_period_steps;
out.debug.note = "ModernTCN raw output; theta_hat 建议先只记录，不直接接入 RhoFilter。";
end

function out = local_default_output(state)
out = struct();
out.seed = state.seed;
out.step = state.step;
out.buffer_count = state.buffer_count;
out.ready = false;
out.did_predict = false;
out.label_main = 1.0;
out.label_turn = 0.0;
out.theta_hat_rad = 0.0;
out.theta_hat_deg = 0.0;
out.conf_main = 1.0;
out.conf_turn = 1.0;
out.main_prob = [1; 0; 0];
out.turn_prob = [0; 1; 0];
out.logits_main = single([0 0 0]);
out.logits_turn = single([0 0 0]);
out.X_window_norm = state.buffer;
out.feature_raw = zeros(1, state.feat_dim);
out.feature_norm = zeros(1, state.feat_dim);
out.debug = struct();
out.debug.infer_period_steps = state.infer_period_steps;
end

function local_publish_output(out)
% Simulink 薄封装通过 base workspace 读取标量，普通 MATLAB 调试也可查看。
try
    assignin('base', 'modern_tcn_online_last_out', out);
catch
end
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    root = pwd;
end
end
