% ============================================================
% 文件名：Mamba_gen_train_data.m
% 版本：V1.1
% 日期：2026-03-25
% 功能：
%   基于 GRU_DataGen.slx 生成 Mamba 训练数据集，输出“传感器输入通道 +
%   回归目标 + 多头分类标签 + 元信息”。
%
% 主要升级（相对 V1.0）：
%   1) 新增回归目标：整车坡度角 y_theta_ground、整车等效转向角 y_delta_vehicle
%   2) 增强路径动态随机化：转弯半径/平滑过渡/坡度幅值按 run 级随机
%   3) 补充中文函数头：说明依赖文件、调用关系与关键参数设置
%
% 依赖文件：
%   - project_root.m
%   - parameters.m
%   - simulink/GRU_DataGen.slx
%   - src/paths/gen_agv_ref_path_v1.m
%   - src/core/agv_model_sfunc_train_data.m
%
% 关键参数约定：
%   - 原始输出 y_raw 默认 34 维（由训练 S-Function 保证）
%   - 整车等效转向角定义：delta_vehicle = atan(L_eq * omega_z / max(v, v_eps))
% ============================================================

%% -------------------- User Config --------------------
root = project_root();
out_dir = fullfile(root, 'data', 'mamba');
if ~exist(out_dir, 'dir')
    mkdir(out_dir);
end

cfg = struct();
cfg.scenes = {'industrial_lite'};

cfg.num_runs = 240;
cfg.num_runs_per_scene = struct( ...
    'industrial_lite', 240 ...
);

cfg.T_end = 150;
cfg.Ts = 0.01;
cfg.seed = 42;
cfg.model_name = 'GRU_DataGen';
cfg.expected_y_dim = 34;
cfg.verbose = true;

cfg.output_file = fullfile(out_dir, 'Mamba_train_data_full.mat');

cfg.noise_on = true;
cfg.noise_profile = struct();
cfg.noise_profile.mode = 'mixed';       % 'match' or 'mixed'
cfg.noise_profile.clean_ratio = 0.30;
cfg.noise_profile.noisy_scales = [1.0, 1.5];
cfg.noise_profile.noisy_probs = [0.7, 0.3];

cfg.path_rand = struct();
cfg.path_rand.v_cruise_range = [0.9, 1.1];
cfg.path_rand.slope_angle_pure_grid_deg = 0.0:0.1:10.0;
cfg.path_rand.slope_angle_composite_ratio = [0.55, 0.85];
cfg.path_rand.turn_scale_pure_fixed = 1.0;
cfg.path_rand.turn_scale_composite_fixed = 1.9;  % 1.9 使复合区右转 ω≈0.07-0.13 rad/s，稳定超过标签阈值 0.05 rad/s；2.5 过激导致其他指标退步
cfg.path_rand.transition_time_range = [1.2, 2.2];
cfg.path_rand.omega_limit_range = [0.14, 0.30];  % 上限从 0.20→0.30，避免放大后的右转 ω 被截断
cfg.path_rand.v_turn_ref_range = [0.08, 0.14];
cfg.path_rand.v_slope_ref_range_deg = [5, 9];

% 回归目标参数：整车等效转向角 delta_vehicle
cfg.target = struct();
cfg.target.v_eps = 0.20;              % [m/s] 低速保护，避免除零放大
cfg.target.delta_smooth_steps = 3;    % 轻度平滑窗口（奇数）

% 事件注入配置：
% 1) 每个回合在黄金测试区(10-50s)注入且仅注入一个主事件
% 2) 额外保留 20%-30% 的异常样本落在 pure_turn/pure_slope/composite 区
cfg.event_cfg = struct();
cfg.event_cfg.golden_zone = [10, 50];
cfg.event_cfg.primary_types = {'slip', 'load_change', 'stall'};
cfg.event_cfg.primary_probs = [0.34, 0.33, 0.33];

cfg.event_cfg.slip = struct( ...
    'duration_range', [1.5, 3.0], ...
    'gamma_range', [0.35, 0.75] ...
);
cfg.event_cfg.load_change = struct( ...
    'duration_range', [2.0, 4.0], ...
    'load_range', [80, 170] ...
);
cfg.event_cfg.stall = struct( ...
    'duration_range', [2.0, 3.2], ...
    'load_range', [210, 320] ...
);

cfg.event_cfg.extra_zone = struct();
cfg.event_cfg.extra_zone.enable = true;
cfg.event_cfg.extra_zone.prob = 0.25;  % 保持在 20%-30% 区间
cfg.event_cfg.extra_zone.targets = {'pure_turn', 'pure_slope', 'composite'};
cfg.event_cfg.extra_zone.type_probs = [0.45, 0.25, 0.30];  % slip/load_change/stall

%% -------------------- Init --------------------
rng(cfg.seed);
params = parameters();

