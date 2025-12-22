function [J, report] = Cost_Function(params, db, cfg, scenes)
% =============================
% 文件名：Cost_Function.m
% 版本号：V2.4
% 最后修改时间：2025-11-20
% 作者：LPV-MPC Project
% 功能描述：
%   复现 Adaptive MPC 闭环，输出加权代价 J 和详细报告
% 输入参数：
%   - params : parameters() 返回的结构体
%   - db     : LPV 数据库（允许为空，内部生成3×3×3默认网格）
%   - cfg    : 结构体，包含权重/范围/滤波/罚值/超参（可选字段见下）
%   - scenes : 结构体，场景权重（字段：turn/slope/straight_turn/bumpy/straight）
% 输出参数：
%   - J      : 总加权代价（若任一场景失败，J >= 1e6）
%   - report : 详细报告（各场景指标、RMSE、Δu、约束违反、求解时间统计、失败次数）
% 依赖：
%   - mpc_setup_single_interp.m / mpc_update_from_rho.m
%   - gen_agv_ref_path.m / state_eq_ref.m / output_eq_ref.m
% 备注：
%   - 统一ρ为有符号：rho=[v; omega; theta]
%   - 颠簸默认幅值 0.2 rad
%   - API 调用：[u, Info] = mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md)
%     其中 plant_model 每步更新，Nominal.U 为 3×1（2 MV + 1 MD）
%   - 成功判定：Info.QPCode == 'feasible' 或 'optimal'
%   - V2.3更新：移除前馈力F_eq，MPC直接输出完整控制力（包含阻力补偿）
% =============================

%% 默认配置
if nargin < 4 || isempty(scenes)
    scenes = struct('turn',0.35,'slope',0.10,'straight_turn',0.10,'bumpy',0.35,'straight',0.10);
end
if nargin < 3 || isempty(cfg)
    cfg = struct();
end

if ~isfield(cfg,'tau'), cfg.tau = 0.4; end                    % ρ滤波时间常数
if ~isfield(cfg,'ey_max'), cfg.ey_max = 1.0; end              % 放宽以匹配 MPC 约束
if ~isfield(cfg,'epsi_max'), cfg.epsi_max = 0.5; end          % 放宽以匹配 MPC 约束
if ~isfield(cfg,'ev_max'), cfg.ev_max = 0.5; end
if ~isfield(cfg,'eomega_max'), cfg.eomega_max = 0.3; end
if ~isfield(cfg,'dF_max'), cfg.dF_max = 400; end
if ~isfield(cfg,'dw_max'), cfg.dw_max = 0.4; end
if ~isfield(cfg,'debug'), cfg.debug = false; end

% 安全范围（log10 映射防止负权重）
clip = @(x,lo,hi) min(hi,max(lo,x));

%% LPV 数据库准备
if nargin < 2 || isempty(db)
    grid.V_grid = [0.8; 1.0; 1.2];
    grid.W_grid = [-0.2; 0.0; 0.2];      % 有符号 ω
    grid.T_grid = [-0.2; 0.0; 0.2];      % 颠簸幅值匹配 0.2 rad
    lin_opts = struct('coord','path','disc','zoh','keep_E',true,'export_mat','plant_grid.mat');
    db = lin_agv_grid(params, grid, lin_opts);
end

%% 控制器准备（优先使用传入的ctrl，避免重复创建）
if isfield(cfg, 'ctrl') && ~isempty(cfg.ctrl)
    % 使用传入的控制器（来自 Bayesian_Optimization）
    % 注意：cfg.ctrl 已经是独立副本（在 Bayesian_Optimization 中克隆）
    ctrl = cfg.ctrl;
else
    % 创建默认控制器（独立测试时）
    ctrl = mpc_setup_single_interp(db, struct());
end

% 提取 mpcobj（注意：这是引用，后续修改会影响 ctrl.mpcobj）
mpcobj = ctrl.mpcobj;
Ts = db.Ts;

% 如果cfg中提供了maps覆盖，应用到ctrl.maps
% 注意：直接修改 ctrl.maps，但因为 ctrl 是独立副本，不会污染其他评估
if isfield(cfg,'ctrl_maps')
    fns = fieldnames(cfg.ctrl_maps);
    for i=1:numel(fns)
        ctrl.maps.(fns{i}) = cfg.ctrl_maps.(fns{i});
    end
end

% V2.3：已移除F_eq前馈，以下物理参数不再需要
% m = params.mass;
% g = params.gravity;
% c_r = params.rolling_resistance;
% rho_air = params.air_density;
% CdA = params.drag_coefficient_area;

%% 归一化端点（用于rho滤波初始化）
rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];

%% 场景列表
scene_order = {'turn','slope','straight_turn','bumpy','straight'};

J_total = 0;
report = struct();
report.scene = struct();
report.fail_count = 0;
report.scene_order = scene_order;

