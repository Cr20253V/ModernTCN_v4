function result = run_stage1_plantfix_dataset(cfg)
%RUN_STAGE1_PLANTFIX_DATASET Build the plantfix raw/dataset chain.
%
% Modes:
%   preflight      - planned files and contract checks only
%   smoke          - one path x one run raw + dataset
%   raw_full       - regenerate all 102 raw runs
%   dataset_full   - prepare dataset from an existing full raw file
%   full           - raw_full + dataset_full
%
% The path manifest is reused. No old v2/v3 artifact is overwritten.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
workflow_dir = fullfile(root, 'results', 'paper', 'agv_model_parameter_correction_workflow');
node_dir = fullfile(workflow_dir, '07_dataset');
local_mkdir(node_dir);

cfg = local_defaults(cfg, root, node_dir);
paths = local_paths(cfg, root, node_dir);
plant = agv_plant_revision(parameters());

result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.mode = cfg.mode;
result.tag = cfg.tag;
result.path_tag = cfg.path_tag;
result.plant_revision = plant;
result.paths = paths;
result.cfg = cfg;

result.preflight = local_preflight(paths, plant);
local_write_json(fullfile(node_dir, 'stage1_dataset_preflight.json'), result.preflight);
local_write_revision_report(node_dir, plant, paths, cfg);
if ~result.preflight.pass
    result.status = 'preflight_failed';
    local_write_report(node_dir, result);
    save(fullfile(node_dir, 'stage1_dataset_result.mat'), 'result', '-v7.3');
    error('stage1_dataset:PreflightFailed', 'Dataset preflight failed. See stage1_dataset_preflight.json.');
end

switch lower(char(cfg.mode))
    case 'preflight'
        result.status = 'preflight_ok';
    case 'smoke'
        result.raw = local_generate_raw(cfg, paths, plant, true);
        result.dataset = local_prepare_dataset(cfg, paths, true);
        result.status = 'smoke_done';
    case 'raw_full'
        result.raw = local_generate_raw(cfg, paths, plant, false);
        result.status = 'raw_full_done';
    case 'dataset_full'
        result.dataset = local_prepare_dataset(cfg, paths, false);
        result.status = 'dataset_full_done';
    case 'full'
        result.raw = local_generate_raw(cfg, paths, plant, false);
        result.dataset = local_prepare_dataset(cfg, paths, false);
        result.status = 'full_done';
    otherwise
        error('stage1_dataset:BadMode', 'Unknown mode: %s', cfg.mode);
end

local_write_report(node_dir, result);
save(fullfile(node_dir, 'stage1_dataset_result.mat'), 'result', '-v7.3');
fprintf('[stage1 dataset] status=%s\n', result.status);
fprintf('[stage1 dataset] report=%s\n', fullfile(node_dir, 'stage1_dataset_report.md'));
end

function cfg = local_defaults(cfg, root, node_dir)
if ~isfield(cfg, 'mode') || isempty(cfg.mode); cfg.mode = 'preflight'; end
if ~isfield(cfg, 'tag') || isempty(cfg.tag)
    cfg.tag = 'agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5';
end
if ~isfield(cfg, 'smoke_tag') || isempty(cfg.smoke_tag)
    cfg.smoke_tag = [cfg.tag '_smoke'];
end
if ~isfield(cfg, 'path_tag') || isempty(cfg.path_tag)
    cfg.path_tag = 'agv_theta10_uniform_v2';
end
if ~isfield(cfg, 'seed') || isempty(cfg.seed); cfg.seed = 20260615; end
if ~isfield(cfg, 'num_runs_per_path') || isempty(cfg.num_runs_per_path); cfg.num_runs_per_path = 2; end
if ~isfield(cfg, 'smoke_max_paths') || isempty(cfg.smoke_max_paths); cfg.smoke_max_paths = 4; end
if ~isfield(cfg, 'noise_on') || isempty(cfg.noise_on); cfg.noise_on = true; end
if ~isfield(cfg, 'verbose') || isempty(cfg.verbose); cfg.verbose = true; end
if ~isfield(cfg, 'fail_on_coverage_violation') || isempty(cfg.fail_on_coverage_violation)
    cfg.fail_on_coverage_violation = false;
end
if ~isfield(cfg, 'update_current_pointer') || isempty(cfg.update_current_pointer)
    cfg.update_current_pointer = false;
end
if ~isfield(cfg, 'node_dir') || isempty(cfg.node_dir); cfg.node_dir = node_dir; end
if ~isfield(cfg, 'data_tcn_dir') || isempty(cfg.data_tcn_dir)
    cfg.data_tcn_dir = fullfile(root, 'data', 'tcn');