scenes = cfg.scenes;
N_scenes = numel(scenes);
scene_runs = zeros(1, N_scenes);
for i = 1:N_scenes
    scene_runs(i) = get_scene_runs(scenes{i}, cfg.num_runs, cfg.num_runs_per_scene);
end
N_total = sum(scene_runs);

data = struct();
data.runs = struct('scene', {}, 't', {}, 'u', {}, 'theta', {}, 'y_raw', {}, ...
                   'y_mamba', {}, 'label_main', {}, 'label_turn', {}, ...
                   'label_slip', {}, 'label_stall', {}, 'label_load_change', {}, ...
                   'y_theta_ground', {}, 'y_delta_vehicle', {}, ...
                   'meta', {});

event_stats = struct();
event_stats.primary = struct('slip', 0, 'load_change', 0, 'stall', 0);
event_stats.extra_added = 0;
event_stats.extra_zone = struct('pure_turn', 0, 'pure_slope', 0, 'composite', 0);
event_stats.total_valid_runs = 0;

if ~bdIsLoaded(cfg.model_name)
    if cfg.verbose
        fprintf('Loading model: %s\n', cfg.model_name);
    end
    load_system(cfg.model_name);
end

% 关键：即使模型已加载，也刷新一次 PreLoad 逻辑，避免沿用旧会话中的
% ctrl/mpc 参数（常见症状：Adaptive MPC 内部出现 6x1 与 4x1 维度冲突）。
prepare_runtime_workspace_local(cfg.model_name, cfg.verbose);

%% -------------------- Generate --------------------
run_idx = 0;
for s_idx = 1:N_scenes
    scene = scenes{s_idx};
    runs_this_scene = scene_runs(s_idx);

    if cfg.verbose
        fprintf('\n========================================\n');
        fprintf('Scene [%d/%d]: %s\n', s_idx, N_scenes, scene);
        fprintf('========================================\n');
    end

    for run = 1:runs_this_scene
        run_idx = run_idx + 1;

        if cfg.verbose
            fprintf('  Run [%d/%d] (Total %d/%d)... ', run, runs_this_scene, run_idx, N_total);
        end

        try
            [ref_path, inj_signal, inject_info, T_end_run] = generate_reference_path_local(scene, params, cfg, run_idx);

            [enable_noise_run, noise_std_scale, noise_variant] = resolve_noise_profile_local(cfg.noise_profile, cfg.noise_on);

            params_sim = params;
            params_sim.enable_noise = enable_noise_run;
            if enable_noise_run
                noise_std_scale = max(noise_std_scale, 0);
                params_sim.current_noise_std = params.current_noise_std * noise_std_scale;
                params_sim.wheel_speed_noise_std = params.wheel_speed_noise_std * noise_std_scale;
                params_sim.disturbance_noise_std = params.disturbance_noise_std * noise_std_scale;
            else
                noise_std_scale = 0;
            end

            set_param(cfg.model_name, 'StopTime', num2str(T_end_run));
            set_param(cfg.model_name, 'FixedStep', num2str(cfg.Ts));

            assignin('base', 'params', params_sim);
            assignin('base', 'ref_path', ref_path);
            assignin('base', 'inj_signal', inj_signal);

            warning('off', 'all');
            sim_out = sim(cfg.model_name, 'ReturnWorkspaceOutputs', 'on', ...
                'SimulationMode', 'normal', 'CaptureErrors', 'on');
            warning('on', 'all');

            [t, y_raw, u, theta] = extract_signals_from_sim(sim_out);
            N = length(t);

            if size(y_raw, 1) ~= N || size(y_raw, 2) ~= cfg.expected_y_dim
                error('y_raw dimension mismatch: expected [%d x %d], got [%d x %d]', ...
                    N, cfg.expected_y_dim, size(y_raw, 1), size(y_raw, 2));
            end
            if size(u, 1) ~= N || size(u, 2) ~= 2
                error('u dimension mismatch: expected [%d x 2], got [%d x %d]', N, size(u, 1), size(u, 2));
            end
            if size(theta, 1) ~= N
                error('theta length mismatch: expected %d rows, got %d', N, size(theta, 1));
            end

            [y_mamba, channel_names] = build_mamba_channels(y_raw);

            [label_main, label_turn, label_slip, label_stall, label_load_change, y_theta_ground, y_delta_vehicle] = ...
                generate_mamba_labels(t, y_raw, theta, ref_path.omega_ref, inject_info, cfg.Ts, params_sim, cfg.target);

            data.runs(run_idx).scene = scene;
            data.runs(run_idx).t = t;
            data.runs(run_idx).u = u;
            data.runs(run_idx).theta = theta;
            data.runs(run_idx).y_raw = y_raw;
            data.runs(run_idx).y_mamba = y_mamba;
            data.runs(run_idx).label_main = label_main;
            data.runs(run_idx).label_turn = label_turn;
            data.runs(run_idx).label_slip = label_slip;
            data.runs(run_idx).label_stall = label_stall;
            data.runs(run_idx).label_load_change = label_load_change;
            data.runs(run_idx).y_theta_ground = y_theta_ground;
            data.runs(run_idx).y_delta_vehicle = y_delta_vehicle;
            data.runs(run_idx).meta.inject_info = inject_info;
            data.runs(run_idx).meta.path_params = ref_path.meta;
            data.runs(run_idx).meta.noise = struct( ...
                'enable_noise', enable_noise_run, ...
                'std_scale', noise_std_scale, ...
                'variant', noise_variant ...
            );

            event_stats.total_valid_runs = event_stats.total_valid_runs + 1;
            ptype = inject_info.primary_event.type;
            if isfield(event_stats.primary, ptype)
                event_stats.primary.(ptype) = event_stats.primary.(ptype) + 1;
            end
            if isfield(inject_info, 'extra_zone_event_added') && inject_info.extra_zone_event_added
                event_stats.extra_added = event_stats.extra_added + 1;
                zname = inject_info.extra_zone_event.zone;
                if isfield(event_stats.extra_zone, zname)
                    event_stats.extra_zone.(zname) = event_stats.extra_zone.(zname) + 1;
                end
            end

            if cfg.verbose
                fprintf('ok (N=%d, flat=%d, stall=%d, slope=%d, slip=%d)\n', ...
                    N, sum(label_main == 1), sum(label_main == 2), sum(label_main == 3), sum(label_slip == 1));
            end

        catch ME
            if cfg.verbose
                fprintf('fail: %s\n', ME.message);
            end
            warning('Mamba_gen_train_data:SimFailed', ...
                'Scene %s run %d failed: %s', scene, run, ME.message);
            continue;
        end
    end
