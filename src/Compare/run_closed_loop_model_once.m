function out_file = run_closed_loop_model_once(model_name, path_file, out_file, cfg)
%RUN_CLOSED_LOOP_MODEL_ONCE Run one Simulink closed-loop model and save logsout.
%
% This helper intentionally saves an in-memory
% Simulink.SimulationData.Dataset, not a DatasetRef.  That keeps the output
% MAT file portable and readable by comparison scripts.

if nargin < 1 || isempty(model_name)
    model_name = 'LPVMPC_AGV_simulink_Modern_TCN';
end
if nargin < 2 || isempty(path_file)
    path_file = fullfile(local_project_root(), 'data', 'paths', ...
        'path_modern_tcn_demo_loop_v1.mat');
end
if nargin < 3 || isempty(out_file)
    [~, path_tag, ~] = fileparts(path_file);
    out_file = fullfile(local_project_root(), 'results', 'compare', ...
        'modern_tcn_gru_closed_loop', sprintf('%s_%s_out.mat', model_name, path_tag));
end
if nargin < 4
    cfg = struct();
end

root = local_project_root();
if exist('init_project', 'file') == 2
    init_project();
end

S = load(path_file, 'ref');
ref = S.ref;
if isfield(cfg, 'stop_time_override') && ~isempty(cfg.stop_time_override)
    stop_time_value = min(double(cfg.stop_time_override), double(ref.t(end)));
else
    stop_time_value = double(ref.t(end));
end
stop_time = num2str(stop_time_value);

out_dir = fileparts(out_file);
if ~isempty(out_dir) && exist(out_dir, 'dir') ~= 7
    mkdir(out_dir);
end

if contains(model_name, 'Modern_TCN', 'IgnoreCase', true)
    clear ModernTCN_State_Classifier_sim ModernTCN_state_classifier ModernTCN_load_predictor
    if ~isfield(cfg, 'modern_tcn_sim_cfg')
        evalin('base', 'clear modern_tcn_sim_cfg');
    end
elseif contains(model_name, 'GRU', 'IgnoreCase', true)
    clear GRU_State_Classifier_gru_sim GRU_state_classifier GRU_load_default_to_base
elseif contains(model_name, 'TCN', 'IgnoreCase', true)
    clear TCN_State_Classifier_sim TCN_state_classifier TCN_load_predictor
end

assignin('base', 'ref', ref);
if isfield(cfg, 'modern_tcn_sim_cfg')
    assignin('base', 'modern_tcn_sim_cfg', cfg.modern_tcn_sim_cfg);
end
if isfield(cfg, 'params_override') && ~isempty(cfg.params_override)
    assignin('base', 'params', cfg.params_override);
    assignin('base', 'parameters', cfg.params_override);
end
if isfield(cfg, 'ff_rt_override') && ~isempty(cfg.ff_rt_override)
    assignin('base', 'ff_rt', cfg.ff_rt_override);
end

model_file = fullfile(root, 'simulink', [model_name '.slx']);
if exist(model_file, 'file') ~= 2 && exist(model_file, 'file') ~= 4
    error('run_closed_loop_model_once:MissingModel', ...
        'Model file not found: %s', model_file);
end

load_system(model_file);
cleanup = onCleanup(@() local_close_model(model_name));

simIn = Simulink.SimulationInput(model_name);
simIn = simIn.setModelParameter('StopTime', stop_time);
simIn = local_set_variable_dual(simIn, model_name, 'ref', ref);
if isfield(cfg, 'modern_tcn_sim_cfg')
    simIn = local_set_variable_dual(simIn, model_name, ...
        'modern_tcn_sim_cfg', cfg.modern_tcn_sim_cfg);
end
if isfield(cfg, 'params_override') && ~isempty(cfg.params_override)
    simIn = local_set_variable_dual(simIn, model_name, ...
        'params', cfg.params_override);
    simIn = local_set_variable_dual(simIn, model_name, ...
        'parameters', cfg.params_override);
end
if isfield(cfg, 'ff_rt_override') && ~isempty(cfg.ff_rt_override)
    simIn = local_set_variable_dual(simIn, model_name, ...
        'ff_rt', cfg.ff_rt_override);
end
if isfield(cfg, 'robustness_case') && ~isempty(cfg.robustness_case)
    simIn = local_set_variable_dual(simIn, model_name, ...
        'robustness_case', cfg.robustness_case);
end

fprintf('[closed-loop] sim %s, path=%s, StopTime=%s\n', ...
    model_name, path_file, stop_time);
simOut = sim(simIn);

logsout = local_materialize_dataset(simOut.logsout);
SimulationMetadata = simOut.SimulationMetadata; %#ok<NASGU>
save(out_file, 'logsout', 'SimulationMetadata', '-v7.3');
fprintf('[closed-loop] saved: %s\n', out_file);
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

error('run_closed_loop_model_once:BadLogsout', ...
    'Unsupported logsout class: %s', class(logs));
end

function simIn = local_set_variable_dual(simIn, model_name, var_name, var_value)
simIn = simIn.setVariable(var_name, var_value);
simIn = simIn.setVariable(var_name, var_value, 'Workspace', model_name);
end

function local_close_model(model_name)
if bdIsLoaded(model_name)
    close_system(model_name, 0);
end
end

function root = local_project_root()
if exist('project_root', 'file') == 2
    root = project_root();
else
    this_file = mfilename('fullpath');
    root = fileparts(fileparts(fileparts(this_file)));
end
end
