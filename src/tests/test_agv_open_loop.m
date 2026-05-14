% =============================
% 文件名：test_agv_open_loop.m
% 功能描述：开环验证 AGV 物理模型在不同参数下的响应 (优化版)
% 修改说明：
%   1. 加入空气阻力到理论计算
%   2. 转向测试中施加维持速度的前馈力，避免速度衰减
%   3. 提高加速度计算的数值稳定性
% =============================

clc; clear;
fprintf('=== AGV 模型开环物理验证脚本 (V2.0 优化版) ===\n');

%% 加载参数
params = parameters();
Ts = params.Ts;
m = params.mass;
g = params.gravity;
c_r = params.rolling_resistance;
rho_air = params.air_density;
CdA = params.drag_coefficient_area;

% 计算有效质量（包含电机/车轮转动惯量）
r_wheel = params.wheel_radius;
n_gear = params.gear_ratio;
Jw = params.wheel_inertia;
Jm = params.motor_inertia;
m_eff = m + 2*(Jw + Jm*n_gear^2) / r_wheel^2;

fprintf('系统参数配置:\n');
fprintf('  - 采样步长 Ts: %.3f s\n', Ts);
fprintf('  - 车辆质量 m:  %.1f kg\n', m);
fprintf('  - 有效质量 m_eff: %.2f kg\n', m_eff);

%% 测试函数定义
run_sim = @(t_end, u_fixed, theta_g, x0) simulate_core(t_end, u_fixed, theta_g, x0, params);

%% [A] 静态平衡测试
fprintf('\n[A] 静态平衡测试 (零输入)...');
t_test = 5.0;
[t, states] = run_sim(t_test, [0; 0], 0, zeros(8,1));
v_peak = max(abs(states(:, 4)));
if v_peak < 1e-4
    fprintf(' [PASS] 峰值速度漂移: %.2e m/s\n', v_peak);
else
    fprintf(' [FAIL] 峰值速度漂移: %.2e m/s\n', v_peak);
end

%% [B] 恒力加速测试
fprintf('[B] 恒力加速测试 (F_cmd=200N)...');
F_input = 200;
[t, states] = run_sim(2.0, [F_input; 0], 0, zeros(8,1));

% 计算理论平均加速度 (考虑滚阻和平均速度下的空气阻力)
v_avg = mean(states(:,4));
F_res_avg = m * g * c_r + 0.5 * rho_air * CdA * v_avg^2;
a_theory = (F_input - F_res_avg) / m_eff;

% 使用 1.0s - 2.0s 之间的平均加速度
idx = t >= 1.0;
v_range = states(idx, 4);
t_range = t(idx);
% 线性回归求斜率
p = polyfit(t_range, v_range, 1);
accel_actual = p(1);
err_pct = abs(accel_actual - a_theory) / a_theory * 100;

if err_pct < 10
    fprintf(' [PASS] 理论加速度=%.3f, 实际=%.3f, 误差=%.1f%%\n', a_theory, accel_actual, err_pct);
else
    fprintf(' [FAIL] 理论加速度=%.3f, 实际=%.3f, 误差=%.1f%%\n', a_theory, accel_actual, err_pct);
end

%% [C] 转向响应测试 (C1-C4)
% 在测试中施加平衡力，保持速度接近 v0=1m/s
v_test = 1.0;
F_bal = m*g*c_r + 0.5*rho_air*CdA*v_test^2;

test_cases = {
    'C1', '左转-低速',  0.1,  10.0;
    'C2', '左转-S弯',   0.37,  2.7;   % 原0.5→0.37 rad/s (匹配S弯)
    'C3', '右转-低速', -0.1,  10.0;
    'C4', '右转-S弯',  -0.37,  2.7;   % 原-0.5→-0.37 rad/s (匹配S弯)
    'C5', '右转-第一弯', -0.39, 2.56  % 匹配industrial路径50-54s的第一个右转 (63°/4s*1.43≈0.39)
};

