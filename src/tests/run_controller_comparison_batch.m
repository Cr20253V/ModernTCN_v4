% =============================
% 文件名：run_controller_comparison_batch.m
% 版本号：V0.3
% 最后修改时间：2026-01-03
% 作者：LPV-MPC Project
% 功能概述：
%   批量跑 LPVMPC 系列控制器（默认仅 GRU，支持扩展 IMU/NMPC），按统一 diag.* 日志契约提取信号，
%   计算关键指标并可保存时序/汇总文件，用于多场景对比与复现。
%
% 调用方式：
%   summary = run_controller_comparison_batch(cfg);
%   - cfg 可留空，使用默认配置；常用可选项：
%     cfg.controller_variants  控制器列表（默认 {'lpvmpc_gru'}，可扩展 lpvmpc_imu/nmpc）
%     cfg.model_map            模型名映射（默认 'lpvmpc_gru'→'LPVMPC_AGV_simulink'）
%     cfg.scenarios            场景列表（默认 five path_*.mat）
%     cfg.repeats              每场景重复次数（默认 1）
%     cfg.stop_time            仿真 StopTime（默认 20s）
%     cfg.enable_noise         是否写回 params.enable_noise（默认 true）
%     cfg.use_fast_restart     是否启用 Fast Restart（默认 false；如需改 params 建议关掉）
%     cfg.save_timeseries      是否保存 sim_out 时序（默认 false）
%     cfg.save_summary         是否保存 summary.mat（默认 true）
%     cfg.F_cmd_limit_fallback 若未日志化 F 限幅时的回退（默认 300N）
%     cfg.Ts                   采样时间（默认空，脚本尝试从 params.Ts 获取）
%
% 输出：
%   summary.controllers(i).reports{k}  按控制器-场景-重复组织的指标与元数据
%   可选保存：timeseries_*（sim_out），closed_loop_summary_*.mat（summary）
%
% 日志/信号契约（默认）：
%   diag.e_*（轨迹误差），diag.F_cmd/omega_cmd（控制输出），
%   diag.F_limit_hi/lo（力上下界，缺省下界时仅 hi），diag.rho_f/rho_n（调度变量），
%   其他可选：diag.solve_time_ms/total_step_time_ms（若模型有输出）
%
% 注意事项：
%   - 运行前需在 base 写入 ref/agv_ref_path 场景变量；
%   - lpvmpc_gru 分支需确保 gru_model 已加载；
%   - 使用 Fast Restart 时，params 等非可调参数的修改不会生效。
% =============================

function summary = run_controller_comparison_batch(cfg)

if nargin < 1 || isempty(cfg)
    cfg = struct();
end
cfg = apply_defaults_local(cfg);
summary.controllers = struct([]);
summary_save_path = '';
timeseries_saved = 0;
total_runs = 0;
total_fail = 0;

controller_tags = cfg.controller_variants;
scenario_list   = cfg.scenarios;
repeat_count    = cfg.repeats;

