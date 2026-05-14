% =============================
% 文件名：test_industrial_open_loop_items.m
% 功能描述：按 Industrial 参考路径(ref.meta.segments)分项进行开环工况验证（含串联/动态评估）
% 说明：
%   - 目标是验证“模型本体”在典型工况下能否产生合理响应（不依赖 MPC 纠偏）
%   - 支持两种模式：
%       * independent: 每段独立（稳态评估）
%       * serial: 串联段落（动态与耦合评估）
%   - 每段使用 ref 信号统计得到的 v/omega/theta 进行开环指令
%   - 参考数据来源：data/paths/path_industrial.mat
% =============================

clc; clear;
fprintf('=== Industrial Path 分项开环验证脚本 (V1.1) ===\n');

%% 加载参数
params = parameters();
Ts = params.Ts;
m = params.mass;
g = params.gravity;
c_r = params.rolling_resistance;
rho_air = params.air_density;
CdA = params.drag_coefficient_area;

% 有效质量（包含电机/车轮转动惯量）
r_wheel = params.wheel_radius;
n_gear = params.gear_ratio;
Jw = params.wheel_inertia;
Jm = params.motor_inertia;
m_eff = m + 2*(Jw + Jm*n_gear^2) / r_wheel^2;

%% 读取当前 Industrial 路径元数据（基于脚本位置定位工程根目录）
script_dir = fileparts(mfilename('fullpath'));
project_root = fileparts(fileparts(script_dir));
p = fullfile(project_root, 'data', 'paths', 'path_industrial.mat');
S = load(p);
assert(isfield(S, 'ref'), 'path_industrial.mat 中未找到 ref');
ref = S.ref;
assert(isfield(ref, 'meta') && isfield(ref.meta, 'segments'), 'ref.meta.segments 不存在');
segments = ref.meta.segments;

assert(isfield(ref, 't') && isfield(ref, 'v_ref') && isfield(ref, 'omega_ref') && isfield(ref, 'theta_ref'), ...
    'ref 中缺少 t/v_ref/omega_ref/theta_ref');
ref_t = ref.t(:);
ref_v = ref.v_ref(:);
ref_omega = ref.omega_ref(:);
ref_theta = ref.theta_ref(:);
assert(isfield(ref, 'X_ref') && isfield(ref, 'Y_ref') && isfield(ref, 'psi_ref'), ...
    'ref 中缺少 X_ref/Y_ref/psi_ref');
ref_X = ref.X_ref(:);
ref_Y = ref.Y_ref(:);
ref_psi = ref.psi_ref(:);

% 参考加速度（用于前馈力）
ref_vdot = gradient(ref_v, ref_t);

fprintf('ref.meta.version: %s\n', safeGetField(ref.meta, 'version', 'N/A'));
fprintf('ref.meta.generation_time: %s\n', safeGetField(ref.meta, 'generation_time', 'N/A'));

%% 测试模式与覆盖策略（可用环境变量覆盖）
% 可选：
%   INDUSTRIAL_OPEN_LOOP_MODE = serial / independent
%   INDUSTRIAL_OPEN_LOOP_INCLUDE_ALL = 1/0
%   INDUSTRIAL_OPEN_LOOP_INCLUDE_ISOLATION = 1/0
mode = getConfigStr('INDUSTRIAL_OPEN_LOOP_MODE', 'serial');
include_all = getConfigBool('INDUSTRIAL_OPEN_LOOP_INCLUDE_ALL', true);
include_isolation = getConfigBool('INDUSTRIAL_OPEN_LOOP_INCLUDE_ISOLATION', true);

% 指令生成方式：
%   ref_replay: 段内按 ref(t) 逐步回放 (F/omega/theta 均可时变)
%   piecewise_constant: 段内用常值近似（更接近“工况稳态验证”）
command_profile = getConfigStr('INDUSTRIAL_OPEN_LOOP_COMMAND_PROFILE', 'ref_replay');

%% 从 segments 构造待测段列表
cases = {};
for i = 1:numel(segments)
    seg = segments(i);
    typ = char(seg.type);
    desc = char(seg.desc);

    dur = seg.t_end - seg.t_start;
    if dur <= 0
        continue;
    end

    if ~include_all
        isKey = false;
        switch typ
            case {'left_turn','right_turn'}
                isKey = true;
            case 'straight'
                if abs(seg.slope) > deg2rad(0.1)
                    isKey = true;
                end
        end
        if ~isKey
            continue;
        end
    end

    if ~include_isolation && contains(desc, '隔离')
        continue;
    end

    cases(end+1, :) = {i, typ, desc, dur, seg.t_start, seg.t_end}; %#ok<SAGROW>
