function test_simulink_closed_loop()
% =============================
% 鏂囦欢鍚嶏細test_simulink_closed_loop.m
% 鍔熻兘鎻忚堪锛氬熀浜?Simulink 妯″瀷鐨?MPC 闂幆楠岃瘉鑴氭湰 (浼樺寲鐗?
%           璋冪敤 LPVMPC_AGV_simulink_Mamba.slx
% =============================

    clear; clc; close all;
    
    %% 1. 鍒濆鍖?
    fprintf('=== 鍒濆鍖栧弬鏁?===\n');
    params = parameters();
    
    % 纭畾椤圭洰鏍圭洰褰?
    script_dir = fileparts(mfilename('fullpath'));
    proj_root = fullfile(script_dir, '..', '..');
    
    % 鍔犺浇 LPV 鏁版嵁搴?
    db_path = fullfile(proj_root, 'data', 'models', 'lin_agv_db.mat');
    if ~exist(db_path, 'file')
        error('鏈壘鍒?LPV 鏁版嵁搴? %s\n璇峰厛杩愯 test_lpvmpc_workflow 鐢熸垚銆?, db_path);
    end
    load(db_path, 'db');
    
    if abs(db.Ts - params.Ts) > 1e-6
        warning('鏁版嵁搴撴闀?%.3fs)涓庡弬鏁版闀?%.3fs)涓嶄竴鑷达紒', db.Ts, params.Ts);
    end
    fprintf('  Ts = %.3f s, 璐ㄩ噺 = %.1f kg\n', params.Ts, params.mass);
    
    %% 2. 鍑嗗 MPC 鎺у埗鍣?
    fprintf('=== 鍑嗗 MPC 鎺у埗鍣?===\n');
    Ts_mpc = db.Ts;
    mpc_opts = struct();
    mpc_opts.Np = round(1.5 / Ts_mpc);
    mpc_opts.Nc = round(0.5 / Ts_mpc);
    % Q/R/dR 浣跨敤 mpc_setup_single_interp 鐨勯粯璁ゅ€?(鏉ヨ嚜璐濆彾鏂紭鍖?
    % 鏄惧紡璁剧疆杞害鏉熸潈閲?
    mpc_opts.soft_weight_pos = 1e3;   % 浣嶇疆璇樊杞害鏉?
    mpc_opts.soft_weight_yaw = 1e3;   % 鑸悜璇樊杞害鏉?
    
    ctrl = mpc_setup_single_interp(db, mpc_opts);
    
    %% 2.1 鍔犺浇璐濆彾鏂紭鍖栨潈閲?
    % 浼樺厛鍔犺浇 maps_best.mat锛屽惁鍒欎娇鐢ㄩ粯璁ゆ潈閲?
    maps_best_path = fullfile(proj_root, 'data', 'models', 'maps_best.mat');
    if exist(maps_best_path, 'file')
        Tm = load(maps_best_path);
        if isfield(Tm, 'maps_best') && all(isfield(Tm.maps_best, {'Q_range', 'R_range', 'dR_range'}))
            maps_best = Tm.maps_best;
            
            % 浠庤寖鍥翠腑鎻愬彇涓€间綔涓哄熀鍑嗘潈閲?
            Q_opt = mean(maps_best.Q_range, 1);
            R_opt = mean(maps_best.R_range, 1);
            dR_opt = mean(maps_best.dR_range, 1);
            
            % 搴旂敤鍒?MPC 鎺у埗鍣?
            ctrl.mpcobj.Weights.OutputVariables = Q_opt;
            ctrl.mpcobj.Weights.ManipulatedVariables = R_opt;
            ctrl.mpcobj.Weights.ManipulatedVariablesRate = dR_opt;
            
            % 鍚屾鏇存柊 ctrl.maps
            ctrl.maps.Q_range = maps_best.Q_range;
            ctrl.maps.R_range = maps_best.R_range;
            ctrl.maps.dR_range = maps_best.dR_range;
            
            % 澶嶅埗鍏朵粬浼樺寲鍙傛暟
            opt_fields = {'omega_threshold', 'q_y_gain_max', 'theta_threshold', 'q_v_gain_max', ...
                          'alpha_Q', 'beta_Q', 'alpha_R', 'beta_R', 'alpha_dR', 'beta_dR'};
            for fi = 1:numel(opt_fields)
                if isfield(maps_best, opt_fields{fi})
                    ctrl.maps.(opt_fields{fi}) = maps_best.(opt_fields{fi});
                end
            end
            
            fprintf('  鉁?宸插姞杞借礉鍙舵柉浼樺寲鏉冮噸 (maps_best.mat)\n');
            fprintf('    Q  = [%.2f, %.2f, %.2f, %.2f]\n', Q_opt(1), Q_opt(2), Q_opt(3), Q_opt(4));
            fprintf('    R  = [%.2e, %.2e]\n', R_opt(1), R_opt(2));
            fprintf('    dR = [%.2e, %.2e]\n', dR_opt(1), dR_opt(2));
            fprintf('    鉁?ctrl.maps 宸插悓姝?Q/R/dR 鑼冨洿涓庤嚜閫傚簲鍙傛暟\n');
        else
            fprintf('  鈿?maps_best.mat 鏍煎紡涓嶆纭紝浣跨敤榛樿鏉冮噸\n');
        end
    else
        fprintf('  鈿?鏈壘鍒?maps_best.mat锛屼娇鐢ㄩ粯璁ゆ潈閲峔n');
    end
    
    %% 2.2 涓存椂鏉冮噸瑕嗙洊锛堣皟璇曠敤锛?
    % 璇ユ宸茬Щ闄わ紝淇濇寔涓?maps_best.mat 涓€鑷?
    
    % 鎺ㄩ€佸埌宸ヤ綔鍖?
    assignin('base', 'mpcobj', ctrl.mpcobj);
    assignin('base', 'maps', ctrl.maps);
    assignin('base', 'params', params);
    assignin('base', 'db', db);
    
    %% 3. 鍦烘櫙瀹氫箟
    scenarios = {
        'industrial',         '宸ヤ笟缁煎悎鍦烘櫙'
    };
    
    results = struct();
    model_name = 'LPVMPC_AGV_simulink_Mamba';
    model_path = fullfile(proj_root, 'simulink', [model_name, '.slx']);
    
    % 鍔犺浇妯″瀷
    if ~exist(model_path, 'file')
        error('鏈壘鍒?Simulink 妯″瀷: %s', model_path);
    end
    if ~bdIsLoaded(model_name)
        load_system(model_path);
    end
    
    fprintf('\n=== 寮€濮?Simulink 闂幆娴嬭瘯 ===\n');
    
    %% 4. 寰幆娴嬭瘯
    for i = 1:size(scenarios, 1)
        name = scenarios{i,1};
        desc = scenarios{i,2};
        
        fprintf('>>> 姝ｅ湪娴嬭瘯鍦烘櫙: %s (%s)\n', name, desc);
        
        % 鍔犺浇鍙傝€冭矾寰勶紙浠呬娇鐢?path_industrial.mat锛?
        path_file = fullfile(proj_root, 'data', 'paths', 'path_industrial.mat');
        if ~exist(path_file, 'file')
            error('鏈壘鍒?path_industrial.mat锛岃鍏堢敓鎴愭渶鏂板伐涓氳矾寰?);
        end
        S_path = load(path_file);
        ref = S_path.ref;
        fprintf('    鉁?宸插姞杞?path_industrial.mat\n');

        % 鍙傝€冭矾寰勫揩閫熶竴鑷存€ф鏌ワ紙鐢ㄤ簬鎺掓煡璺緞/绗﹀彿闂锛?
        validate_ref(ref);

        stop_time = num2str(ref.t(end));
        assignin('base', 'ref', ref);
        
        % 閰嶇疆浠跨湡
        simIn = Simulink.SimulationInput(model_name);
        simIn = simIn.setModelParameter('StopTime', stop_time);
        
        % 鍏抽敭锛氬湪 sim() 鍓嶉噸鏂版帹閫佷慨鏀瑰悗鐨?mpcobj锛岃鐩?PreLoadFcn 鐨勮缃?
        % 浣跨敤 setVariable 纭繚浠跨湡浣跨敤鑴氭湰涓慨鏀圭殑鏉冮噸
        simIn = simIn.setVariable('mpcobj', ctrl.mpcobj, 'Workspace', model_name);
        simIn = simIn.setVariable('maps', ctrl.maps, 'Workspace', model_name);
        simIn = simIn.setVariable('ctrl', ctrl, 'Workspace', model_name); % [Fix] 蹇呴』瑕嗙洊 ctrl 缁撴瀯浣?
        simIn = simIn.setVariable('ref', ref, 'Workspace', model_name);   % [Fix] 纭繚妯″瀷浣跨敤鏈€鏂板弬鑰冭矾寰?
        
        try
            simOut = sim(simIn);
            logs = simOut.logsout;
            
            % 璇诲彇淇″彿锛堝甫瀹归敊锛?
            [e_y, t] = safe_get_signal(logs, 'e_y');
            [e_psi, ~] = safe_get_signal(logs, 'e_psi');
            [F_cmd, ~] = safe_get_signal(logs, 'F_cmd');
            [omega_cmd, ~] = safe_get_signal(logs, 'omega_cmd');
            [X, ~] = safe_get_signal(logs, 'X');
            [Y, ~] = safe_get_signal(logs, 'Y');
            [psi, ~] = safe_get_signal(logs, 'psi');
            [v, ~] = safe_get_signal(logs, 'v');
            [omega, ~] = safe_get_signal(logs, 'omega');
            
            % 蹇界暐鍓?0.5s
            mask = t > 0.5;
            
            % 鎬ц兘璁＄畻
            metrics = struct();
            metrics.ey_rmse = rms(e_y(mask));
            metrics.ey_peak = max(abs(e_y(mask)));
            metrics.epsi_rmse = rms(e_psi(mask));
            metrics.epsi_peak = max(abs(e_psi(mask)));
            
            % 鏂板鎸囨爣锛氭帶鍒惰緭鍏ョ粺璁?
            metrics.F_cmd_mean = mean(F_cmd(mask));
            metrics.F_cmd_range = [min(F_cmd(mask)), max(F_cmd(mask))];
            metrics.F_cmd_sat_pct = mean(abs(F_cmd(mask)) >= 595) * 100; % 楗卞拰搴﹀崰姣?(>595N)
            metrics.omega_cmd_mean = mean(omega_cmd(mask));
            metrics.omega_cmd_range = [min(omega_cmd(mask)), max(omega_cmd(mask))];
            
            % 鏂板鎸囨爣锛氶€熷害/瑙掗€熷害璺熻釜
            v_ref_interp = interp1(ref.t, ref.v_ref, t, 'linear', 'extrap');
            e_v = v - v_ref_interp;
            metrics.ev_rmse = rms(e_v(mask));
            metrics.ev_peak = max(abs(e_v(mask)));

            omega_ref_interp = interp1(ref.t, ref.omega_ref, t, 'linear', 'extrap');
            e_omega = omega - omega_ref_interp;
            metrics.eomega_rmse = rms(e_omega(mask));
            metrics.eomega_peak = max(abs(e_omega(mask)));
            
            % 鍒ゅ畾
            is_pass = metrics.ey_rmse < 0.20 && metrics.epsi_rmse < 0.10;
            
            fprintf('  缁撴灉: %s\n', pass_fail_str(is_pass));
            fprintf('    e_y:   RMSE=%.4f m, Peak=%.4f m\n', metrics.ey_rmse, metrics.ey_peak);
            fprintf('    e_psi: RMSE=%.4f rad, Peak=%.4f rad\n', metrics.epsi_rmse, metrics.epsi_peak);
            
            fprintf('    e_v:   RMSE=%.4f m/s, Peak=%.4f m/s\n', metrics.ev_rmse, metrics.ev_peak);
            fprintf('    e_蠅:   RMSE=%.4f rad/s, Peak=%.4f rad/s\n', metrics.eomega_rmse, metrics.eomega_peak);
            fprintf('    F_cmd: 鍧囧€?%.1f N, 鑼冨洿=[%.1f, %.1f] N, 楗卞拰鍗犳瘮=%.1f%%\n', ...
                metrics.F_cmd_mean, metrics.F_cmd_range(1), metrics.F_cmd_range(2), metrics.F_cmd_sat_pct);
            fprintf('    蠅_cmd: 鍧囧€?%.3f rad/s, 鑼冨洿=[%.3f, %.3f] rad/s\n', ...
                metrics.omega_cmd_mean, metrics.omega_cmd_range(1), metrics.omega_cmd_range(2));

            % 缃戞牸瑕嗙洊鐜囪瘖鏂紙鍩轰簬瀹為檯杩愯鐐癸級
            coverage = analyze_grid_coverage(t, v, omega, db);

            % 鍒嗗尯璇婃柇锛堟寜 ref.meta.zones 鎴栭粯璁ゅ垎鍖猴級
            zone_report = analyze_zones(t, e_y, e_psi, e_v, e_omega, F_cmd, omega_cmd, v, omega, ref, db, ctrl);
            results.(name).coverage = coverage;
            results.(name).zones = zone_report;
            results.(name).worst_zone = zone_report.worst_zone;
            
            % 淇濆瓨缁撴灉
            results.(name) = metrics;
            results.(name).pass = is_pass;
            results.(name).t = t;
            results.(name).e_y = e_y;
            results.(name).e_psi = e_psi;
            results.(name).X = X;
            results.(name).Y = Y;
            results.(name).ref = ref;
            
        catch ME
            fprintf('  [ERROR] 浠跨湡澶辫触: %s\n', ME.message);
            results.(name).pass = false;
        end
        fprintf('\n');
    end
    
    %% 5. 姹囨€绘姤鍛?
    print_summary(results);
end

%% === 杈呭姪鍑芥暟 ===
function [data, time] = safe_get_signal(logs, name)
    sig = logs.get(name);
    if isempty(sig)
        warning('鏈壘鍒颁俊鍙? %s', name);
        data = []; time = [];
    else
        data = squeeze(sig.Values.Data);
        time = sig.Values.Time;
    end
end

function s = pass_fail_str(is_pass)
    if is_pass, s = '[PASS]'; else, s = '[FAIL]'; end
end

function print_summary(res)
    fprintf('==========================================\n');
    fprintf('        Simulink 闂幆楠岃瘉缁撴灉姹囨€籠n');
    fprintf('------------------------------------------\n');
    fprintf('%-20s | %-10s | %-10s\n', '鍦烘櫙', 'e_y RMSE', '鍒ゅ畾');
    fprintf('------------------------------------------\n');
    fns = fieldnames(res);
    for i = 1:length(fns)
        name = fns{i};
        r = res.(name);
        if isfield(r, 'ey_rmse')
            fprintf('%-20s | %.4f     | %s\n', name, r.ey_rmse, pass_fail_str(r.pass));
        end
    end
    fprintf('==========================================\n');
end

function coverage = analyze_grid_coverage(t, v, omega, db)
% 妫€鏌ュ疄闄呰繍琛岀偣鏄惁钀藉湪 LPV 缃戞牸鑼冨洿鍐咃紙鍩轰簬 db.grid锛?

    V_bounds = [db.grid.V(1), db.grid.V(end)];
    W_bounds = [db.grid.W(1), db.grid.W(end)];

    v_out = v < V_bounds(1) | v > V_bounds(2);
    w_out = omega < W_bounds(1) | omega > W_bounds(2);

    coverage = struct();
    coverage.v_out_pct = mean(v_out) * 100;
    coverage.w_out_pct = mean(w_out) * 100;

    fprintf('    [Grid Coverage] v瓒婄晫: %.2f%%, 蠅瓒婄晫: %.2f%%\n', ...
        coverage.v_out_pct, coverage.w_out_pct);
end

function report = analyze_zones(t, e_y, e_psi, e_v, e_omega, F_cmd, omega_cmd, v, omega, ref, db, ctrl)
% 鎸夊垎鍖鸿緭鍑鸿瘖鏂寚鏍囷紝瀹氫綅闂鍖哄煙

    fprintf('    [Zone Analysis]\n');
    zones = get_ref_zones(ref);
    zone_names = fieldnames(zones);

    report = struct();
    fprintf('    %-12s | %6s | %8s | %8s | %8s | %8s | %6s | %6s | %6s | %6s\n', ...
        'zone', 't[s]', 'ey_rmse', 'epsi', 'ev', 'e蠅', 'F_sat', '蠅_sat', 'v_out', 'pass');
    fprintf('    %s\n', repmat('-', 1, 106));

    % 鍒嗗尯鍒ゅ畾闃堝€硷紙涓庡叏灞€涓€鑷达級
    thr_ey = 0.20;
    thr_epsi = 0.10;

    worst_score = -inf;
    worst_zone = '';

    for i = 1:numel(zone_names)
        zn = zone_names{i};
        tr = zones.(zn);
        mask = t >= tr(1) & t < tr(2);
        if nnz(mask) < 5
            continue;
        end
        ey_rmse = rms(e_y(mask));
        epsi_rmse = rms(e_psi(mask));
        ev_rmse = rms(e_v(mask));
        eomega_rmse = rms(e_omega(mask));
        F_sat = mean(abs(F_cmd(mask)) >= 595) * 100;
        w_sat = mean(abs(omega_cmd(mask)) >= 0.60) * 100;
        v_out = mean(v(mask) < db.grid.V(1) | v(mask) > db.grid.V(end)) * 100;

        z_pass = ey_rmse < thr_ey && epsi_rmse < thr_epsi;
        % 璇勫垎锛氫紭鍏堢湅ey/epsi瓒呴檺绋嬪害
        score = max(ey_rmse / thr_ey, epsi_rmse / thr_epsi);
        if score > worst_score
            worst_score = score;
            worst_zone = zn;
        end

        % 宄板€煎畾浣嶏細ey 涓?epsi 鐨勫嘲鍊煎強瀵瑰簲鏃跺埢
        [ey_peak, idx_ey] = max(abs(e_y(mask)));
        [epsi_peak, idx_ep] = max(abs(e_psi(mask)));
        idx_list = find(mask);
        t_ey = t(idx_list(idx_ey));
        t_ep = t(idx_list(idx_ep));

        % 宄板€煎鐨勯€熷害/鍙傝€冮€熷害
        v_act_ey = v(idx_list(idx_ey));
        v_act_ep = v(idx_list(idx_ep));
        v_ref_ey = interp1(ref.t, ref.v_ref, t_ey, 'linear', 'extrap');
        v_ref_ep = interp1(ref.t, ref.v_ref, t_ep, 'linear', 'extrap');

        % 宄板€煎鐨勮宸鍙凤紙闈炵粷瀵瑰€硷級
        ey_raw = e_y(idx_list(idx_ey));
        epsi_raw = e_psi(idx_list(idx_ep));

        % omega 鐩稿叧瀵规瘮
        omega_ref_ey = interp1(ref.t, ref.omega_ref, t_ey, 'linear', 'extrap');
        omega_ref_ep = interp1(ref.t, ref.omega_ref, t_ep, 'linear', 'extrap');
        omega_cmd_ey = omega_cmd(idx_list(idx_ey));
        omega_cmd_ep = omega_cmd(idx_list(idx_ep));
        omega_act_ey = omega(idx_list(idx_ey));
        omega_act_ep = omega(idx_list(idx_ep));

        % 鑻ュ彲鑾峰彇绾︽潫锛屾鏌?omega_cmd 鏄惁瓒呴檺锛堝府鍔╃‘璁も€滅害鏉熸槸鍚︾敓鏁?璁板綍鐐规槸鍚﹀湪楗卞拰鍓嶁€濓級
        w_min = NaN; w_max = NaN;
        try
            w_min = ctrl.mpcobj.MV(2).Min;
            w_max = ctrl.mpcobj.MV(2).Max;
        catch
        end

        report.(zn) = struct('t_range', tr, 'ey_rmse', ey_rmse, 'epsi_rmse', epsi_rmse, ...
            'ev_rmse', ev_rmse, 'eomega_rmse', eomega_rmse, 'F_sat_pct', F_sat, 'omega_sat_pct', w_sat, ...
            'v_out_pct', v_out, 'pass', z_pass, 'score', score, ...
            'ey_peak', ey_peak, 'epsi_peak', epsi_peak, ...
            't_ey_peak', t_ey, 't_epsi_peak', t_ep, ...
            'omega_ref_at_ey', omega_ref_ey, 'omega_ref_at_epsi', omega_ref_ep, ...
            'omega_cmd_at_ey', omega_cmd_ey, 'omega_cmd_at_epsi', omega_cmd_ep, ...
            'omega_at_ey', omega_act_ey, 'omega_at_epsi', omega_act_ep, ...
            'v_at_ey', v_act_ey, 'v_at_epsi', v_act_ep, 'v_ref_at_ey', v_ref_ey, 'v_ref_at_epsi', v_ref_ep, ...
            'ey_raw_at_ey', ey_raw, 'epsi_raw_at_epsi', epsi_raw, ...
            'omega_cmd_min', w_min, 'omega_cmd_max', w_max);

        fprintf('    %-12s | %6.0f | %8.4f | %8.4f | %8.4f | %8.4f | %6.1f | %6.1f | %6.1f | %6s\n', ...
            zn, tr(2)-tr(1), ey_rmse, epsi_rmse, ev_rmse, eomega_rmse, F_sat, w_sat, v_out, pass_fail_str(z_pass));

        fprintf('      peaks: ey=%.3f(raw=%+.3f)@t=%.2f v=%.3f(v_ref=%.3f) (蠅_ref=%.3f, 蠅_cmd=%.3f, 蠅=%.3f)\n', ...
            ey_peak, ey_raw, t_ey, v_act_ey, v_ref_ey, omega_ref_ey, omega_cmd_ey, omega_act_ey);
        fprintf('             epsi=%.3f(raw=%+.3f)@t=%.2f v=%.3f(v_ref=%.3f) (蠅_ref=%.3f, 蠅_cmd=%.3f, 蠅=%.3f)\n', ...
            epsi_peak, epsi_raw, t_ep, v_act_ep, v_ref_ep, omega_ref_ep, omega_cmd_ep, omega_act_ep);

        if isfinite(w_min) && isfinite(w_max)
            if omega_cmd_ey < w_min - 1e-6 || omega_cmd_ey > w_max + 1e-6 || omega_cmd_ep < w_min - 1e-6 || omega_cmd_ep > w_max + 1e-6
                fprintf('      鈿?omega_cmd 瓒呭嚭 mpcobj.MV(2) 绾︽潫鑼冨洿: [%.3f, %.3f]\n', w_min, w_max);
            end
        end
    end

    report.worst_zone = worst_zone;
    report.worst_score = worst_score;
    if ~isempty(worst_zone)
        fprintf('    [Worst Zone] %s (score=%.2f)\n', worst_zone, worst_score);
    end
end

function validate_ref(ref)
% 鎵撳嵃骞舵鏌ュ弬鑰冭矾寰勭殑鍩烘湰涓€鑷存€э紝甯姪鎺掓煡绗﹀彿/涓嶈繛缁?

    req = {'t','X_ref','Y_ref','psi_ref','v_ref','omega_ref','theta_ref'};
    for i = 1:numel(req)
        if ~isfield(ref, req{i})
            error('ref 缂哄皯瀛楁: %s', req{i});
        end
    end

    t = ref.t(:);
    if any(~isfinite(t)) || any(diff(t) <= 0)
        error('ref.t 闈炰弗鏍奸€掑鎴栧寘鍚潪鏈夐檺鍊?);
    end

    fprintf('    [ref] T=%.2fs, dt鈮?.4fs, v鈭圼%.3f,%.3f], 蠅鈭圼%.3f,%.3f], 胃鈭圼%.1f,%.1f]deg\n', ...
        t(end), median(diff(t)), min(ref.v_ref), max(ref.v_ref), min(ref.omega_ref), max(ref.omega_ref), ...
        rad2deg(min(ref.theta_ref)), rad2deg(max(ref.theta_ref)));

    % psi/omega 涓€鑷存€э細omega 鈮?d(psi)/dt
    psi = unwrap(ref.psi_ref(:));
    dpsi = diff(psi) ./ diff(t);
    omega_mid = 0.5 * (ref.omega_ref(1:end-1) + ref.omega_ref(2:end));
    w_err = dpsi - omega_mid(:);
    fprintf('    [ref] check: RMS(dpsi/dt - omega_ref)=%.4f rad/s, max|螖psi|=%.4f rad/step\n', ...
        rms(w_err(~isnan(w_err) & isfinite(w_err))), max(abs(diff(psi))));
end

function zones = get_ref_zones(ref)
% 灏濊瘯浠?ref.meta.zones 鑾峰彇鍒嗗尯锛涘惁鍒欎娇鐢ㄥ伐涓氶粯璁ゅ垎鍖?

    zones = struct();
    if isfield(ref, 'meta') && isfield(ref.meta, 'zones')
        z = ref.meta.zones;
        fns = fieldnames(z);
        for i = 1:numel(fns)
            zones.(fns{i}) = z.(fns{i});
        end
        return;
    end

    % 榛樿宸ヤ笟鍒嗗尯 (120s)
    zones.startup = [0, 10];
    zones.golden_test = [10, 50];
    zones.pure_turn = [50, 70];
    zones.pure_slope = [70, 90];
    zones.composite = [90, 110];
    zones.closure = [110, 120];
end


