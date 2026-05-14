function [best, boResults] = Bayesian_Optimization(params, db, options)
% =============================
% 文件名：Bayesian_Optimization.m
% 版本号：V2.12
% 最后修改时间：2026-03-07
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
%   - V2.11更新（2026-03-06）：IsObjectiveDeterministic 改为 false
%       原因：并行仿真（UseParallel=true）时，各worker的persistent base_ctrl初始化时序
%       不可控，导致同参数两次调用代价差值达0.1~0.2级别。声明false使bayesopt使用
%       噪声感知高斯过程，避免代理模型在噪声数据上过度乐观拟合，bestPoint更可靠。
%   - V2.12更新（2026-03-07）：修复Phase 1与LocalRefine的比较逻辑（问题4）
%       原问题：Phase 1将代理预测值(bestJ_pred)与实际采样(min_objective_stage1)混合
%       比较；LocalRefine将stage2实际采样与stage1代理预测值比较——苹果与橘子对比。
%       修复：Phase 1始终采用实际观测最优(min_row_stage1)作为最终结果；LocalRefine
%       改为与min_objective_stage1（stage1实际采样最小值）比较，统一比较基准。
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
%       - options.phase：优化阶段（1=核心权重, 2=场景自适应, 3=微调）
%       - options.phase1_result：Phase 1的最优结果（Phase 2/3使用）
if nargin < 3
    options = struct();
end

%% ========== 分阶段优化配置 ==========
% 策略说明：
%   Phase 1: 只优化 Q, R, dR 共8个核心变量（夯实基础）
%   Phase 2: 固定核心权重，只优化4个场景自适应变量（场景攻坚）
%   Phase 3: 放开部分变量进行微调（可选）
%
% 被冻结的变量：
%   - alpha/beta_*: 形状参数（固定为0.5，线性插值）
%   - scale_*: 约束缩放（固定为1.0，信任物理参数）
%   - tau: rho滤波常数（固定为0.35）
% =====================================

phase = 1;  % 默认Phase 1
if isfield(options, 'phase')
    phase = options.phase;
end
fprintf('[Bayesian_Optimization] 当前优化阶段: Phase %d\n', phase);

%% 冻结参数（不参与优化的固定值）
frozen = struct();
frozen.alpha_Q = 0.5;   % 线性插值
frozen.beta_Q = 0.5;
frozen.alpha_R = 0.5;
frozen.beta_R = 0.5;
frozen.alpha_dR = 0.5;
frozen.beta_dR = 0.5;
frozen.scale_umin_lo = 1.0;  % 信任物理约束
frozen.scale_umin_hi = 1.0;
frozen.scale_umax_lo = 1.0;
frozen.scale_umax_hi = 1.0;
frozen.tau = 0.35;           % rho滤波常数
% 场景自适应默认值（Phase 1时固定）
% 场景自适应默认值（完整列表，确保objective_wrapper不会缺字段）
frozen.omega_threshold = 0.15;
frozen.q_y_gain_max = 1.0;           % 不放大 = 关闭自适应
frozen.theta_threshold = 0.04;
frozen.q_v_gain_max = 1.0;
frozen.transition_width = 0.03;      % 默认过渡宽度
frozen.theta_transition_width = 0.02;
frozen.R_F_gain_max_uphill = 1.0;    % 控制增益（不放大）
frozen.R_F_gain_max_downhill = 1.0;
frozen.dR_F_gain_max_uphill = 1.0;
frozen.dR_F_gain_max_downhill = 1.0;

% [新增] 传递路径文件和分区配置 (加载模式)
if isfield(options, 'path_file'), frozen.path_file = options.path_file; end
if isfield(options, 'zones'), frozen.zones = options.zones; end