for ic = 1:numel(controller_tags)
    tag = controller_tags{ic};
    model = cfg.model_map.(tag);

    % 预加载模型，启用 Fast Restart 时可复用状态
    load_system(model);

    reports = {};
    report_idx = 1;

    for is = 1:numel(scenario_list)
        sc = scenario_list(is);

        for ir = 1:repeat_count
            seed = derive_seed_local(cfg, tag, sc.name, ir);
            rng(seed, 'twister');

            % 将当前场景变量写入基础工作区
            Sref = load(sc.path_file);        % path_*.mat 内应包含 ref 结构
            if isfield(Sref, 'ref')
                assignin('base', 'ref', Sref.ref);
                assignin('base', 'agv_ref_path', Sref.ref); % 保持命名兼容
            else
                error('场景文件缺少 ref: %s', sc.path_file);
            end

            % 同步开启噪声（使用 parameters.m 中的 params.enable_noise）
            try
                params = evalin('base', 'params');
                params.enable_noise = cfg.enable_noise;
                assignin('base', 'params', params);
            catch ME
                warning('未能更新 params.enable_noise（%s），请确认 PreLoadFcn 已加载 params。', ME.message);
            end

            % 组装仿真输入，尽量利用 Fast Restart
            sim_in = Simulink.SimulationInput(model);
            sim_in = sim_in.setModelParameter('StopTime', num2str(cfg.stop_time));
            if cfg.use_fast_restart
                sim_in = sim_in.setModelParameter('FastRestart', 'on');
            end

            % GRU 分支检查：若是 GRU 控制器，需要确保 gru_model 已加载
            if strcmp(tag, 'lpvmpc_gru')
                if evalin('base','exist(''gru_model'',''var'')') ~= 1
                    error('缺少 gru_model：请先在 PreLoadFcn 或脚本中加载 GRU 模型。');
                end
            end

            sim_out = sim(sim_in);

            data = extract_signals_local(sim_out, cfg.signal_names);
            metrics = analyze_results_local(data, cfg.metrics_window, cfg.Ts, cfg.F_cmd_limit_fallback);

            % 轻量日志：控制器/场景/seed + 主要指标摘要（中文）
            fprintf(['[仿真结果] 控制器:%-10s 场景:%-18s 次数:%2d Seed:%6d\n' ...
                    '  误差RMS: e_y=%.3f, e_psi=%.3f, e_v=%.3f | 饱和占比: %.3f | 失败标志: %d\n'], ...
                    tag, sc.name, ir, seed, ...
                    metrics.e_y_rms, metrics.e_psi_rms, metrics.e_v_rms, metrics.sat_ratio_F_cmd, metrics.fail_flag);
            total_runs = total_runs + 1;
            if metrics.fail_flag, total_fail = total_fail + 1; end

            save_path = '';
            if cfg.save_timeseries
                fname = sprintf('timeseries_%s_%s_r%d.mat', tag, sc.name, ir);
                save_path = fullfile(cfg.results_dir, fname);
                save(save_path, 'sim_out', '-v7.3');
                timeseries_saved = timeseries_saved + 1;
            end

            reports{report_idx,1} = struct( ...
                'controller', tag, ...
                'model', model, ...
                'scenario', sc.name, ...
                'repeat', ir, ...
                'seed', seed, ...
                'metrics', metrics, ...
                't_stop', cfg.stop_time, ...
                'save_path', save_path );

            report_idx = report_idx + 1;
        end
    end

    summary.controllers(ic).name = tag;
    summary.controllers(ic).model = model;
    summary.controllers(ic).reports = reports;
    summary.controllers(ic).stats = []; % 聚合统计可后续填充
end

% 可选：保存 summary
if cfg.save_summary
    fname = sprintf('closed_loop_summary_%s.mat', datestr(now, 'yyyymmdd_HHMMSS'));
    fpath = fullfile(cfg.results_dir, fname);
    save(fpath, 'summary', '-v7.3');
    summary.save_path = fpath;
    summary_save_path = fpath;
end

% 结束时输出简短汇总
if isempty(summary_save_path), summary_path_str = 'none'; else, summary_path_str = summary_save_path; end
fprintf(['=== 批处理结束 ===\n' ...
    '总仿真次数: %d | 失败次数: %d | 保存时序数: %d\n' ...
    'summary 文件: %s\n'], ...
    total_runs, total_fail, timeseries_saved, summary_path_str);