end

fprintf('\n待测段数量：%d（mode=%s, include_all=%d）\n', size(cases,1), mode, include_all);

%% 测试配置
min_run_time = 6.0;       % independent 模式每段最短仿真时长
steady_window = 2.0;      % 末尾稳态统计窗口
min_rmse_eval_dur = 0.5;  % 段太短时不做 RMSE 判定（用端点/符号替代）

% 容差（可根据模型实际调整）
v_tol = 0.10;             % m/s（稳态均值）
omega_rel_tol = 0.15;     % 相对误差（稳态均值）
omega_abs_tol = 0.02;     % rad/s (omega_cmd≈0 时)
v_rmse_tol = 0.12;        % m/s（动态 RMSE）
omega_rmse_tol = 0.08;    % rad/s（动态 RMSE）
v_end_tol = 0.20;         % m/s（短段/加减速段端点速度误差）
omega_end_tol = 0.06;     % rad/s（短段端点角速度误差）

% 诊断阈值（用于全程统计）
slip_ratio_warn = 0.20;   % 纵向滑移率警戒阈值
beta_warn_deg = 5.0;      % 质心侧偏角警戒阈值 [deg]

%% 逐段执行
results = struct('idx',{},'type',{},'desc',{},'pass',{},'v_mean',{},'omega_mean',{},'theta_g',{},'note',{},'v_rmse',{},'omega_rmse',{},'v_end_err',{},'omega_end_err',{});

% 串联模式初值
x0_serial = zeros(8,1);
x0_serial(4) = 0; % 从静止开始

% 全程记录
t_global = [];
x_global = [];
u_global = [];
theta_global = [];

