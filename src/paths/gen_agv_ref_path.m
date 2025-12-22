function ref = gen_agv_ref_path(path_type, params, opts)
% =============================
% 文件名：gen_agv_ref_path.m
% 版本号：V1.3
% 最后修改时间：2025-11-20
% 作者：LPV-MPC Project
% 功能描述：
%   为AGV生成5种场景的参考轨迹数据：
%   - 'straight'      : 平地直线行驶
%   - 'turn'          : 转弯（恒定半径圆弧）
%   - 'straight_turn' : 先直线后左转弯（向后兼容，等价于 straight_left_turn）
%   - 'straight_left_turn'  : 先直线后左转弯
%   - 'straight_right_turn' : 先直线后右转弯
%   - 'slope'         : 坡度直线行驶
%   - 'bumpy'         : 颠簸直线行驶（地面扰动）
%   - 's_curve'       : 直行后S弯（右转后左转）
%
% 输入参数：
%   - path_type : 字符串，路径类型（见上述5种）
%   - params    : 结构体，来自 parameters.m，至少包含 Ts
%   - opts      : 可选参数结构体（可选字段见下）
%       .T_end          : 仿真时长 [s]，默认 20
%       .R              : 转弯半径 [m]，默认 10
%       .v0             : 初速度 [m/s]，默认 1.0
%       .theta_slope    : 坡度角 [rad]，默认 deg2rad(5)
%       .bumpy_amp      : 颠簸振幅 [rad]，默认 0.2（地面坡度扰动振幅）
%       .rho_filter_tau : 调度变量滤波时间常数 [s]，默认 0.4
%       .turn_transition: 转弯过渡时间 [s]，默认 0.4（straight_turn 专用）
%       .turn_direction : 转弯方向，'left'（默认，逆时针/omega>0）或 'right'（顺时针/omega<0）
%       .s_curve_straight_time : S弯前直行时间 [s]，默认 2.0
%       .s_curve_radius : S弯两段转弯半径 [m]，默认 5.0
%       .s_curve_turn_angle : 单个转弯的角度 [rad]，默认 pi/2（90°）
%
% 输出参数：
%   - ref : 结构体，包含以下字段
%       .t          : 时间向量 [Nx1]
%       .X_ref      : 全局X坐标 [Nx1] [m]
%       .Y_ref      : 全局Y坐标 [Nx1] [m]
%       .psi_ref    : 参考航向角 [Nx1] [rad]
%       .v_ref      : 参考纵向速度 [Nx1] [m/s]
%       .omega_ref  : 参考角速度 [Nx1] [rad/s]
%       .theta_ref  : 坡度角参考 [Nx1] [rad]
%       .e_y_ref    : 横向误差参考（=0）[Nx1] [m]
%       .e_psi_ref  : 航向误差参考（=0）[Nx1] [rad]
%       .e_v_ref    : 速度误差参考（=0）[Nx1] [m/s]
%       .rho        : 调度变量轨迹 [Nx3]，列为 [v, omega, theta]
%       .time       : 时间向量（用于From Workspace）
%       .signals    : 信号结构体（用于From Workspace）
%       .meta       : 元数据（生成时间、参数、版本等）
%
% 依赖：
%   - parameters.m (提供 Ts)
%
% 备注：
%   - 所有参考误差量（e_y_ref, e_psi_ref, e_v_ref）设为0，便于MPC跟踪
%   - rho调度变量经过一阶滤波，避免快速跳变
%   - 输出格式兼容Simulink From Workspace模块
% =============================

%% 输入参数处理
if nargin < 3
    opts = struct();
end

% 默认参数
T_end = getFieldOrDefault(opts, 'T_end', 20.0);
R = getFieldOrDefault(opts, 'R', 10.0);
v0 = getFieldOrDefault(opts, 'v0', 1.0);
theta_slope = getFieldOrDefault(opts, 'theta_slope', deg2rad(5));  % 改为5度
bumpy_amp = getFieldOrDefault(opts, 'bumpy_amp', deg2rad(5));      % 改为5度 (±5° 颠簸振幅)
rho_filter_tau = getFieldOrDefault(opts, 'rho_filter_tau', 0.4);
turn_transition = getFieldOrDefault(opts, 'turn_transition', 0.4);  % 转弯过渡时间
turn_direction = getFieldOrDefault(opts, 'turn_direction', 'left');  % 转弯方向（'left'=逆时针，'right'=顺时针）
s_curve_straight_time = getFieldOrDefault(opts, 's_curve_straight_time', 2.0);
s_curve_radius = getFieldOrDefault(opts, 's_curve_radius', 5.0);
s_curve_turn_angle = getFieldOrDefault(opts, 's_curve_turn_angle', pi/2);

