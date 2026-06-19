function result = run_stage1_closed_loop_validation(cfg)
%RUN_STAGE1_CLOSED_LOOP_VALIDATION Run three-path plantfix closed-loop validation.
%
% Modes:
%   preflight - verify artifacts only
%   smoke     - run each controller on a short prefix
%   full      - run the full three-path comparison

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '09_closed_loop');
if exist(node_dir, 'dir') ~= 7
    mkdir(node_dir);
end
if ~isfield(cfg, 'mode') || isempty(cfg.mode); cfg.mode = 'preflight'; end
if ~isfield(cfg, 'stop_time_override') || isempty(cfg.stop_time_override)
    if strcmpi(cfg.mode, 'smoke')
        cfg.stop_time_override = 5.0;
    else
        cfg.stop_time_override = [];
    end
end
if ~isfield(cfg, 'stop_on_error') || isempty(cfg.stop_on_error); cfg.stop_on_error = true; end

plant = agv_plant_revision(parameters());
paths = local_paths(root, node_dir);
models = local_models(root, cfg.mode);
preflight = local_preflight(paths, models, plant);
mpc_candidate = [];
if exist(paths.maps_file, 'file') == 2
    mpc_candidate = local_load_mpc_candidate(paths.maps_file);
end

result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.mode = cfg.mode;
result.cfg = cfg;
result.plant_revision = plant;
result.models = models;
result.paths = paths;
result.mpc_candidate = mpc_candidate;
result.preflight = preflight;
local_write_json(fullfile(node_dir, 'stage1_closed_loop_preflight.json'), preflight);

if ~preflight.pass || strcmpi(cfg.mode, 'preflight')
    if preflight.pass
        result.status = 'preflight_ok';
    else
        result.status = 'preflight_failed';
    end
    result.path_runs = table();
    local_write_report(node_dir, result);
    save(fullfile(node_dir, 'stage1_closed_loop_result.mat'), 'result', '-v7.3');
    if ~preflight.pass
        error('stage1_closed_loop:PreflightFailed', 'Closed-loop preflight failed.');
    end
    return;
end

path_runs = local_run_all(root, node_dir, paths, models, cfg, mpc_candidate);
result.path_runs = path_runs;
writetable(path_runs, fullfile(node_dir, 'stage1_closed_loop_path_runs.csv'));

[summary_table, aggregate_table] = local_collect(path_runs);
result.summary_table = summary_table;
result.aggregate_table = aggregate_table;
if ~isempty(summary_table)
    writetable(summary_table, fullfile(node_dir, 'stage1_closed_loop_summary.csv'));
end
if ~isempty(aggregate_table)
    writetable(aggregate_table, fullfile(node_dir, 'stage1_closed_loop_aggregate.csv'));
end
result.status = 'done';
local_write_report(node_dir, result);
save(fullfile(node_dir, 'stage1_closed_loop_result.mat'), 'result', '-v7.3');
fprintf('[stage1 closed-loop] done: %s\n', fullfile(node_dir, 'stage1_closed_loop_report.md'));
end

function models = local_models(root, mode)
model_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models');
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
if strcmpi(mode, 'smoke')
    phase = 'smoke';
    gru_tag = 'smoke_gru_v5_plantfix_passive17_plus_all5_seed101';
    tcn_tag = 'smoke_tcn_v5_plantfix_passive17_plus_all5_seed21';
    tcn_seed = 21;
else
    phase = 'full';
    gru_tag = 'full_gru_v5_plantfix_passive17_plus_all5_seed101';
    tcn_tag = 'full_tcn_v5_plantfix_passive17_plus_all5_seed101';
    tcn_seed = 101;
end
models = struct();
models.phase = phase;
models.dataset_file = dataset_file;
models.modern_tcn = struct( ...
    'seed', 21, ...
    'dataset_file', dataset_file, ...
    'onnx_file', fullfile(model_dir, 'modern_tcn', ...
        'modern_tcn_v5_plantfix_passive17_plus_all5_seed21', 'modern_tcn_seed21.onnx'), ...
    'run_tag', 'stage1_v5_plantfix_passive17_plus_all5_seed21');