% -------------------------------------------------------------------------
function cfg = apply_defaults_local(cfg)
    % 默认仅跑现有的 GRU 模型；如需 IMU/NMPC 请在 cfg 里自行添加：
    % cfg.controller_variants = {'lpvmpc_gru','lpvmpc_imu','nmpc'};
    % cfg.model_map = struct('lpvmpc_gru','LPVMPC_AGV_simulink', ...
    %                        'lpvmpc_imu','LPVMPC_AGV_simulink_IMU', ...
    %                        'nmpc','LPVMPC_AGV_simulink_NMPC');
    if ~isfield(cfg, 'controller_variants'), cfg.controller_variants = {'lpvmpc_gru'}; end
    if ~isfield(cfg, 'model_map')
        cfg.model_map = struct( ...
            'lpvmpc_gru', 'LPVMPC_AGV_simulink');
    end
    if ~isfield(cfg, 'scenarios')
        % 默认五条路径场景，对应 data/paths 下的 path_*.mat
        cfg.scenarios = [ ...
            struct('name','straight',             'path_file', fullfile(project_root(),'data','paths','path_straight.mat')), ...
            struct('name','straight_left_turn',   'path_file', fullfile(project_root(),'data','paths','path_straight_left_turn.mat')), ...
            struct('name','straight_right_turn',  'path_file', fullfile(project_root(),'data','paths','path_straight_right_turn.mat')), ...
            struct('name','slope',                'path_file', fullfile(project_root(),'data','paths','path_slope.mat')), ...
            struct('name','bumpy',                'path_file', fullfile(project_root(),'data','paths','path_bumpy.mat')) ...
        ];
    end
    if ~isfield(cfg, 'repeats'), cfg.repeats = 1; end                                 % 每条路径重复次数（用于统计均值方差）
    if ~isfield(cfg, 'stop_time'), cfg.stop_time = 20; end                            % 统一 StopTime=20s
    if ~isfield(cfg, 'enable_noise'), cfg.enable_noise = true; end                    % 默认开启噪声，写回 params.enable_noise
    if ~isfield(cfg, 'rng_policy'), cfg.rng_policy = 'hash'; end                      % 随机种子策略：'hash' 派生，'fixed' 固定
    if ~isfield(cfg, 'seed_base'), cfg.seed_base = 1; end                             % 基础种子（脚本内使用），保证可复现
    if ~isfield(cfg, 'results_dir'), cfg.results_dir = results_dir('simulink'); end    % 结果输出目录（timeseries/summary），统一放在 results/simulink
    if ~isfield(cfg, 'save_timeseries'), cfg.save_timeseries = false; end             % 是否保存 sim_out 时序
    if ~isfield(cfg, 'save_summary'), cfg.save_summary = true; end                    % 是否保存 summary.mat
    if ~isfield(cfg, 'use_fast_restart'), cfg.use_fast_restart = false; end            % 是否启用 Fast Restart
    if ~isfield(cfg, 'metrics_window'), cfg.metrics_window = struct('steady_ratio', 0.10); end % 指标稳态窗口比例
    if ~isfield(cfg, 'signal_names'), cfg.signal_names = default_signal_names_local(); end % logsout 信号名映射（diag.* 契约）
    if ~isfield(cfg, 'F_cmd_limit_fallback'), cfg.F_cmd_limit_fallback = 300; end     % 若未日志化 F_limit，使用的默认力限幅
    if ~isfield(cfg, 'Ts'), cfg.Ts = []; end                                          % 采样时间（若留空则尝试从 params.Ts 获取）
end