for i = 1:size(test_cases, 1)
    id = test_cases{i,1};
    desc = test_cases{i,2};
    w_cmd = test_cases{i,3};
    R_theory = test_cases{i,4};
    
    fprintf('[%s] %s (ω_cmd=%+.2f rad/s)...\n', id, desc, w_cmd);
    
    x0 = zeros(8,1); x0(4) = v_test;
    [t, states] = run_sim(8.0, [F_bal; w_cmd], 0, x0);
    
    % 取最后 2 秒的均值
    final_idx = t > 6.0;
    w_actual = mean(states(final_idx, 5));
    v_actual = mean(states(final_idx, 4));
    delta_lf_actual = mean(states(final_idx, 6));
    delta_rr_actual = mean(states(final_idx, 7));
    beta_actual = mean(states(final_idx, 8));
    
    R_actual = abs(v_actual / (w_actual + eps));
    err_pct = abs(R_actual - R_theory) / R_theory * 100;
    w_tracking_ratio = w_actual / w_cmd * 100; % 角速度跟踪比 (%)
    
    % 诊断输出
    fprintf('     诊断: v=%.3f m/s, ω=%.4f rad/s (跟踪率=%.1f%%)\n', v_actual, w_actual, w_tracking_ratio);
    fprintf('           δ_lf=%.2f°, δ_rr=%.2f°, β=%.3f°\n', rad2deg(delta_lf_actual), rad2deg(delta_rr_actual), rad2deg(beta_actual));
    fprintf('           理论R=%.1fm, 实际R=%.2fm, 误差=%.1f%%\n', R_theory, R_actual, err_pct);
    
    if err_pct < 15 && sign(w_actual) == sign(w_cmd)
        fprintf('     [PASS]\n');
    else
        fprintf('     [FAIL] <- 可能原因: ');
        if abs(w_tracking_ratio) < 90
            fprintf('角速度跟踪不足\n');
        elseif abs(v_actual - v_test) > 0.1
            fprintf('速度偏离目标\n');
        else
            fprintf('需进一步分析\n');
        end
    end
end

%% [D] 坡度阻力测试
fprintf('[D] 坡度阻力测试 (theta=5 deg)...');
theta_deg = 5;
theta_rad = deg2rad(theta_deg);
x0 = zeros(8,1); x0(4) = 1.5;
[t, states] = run_sim(1.0, [0; 0], theta_rad, x0);

v_avg = mean(states(:,4));
a_theory = (-m*g*sin(theta_rad) - m*g*cos(theta_rad)*c_r - 0.5*rho_air*CdA*v_avg^2) / m_eff;

p = polyfit(t, states(:,4), 1);
accel_actual = p(1);
err_pct = abs(accel_actual - a_theory) / abs(a_theory) * 100;

if err_pct < 10
    fprintf(' [PASS] 理论减速度=%.3f, 实际=%.3f, 误差=%.1f%%\n', a_theory, accel_actual, err_pct);
else
    fprintf(' [FAIL] 理论减速度=%.3f, 实际=%.3f, 误差=%.1f%%\n', a_theory, accel_actual, err_pct);
end

%% [E] 稳态速度测试
fprintf('[E] 稳态速度测试 (平衡阻力)...');
v_target = 1.2; % 提高到 1.2m/s
F_maintain = m*g*c_r + 0.5*rho_air*CdA*v_target^2;

x0 = zeros(8,1); x0(4) = v_target;
[t, states] = run_sim(10.0, [F_maintain; 0], 0, x0);
% 使用基于时间的索引，取最后 2 秒
steady_idx = t > (t(end) - 2.0);
v_steady = mean(states(steady_idx, 4));
v_rmse = sqrt(mean((states(steady_idx,4) - v_target).^2));

if v_rmse < 0.05
    fprintf(' [PASS] 目标=%.2f, 稳态=%.2f, RMSE=%.3f m/s\n', v_target, v_steady, v_rmse);