models.gru = struct( ...
    'seed', 101, ...
    'dataset_file', dataset_file, ...
    'model_file', fullfile(model_dir, 'models', ...
        ['GRU_model_' gru_tag '.mat']), ...
    'meta_file', fullfile(model_dir, 'models', ...
        ['GRU_meta_' gru_tag '.mat']));
models.tcn = struct( ...
    'seed', tcn_seed, ...
    'dataset_file', dataset_file, ...
    'model_file', fullfile(model_dir, 'models', ...
        ['TCN_model_' tcn_tag '.mat']), ...
    'meta_file', fullfile(model_dir, 'models', ...
        ['TCN_meta_' tcn_tag '.mat']));
end

function paths = local_paths(root, node_dir)
paths = struct();
paths.node_dir = node_dir;
paths.path_files = { ...
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v3.mat'), ...
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat'), ...
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')};
paths.theta0_model = fullfile(root, 'simulink', 'LPVMPC_AGV_simulink_IMU.slx');
paths.oracle_ref_model = fullfile(root, 'simulink', 'LPVMPC_AGV_simulink_ref.slx');
paths.modern_model = fullfile(root, 'simulink', 'LPVMPC_AGV_simulink_Modern_TCN.slx');
paths.gru_model = fullfile(root, 'simulink', 'LPVMPC_AGV_simulink_GRU.slx');
paths.tcn_model = fullfile(root, 'simulink', 'LPVMPC_AGV_simulink_TCN.slx');
paths.maps_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning', ...
    'maps_best_agv_physics_v2_plantfix_stage1.mat');
end

function preflight = local_preflight(paths, models, plant)
checks = struct();
checks.plant_revision = strcmp(plant.id, 'agv_physics_v2_plantfix');
checks.dataset = exist(models.dataset_file, 'file') == 2;
checks.modern_onnx = exist(models.modern_tcn.onnx_file, 'file') == 2;
checks.gru_model = exist(models.gru.model_file, 'file') == 2 && exist(models.gru.meta_file, 'file') == 2;
checks.tcn_model = exist(models.tcn.model_file, 'file') == 2 && exist(models.tcn.meta_file, 'file') == 2;
checks.oracle_ref_shell = local_exists_file_or_model(paths.oracle_ref_model);
checks.theta0_shell = local_exists_file_or_model(paths.theta0_model);
checks.learned_shells = local_exists_file_or_model(paths.modern_model) && ...
    local_exists_file_or_model(paths.gru_model) && local_exists_file_or_model(paths.tcn_model);
checks.three_paths = all(cellfun(@(p) exist(p, 'file') == 2, paths.path_files));
checks.oracle_not_imu = contains(paths.oracle_ref_model, 'simulink_ref') && ...
    ~contains(paths.oracle_ref_model, 'simulink_IMU');
checks.maps_candidate = exist(paths.maps_file, 'file') == 2;
preflight = struct('checks', checks, 'pass', all(structfun(@(x) isequal(x, true), checks)));
end

