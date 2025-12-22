% =============================
% 文件名：start_bayesian.m
% 版本号：V1.2
% 最后修改时间：2025-11-04
% 功能描述：启动贝叶斯优化并显示详细结果
% 更新记录：
%   V1.2 - 添加第二阶段评估次数配置，修复全局最优丢失问题
% =============================

clear; clc;

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');

fprintf('========================================\n');
fprintf('  贝叶斯优化 MPC 参数调优\n');
fprintf('========================================\n\n');

%% 1. 加载参数
fprintf('【步骤1/4】加载参数...\n');
params = parameters();
fprintf('  ✓ 采样周期: %.3f s\n', params.Ts);
fprintf('  ✓ 车辆质量: %.1f kg\n\n', params.mass);

%% 2. 加载 db（从 lin_agv_db.mat）
fprintf('【步骤2/4】加载 LPV 数据库...\n');
db_file = fullfile(data_models_dir, 'lin_agv_db.mat');
S = load(db_file, 'db');
db = S.db;
fprintf('  ✓ 网格尺寸: %d×%d×%d = %d 点\n', db.Nv, db.Nw, db.Nt, db.Nv*db.Nw*db.Nt);
fprintf('  ✓ 速度范围: [%.2f, %.2f] m/s\n', db.grid.V(1), db.grid.V(end));
fprintf('  ✓ 角速度范围: [%.3f, %.3f] rad/s\n\n', db.grid.W(1), db.grid.W(end));

%% 3. 配置 options
fprintf('【步骤3/4】配置优化选项...\n');
options = struct();

% 第一阶段（全局搜索）评估次数
options.MaxObjectiveEvaluations = 500;  % 推荐：60-200（快速测试可设为10-30）

% 第二阶段（局部精细搜索）配置
% 如果不配置，默认使用 30% * MaxObjectiveEvaluations（最小10，最大30）
options.local_refine.enable = true;        % 是否启用第二阶段（默认：true）
options.local_refine.num_evals = 200;      % 第二阶段评估次数（可自定义）
% 其他可选参数（通常不需要修改）：
% options.local_refine.shrink = 0.35;     % 局部搜索范围（相对全局）
% options.local_refine.num_seeds = 8;     % 随机种子点数量
% options.local_refine.jitter = 0.08;     % 抖动幅度

% 其他选项
options.save_history = true;              % 保存历史记录（true/false）

fprintf('  ✓ 第一阶段评估次数: %d\n', options.MaxObjectiveEvaluations);
fprintf('  ✓ 第二阶段评估次数: %d\n', options.local_refine.num_evals);
fprintf('  ✓ 保存历史: %s\n\n', mat2str(options.save_history));

%% 4. 执行优化
fprintf('【步骤4/4】开始优化...\n');
fprintf('========================================\n\n');

tic;
[best, boResults] = Bayesian_Optimization(params, db, options);
elapsed_time = toc;

%% 5. 显示详细结果
fprintf('\n\n');
fprintf('╔════════════════════════════════════════╗\n');
fprintf('║       贝叶斯优化结果详细报告           ║\n');
fprintf('╚════════════════════════════════════════╝\n\n');

% ===== 迭代信息 =====
fprintf('【1. 迭代信息】\n');
fprintf('  总迭代次数: %d / %d\n', boResults.NumObjectiveEvaluations, ...
    options.MaxObjectiveEvaluations);
% 使用实际测量的总时间（最准确）
if elapsed_time > 0
    fprintf('  总耗时: %.2f 分钟 (%.1f 秒/次)\n', elapsed_time/60, ...
        elapsed_time/boResults.NumObjectiveEvaluations);
else
    % 备用：从 boResults.TotalElapsedTime 获取（如果有）
    if isprop(boResults, 'TotalElapsedTime') || isfield(boResults, 'TotalElapsedTime')
        total_time = boResults.TotalElapsedTime;
    else
        total_time = sum(table2array(boResults.UserDataTrace(:, end))); % 最后一列通常是时间
    end
    fprintf('  总耗时: %.2f 分钟 (%.1f 秒/次)\n', total_time/60, ...
        total_time/boResults.NumObjectiveEvaluations);