% -------------------------------------------------------------------------
function signal_names = default_signal_names_local()
% 逻辑名称到 logsout 名称的映射（diag.* 契约）
    signal_names = struct();
    signal_names.X          = 'diag.X';
    signal_names.Y          = 'diag.Y';
    signal_names.psi        = 'diag.psi';
    signal_names.v          = 'diag.v';
    signal_names.omega      = 'diag.omega';
    signal_names.X_ref      = 'diag.X_ref';
    signal_names.Y_ref      = 'diag.Y_ref';
    signal_names.psi_ref    = 'diag.psi_ref';
    signal_names.v_ref      = 'diag.v_ref';
    signal_names.omega_ref  = 'diag.omega_ref';
    signal_names.e_y        = 'diag.e_y';
    signal_names.e_psi      = 'diag.e_psi';
    signal_names.e_v        = 'diag.e_v';
    signal_names.e_omega    = 'diag.e_omega';
    signal_names.F_cmd      = 'diag.F_cmd';
    signal_names.omega_cmd  = 'diag.omega_cmd';
    signal_names.theta_hat  = 'diag.theta_hat';
    signal_names.theta_ground = 'diag.theta_ground';
    signal_names.label_main = 'diag.label_main';
    signal_names.rho_f      = 'diag.rho_f';
    signal_names.rho_n      = 'diag.rho_n';
    signal_names.F_limit    = '';                  % 若模型仍输出 diag.F_limit，可在需要时填回
    signal_names.F_limit_hi = 'diag.F_limit_hi';   % 力正向上界（若模型提供非对称/独立限幅）
    signal_names.F_limit_lo = 'diag.F_limit_lo';   % 力负向下界（若模型提供非对称/独立限幅）
    % 以下两个可选：若模型输出了求解/总步耗时日志，可改成 'diag.solve_time_ms'、'diag.total_step_time_ms'
    signal_names.solve_time_ms      = '';
    signal_names.total_step_time_ms = '';
end

% -------------------------------------------------------------------------
function seed = derive_seed_local(cfg, controller, scenario_name, repeat_idx)
    switch cfg.rng_policy
        case 'fixed'
            seed = cfg.seed_base;
        otherwise % 'hash' or default
            % 简单可复现的哈希：基础种子 + 控制器/场景字符和 + 重复次数偏移
            cval = sum(double(controller)) + numel(controller)*31;
            sval = sum(double(scenario_name)) + numel(scenario_name)*17;
            seed = cfg.seed_base + cval + sval + 97*repeat_idx;
    end
end

% -------------------------------------------------------------------------
function data = extract_signals_local(sim_out, signal_names)
    logs = sim_out.logsout;
    fn = fieldnames(signal_names);
    data = struct();
    for i = 1:numel(fn)
        key = fn{i};
        sig_name = signal_names.(key);
        if isempty(sig_name)
            data.(key) = [];
            continue;
        end
        try
            el = logs.getElement(sig_name);
            data.(key) = el.Values;
        catch
            data.(key) = [];
        end
    end
end

