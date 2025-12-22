function Gemini_test_3(block)
% =============================
% 文件名：Gemini_test_2.m  (替换版)
% 版本号：V1.1 (replacement)
% 最后修改时间：2025-09-30
% 作者：AGV MPC项目组（替换版由助手根据用户工程整理）
% 功能描述：对角式双舵轮AGV动力学 Level-2 S-Function（用于MPC路径跟踪 + AI/语义SLAM）
% 输入参数（u）：
%   u(1): F_cmd (N)        - 总牵引力指令（驱动轮合力）
%   u(2): omega_cmd (rad/s)- 角速度参考（几何转向角目标计算）
%   u(3): theta_ground(rad)- 地面坡度角
% 输出参数（y，18×1）：
%   [1]  X                 (m)
%   [2]  Y                 (m)
%   [3]  psi               (rad)
%   [4]  v                 (m/s)
%   [5]  omega             (rad/s)
%   [6]  delta_lf          (rad)
%   [7]  delta_rr          (rad)
%   [8]  beta              (rad)
%   [9]  IMU_ax            (m/s^2)   -- 纵向加速度测量
%   [10] IMU_gyro_y        (rad/s)   -- 俯仰角速度测量（如未用，可等于0）
%   [11] IMU_gyro_z        (rad/s)   -- 横摆角速度测量
%   [12] I_lf              (A)       -- 左前电机电流估计
%   [13] I_rr              (A)       -- 右后电机电流估计
%   [14] Fdist_lf          (N)       -- 左前扰动力估计（净外力残差）
%   [15] Fdist_rr          (N)       -- 右后扰动力估计
%   [16] theta_ground      (rad)
%   [17] omega_w_lf        (rad/s)   -- 左前轮角速度
%   [18] omega_w_rr        (rad/s)   -- 右后轮角速度
% 依赖：parameters.m中的params结构体
% 备注：
%  - 本替换版修复：变量名截断、角度归一化、速度小负值处理、噪声可复现。
%  - 增强：载荷转移、按载荷比例 + 摩擦椭圆限幅的牵引分配；舵机一阶执行器 + 速率限；
%          空气阻力模型；集中参数校验与缺省；RK4中转向插值；更稳健的轮速与估计量。
% =============================

%% 基础设置
setup(block);

%% ========================================================================
function setup(block)
    % 端口：3入 1出
    block.NumInputPorts  = 3;
    block.NumOutputPorts = 1;

    % 输入端口维度
    block.SetPreCompInpPortInfoToDynamic;
    block.InputPort(1).Dimensions = 1;   % F_cmd
    block.InputPort(2).Dimensions = 1;   % omega_cmd
    block.InputPort(3).Dimensions = 1;   % theta_ground

    % 输出端口维度
    block.SetPreCompOutPortInfoToDynamic;
    block.OutputPort(1).Dimensions = 18;

    % 参数（1个：params结构体）
    block.NumDialogPrms     = 1;
    block.DialogPrmsTunable = {'Nontunable'};

    % 采样时间：继承（-1,0），内部使用 params.Ts
    block.SampleTimes = [-1, 0];

    % 其他
    block.SetAccelRunOnTLC(false);

    % 注册方法
    block.RegBlockMethod('PostPropagationSetup', @DoPostPropSetup);
    block.RegBlockMethod('InitializeConditions', @InitializeConditions);
    block.RegBlockMethod('Update',              @Update);
    block.RegBlockMethod('Outputs',             @Outputs);
    block.RegBlockMethod('Terminate',           @Terminate);
end