else
    fprintf(' [FAIL] 目标=%.2f, 稳态=%.2f, RMSE=%.3f m/s\n', v_target, v_steady, v_rmse);
end

fprintf('\n所有开环验证完成。\n');

%% [F] Mamba 新增输出变量验证 (V4.3)
fprintf('\n=== [F] Mamba 新增输出变量验证 (V4.3) ===\n');
fprintf('  清除 persistent 变量...\n');
clear output_eq_ref;  % 清除 persistent 变量

% 场景 F1: 平地直行 - slip_ratio 应接近 0, gyro_y 应接近 0, accel_y 应接近 0
fprintf('[F1] 平地直行 - 验证新输出变量...\n');
x0_f1 = zeros(8,1); x0_f1(4) = 1.0;  % 初始速度 1 m/s
[t_f1, states_f1, outputs_f1] = simulate_core_with_outputs(5.0, [50; 0], 0, x0_f1, params);

slip_lf_mean = mean(outputs_f1(end-100:end, 32));
slip_rr_mean = mean(outputs_f1(end-100:end, 33));
gyro_y_mean = mean(outputs_f1(end-100:end, 10));
accel_y_mean = mean(outputs_f1(end-100:end, 34));

fprintf('    slip_ratio_lf: %.4f (期望≈0)\n', slip_lf_mean);
fprintf('    slip_ratio_rr: %.4f (期望≈0)\n', slip_rr_mean);
fprintf('    gyro_y_meas:   %.4f rad/s (期望≈0)\n', gyro_y_mean);
fprintf('    accel_y_meas:  %.4f m/s² (期望≈0)\n', accel_y_mean);

if abs(slip_lf_mean) < 0.1 && abs(slip_rr_mean) < 0.1 && abs(gyro_y_mean) < 0.05 && abs(accel_y_mean) < 0.2
    fprintf('    [PASS]\n');
else
    fprintf('    [FAIL] 某些输出超出预期范围\n');
end

% 场景 F2: 平地转弯 - accel_y 应有明显变化
fprintf('[F2] 平地转弯 - 验证横向加速度...\n');
clear output_eq_ref;
x0_f2 = zeros(8,1); x0_f2(4) = 1.0;
[t_f2, states_f2, outputs_f2] = simulate_core_with_outputs(5.0, [50; 0.2], 0, x0_f2, params);

accel_y_turn_mean = mean(abs(outputs_f2(end-100:end, 34)));
gyro_y_turn_mean = mean(abs(outputs_f2(end-100:end, 10)));

fprintf('    accel_y_meas 均值: %.4f m/s² (期望 > 0)\n', accel_y_turn_mean);
fprintf('    gyro_y_meas 均值:  %.4f rad/s (期望≈0，平地无坡度变化)\n', gyro_y_turn_mean);

if accel_y_turn_mean > 0.01
    fprintf('    [PASS] 转弯时横向加速度有响应\n');
else
    fprintf('    [FAIL] 转弯时横向加速度无明显响应\n');
end

% 场景 F3: 坡度切换 - gyro_y 应在切换时有脉冲
fprintf('[F3] 坡度切换 - 验证俯仰角速度...\n');
clear output_eq_ref;
x0_f3 = zeros(8,1); x0_f3(4) = 1.0;

% 模拟坡度切换: 前2秒平地，后3秒上坡
t_switch = 2.0;
theta_slope = deg2rad(5);
[t_f3, ~, outputs_f3] = simulate_core_with_slope_switch(5.0, [100; 0], x0_f3, params, t_switch, theta_slope);

% 找到切换时刻附近的 gyro_y 峰值
switch_idx = find(t_f3 >= t_switch, 1, 'first');
gyro_y_around_switch = outputs_f3(max(1,switch_idx-5):min(end,switch_idx+10), 10);
gyro_y_peak = max(abs(gyro_y_around_switch));
gyro_y_before = mean(abs(outputs_f3(1:switch_idx-10, 10)));
gyro_y_after = mean(abs(outputs_f3(switch_idx+50:end, 10)));