end
end

function paths = local_paths(cfg, root, node_dir)
paths = struct();
paths.node_dir = node_dir;
paths.path_manifest = fullfile(root, 'data', 'paths', cfg.path_tag, [cfg.path_tag '_manifest.csv']);
paths.train_data_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_train_data_' cfg.tag '.mat']);
paths.dataset_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_dataset_' cfg.tag '.mat']);
paths.scaler_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_scaler_' cfg.tag '.mat']);
paths.split_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_shared_run_split_' cfg.tag '.mat']);
paths.prepare_report_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_prepare_dataset_' cfg.tag '_report.md']);
paths.contract_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_dataset_' cfg.tag '_contract.json']);
paths.coverage_report_file = fullfile(root, 'results', 'modern_tcn', ['ModernTCN_dataset_' cfg.tag '_coverage.md']);
paths.smoke_train_data_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_train_data_' cfg.smoke_tag '.mat']);
paths.smoke_dataset_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_dataset_' cfg.smoke_tag '.mat']);
paths.smoke_scaler_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_scaler_' cfg.smoke_tag '.mat']);
paths.smoke_split_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_shared_run_split_' cfg.smoke_tag '.mat']);
paths.smoke_prepare_report_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_prepare_dataset_' cfg.smoke_tag '_report.md']);
paths.smoke_contract_file = fullfile(cfg.data_tcn_dir, ['ModernTCN_dataset_' cfg.smoke_tag '_contract.json']);
paths.current_pointer = fullfile(cfg.data_tcn_dir, 'CURRENT_ModernTCN_DATASET.json');
end

function preflight = local_preflight(paths, plant)
checks = struct();
checks.path_manifest_exists = exist(paths.path_manifest, 'file') == 2;
checks.revision_id = strcmp(plant.id, 'agv_physics_v2_plantfix');
checks.cornering_stiffness = plant.front_cornering_stiffness == 3000 && plant.rear_cornering_stiffness == 3000;
checks.yaw_damping = plant.yaw_damping == 250;
checks.beta_normal_damping_removed = plant.sideslip_damping == 0;
checks.beta_low_speed_damping_present = plant.sideslip_low_speed_damping == 1;
checks.full_outputs_are_v5 = contains(paths.train_data_file, 'v5_plantfix') && ...
    contains(paths.dataset_file, 'v5_plantfix');
checks.old_v2_v3_not_targeted = ~contains(paths.train_data_file, 'h0_v2') && ...
    ~contains(paths.dataset_file, 'h0_v3');
preflight = struct('checks', checks, 'pass', all(structfun(@(x) isequal(x, true), checks)));
end

function raw_result = local_generate_raw(cfg, paths, plant, is_smoke)
build_cfg = struct();
build_cfg.tag = cfg.tag;
build_cfg.path_tag = cfg.path_tag;
build_cfg.generate_paths = false;
build_cfg.generate_train_data = true;
build_cfg.prepare_dataset = false;
build_cfg.coverage_report = false;
build_cfg.seed = cfg.seed;
build_cfg.num_runs_per_path = cfg.num_runs_per_path;
build_cfg.noise_on = cfg.noise_on;
build_cfg.verbose = cfg.verbose;
build_cfg.use_manifest_paths = true;
build_cfg.fail_on_coverage_violation = cfg.fail_on_coverage_violation;
if is_smoke
    build_cfg.tag = cfg.smoke_tag;
    build_cfg.max_paths = cfg.smoke_max_paths;
    build_cfg.num_runs_per_path = 1;
end
build_cfg.plant_revision = plant;
outputs = build_agv_theta10_uniform_dataset(build_cfg);
raw_result = struct();
raw_result.output_file = outputs.train_data_file;
raw_result.exists = exist(outputs.train_data_file, 'file') == 2;
if raw_result.exists
    if is_smoke
        raw_result.validation = local_validate_raw(outputs.train_data_file, plant, cfg.smoke_max_paths, false);
    else
        raw_result.validation = local_validate_raw(outputs.train_data_file, plant, 102, true);
    end
else
    raw_result.validation = struct('pass', false, 'reason', 'raw file missing');
end
if ~raw_result.validation.pass
    error('stage1_dataset:RawValidationFailed', 'Raw validation failed for %s', outputs.train_data_file);
end
if ~is_smoke && ~strcmp(outputs.train_data_file, paths.train_data_file)
    error('stage1_dataset:RawPathMismatch', 'Unexpected full raw file path.');
