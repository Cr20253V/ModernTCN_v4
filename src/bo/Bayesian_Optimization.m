function [best, boResults] = Bayesian_Optimization(params, db, options)
% =============================
% 文件名：Bayesian_Optimization.m
% 版本号：V2.10
% 最后修改时间：2025-11-20
% 作者：LPV-MPC Project
% 功能描述：
%   两阶段贝叶斯优化：全局搜索 + 局部精细搜索
%   使用 bayesopt 调度 Cost_Function，获得最优参数并生成 maps_best.mat（根目录）
% 输入参数：
%   - params : parameters() 结果
%   - db     : LPV 库（可为空，内部生成3×3×3默认网格）
%   - options: 结构体（可选），含以下字段：
%       .MaxObjectiveEvaluations - 第一阶段评估次数（默认：100）
%       .local_refine.num_evals  - 第二阶段评估次数（默认：30% * 第一阶段）
%       .local_refine.enable     - 是否启用第二阶段（默认：true）
%       .scenes                  - 场景权重（默认：turn=0.35, bumpy=0.35, slope=0.10, straight_turn=0.10, straight=0.10）
%       .save_history            - 是否保存历史（默认：false）
% 输出参数：
%   - best      : 最优设计（变量、代价、统计）
%   - boResults : bayesopt 原始结果（第二阶段或第一阶段）
% 备注：
%   - 变量集包含 Q/R/dR、alpha/beta 形状、scale_* 缩放、tau、场景自适应参数
%   - 产物保存至根目录：maps_best.mat（含权重/约束映射）
%   - 可选历史记录：bo_history_<timestamp>.mat
%   - db为空时自动生成默认网格（V=[0.8,1.0,1.2], W=[-0.2,0,0.2], T=[-0.2,0,0.2]）
%   - V2.5更新：调整优化范围以适应移除F_eq后的系统（提高q_v，放宽r_F）
%   - V2.6更新（关键修复）：第二阶段显式记录第一阶段最优点，确保全局最优不丢失
%   - V2.7更新（关键修复）：修复LocalRefine丢失全局最优的bug，现在比较两阶段的全局最小值而不仅是bestPoint
%   - V2.8更新（流程优化）：按照正确流程重新组织第二阶段：验证第一阶段最优 → 生成局部初始点 → 局部优化 → 按情况选择结果
%   - V2.9更新（关键修复）：修复第一阶段选择逻辑，现在选择实际观察到的最小代价点而不仅是bestPoint预测的最优点
%   - V2.10更新（2025-11-20）：更新场景权重默认值（bumpy: 0.10→0.35, slope: 0.30→0.10, straight_turn: 0.20→0.10, straight: 0.05→0.10），使优化更关注颠簸场景
% =============================

root = project_root();
data_models_dir = fullfile(root, 'data', 'models');

%% 参数处理
% params：如果未传入或为空，调用 parameters() 生成默认参数
if nargin < 1 || isempty(params)
    fprintf('[Bayesian_Optimization] params 未传入，使用 parameters() 生成默认参数。\n');
    params = parameters();
else
    fprintf('[Bayesian_Optimization] 使用显式传入的 params。\n');
end

% db：如果未传入，设为空（后续会自动生成默认网格）
%     推荐用法：显式加载 lin_agv_db.mat 并传入
%     示例：S = load('lin_agv_db.mat', 'db'); db = S.db;
if nargin < 2
    db = [];
end

if isempty(db)
    fprintf('[Bayesian_Optimization] db 为空，将在首次评估时生成默认 3×3×3 网格。\n');
    fprintf('[Bayesian_Optimization] 推荐：显式加载 lin_agv_db.mat 以节省时间。\n');
else
    fprintf('[Bayesian_Optimization] 使用显式传入的 db。\n');
    fprintf('[Bayesian_Optimization]   网格尺寸: %d×%d×%d = %d 点\n', ...
        db.Nv, db.Nw, db.Nt, db.Nv*db.Nw*db.Nt);
end