function path_runs = local_run_all(root, node_dir, paths, models, cfg, mpc_candidate)
rows = repmat(local_path_row(), numel(paths.path_files), 1);
for i = 1:numel(paths.path_files)
    path_file = paths.path_files{i};
    [~, path_tag] = fileparts(path_file);
    path_dir = fullfile(node_dir, path_tag);
    if exist(path_dir, 'dir') ~= 7; mkdir(path_dir); end
    rows(i).path_tag = string(path_tag);
    rows(i).path_file = string(path_file);
    rows(i).out_dir = string(path_dir);
    try
        sim_cfg = struct('stop_time_override', cfg.stop_time_override);
        if ~isempty(mpc_candidate)
            sim_cfg.mpc_runtime_override = mpc_candidate.runtime_override;
        end
        modern_out = fullfile(path_dir, 'ModernTCN_v5_plantfix_out.mat');
        gru_out = fullfile(path_dir, 'GRU_v5_plantfix_out.mat');
        tcn_out = fullfile(path_dir, 'TCN_v5_plantfix_out.mat');
        theta0_out = fullfile(path_dir, 'lpvmpc_theta0_out.mat');
        oracle_out = fullfile(path_dir, 'lpvmpc_oracle_theta_out.mat');

        local_run_learned(root, 'LPVMPC_AGV_simulink_Modern_TCN', path_file, modern_out, sim_cfg, models, 'modern_tcn');
        local_run_learned(root, 'LPVMPC_AGV_simulink_GRU', path_file, gru_out, sim_cfg, models, 'gru');
        local_run_learned(root, 'LPVMPC_AGV_simulink_TCN', path_file, tcn_out, sim_cfg, models, 'tcn');
        local_run_theta0(path_file, path_dir, sim_cfg);
        local_run_oracle_ref(root, path_file, oracle_out, sim_cfg);

        extra_runs = [ ...
            struct('label', "LPV-MPC_theta0", 'file', theta0_out), ...
            struct('label', "LPV-MPC_oracle_theta", 'file', oracle_out)];
        compare_tcn_gru_modern_closed_loop_out( ...
            modern_out, gru_out, tcn_out, path_file, path_dir, ...
            "ModernTCN", extra_runs, ...
            'Stage 1 plantfix ModernTCN/GRU/TCN closed-loop comparison', ...
            'stage1_plantfix_closed_loop');

        rows(i).modern_file = string(modern_out);
        rows(i).gru_file = string(gru_out);
        rows(i).tcn_file = string(tcn_out);
        rows(i).theta0_file = string(theta0_out);
        rows(i).oracle_file = string(oracle_out);
        rows(i).summary_file = string(fullfile(path_dir, 'stage1_plantfix_closed_loop_summary.csv'));
        rows(i).rank_file = string(fullfile(path_dir, 'stage1_plantfix_closed_loop_rank.csv'));
        rows(i).status = "ok";
    catch ME
        rows(i).status = "error";
        rows(i).message = string(ME.message);
        if cfg.stop_on_error
            path_runs = struct2table(rows(1:i));
            writetable(path_runs, fullfile(node_dir, 'stage1_closed_loop_path_runs_partial.csv'));
            rethrow(ME);
        end
    end
end
path_runs = struct2table(rows);
end

function local_run_learned(root, model_name, path_file, out_file, cfg, models, kind)
params = parameters();
sim_cfg = struct();
switch kind
    case 'modern_tcn'
        sim_cfg.modern_tcn_sim_cfg = struct( ...
            'seed', models.modern_tcn.seed, ...
            'run_tag', models.modern_tcn.run_tag, ...
            'dataset_file', models.modern_tcn.dataset_file, ...
            'onnx_file', models.modern_tcn.onnx_file, ...
            'theta_output_gain', 1.0, ...
            'theta_abs_limit', deg2rad(12.0), ...
            'theta_rate_limit', deg2rad(5.0), ...
            'theta_mpc_deadzone', deg2rad(2.0));
    case 'gru'
        Sg = load(models.gru.model_file, 'model');
        Mg = load(models.gru.meta_file, 'meta');
        assignin('base', 'gru_model', Sg.model);
        assignin('base', 'gru_meta', Mg.meta);
        sim_cfg.gru_sim_cfg = struct( ...
            'seed', models.gru.seed, ...
            'dataset_file', models.gru.dataset_file, ...
            'model_file', models.gru.model_file, ...
            'meta_file', models.gru.meta_file, ...
            'theta_output_gain', 1.0, ...
            'theta_abs_limit', deg2rad(12.0), ...
            'theta_rate_limit', deg2rad(5.0), ...
            'theta_mpc_deadzone', deg2rad(2.0));
    case 'tcn'
        St = load(models.tcn.model_file, 'model');
        Mt = load(models.tcn.meta_file, 'meta');
        assignin('base', 'tcn_model', St.model);
        assignin('base', 'tcn_meta', Mt.meta);
        sim_cfg.tcn_sim_cfg = struct( ...
            'seed', models.tcn.seed, ...
            'dataset_file', models.tcn.dataset_file, ...
            'model_file', models.tcn.model_file, ...
            'meta_file', models.tcn.meta_file, ...
            'theta_output_gain', 1.0, ...
            'theta_abs_limit', deg2rad(12.0), ...
            'theta_rate_limit', deg2rad(5.0), ...
            'theta_mpc_deadzone', deg2rad(2.0));