end

%% -------------------- Meta & Save --------------------
data.meta = struct();
data.meta.generation_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
data.meta.version = 'V1.1';
data.meta.author = 'LPV-MPC Project';
data.meta.model_name = cfg.model_name;
data.meta.scenes = scenes;
data.meta.num_runs_per_scene = scene_runs;
data.meta.T_end = cfg.T_end;
data.meta.Ts = cfg.Ts;
data.meta.seed = cfg.seed;
data.meta.expected_y_dim = cfg.expected_y_dim;
data.meta.mamba_channels = channel_names;
data.meta.mamba_channel_desc = [ ...
    "accel_x_meas, gyro_y_meas, gyro_z_meas, I_meas_lf, I_meas_rr, " + ...
    "omega_wheel_lf, omega_wheel_rr, slip_ratio_lf, slip_ratio_rr, accel_y_meas" ...
];
data.meta.label_map_main = struct('flat', 1, 'stall', 2, 'slope', 3);
data.meta.label_map_turn = struct('right', -1, 'straight', 0, 'left', 1);
data.meta.label_map_load_change = struct('normal', 0, 'load_change', 1);
data.meta.regression_targets = struct( ...
    'y_theta_ground', 'ground slope angle [rad]', ...
    'y_delta_vehicle', 'equivalent whole-vehicle steering angle [rad]' ...
);
data.meta.delta_vehicle_formula = 'atan(L_eq * omega_z / max(v, v_eps))';
data.meta.delta_vehicle_params = cfg.target;
data.meta.event_cfg = cfg.event_cfg;
if event_stats.total_valid_runs > 0
    data.meta.event_stats = event_stats;
    data.meta.event_stats.extra_ratio = event_stats.extra_added / event_stats.total_valid_runs;
else
    data.meta.event_stats = event_stats;
    data.meta.event_stats.extra_ratio = 0;
end
data.meta.notes = 'Designed for Mamba sensor-driven training with dynamic path randomization and regression targets.';

if cfg.verbose
    fprintf('\nSaving to: %s\n', cfg.output_file);
end
save(cfg.output_file, 'data', '-v7.3');

if cfg.verbose
    fprintf('Done. Valid runs: %d\n', numel(data.runs));
    if isfield(data.meta, 'event_stats')
        es = data.meta.event_stats;
        fprintf('Primary events: slip=%d, load_change=%d, stall=%d\n', ...
            es.primary.slip, es.primary.load_change, es.primary.stall);
        fprintf('Extra-zone events: %d/%d (ratio=%.3f), target=%.2f\n', ...
            es.extra_added, es.total_valid_runs, es.extra_ratio, cfg.event_cfg.extra_zone.prob);
        fprintf('Extra-zone distribution: pure_turn=%d, pure_slope=%d, composite=%d\n', ...
            es.extra_zone.pure_turn, es.extra_zone.pure_slope, es.extra_zone.composite);
    end
end

%% ==================== Local Helpers ====================
function [t, y_raw, u, theta] = extract_signals_from_sim(sim_out)
% =============================
% 函数名：extract_signals_from_sim
% 功能：从 Simulink.SimulationOutput 中提取 t/y_raw/u/theta 四组信号。
% 依赖：
%   - Simulink.SimulationOutput（sim 返回类型）
% 调用：
%   - 被主循环调用，用于统一信号提取与格式校验入口
% 参数设置：
%   - 要求 sim_out 中存在 tout、y_raw、u、theta 这四类记录
% =============================
if ~isa(sim_out, 'Simulink.SimulationOutput')
    error('sim output is not Simulink.SimulationOutput');
