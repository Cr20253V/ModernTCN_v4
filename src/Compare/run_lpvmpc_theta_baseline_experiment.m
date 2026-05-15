function result = run_lpvmpc_theta_baseline_experiment(cfg)
%RUN_LPVMPC_THETA_BASELINE_EXPERIMENT Run LPV-MPC theta-source baselines.
%
% Default experiment:
%   - same showcase path as the current ModernTCN/GRU/TCN closed-loop table
%   - same LPV-MPC controller and plant model
%   - theta_mode=1: nominal theta=0
%   - theta_mode=2: IMU theta estimate
%   - theta_mode=3: oracle true theta upper bound
%
% Example:
%   result = run_lpvmpc_theta_baseline_experiment();
%
% Smoke test:
%   cfg = struct('compare_with_learned', false, 'stop_time_override', 0.2);
%   cfg.modes = struct('tag', 'lpvmpc_theta0', 'label', 'LPV-MPC_theta0', 'value', 1);
%   result = run_lpvmpc_theta_baseline_experiment(cfg);

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();
cfg = local_apply_defaults(cfg, root);

S = load(cfg.path_file, 'ref');
if ~isfield(S, 'ref')
    error('run_lpvmpc_theta_baseline:MissingRef', ...
        'Path file has no ref variable: %s', cfg.path_file);
end
ref = S.ref;

if isempty(cfg.stop_time_override)
    stop_time = num2str(ref.t(end));
else
    stop_time = num2str(cfg.stop_time_override);
end

if exist(cfg.out_dir, 'dir') ~= 7
    mkdir(cfg.out_dir);
end

fprintf('\n[theta-baseline] path: %s\n', cfg.path_file);
fprintf('[theta-baseline] output: %s\n', cfg.out_dir);
fprintf('[theta-baseline] StopTime=%s, modes=%d\n\n', stop_time, numel(cfg.modes));

mode_runs = repmat(local_mode_run_template(), numel(cfg.modes), 1);
for i = 1:numel(cfg.modes)
    one = cfg.modes(i);
    fprintf('[theta-baseline] %d/%d %s (theta_mode=%g)\n', ...
        i, numel(cfg.modes), one.label, one.value);

    out_file = fullfile(cfg.out_dir, sprintf('%s_out.mat', one.tag));
    t0 = tic;
    try
        mode_runs(i).tag = string(one.tag);
        mode_runs(i).label = string(one.label);
        mode_runs(i).theta_mode = double(one.value);
        mode_runs(i).file = out_file;

        local_run_one_mode(cfg, ref, stop_time, one.value, out_file);

        mode_runs(i).status = "ok";
        mode_runs(i).elapsed_sec = toc(t0);
        fprintf('[theta-baseline] saved: %s\n', out_file);
    catch ME
        mode_runs(i).status = "error";
        mode_runs(i).message = string(ME.message);
        mode_runs(i).elapsed_sec = toc(t0);
        if cfg.stop_on_error
            rethrow(ME);
        end
        warning('run_lpvmpc_theta_baseline:ModeFailed', ...
            '%s failed: %s', one.label, ME.message);
    end
end

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.path_file = cfg.path_file;
result.out_dir = cfg.out_dir;
result.model_name = cfg.model_name;
result.mode_runs = mode_runs;
result.compare = [];

save(fullfile(cfg.out_dir, 'lpvmpc_theta_baseline_runs.mat'), 'result', '-v7.3');

if cfg.compare_with_learned
    ok_mask = arrayfun(@(r) strcmp(char(r.status), 'ok'), mode_runs);
    ok = mode_runs(ok_mask);
    extra_runs = repmat(struct('label', "", 'file', ""), 1, numel(ok));
    for i = 1:numel(ok)
        extra_runs(i).label = ok(i).label;
        extra_runs(i).file = ok(i).file;
    end

    result.compare = compare_tcn_gru_modern_closed_loop_out( ...
        cfg.learned_outputs.ModernTCN, ...
        cfg.learned_outputs.GRU, ...
        cfg.learned_outputs.TCN, ...
        cfg.path_file, ...
        cfg.out_dir, ...
        "ModernTCN", ...
        extra_runs, ...
        'ModernTCN、GRU、TCN 与 LPV-MPC theta 基线闭环对比报告', ...
        'tcn_gru_modern_lpvmpc_theta_baseline');

    save(fullfile(cfg.out_dir, 'lpvmpc_theta_baseline_runs.mat'), 'result', '-v7.3');
end

fprintf('\n[theta-baseline] done: %s\n', cfg.out_dir);
end

function cfg = local_apply_defaults(cfg, root)
if ~isfield(cfg, 'model_name') || isempty(cfg.model_name)
    cfg.model_name = 'LPVMPC_AGV_simulink_IMU';
end
if ~isfield(cfg, 'model_file') || isempty(cfg.model_file)
    cfg.model_file = fullfile(root, 'simulink', [cfg.model_name '.slx']);