end
end

function ds_result = local_prepare_dataset(cfg, paths, is_smoke)
build_cfg = struct();
build_cfg.tag = cfg.tag;
build_cfg.path_tag = cfg.path_tag;
build_cfg.generate_paths = false;
build_cfg.generate_train_data = false;
build_cfg.prepare_dataset = true;
build_cfg.coverage_report = ~is_smoke;
build_cfg.seed = cfg.seed;
build_cfg.verbose = cfg.verbose;
build_cfg.fail_on_coverage_violation = cfg.fail_on_coverage_violation;
if is_smoke
    build_cfg.tag = cfg.smoke_tag;
    build_cfg.coverage_report = false;
    build_cfg.train_ratio = 0.50;
    build_cfg.val_ratio = 0.25;
    build_cfg.test_ratio = 0.25;
    build_cfg.split_search_trials = 200;
end
outputs = build_agv_theta10_uniform_dataset(build_cfg);
ds_result = local_validate_dataset(outputs.dataset_file, outputs.contract_file, is_smoke);
if ~ds_result.pass
    error('stage1_dataset:DatasetValidationFailed', 'Dataset validation failed for %s', outputs.dataset_file);
end
if ~is_smoke && cfg.update_current_pointer
    local_update_current_pointer(paths, outputs);
end
end

function validation = local_validate_raw(raw_file, plant, expected_run_count, require_count)
validation = struct('file', raw_file, 'pass', false);
S = load(raw_file, 'data');
if ~isfield(S, 'data') || ~isfield(S.data, 'runs')
    validation.reason = 'missing data.runs';
    return;
end
data = S.data;
validation.run_count = numel(data.runs);
validation.expected_run_count = expected_run_count;
validation.has_plant_revision = isfield(data, 'meta') && isfield(data.meta, 'plant_revision');
validation.plant_revision = '';
if validation.has_plant_revision && isfield(data.meta.plant_revision, 'id')
    validation.plant_revision = data.meta.plant_revision.id;
end
bad = false;
for i = 1:numel(data.runs)
    r = data.runs(i);
    if any(~isfinite(r.t(:))) || any(~isfinite(r.u(:))) || ...
            any(~isfinite(r.y_raw(:))) || any(~isfinite(r.theta(:)))
        bad = true;
        break;
    end
end
validation.no_nan_inf = ~bad;
validation.pass = validation.run_count > 0 && validation.no_nan_inf && ...
    validation.has_plant_revision && strcmp(validation.plant_revision, plant.id);
if require_count
    validation.pass = validation.pass && validation.run_count == expected_run_count;
end
if validation.run_count ~= validation.expected_run_count
    validation.note = 'smoke runs or partial full raw; full phase expects 102 runs';
end
end

function validation = local_validate_dataset(dataset_file, contract_file, is_smoke)
validation = struct('dataset_file', dataset_file, 'contract_file', contract_file, 'pass', false);
if exist(dataset_file, 'file') ~= 2 || exist(contract_file, 'file') ~= 2
    validation.reason = 'missing dataset or contract';
    return;
end
S = load(dataset_file, 'dataset');
dataset = S.dataset;
validation.input_dim = size(dataset.X_train, 3);
validation.train_windows = size(dataset.X_train, 1);
validation.val_windows = size(dataset.X_val, 1);
validation.test_windows = size(dataset.X_test, 1);
validation.no_nan_inf = all(isfinite(dataset.X_train(:))) && ...
    all(isfinite(dataset.X_val(:))) && all(isfinite(dataset.X_test(:)));
validation.has_plant_revision = isfield(dataset.meta, 'plant_revision') && ...
    isfield(dataset.meta.plant_revision, 'id');
contract = local_read_json(contract_file);
validation.contract_feature = local_json_field(contract, 'feature_contract', '');
validation.contract_input_dim = local_json_field(contract, 'input_dim', NaN);
validation.contract_has_plant_revision = isfield(contract, 'plant_revision');
validation.pass = validation.input_dim == 22 && validation.no_nan_inf && ...
    strcmp(char(validation.contract_feature), 'passive17_plus_all5') && ...
    double(validation.contract_input_dim) == 22 && validation.has_plant_revision;
if ~is_smoke
    validation.pass = validation.pass && validation.train_windows > 0 && ...
        validation.val_windows > 0 && validation.test_windows > 0;
end
end