for k = 1:size(cases,1)
    idx = cases{k,1};
    typ = cases{k,2};
    desc = cases{k,3};
    dur = cases{k,4};
    t_start = cases{k,5};
    t_end_ref = cases{k,6};

    [v_ref_mean, omega_ref_mean, theta_ref_mean, vdot_ref_mean] = refSegmentStats(ref_t, ref_v, ref_omega, ref_theta, t_start, t_end_ref);
    [v_ref_steady_mean, omega_ref_steady_mean] = refSteadyStats(ref_t, ref_v, ref_omega, t_start, t_end_ref, steady_window);

    if strcmpi(mode, 'independent')
        t_end = max(dur, min_run_time);
        x0 = zeros(8,1);
        x0(4) = max(v_ref_mean, 0);
    else
        t_end = max(dur, Ts);
        x0 = x0_serial;
    end

    if strcmpi(command_profile, 'ref_replay')
        % 段内按 ref(t) 回放：F/omega/theta 都随时间变化
        u_fun = @(t_local) [ ...
            computeForceFromRef(t_start + t_local, ref_t, ref_v, ref_vdot, ref_theta, m, g, c_r, rho_air, CdA, m_eff); ...
            interp1(ref_t, ref_omega, t_start + t_local, 'linear', 'extrap') ...
        ];
        theta_fun = @(t_local) interp1(ref_t, ref_theta, t_start + t_local, 'linear', 'extrap');
        [t, states] = simulate_core_tv(t_end, u_fun, theta_fun, x0, params);
        theta_g = theta_ref_mean;
        omega_cmd = omega_ref_mean;
    else
        % 段内常值近似：使用段均值（更接近“稳态工况”）
        theta_g = theta_ref_mean;
        omega_cmd = omega_ref_mean;
        F_ff = computeForceToTrackSpeedAndAccel(v_ref_mean, vdot_ref_mean, theta_g, m, g, c_r, rho_air, CdA, m_eff);
        u_fun = @(t_local) [F_ff; omega_cmd];
        theta_fun = @(t_local) theta_g;
        [t, states] = simulate_core(t_end, [F_ff; omega_cmd], theta_g, x0, params);
    end

    if strcmpi(mode, 'serial')
        x0_serial = states(end, :)';
    end

    % 记录本段输入/坡度（用于全程统计）
    u_hist = zeros(numel(t), 2);
    theta_hist = zeros(numel(t), 1);
    for ii = 1:numel(t)
        u_hist(ii, :) = u_fun(t(ii))';
        theta_hist(ii) = theta_fun(t(ii));
    end

    t_abs = t_start + t;
    if isempty(t_global)
        keep_idx = 1:numel(t_abs);
    else
        keep_idx = 2:numel(t_abs); % 避免段首重复点
    end
    t_global = [t_global; t_abs(keep_idx)]; %#ok<AGROW>
    x_global = [x_global; states(keep_idx, :)]; %#ok<AGROW>
    u_global = [u_global; u_hist(keep_idx, :)]; %#ok<AGROW>
    theta_global = [theta_global; theta_hist(keep_idx)]; %#ok<AGROW>

    % 动态对齐（与 ref 段内曲线比较）
    t_eval = min(dur, t(end));
    ref_t_local = ref_t - t_start;
    idx_ref = ref_t >= t_start & ref_t <= t_end_ref;
    t_ref_seg = ref_t_local(idx_ref);
    v_ref_seg = ref_v(idx_ref);
    omega_ref_seg = ref_omega(idx_ref);

    t_sim = t(t <= t_eval);
    v_sim = states(1:numel(t_sim), 4);
    omega_sim = states(1:numel(t_sim), 5);

    v_ref_interp = interp1(t_ref_seg, v_ref_seg, t_sim, 'linear', 'extrap');
    omega_ref_interp = interp1(t_ref_seg, omega_ref_seg, t_sim, 'linear', 'extrap');

    v_rmse = sqrt(mean((v_sim - v_ref_interp).^2));
    omega_rmse = sqrt(mean((omega_sim - omega_ref_interp).^2));

    v_end_err = abs(v_sim(end) - v_ref_interp(end));
    omega_end_err = abs(omega_sim(end) - omega_ref_interp(end));

    % 末尾稳态统计（用于与 ref 同窗口对比）
    steady_idx = t > (t(end) - min(steady_window, t(end)));
    v_mean = mean(states(steady_idx, 4));
    omega_mean = mean(states(steady_idx, 5));

    % 判据（按段类型/段长做差异化）
    is_short = dur < min_rmse_eval_dur;
    is_accel = strcmpi(typ, 'accel');
    is_decel = strcmpi(typ, 'decel');

    pass_dyn = (v_rmse <= v_rmse_tol) && (omega_rmse <= omega_rmse_tol);
    pass_end = (v_end_err <= v_end_tol) && (omega_end_err <= omega_end_tol);

    % 稳态均值判据：只用于非加减速且段长足够的情况
    if ~(is_accel || is_decel) && ~is_short
        % 注意：必须与 ref 的“段末同一时间窗口”对齐，否则会把段内过渡当作稳态误差
        pass_v = abs(v_mean - v_ref_steady_mean) <= v_tol;
        omega_err = omega_mean - omega_ref_steady_mean;
        omega_allow = max(omega_abs_tol, omega_rel_tol * abs(omega_ref_steady_mean));

        if abs(omega_ref_steady_mean) < 0.05
            % 近零角速度不宜用相对误差（会被放大）
            pass_w = abs(omega_err) <= omega_abs_tol;
        else
            pass_w = abs(omega_err) <= omega_allow && sign(omega_mean) == sign(omega_ref_steady_mean);
        end
    else
        pass_v = true;
        pass_w = true;
    end

    if is_short
        pass = pass_end;
    else
        pass = pass_v && pass_w && pass_dyn;
    end

    note = '';
    if ~pass
        if is_short
            note = [note, sprintf('短段端点误差(v=%.3f, omega=%.4f); ', v_end_err, omega_end_err)];
        else
            if ~pass_v
                note = [note, sprintf('v偏差(%.3f vs %.3f); ', v_mean, v_ref_steady_mean)];
            end
            if ~pass_w
                note = [note, sprintf('omega偏差(%.4f vs %.4f); ', omega_mean, omega_ref_steady_mean)];
            end
            if ~pass_dyn
                note = [note, sprintf('RMSE(v=%.3f, omega=%.4f); ', v_rmse, omega_rmse)];
            end
        end
    end

    results(end+1) = struct( ...
        'idx', idx, ...
        'type', typ, ...
        'desc', desc, ...
        'pass', pass, ...
        'v_mean', v_mean, ...
        'omega_mean', omega_mean, ...
        'theta_g', theta_g, ...
        'note', note, ...
        'v_rmse', v_rmse, ...
        'omega_rmse', omega_rmse, ...
        'v_end_err', v_end_err, ...
        'omega_end_err', omega_end_err);

    fprintf('[%02d] %-10s | theta=%+5.2fdeg | omega_cmd=%+7.4f | v=%.3f | omega=%.4f | RMSE(v=%.3f, w=%.4f) | %s\n', ...
        idx, typ, rad2deg(theta_g), omega_cmd, v_mean, omega_mean, v_rmse, omega_rmse, ternary(pass,'PASS','FAIL'));
    if ~pass
        fprintf('     note: %s\n', note);
        fprintf('     desc: %s\n', desc);
    end
end