% options：如果未传入，初始化为空结构体（使用默认配置）
%     可配置项：
%       - options.scenes：场景权重（默认：turn=0.35, slope=0.30, ...）
%       - options.MaxObjectiveEvaluations：最大评估次数（默认：100）
%       - options.save_history：是否保存历史（默认：false）
if nargin < 3
    options = struct();
end

% 变量范围（V2.5: 调整以适应移除F_eq后的系统）
vars = [
    optimizableVariable('q_y',[15,35],'Type','real');         % ↑↑ 进一步提升横向跟踪（解决 turn e_y 大的问题）
    optimizableVariable('q_psi',[12,30],'Type','real');       % ↑↑ 进一步提升航向跟踪
    optimizableVariable('q_v',[3.0,8],'Type','real');         % ↑↑ V2.5: 提高范围以应对阻力补偿需求（原[2.0,6]）
    optimizableVariable('q_omega',[0.5,3],'Type','real');     % 维持
    optimizableVariable('log10_r_F',[-4.0,-2.5],'Type','real'); % ↓↓ V2.5: 放宽下界，允许更大控制努力（原[-3.5,-2]）
    optimizableVariable('log10_r_omega',[-3.8,-2.2],'Type','real'); % 放松角速度指令权重
    optimizableVariable('log10_rdF',[-2.2,-1],'Type','real'); % ↑ 提升纵向平滑性
    optimizableVariable('log10_rdw',[-2.5,-1],'Type','real'); % ↑ 提升角速度平滑性
    optimizableVariable('alpha_Q',[0.0,1.0],'Type','real');
    optimizableVariable('beta_Q',[0.0,1.0],'Type','real');
    optimizableVariable('alpha_R',[0.0,1.0],'Type','real');
    optimizableVariable('beta_R',[0.0,1.0],'Type','real');
    optimizableVariable('alpha_dR',[0.0,1.0],'Type','real');
    optimizableVariable('beta_dR',[0.0,1.0],'Type','real');
    optimizableVariable('scale_umin_lo',[0.9,1.1],'Type','real');
    optimizableVariable('scale_umin_hi',[0.9,1.1],'Type','real');
    optimizableVariable('scale_umax_lo',[0.9,1.1],'Type','real');
    optimizableVariable('scale_umax_hi',[0.9,1.1],'Type','real');
    optimizableVariable('tau',[0.2,0.6],'Type','real');
    % 场景自适应参数（方案B+C）
    optimizableVariable('omega_threshold',[0.05,0.20],'Type','real');
    optimizableVariable('transition_width',[0.02,0.06],'Type','real');
    optimizableVariable('q_y_gain_max',[1.2,2.5],'Type','real');
    optimizableVariable('theta_threshold',[0.03,0.05],'Type','real');
    optimizableVariable('theta_transition_width',[0.01,0.025],'Type','real');
    optimizableVariable('q_v_gain_max',[1.2,2.0],'Type','real');
    optimizableVariable('R_F_gain_max_uphill',[1.0,1.6],'Type','real');
    optimizableVariable('R_F_gain_max_downhill',[1.0,2.0],'Type','real');
    optimizableVariable('dR_F_gain_max_uphill',[1.0,1.8],'Type','real');
    optimizableVariable('dR_F_gain_max_downhill',[1.0,2.2],'Type','real')
];

%% 场景权重配置
% 默认权重（共 5 个场景）
% 可通过 options.scenes 覆盖
if ~isfield(options,'scenes')
    scenes = struct('straight_left_turn',0.25,'straight_right_turn',0.25,...
                    'slope',0.15,'bumpy',0.20,'straight',0.15);
    fprintf('[Bayesian_Optimization] 使用默认场景权重。\n');
else
    scenes = options.scenes;
    fprintf('[Bayesian_Optimization] 使用自定义场景权重。\n');
end
fprintf('[Bayesian_Optimization]   straight_left/right=%.2f/%.2f, slope=%.2f, bumpy=%.2f, straight=%.2f\n', ...
    scenes.straight_left_turn, scenes.straight_right_turn, scenes.slope, scenes.bumpy, scenes.straight);

