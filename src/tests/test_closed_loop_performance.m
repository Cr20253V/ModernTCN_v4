% =============================
% 文件名：test_closed_loop_performance.m
% 版本号：V1.0
% 最后修改时间：2025-11-24
% 作者：LPV-MPC Project
% 功能描述：
%   批量运行 LPVMPC_AGV_simulink，提取速度、姿态、坡度识别、
%   执行器饱和等闭环指标，用于对比不同 GRU 或控制配置。
%   默认会针对 flat / straight / turn / straight_turn / slope / bumpy
%   等行驶模式逐一取样仿真，亦可通过 cfg.scenarios 自定义。
% 使用方法：
%   >> test_closed_loop_performance();
%   >> cfg = struct('mode_names', {{'flat','slope','bumpy'}}, 'mode_sample_count', 2);
%   >> test_closed_loop_performance(cfg);
% 输出：
%   - timeseries_<scene>.mat：仿真时序数据（可选）
%   - closed_loop_summary_<tag>.mat：各场景指标与均值
% 依赖：
%   - LPVMPC_AGV_simulink.slx（需开启 diag.* 日志）
%   - 各 path_*.mat 参考轨迹文件（或自定义结构体）
% 备注：
%   - cfg.scenarios 可传字符串或结构体，结构体需包含 name/path_file
%   - 指标计算依赖 signal_names 映射，可按需求扩展
% =============================

function summary = test_closed_loop_performance(cfg)

root = project_root();
data_paths_dir = fullfile(root, 'data', 'paths');
default_results_dir = results_dir('closed_loop');

if nargin < 1 || isempty(cfg)
    cfg = struct();
end

% 统一填充默认参数，提高脚本易用性
cfg = apply_defaults(cfg, struct( ...
    'model_name',           'LPVMPC_AGV_simulink', ...
    'scenarios',            {{'flat','straight','turn','straight_turn','slope','bumpy'}}, ...
    'mode_sample_count',    10, ...
    'stop_time',            [], ...
    'results_dir',          default_results_dir, ...
    'save_timeseries',      true, ...
    'signal_names',         default_signal_names(), ...
    'F_cmd_limit',          300, ...
    'deadzone_info',        struct('theta_low',1,'theta_high',1.5), ...
    'report_tag',           datestr(now,'yyyymmdd_HHMMSS') ...
));

fprintf('\n===============================================\n');
fprintf('闭环仿真评估 (test_closed_loop_performance)\n');
fprintf('===============================================\n');
scenario_list = scenario_names_to_cell(cfg.scenarios);
fprintf('  目标场景列表: %s\n', strjoin(scenario_list, ', '));

% 加载 Simulink 模型，提前创建输出目录
if ~bdIsLoaded(cfg.model_name)
    load_system(cfg.model_name);
end
if ~exist(cfg.results_dir, 'dir')
    mkdir(cfg.results_dir);
end

% 构建场景配置（文件或结构体），并逐个仿真
scenario_defs = build_scenarios(cfg.scenarios, cfg.stop_time);
scenario_defs = replicate_scenarios(scenario_defs, cfg.mode_sample_count);
fprintf('  实际仿真场景数: %d (mode_sample_count=%d)\n', numel(scenario_defs), cfg.mode_sample_count);
reports = cell(numel(scenario_defs), 1);
for i = 1:numel(scenario_defs)
    sc = scenario_defs{i};
    fprintf('\n[%d/%d] 场景 %s\n', i, numel(scenario_defs), sc.name);
    % 调用 run_simulation 执行 Simulink 仿真
    sim_out = run_simulation(cfg.model_name, sc);
    % 对仿真结果做统一解析
    rpt = analyze_results(sim_out, sc, cfg.signal_names, cfg.F_cmd_limit);
    reports{i} = rpt;
    if cfg.save_timeseries
        save(fullfile(cfg.results_dir, sprintf('timeseries_%s.mat', sc.name)), 'sim_out');
    end
end
% 聚合指标并保存
summary = aggregate_reports(reports, cfg);
save(fullfile(cfg.results_dir, sprintf('closed_loop_summary_%s.mat', cfg.report_tag)), 'summary');

print_final(summary);

end

%% ======================================================================
function scenario_defs = build_scenarios(names_or_structs, stop_time_override)
% 将字符串/结构体输入统一转换为标准场景结构
if isstruct(names_or_structs)
    entries = num2cell(names_or_structs);
else
    entries = scenario_names_to_cell(names_or_structs);