% 采样周期
Ts = params.Ts;

% 生成时间向量
t = (0:Ts:T_end)';
N = length(t);

%% 根据路径类型生成轨迹
switch lower(path_type)
    case 'straight'
        [X, Y, psi, v, omega, theta] = gen_straight(t, v0);
        
    case 'turn'
        [X, Y, psi, v, omega, theta] = gen_turn(t, v0, R, turn_direction);
        
    case 'straight_turn'
        turn_dir = getFieldOrDefault(opts, 'turn_direction', 'left');
        [X, Y, psi, v, omega, theta] = gen_straight_turn(t, v0, R, turn_transition, Ts, turn_dir);

    case 'straight_left_turn'
        [X, Y, psi, v, omega, theta] = gen_straight_turn(t, v0, R, turn_transition, Ts, 'left');

    case 'straight_right_turn'
        [X, Y, psi, v, omega, theta] = gen_straight_turn(t, v0, R, turn_transition, Ts, 'right');
        
    case 'slope'
        [X, Y, psi, v, omega, theta] = gen_slope(t, v0, theta_slope);
        
    case 'bumpy'
        [X, Y, psi, v, omega, theta] = gen_bumpy(t, v0, bumpy_amp);
    
    case 's_curve'
        [X, Y, psi, v, omega, theta] = gen_s_curve(t, v0, s_curve_radius, s_curve_straight_time, s_curve_turn_angle);
        
    otherwise
        error('gen_agv_ref_path:InvalidType', ...
              '未知的路径类型: %s。支持类型: straight, turn, straight_turn, slope, bumpy, s_curve', path_type);
end

%% 构建路径坐标系误差参考（设为0，便于MPC跟踪）
e_y_ref = zeros(N, 1);
e_psi_ref = zeros(N, 1);
e_v_ref = zeros(N, 1);

%% 构建调度变量 rho = [v, omega, theta]（均为有符号）并滤波
rho_raw = [v, omega, theta];
rho = applyFirstOrderFilter(rho_raw, Ts, rho_filter_tau);

%% 构建输出结构体
ref.t = t;
ref.X_ref = X;
ref.Y_ref = Y;
ref.psi_ref = psi;
ref.v_ref = v;
ref.omega_ref = omega;
ref.theta_ref = theta;
ref.e_y_ref = e_y_ref;
ref.e_psi_ref = e_psi_ref;
ref.e_v_ref = e_v_ref;
ref.rho = rho;

% 构建From Workspace兼容格式
ref.time = t;
ref.signals.values = [X, Y, psi, v, omega, theta, e_y_ref, e_psi_ref, e_v_ref];
ref.signals.dimensions = 9;

% 元数据
ref.meta.path_type = path_type;
ref.meta.generation_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
ref.meta.version = 'V1.3';
ref.meta.author = 'LPV-MPC Project';
ref.meta.params.T_end = T_end;
ref.meta.params.R = R;
ref.meta.params.v0 = v0;
ref.meta.params.theta_slope = theta_slope;
ref.meta.params.bumpy_amp = bumpy_amp;
ref.meta.params.rho_filter_tau = rho_filter_tau;
ref.meta.params.turn_transition = turn_transition;
ref.meta.params.s_curve_straight_time = s_curve_straight_time;
ref.meta.params.s_curve_radius = s_curve_radius;
ref.meta.params.s_curve_turn_angle = s_curve_turn_angle;
ref.meta.params.Ts = Ts;

end

%% ========== 子函数：各路径类型生成器 ==========

function [X, Y, psi, v, omega, theta] = gen_straight(t, v0)
% 直线路径：匀速直线运动
N = length(t);