%% 变量定义（根据Phase选择不同变量集）
switch phase
    case 1
        % ===== Phase 1: 核心权重优化 (8个变量) =====
        % 目标：搞定直道、缓弯和微小干扰
        fprintf('[Phase 1] 核心权重优化 (8个变量)\n');
        vars = [
            % --- 状态误差权重 Q ---
            optimizableVariable('q_y',[10,150],'Type','real');     % 横向误差惩罚（S弯关键）[上界150←0100，前次优化达上界99.45]
            optimizableVariable('q_psi',[15,100],'Type','real');   % 航向误差惩罚（方向稳定性）
            optimizableVariable('q_v',[3.0,50],'Type','real');     % 速度误差惩罚（坡道爬坡）[上界50←35，前次优化达上界]
            optimizableVariable('q_omega',[0.5,1.5],'Type','real');  % 角速度误差惩罚 [上界1.5←4.0，防止过度惩罚导致振荡]
            % --- 控制量权重 R ---
            optimizableVariable('log10_r_F',[-4.0,-0.5],'Type','real');    % 驱动力惩罚 (10^-4 ~ 10^-0.5)
            optimizableVariable('log10_r_omega',[-4.5,-1.0],'Type','real');% 角速度指令惩罚 [上界-1.0←-1.5，前次优化达上界]
            % --- 控制增量权重 dR ---
            optimizableVariable('log10_rdF',[-2.5,0],'Type','real');       % 驱动力平滑性[上界0←-1]
            optimizableVariable('log10_rdw',[-2.5,-0.5],'Type','real');    % 角速度平滑性 [放宽上限以允许更强平滑]
        ];
        
    case 2
        % ===== Phase 2: 场景自适应优化 (4个变量) =====
        % 前提：Phase 1的核心权重已固定
        fprintf('[Phase 2] 场景自适应优化 (4个变量)\n');
        
        % 检查Phase 1结果是否传入
        if ~isfield(options, 'phase1_result')
            error('Phase 2需要传入options.phase1_result（Phase 1的最优解）');
        end
        p1 = options.phase1_result;
        
        % 将Phase 1结果加入frozen
        frozen.q_y = p1.q_y;
        frozen.q_psi = p1.q_psi;
        frozen.q_v = p1.q_v;
        frozen.q_omega = p1.q_omega;
        frozen.log10_r_F = p1.log10_r_F;
        frozen.log10_r_omega = p1.log10_r_omega;
        frozen.log10_rdF = p1.log10_rdF;
        frozen.log10_rdw = p1.log10_rdw;
        
        vars = [
            % --- 弯道自适应 ---
            optimizableVariable('omega_threshold',[0.08,0.50],'Type','real');  % 弯道触发阈值 [rad/s] [下限0.08←0.03，防止伪最优全程放大]
            optimizableVariable('q_y_gain_max',[0.5,6.0],'Type','real');       % 弯道横向权重放大倍数 [0.5,6.0]←[0.5,4.0]，前次优化达上界
            % --- 坡道自适应 ---
            optimizableVariable('theta_threshold',[0.01,0.15],'Type','real');  % 坡道触发阈值 [rad] [上限0.15←0.12，复合区实际坡度超內06.88°]
            optimizableVariable('q_v_gain_max',[1.0,4.0],'Type','real');       % 坡道速度权重放大倍数 [扩展1.0-4.0←1.2-2.5，优化达上界]
            % --- 坡道控制增益 ---
            % 语义：R_interp(1) = R_interp(1) / R_F_gain_max_uphill
            %       增益越大，上坡驱动力惩罚越小，更倾向保速爬坡
            optimizableVariable('R_F_gain_max_uphill',[1.0,2.5],'Type','real');
        ];
        
    case 3
        % ===== Phase 3: 全量微调 (可选) =====
        fprintf('[Phase 3] 全量微调 (12个变量)\n');
        
        % 检查Phase 2结果
        if ~isfield(options, 'phase2_result')
            error('Phase 3需要传入options.phase2_result');
        end
        
        % 使用前两阶段结果作为初始点，小范围搜索
        % TODO: 根据需要实现
        error('Phase 3暂未实现，请使用Phase 1/2');
        
    otherwise
        error('未知的优化阶段: %d (支持 1, 2, 3)', phase);
end

fprintf('[Bayesian_Optimization] 优化变量数: %d\n', numel(vars));

%% 场景权重配置
% V3.5: 按功能分区定义（共6个区，与路径时间段对应）
% 可通过 options.scenes 覆盖
if ~isfield(options,'scenes')
    scenes = struct(...
        'startup',0.05, ...       % 0-10s: 启动区（低权重）
        'golden_test',0.20, ...   % 10-50s: 黄金测试区
        'pure_turn',0.25, ...     % 50-70s: 纯转弯区（S弯120°）
        'pure_slope',0.20, ...    % 70-90s: 纯坡度区
        'composite',0.25, ...     % 90-110s: 复合区（坡度+转弯耦合）
        'closure',0.05);          % 110-120s: 闭环区（低权重）
    fprintf('[Bayesian_Optimization] 使用V3.5功能分区权重。\n');