end

% CaptureErrors='on' 时，sim 可能返回对象但包含 ErrorMessage。
% 若不先判断，会在访问 tout 时出现“字段不存在”的二次报错，掩盖真正根因。
try
    sim_err = sim_out.ErrorMessage;
catch
    sim_err = '';
end
if ~isempty(sim_err)
    error('Simulink simulation failed: %s', sim_err);
end

if ~isprop(sim_out, 'tout') || isempty(sim_out.tout)
    error('sim output has no tout. Check model compile/runtime diagnostics first.');
end

t = sim_out.tout;

if ~isstruct(sim_out.y_raw1) || ~isfield(sim_out.y_raw1, 'signals')
    error('y_raw format invalid');
end
y_raw = sim_out.y_raw1.signals.values;

if ~isstruct(sim_out.u1) || ~isfield(sim_out.u1, 'signals')
    error('u format invalid');
end
u = sim_out.u1.signals.values;

if ~isstruct(sim_out.theta1) || ~isfield(sim_out.theta1, 'signals')
    error('theta format invalid');
end
theta = sim_out.theta1.signals.values;
end

function [y_mamba, names] = build_mamba_channels(y_raw)
% =============================
% 函数名：build_mamba_channels
% 功能：从 34 维 y_raw 中选取 Mamba 输入通道（传感器导向）。
% 依赖：
%   - output_eq_ref_train_data.m 的输出索引定义
% 调用：
%   - 主循环在每次仿真后调用
% 参数设置：
%   - 当前固定 10 维通道，可按部署传感器约束扩展
% =============================
idx = [9, 10, 11, 12, 13, 17, 18, 32, 33, 34];
y_mamba = y_raw(:, idx);
names = { ...
    'accel_x_meas', 'gyro_y_meas', 'gyro_z_meas', ...
    'I_meas_lf', 'I_meas_rr', ...
    'omega_wheel_lf', 'omega_wheel_rr', ...
    'slip_ratio_lf', 'slip_ratio_rr', 'accel_y_meas' ...
};
end

function [label_main, label_turn, label_slip, label_stall, label_load_change, y_theta_ground, y_delta_vehicle] = ...
    generate_mamba_labels(t, y_raw, theta, omega_ref, inject_info, Ts, params_sim, target_cfg)
% =============================
% 函数名：generate_mamba_labels
% 功能：
%   1) 生成多头分类标签（main/turn/slip/stall）
%   2) 生成回归目标（坡度角 y_theta_ground、整车等效转向角 y_delta_vehicle）
% 依赖：
%   - y_raw 索引：v=y_raw(:,4), omega_z=y_raw(:,5), slip_ratio=y_raw(:,32:33)
%   - 参数结构 params_sim（读取 L 作为等效轴距）
% 调用：
%   - 主循环每次 run 处理完 y_raw 后调用
% 参数设置：
%   - target_cfg.v_eps: 低速保护阈值
%   - target_cfg.delta_smooth_steps: 转向角标签平滑窗口长度
% =============================
N = length(t);
label_main = ones(N, 1);  % 1=flat
label_slip = zeros(N, 1);
label_stall = zeros(N, 1);
label_load_change = zeros(N, 1);

% 回归目标1：坡度角（直接采用仿真真实量）
y_theta_ground = theta;

% 回归目标2：整车等效转向角
% 定义：delta = atan(L_eq * omega_z / max(v, v_eps))
L_eq = get_field(params_sim, 'L', 2.0);
v_eps = get_field(target_cfg, 'v_eps', 0.20);
omega_z = y_raw(:, 5);
v_long = y_raw(:, 4);
v_safe = max(v_long, v_eps);
kappa = omega_z ./ v_safe;
y_delta_vehicle = atan(L_eq .* kappa);

% 轻度滑动平均，降低低速与噪声引发的尖峰
smooth_steps = max(1, round(get_field(target_cfg, 'delta_smooth_steps', 1)));
if mod(smooth_steps, 2) == 0
    smooth_steps = smooth_steps + 1;
end
if smooth_steps > 1
    y_delta_vehicle = smoothdata(y_delta_vehicle, 'movmean', smooth_steps);
end

% Main labels: stall > slope > flat
% V1.3 修正：去掉速度门控（v < 0.40 m/s）。
%   原因：stall 注入为增大负载（210~320 kg），AGV 电机扭矩足够使车辆维持正常行驶速度，
%         速度门控导致注入窗口内几乎无帧被标为 stall → 训练集 stall 正样本实际为 0。
%   现策略：注入窗口全帧标为 stall（ground truth 已知）。
%   stall / slope 的训练对比依赖电流幅值差异（stall负载210~320kg >> slope重力分量），
%   模型从电流特征区分，不依赖标注时的速度过滤。
v_meas_vec = y_raw(:, 4);      % y_raw(:,4) = v（纵向速度），保留供启发式 stall 使用