% 目标函数封装
obj = @(X) objective_wrapper(X, params, db, scenes);

%% bayesopt 配置
% 默认配置：MaxObjectiveEvaluations=100, UseParallel=false
% 可通过 options 覆盖：
%   options.MaxObjectiveEvaluations = 50;  % 修改迭代次数
%   options.save_history = true;           % 保存优化历史
boOpts = struct();
boOpts.AcquisitionFunctionName = 'expected-improvement-plus';
boOpts.IsObjectiveDeterministic = true;
boOpts.Verbose = 1;
boOpts.PlotFcn = [];
boOpts.MaxObjectiveEvaluations = 3;  % 默认100次评估
boOpts.UseParallel = false;

% 从 options 中覆盖配置
if isfield(options,'MaxObjectiveEvaluations')
    boOpts.MaxObjectiveEvaluations = options.MaxObjectiveEvaluations;
end

fprintf('[Bayesian_Optimization] 最大评估次数: %d\n', boOpts.MaxObjectiveEvaluations);
fprintf('[Bayesian_Optimization] 采集函数: %s\n', boOpts.AcquisitionFunctionName);

% 初始点：当前默认 + 9 个 LHS 样本
% 这里仅用自动采样，若需要自定义初始点，可使用 InitialX

boResults = bayesopt(obj, vars, 'AcquisitionFunctionName', boOpts.AcquisitionFunctionName, ...
    'IsObjectiveDeterministic', boOpts.IsObjectiveDeterministic, 'Verbose', boOpts.Verbose, ...
    'MaxObjectiveEvaluations', boOpts.MaxObjectiveEvaluations, 'UseParallel', boOpts.UseParallel);

% ★ 关键修复：选择实际观察到的最小代价点，而不是bestPoint预测的最优点
% bestPoint返回的是代理模型预测的最优点，可能不是实际评估过的最小代价点
bestRow_pred = bestPoint(boResults);  % 代理模型预测的最优点
[bestJ_pred, best_pred] = objective_wrapper(bestRow_pred, params, db, scenes);

% 获取第一阶段实际观察到的最小代价点
all_objectives_stage1 = boResults.ObjectiveTrace;
min_objective_stage1 = min(all_objectives_stage1);
min_idx_stage1 = find(all_objectives_stage1 == min_objective_stage1, 1, 'first');
min_row_stage1 = boResults.XTrace(min_idx_stage1,:);

fprintf('[Bayesian_Optimization] 第一阶段完成：\n');
fprintf('[Bayesian_Optimization]   bestPoint预测最优: J = %.6f\n', bestJ_pred);
fprintf('[Bayesian_Optimization]   实际观察最小值: J = %.6f (迭代 #%d)\n', min_objective_stage1, min_idx_stage1);

% 选择实际观察到的最小代价点作为第一阶段最优
if min_objective_stage1 < bestJ_pred
    fprintf('[Bayesian_Optimization]   ✓ 选择实际观察最小值（比预测值更好: %.6f）\n', bestJ_pred - min_objective_stage1);
    bestRow = min_row_stage1;
    [bestJ, best] = objective_wrapper(bestRow, params, db, scenes);
else
    fprintf('[Bayesian_Optimization]   ◯ 使用bestPoint预测最优\n');
    bestRow = bestRow_pred;
    bestJ = bestJ_pred;
    best = best_pred;
end

%% 二阶段：局部精细搜索（围绕当前最优点收缩边界）
% options.local_refine 可选配置：
%   .enable(true/false) .shrink(0.35) .num_evals(30) .num_seeds(8) .jitter(0.08)
boResults_final = boResults; best_final = best; bestJ_final = bestJ; bestRow_final = bestRow;

if ~exist('options','var') || ~isfield(options,'local_refine') || isempty(options.local_refine)
    local_refine = struct();
else
    local_refine = options.local_refine;