X = v0 * t;                % X = v0 * t
Y = zeros(N, 1);           % Y = 0
psi = zeros(N, 1);         % 航向角 = 0 (沿x轴)
v = v0 * ones(N, 1);       % 恒定速度
omega = zeros(N, 1);       % 角速度 = 0
theta = zeros(N, 1);       % 坡度角 = 0
end

function [X, Y, psi, v, omega, theta] = gen_turn(t, v0, R, direction)
% 转弯路径：恒定半径圆弧运动（带角速度渐变启动）
% 从初速度v0开始，转弯半径R
% 改进：前0.5s使用余弦S曲线从omega=0平滑过渡到omega=v0/R
% 输入：
%   - t: 时间向量
%   - v0: 初速度
%   - R: 转弯半径
%   - direction: 转弯方向（'left'=逆时针/omega>0，'right'=顺时针/omega<0）

if nargin < 4
    direction = 'left';  % 默认左转（逆时针）
end

N = length(t);
Ts = t(2) - t(1);  % 采样周期
omega_target = v0 / R;        % 目标角速度幅值 = v / R

% 根据方向调整符号
if strcmpi(direction, 'right')
    omega_target = -omega_target;  % 右转：负角速度（顺时针）
end

t_ramp = 2.0;  % 渐变时间 [s]（延长到2秒，给MPC足够的适应时间）

% 初始化
v = v0 * ones(N, 1);
omega = zeros(N, 1);
psi = zeros(N, 1);
X = zeros(N, 1);
Y = zeros(N, 1);
theta = zeros(N, 1);

% 计算 omega（前0.5s S曲线渐变）
for i = 1:N
    if t(i) <= t_ramp
        % S曲线渐变：omega: 0 → omega_target
        tau = t(i) / t_ramp;  % 归一化时间 [0,1]
        omega(i) = omega_target * 0.5 * (1 - cos(pi * tau));
    else
        % 恒定角速度
        omega(i) = omega_target;
    end
end

% 积分 omega 得到 psi
for i = 2:N
    psi(i) = psi(i-1) + omega(i-1) * Ts;
end

% 根据 psi 计算 X, Y（圆弧轨迹）
for i = 1:N
    X(i) = R * sin(psi(i));
    Y(i) = R * (1 - cos(psi(i)));
end
end

function [X, Y, psi, v, omega, theta] = gen_straight_turn(t, v0, R, t_trans, Ts, direction)
% 直线+转弯路径：前10m直线，后续圆弧，曲率S曲线平滑过渡
% 
% 改进：在 t_switch 处不阶跃，而是用余弦S曲线在 t_trans 时间内平滑过渡
% omega: 0 → v0/R，避免调度变量跳变
N = length(t);

if nargin < 6 || isempty(direction)
    direction = 'left';
end
dir_sign = 1;
if strcmpi(direction, 'right')
    dir_sign = -1;
end

% 直线段长度
straight_dist = 10.0;  % [m]
t_switch = straight_dist / v0;  % 切换时间点
omega_max = dir_sign * (v0 / R);    % 目标角速度，右转为负

% 初始化
X = zeros(N, 1);
Y = zeros(N, 1);
psi = zeros(N, 1);
v = v0 * ones(N, 1);
omega = zeros(N, 1);
theta = zeros(N, 1);

% 计算 psi 积分（需要先计算 omega）
for i = 1:N
    if t(i) <= t_switch
        % 直线段
        omega(i) = 0;
    elseif t(i) <= t_switch + t_trans
        % 过渡段：余弦S曲线
        tau = (t(i) - t_switch) / t_trans;  % 归一化时间 [0,1]
        omega(i) = omega_max * 0.5 * (1 - cos(pi * tau));  % 余弦S曲线（含方向）
    else
        % 转弯段
        omega(i) = omega_max;
    end
end

% 积分 omega 得到 psi
for i = 2:N
    psi(i) = psi(i-1) + omega(i-1) * Ts;  % 欧拉积分
end

% 根据 psi 计算 X, Y（分段处理，保证连续性）
X(1) = 0;
Y(1) = 0;
for i = 2:N
    if t(i) <= t_switch
        % 直线段
        X(i) = v0 * t(i);
        Y(i) = 0;
    else
        % 转弯段（包括过渡）：从上一点积分
        ds = v0 * Ts;  % 微小位移
        X(i) = X(i-1) + ds * cos(psi(i-1));
        Y(i) = Y(i-1) + ds * sin(psi(i-1));
    end