if isfield(inject_info, 'stall_injected') && inject_info.stall_injected
    if isfield(inject_info, 'stall_windows') && ~isempty(inject_info.stall_windows)
        wins = inject_info.stall_windows;
    else
        wins = inject_info.stall_window;
    end
    for w = 1:size(wins, 1)
        m = t >= wins(w, 1) & t <= wins(w, 2);
        % 注入窗口内全帧标为 stall（已知 ground truth，无需速度过滤）
        label_main(m) = 2;
        label_stall(m) = 1;
    end
end

theta_slope_thresh = deg2rad(2.0);
m_slope = abs(theta) >= theta_slope_thresh & label_main == 1;
label_main(m_slope) = 3;

% Turn labels from omega_ref with dwell
omega_turn_thresh = 0.05;
raw_turn = zeros(N, 1);
raw_turn(omega_ref > omega_turn_thresh) = 1;
raw_turn(omega_ref < -omega_turn_thresh) = -1;
label_turn = apply_turn_dwell(raw_turn, max(1, round(0.40 / Ts)));

% Slip labels - V1.5: 纯窗口标注（仅注入 ground truth）
% 根因修复（output_eq_ref_train_data.m V1.5）：slip_gamma<0.95 时注入非对称轮速滑差，
%   LF 正向加速、RR 反向减速，使 slip_ratio_lf/rr 通道在注入期间真实非零。
% 标注策略：仅使用注入窗口作为 ground truth；不使用 slip_abs 阈值兜底。
%   原因：工业路径紧弯（R≈3m）产生运动学差速 slip_abs≈0.10，
%         高于 slip 注入本身（gamma=0.35 → ≈0.056），任何阈值均会产生标签污染。

if isfield(inject_info, 'slip_injected') && inject_info.slip_injected
    for w = 1:size(inject_info.slip_windows, 1)
        m = t >= inject_info.slip_windows(w, 1) & t <= inject_info.slip_windows(w, 2);
        label_slip(m) = 1;
    end
end
% 注意：不使用 slip_abs 兜底阈值。
% 原因：工业路径紧弯（R≈3m）产生运动学轮速差 slip_abs≈0.10，
%       高于 slip 注入（gamma=0.35 → ≈0.056），任何阈值均无法区分转弯与滑转。
%       标签唯一可靠来源是注入窗口 ground truth。

% Load-change 标签：基于注入窗口直接标注（不改变 main 层级）
if isfield(inject_info, 'load_change_injected') && inject_info.load_change_injected
    if isfield(inject_info, 'load_change_windows') && ~isempty(inject_info.load_change_windows)
        lwins = inject_info.load_change_windows;
        for w = 1:size(lwins, 1)
            m = t >= lwins(w, 1) & t <= lwins(w, 2);
            label_load_change(m) = 1;
        end
    elseif isfield(inject_info, 'load_change_window')
        m = t >= inject_info.load_change_window(1) & t <= inject_info.load_change_window(2);
        label_load_change(m) = 1;
    end
end

% Heuristic stall supplement (without overriding existing slope/stall hierarchy)
% 仅当 label_main==1(flat) 且车速接近零（omega_wheel<0.1 rad/s ≈ v<0.015 m/s）时补充 stall 标注
I_sum = abs(y_raw(:, 12)) + abs(y_raw(:, 13));
omega_l = abs(y_raw(:, 17));
omega_r = abs(y_raw(:, 18));
heur_stall = (I_sum > 12) & (omega_l < 0.1) & (omega_r < 0.1) & (v_meas_vec < 0.20);
heur_stall = apply_dwell(heur_stall, max(1, round(0.8 / Ts)));
label_stall(heur_stall) = 1;
label_main(heur_stall & label_main == 1) = 2;
end

function out = apply_turn_dwell(raw_turn, dwell_steps)
% =============================
% 函数名：apply_turn_dwell
% 功能：对左右转标签分别做持续时间过滤，抑制短时毛刺。
% 依赖：
%   - apply_dwell
% 调用：
%   - generate_mamba_labels
% 参数设置：
%   - dwell_steps 建议按 0.3~0.5s 折算
% =============================
N = numel(raw_turn);
out = zeros(N, 1);
for sgn = [-1, 1]
    mask = (raw_turn == sgn);
    mask = apply_dwell(mask, dwell_steps);
    out(mask) = sgn;
end
end

