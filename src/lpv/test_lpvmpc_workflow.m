% =============================
% 文件名：test_lpvmpc_workflow.m
% 版本号：V1.0
% 最后修改时间：2025-10-03
% 作者：Auto-generated
% 功能描述：
%   LPV-MPC完整工作流程测试脚本
%   演示从线性化、MPC创建到在线更新的完整流程
% 依赖：
%   - parameters.m
%   - lin_agv_grid.m
%   - mpc_setup_single_interp.m
%   - mpc_update_from_rho.m
% 备注：
%   - 此脚本用于验证工作流程的正确性
%   - 实际使用时可根据需求调整网格密度和参数
% =============================

clear; clc; close all;

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
if ~exist(data_models_dir, 'dir')
    mkdir(data_models_dir);
end

fprintf('========================================\n');
fprintf('  LPV-MPC 完整工作流程测试\n');
fprintf('========================================\n\n');

%% 第1步：加载参数
fprintf('【步骤1/5】加载参数...\n');
params = parameters();
fprintf('  采样周期 Ts = %.3f s\n', params.Ts);
fprintf('  车辆质量 m = %.1f kg\n', params.mass);
fprintf('  轴距 L = %.2f m\n\n', params.L);

%% 第2步：定义线性化网格
fprintf('【步骤2/5】定义线性化网格...\n');

% 网格定义（5×5×5密集网格，共125点）
grid = struct();
grid.V_grid = linspace(0.8, 1.2, 5)';    % 速度 [m/s]，5个点
grid.W_grid = linspace(-0.2, 0.2, 5)';   % 角速度（有符号）[rad/s]，5个点
grid.T_grid = linspace(-0.2, 0.2, 5)';   % 坡度角 [rad]，5个点

fprintf('  速度网格: [%.2f → %.2f] m/s，%d点\n', grid.V_grid(1), grid.V_grid(end), length(grid.V_grid));
fprintf('  角速度网格: [%.3f → %.3f] rad/s（有符号），%d点\n', grid.W_grid(1), grid.W_grid(end), length(grid.W_grid));
fprintf('  坡度网格: [%.2f° → %.2f°]，%d点\n', rad2deg(grid.T_grid(1)), rad2deg(grid.T_grid(end)), length(grid.T_grid));
fprintf('  总网格点数: %d × %d × %d = %d\n\n', length(grid.V_grid), length(grid.W_grid), length(grid.T_grid), ...
    length(grid.V_grid) * length(grid.W_grid) * length(grid.T_grid));

%% 第3步：执行网格线性化
fprintf('【步骤3/5】执行网格线性化...\n');

% 线性化选项
lin_opts = struct();
lin_opts.coord = 'path';
lin_opts.disc = 'zoh';
lin_opts.keep_E = true;
lin_opts.export_mat = fullfile(data_models_dir, 'plant_grid_test.mat');

% 执行线性化
try
    db = lin_agv_grid(params, grid, lin_opts);
    fprintf('  线性化完成！\n');
    fprintf('  数据库维度: A(%d×%d×%d×%d×%d)\n', ...
        db.Nv, db.Nw, db.Nt, db.nx, db.nx);
    fprintf('  不稳定点数: %d / %d\n\n', db.meta.unstable_count, db.Nv*db.Nw*db.Nt);
    
    % 保存 db 到 lin_agv_db.mat（用于贝叶斯优化等后续流程）
    lin_db_path = fullfile(data_models_dir, 'lin_agv_db.mat');
    fprintf('  保存数据库到 %s...\n', lin_db_path);
    save(lin_db_path, 'db');
    file_info = dir(lin_db_path);
    fprintf('  √ 已保存 (%.2f MB, Ts=%.3fs)\n\n', file_info.bytes/1e6, db.Ts);
    
catch ME
    fprintf('  错误: 线性化失败\n');
    fprintf('  %s\n\n', ME.message);
    return;
end

%% 第4步：创建MPC控制器
fprintf('【步骤4/5】创建MPC控制器...\n');

% MPC设计选项
mpc_opts = struct();
mpc_opts.Np = 50;  % 预测时域（步数）
mpc_opts.Nc = 12;  % 控制时域（步数）
mpc_opts.Q = [15.1924, 28.2259, 5.0984, 2.5793];  % 输出权重 [e_y, e_psi, e_v, e_omega]
mpc_opts.R = [0.001837, 0.002424];  % 输入权重 [F_cmd, omega_cmd]
mpc_opts.dR = [0.028222, 0.023107]; % 输入变化率权重
mpc_opts.soft_weight_pos = 1e4;  % 位置误差软约束惩罚
mpc_opts.soft_weight_yaw = 1.5e4; % 航向误差软约束惩罚（更重要）

try
    ctrl = mpc_setup_single_interp(db, mpc_opts);
    % Hook: print average solver time if available from base workspace
    avg_ms = NaN;
    try
        if evalin('base','exist(''mpc_avg_solve_time_ms'',''var'')')
            avg_ms = evalin('base','mpc_avg_solve_time_ms');
        elseif evalin('base','exist(''mpc_solve_times'',''var'')')
            st = evalin('base','mpc_solve_times');
            if ~isempty(st), avg_ms = 1e3*mean(st); end
        end
    catch
    end
    fprintf('  ƽ����⹤����(��): %.3f ms\n', avg_ms);
    fprintf('  MPC控制器创建完成！\n');
    fprintf('  预测时域: %.2f s\n', ctrl.meta.prediction_horizon_sec);
    fprintf('  控制时域: %.2f s\n\n', ctrl.meta.control_horizon_sec);