end
if ~isfield(local_refine,'enable'),     local_refine.enable = true; end
if ~isfield(local_refine,'shrink'),     local_refine.shrink = 0.35; end
if ~isfield(local_refine,'num_evals')
    local_refine.num_evals = max(10, min(30, round(0.3 * boOpts.MaxObjectiveEvaluations)));
end
if ~isfield(local_refine,'num_seeds'),  local_refine.num_seeds = 8; end
if ~isfield(local_refine,'jitter'),     local_refine.jitter = 0.08; end

if local_refine.enable
    fprintf('[LocalRefine] 启用：shrink=%.2f, seeds=%d, evals=%d, jitter=%.2f\n', ...
        local_refine.shrink, local_refine.num_seeds, local_refine.num_evals, local_refine.jitter);

    % 全局边界
    nVar = numel(vars);
    varNames = cell(nVar,1); glbLo = zeros(nVar,1); glbHi = zeros(nVar,1);
    for i = 1:nVar
        varNames{i} = vars(i).Name;
        glbLo(i) = vars(i).Range(1);
        glbHi(i) = vars(i).Range(2);
    end

    % 局部边界（以 bestRow 为中心、按 shrink 收缩）
    vars_local = optimizableVariable.empty(0, nVar);
    locLo = zeros(nVar,1); locHi = zeros(nVar,1);
    for i = 1:nVar
        c  = bestRow.(varNames{i});
        hw = 0.5 * (glbHi(i) - glbLo(i)) * local_refine.shrink;
        lo = max(glbLo(i), c - hw);
        hi = min(glbHi(i), c + hw);
        if hi <= lo
            epsw = max(1e-6, 1e-3 * (glbHi(i) - glbLo(i)));
            lo = max(glbLo(i), c - epsw);
            hi = min(glbHi(i), c + epsw);
        end
        locLo(i) = lo; locHi(i) = hi;
        vars_local(i) = optimizableVariable(varNames{i}, [lo, hi], 'Type', 'real');
    end

    % ★ 按照您描述的正确流程：第二阶段第一次评估复现第一阶段最优，之后继续优化

    fprintf('[LocalRefine] 开始第二阶段优化...\n');
    fprintf('[LocalRefine]   第一阶段最优: J = %.6f\n', bestJ_final);

    % 步骤1：验证第一阶段最优结果（相当于"第二次优化是为了复现第一阶段的最好结果"）
    fprintf('[LocalRefine]   步骤1: 验证第一阶段最优结果...\n');
    [J_verify, result_verify] = objective_wrapper(bestRow, params, db, scenes);
    fprintf('[LocalRefine]     验证结果: J = %.6f (原始: %.6f, 差值: %.2e)\n', J_verify, bestJ_final, J_verify - bestJ_final);

    % 如果验证结果与第一阶段差异太大，发出警告
    if abs(J_verify - bestJ_final) > 1e-3
        fprintf('[LocalRefine]     ⚠ 警告: 验证结果与第一阶段不一致，可能存在随机性问题\n');
    end

    % 步骤2：生成局部搜索的初始点（在第一阶段最优附近）
    fprintf('[LocalRefine]   步骤2: 生成局部搜索初始点...\n');

    % 只使用随机抖动点作为第二阶段的初始点（不包括第一阶段最优点，因为已经验证过了）
    initialX_local = table();
    for s = 1:local_refine.num_seeds
        row = table();
        for i = 1:nVar
            span = (locHi(i) - locLo(i));
            % 在第一阶段最优点附近生成抖动点
            v_base = bestRow.(varNames{i});
            v = v_base + local_refine.jitter * span * (rand() - 0.5);
            v = min(max(v, locLo(i)), locHi(i));  % 确保在局部边界内
            row.(varNames{i}) = v;
        end
        initialX_local = [initialX_local; row]; %#ok<AGROW>
    end

    fprintf('[LocalRefine]     生成 %d 个局部搜索初始点\n', local_refine.num_seeds);

    % 步骤3：执行局部贝叶斯优化（在第一阶段最优基础上继续优化）
    fprintf('[LocalRefine]   步骤3: 执行局部贝叶斯优化...\n');
    boResults2 = bayesopt(obj, vars_local, ...
        'AcquisitionFunctionName', boOpts.AcquisitionFunctionName, ...
        'IsObjectiveDeterministic', boOpts.IsObjectiveDeterministic, ...
        'Verbose', boOpts.Verbose, ...
        'MaxObjectiveEvaluations', local_refine.num_evals, ...
        'UseParallel', boOpts.UseParallel, ...
        'InitialX', initialX_local);

    % 步骤4：分析第二阶段结果并确定最终最优
    fprintf('[LocalRefine]   步骤4: 分析结果并确定最终最优...\n');

    bestRow2 = bestPoint(boResults2);
    [bestJ2, best2] = objective_wrapper(bestRow2, params, db, scenes);

    % 获取第二阶段观察到的全局最小值
    all_objectives_stage2 = boResults2.ObjectiveTrace;
    min_objective_stage2 = min(all_objectives_stage2);
    min_idx_stage2 = find(all_objectives_stage2 == min_objective_stage2, 1, 'first');
    min_row_stage2 = boResults2.XTrace(min_idx_stage2,:);

    fprintf('[LocalRefine] 第二阶段完成：\n');
    fprintf('[LocalRefine]   第一阶段最优: J = %.6f\n', bestJ_final);
    fprintf('[LocalRefine]   第二阶段 bestPoint: J = %.6f\n', bestJ2);
    fprintf('[LocalRefine]   第二阶段全局最小: J = %.6f (迭代 #%d)\n', min_objective_stage2, min_idx_stage2);

    % 调试信息：显示第二阶段的所有评估结果
    fprintf('[LocalRefine]   第二阶段评估统计:\n');
    fprintf('[LocalRefine]     总评估次数: %d\n', length(all_objectives_stage2));
    fprintf('[LocalRefine]     成功评估: %d (代价 < 1e6)\n', sum(all_objectives_stage2 < 1e6));
    fprintf('[LocalRefine]     失败评估: %d (代价 >= 1e6)\n', sum(all_objectives_stage2 >= 1e6));
    if sum(all_objectives_stage2 < 1e6) > 0
        fprintf('[LocalRefine]     成功评估的最小代价: %.6f\n', min(all_objectives_stage2(all_objectives_stage2 < 1e6)));
        fprintf('[LocalRefine]     成功评估的最大代价: %.6f\n', max(all_objectives_stage2(all_objectives_stage2 < 1e6)));
    end

    % 步骤5：按照您描述的情况确定最终结果
    % 情况1：第二阶段没找到更好结果，保存第一阶段最优
    % 情况2：第二阶段找到更好结果，保存该结果

    % 比较第一阶段最优与第二阶段全局最小
    if isfinite(min_objective_stage2) && (min_objective_stage2 < bestJ_final)
        % 情况2：第二阶段找到更好结果
        fprintf('[LocalRefine] ✓ 情况2: 第二阶段找到更优解！采用全局最小结果（改进: %.6f）\n', bestJ_final - min_objective_stage2);
        [bestJ_global, best_global] = objective_wrapper(min_row_stage2, params, db, scenes);
        boResults_final = boResults2; best_final = best_global; bestJ_final = bestJ_global; bestRow_final = min_row_stage2;
    else
        % 情况1：第二阶段没找到更好结果，保存第一阶段最优
        fprintf('[LocalRefine] ◯ 情况1: 第二阶段未找到更好结果，采用第一阶段最优结果\n');
        fprintf('[LocalRefine]   第二阶段最小: J = %.6f, 第一阶段: J = %.6f\n', min_objective_stage2, bestJ_final);
        % 保持第一阶段结果（best_final, bestJ_final, bestRow_final 已设置为第一阶段结果）
    end
