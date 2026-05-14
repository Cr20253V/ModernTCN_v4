% =============================
% 文件名：start_bayesian.m
% 版本号：V2.0 (分阶段优化)
% 最后修改时间：2026-01-14
% 功能描述：启动分阶段贝叶斯优化
%
% 分阶段策略说明：
%   Phase 1: 只优化 Q, R, dR 共8个核心变量（夯实基础）
%   Phase 2: 固定核心权重，只优化4个场景自适应变量（场景攻坚）
%
% 使用方法：
%   1. 直接运行此脚本（默认执行Phase 1）
%   2. Phase 1完成后，设置 RUN_PHASE = 2 再次运行
% =============================

clear; clc;
clear objective_wrapper;  % 强制清除 persistent base_ctrl，防止参数陈旧

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');
results_dir = fullfile(root, 'results', 'bo_results');
if ~exist(results_dir, 'dir'), mkdir(results_dir); end

%% ========== 配置区 ==========
% 选择运行的阶段 (1 或 2)
RUN_PHASE = 2;  % <- 修改这里选择阶段

% === 通用配置 ===
USE_PARALLEL = true;         % 是否启用并行计算（需先执行 parpool）
% parpool('local');           % 取消注释以启动并行池（或手动在命令行执行）
LOCAL_REFINE_EVALS = 20;     % 局部优化评估次数（手动指定，0=自动按30%计算）

% Phase 1 配置（核心权重优化）
phase1_config = struct();
phase1_config.MaxObjectiveEvaluations = 150;  % 推荐：80-150
phase1_config.scenes = struct(...
    'startup',0.00, ...       % 忽略启动区
    'golden_test',0.10, ...   % 直道（易优化，低权重）
    'pure_turn',0.35, ...     % 重点：纯转弯
    'pure_slope',0.30, ...    % 坡度是 q_v/r_F 关键约束（从0.25提升补回）
    'composite',0.25, ...     % 复合区（从0.20提升补回）
    'closure',0.00);          % 闭环段：Phase1宽搜索时极易失败，交由Phase2处理

% Phase 2 配置（场景自适应优化）
phase2_config = struct();
phase2_config.MaxObjectiveEvaluations = 80;   % 推荐：40-80
phase2_config.scenes = struct(...
    'startup',0.00, ...
    'golden_test',0.05, ...   % 原 0.10，降低
    'pure_turn',0.20, ...     % 不变
    'pure_slope',0.35, ...    % 补回：+0.05（原0.30）
    'composite',0.40, ...     % 补回：+0.10（原0.30）
    'closure',0.00);          % 闭环段：宽搜索时仍极易失败（0.15×1e6=1.5e5），置零
% ==============================

fprintf('╔════════════════════════════════════════╗\n');
fprintf('║   分阶段贝叶斯优化 MPC 参数调优        ║\n');
fprintf('╚════════════════════════════════════════╝\n\n');

%% 1. 加载参数
fprintf('【步骤1/4】加载参数...\n');
params = parameters();
fprintf('  ✓ 采样周期: %.3f s\n', params.Ts);
fprintf('  ✓ 车辆质量: %.1f kg\n\n', params.mass);

% 若存在自动粗调结果，则覆盖关键动力学参数作为 BO 初始值
auto_tune_file = fullfile(data_models_dir, 'auto_tuned_params.mat');
if exist(auto_tune_file, 'file')
    try
        S_auto = load(auto_tune_file, 'best');
        if isfield(S_auto, 'best') && isfield(S_auto.best, 'params')
            p_best = S_auto.best.params;
            % 仅覆盖与粗调相关的字段，避免污染其他设置
            if isfield(p_best, 'friction_coefficient'), params.friction_coefficient = p_best.friction_coefficient; end
            if isfield(p_best, 'steering_time_constant'), params.steering_time_constant = p_best.steering_time_constant; end
            if isfield(p_best, 'max_steering_rate'), params.max_steering_rate = p_best.max_steering_rate; end
            if isfield(p_best, 'omega_cmd_geom_kv2'), params.omega_cmd_geom_kv2 = p_best.omega_cmd_geom_kv2; end
            if isfield(p_best, 'omega_cmd_geom_omega_scale'), params.omega_cmd_geom_omega_scale = p_best.omega_cmd_geom_omega_scale; end

            fprintf('  ✓ 已加载自动粗调参数: %s\n', auto_tune_file);
        end
    catch
        fprintf('  ⚠ 自动粗调参数加载失败，继续使用默认参数。\n');
    end
end

%% 2. 加载 db（从 lin_agv_db.mat）
fprintf('【步骤2/4】加载 LPV 数据库...\n');
db_file = fullfile(data_models_dir, 'lin_agv_db.mat');
S = load(db_file, 'db');
db = S.db;
fprintf('  ✓ 网格尺寸: %d×%d×%d = %d 点\n', db.Nv, db.Nw, db.Nt, db.Nv*db.Nw*db.Nt);
fprintf('  ✓ 速度范围: [%.2f, %.2f] m/s\n', db.grid.V(1), db.grid.V(end));
fprintf('  ✓ 角速度范围: [%.3f, %.3f] rad/s\n\n', db.grid.W(1), db.grid.W(end));