catch ME
    fprintf('  错误: MPC创建失败\n');
    fprintf('  %s\n\n', ME.message);
    return;
end

%% 第5步：测试在线模型更新
fprintf('【步骤5/5】测试在线模型更新...\n');

% 测试不同的调度变量点（omega保留符号）
test_rhos = [
    1.0,  0.0,   0.0;   % 直线匀速
    1.0,  0.1,   0.0;   % 左转弯
    1.0, -0.1,   0.0;   % 右转弯
    0.9,  0.15,  0.05;  % 转弯+上坡
    1.1, -0.05, -0.03   % 右转+下坡
];

fprintf('  测试%d个工况点:\n', size(test_rhos, 1));
for i = 1:size(test_rhos, 1)
    rho = test_rhos(i, :)';
    
    try
        upd = mpc_update_from_rho(rho, db, ctrl.maps);
        
        fprintf('  [%d] ρ=[%.2f, %+.3f, %+.2f°] → ', i, rho(1), rho(2), rad2deg(rho(3)));
        fprintf('rho_n=[%.3f, %.3f, %.3f], ', upd.rho_n(1), upd.rho_n(2), upd.rho_n(3));
        fprintf('max|eig(A)|=%.3f\n', max(abs(eig(upd.A))));
        
    catch ME
        fprintf('  [%d] 错误: %s\n', i, ME.message);
    end
end

fprintf('\n');

%% 左右转对称性检查
fprintf('【对称性检查】左转 vs 右转的模型差异\n');
try
    updL = mpc_update_from_rho([1.0; +0.1; 0.0], db, ctrl.maps);  % 左转
    updR = mpc_update_from_rho([1.0; -0.1; 0.0], db, ctrl.maps);  % 右转
    
    A_diff_norm = norm(updL.A - updR.A, 'fro');
    B_diff_norm = norm(updL.B - updR.B, 'fro');
    
    fprintf('  ‖A(+ω) - A(-ω)‖_F = %.3e\n', A_diff_norm);
    fprintf('  ‖B(+ω) - B(-ω)‖_F = %.3e\n', B_diff_norm);
    
    if A_diff_norm < 1e-10 && B_diff_norm < 1e-10
        fprintf('  ⚠️ 模型完全对称（可能未正确使用有符号ω）\n');
    else
        fprintf('  ✓ 模型正确区分左右转（有符号ω生效）\n');
    end
    
catch ME
    fprintf('  对称性检查失败: %s\n', ME.message);
end

fprintf('\n');

%% 第6步：可视化基准模型极点分布（可选）
fprintf('【可视化】基准模型极点分布\n');

i_center = ceil(db.Nv / 2);
j_center = ceil(db.Nw / 2);
k_center = ceil(db.Nt / 2);
A_center = squeeze(db.A(i_center, j_center, k_center, :, :));

eigs_center = eig(A_center);

figure('Name', 'LPV-MPC基准模型极点分布', 'NumberTitle', 'off');
plot(real(eigs_center), imag(eigs_center), 'bx', 'MarkerSize', 10, 'LineWidth', 2);
hold on;
theta = linspace(0, 2*pi, 100);
plot(cos(theta), sin(theta), 'r--', 'LineWidth', 1.5);
grid on;
xlabel('Real');
ylabel('Imaginary');
title('基准工作点离散系统极点分布');
legend('极点', '单位圆', 'Location', 'best');
axis equal;
xlim([-1.5, 1.5]);
ylim([-1.5, 1.5]);

tol_unstable = 1e-6;
maxmod = max(abs(eigs_center));
fprintf('  最大极点模: %.6f\n', maxmod);
if maxmod > 1.0 + tol_unstable
    fprintf('  ✗ 系统不稳定（存在极点在单位圆外）\n');
elseif abs(maxmod - 1.0) <= tol_unstable
    fprintf('  ○ 边界稳定（含积分器/保持极点在 z=1）\n');
else
    fprintf('  ✓ 系统稳定（所有极点在单位圆内）\n');
end

%% 总结
fprintf('\n========================================\n');
fprintf('  工作流程测试完成！\n');
fprintf('========================================\n');
fprintf('生成的文件:\n');
fprintf('  - plant_grid_test.mat (LPV模型数据库)\n');
fprintf('\n使用说明:\n');
fprintf('  1. 在 Simulink 中使用 Adaptive MPC 块\n');
fprintf('  2. 设置"自定义模型更新函数"调用 mpc_update_from_rho\n');
fprintf('  3. 输入调度变量 rho = [v; omega; theta]（注意：omega有符号）\n');
fprintf('  4. MPC将自动插值更新预测模型（三线性插值）\n');
fprintf('\n下一步:\n');
fprintf('  - 调整网格密度以提高精度\n');
fprintf('  - 使用贝叶斯优化调整权重\n');
fprintf('  - 集成到完整的Simulink仿真\n');
fprintf('========================================\n');