%% 汇总
pass_count = sum([results.pass]);
fprintf('\n=== 汇总：%d/%d 通过 ===\n', pass_count, numel(results));

fail_idx = find(~[results.pass]);
if ~isempty(fail_idx)
    fprintf('未通过段索引: ');
    fprintf('%d ', [results(fail_idx).idx]);
    fprintf('\n');
    fprintf('建议：优先查看这些段对应的 turn/slope 参数、以及模型的 omega 跟踪机制/输入限幅。\n');
else
    fprintf('所有关键工况段均满足开环验收判据。\n');
end

%% 全程统计：轨迹漂移 / 侧偏 / 滑移 / 网格覆盖
if ~isempty(t_global)
    % 轨迹误差（对齐参考）
    X_ref_interp = interp1(ref_t, ref_X, t_global, 'linear', 'extrap');
    Y_ref_interp = interp1(ref_t, ref_Y, t_global, 'linear', 'extrap');
    psi_ref_interp = interp1(ref_t, ref_psi, t_global, 'linear', 'extrap');

    X_err = x_global(:,1) - X_ref_interp;
    Y_err = x_global(:,2) - Y_ref_interp;
    psi_err = wrapToPi(x_global(:,3) - psi_ref_interp);

    fprintf('\n=== 全程轨迹误差统计 ===\n');
    fprintf('RMSE: X=%.3f m, Y=%.3f m, psi=%.3f deg\n', rms(X_err), rms(Y_err), rad2deg(rms(psi_err)));
    fprintf('终点误差: X=%.3f m, Y=%.3f m, psi=%.3f deg\n', X_err(end), Y_err(end), rad2deg(psi_err(end)));

    % 侧偏角与滑移率统计
    beta = x_global(:,8);
    beta_warn = abs(beta) > deg2rad(beta_warn_deg);

    slip_lf = nan(size(t_global));
    slip_rr = nan(size(t_global));
    for ii = 1:numel(t_global)
        y = output_eq_ref(x_global(ii,:)', u_global(ii,:)', theta_global(ii), params);
        slip_lf(ii) = y(32);
        slip_rr(ii) = y(33);
    end
    slip_warn = (abs(slip_lf) > slip_ratio_warn) | (abs(slip_rr) > slip_ratio_warn);

    fprintf('\n=== 侧偏/滑移统计 ===\n');
    fprintf('beta超限(>%.1fdeg): %d / %d (%.2f%%)\n', beta_warn_deg, sum(beta_warn), numel(beta_warn), 100*mean(beta_warn));
    fprintf('slip_ratio超限(>%.2f): %d / %d (%.2f%%)\n', slip_ratio_warn, sum(slip_warn), numel(slip_warn), 100*mean(slip_warn));

    % 输入饱和统计（按电机电流限制推算）
    F_wheel_max = params.current_limit * params.motor_torque_constant * (params.gear_efficiency * params.gear_ratio) / max(params.wheel_radius,1e-6);
    F_cmd_max_total = 2 * F_wheel_max;
    F_cmd = u_global(:,1);
    F_sat = abs(F_cmd) > F_cmd_max_total;
    fprintf('\n=== 输入饱和统计 ===\n');
    fprintf('F_cmd 超限: %d / %d (%.2f%%), F_cmd_max=%.1f N\n', sum(F_sat), numel(F_sat), 100*mean(F_sat), F_cmd_max_total);

    % LPV 网格覆盖
    grid_file = fullfile(project_root, 'models', 'lin_agv_db.mat');
    if exist(grid_file, 'file')
        G = load(grid_file);
        [V_grid, W_grid, T_grid] = extractLPVGrid(G);
        if ~isempty(V_grid) && ~isempty(W_grid) && ~isempty(T_grid)
            v_in = x_global(:,4);
            w_in = x_global(:,5);
            t_in = theta_global;
            out_v = v_in < min(V_grid) | v_in > max(V_grid);
            out_w = w_in < min(W_grid) | w_in > max(W_grid);
            out_t = t_in < min(T_grid) | t_in > max(T_grid);
            fprintf('\n=== LPV 网格覆盖统计 ===\n');
            fprintf('V超网格: %d / %d (%.2f%%)\n', sum(out_v), numel(out_v), 100*mean(out_v));
            fprintf('W超网格: %d / %d (%.2f%%)\n', sum(out_w), numel(out_w), 100*mean(out_w));
            fprintf('T超网格: %d / %d (%.2f%%)\n', sum(out_t), numel(out_t), 100*mean(out_t));
        end
    end
end

%% ========== Local Functions ==========