end
sim_cfg.params_override = params;
sim_cfg.stop_time_override = cfg.stop_time_override;
if isfield(cfg, 'mpc_runtime_override') && ~isempty(cfg.mpc_runtime_override)
    sim_cfg.mpc_runtime_override = cfg.mpc_runtime_override;
end
run_closed_loop_model_once(model_name, path_file, out_file, sim_cfg);
local_append_audit(out_file, kind, model_name, path_file, models, root);
end

function local_run_theta0(path_file, path_dir, sim_cfg)
bcfg = struct();
bcfg.path_file = path_file;
bcfg.out_dir = path_dir;
bcfg.compare_with_learned = false;
bcfg.stop_time_override = sim_cfg.stop_time_override;
bcfg.stop_on_error = true;
bcfg.params_override = parameters();
if isfield(sim_cfg, 'mpc_runtime_override') && ~isempty(sim_cfg.mpc_runtime_override)
    bcfg.runtime_override = sim_cfg.mpc_runtime_override;
end
bcfg.modes = struct('tag', 'lpvmpc_theta0', 'label', 'LPV-MPC_theta0', 'value', 1);
run_lpvmpc_theta_baseline_experiment(bcfg);
end

function local_run_oracle_ref(root, path_file, out_file, cfg)
model_name = 'LPVMPC_AGV_simulink_ref';
S = load(path_file, 'ref');
ref = S.ref;
if isempty(cfg.stop_time_override)
    stop_time = num2str(ref.t(end));
else
    stop_time = num2str(min(double(cfg.stop_time_override), double(ref.t(end))));
end
assignin('base', 'ref', ref);
assignin('base', 'params', parameters());
assignin('base', 'preload_skip_gru_model', true);
had_override = evalin('base', 'exist(''mpc_runtime_override'', ''var'')==1');
old_override = [];
if had_override
    old_override = evalin('base', 'mpc_runtime_override');
end
cleanup_override = onCleanup(@() local_restore_base_var('mpc_runtime_override', had_override, old_override)); %#ok<NASGU>
if isfield(cfg, 'mpc_runtime_override') && ~isempty(cfg.mpc_runtime_override)
    assignin('base', 'mpc_runtime_override', cfg.mpc_runtime_override);
end
model_file = fullfile(root, 'simulink', [model_name '.slx']);
if bdIsLoaded(model_name); close_system(model_name, 0); end
load_system(model_file);
cleanup = onCleanup(@() local_close_model(model_name)); %#ok<NASGU>
simIn = Simulink.SimulationInput(model_name);
simIn = simIn.setModelParameter('StopTime', stop_time);
simIn = simIn.setVariable('ref', ref);
simIn = simIn.setVariable('params', parameters());
simIn = simIn.setVariable('preload_skip_gru_model', true);
if isfield(cfg, 'mpc_runtime_override') && ~isempty(cfg.mpc_runtime_override)
    simIn = simIn.setVariable('mpc_runtime_override', cfg.mpc_runtime_override);
    simIn = simIn.setVariable('mpc_runtime_override', cfg.mpc_runtime_override, 'Workspace', model_name);