else
    scenes = options.scenes;
    fprintf('[Bayesian_Optimization] 使用自定义场景权重。\n');
end
fprintf('[Bayesian_Optimization]   startup=%.2f, golden=%.2f, turn=%.2f, slope=%.2f, composite=%.2f, closure=%.2f\n', ...
    scenes.startup, scenes.golden_test, scenes.pure_turn, scenes.pure_slope, scenes.composite, scenes.closure);

% === 步骤1修复：主进程预创建 base_ctrl，解决并行随机性 ===
% 原方案：每个并行 worker 各自通过 persistent 变量在首次调用时初始化 base_ctrl，
% 时序不可控导致同参数两次仿真 J 值差异可达 1 量级。
% 新方案：在主进程（单线程）中创建唯一的 base_ctrl 实例，
% 写入 frozen.base_ctrl 后随匿名函数广播到所有 worker（MATLAB 自动序列化）。
fprintf('[Bayesian_Optimization] 主进程预创建基准控制器（消除并行随机性）...\n');
base_opts_main = struct(...
    'Np', 150, 'Nc', 50, ...          % 与 preloadfcn_v2 TARGET_NP/NC 对齐（1.5s/0.5s 时域）
    'Q',[10,15,2,1], ...
    'R',[1e-3,1e-3], ...
    'dR',[1e-2,1e-2], ...
    'umin',[-600; -1.2], ...
    'umax',[600; 1.2], ...
    'dumin',[-400; -0.9], ...
    'dumax',[400; 0.9]);
evalc('base_ctrl_main = mpc_setup_single_interp(db, base_opts_main);');
frozen.base_ctrl = base_ctrl_main;
fprintf('[Bayesian_Optimization] 基准控制器已写入 frozen.base_ctrl，各 worker 将复用此唯一实例。\n');

% 目标函数封装（传入frozen以合并未优化的参数，含 base_ctrl）
obj = @(X) objective_wrapper(X, frozen, params, db, scenes);

%% bayesopt 配置
% 默认配置：MaxObjectiveEvaluations=100, UseParallel=false
% 可通过 options 覆盖：
%   options.MaxObjectiveEvaluations = 50;  % 修改迭代次数
%   options.save_history = true;           % 保存优化历史
boOpts = struct();
boOpts.AcquisitionFunctionName = 'expected-improvement-plus';
boOpts.IsObjectiveDeterministic = false;  % V2.11: 并行仿真存在随机性，声明为false使代理模型使用噪声感知GP
boOpts.Verbose = 1;
boOpts.PlotFcn = [];
boOpts.MaxObjectiveEvaluations = 10;  % V3.5快速验证（原3）
boOpts.UseParallel = true;  % 启用并行计算（需先执行 parpool）

% 从 options 中覆盖配置
if isfield(options,'MaxObjectiveEvaluations')
    boOpts.MaxObjectiveEvaluations = options.MaxObjectiveEvaluations;
end
if isfield(options,'UseParallel')
    boOpts.UseParallel = options.UseParallel;  % 用户配置并行开关
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
[bestJ_pred, best_pred] = objective_wrapper(bestRow_pred, frozen, params, db, scenes);

% 获取第一阶段实际观察到的最小代价点
all_objectives_stage1 = boResults.ObjectiveTrace;
min_objective_stage1 = min(all_objectives_stage1);
min_idx_stage1 = find(all_objectives_stage1 == min_objective_stage1, 1, 'first');
min_row_stage1 = boResults.XTrace(min_idx_stage1,:);

fprintf('[Bayesian_Optimization] 第一阶段完成：\n');
fprintf('[Bayesian_Optimization]   bestPoint预测最优: J = %.6f (仅供参考，不参与决策)\n', bestJ_pred);
fprintf('[Bayesian_Optimization]   实际观察最小值: J = %.6f (迭代 #%d) ← 采用此值\n', min_objective_stage1, min_idx_stage1);