end

% 落盘 maps_best.mat（数据目录）
maps_best = pack_maps(best_final);
maps_best_file = fullfile(data_models_dir, 'maps_best.mat');
save(maps_best_file,'maps_best');

%% 保存优化历史（可选）
% 通过 options.save_history = true 启用
% 默认：false（不保存）
if isfield(options,'save_history') && options.save_history
    history_dir = results_dir('bo/history');
    history_file = fullfile(history_dir, sprintf('bo_history_%s.mat', datestr(now,'yyyymmdd_HHMMSS')));
    save(history_file, 'boResults');
    fprintf('[Bayesian_Optimization] 优化历史已保存: %s\n', history_file);
else
    fprintf('[Bayesian_Optimization] 未保存优化历史（options.save_history=false）。\n');
end

fprintf('\n========== 优化结果摘要 ==========\n');
fprintf('最优代价 J = %.6f\n', best_final.J);
fprintf('失败场景数: %d\n', best_final.report.fail_count);
fprintf('=================================\n');

% 返回最终结果（可能来自一阶段或二阶段）
best = best_final;
boResults = boResults_final;

end

function [J, out] = objective_wrapper(X, params, db, scenes)
% 将 X 解包到 cfg 与 ctrl maps 的映射
persistent base_ctrl;  % 持久变量：只创建一次基准控制器