% -------------------------------------------------------------------------
function metrics = analyze_results_local(data, metrics_window, Ts, F_cmd_limit_fallback)
    metrics = struct();

    % 采样时间：优先 cfg.Ts；为空则尝试从 params.Ts；再为空则设 1 避免零除
    if isempty(Ts)
        try
            params = evalin('base','params');
            Ts = params.Ts;
        catch
            Ts = 1;
        end
    end
    if Ts <= 0, Ts = 1; end

    % 计算全时域 RMS/峰值的辅助函数
    function [rmsv, peakv] = rms_peak(sig)
        if isempty(sig)
            rmsv = NaN; peakv = NaN; return; end
        vals = sig.Data;
        rmsv = sqrt(mean(vals.^2));
        peakv = max(abs(vals));
    end

    [metrics.e_y_rms, metrics.e_y_peak] = rms_peak(data.e_y);
    [metrics.e_psi_rms, metrics.e_psi_peak] = rms_peak(data.e_psi);
    [metrics.e_v_rms, metrics.e_v_peak] = rms_peak(data.e_v);

    % 稳态窗口统计（最后 steady_ratio 比例）
    function steady_mean = steady_mean_fn(sig)
        if isempty(sig)
            steady_mean = NaN; return; end
        vals = sig.Data;
        n = numel(vals);
        idx0 = max(1, floor(n*(1-metrics_window.steady_ratio)));
        steady_mean = mean(vals(idx0:end));
    end
    metrics.e_y_steady = steady_mean_fn(data.e_y);
    metrics.e_psi_steady = steady_mean_fn(data.e_psi);
    metrics.e_v_steady = steady_mean_fn(data.e_v);

    % 控制输出与变化率
    [metrics.F_cmd_rms, metrics.F_cmd_peak_abs] = rms_peak(data.F_cmd);
    [metrics.omega_cmd_rms, metrics.omega_cmd_peak_abs] = rms_peak(data.omega_cmd);

    metrics.dF_cmd_rms = NaN; metrics.domega_cmd_rms = NaN;
    if ~isempty(data.F_cmd)
        dv = diff(data.F_cmd.Data) / Ts;  % 按计划要求除以采样周期
        metrics.dF_cmd_rms = sqrt(mean(dv.^2));
    end
    if ~isempty(data.omega_cmd)
        dv = diff(data.omega_cmd.Data) / Ts;
        metrics.domega_cmd_rms = sqrt(mean(dv.^2));
    end

    % 饱和占比（需 F_cmd 限幅）：
    % - 优先使用 diag.F_limit_hi / diag.F_limit_lo（分别为上/下界，可缺省下界）
    % - 若未提供 hi/lo，再尝试 diag.F_limit(1,:) 作为力上界，第二行为下界（可缺省）
    % - 若仍缺失，使用 cfg.F_cmd_limit_fallback
    metrics.sat_ratio_F_cmd = NaN;
    F_hi = [];
    F_lo = [];
    if isfield(data, 'F_limit_hi') && ~isempty(data.F_limit_hi)
        F_hi = squeeze(data.F_limit_hi.Data);
    end
    if isfield(data, 'F_limit_lo') && ~isempty(data.F_limit_lo)
        F_lo = squeeze(data.F_limit_lo.Data);
    end

    if isempty(F_hi) && isfield(data, 'F_limit') && ~isempty(data.F_limit)
        vals = squeeze(data.F_limit.Data);
        if ~isempty(vals)
            F_hi = vals(1,:);                   % 第一行对应 F_cmd 上界
            if size(vals,1) >= 2
                F_lo = vals(2,:);               % 若第二行提供下界（可选）
            end
        end
    end

    % 计算力限幅的绝对上界，支持非对称：取 |上界| 与 |下界| 的最大值
    F_limit_abs = F_cmd_limit_fallback;
    hi_max = -Inf; lo_max = -Inf;
    if ~isempty(F_hi)
        hi_max = max(abs(F_hi(:)));
    end
    if ~isempty(F_lo)
        lo_max = max(abs(F_lo(:)));
    end
    candidate = max([hi_max, lo_max]);
    if candidate > 0 && ~isinf(candidate)
        F_limit_abs = candidate;
    end

    if ~isempty(data.F_cmd) && ~isnan(F_limit_abs) && F_limit_abs > 0
        metrics.sat_ratio_F_cmd = mean(abs(data.F_cmd.Data) > 0.95 * F_limit_abs);
    end

    % 求解耗时（若有）
    metrics.solve_time_ms_mean = NaN;
    metrics.solve_time_ms_p95  = NaN;
    metrics.solve_time_ms_max  = NaN;
    if ~isempty(data.solve_time_ms)
        v = data.solve_time_ms.Data;
        metrics.solve_time_ms_mean = mean(v);
        metrics.solve_time_ms_p95  = prctile(v, 95);
        metrics.solve_time_ms_max  = max(v);
    end

    metrics.total_step_time_ms_mean = NaN;
    if ~isempty(data.total_step_time_ms)
        metrics.total_step_time_ms_mean = mean(data.total_step_time_ms.Data);
    end

    % 仿真/求解失败标志（粗粒度占位）：若 logs 中缺失核心信号或 sim 抛异常可在上层捕获
    metrics.fail_flag = false;
    metrics.fail_reason = '';
    metrics.fail_count = 0;
    if isempty(data.F_cmd) || isempty(data.e_y)
        metrics.fail_flag = true;
        metrics.fail_reason = 'missing_signals';
        metrics.fail_count = 1;
    end
end

end