end
simOut = sim(simIn);
logsout = local_materialize_dataset(simOut.logsout);
SimulationMetadata = simOut.SimulationMetadata; %#ok<NASGU>
node6_model_audit = struct('kind', 'ref_oracle', ...
    'oracle_model', model_name, 'theta_mode_used', NaN, ...
    'plant_revision', 'agv_physics_v2_plantfix', ...
    'mpc_runtime_override', local_field_or_empty(cfg, 'mpc_runtime_override'), ...
    'path_file', path_file, 'time', char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'))); %#ok<NASGU>
oracle_model_used = model_name; %#ok<NASGU>
theta_mode_used = NaN; %#ok<NASGU>
save(out_file, 'logsout', 'SimulationMetadata', 'node6_model_audit', ...
    'oracle_model_used', 'theta_mode_used', '-v7.3');
local_write_json(strrep(out_file, '.mat', '_model_audit.json'), node6_model_audit);
end

function [summary_table, aggregate_table] = local_collect(path_runs)
summary_table = table();
for i = 1:height(path_runs)
    if path_runs.status(i) ~= "ok" || exist(path_runs.summary_file(i), 'file') ~= 2
        continue;
    end
    T = readtable(path_runs.summary_file(i), 'TextType', 'string');
    T.path_tag = repmat(path_runs.path_tag(i), height(T), 1);
    summary_table = [summary_table; T]; %#ok<AGROW>
end
if isempty(summary_table)
    aggregate_table = table();
    return;
end
controllers = unique(summary_table.controller, 'stable');
rows = repmat(struct('controller', "", 'n_paths', 0, 'ey_rmse_mean', NaN, ...
    'ey_peak_worst', NaN, 'xy_rmse_mean', NaN, 'j_du_mean', NaN, ...
    'rank_ey', NaN), numel(controllers), 1);
for i = 1:numel(controllers)
    mask = summary_table.controller == controllers(i);
    rows(i).controller = controllers(i);
    rows(i).n_paths = sum(mask);
    rows(i).ey_rmse_mean = mean(summary_table.ey_rmse(mask), 'omitnan');
    rows(i).ey_peak_worst = max(summary_table.ey_peak(mask), [], 'omitnan');
    rows(i).xy_rmse_mean = mean(summary_table.xy_rmse(mask), 'omitnan');
    rows(i).j_du_mean = mean(summary_table.j_du(mask), 'omitnan');
end
aggregate_table = sortrows(struct2table(rows), 'ey_rmse_mean');
aggregate_table.rank_ey = (1:height(aggregate_table))';
end

function row = local_path_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", ...
    'modern_file', "", 'gru_file', "", 'tcn_file', "", ...
    'theta0_file', "", 'oracle_file', "", 'summary_file', "", ...
    'rank_file', "", 'status', "", 'message', "");
end

function local_append_audit(out_file, kind, model_name, path_file, models, root)
audit = struct();
audit.kind = kind;
audit.model_name = model_name;
audit.path_file = path_file;
audit.plant_revision = 'agv_physics_v2_plantfix';
audit.root = root;
switch kind
    case 'modern_tcn'
        audit.dataset_file = models.modern_tcn.dataset_file;
        audit.onnx_file = models.modern_tcn.onnx_file;
    case 'gru'
        audit.dataset_file = models.gru.dataset_file;
        audit.model_file = models.gru.model_file;
        audit.meta_file = models.gru.meta_file;
    case 'tcn'
        audit.dataset_file = models.tcn.dataset_file;
        audit.model_file = models.tcn.model_file;
        audit.meta_file = models.tcn.meta_file;
end
local_write_json(strrep(out_file, '.mat', '_model_audit.json'), audit);
end

function mpc_candidate = local_load_mpc_candidate(maps_file)
S = load(maps_file, 'maps_best', 'opts', 'db_file');
if ~isfield(S, 'maps_best')
    error('stage1_closed_loop:MissingMapsBest', 'No maps_best in %s.', maps_file);
end
maps_best = S.maps_best;
if isfield(S, 'opts')
    opts = S.opts;
else
    opts = maps_best;
end
runtime_override = struct();
runtime_override.id = local_field_or_default(maps_best, 'id', 'stage1_plantfix_p0');
runtime_override.Np = local_field_or_default(opts, 'Np', local_field_or_default(maps_best, 'Np', 150));
runtime_override.Nc = local_field_or_default(opts, 'Nc', local_field_or_default(maps_best, 'Nc', 30));
runtime_override.Q = local_field_or_default(opts, 'Q', local_field_or_default(maps_best, 'Q', [100 100 15 3]));
runtime_override.R = local_field_or_default(opts, 'R', local_field_or_default(maps_best, 'R', [3e-5 3e-5]));
runtime_override.dR = local_field_or_default(opts, 'dR', local_field_or_default(maps_best, 'dR', [1e-3 1e-3]));
runtime_override.maps_template = maps_best;
if isfield(S, 'db_file') && ~isempty(S.db_file)
    runtime_override.db_file = S.db_file;
elseif isfield(maps_best, 'db_file') && ~isempty(maps_best.db_file)
    runtime_override.db_file = maps_best.db_file;