cfg = struct();
cfg.tau = X.tau;

% 权重与范围
Q0 = [X.q_y, X.q_psi, X.q_v, X.q_omega];
R0 = [10^(X.log10_r_F), 10^(X.log10_r_omega)];
dR0= [10^(X.log10_rdF), 10^(X.log10_rdw)];

% 形状参数:强制 alpha <= beta（修正非法值）
alpha_Q_val = min(X.alpha_Q, X.beta_Q);  % 取小者作为 alpha
beta_Q_val  = max(X.alpha_Q, X.beta_Q);  % 取大者作为 beta
alpha_R_val = min(X.alpha_R, X.beta_R);
beta_R_val  = max(X.alpha_R, X.beta_R);
alpha_dR_val= min(X.alpha_dR, X.beta_dR);
beta_dR_val = max(X.alpha_dR, X.beta_dR);

alpha_Q = repmat(alpha_Q_val, 1, 4);
beta_Q  = repmat(beta_Q_val, 1, 4);
alpha_R = repmat(alpha_R_val, 1, 2);
beta_R  = repmat(beta_R_val, 1, 2);
alpha_dR= repmat(alpha_dR_val, 1, 2);
beta_dR = repmat(beta_dR_val, 1, 2);

% 约束缩放（示例：两端缩放均一）
scale_umin_lo = [X.scale_umin_lo, X.scale_umin_lo];
scale_umin_hi = [X.scale_umin_hi, X.scale_umin_hi];
scale_umax_lo = [X.scale_umax_lo, X.scale_umax_lo];
scale_umax_hi = [X.scale_umax_hi, X.scale_umax_hi];

% 构建 ctrl（只在第一次调用时创建基准控制器，后续复用）
if isempty(db)
    fprintf('[Bayesian_Optimization] db 为空，生成默认 3x3x3 网格...\n');
    grid.V_grid = [0.8; 1.0; 1.2];
    grid.W_grid = [-0.2; 0.0; 0.2];  % 有符号 ω
    grid.T_grid = [-0.2; 0.0; 0.2];  % 匹配颠簸幅值 0.2 rad
    lin_opts = struct('coord','path','disc','zoh','keep_E',true, ...
        'export_mat', fullfile(data_models_dir, 'plant_grid.mat'));
    db = lin_agv_grid(params, grid, lin_opts);
    fprintf('[Bayesian_Optimization] 默认网格生成完成。\n');
end

% 只在第一次调用时创建基准控制器（使用持久变量避免重复创建）
if isempty(base_ctrl)
    fprintf('[Bayesian_Optimization] 首次评估：创建基准控制器...\n');
    % 使用中等偏保守的默认权重创建控制器（不影响后续maps覆盖）
    base_opts = struct('Q',[10,15,2,1],'R',[1e-3,1e-3],'dR',[1e-2,1e-2]);
    evalc('base_ctrl = mpc_setup_single_interp(db, base_opts);');
    fprintf('[Bayesian_Optimization] 基准控制器创建完成（后续评估将复用此控制器）\n');