function [v_mean, omega_mean, theta_mean, vdot_mean] = refSegmentStats(t, v_ref, omega_ref, theta_ref, t_start, t_end)
    idx = t >= t_start & t <= t_end;
    if ~any(idx)
        v_mean = 0; omega_mean = 0; theta_mean = 0; vdot_mean = 0;
        return;
    end

    v_seg = v_ref(idx);
    omega_seg = omega_ref(idx);
    theta_seg = theta_ref(idx);
    t_seg = t(idx);

    v_mean = mean(v_seg);
    omega_mean = mean(omega_seg);
    theta_mean = mean(theta_seg);

    if numel(v_seg) >= 2
        vdot = diff(v_seg) ./ diff(t_seg);
        vdot_mean = mean(vdot);
    else
        vdot_mean = 0;
    end
end

function [v_steady_mean, omega_steady_mean] = refSteadyStats(t, v_ref, omega_ref, t_start, t_end, steady_window)
    % 段末稳态窗口必须限制在该段内部，避免把上一段尾巴混进来
    t0 = max(t_start, t_end - steady_window);
    idx = t >= t0 & t <= t_end;
    if ~any(idx)
        v_steady_mean = v_ref(find(t <= t_end, 1, 'last'));
        omega_steady_mean = omega_ref(find(t <= t_end, 1, 'last'));
        return;
    end
    v_steady_mean = mean(v_ref(idx));
    omega_steady_mean = mean(omega_ref(idx));
end

function F = computeForceToTrackSpeedAndAccel(v, vdot, theta_g, m, g, c_r, rho_air, CdA, m_eff)
    % 目标：用前馈力近似跟踪速度与加速度
    % F = m_eff*vdot + F_rr + F_grade + F_aero
    F = m_eff * vdot + m*g*cos(theta_g)*c_r + m*g*sin(theta_g) + 0.5*rho_air*CdA*v^2;
end

function F = computeForceFromRef(t_abs, ref_t, ref_v, ref_vdot, ref_theta, m, g, c_r, rho_air, CdA, m_eff)
    v = interp1(ref_t, ref_v, t_abs, 'linear', 'extrap');
    vdot = interp1(ref_t, ref_vdot, t_abs, 'linear', 'extrap');
    theta_g = interp1(ref_t, ref_theta, t_abs, 'linear', 'extrap');
    F = m_eff * vdot + m*g*cos(theta_g)*c_r + m*g*sin(theta_g) + 0.5*rho_air*CdA*v^2;
end

function out = ternary(cond, a, b)
    if cond
        out = a;
    else
        out = b;
    end
end

function v = getConfigStr(envName, defaultValue)
    v = getenv(envName);
    if isempty(v)
        v = defaultValue;
    end
end

function v = getConfigBool(envName, defaultValue)
    s = getenv(envName);
    if isempty(s)
        v = defaultValue;
        return;
    end
    v = any(strcmpi(s, {'1','true','yes','on'}));
end

function v = safeGetField(s, fieldName, defaultValue)
    if isstruct(s) && isfield(s, fieldName)
        v = s.(fieldName);
    else
        v = defaultValue;
    end
end

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

function [t_vec, x_history] = simulate_core_tv(t_end, u_fun, theta_fun, x0, params)
    Ts = params.Ts;
    N = round(t_end / Ts);
    t_vec = (0:Ts:N*Ts)';
    x_history = zeros(N+1, 8);
    x_history(1, :) = x0';

    xk = x0;
    for k = 1:N
        t_local = (k-1) * Ts;
        u = u_fun(t_local);
        theta_g = theta_fun(t_local);
        xk = state_eq_ref(xk, u, theta_g, params);
        x_history(k+1, :) = xk';
    end
end

function [V_grid, W_grid, T_grid] = extractLPVGrid(G)
    V_grid = [];
    W_grid = [];
    T_grid = [];

    if isfield(G, 'V_grid'), V_grid = G.V_grid; end
    if isfield(G, 'W_grid'), W_grid = G.W_grid; end
    if isfield(G, 'T_grid'), T_grid = G.T_grid; end

    if isempty(V_grid) || isempty(W_grid) || isempty(T_grid)
        % 尝试从结构体字段中递归提取
        names = fieldnames(G);
        for i = 1:numel(names)
            v = G.(names{i});
            if isstruct(v)
                if isempty(V_grid) && isfield(v,'V_grid'), V_grid = v.V_grid; end
                if isempty(W_grid) && isfield(v,'W_grid'), W_grid = v.W_grid; end
                if isempty(T_grid) && isfield(v,'T_grid'), T_grid = v.T_grid; end
            end
        end
    end
end