% V2.12修复：始终采用实际观测最优，不再与代理预测值比较
% 原因：IsObjectiveDeterministic=false时代理模型预测值有较大不确定性，
% 实际采样结果（min_objective_stage1）是唯一可信的真实评估结果。
best = best_pred;  % 先赋初值，下面用 min_row_stage1 重新评估覆盖
bestRow = min_row_stage1;
[bestJ, best] = objective_wrapper(bestRow, frozen, params, db, scenes);
fprintf('[Bayesian_Optimization]   ✓ 以实际观测最优点重新评估确认: J = %.6f\n', bestJ);

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
if ~isfield(local_refine,'shrink'),     local_refine.shrink = 0.5; end
% 局部优化次数：优先使用 options.local_refine_evals，否则按比例计算
if isfield(options, 'local_refine_evals') && options.local_refine_evals > 0
    local_refine.num_evals = options.local_refine_evals;  % 用户手动指定
elseif ~isfield(local_refine,'num_evals')
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

    % 局部边界（以实际观测最优 min_row_stage1 为中心、按 shrink 收缩）
    % V2.11修复: 原来以 bestRow（代理模型预测）为中心，但存在随机性时预测值不可信，
    % 改为以第一阶段实际观测到的最小代价点为中心，确保局部搜索在有效区域展开。
    vars_local = optimizableVariable.empty(0, nVar);
    locLo = zeros(nVar,1); locHi = zeros(nVar,1);
    for i = 1:nVar
        c  = min_row_stage1.(varNames{i});  % V2.11: 以实际观测最优为中心，而非代理模型预测的bestPoint
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
    [J_verify, result_verify] = objective_wrapper(bestRow, frozen, params, db, scenes);
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
    [bestJ2, best2] = objective_wrapper(bestRow2, frozen, params, db, scenes);

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

    % 步骤5：确定最终结果（V2.12修复：统一使用实际观测值比较，不再混入代理预测值）
    % 情况1：第二阶段实际采样未优于第一阶段实际采样 → 保留第一阶段结果
    % 情况2：第二阶段实际采样优于第一阶段实际采样 → 采用第二阶段结果

    % 使用 min_objective_stage1（实际观测值）作为比较基准，而非 bestJ_final（可能含预测值）
    if isfinite(min_objective_stage2) && (min_objective_stage2 < min_objective_stage1)
        % 情况2：第二阶段找到更好结果（两个都是实际采样，比较可信）
        fprintf('[LocalRefine] ✓ 情况2: 第二阶段找到更优解！采用全局最小结果（改进: %.6f）\n', min_objective_stage1 - min_objective_stage2);
        [bestJ_global, best_global] = objective_wrapper(min_row_stage2, frozen, params, db, scenes);
        boResults_final = boResults2; best_final = best_global; bestJ_final = bestJ_global; bestRow_final = min_row_stage2;
    else
        % 情况1：第二阶段没找到更好结果，保存第一阶段实际最优
        fprintf('[LocalRefine] ◯ 情况1: 第二阶段未找到更好结果，采用第一阶段实际最优\n');
        fprintf('[LocalRefine]   第二阶段实际最小: J = %.6f, 第一阶段实际最小: J = %.6f\n', min_objective_stage2, min_objective_stage1);
        % best_final/bestJ_final/bestRow_final 已在第266行基于min_row_stage1设置，直接保留
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
    history_dir = fullfile(results_dir, 'bo', 'history');
    if ~exist(history_dir, 'dir'), mkdir(history_dir); end
    history_file = fullfile(history_dir, sprintf('bo_history_%s.mat', datestr(now,'yyyymmdd_HHMMSS')));
    boResults = boResults_final; %#ok<NASGU>
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

function [J, out] = objective_wrapper(X, frozen, params, db, scenes)
% =============================
% objective_wrapper - 目标函数封装
%
% 输入:
%   X      - bayesopt优化变量（table类型，只包含当前阶段变量）
%   frozen - 冻结参数（struct类型，包含所有不参与优化的固定值）
%   params - 系统参数
%   db     - LPV模型数据库
%   scenes - 场景权重配置
%
% 核心机制:
%   bayesopt的X只包含当前Phase被优化的变量。
%   frozen包含所有其他变量的固定值。
%   合并后的P包含完整的参数集。
% =============================

% [步骤2修复] 已删除 persistent base_ctrl，改为从 frozen.base_ctrl（即P.base_ctrl）读取。
% 原 persistent 方案在并行 worker 中各自独立初始化，时序不可控，引入大幅随机性。

%% === 关键修复：合并优化变量X与冻结参数frozen ===
% 1. 首先复制frozen作为基础
P = frozen;

% 2. 用X中的优化变量覆盖P中的同名变量
% 注意：X是table类型（bayesopt特性），需逐个字段覆盖
if istable(X)
    var_names = X.Properties.VariableNames;
    for i = 1:length(var_names)
        vn = var_names{i};
        P.(vn) = X.(vn);
    end
