function [plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax] = UpdatePlantModel(rho, db_rt, MPC_idx, ff_rt, v_ff_nom, label_vec)
%#codegen
% =========================================================================
% UpdatePlantModel - 使用当前 phase1/phase2 最优参数 + Nominal 前馈
%
% 版本：V2.0（2026-04-06）
%
% 说明：
% 1) Q/R/dR 核心权重区间来自 phase1_best/phase2_best 的 best.ctrl_maps；
% 2) 场景自适应参数来自 phase2_best 的最新结果；
% 3) plant.U(1) 注入重力+滚阻前馈 F_eq，减小上坡"被惩罚"问题；
% 4) V2：新增 label_vec=[label_main; label_slip] 输入，接入 Mamba2 分类输出：
%       - label_main==2 (stall)：放宽 F_cmd 约束，防止 MPC 因力限制求解失败
%       - label_slip==1 (slip) ：降低 F_cmd 上限，减少向打滑轮的驱动力输入
%
% 接口：
%   [plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax] = ...
%       UpdatePlantModel(rho, db_rt, MPC_idx, ff_rt, v_ff_nom, label_vec)
%
% 输入：
%   rho      (3×1)  调度变量 [v_f; omega_f; theta_f]（来自 RhoFilter 输出）
%   db_rt           LPV 模型数据库（来自 lin_agv_db.mat）
%   MPC_idx         保留（未使用，兼容旧接口）
%   ff_rt           前馈参数结构体（含 m/g/c_r 字段）
%   v_ff_nom        保留（未使用，兼容旧接口）
%   label_vec (2×1) 分类标签 [label_main; label_slip]
%                   label_main: 1=flat, 2=stall, 3=slope
%                   label_slip:  0=normal, 1=slip
%
% 输出：plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax（接 Adaptive MPC 各端口）
% =========================================================================

% 保留接口兼容
unused = MPC_idx; %#ok<NASGU>
unused = v_ff_nom; %#ok<NASGU>

%% ==================== Persistent 状态（两处减振功能）====================
persistent rho_omega_lpf stall_on stall_on_cnt stall_off_cnt slope_on slope_on_cnt slope_off_cnt

% 初始化：omega LPF
if isempty(rho_omega_lpf)
    rho_omega_lpf = rho(2);
end

% 初始化：stall 迟滞滤波状态
if isempty(stall_on)
    stall_on      = false;
    stall_on_cnt  = 0;
    stall_off_cnt = 0;
end

% 初始化：slope 迟滞滤波状态
if isempty(slope_on)
    slope_on      = false;
    slope_on_cnt  = 0;
    slope_off_cnt = 0;
end

%% ==================== 基于当前 BO 结果构建 maps_local ====================
% 当前读取来源：
% - Q/R/dR/rho范围/约束范围：phase2_best.mat -> best.ctrl_maps
% - 场景自适应参数：phase2_best.mat -> combined(best.ctrl_maps 同值)

Q_range_bo = [ ...
65.5231, 8.1684, 18.3989, 0.4160; ...
196.5693, 24.5051, 55.1966, 1.2481];

R_range_bo = [ ...
0.0015, 0.0058; ...
0.0046, 0.0173];

dR_range_bo = [ ...
0.0017, 0.1309; ...
0.0050, 0.3927];

maps_local = struct( ...
    'enable_weight_interp', true, ...
    'Q_range', Q_range_bo, ...
    'R_range', R_range_bo, ...
    'dR_range', dR_range_bo, ...
    'alpha_Q', [0.5, 0.5, 0.5, 0.5], ...
    'beta_Q', [0.5, 0.5, 0.5, 0.5], ...
    'alpha_R', [0.5, 0.5], ...
    'beta_R', [0.5, 0.5], ...
    'alpha_dR', [0.5, 0.5], ...
    'beta_dR', [0.5, 0.5], ...
    'scale_umin_lo', [1, 1], ...
    'scale_umin_hi', [1, 1], ...
    'scale_umax_lo', [1, 1], ...
    'scale_umax_hi', [1, 1], ...
    'rho_min', [0.02; -1.2; -0.1745], ...
    'rho_max', [1.2; 1.2; 0.1745], ...
    'tau', 0.35, ...
    'omega_threshold', 0.139817184968, ...
    'q_y_gain_max', 5.54865433581, ...
    'transition_width', 0.03, ...
    'theta_threshold', 0.125151060428, ...
    'q_v_gain_max', 3.46559044719, ...
    'theta_transition_width', 0.02, ...
    'R_F_gain_max_uphill', 1.00755999315, ...
    'R_F_gain_max_downhill', 1.0, ...
    'dR_F_gain_max_uphill', 1.0, ...
    'dR_F_gain_max_downhill', 1.0, ...
    'umin_range', [-720, -1.44; -600, -1.2], ...
    'umax_range', [ 600, 1.2; 720, 1.44] ...
);

%% ==================== 调度变量预处理：omega 补充 LPF ====================
% 问题根因：上游 RhoFilter (tau=0.35s) 在转弯入口 omega 从 0 快速上升时
%   仍会使 LPV 插值点较快跳变，引起 e_psi 和 e_omega 在进入转弯区时颤振。
% 修复：在此内部补充一层 LPF (tau=0.25s)，级联后等效 tau_omega ≈ 0.60s。
% 注意：rho(3) 不追加滞后（保持坡度信息实时用于 F_eq 重力前馈）
Ts_upm    = 0.01;      % UpdatePlantModel 执行步长 [s]
tau_omega = 0.25;      % 补充 LPF 时间常数 [s]
alpha_omg = Ts_upm / (Ts_upm + tau_omega);
rho_omega_lpf = alpha_omg * rho(2) + (1.0 - alpha_omg) * rho_omega_lpf;
rho_upd = [rho(1); rho_omega_lpf; rho(3)];