%% 3. 配置 options
fprintf('【步骤3/4】配置优化选项 (Phase %d)...\n', RUN_PHASE);
options = struct();
options.phase = RUN_PHASE;
options.save_history = true;
options.UseParallel = USE_PARALLEL;               % 并行计算开关
options.local_refine_evals = LOCAL_REFINE_EVALS;  % 局部优化次数

% [更新] 使用新的目标路径（industrial_lite）
options.path_file = fullfile(root, 'data', 'paths', 'path_industrial_lite.mat');

% [更新] 优先从路径文件自动读取分区，避免脚本内硬编码时间段过时
if exist(options.path_file, 'file')
    S_ref = load(options.path_file, 'ref');
    if isfield(S_ref, 'ref') && isfield(S_ref.ref, 'meta') && isfield(S_ref.ref.meta, 'zones')
        options.zones = S_ref.ref.meta.zones;
        fprintf('  ✓ 已从 ref.meta.zones 自动加载时间分区\n');
    else
        warning('路径文件缺少 ref.meta.zones，使用默认150s分区。');
        options.zones = struct(...
            'startup',      [0, 10], ...
            'golden_test',  [10, 50], ...
            'pure_turn',    [50, 72], ...
            'pure_slope',   [72, 92], ...
            'composite',    [92, 112], ...
            'closure',      [112, 150]);
    end
else
    warning('未找到路径文件 %s，使用默认150s分区。', options.path_file);
    options.zones = struct(...
        'startup',      [0, 10], ...
        'golden_test',  [10, 50], ...
        'pure_turn',    [50, 72], ...
        'pure_slope',   [72, 92], ...
        'composite',    [92, 112], ...
        'closure',      [112, 150]);
end

switch RUN_PHASE
    case 1
        % ===== Phase 1: 核心权重优化 =====
        options.MaxObjectiveEvaluations = phase1_config.MaxObjectiveEvaluations;
        options.scenes = phase1_config.scenes;
        fprintf('  Phase 1: 核心权重优化 (8个变量)\n');
        fprintf('  ✓ 场景权重: golden=%.2f, turn=%.2f, slope=%.2f, composite=%.2f\n', ...
            options.scenes.golden_test, options.scenes.pure_turn, ...
            options.scenes.pure_slope, options.scenes.composite);
        
    case 2
        % ===== Phase 2: 场景自适应优化 =====
        % 需要加载Phase 1结果
        phase1_file = fullfile(results_dir, 'phase1_best.mat');
        if ~exist(phase1_file, 'file')
            error('未找到Phase 1结果！请先运行Phase 1。\n  期望文件: %s', phase1_file);
        end
        S_p1 = load(phase1_file, 'best', 'bestPoint');
        options.phase1_result = S_p1.bestPoint;
        options.MaxObjectiveEvaluations = phase2_config.MaxObjectiveEvaluations;
        options.scenes = phase2_config.scenes;
        
        fprintf('  Phase 2: 场景自适应优化 (5个变量)\n');
        fprintf('  ✓ 已加载Phase 1结果:\n');
        fprintf('      q_y=%.2f, q_psi=%.2f, q_v=%.2f, q_omega=%.2f\n', ...
            S_p1.bestPoint.q_y, S_p1.bestPoint.q_psi, ...
            S_p1.bestPoint.q_v, S_p1.bestPoint.q_omega);
        fprintf('  ✓ 场景权重: golden=%.2f, turn=%.2f, slope=%.2f, composite=%.2f\n', ...
            options.scenes.golden_test, options.scenes.pure_turn, ...
            options.scenes.pure_slope, options.scenes.composite);
        
    otherwise
        error('不支持的阶段: %d (请设置 RUN_PHASE = 1 或 2)', RUN_PHASE);
end

fprintf('  ✓ 评估次数: %d\n\n', options.MaxObjectiveEvaluations);

%% 4. 执行优化
fprintf('【步骤4/4】开始 Phase %d 优化...\n', RUN_PHASE);
fprintf('========================================\n\n');

tic;
[best, boResults] = Bayesian_Optimization(params, db, options);
elapsed_time = toc;

%% 5. 保存结果
bestPoint = boResults.XAtMinObjective;