end

scenario_defs = cell(numel(entries), 1);
for i = 1:numel(entries)
    entry = entries{i};
    if ischar(entry) || isstring(entry)
        scenario_defs{i} = scenario_from_name(char(entry));
    elseif isstruct(entry)
        scenario_defs{i} = entry;
    else
        error('scenarios 参数不支持的类型：%s', class(entry));
    end
    if ~isempty(stop_time_override)
        scenario_defs{i}.stop_time = stop_time_override;
    end
end
end

function scenario_defs = replicate_scenarios(base_scenarios, sample_count)
% 根据 sample_count 复制场景，用于多次取样
if isempty(base_scenarios)
    error('场景列表为空，无法执行仿真。');
end
sample_count = max(1, round(sample_count));
if sample_count == 1
    scenario_defs = base_scenarios;
    return;
end

scenario_defs = cell(numel(base_scenarios)*sample_count, 1);
idx = 1;
for i = 1:numel(base_scenarios)
    base = base_scenarios{i};
    for k = 1:sample_count
        sc = base;
        sc.name = sprintf('%s_%02d', base.name, k);
        scenario_defs{idx} = sc;
        idx = idx + 1;
    end
end
end

function sc = scenario_from_name(name)
paths_dir = fullfile(project_root(), 'data', 'paths');
% 预设三种常用场景，便于快速调用
switch name
    case {'path_flat_default','flat'}
        sc = struct('name','path_flat_default','path_file',fullfile(paths_dir,'path_straight.mat'),'description','平路/低坡');
    case {'straight','path_straight'}
        sc = struct('name','path_straight','path_file',fullfile(paths_dir,'path_straight.mat'),'description','直线恒速');
    case {'turn','path_turn'}
        sc = struct('name','path_turn','path_file',fullfile(paths_dir,'path_turn.mat'),'description','恒速转弯');
    case {'straight_turn','path_straight_turn'}
        sc = struct('name','path_straight_turn','path_file',fullfile(paths_dir,'path_straight_turn.mat'),'description','直线+弯道混合');
    case {'path_slope_default','slope'}
        sc = struct('name','path_slope_default','path_file',fullfile(paths_dir,'path_slope.mat'),'description','长上坡');
    case {'path_bumpy_default','bumpy'}
        sc = struct('name','path_bumpy_default','path_file',fullfile(paths_dir,'path_bumpy.mat'),'description','连续扰动');
    otherwise
        error('未知场景名称: %s', name);
end
end

%% ======================================================================
function sim_out = run_simulation(model_name, sc)
% 根据场景加载参考路径并调用 Simulink
ref_struct = load_ref_path(sc.path_file);
assignin('base','agv_ref_path', ref_struct);
assignin('base','ref', ref_struct);  % 兼容 From Workspace 的默认变量名
if isfield(sc,'stop_time') && ~isempty(sc.stop_time)
        stop_time = sc.stop_time;
else
    stop_time = ref_struct.t(end);
end
simIn = Simulink.SimulationInput(model_name);
simIn = simIn.setModelParameter('StopTime', num2str(stop_time));
simIn = simIn.setModelParameter('SignalLogging','on');
simIn = simIn.setModelParameter('LoggingToFile','off');

try
    sim_out = sim(simIn);
catch ME
    warning(ME.identifier, 'Simulink 仿真失败: %s', ME.message);
    rethrow(ME);
end
end

function ref = load_ref_path(path_file)
% 载入路径文件并兼容旧版格式
if ~exist(path_file, 'file')
    error('路径文件不存在: %s', path_file);
end
S = load(path_file);
if isfield(S, 'ref')
    ref = S.ref;
else
    ref = S; % 兼容历史文件
end
end

%% ======================================================================
function rpt = analyze_results(sim_out, sc, signal_names, F_cmd_limit)
if nargin < 4
    F_cmd_limit = [];
end
% 提取仿真日志信号并计算各类误差指标
logsout = sim_out.logsout;
required = struct2cell(signal_names);
missing = {};
for i = 1:numel(required)
    if isempty(logsout.get(required{i}))
        missing{end+1} = required{i}; %#ok<AGROW>
    end
end
if ~isempty(missing)
    error('缺少日志信号: %s', strjoin(missing, ', '));
end

sig = struct();
fields = fieldnames(signal_names);
for i = 1:numel(fields)
    f = fields{i};
    sig.(f) = logsout.get(signal_names.(f)).Values;