end

% 深拷贝基准控制器（避免 mpcobj 对象被后续评估污染）
% 方法：每次重新创建 mpcobj（从 base_ctrl 的模型和参数）
% 注意：虽然重新创建，但只是克隆现有配置，不涉及复杂计算
ctrl = struct();
ctrl.db = base_ctrl.db;
ctrl.opts = base_ctrl.opts;
ctrl.maps = base_ctrl.maps;
ctrl.meta = base_ctrl.meta;

% 从 base_ctrl.mpcobj 克隆配置创建新实例
plant_base = base_ctrl.mpcobj.Model.Plant;
Ts = base_ctrl.mpcobj.Ts;
Np = base_ctrl.mpcobj.PredictionHorizon;
Nc = base_ctrl.mpcobj.ControlHorizon;

% 创建新的 mpcobj（快速，只是对象实例化）
ctrl.mpcobj = mpc(plant_base, Ts, Np, Nc);

% 复制权重（使用基准值，后续会被 mpc_update_from_rho 覆盖）
ctrl.mpcobj.Weights.OutputVariables = base_ctrl.opts.Q;
ctrl.mpcobj.Weights.ManipulatedVariables = base_ctrl.opts.R;
ctrl.mpcobj.Weights.ManipulatedVariablesRate = base_ctrl.opts.dR;

% 复制约束
for i = 1:2  % 2个MV
    ctrl.mpcobj.MV(i).Min = base_ctrl.mpcobj.MV(i).Min;
    ctrl.mpcobj.MV(i).Max = base_ctrl.mpcobj.MV(i).Max;
    ctrl.mpcobj.MV(i).RateMin = base_ctrl.mpcobj.MV(i).RateMin;
    ctrl.mpcobj.MV(i).RateMax = base_ctrl.mpcobj.MV(i).RateMax;
end

% 复制输出约束
for i = 1:4  % 4个OV
    ctrl.mpcobj.OV(i).Min = base_ctrl.mpcobj.OV(i).Min;
    ctrl.mpcobj.OV(i).Max = base_ctrl.mpcobj.OV(i).Max;
    if isfinite(base_ctrl.mpcobj.OV(i).MinECR)
        ctrl.mpcobj.OV(i).MinECR = base_ctrl.mpcobj.OV(i).MinECR;
    end
    if isfinite(base_ctrl.mpcobj.OV(i).MaxECR)
        ctrl.mpcobj.OV(i).MaxECR = base_ctrl.mpcobj.OV(i).MaxECR;
    end
end

% 覆盖 maps（核心：所有优化参数通过maps在线调度，而非重建控制器）
ctrl.maps.Q_range = [Q0*0.5; Q0*1.5];
ctrl.maps.R_range = [R0*0.5; R0*1.5];
ctrl.maps.dR_range= [dR0*0.5; dR0*1.5];

% 调试：打印当前评估的权重范围（已验证修复成功，可注释）
% fprintf('[BO-DEBUG] Q0=[%.2f,%.2f,%.2f,%.2f], R0=[%.2e,%.2e], dR0=[%.2e,%.2e]\n', ...
%     Q0(1), Q0(2), Q0(3), Q0(4), R0(1), R0(2), dR0(1), dR0(2));
ctrl.maps.alpha_Q = alpha_Q; ctrl.maps.beta_Q = beta_Q;
ctrl.maps.alpha_R = alpha_R; ctrl.maps.beta_R = beta_R;
ctrl.maps.alpha_dR= alpha_dR;ctrl.maps.beta_dR = beta_dR;
ctrl.maps.scale_umin_lo = scale_umin_lo; ctrl.maps.scale_umin_hi = scale_umin_hi;
ctrl.maps.scale_umax_lo = scale_umax_lo; ctrl.maps.scale_umax_hi = scale_umax_hi;

% 传递 rho_min/rho_max（从db.grid提取）
ctrl.maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
ctrl.maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];

% 滤波时间常数（用于rho一阶滤波）
ctrl.maps.tau = X.tau;