fprintf('    坡度切换前 gyro_y 均值: %.4f rad/s\n', gyro_y_before);
fprintf('    坡度切换时 gyro_y 峰值: %.4f rad/s\n', gyro_y_peak);
fprintf('    坡度切换后 gyro_y 均值: %.4f rad/s\n', gyro_y_after);

if gyro_y_peak > gyro_y_before * 5 && gyro_y_peak > 0.01
    fprintf('    [PASS] 坡度切换时 gyro_y 出现脉冲\n');
else
    fprintf('    [FAIL] 坡度切换时 gyro_y 无明显脉冲\n');
end

fprintf('\n=== Mamba 新增输出变量验证完成 ===\n');

%% [G] 极限爬坡测试 (10度坡)
fprintf('\n[G] 极限爬坡测试 (10度坡, F_cmd=600N)...\n');
theta_climb = deg2rad(10);
F_climb = 600;
x0_climb = zeros(8,1); % Still zero speed start
[t_g, states_g] = run_sim(5.0, [F_climb; 0], theta_climb, x0_climb);

v_final_g = mean(states_g(end-50:end, 4));
dist_g = states_g(end, 1); % X position

fprintf('    最终速度: %.3f m/s\n', v_final_g);
fprintf('    爬升距离: %.3f m\n', dist_g);

% 判定: 速度 > 0.1 m/s (能爬上去)
if v_final_g > 0.1
    fprintf('    [PASS] 车辆成功爬上 10 度坡\n');
else
    fprintf('    [FAIL] 车辆爬坡失败 (速度不足)\n');
end

%% 核心仿真循环函数
function [t_vec, x_history] = simulate_core(t_end, u_fixed, theta_g, x0, params)
    Ts = params.Ts;
    N = round(t_end / Ts);
    t_vec = (0:Ts:N*Ts)';
    x_history = zeros(N+1, 8);
    x_history(1, :) = x0';
    
    xk = x0;
    for k = 1:N
        xk = state_eq_ref(xk, u_fixed, theta_g, params);
        x_history(k+1, :) = xk';
    end
end

%% 核心仿真循环函数 (含输出采集)
function [t_vec, x_history, y_history] = simulate_core_with_outputs(t_end, u_fixed, theta_g, x0, params)
    Ts = params.Ts;
    N = round(t_end / Ts);
    t_vec = (0:Ts:N*Ts)';
    x_history = zeros(N+1, 8);
    y_history = zeros(N+1, 34);  % V4.3: 34 维输出
    x_history(1, :) = x0';
    y_history(1, :) = output_eq_ref(x0, u_fixed, theta_g, params)';
    
    xk = x0;
    for k = 1:N
        xk = state_eq_ref(xk, u_fixed, theta_g, params);
        yk = output_eq_ref(xk, u_fixed, theta_g, params);
        x_history(k+1, :) = xk';
        y_history(k+1, :) = yk';
    end
end

%% 坡度切换仿真函数
function [t_vec, x_history, y_history] = simulate_core_with_slope_switch(t_end, u_fixed, x0, params, t_switch, theta_after)
    Ts = params.Ts;
    N = round(t_end / Ts);
    t_vec = (0:Ts:N*Ts)';
    x_history = zeros(N+1, 8);
    y_history = zeros(N+1, 34);
    x_history(1, :) = x0';
    
    xk = x0;
    for k = 1:N
        t_current = (k-1) * Ts;
        if t_current < t_switch
            theta_g = 0;
        else
            theta_g = theta_after;
        end
        
        xk = state_eq_ref(xk, u_fixed, theta_g, params);
        yk = output_eq_ref(xk, u_fixed, theta_g, params);
        x_history(k+1, :) = xk';
        y_history(k+1, :) = yk';
    end
end