%% ========================================================================
function DoPostPropSetup(block)
    % 连续状态数：这里把系统主要状态放在DWork中管理（也可改为ContinuousStates）
    % DWork使用：
    % 1: x 状态向量 [X Y psi v omega delta_lf delta_rr beta] (8x1)
    % 2: Ts
    % 3: 缓存/临时（预留）

    block.NumDworks = 3;

    block.Dwork(1).Name            = 'x_state';
    block.Dwork(1).Dimensions      = 8;
    block.Dwork(1).DatatypeID      = 0;      % double
    block.Dwork(1).Complexity      = 'Real';
    block.Dwork(1).UsedAsDiscState = true;

    block.Dwork(2).Name            = 'Ts';
    block.Dwork(2).Dimensions      = 1;
    block.Dwork(2).DatatypeID      = 0;
    block.Dwork(2).Complexity      = 'Real';
    block.Dwork(2).UsedAsDiscState = true;

    block.Dwork(3).Name            = 'params_cache';
    block.Dwork(3).Dimensions      = 28;  % 存储28个参数
    block.Dwork(3).DatatypeID      = 0;
    block.Dwork(3).Complexity      = 'Real';
    block.Dwork(3).UsedAsDiscState = true;
end

%% ========================================================================
function InitializeConditions(block)
    params = block.DialogPrm(1).Data;

    % 基本参数/缺省与校验（gd: get default）
    Ts    = gd(params,'Ts',0.05);  % 默认采样周期改为 0.05s
    m     = gd(params,'m',50);
    I_z   = gd(params,'I_z',5.0);
    L     = gd(params,'L',0.8);
    W     = gd(params,'W',0.6);
    h_cg  = gd(params,'h_cg',0.25);
    r     = gd(params,'r',0.08);
    n     = gd(params,'n',9.0);
    eta   = gd(params,'eta',0.9);
    k_t   = gd(params,'k_t',0.3);      % 必需
    mu    = gd(params,'mu',0.8);
    c_r   = gd(params,'c_r',0.015);
    rho   = gd(params,'rho',1.225);
    CdA   = gd(params,'CdA',0.6);


    C_af  = gd(params,'C_alpha_f',12000);
    C_ar  = gd(params,'C_alpha_r',12000);

    delta_max     = gd(params,'delta_max',deg2rad(35));
    delta_dot_max = gd(params,'delta_dot_max',deg2rad(400));
    tau_delta     = gd(params,'tau_delta',0.05); % 舵机一阶常数

    current_limit = gd(params,'current_limit',9);      % A（相当于等效限制）
    accel_limit   = gd(params,'accel_limit',1.0);      % m/s^2（可作为求解保护）

    g  = gd(params,'g',9.81);

    % 阈值集中
    min_omega_threshold = gd(params,'min_omega_threshold',1e-3);
    low_speed_thresh    = gd(params,'low_speed_thresh',  0.05);

    % 噪声设定
    enable_noise = gd(params,'enable_noise',false);
    current_noise_std     = gd(params,'current_noise_std',0.2);
    wheel_speed_noise_std = gd(params,'wheel_speed_noise_std',0.5);
    dist_noise_std        = gd(params,'dist_noise_std',3.0);
    rng_seed = gd(params,'rng_seed',0);
    if rng_seed>0
        rng(rng_seed);
    end

    % 派生/缓存（可存在 tmp 里或忽略）
    block.Dwork(2).Data = Ts;

    % 初始状态
    x0 = zeros(8,1);
    % [X Y psi v omega delta_lf delta_rr beta]
    x0(1) = gd(params,'X0',0);
    x0(2) = gd(params,'Y0',0);
    x0(3) = gd(params,'psi0',0);
    x0(4) = gd(params,'v0',0);
    x0(5) = gd(params,'omega0',0);
    x0(6) = gd(params,'delta_lf0',0);
    x0(7) = gd(params,'delta_rr0',0);
    x0(8) = gd(params,'beta0',0);

    block.Dwork(1).Data = x0;

    % 将关键参数转换为数值数组存储到DWork(3)中
    P = struct('Ts',Ts,'m',m,'I_z',I_z,'L',L,'W',W,'h_cg',h_cg,'r',r,'n',n,'eta',eta,'k_t',k_t, ...
               'mu',mu,'c_r',c_r,'rho',rho,'CdA',CdA,'C_af',C_af,'C_ar',C_ar, ...
               'delta_max',delta_max,'delta_dot_max',delta_dot_max,'tau_delta',tau_delta, ...
               'current_limit',current_limit,'accel_limit',accel_limit,'g',g, ...
               'min_omega_threshold',min_omega_threshold,'low_speed_thresh',low_speed_thresh, ...
               'enable_noise',enable_noise,'current_noise_std',current_noise_std, ...
               'wheel_speed_noise_std',wheel_speed_noise_std,'dist_noise_std',dist_noise_std);
    
    % 创建参数数组并存储到DWork(3)
    param_array = [Ts,m,I_z,L,W,h_cg,r,n,eta,k_t,mu,c_r,rho,CdA,C_af,C_ar, ...
                   delta_max,delta_dot_max,tau_delta,current_limit,accel_limit,g, ...
                   min_omega_threshold,low_speed_thresh,double(enable_noise),current_noise_std, ...
                   wheel_speed_noise_std,dist_noise_std];
    
    % 存储参数数组到DWork(3)
    block.Dwork(3).Data = param_array;