for s = 1:numel(scene_order)
    name = scene_order{s};
    if ~isfield(scenes,name), continue; end
    weight_s = scenes.(name);

    try
        % 生成参考（使用 gen_agv_ref_path 的默认参数，包括 bumpy_amp=deg2rad(5) 和 6s 延迟）
        ref = gen_agv_ref_path(name, params, struct('T_end',20));
        N = numel(ref.t);

        % 初始状态：8维 [X Y psi v omega delta_lf delta_rr beta]
        x_plant = [params.initial_x; params.initial_y; params.initial_heading; ...
                   params.initial_velocity; params.initial_angular_velocity; ...
                   params.initial_front_steering; params.initial_rear_steering; ...
                   params.initial_sideslip];

        % MPC状态初始化
        xmpc = mpcstate(mpcobj);

        % 统计量
        ey = zeros(N,1); epsi = zeros(N,1); ev = zeros(N,1); eomega = zeros(N,1);
        u_hist = zeros(N,2); du_hist = zeros(N,2);
        solve_ms = zeros(N,1);
        cons_violation = zeros(N,1);

        u_prev = [0; 0];
        rho_prev = [ref.v_ref(1); ref.omega_ref(1); ref.theta_ref(1)];
        fail_scene = false;

        for k = 1:N
            %% 1. 从8维状态计算4维路径坐标系误差
            X = x_plant(1); Y = x_plant(2); psi = x_plant(3);
            v = x_plant(4); omega = x_plant(5);
            
            X_ref = ref.X_ref(k); Y_ref = ref.Y_ref(k); psi_ref = ref.psi_ref(k);
            v_ref = ref.v_ref(k); omega_ref = ref.omega_ref(k);
            
            % 全局误差
            ex = X - X_ref;
            ey_global = Y - Y_ref;
            
            % 路径坐标系误差（Frenet坐标转换）
            e_y = -sin(psi_ref)*ex + cos(psi_ref)*ey_global;
            e_psi = wrapToPi(psi - psi_ref);
            e_v = v - v_ref;
            e_omega = omega - omega_ref;
            
            y_meas = [e_y; e_psi; e_v; e_omega];
            
            %% 2. 参考轨迹（误差期望为零）
            r_ref = [0; 0; 0; 0];
            
            %% 3. 测量扰动（坡度角）
            theta_meas = ref.theta_ref(k);
            md = theta_meas;
            
            %% 4. 组装 rho（有符号）并一阶滤波
            rho_cur = [v_ref; omega_ref; theta_meas];
            rho_filter_alpha = Ts / (Ts + cfg.tau);
            rho_f = rho_filter_alpha * rho_cur + (1-rho_filter_alpha) * rho_prev;
            rho_prev = rho_f;
            
            %% 5. 在线插值模型与权重/约束
            upd = mpc_update_from_rho(rho_f, db, ctrl.maps);
            
            % 构造更新后的植物模型（离散状态空间）
            % B矩阵包含 [2个MV列, 1个MD列]
            B_updated = [upd.B, upd.E];  % [4×2] + [4×1] = [4×3]
            D_updated = [upd.D, zeros(4,1)];  % [4×2] + [4×1] = [4×3]
            
            plant_model = ss(upd.A, B_updated, upd.C, D_updated, Ts);
            
            % 构造 Nominal 结构体（工作点，所有为零 = 误差坐标系）
            Nominal = struct();
            Nominal.X = zeros(4,1);   % 状态工作点
            Nominal.U = zeros(3,1);   % 输入工作点（2 MV + 1 MD）
            Nominal.Y = zeros(4,1);   % 输出工作点
            Nominal.DX = zeros(4,1);  % 状态导数工作点
            
            % 更新权重（通过修改 mpcobj 属性）
            mpcobj.Weights.OutputVariables = upd.Q;
            mpcobj.Weights.ManipulatedVariables = upd.R;
            mpcobj.Weights.ManipulatedVariablesRate = upd.dR;
            
            % 更新约束
            mpcobj.MV(1).Min = upd.umin(1); mpcobj.MV(1).Max = upd.umax(1);
            mpcobj.MV(2).Min = upd.umin(2); mpcobj.MV(2).Max = upd.umax(2);
            
            %% 6. MPC求解（mpcmoveAdaptive）
            % V2.3：移除F_eq前馈，MPC直接输出完整控制力
            % 使用 evalc 捕获并抑制所有输出（包括 fprintf/disp）
            tic;
            evalc('[u_mpc, Info] = mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md);');
            solve_time = toc * 1000;  % ms
            
            % V2.3：直接使用MPC输出，不再叠加前馈力
            u = u_mpc;
            
            %% 8. 检查求解状态
            % 使用 Info.QPCode 判定成功（字符串 'feasible' 或 'optimal'）
            if isfield(Info, 'QPCode')
                qp_success = strcmpi(Info.QPCode, 'feasible') || strcmpi(Info.QPCode, 'optimal');
                if ~qp_success
                    fail_scene = true;
                    if cfg.debug
                        fprintf('  [DEBUG] 步%d: QPCode=%s, 求解失败\n', k, Info.QPCode);
                        fprintf('         rho=[%.3f, %.5f, %.5f]\n', rho_f(1), rho_f(2), rho_f(3));
                        fprintf('         y_meas=[%.5f, %.5f, %.5f, %.5f]\n', ...
                            y_meas(1), y_meas(2), y_meas(3), y_meas(4));
                    end
                    break;
                end
            else
                % 回退：若无 QPCode，检查 Cost 是否为有限值
                if ~isfield(Info, 'Cost') || ~isfinite(Info.Cost)
                    fail_scene = true;
                    if cfg.debug
                        fprintf('  [DEBUG] 步%d: 无有效 Info 字段，求解失败\n', k);
                    end
                    break;
                end
            end
            
            %% 9. 约束违反检查
            cons_viol = 0;
            % 输出约束
            if abs(e_y) > cfg.ey_max + 1e-6, cons_viol = cons_viol + abs(e_y) - cfg.ey_max; end
            if abs(e_psi) > cfg.epsi_max + 1e-6, cons_viol = cons_viol + abs(e_psi) - cfg.epsi_max; end
            % MV约束（检查是否命中边界）
            if abs(u(1)) > abs(mpcobj.MV(1).Max) + 1e-6, cons_viol = cons_viol + abs(u(1)) - abs(mpcobj.MV(1).Max); end
            if abs(u(2)) > abs(mpcobj.MV(2).Max) + 1e-6, cons_viol = cons_viol + abs(u(2)) - abs(mpcobj.MV(2).Max); end
            
            %% 10. 推进Plant状态（使用state_eq_ref）
            x_plant = state_eq_ref(x_plant, u, theta_meas, params);
            
            %% 11. 记录
            ey(k) = e_y; epsi(k) = e_psi; ev(k) = e_v; eomega(k) = e_omega;
            u_hist(k,:) = u.';
            du_hist(k,:) = (u - u_prev).';
            u_prev = u;
            solve_ms(k) = solve_time;
            cons_violation(k) = cons_viol;
            
            %% 12. 失败判定
            if any(~isfinite([e_y, e_psi, e_v, e_omega])) || any(~isfinite(u))
                fail_scene = true;
                break;
            end
        end

        % 代价计算
        RMSE = @(z) sqrt(mean(z.^2)); RMS = @(z) sqrt(mean(z.^2));
        J_trk = 1.1*RMSE(ey)/cfg.ey_max + 1.0*RMSE(epsi)/cfg.epsi_max + 0.2*RMSE(eomega)/cfg.eomega_max + 0.1*RMSE(ev)/cfg.ev_max;
        J_smooth = 0.08*RMS(du_hist(:,1))/cfg.dF_max + 0.07*RMS(du_hist(:,2))/cfg.dw_max;

        % 约束惩罚（L1/L∞ 混合）
        L1 = mean(abs(cons_violation)); Linf = max(abs(cons_violation));
        J_cons = 10*L1 + 50*Linf;

        % 实时惩罚
        avg_ms = mean(solve_ms); max_ms = max(solve_ms);
        J_rt = max(0, (avg_ms - 5.0)/5.0) + (max_ms > 10.0)*0.5;

        J_scene = J_trk + J_smooth + J_cons + J_rt;

        if fail_scene
            J_scene = 1e6; report.fail_count = report.fail_count + 1; end

        J_total = J_total + weight_s * J_scene;

        % 报告
        rep = struct();
        rep.RMSE = struct('ey',RMSE(ey),'epsi',RMSE(epsi),'ev',RMSE(ev),'eomega',RMSE(eomega));
        rep.RMS_du = struct('dF',RMS(du_hist(:,1)),'dw',RMS(du_hist(:,2)));
        rep.cons = struct('L1',L1,'Linf',Linf);
        rep.solve_ms = struct('avg',avg_ms,'max',max_ms);
        rep.failed = fail_scene;
        report.scene.(name) = rep;

    catch ME
        % 场景失败：记大罚，不中断其它场景
        J_total = J_total + weight_s * 1e6;
        report.fail_count = report.fail_count + 1;
        report.scene.(name) = struct('error',ME.message,'failed',true);
    end
end

J = J_total;

% 总体失败标记（只要有一个场景失败即置位）
report.failed = report.fail_count > 0;
report.timestamp = datestr(now,'yyyy-mm-dd HH:MM:SS');

% 可选落盘（根目录）
if isfield(cfg,'save_report') && cfg.save_report
    save(sprintf('bo_report_%s.mat',datestr(now,'yyyymmdd_HHMMSS')),'J','report');
end

end