else
    workflow_dir = fileparts(fileparts(maps_file));
    runtime_override.db_file = fullfile(workflow_dir, '04_lpv_database', ...
        'lin_agv_db_agv_physics_v2_plantfix.mat');
end
mpc_candidate = struct('maps_file', maps_file, 'maps_best', maps_best, ...
    'runtime_override', runtime_override);
end

function value = local_field_or_default(s, name, default_value)
if isstruct(s) && isfield(s, name) && ~isempty(s.(name))
    value = s.(name);
else
    value = default_value;
end
end

function value = local_field_or_empty(s, name)
if isstruct(s) && isfield(s, name)
    value = s.(name);
else
    value = [];
end
end

function logsout = local_materialize_dataset(logs)
if isa(logs, 'Simulink.SimulationData.Dataset')
    logsout = logs;
elseif isa(logs, 'Simulink.SimulationData.DatasetRef')
    logsout = Simulink.SimulationData.Dataset;
    for i = 1:logs.numElements
        logsout = logsout.addElement(logs.get(i));
    end
else
    error('stage1_closed_loop:BadLogsout', 'Unsupported logsout class: %s', class(logs));
end
end

function tf = local_exists_file_or_model(path_in)
tf = exist(path_in, 'file') == 2 || exist(path_in, 'file') == 4;
end

function local_close_model(model_name)
if bdIsLoaded(model_name)
    close_system(model_name, 0);
end
end

function local_restore_base_var(name, had_value, old_value)
if had_value
    assignin('base', name, old_value);
else
    evalin('base', sprintf('clear %s', name));
end
end

function local_write_report(node_dir, result)
file = fullfile(node_dir, 'stage1_closed_loop_report.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 Plantfix Closed-Loop Report\n\n');
fprintf(fid, '- status: `%s`\n', result.status);
fprintf(fid, '- mode: `%s`\n', result.mode);
fprintf(fid, '- plant_revision: `%s`\n\n', result.plant_revision.id);
fprintf(fid, '## Preflight\n\n');
names = fieldnames(result.preflight.checks);
fprintf(fid, '| check | pass |\n|---|---:|\n');
for i = 1:numel(names)
    fprintf(fid, '| `%s` | %d |\n', names{i}, double(result.preflight.checks.(names{i})));
end
fprintf(fid, '\n## Oracle Provenance\n\n');
fprintf(fid, '- oracle entrypoint: `LPVMPC_AGV_simulink_ref.slx`\n');
fprintf(fid, '- theta0 entrypoint: `LPVMPC_AGV_simulink_IMU.slx` with `theta_mode=1`\n');
fprintf(fid, '- these are recorded as separate controller rows and are not merged.\n');
if isfield(result, 'models') && isfield(result.models, 'phase')
    fprintf(fid, '- model phase: `%s`\n', result.models.phase);
end
if isfield(result, 'mpc_candidate') && ~isempty(result.mpc_candidate)
    fprintf(fid, '- MPC runtime override: `%s`\n', result.mpc_candidate.runtime_override.id);
    fprintf(fid, '- MPC maps file: `%s`\n', result.mpc_candidate.maps_file);
end
if isfield(result, 'aggregate_table') && ~isempty(result.aggregate_table)
    fprintf(fid, '\n## Aggregate Ranking\n\n');
    fprintf(fid, '| rank | controller | ey_rmse_mean | ey_peak_worst | j_du_mean |\n');
    fprintf(fid, '|---:|---|---:|---:|---:|\n');
    for i = 1:height(result.aggregate_table)
        fprintf(fid, '| %d | `%s` | %.6g | %.6g | %.6g |\n', ...
            result.aggregate_table.rank_ey(i), result.aggregate_table.controller(i), ...
            result.aggregate_table.ey_rmse_mean(i), result.aggregate_table.ey_peak_worst(i), ...
            result.aggregate_table.j_du_mean(i));
    end
end
end

function local_write_json(file, payload)
folder = fileparts(file);
if ~isempty(folder) && exist(folder, 'dir') ~= 7; mkdir(folder); end
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
try
    txt = jsonencode(payload, 'PrettyPrint', true);
catch
    txt = jsonencode(payload);
end
fprintf(fid, '%s\n', txt);
end