function local_update_current_pointer(paths, outputs)
payload = struct();
payload.name = 'ModernTCN current training dataset';
payload.status = 'stage1_plantfix_current';
payload.updated_at = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
payload.feature_contract = 'passive17_plus_all5';
payload.plant_revision = 'agv_physics_v2_plantfix';
payload.canonical_files = struct( ...
    'train_data', outputs.train_data_file, ...
    'dataset', outputs.dataset_file, ...
    'scaler', outputs.scaler_file, ...
    'split', outputs.split_file, ...
    'contract', outputs.contract_file);
payload.note = ['Updated only after v5 plantfix raw/dataset validation. ' ...
    'Old v2/v3 files remain historical baselines.'];
local_write_json(paths.current_pointer, payload);
end

function local_write_revision_report(node_dir, plant, paths, cfg)
file = fullfile(node_dir, 'plant_revision_agv_physics_v2_plantfix.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Plant Revision Freeze\n\n');
fprintf(fid, '- revision: `%s`\n', plant.id);
fprintf(fid, '- params version: `%s`\n', char(string(plant.params_version)));
fprintf(fid, '- front_cornering_stiffness: `%.10g`\n', plant.front_cornering_stiffness);
fprintf(fid, '- rear_cornering_stiffness: `%.10g`\n', plant.rear_cornering_stiffness);
fprintf(fid, '- yaw_damping: `%.10g`\n', plant.yaw_damping);
fprintf(fid, '- sideslip_damping: `%.10g`\n', plant.sideslip_damping);
fprintf(fid, '- sideslip_low_speed_damping: `%.10g`\n\n', plant.sideslip_low_speed_damping);
fprintf(fid, '## Data Targets\n\n');
fprintf(fid, '- tag: `%s`\n', cfg.tag);
fprintf(fid, '- path manifest: `%s`\n', paths.path_manifest);
fprintf(fid, '- raw: `%s`\n', paths.train_data_file);
fprintf(fid, '- dataset: `%s`\n', paths.dataset_file);
fprintf(fid, '- contract: `%s`\n\n', paths.contract_file);
fprintf(fid, 'Old `v2/v3` raw, split, scaler, and model files are reference-only for this phase.\n');
end

function local_write_report(node_dir, result)
file = fullfile(node_dir, 'stage1_dataset_report.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 Plantfix Dataset Report\n\n');
fprintf(fid, '- status: `%s`\n', local_field(result, 'status', 'unknown'));
fprintf(fid, '- mode: `%s`\n', result.mode);
fprintf(fid, '- tag: `%s`\n', result.tag);
fprintf(fid, '- plant_revision: `%s`\n\n', result.plant_revision.id);
fprintf(fid, '## Preflight\n\n');
names = fieldnames(result.preflight.checks);
fprintf(fid, '| check | pass |\n|---|---:|\n');
for i = 1:numel(names)
    fprintf(fid, '| `%s` | %d |\n', names{i}, double(result.preflight.checks.(names{i})));
end
fprintf(fid, '\n## Artifacts\n\n');
fprintf(fid, '- raw: `%s`\n', result.paths.train_data_file);
fprintf(fid, '- dataset: `%s`\n', result.paths.dataset_file);
fprintf(fid, '- scaler: `%s`\n', result.paths.scaler_file);
fprintf(fid, '- split: `%s`\n', result.paths.split_file);
fprintf(fid, '- contract: `%s`\n', result.paths.contract_file);
fprintf(fid, '- smoke raw: `%s`\n', result.paths.smoke_train_data_file);
fprintf(fid, '- smoke dataset: `%s`\n', result.paths.smoke_dataset_file);
end

function v = local_field(s, name, default_value)
if isstruct(s) && isfield(s, name)
    v = s.(name);
else
    v = default_value;
end
end

function value = local_json_field(s, name, default_value)
if isstruct(s) && isfield(s, name)
    value = s.(name);
else
    value = default_value;
end
end

function local_write_json(file, payload)
folder = fileparts(file);
if ~isempty(folder) && exist(folder, 'dir') ~= 7
    mkdir(folder);
end
fid = fopen(file, 'w');
if fid < 0
    warning('Cannot write JSON: %s', file);
    return;
end
cleanup = onCleanup(@() fclose(fid));
try
    txt = jsonencode(payload, 'PrettyPrint', true);
catch
    txt = jsonencode(payload);
end
fprintf(fid, '%s\n', txt);
end

function s = local_read_json(file)
txt = fileread(file);
s = jsondecode(txt);
end

function local_mkdir(path_in)
if exist(path_in, 'dir') ~= 7
    mkdir(path_in);
end
end