function m2 = apply_dwell(m, dwell_steps)
% =============================
% 函数名：apply_dwell
% 功能：布尔序列驻留过滤，仅保留长度>=dwell_steps的连续片段。
% 依赖：无
% 调用：
%   - apply_turn_dwell
%   - generate_mamba_labels（stall 启发式）
% 参数设置：
%   - dwell_steps 越大，标签越平滑但响应越慢
% =============================
N = numel(m);
m2 = false(N, 1);
i = 1;
while i <= N
    if m(i)
        j = i;
        while j <= N && m(j)
            j = j + 1;
        end
        if (j - i) >= dwell_steps
            m2(i:j-1) = true;
        end
        i = j;
    else
        i = i + 1;
    end
end
end

function [ref_path, inj_signal, inject_info, T_end_scene] = generate_reference_path_local(scene, params, cfg, run_idx)
% =============================
% 函数名：generate_reference_path_local
% 功能：
%   1) 生成 150s 工业分区路径（gen_agv_ref_path_v1）
%   2) 黄金区(10-50s)每回合注入单事件样本（slip/load_change/stall）
%   3) 以 20%-30% 概率在 pure_turn/pure_slope/composite 额外注入异常
%   4) 输出注入信号 inj_signal（两通道：slip_gamma/stall_load）及元信息
% 依赖：
%   - gen_agv_ref_path_v1.m
%   - cfg.path_rand / cfg.event_cfg
% 调用：
%   - 主循环每次 run 调用
% 参数设置：
%   - 每次 run 的坡度幅值与转弯强度动态随机化
%   - 黄金区强制单事件，区外异常保持 0.25 概率
% =============================
opts = struct();
T_end_scene = cfg.T_end;

% 每个 run 在工业分区模板上做动态参数随机化
opts.T_end = T_end_scene;
opts.path_type = scene;
opts.v_cruise = cfg.path_rand.v_cruise_range(1) + diff(cfg.path_rand.v_cruise_range) * rand();

theta_grid = cfg.path_rand.slope_angle_pure_grid_deg(:)';
if isempty(theta_grid)
    theta_grid = 8.0;
end
theta_idx = mod(max(1, round(run_idx)) - 1, numel(theta_grid)) + 1;
theta_pure_deg = theta_grid(theta_idx);
ratio = cfg.path_rand.slope_angle_composite_ratio(1) + ...
    diff(cfg.path_rand.slope_angle_composite_ratio) * rand();

opts.slope_angle_pure = deg2rad(theta_pure_deg);
opts.slope_angle_composite = deg2rad(theta_pure_deg * ratio);
opts.turn_scale_pure = cfg.path_rand.turn_scale_pure_fixed;
opts.turn_scale_composite = cfg.path_rand.turn_scale_composite_fixed;
opts.transition_time = cfg.path_rand.transition_time_range(1) + ...
    diff(cfg.path_rand.transition_time_range) * rand();
opts.omega_limit = cfg.path_rand.omega_limit_range(1) + ...
    diff(cfg.path_rand.omega_limit_range) * rand();
opts.v_turn_ref = cfg.path_rand.v_turn_ref_range(1) + ...
    diff(cfg.path_rand.v_turn_ref_range) * rand();
opts.v_slope_ref = deg2rad(cfg.path_rand.v_slope_ref_range_deg(1) + ...
    diff(cfg.path_rand.v_slope_ref_range_deg) * rand());

ref_path = gen_agv_ref_path_v1(params, opts);

inject_info = struct();
inject_info.slip_injected = false;
inject_info.stall_injected = false;
inject_info.load_change_injected = false;
inject_info.slip_windows = [];
inject_info.slip_gammas = [];
inject_info.stall_windows = [];
inject_info.stall_loads = [];
inject_info.load_change_windows = [];
inject_info.load_changes = [];

zones = ref_path.meta.zones;
golden = cfg.event_cfg.golden_zone;
Ts_ref = params.Ts;

% 每回合黄金区单事件（slip / load_change / stall 三选一）
primary_type = sample_event_type_local(cfg.event_cfg.primary_types, cfg.event_cfg.primary_probs);
[p_start, p_end] = sample_window_in_zone_local(golden, cfg.event_cfg.(primary_type).duration_range, Ts_ref);

inject_info.primary_event = struct('type', primary_type, 'window', [p_start, p_end]);
inject_info = apply_event_to_inject_info_local(inject_info, primary_type, [p_start, p_end], cfg.event_cfg);

% 20%-30% 额外异常样本继续放在转弯区和坡度区（含复合区）
inject_info.extra_zone_event_added = false;
if cfg.event_cfg.extra_zone.enable && rand() < cfg.event_cfg.extra_zone.prob
    zname = cfg.event_cfg.extra_zone.targets{randi(numel(cfg.event_cfg.extra_zone.targets))};
    zwin = zones.(zname);
    etype = sample_event_type_local(cfg.event_cfg.primary_types, cfg.event_cfg.extra_zone.type_probs);
    [e_start, e_end] = sample_window_in_zone_local(zwin, cfg.event_cfg.(etype).duration_range, Ts_ref);
    inject_info = apply_event_to_inject_info_local(inject_info, etype, [e_start, e_end], cfg.event_cfg);
    inject_info.extra_zone_event_added = true;
    inject_info.extra_zone_event = struct('zone', zname, 'type', etype, 'window', [e_start, e_end]);