end

% 停止原因分析
if boResults.NumObjectiveEvaluations >= options.MaxObjectiveEvaluations
    fprintf('  停止原因: 达到最大评估次数限制\n');
elseif isfield(boResults, 'IterationTimeTrace') && ...
       length(boResults.IterationTimeTrace) < options.MaxObjectiveEvaluations
    fprintf('  停止原因: 提前收敛或满足终止条件\n');
else
    fprintf('  停止原因: 优化正常完成\n');
end
fprintf('\n');

% ===== 最优结果 =====
fprintf('【2. 最优结果】\n');
fprintf('  最优代价 J_min: %.6f\n', best.J);
fprintf('  失败场景数: %d\n', best.report.fail_count);

% 获取最优点参数
bestPoint = boResults.XAtMinObjective;
fprintf('\n  最优参数组合:\n');
fprintf('    权重 Q:\n');
fprintf('      q_y     = %.4f\n', bestPoint.q_y);
fprintf('      q_psi   = %.4f\n', bestPoint.q_psi);
fprintf('      q_v     = %.4f\n', bestPoint.q_v);
fprintf('      q_omega = %.4f\n', bestPoint.q_omega);
fprintf('    权重 R:\n');
fprintf('      r_F     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_r_F, bestPoint.log10_r_F);
fprintf('      r_omega = %.6f (log10: %.2f)\n', 10^bestPoint.log10_r_omega, bestPoint.log10_r_omega);
fprintf('    权重 dR:\n');
fprintf('      rdF     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_rdF, bestPoint.log10_rdF);
fprintf('      rdw     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_rdw, bestPoint.log10_rdw);
fprintf('    形状参数（自动修正为 alpha <= beta）:\n');
% 显示修正后的值（与实际使用的一致）
alpha_Q_corrected = min(bestPoint.alpha_Q, bestPoint.beta_Q);
beta_Q_corrected = max(bestPoint.alpha_Q, bestPoint.beta_Q);
alpha_R_corrected = min(bestPoint.alpha_R, bestPoint.beta_R);
beta_R_corrected = max(bestPoint.alpha_R, bestPoint.beta_R);
alpha_dR_corrected = min(bestPoint.alpha_dR, bestPoint.beta_dR);
beta_dR_corrected = max(bestPoint.alpha_dR, bestPoint.beta_dR);
fprintf('      alpha_Q = %.3f,  beta_Q  = %.3f\n', alpha_Q_corrected, beta_Q_corrected);
fprintf('      alpha_R = %.3f,  beta_R  = %.3f\n', alpha_R_corrected, beta_R_corrected);
fprintf('      alpha_dR= %.3f,  beta_dR = %.3f\n', alpha_dR_corrected, beta_dR_corrected);
fprintf('    约束缩放:\n');
fprintf('      scale_umin: lo=%.3f, hi=%.3f\n', bestPoint.scale_umin_lo, bestPoint.scale_umin_hi);
fprintf('      scale_umax: lo=%.3f, hi=%.3f\n', bestPoint.scale_umax_lo, bestPoint.scale_umax_hi);
fprintf('    滤波时间:\n');
fprintf('      tau = %.3f s\n', bestPoint.tau);
fprintf('    场景自适应参数（方案B+C）:\n');
fprintf('      [转弯场景 - 方案B]\n');
fprintf('        omega_threshold = %.4f rad/s\n', bestPoint.omega_threshold);
fprintf('        transition_width = %.4f rad/s\n', bestPoint.transition_width);
fprintf('        q_y_gain_max = %.3f\n', bestPoint.q_y_gain_max);
fprintf('      [坡度场景 - 方案C]\n');
fprintf('        theta_threshold = %.4f rad (%.2f°)\n', bestPoint.theta_threshold, rad2deg(bestPoint.theta_threshold));
fprintf('        theta_transition_width = %.4f rad (%.2f°)\n', bestPoint.theta_transition_width, rad2deg(bestPoint.theta_transition_width));
fprintf('        q_v_gain_max = %.3f\n', bestPoint.q_v_gain_max);
fprintf('        R_F_gain_max: uphill=%.3f, downhill=%.3f\n', bestPoint.R_F_gain_max_uphill, bestPoint.R_F_gain_max_downhill);
fprintf('        dR_F_gain_max: uphill=%.3f, downhill=%.3f\n', bestPoint.dR_F_gain_max_uphill, bestPoint.dR_F_gain_max_downhill);
fprintf('\n');

% ===== 各场景性能 =====
fprintf('【3. 各场景性能】\n');
scene_names = fieldnames(best.report.scene);
for i = 1:length(scene_names)
    scene = scene_names{i};
    if isfield(best.report.scene.(scene), 'RMSE')
        rep = best.report.scene.(scene);
        fprintf('  场景: %s\n', scene);
        fprintf('    RMSE(e_y)    = %.4f m\n', rep.RMSE.ey);
        fprintf('    RMSE(e_psi)  = %.4f rad (%.2f°)\n', rep.RMSE.epsi, rad2deg(rep.RMSE.epsi));
        fprintf('    RMSE(e_v)    = %.4f m/s\n', rep.RMSE.ev);
        fprintf('    RMSE(e_omega)= %.4f rad/s\n', rep.RMSE.eomega);
        fprintf('    求解时间: avg=%.2f ms, max=%.2f ms\n', ...
            rep.solve_ms.avg, rep.solve_ms.max);
        fprintf('    约束违反: L1=%.4f, Linf=%.4f\n', rep.cons.L1, rep.cons.Linf);
        if rep.failed
            fprintf('    状态: 失败 ❌\n');
        else
            fprintf('    状态: 成功 ✓\n');
        end
        fprintf('\n');
    end
end

% ===== 优化历史统计 =====
fprintf('【4. 优化历史统计】\n');
all_objectives = boResults.ObjectiveTrace;
fprintf('  最小代价: %.6f\n', min(all_objectives));
fprintf('  最大代价: %.6f\n', max(all_objectives));
fprintf('  平均代价: %.6f\n', mean(all_objectives));
fprintf('  中位数: %.6f\n', median(all_objectives));
fprintf('  标准差: %.6f\n', std(all_objectives));

% 改进分析
first_obj = all_objectives(1);
best_obj = min(all_objectives);
improvement = (first_obj - best_obj) / first_obj * 100;
fprintf('  相对改进: %.2f%%\n', improvement);
fprintf('\n');

% ===== 推荐的下一步行动 =====
fprintf('【5. 建议】\n');
if best.report.fail_count > 0
    fprintf('  ⚠ 存在失败场景，建议:\n');
    fprintf('    - 检查失败场景的参数配置\n');
    fprintf('    - 放宽输出约束或增加软约束权重\n');
    fprintf('    - 增加评估次数继续优化\n');
elseif max(all_objectives) - min(all_objectives) > 0.1 * min(all_objectives)
    fprintf('  ℹ 优化空间较大，建议:\n');
    fprintf('    - 增加评估次数 (当前: %d)\n', options.MaxObjectiveEvaluations);
    fprintf('    - 在当前最优点附近精细搜索\n');
else
    fprintf('  ✓ 优化效果良好！\n');
    fprintf('    - 可以直接使用 maps_best.mat\n');
    fprintf('    - 建议在 Simulink 中验证性能\n');
end
fprintf('\n');

% ===== 产物文件 =====
fprintf('【6. 产物文件】\n');
fprintf('  ✓ maps_best.mat (根目录)\n');
if options.save_history
    fprintf('  ✓ bo_history_<timestamp>.mat (根目录)\n');
end
fprintf('\n');

fprintf('╔════════════════════════════════════════╗\n');
fprintf('║           优化流程完成！               ║\n');
fprintf('╚════════════════════════════════════════╝\n');