switch RUN_PHASE
    case 1
        save_file = fullfile(results_dir, 'phase1_best.mat');
        save(save_file, 'best', 'bestPoint', 'boResults');
        fprintf('\n✓ Phase 1 结果已保存: %s\n', save_file);
        
    case 2
        save_file = fullfile(results_dir, 'phase2_best.mat');
        % 合并Phase 1和Phase 2的结果
        combined = struct();
        combined.q_y = S_p1.bestPoint.q_y;
        combined.q_psi = S_p1.bestPoint.q_psi;
        combined.q_v = S_p1.bestPoint.q_v;
        combined.q_omega = S_p1.bestPoint.q_omega;
        combined.log10_r_F = S_p1.bestPoint.log10_r_F;
        combined.log10_r_omega = S_p1.bestPoint.log10_r_omega;
        combined.log10_rdF = S_p1.bestPoint.log10_rdF;
        combined.log10_rdw = S_p1.bestPoint.log10_rdw;
        combined.omega_threshold = bestPoint.omega_threshold;
        combined.q_y_gain_max = bestPoint.q_y_gain_max;
        combined.theta_threshold = bestPoint.theta_threshold;
        combined.q_v_gain_max = bestPoint.q_v_gain_max;
        if isfield(bestPoint, 'R_F_gain_max_uphill')
            combined.R_F_gain_max_uphill = bestPoint.R_F_gain_max_uphill;
        end
        save(save_file, 'best', 'bestPoint', 'combined', 'boResults');
        fprintf('\n✓ Phase 2 结果已保存: %s\n', save_file);
end

%% 6. 显示结果摘要
fprintf('\n');
fprintf('╔════════════════════════════════════════╗\n');
fprintf('║     Phase %d 优化完成！                 ║\n', RUN_PHASE);
fprintf('╚════════════════════════════════════════╝\n\n');

fprintf('【优化结果摘要】\n');
fprintf('  最优代价 J_min: %.6f\n', best.J);
fprintf('  总耗时: %.2f 分钟 (%.1f 秒/次)\n', elapsed_time/60, ...
    elapsed_time/boResults.NumObjectiveEvaluations);
fprintf('\n');

fprintf('【最优参数】\n');
switch RUN_PHASE
    case 1
        fprintf('  状态权重 Q:\n');
        fprintf('    q_y     = %.4f\n', bestPoint.q_y);
        fprintf('    q_psi   = %.4f\n', bestPoint.q_psi);
        fprintf('    q_v     = %.4f\n', bestPoint.q_v);
        fprintf('    q_omega = %.4f\n', bestPoint.q_omega);
        fprintf('  控制权重 R:\n');
        fprintf('    r_F     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_r_F, bestPoint.log10_r_F);
        fprintf('    r_omega = %.6f (log10: %.2f)\n', 10^bestPoint.log10_r_omega, bestPoint.log10_r_omega);
        fprintf('  控制增量权重 dR:\n');
        fprintf('    rdF     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_rdF, bestPoint.log10_rdF);
        fprintf('    rdw     = %.6f (log10: %.2f)\n', 10^bestPoint.log10_rdw, bestPoint.log10_rdw);
        fprintf('\n');
        fprintf('【下一步】\n');
        fprintf('  1. 验证Phase 1结果效果\n');
        fprintf('  2. 设置 RUN_PHASE = 2 并重新运行此脚本\n');
        
    case 2
        fprintf('  弯道自适应:\n');
        fprintf('    omega_threshold = %.4f rad/s\n', bestPoint.omega_threshold);
        fprintf('    q_y_gain_max    = %.3f\n', bestPoint.q_y_gain_max);
        fprintf('  坡道自适应:\n');
        fprintf('    theta_threshold = %.4f rad (%.2f°)\n', bestPoint.theta_threshold, rad2deg(bestPoint.theta_threshold));
        fprintf('    q_v_gain_max    = %.3f\n', bestPoint.q_v_gain_max);
        if isfield(bestPoint, 'R_F_gain_max_uphill')
            fprintf('    R_F_gain_max_uphill = %.3f\n', bestPoint.R_F_gain_max_uphill);
        end
        fprintf('\n');
        fprintf('【最终合并参数】\n');
        fprintf('  已保存到: %s\n', save_file);
        fprintf('  使用 combined 结构体获取完整参数\n');
end
fprintf('\n');

%% 7. 各分区性能
fprintf('【各分区性能】\n');
scene_names = fieldnames(best.report.scene);
for i = 1:length(scene_names)
    sn = scene_names{i};
    if isfield(best.report.scene.(sn), 'RMSE')
        rep = best.report.scene.(sn);
        % 获取权重 (从options.zones或传入的scenes中获取)
        if isfield(options.scenes, sn)
            w = options.scenes.(sn);
        else
            w = 0; % 默认
        end
        fprintf('  %s (权重=%.2f):\n', sn, w);
        fprintf('    RMSE: ey=%.4fm, epsi=%.2f°, ev=%.4fm/s\n', ...
            rep.RMSE.ey, rad2deg(rep.RMSE.epsi), rep.RMSE.ev);
        fprintf('    RMS du: dF=%.2fN, dw=%.4frad/s\n', rep.RMS_du.dF, rep.RMS_du.dw);
    end
end
fprintf('\n');

fprintf('========================================\n');
fprintf('  优化流程完成！\n');
fprintf('========================================\n');