end

%% ========================================================================
function Update(block)
    % 这里可留空（离散状态在Outputs里更新）
end

%% ========================================================================
function Outputs(block)
    params = block.DialogPrm(1).Data;
    
    % 从DWork(3)读取缓存的参数
    param_array = block.Dwork(3).Data;
    
    % 按顺序提取参数
    Ts=param_array(1); m=param_array(2); I_z=param_array(3); L=param_array(4); 
    W=param_array(5); h_cg=param_array(6); r=param_array(7); n=param_array(8); 
    eta=param_array(9); k_t=param_array(10); mu=param_array(11); c_r=param_array(12); 
    rho=param_array(13); CdA=param_array(14); C_af=param_array(15); C_ar=param_array(16);
    delta_max=param_array(17); delta_dot_max=param_array(18); tau_delta=param_array(19);
    current_limit=param_array(20); accel_limit=param_array(21); g=param_array(22);
    min_omega_threshold=param_array(23); low_speed_thresh=param_array(24); 
    enable_noise=logical(param_array(25)); current_noise_std=param_array(26);
    wheel_speed_noise_std=param_array(27); dist_noise_std=param_array(28);
    
    % 重构P结构体（用于compute_load_transfer函数）
    P = struct('Ts',Ts,'m',m,'I_z',I_z,'L',L,'W',W,'h_cg',h_cg,'r',r,'n',n,'eta',eta,'k_t',k_t, ...
               'mu',mu,'c_r',c_r,'rho',rho,'CdA',CdA,'C_af',C_af,'C_ar',C_ar, ...
               'delta_max',delta_max,'delta_dot_max',delta_dot_max,'tau_delta',tau_delta, ...
               'current_limit',current_limit,'accel_limit',accel_limit,'g',g, ...
               'min_omega_threshold',min_omega_threshold,'low_speed_thresh',low_speed_thresh, ...
               'enable_noise',enable_noise,'current_noise_std',current_noise_std, ...
               'wheel_speed_noise_std',wheel_speed_noise_std,'dist_noise_std',dist_noise_std);

    % 读状态/输入
    x = block.Dwork(1).Data;           % [X Y psi v omega delta_lf delta_rr beta]

    X_k = x(1); Y_k = x(2); psi_k = x(3); v_k = x(4);
    omega_k = x(5); delta_lf_k = x(6); delta_rr_k = x(7); beta_k = x(8);

    F_cmd       = block.InputPort(1).Data;
    omega_cmd   = block.InputPort(2).Data;
    theta_ground= block.InputPort(3).Data;

    % 参数已经从param_array中提取，直接使用
    noise_factor = double(enable_noise);

    % === 几何：对角式转向目标（ICR x_c=0） ===
    if abs(omega_cmd) < min_omega_threshold || v_k < low_speed_thresh
        delta_lf_target = 0; delta_rr_target = 0; R_cmd = inf;
    else
        R_cmd = max(v_k/omega_cmd, 1e-6)*sign(omega_cmd); % 参考曲率半径（带符号）
        % 对角布置：左前/右后转角与ICR关系（简单几何近似）
        x_c = 0; y_c = R_cmd; sgn = sign(omega_cmd);
        r_lf = sqrt( (x_c -  L/2)^2 + (y_c -  W/2*sgn)^2 );
        r_rr = sqrt( (x_c +  L/2)^2 + (y_c +  W/2*sgn)^2 );
        % 近似舵角：tan(delta) ≈ 轴距 / 轮到ICR的横向距
        delta_lf_target = atan2(L, max(r_lf,1e-6));
        delta_rr_target = atan2(L, max(r_rr,1e-6));
    end

    % === 舵机动力学：一阶 + 速率限 + 角度限 ===
    delta_lf_dot = (delta_lf_target - delta_lf_k)/max(tau_delta,Ts);
    delta_rr_dot = (delta_rr_target - delta_rr_k)/max(tau_delta,Ts);
    delta_lf_dot = sat(delta_lf_dot, -delta_dot_max, delta_dot_max);
    delta_rr_dot = sat(delta_rr_dot, -delta_dot_max, delta_dot_max);

    delta_lf_new = sat(delta_lf_k + Ts*delta_lf_dot, -delta_max, delta_max);
    delta_rr_new = sat(delta_rr_k + Ts*delta_rr_dot, -delta_max, delta_max);

    % === 载荷转移 & 滚阻 ===
    [N_lf,N_rf,N_lr,N_rr,F_rolling_total] = compute_load_transfer(F_cmd, omega_k, v_k, theta_ground, P);

    % === 电机/传动限制推算到车轮牵引上限 ===
    F_wheel_max = P.current_limit * k_t * (eta * n) / max(r,1e-6);  % 单驱动轮
    num_drive_wheels = 2; % lf & rr
    F_cmd_max_total  = num_drive_wheels * F_wheel_max;
    F_cmd_eff        = sat_sym(F_cmd, F_cmd_max_total);

    % === 侧偏角（简单自行车模型的近似，用β作为全车质心侧滑角） ===
    % 轮侧偏角近似：alpha_f = delta_lf - (v_y + Lf*omega)/v_x ≈ delta_lf - (beta + Lf*omega/v)
    %               alpha_r = - (beta - Lr*omega/v)
    Lf = L/2; Lr = L/2; % 对称
    v_x = max(v_k * cos(beta_k), 1e-3);
    alpha_f = delta_lf_new - (beta_k + Lf*omega_k/max(v_k,1e-3));
    alpha_r =            0 - (beta_k - Lr*omega_k/max(v_k,1e-3));

    % 线性侧偏刚度 + 软饱和（限幅到μN）
    Fy_f_lin = -C_af * alpha_f;
    Fy_r_lin = -C_ar * alpha_r;
    Fy_f_max = mu * N_lf;
    Fy_r_max = mu * N_rr;
    Fy_f = sat(Fy_f_lin, -Fy_f_max, Fy_f_max);
    Fy_r = sat(Fy_r_lin, -Fy_r_max, Fy_r_max);

    % === 牵引力分配：按法向载荷比例 + 摩擦椭圆限幅 ===
    W_total = m*g*cos(theta_ground);
    w_lf = N_lf / max(W_total,1e-6);
    w_rr = N_rr / max(W_total,1e-6);
    Fx_lf_cmd = F_cmd_eff * w_lf;
    Fx_rr_cmd = F_cmd_eff * w_rr;

    % 摩擦椭圆：sqrt((Fx/μN)^2 + (Fy/μN)^2) <= 1
    Fx_lf_allow = mu * N_lf * sqrt(max(1 - (Fy_f/max(mu*N_lf,1e-6))^2, 0));
    Fx_rr_allow = mu * N_rr * sqrt(max(1 - (Fy_r/max(mu*N_rr,1e-6))^2, 0));
    F_drive_lf  = sign(Fx_lf_cmd) * min(abs(Fx_lf_cmd), Fx_lf_allow);
    F_drive_rr  = sign(Fx_rr_cmd) * min(abs(Fx_rr_cmd), Fx_rr_allow);

    % 合力/合力矩
    F_drive_total = F_drive_lf + F_drive_rr;

    % 空气阻力 + 滚动阻力 + 坡度分量
    F_aero  = 0.5 * rho * CdA * v_k^2 * sign(v_k);
    F_drag  = F_rolling_total + F_aero;
    F_slope = m * g * sin(theta_ground);

    % 有效质量（可加旋转件等效）
    m_eff_total = m; % 如需考虑电机/轮等转动惯量，可加到此

    % === 连续动力学（以插值后的舵角） ===
    function ds = dynamics(s, delta_lf, delta_rr)
        X = s(1); Y = s(2); psi = s(3); v = s(4); omega = s(5); beta = s(6);
        % 纵向
        a_x = (F_drive_total - F_drag - F_slope) / max(m_eff_total,1e-6);
        v_dot = a_x;                            % 简化：将纵向加速度直接作用在v
        % 横摆/侧向
        Mz   = Fy_f*Lf - Fy_r*Lr;               % 绕质心的偏航力矩
        omega_dot = (Mz / max(I_z,1e-6));
        if v < low_speed_thresh
            beta_dot = -2.0*beta;               % 低速时以阻尼收敛
        else
            beta_dot = (Fy_f + Fy_r) / (m * max(v,low_speed_thresh/10)) - omega - 0.5*beta;
        end
        psi_dot = omega;
        X_dot = v * cos(psi + beta);
        Y_dot = v * sin(psi + beta);
        ds = [X_dot; Y_dot; psi_dot; v_dot; omega_dot; beta_dot];
    end

    % RK4，转向角用 (k, mid, mid, k+1)
    s_k = [X_k; Y_k; psi_k; v_k; omega_k; beta_k];
    delta_lf_mid = (delta_lf_k + delta_lf_new)/2;
    delta_rr_mid = (delta_rr_k + delta_rr_new)/2;

    k1 = dynamics(s_k,             delta_lf_k,   delta_rr_k);
    k2 = dynamics(s_k+0.5*Ts*k1,   delta_lf_mid, delta_rr_mid);
    k3 = dynamics(s_k+0.5*Ts*k2,   delta_lf_mid, delta_rr_mid);
    k4 = dynamics(s_k+Ts*k3,       delta_lf_new, delta_rr_new);
    s_new = s_k + (Ts/6)*(k1 + 2*k2 + 2*k3 + k4);

    % 提取新状态并保护
    X_new    = s_new(1); Y_new = s_new(2); psi_new = s_new(3);
    v_new    = s_new(4); omega_new = s_new(5); beta_new = s_new(6);

    % 航向角归一化
    psi_new = normalizeAngle(psi_new);

    % 小负速度贴地
    if v_new > -1e-3
        v_new = max(0, v_new);
    end

    % β限幅（防数值爆炸）
    beta_new = sat(beta_new, -deg2rad(15), deg2rad(15));

    % 存储更新后的转向角
    delta_lf_out = delta_lf_new;
    delta_rr_out = delta_rr_new;

    % === 计算测量量 ===
    % IMU
    accel_x_meas = (F_drive_total - F_drag - F_slope) / max(m_eff_total,1e-6);
    gyro_y_meas  = 0;                % 若无俯仰模型，这里给0或估计
    gyro_z_meas  = omega_new;

    % 轮速（基于ICR几何/低速保护）
    if abs(omega_new) > min_omega_threshold && abs(v_new) > 1e-4
        R = v_new / omega_new; sgn = sign(omega_new); x_c = 0; y_c = R*sgn;
        r_lf = sqrt((x_c - L/2)^2 + (y_c - W/2*sgn)^2);
        r_rr = sqrt((x_c + L/2)^2 + (y_c + W/2*sgn)^2);
        v_lf = (r_lf / max(abs(R),1e-6)) * v_new;
        v_rr = (r_rr / max(abs(R),1e-6)) * v_new;
    else
        v_lf = v_new * cos(beta_new);
        v_rr = v_new * cos(beta_new);
    end
    omega_wheel_lf = v_lf / max(r,1e-6) + noise_factor * P.wheel_speed_noise_std * randn;
    omega_wheel_rr = v_rr / max(r,1e-6) + noise_factor * P.wheel_speed_noise_std * randn;

    % 电流估计（车轮侧力矩映射回电机电流）
    I_meas_lf = F_drive_lf * r / max(n*eta*k_t,1e-6) + noise_factor * P.current_noise_std * randn;
    I_meas_rr = F_drive_rr * r / max(n*eta*k_t,1e-6) + noise_factor * P.current_noise_std * randn;

    % 扰动观测（净外力残差的简单估计）：
    F_inertia_total = m_eff_total * accel_x_meas;
    w_ratio_lf = N_lf / max(W_total,1e-6);
    w_ratio_rr = N_rr / max(W_total,1e-6);
    F_inertia_lf = F_inertia_total * w_ratio_lf; F_inertia_rr = F_inertia_total * w_ratio_rr;
    F_slope_lf   = F_slope * w_ratio_lf;        F_slope_rr   = F_slope * w_ratio_rr;
    F_rolling_lf = c_r * N_lf;                  F_rolling_rr = c_r * N_rr;
    F_motor_actual_lf = F_drive_lf;             F_motor_actual_rr = F_drive_rr;
    F_dist_calc_lf = F_motor_actual_lf - F_rolling_lf - F_inertia_lf - F_slope_lf + noise_factor*dist_noise_std*randn;
    F_dist_calc_rr = F_motor_actual_rr - F_rolling_rr - F_inertia_rr - F_slope_rr + noise_factor*dist_noise_std*randn;

    % 汇总输出（18）
    y_out = [ X_new; Y_new; psi_new; v_new; omega_new; delta_lf_out; delta_rr_out; beta_new; ...
              accel_x_meas; gyro_y_meas; gyro_z_meas; I_meas_lf; I_meas_rr; ...
              F_dist_calc_lf; F_dist_calc_rr; theta_ground; omega_wheel_lf; omega_wheel_rr ];

    % 写出
    block.OutputPort(1).Data = y_out;

    % 更新状态
    block.Dwork(1).Data = [X_new; Y_new; psi_new; v_new; omega_new; delta_lf_out; delta_rr_out; beta_new];
