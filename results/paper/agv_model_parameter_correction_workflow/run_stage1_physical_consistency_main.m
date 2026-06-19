function result = run_stage1_physical_consistency_main(cfg)
%RUN_STAGE1_PHYSICAL_CONSISTENCY_MAIN Orchestrate Stage 1 plantfix workflow.
%
% Modes:
%   preflight
%   open_loop
%   dataset_smoke
%   dataset_full
%   lpv_preflight
%   lpv_rebuild
%   mpc_candidate
%   train_preflight
%   train_smoke
%   train_full
%   closed_loop_preflight
%   closed_loop_smoke
%   closed_loop_full

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end
root = project_root();
workflow_dir = fullfile(root, 'results', 'paper', 'agv_model_parameter_correction_workflow');
if ~isfield(cfg, 'mode') || isempty(cfg.mode); cfg.mode = 'preflight'; end
mode = lower(char(cfg.mode));

addpath(fullfile(workflow_dir, '03_open_loop'));
addpath(fullfile(workflow_dir, '04_lpv_database'));
addpath(fullfile(workflow_dir, '06_mpc_retuning'));
addpath(fullfile(workflow_dir, '07_dataset'));
addpath(fullfile(workflow_dir, '09_closed_loop'));

result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.mode = mode;
result.workflow_dir = workflow_dir;

switch mode
    case 'preflight'
        result.plant_revision = agv_plant_revision(parameters());
        result.dataset = run_stage1_plantfix_dataset(struct('mode', 'preflight'));
        result.lpv = run_stage1_lpv_rebuild(struct('mode', 'preflight'));
        result.status = 'preflight_ok';
    case 'open_loop'
        result.open_loop = run_stage1_open_loop_smoke();
        result.status = 'open_loop_done';
    case 'dataset_smoke'
        result.dataset = run_stage1_plantfix_dataset(struct('mode', 'smoke'));
        result.status = 'dataset_smoke_done';
    case 'dataset_full'
        result.dataset = run_stage1_plantfix_dataset(struct('mode', 'full', ...
            'update_current_pointer', true));
        result.status = 'dataset_full_done';
    case 'lpv_preflight'
        result.lpv = run_stage1_lpv_rebuild(struct('mode', 'preflight'));
        result.status = 'lpv_preflight_ok';
    case 'lpv_rebuild'
        write_canonical = local_field(cfg, 'write_canonical', false);
        result.lpv = run_stage1_lpv_rebuild(struct('mode', 'rebuild', ...
            'write_canonical', write_canonical));
        result.status = 'lpv_rebuild_done';
    case 'mpc_candidate'
        result.mpc = run_stage1_mpc_candidate(cfg);
        result.status = 'mpc_candidate_done';
    case 'train_preflight'
        result.status = local_run_python_train('preflight');
    case 'train_smoke'
        result.status = local_run_python_train('smoke');
    case 'train_full'
        result.status = local_run_python_train('all');
    case 'closed_loop_preflight'
        result.closed_loop = run_stage1_closed_loop_validation(struct('mode', 'preflight'));
        result.status = 'closed_loop_preflight_ok';
    case 'closed_loop_smoke'
        result.closed_loop = run_stage1_closed_loop_validation(struct('mode', 'smoke'));
        result.status = 'closed_loop_smoke_done';
    case 'closed_loop_full'
        result.closed_loop = run_stage1_closed_loop_validation(struct('mode', 'full'));
        result.status = 'closed_loop_full_done';
    otherwise
        error('stage1_main:BadMode', 'Unknown mode: %s', mode);
end

save(fullfile(workflow_dir, 'stage1_physical_consistency_main_result.mat'), 'result', '-v7.3');
local_write_status(workflow_dir, result);
fprintf('[stage1 main] status=%s\n', result.status);
end

function value = local_field(s, name, default_value)
if isstruct(s) && isfield(s, name)
    value = s.(name);
else
    value = default_value;
end
end

function status = local_run_python_train(mode)
root = project_root();
script = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', ...
    'run_stage1_plantfix_train.py');
cmd = sprintf('"%s" "%s" --mode %s', string(pyenv().Executable), script, mode);
[code, out] = system(cmd);
if code ~= 0
    error('stage1_main:PythonTrainFailed', 'Python train runner failed:\n%s', out);
end
disp(out);
status = ['train_' mode '_done'];
end

function local_write_status(workflow_dir, result)
file = fullfile(workflow_dir, 'stage1_physical_consistency_status.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 Physical Consistency Status\n\n');
fprintf(fid, '- timestamp: `%s`\n', result.timestamp);
fprintf(fid, '- mode: `%s`\n', result.mode);
fprintf(fid, '- status: `%s`\n\n', result.status);
fprintf(fid, 'Use `run_stage1_physical_consistency_main(struct(''mode'',''<mode>''))` to continue the staged workflow.\n');
end