% 场景自适应参数（方案B+C）
ctrl.maps.omega_threshold          = X.omega_threshold;
ctrl.maps.transition_width        = X.transition_width;
ctrl.maps.q_y_gain_max           = X.q_y_gain_max;
ctrl.maps.theta_threshold        = X.theta_threshold;
ctrl.maps.theta_transition_width = X.theta_transition_width;
ctrl.maps.q_v_gain_max           = X.q_v_gain_max;
ctrl.maps.R_F_gain_max_uphill    = X.R_F_gain_max_uphill;
ctrl.maps.R_F_gain_max_downhill  = X.R_F_gain_max_downhill;
ctrl.maps.dR_F_gain_max_uphill   = X.dR_F_gain_max_uphill;
ctrl.maps.dR_F_gain_max_downhill = X.dR_F_gain_max_downhill;

% 评估（将ctrl和ctrl_maps传入cfg，避免重复创建控制器）
cfg.ctrl = ctrl;
cfg.ctrl_maps = ctrl.maps;
[cost, report] = Cost_Function(params, db, cfg, scenes);

% 失败返回大罚
if ~isfinite(cost)
    J = 1e6;
else
    J = cost;
end

out = struct('J',J,'report',report,'ctrl_maps',ctrl.maps);

end

function maps_best = pack_maps(best)
maps_best = struct();
% 存储关键超参（完整）
if isfield(best,'ctrl_maps')
    maps_best.Q_range = best.ctrl_maps.Q_range;
    maps_best.R_range = best.ctrl_maps.R_range;
    maps_best.dR_range= best.ctrl_maps.dR_range;
    maps_best.alpha_Q = best.ctrl_maps.alpha_Q; maps_best.beta_Q = best.ctrl_maps.beta_Q;
    maps_best.alpha_R = best.ctrl_maps.alpha_R; maps_best.beta_R = best.ctrl_maps.beta_R;
    maps_best.alpha_dR= best.ctrl_maps.alpha_dR; maps_best.beta_dR = best.ctrl_maps.beta_dR;
    maps_best.scale_umin_lo = best.ctrl_maps.scale_umin_lo;
    maps_best.scale_umin_hi = best.ctrl_maps.scale_umin_hi;
    maps_best.scale_umax_lo = best.ctrl_maps.scale_umax_lo;
    maps_best.scale_umax_hi = best.ctrl_maps.scale_umax_hi;
    % 归一化端点
    if isfield(best.ctrl_maps,'rho_min')
        maps_best.rho_min = best.ctrl_maps.rho_min;
        maps_best.rho_max = best.ctrl_maps.rho_max;
    end
    % 滤波时间常数
    if isfield(best.ctrl_maps,'tau')
        maps_best.tau = best.ctrl_maps.tau;
    end
    % 场景自适应参数（方案B+C）
    if isfield(best.ctrl_maps,'omega_threshold')
        maps_best.omega_threshold          = best.ctrl_maps.omega_threshold;
        maps_best.transition_width        = best.ctrl_maps.transition_width;
        maps_best.q_y_gain_max           = best.ctrl_maps.q_y_gain_max;
        maps_best.theta_threshold        = best.ctrl_maps.theta_threshold;
        maps_best.theta_transition_width = best.ctrl_maps.theta_transition_width;
        maps_best.q_v_gain_max           = best.ctrl_maps.q_v_gain_max;
        maps_best.R_F_gain_max_uphill    = best.ctrl_maps.R_F_gain_max_uphill;
        maps_best.R_F_gain_max_downhill  = best.ctrl_maps.R_F_gain_max_downhill;
        maps_best.dR_F_gain_max_uphill   = best.ctrl_maps.dR_F_gain_max_uphill;
        maps_best.dR_F_gain_max_downhill = best.ctrl_maps.dR_F_gain_max_downhill;
    end
end
% 元数据
maps_best.timestamp = datestr(now,'yyyy-mm-dd HH:MM:SS');
maps_best.version = 'V2.5';
end