end

t = ref_path.t;
N = numel(t);
slip_gamma_vec = ones(N, 1);
stall_load_vec = zeros(N, 1);

if inject_info.slip_injected && ~isempty(inject_info.slip_windows)
    for w = 1:size(inject_info.slip_windows, 1)
        ww = inject_info.slip_windows(w, :);
        m = t >= ww(1) & t <= ww(2);
        slip_gamma_vec(m) = inject_info.slip_gammas(w);
    end
end

if inject_info.stall_injected && ~isempty(inject_info.stall_windows)
    for w = 1:size(inject_info.stall_windows, 1)
        ww = inject_info.stall_windows(w, :);
        m = t >= ww(1) & t <= ww(2);
        stall_load_vec(m) = inject_info.stall_loads(w);
    end
end

if inject_info.load_change_injected && ~isempty(inject_info.load_change_windows)
    for w = 1:size(inject_info.load_change_windows, 1)
        ww = inject_info.load_change_windows(w, :);
        m = t >= ww(1) & t <= ww(2);
        stall_load_vec(m) = stall_load_vec(m) + inject_info.load_changes(w);
    end
end

% 向后兼容字段（便于已有分析函数直接复用）
if inject_info.slip_injected
    inject_info.slip_window = inject_info.slip_windows(1, :);
    inject_info.slip_gamma = inject_info.slip_gammas(1);
end
if inject_info.stall_injected
    inject_info.stall_window = inject_info.stall_windows(1, :);
    inject_info.stall_load = inject_info.stall_loads(1);
end
if inject_info.load_change_injected
    inject_info.load_change_window = inject_info.load_change_windows(1, :);
    inject_info.load_change = inject_info.load_changes(1);
end

inj_signal = struct();
inj_signal.time = t;
inj_signal.signals = struct();
inj_signal.signals.values = [slip_gamma_vec, stall_load_vec];
inj_signal.signals.dimensions = 2;
end

function event_type = sample_event_type_local(type_list, probs)
% 从候选事件类型中按概率采样
if nargin < 2 || isempty(probs)
    probs = ones(1, numel(type_list)) / numel(type_list);
else
    probs = probs(:)' / sum(probs);
end
cs = cumsum(probs);
r = rand();
idx = find(r <= cs, 1, 'first');
if isempty(idx)
    idx = numel(type_list);
end
event_type = type_list{idx};
end

function [t_start, t_end] = sample_window_in_zone_local(zone, dur_range, Ts)
% 在指定 zone 内随机采样事件窗口，确保窗口长度合法
z0 = zone(1);
z1 = zone(2);
dur = dur_range(1) + (dur_range(2) - dur_range(1)) * rand();
dur = max(dur, Ts);
if z1 - z0 <= dur + Ts
    t_start = z0;
    t_end = z1;
    return;
end
t_start = z0 + (z1 - z0 - dur) * rand();
t_end = t_start + dur;
end

function inject_info = apply_event_to_inject_info_local(inject_info, event_type, window, event_cfg)
% 将事件写入注入信息结构（支持 slip / load_change / stall）
switch lower(event_type)
    case 'slip'
        inject_info.slip_injected = true;
        gamma = event_cfg.slip.gamma_range(1) + diff(event_cfg.slip.gamma_range) * rand();
        inject_info.slip_windows = [inject_info.slip_windows; window];
        inject_info.slip_gammas = [inject_info.slip_gammas; gamma];

    case 'stall'
        inject_info.stall_injected = true;
        load_val = event_cfg.stall.load_range(1) + diff(event_cfg.stall.load_range) * rand();
        inject_info.stall_windows = [inject_info.stall_windows; window];
        inject_info.stall_loads = [inject_info.stall_loads; load_val];

    case 'load_change'
        inject_info.load_change_injected = true;
        load_val = event_cfg.load_change.load_range(1) + diff(event_cfg.load_change.load_range) * rand();
        inject_info.load_change_windows = [inject_info.load_change_windows; window];
        inject_info.load_changes = [inject_info.load_changes; load_val];

    otherwise
        error('unknown event type: %s', event_type);
end
end

function n = get_scene_runs(scene, default_runs, per_scene)
% =============================
% 函数名：get_scene_runs
% 功能：读取场景 run 数，支持 per-scene 覆盖默认值。
% 依赖：无
% 调用：
%   - 主脚本初始化阶段
% 参数设置：
%   - per_scene.<scene> 优先，缺失时回退 default_runs
% =============================
if isstruct(per_scene) && isfield(per_scene, scene)
    n = per_scene.(scene);
else
    n = default_runs;
end
n = max(1, round(n));
end