%% ==================== 在线插値：模型/权重/约束 ====================
upd = mpc_update_from_rho(rho_upd, db_rt, maps_local);

%% ==================== Mamba2 分类标签覆盖（V2 新增）====================
% label_vec = [label_main; label_slip]
% label_main: 1=flat, 2=stall, 3=slope
% label_slip:  0=normal, 1=slip
lbl_main = label_vec(1);
lbl_slip  = label_vec(2);

% --- stall 非对称迟滞滤波（解决 2↔3 快速切换导致约束抖动的问题）---
% 问题根因：Mamba 在坡道爬坡时 label_main 每 0.05s 在 2(stall)↔3(slope) 之间切换，
%   导致 UpdatePlantModel 对 umin/umax 每 5 步交替放宽/还原，MPC 求解状态抖动。
% 修复：非对称迟滞滤波（ON 阈值小、OFF 阈值大）
%   - 需要连续 20 步 (0.2s) 检测到 stall 才激活（防误判干扰 MPC）
%   - 需要连续 50 步 (0.5s) 未检测到 stall 才退出（防止进/出护振荡）
STALL_ON_THRESH  = 20;
STALL_OFF_THRESH = 50;

if lbl_main == 2
    stall_on_cnt  = stall_on_cnt + 1;
    stall_off_cnt = 0;
    if stall_on_cnt >= STALL_ON_THRESH
        stall_on = true;
    end
else
    stall_off_cnt = stall_off_cnt + 1;
    stall_on_cnt  = 0;
    if stall_off_cnt >= STALL_OFF_THRESH
        stall_on = false;
    end
end

% 稳定化后的有效判断标志
lbl_main_eff = lbl_main;
if stall_on
    lbl_main_eff = 2;  % 持续保持 stall 激活（stall 优先级最高）
end

% --- slope 非对称迟滞滤波（防止 slope(3)↔flat(1) 高频切换）---
% 问题根因：Mamba 在坡道入/出边界处 label_main 在 1(flat)↔3(slope) 间高频跳变，
%   导致下游消费者（约束调度、scope 显示）收到噪声信号，引起 e_omega 脉冲尖峰。
% 参数选择：slope 比 stall 更保守（OFF 阈值更大），坡道行驶时间较长，
%   错误延迟退出坡道判断的代价低于错误进入坡道判断。
SLOPE_ON_THRESH  = 30;   % 连续 30 步 (0.3s) 检测到 slope 才激活
SLOPE_OFF_THRESH = 80;   % 连续 80 步 (0.8s) 未检测到 slope 才退出

if lbl_main == 3
    slope_on_cnt  = slope_on_cnt + 1;
    slope_off_cnt = 0;
    if slope_on_cnt >= SLOPE_ON_THRESH
        slope_on = true;
    end
else
    slope_off_cnt = slope_off_cnt + 1;
    slope_on_cnt  = 0;
    if slope_off_cnt >= SLOPE_OFF_THRESH
        slope_on = false;
    end
end

% slope 迟滞仅在非 stall 状态下覆盖（stall 优先级更高）
if slope_on && lbl_main_eff == 1
    lbl_main_eff = 3;  % 维持 slope 激活，消除 flat 瞬间误判
end

% --- 堵转（stall）：放宽驱动力上下界，防止 AGV 被困时 MPC 无法输出足够力 ---
% 堵转时摩擦力骤增（外部阻力远超正常值），若约束不放宽 MPC 将持续求解失败
if lbl_main_eff == 2
    stall_f_scale = 1.4;  % F_cmd 约束放宽到 140%
    upd.umin(1) = upd.umin(1) * stall_f_scale;
    upd.umax(1) = upd.umax(1) * stall_f_scale;
end

% --- 打滑（slip）：降低最大驱动力，通过减少驱动扭矩使轮胎恢复牵引力 ---
% 理论依据：轮胎打滑时纵向力已过峰值，继续施力只会增大滑移率
if lbl_slip == 1
    slip_f_scale = 0.65;  % F_cmd 上限降低到 65%
    upd.umax(1) = upd.umax(1) * slip_f_scale;
    % 放宽速度跟踪权重（Q 索引 3 = q_v），允许 AGV 自然减速
    upd.Q(3) = upd.Q(3) * 0.5;
end

%% ==================== 组装 plant（带 Nominal 前馈） ====================
nx = size(upd.A, 1);
ny = size(upd.C, 1);

plant.A = upd.A;

hasE = isfield(upd, 'E') && ~isempty(upd.E);
if hasE
    E_col = upd.E;
else
    E_col = zeros(nx, 1);
end

plant.B = [upd.B, E_col];
plant.C = upd.C;
plant.D = [upd.D, zeros(ny,1)];

% 重力 + 滚阻前馈
m_agv    = ff_rt.m;
g_acc    = ff_rt.g;
c_roll   = ff_rt.c_r;
theta_meas = rho(3);

F_eq = m_agv * g_acc * (sin(theta_meas) + c_roll * cos(theta_meas));

% Nominal: [MV1; MV2; MD]
plant.U  = [F_eq; 0; 0];
plant.X  = zeros(nx,1);
plant.Y  = zeros(ny,1);
plant.DX = zeros(nx,1);
plant.Ts = db_rt.Ts;

%% ==================== 输出给 MPC ====================
y_wt  = upd.Q(:);
u_wt  = upd.R(:);
du_wt = upd.dR(:);

ecr_wt = 1e4;
umin = upd.umin(:);
umax = upd.umax(:);

end