end

% 速度误差指标
speed_err = sig.v_ref.Data - sig.v.Data;
rpt.speed_rms = rms(speed_err);
rpt.speed_peak = max(abs(speed_err));
rpt.speed_steady = mean(speed_err(end-round(0.1*numel(speed_err)):end));

% theta 相关
rpt.theta_mae = mean(abs(sig.theta_ref.Data - sig.theta_hat.Data));

% 命令饱和：统计驱动力指令超过 95% 阈值的比例
cmd_abs = abs(sig.F_cmd.Data);
if isempty(F_cmd_limit)
    max_cmd = max(cmd_abs);
    if max_cmd <= 0
        sat_threshold = Inf; % 避免 0/0，表示无饱和
    else
        sat_threshold = 0.95 * max_cmd;
    end
else
    sat_threshold = 0.95 * F_cmd_limit;
end
rpt.cmd_sat_ratio = mean(cmd_abs > sat_threshold);

% slope 检测延迟：将 label_main 与地面坡度变化对齐
rpt.slope_delay = compute_delay(sig.label_main, sig.theta_ground);

rpt.name = sc.name;
rpt.description = sc.description;
rpt.duration = sig.v.Time(end) - sig.v.Time(1);
end

function delay = compute_delay(label_signal, theta_ground_signal)
% 计算 slope 场景中预测与真值的首次出现时间差
truth_idx = find(theta_ground_signal.Data > deg2rad(1), 1, 'first');
pred_idx = find(label_signal.Data == 4, 1, 'first');
if isempty(truth_idx) || isempty(pred_idx)
    delay = NaN;
else
    delay = label_signal.Time(pred_idx) - theta_ground_signal.Time(truth_idx);
end
end

%% ======================================================================
function summary = aggregate_reports(reports, cfg)
% 聚合所有场景的统计量，便于横向对比
speed_rms = cellfun(@(r) r.speed_rms, reports);
theta_mae = cellfun(@(r) r.theta_mae, reports);
delay = cellfun(@(r) r.slope_delay, reports);
summary = struct();
summary.reports = reports;
summary.mean_speed_rms = mean(speed_rms);
summary.mean_theta_mae = mean(theta_mae);
summary.mean_delay = mean(delay,'omitnan');
summary.config = cfg;
end

function print_final(summary)
% 控制台输出核心指标，配合保存的 mat 文件查看详情
fprintf('\n关键指标\n');
fprintf('  - 平均速度 RMS 误差: %.3f m/s\n', summary.mean_speed_rms);
fprintf('  - 平均坡度 MAE: %.3f rad\n', summary.mean_theta_mae);
fprintf('  - 平均坡度识别延迟: %.2f s\n', summary.mean_delay);
fprintf('\n  场景拆分指标：\n');
for i = 1:numel(summary.reports)
    rpt = summary.reports{i};
    fprintf('    • %-18s | v_RMS=%.3f m/s | θ_MAE=%.3f rad | delay=%s | sat=%.1f%%%%\n', ...
        rpt.name, rpt.speed_rms, rpt.theta_mae, format_delay_text(rpt.slope_delay), rpt.cmd_sat_ratio*100);
end
end

function txt = format_delay_text(val)
if isnan(val)
    txt = 'NaN';
else
    txt = sprintf('%.2f s', val);
end
end

%% ======================================================================
function names = default_signal_names()
% 默认日志信号映射，可根据 Simulink 日志命名调整
names = struct();
names.v = 'diag.v';
names.v_ref = 'diag.v_ref';
names.theta_hat = 'diag.theta_hat';
names.theta_ref = 'diag.theta_ref';
names.theta_ground = 'diag.theta_ground';
names.label_main = 'diag.label_main';
names.F_cmd = 'diag.F_cmd';
end

%% ======================================================================
function cfg = apply_defaults(cfg, defaults)
% 递归填充缺省配置项
fields = fieldnames(defaults);
for i = 1:numel(fields)
    f = fields{i};
    if ~isfield(cfg, f) || isempty(cfg.(f))
        cfg.(f) = defaults.(f);
    end
end
end

function names = scenario_names_to_cell(input)
% 将字符串/字符向量/元胞混合转换为 cellstr
if iscell(input)
    names = input;
elseif isstring(input)
    names = cellstr(input);
elseif ischar(input)
    names = {input};
else
    error('场景名称必须为字符串、字符向量或其元胞数组，收到类型: %s', class(input));
end
end