function [enable_noise, std_scale, variant] = resolve_noise_profile_local(profile, noise_on)
% =============================
% 函数名：resolve_noise_profile_local
% 功能：根据噪声策略决定本次 run 的噪声开关与噪声倍率。
% 依赖：
%   - get_field
%   - ternary
% 调用：
%   - 主循环每次 run 调用
% 参数设置：
%   - profile.mode='match' 或 'mixed'
%   - mixed 模式下可配置 clean_ratio/noisy_scales/noisy_probs
% =============================
mode = get_field(profile, 'mode', 'match');
if strcmpi(mode, 'match')
    enable_noise = logical(noise_on);
    std_scale = double(enable_noise);
    variant = ternary(enable_noise, 'match_noisy', 'match_clean');
    if enable_noise && std_scale == 0
        std_scale = 1.0;
    end
    return;
end

clean_ratio = get_field(profile, 'clean_ratio', 0.3);
scales = get_field(profile, 'noisy_scales', [1.0]);
probs = get_field(profile, 'noisy_probs', []);

if rand() < clean_ratio
    enable_noise = false;
    std_scale = 0;
    variant = 'mixed_clean';
    return;
end

enable_noise = true;
if isempty(scales)
    scales = [1.0];
end
if isempty(probs)
    probs = ones(size(scales)) / numel(scales);
else
    probs = probs(:)';
    probs = probs / sum(probs);
end

r = rand();
cs = cumsum(probs);
idx = find(r <= cs, 1, 'first');
if isempty(idx)
    idx = numel(scales);
end
std_scale = scales(idx);
variant = sprintf('mixed_noisy_x%.2f', std_scale);
end

function v = get_field(s, name, default_v)
% =============================
% 函数名：get_field
% 功能：安全读取结构体字段，不存在时返回默认值。
% 依赖：无
% 调用：
%   - 多个本地函数
% 参数设置：
%   - default_v 用于统一默认参数入口
% =============================
if isstruct(s) && isfield(s, name)
    v = s.(name);
else
    v = default_v;
end
end

function out = ternary(cond, a, b)
% =============================
% 函数名：ternary
% 功能：三元表达式辅助函数。
% 依赖：无
% 调用：
%   - resolve_noise_profile_local
% 参数设置：无
% =============================
if cond
    out = a;
else
    out = b;
end
end

function prepare_runtime_workspace_local(model_name, verbose)
% =============================
% 函数名：prepare_runtime_workspace_local
% 功能：
%   在数据生成前刷新模型运行时依赖（尤其是 ctrl/mpc 相关变量），
%   避免当前 MATLAB 会话遗留变量导致 Adaptive MPC 维度冲突。
% 依赖：
%   - preloadfcn_v2.m（优先）或 preloadfcn_v1.m
% 调用：
%   - 主脚本初始化阶段，load_system 后调用一次
% 参数设置：
%   - model_name: Simulink 模型名
%   - verbose: 是否打印过程信息
% =============================
if nargin < 2
    verbose = false;
end

if verbose
    fprintf('Preparing runtime workspace for model: %s\n', model_name);
end

% 先尝试执行项目路径初始化，确保 preload 函数可解析。
if exist('init_project', 'file') == 2
    try
        init_project();
    catch ME
        if verbose
            fprintf('  init_project skipped: %s\n', ME.message);
        end
    end
end

% 优先使用新版 preload，确保 ctrl/maps 与当前模型结构一致。
if exist('preloadfcn_v2', 'file') == 2
    try
        evalin('base', 'preloadfcn_v2');  % 必须在base workspace执行，否则Bus.createObject的eval找不到临时变量
    catch ME
        warning('Mamba_gen_train_data:PreloadFailed', ...
            'preloadfcn_v2 failed: %s', ME.message);
    end
elseif exist('preloadfcn_v1', 'file') == 2
    try
        evalin('base', 'preloadfcn_v1');  % 同理，确保在base workspace执行
    catch ME
        warning('Mamba_gen_train_data:PreloadFailed', ...
            'preloadfcn_v1 failed: %s', ME.message);
    end
else
    if verbose
        fprintf('  preload function not found, continue with current base workspace.\n');
    end
end

% 补充 UpdatePlantModel MATLAB Function block 需要但 preloadfcn 不创建的变量。
% MPC_idx 在 UpdatePlantModel 内部实际未使用（标记为 unused），但 Simulink
% 编译器仍要求它存在于工作区中。默认值设为 LPV 网格中心点索引。
if ~evalin('base', 'exist(''MPC_idx'',''var'')')
    try
        db_tmp = evalin('base', 'db_rt');
        MPC_idx_val = [ceil(db_tmp.Nv/2), ceil(db_tmp.Nw/2), ceil(db_tmp.Nt/2), 1];
    catch
        MPC_idx_val = [6, 8, 11, 1];  % 安全回退值
    end
    assignin('base', 'MPC_idx', MPC_idx_val);
    if verbose
        fprintf('  → 已补充 MPC_idx = [%d, %d, %d] 到 base workspace\n', MPC_idx_val);
    end
end
end