elseif isstruct(X)
    % 如果X是struct（手动调用时可能发生）
    fn = fieldnames(X);
    for i = 1:length(fn)
        P.(fn{i}) = X.(fn{i});
    end
end

%% 从合并后的P读取所有参数（而非从X直接读取）
cfg = struct();
cfg.tau = P.tau;
% [新增] 传递路径配置到 Cost_Function
if isfield(P, 'path_file'), cfg.path_file = P.path_file; end
if isfield(P, 'zones'), cfg.zones = P.zones; end

% 权重与范围
Q0 = [P.q_y, P.q_psi, P.q_v, P.q_omega];
R0 = [10^(P.log10_r_F), 10^(P.log10_r_omega)];
dR0= [10^(P.log10_rdF), 10^(P.log10_rdw)];

% 形状参数:强制 alpha <= beta（修正非法值）
alpha_Q_val = min(P.alpha_Q, P.beta_Q);  % 取小者作为 alpha
beta_Q_val  = max(P.alpha_Q, P.beta_Q);  % 取大者作为 beta
alpha_R_val = min(P.alpha_R, P.beta_R);
beta_R_val  = max(P.alpha_R, P.beta_R);
alpha_dR_val= min(P.alpha_dR, P.beta_dR);
beta_dR_val = max(P.alpha_dR, P.beta_dR);

alpha_Q = repmat(alpha_Q_val, 1, 4);
beta_Q  = repmat(beta_Q_val, 1, 4);
alpha_R = repmat(alpha_R_val, 1, 2);
beta_R  = repmat(beta_R_val, 1, 2);
alpha_dR= repmat(alpha_dR_val, 1, 2);
beta_dR = repmat(beta_dR_val, 1, 2);

% 约束缩放（使用冻结的固定值）
scale_umin_lo = [P.scale_umin_lo, P.scale_umin_lo];
scale_umin_hi = [P.scale_umin_hi, P.scale_umin_hi];
scale_umax_lo = [P.scale_umax_lo, P.scale_umax_lo];
scale_umax_hi = [P.scale_umax_hi, P.scale_umax_hi];

% 构建 ctrl（只在第一次调用时创建基准控制器，后续复用）
if isempty(db)
    fprintf('[Bayesian_Optimization] db 为空，生成默认 7x7x5 网格...\n');
    root = project_root();
    data_models_dir = fullfile(root, 'data', 'models');
    grid.V_grid = linspace(0.1, 1.2, 7)';   % 速度 [m/s]，覆盖启动/减速
    grid.W_grid = linspace(-1.2, 1.2, 7)';  % 角速度 [rad/s]，与 MPC omega_cmd 约束一致
    grid.T_grid = linspace(-0.2, 0.2, 7)';% 坡度 [rad]，覆盖±11.5°
    lin_opts = struct('coord','path','disc','zoh','keep_E',true, ...
        'export_mat', fullfile(data_models_dir, 'plant_grid_test.mat'));
    db = lin_agv_grid(params, grid, lin_opts);
    fprintf('[Bayesian_Optimization] 默认网格生成完成。\n');
end

% [步骤2修复] base_ctrl 由主进程预创建并通过 frozen.base_ctrl 传入，此处直接读取。
% 所有并行 worker 共享同一个预创建的控制器实例，消除初始化时序随机性。
base_ctrl = P.base_ctrl;

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
ctrl.maps.tau = P.tau;

% 场景自适应参数（从合并后的P读取）
ctrl.maps.omega_threshold          = P.omega_threshold;
ctrl.maps.transition_width        = P.transition_width;
ctrl.maps.q_y_gain_max           = P.q_y_gain_max;
ctrl.maps.theta_threshold        = P.theta_threshold;
ctrl.maps.theta_transition_width = P.theta_transition_width;
ctrl.maps.q_v_gain_max           = P.q_v_gain_max;
ctrl.maps.R_F_gain_max_uphill    = P.R_F_gain_max_uphill;
ctrl.maps.R_F_gain_max_downhill  = P.R_F_gain_max_downhill;
ctrl.maps.dR_F_gain_max_uphill   = P.dR_F_gain_max_uphill;
ctrl.maps.dR_F_gain_max_downhill = P.dR_F_gain_max_downhill;

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