end
if ~isfield(cfg, 'path_file') || isempty(cfg.path_file)
    cfg.path_file = fullfile(root, 'data', 'paths', ...
        'path_factory_logistics_showcase_theta10_v3.mat');
end
if ~isfield(cfg, 'out_dir') || isempty(cfg.out_dir)
    [~, path_tag] = fileparts(cfg.path_file);
    cfg.out_dir = fullfile(root, 'results', 'compare', ...
        'lpvmpc_theta_baseline', path_tag);
end
if ~isfield(cfg, 'mode_block') || isempty(cfg.mode_block)
    cfg.mode_block = [cfg.model_name '/Constant4'];
end
if ~isfield(cfg, 'modes') || isempty(cfg.modes)
    cfg.modes = [ ...
        struct('tag', 'lpvmpc_theta0', 'label', 'LPV-MPC_theta0', 'value', 1), ...
        struct('tag', 'lpvmpc_imu_theta', 'label', 'LPV-MPC_IMU_theta', 'value', 2), ...
        struct('tag', 'lpvmpc_oracle_theta', 'label', 'LPV-MPC_oracle_theta', 'value', 3)];
end
if ~isfield(cfg, 'compare_with_learned')
    cfg.compare_with_learned = true;
end
if ~isfield(cfg, 'learned_outputs') || ~isstruct(cfg.learned_outputs)
    cfg.learned_outputs = struct();
end
if ~isfield(cfg.learned_outputs, 'ModernTCN') || isempty(cfg.learned_outputs.ModernTCN)
    cfg.learned_outputs.ModernTCN = fullfile(root, 'ModernTCN_out.mat');
end
if ~isfield(cfg.learned_outputs, 'GRU') || isempty(cfg.learned_outputs.GRU)
    cfg.learned_outputs.GRU = fullfile(root, 'GRU_out.mat');
end
if ~isfield(cfg.learned_outputs, 'TCN') || isempty(cfg.learned_outputs.TCN)
    cfg.learned_outputs.TCN = fullfile(root, 'TCN_out.mat');
end
if ~isfield(cfg, 'stop_time_override')
    cfg.stop_time_override = [];
end
if ~isfield(cfg, 'stop_on_error')
    cfg.stop_on_error = true;
end

if exist(cfg.model_file, 'file') ~= 2 && exist(cfg.model_file, 'file') ~= 4
    error('run_lpvmpc_theta_baseline:MissingModel', ...
        'Model file not found: %s', cfg.model_file);
end
end

function local_run_one_mode(cfg, ref, stop_time, theta_mode, out_file)
assignin('base', 'preload_skip_gru_model', true);
assignin('base', 'theta_mode', double(theta_mode));
assignin('base', 'ref', ref);

if bdIsLoaded(cfg.model_name)
    close_system(cfg.model_name, 0);
end
load_system(cfg.model_file);
cleanup = onCleanup(@() local_close_model(cfg.model_name));

simIn = Simulink.SimulationInput(cfg.model_name);
simIn = simIn.setModelParameter('StopTime', stop_time);
simIn = simIn.setVariable('preload_skip_gru_model', true);
simIn = simIn.setVariable('theta_mode', double(theta_mode));
simIn = simIn.setVariable('ref', ref);
simIn = simIn.setVariable('theta_mode', double(theta_mode), 'Workspace', cfg.model_name);
simIn = simIn.setVariable('ref', ref, 'Workspace', cfg.model_name);
simIn = simIn.setBlockParameter(cfg.mode_block, 'Value', 'theta_mode');

simOut = sim(simIn);
if isprop(simOut, 'ErrorMessage') && ~isempty(simOut.ErrorMessage)
    error('run_lpvmpc_theta_baseline:SimulationError', '%s', simOut.ErrorMessage);
end

logsout = local_materialize_dataset(simOut.logsout);
SimulationMetadata = simOut.SimulationMetadata; %#ok<NASGU>
theta_mode_used = double(theta_mode); %#ok<NASGU>
save(out_file, 'logsout', 'SimulationMetadata', 'theta_mode_used', '-v7.3');
end

function logsout = local_materialize_dataset(logs)
if isa(logs, 'Simulink.SimulationData.Dataset')
    logsout = logs;
    return;
end

if isa(logs, 'Simulink.SimulationData.DatasetRef')
    logsout = Simulink.SimulationData.Dataset;
    for i = 1:logs.numElements
        logsout = logsout.addElement(logs.get(i));
    end
    return;
end

error('run_lpvmpc_theta_baseline:BadLogsout', ...
    'Unsupported logsout class: %s', class(logs));
end

function row = local_mode_run_template()
row = struct('tag', "", 'label', "", 'theta_mode', NaN, ...
    'file', "", 'status', "pending", 'message', "", 'elapsed_sec', NaN);
end

function local_close_model(model_name)
if bdIsLoaded(model_name)
    close_system(model_name, 0);
end
end