end
end

function [X, Y, psi, v, omega, theta] = gen_slope(t, v0, theta_slope)
% 坡度直线路径：沿x轴直线 + 固定坡度角
N = length(t);

X = v0 * t;
Y = zeros(N, 1);
psi = zeros(N, 1);
v = v0 * ones(N, 1);
omega = zeros(N, 1);
theta = theta_slope * ones(N, 1);  % 恒定坡度角
end

function [X, Y, psi, v, omega, theta] = gen_bumpy(t, v0, bumpy_amp)
% 颠簸直线路径：直线几何路径 + 地面坡度扰动（模拟颠簸）
% 
% 改进：颠簸体现在 theta（地面扰动），而非 Y（几何扰动）
% 这样保持路径坐标系几何仍是直线，更符合"误差=0"理念
% 
% V1.3 改进：前 6s 保持平地直线（theta=0），从第 6s 开始坡度振荡
N = length(t);
t_flat = 6.0;  % 平地直线段持续时间 [s]

% 基础直线轨迹（几何路径保持直线）
X = v0 * t;
Y = zeros(N, 1);            % Y保持为0，几何路径是直线
psi = zeros(N, 1);
v = v0 * ones(N, 1);
omega = zeros(N, 1);

% 颠簸体现在地面坡度扰动（供 MD 端口/AI 使用）
% 前 6s：平地（theta=0）；6s 后：正弦坡度振荡
theta = zeros(N, 1);
for i = 1:N
    if t(i) > t_flat
        theta(i) = bumpy_amp * sin(t(i) - t_flat);  % 从 t_flat 开始计时
    end
end

end

function [X, Y, psi, v, omega, theta] = gen_s_curve(t, v0, R, t_straight, turn_angle)
% S弯路径：先直行，再右转后左转，保持恒速
N = length(t);
if N < 2
    error('gen_s_curve:TimeVectorTooShort', '时间向量长度至少为2');
end

Ts = t(2) - t(1);
t_straight = max(0, t_straight);
remaining = max(t(end) - t_straight, 0);
turn_angle = max(0, abs(turn_angle));
if turn_angle == 0
    turn_angle = pi/2;
end
omega_mag = v0 / max(R, eps);
t_arc_nominal = turn_angle / omega_mag;  % 需要的时间
t_arc = min(t_arc_nominal, remaining / 2);
t2 = t_straight + t_arc;
t3 = t2 + t_arc;

X = zeros(N, 1);
Y = zeros(N, 1);
psi = zeros(N, 1);
v = v0 * ones(N, 1);
omega = zeros(N, 1);
theta = zeros(N, 1);

for i = 1:N
    if t(i) <= t_straight
        omega(i) = 0;
    elseif t(i) <= t2
        omega(i) = -omega_mag;  % 右转
    elseif t(i) <= t3
        omega(i) = omega_mag;   % 左转
    else
        omega(i) = 0;
    end
end

for k = 2:N
    psi(k) = psi(k-1) + omega(k-1) * Ts;
    X(k) = X(k-1) + v0 * Ts * cos(psi(k-1));
    Y(k) = Y(k-1) + v0 * Ts * sin(psi(k-1));
end

% 若剩余时间不足完整S弯，psi可能无法回到0，这里不额外矫正
end

%% ========== 工具函数 ==========
%% ========== 工具函数 ==========

function rho_filtered = applyFirstOrderFilter(rho_raw, Ts, tau)
% 对调度变量应用一阶低通滤波器
% 离散形式: y[k] = alpha * x[k] + (1-alpha) * y[k-1]
% 其中 alpha = Ts / (Ts + tau)

[N, dim] = size(rho_raw);
alpha = Ts / (Ts + tau);
rho_filtered = zeros(N, dim);
rho_filtered(1, :) = rho_raw(1, :);  % 初始值

for k = 2:N
    rho_filtered(k, :) = alpha * rho_raw(k, :) + (1 - alpha) * rho_filtered(k-1, :);
end
end

function value = getFieldOrDefault(s, fieldname, default_value)
% 安全获取结构体字段，若不存在则返回默认值
if isfield(s, fieldname)
    value = s.(fieldname);
else
    value = default_value;
end
end