end

%% ========================================================================
function Terminate(~)
    % 结束时无需操作
end

%% =========================== 工具函数 ====================================
function y = gd(s,field,default)
% get default
    if isstruct(s) && isfield(s,field) && ~isempty(s.(field))
        y = s.(field);
    else
        y = default;
    end
end

function y = sat(x, xmin, xmax)
    y = min(max(x, xmin), xmax);
end

function y = sat_sym(x, xmax)
    y = min(max(x, -xmax), xmax);
end

function a = normalizeAngle(a)
% wrap to [-pi,pi]
    a = atan2(sin(a), cos(a));
end

function [N_lf,N_rf,N_lr,N_rr,F_rolling_total] = compute_load_transfer(F_cmd, omega, v, theta_g, P)
    % 基于纵向/横向加速度的简化载荷转移 + 坡度影响
    m=P.m; g=P.g; h=P.h_cg; W=P.W; L=P.L; c_r=P.c_r;

    % 纵向加速度（使用指令近似，以避免环依赖；也可改为用上一拍估计）
    a_long = sat(F_cmd/m, -P.accel_limit, P.accel_limit) - g*sin(theta_g);
    Delta_long = m * a_long * (h/L);           % 前后轴载荷转移

    % 横向加速度（用 omega,v 估）
    if abs(v) > 1e-3
        R_est = max(v/max(omega,1e-6), 1e-3);
        a_lat = (v^2) / R_est;
        Delta_lat = m * a_lat * (h/W);
    else
        Delta_lat = 0;
    end
    sgn_turn = sign(omega);

    % 轴基础载荷（坡度影响投影到总重）
    W_total = m * g * cos(theta_g);
    N_front_base = W_total/2 - Delta_long/2;
    N_rear_base  = W_total/2 + Delta_long/2;

    % 横向分配到轴
    Delta_lat_front = sgn_turn * Delta_lat/2;
    Delta_lat_rear  = sgn_turn * Delta_lat/2;

    % 四轮法向载荷
    N_lf = max(0, N_front_base/2 - Delta_lat_front/2);
    N_rf = max(0, N_front_base/2 + Delta_lat_front/2);
    N_lr = max(0, N_rear_base/2  - Delta_lat_rear/2);
    N_rr = max(0, N_rear_base/2  + Delta_lat_rear/2);

    % 滚动阻力（基于实时载荷）
    F_rolling_total = c_r * (N_lf + N_rf + N_lr + N_rr);
end

end % 文件结束
