function summary = run_stage1_gru_tcn_train(cfg)
%RUN_STAGE1_GRU_TCN_TRAIN Train GRU and TCN on the v5 plantfix dataset.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
if ~isfield(cfg, 'node_dir') || isempty(cfg.node_dir)
    cfg.node_dir = fullfile(root, 'results', 'paper', ...
        'agv_model_parameter_correction_workflow', '08_models');
end
if ~isfield(cfg, 'dataset_file') || isempty(cfg.dataset_file)
    cfg.dataset_file = fullfile(root, 'data', 'tcn', ...
        'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');
end
if ~isfield(cfg, 'mode') || isempty(cfg.mode); cfg.mode = 'smoke'; end
if ~isfield(cfg, 'models') || isempty(cfg.models); cfg.models = {'GRU','TCN'}; end
if ~isfield(cfg, 'use_gpu') || isempty(cfg.use_gpu); cfg.use_gpu = true; end
if ~isfield(cfg, 'verbose') || isempty(cfg.verbose); cfg.verbose = true; end
if ~isfield(cfg, 'skip_existing') || isempty(cfg.skip_existing); cfg.skip_existing = true; end
if ~isfield(cfg, 'max_epochs') || isempty(cfg.max_epochs); cfg.max_epochs = 140; end

if strcmpi(cfg.mode, 'smoke')
    cfg.seeds_gru = 101;
    cfg.seeds_tcn = 21;
elseif strcmpi(cfg.mode, 'full')
    cfg.seeds_gru = [21 73 101];
    cfg.seeds_tcn = [21 73 101];
else
    error('stage1_train:BadMode', 'Unknown mode: %s', cfg.mode);
end

local_check_dataset_contract(cfg.dataset_file);
local_mkdir(cfg.node_dir);
local_mkdir(fullfile(cfg.node_dir, 'matlab_logs'));
local_mkdir(fullfile(cfg.node_dir, 'models'));

rows = repmat(local_empty_row(), 0, 1);
models = cellstr(cfg.models);
for im = 1:numel(models)
    model_name = upper(string(models{im}));
    switch model_name
        case "GRU"
            for seed = cfg.seeds_gru
                rows(end+1) = local_train_gru(root, cfg, seed); %#ok<AGROW>
            end
        case "TCN"
            for seed = cfg.seeds_tcn
                rows(end+1) = local_train_tcn(root, cfg, seed); %#ok<AGROW>
            end
        otherwise
            error('stage1_train:BadModel', 'Unknown model: %s', model_name);
    end
end

T = struct2table(rows);
summary = struct();
summary.mode = cfg.mode;
summary.dataset_file = cfg.dataset_file;
summary.rows = T;
summary.summary_file = fullfile(cfg.node_dir, sprintf('stage1_%s_gru_tcn_summary.csv', lower(cfg.mode)));
summary.mat_file = fullfile(cfg.node_dir, sprintf('stage1_%s_gru_tcn_summary.mat', lower(cfg.mode)));
writetable(T, summary.summary_file);
save(summary.mat_file, 'summary');
fprintf('[stage1 GRU/TCN] mode=%s done: %s\n', cfg.mode, summary.summary_file);
end

function row = local_train_gru(root, cfg, seed)
run_name = sprintf('%s_gru_v5_plantfix_passive17_plus_all5_seed%d', lower(cfg.mode), seed);
log_dir = fullfile(cfg.node_dir, 'matlab_logs', run_name);
local_mkdir(log_dir);

train_cfg = GRU_recommended_cfg('inputstats_hidden96');
train_cfg.case_name = 'inputstats_hidden96_l2';
train_cfg.num_layers = 2;
train_cfg.dropout = 0.20;
train_cfg.input_file = cfg.dataset_file;
train_cfg.seed = seed;
train_cfg.max_epochs = cfg.max_epochs;
train_cfg.batch_size = 128;
train_cfg.use_gpu = cfg.use_gpu;
train_cfg.verbose = cfg.verbose;
train_cfg.initial_lr = 1e-3;
train_cfg.grad_clip_mode = 'global';
train_cfg.grad_clip = 5.0;
train_cfg.class_weight_method = 'sqrt_inverse';
train_cfg.turn_class_weight_method = 'sqrt_inverse';
train_cfg.turn_class_multipliers = [1.08 1.00 1.08];
train_cfg.lambda_turn = 0.08;
train_cfg.lambda_theta = 0.55;
train_cfg.lambda_theta_flat = 0.12;
train_cfg.theta_flat_loss_mode = 'near_zero';
train_cfg.theta_flat_zero_tol_deg = 0.3;
train_cfg.best_metric = 'composite';
train_cfg.select_main_error_weight = 0.45;
train_cfg.select_turn_error_weight = 0.30;
train_cfg.select_theta_weight = 0.30;
train_cfg.select_theta_ref_deg = 2.0;
train_cfg.select_turn_transition_weight = 1.20;
train_cfg.select_turn_transition_target = 0.75;
train_cfg.select_turn_lr_weight = 0.20;
train_cfg.select_turn_lr_target = 0.85;
train_cfg.early_stop_min_epochs = min(45, max(1, cfg.max_epochs));
train_cfg.selection_start_epoch = min(10, max(1, cfg.max_epochs));
train_cfg.patience = 25;
train_cfg.print_every = 5;
train_cfg.log_dir = log_dir;
train_cfg.model_file = fullfile(cfg.node_dir, 'models', sprintf('GRU_model_%s.mat', run_name));
train_cfg.meta_file = fullfile(cfg.node_dir, 'models', sprintf('GRU_meta_%s.mat', run_name));
train_cfg.report_file = fullfile(log_dir, 'GRU_train_report.md');

row = local_run_train('GRU', 'inputstats_hidden96_l2', train_cfg, cfg.skip_existing);
row.hidden_size = local_get_numeric(train_cfg, 'hidden_size', NaN);
row.num_layers = train_cfg.num_layers;
row.num_blocks = NaN;
row.num_filters = NaN;
row.kernel_size = NaN;
row.root = string(root);
end

function row = local_train_tcn(root, cfg, seed)
run_name = sprintf('%s_tcn_v5_plantfix_passive17_plus_all5_seed%d', lower(cfg.mode), seed);
log_dir = fullfile(cfg.node_dir, 'matlab_logs', run_name);
local_mkdir(log_dir);

train_cfg = TCN_recommended_cfg('production_current');
train_cfg.case_name = 'tcn96_rawtheta_sym';
train_cfg.input_file = cfg.dataset_file;
train_cfg.seed = seed;
train_cfg.max_epochs = cfg.max_epochs;
train_cfg.batch_size = 128;
train_cfg.use_gpu = cfg.use_gpu;
train_cfg.verbose = cfg.verbose;
if ~isfield(train_cfg, 'num_blocks'); train_cfg.num_blocks = 6; end
if ~isfield(train_cfg, 'num_filters'); train_cfg.num_filters = 96; end
if ~isfield(train_cfg, 'kernel_size'); train_cfg.kernel_size = 3; end
if ~isfield(train_cfg, 'dropout'); train_cfg.dropout = 0.15; end
train_cfg.initial_lr = 1e-3;
train_cfg.grad_clip_mode = 'global';
train_cfg.grad_clip = 5.0;
train_cfg.class_weight_method = 'sqrt_inverse';
train_cfg.turn_class_weight_method = 'sqrt_inverse';
train_cfg.main_class_multipliers = [1.00 1.00 1.00];
train_cfg.turn_class_multipliers = [1.08 1.00 1.08];
train_cfg.lambda_turn = 0.08;
train_cfg.lambda_theta = 0.55;
train_cfg.lambda_theta_flat = 0.12;
train_cfg.theta_flat_loss_mode = 'near_zero';
train_cfg.theta_flat_zero_tol_deg = 0.3;
train_cfg.theta_near_flat_deg = 0.5;
train_cfg.lambda_aux = 0.00;
train_cfg.lambda_phy = 0.00;
train_cfg.lambda_smooth = 0.00;
train_cfg.select_theta_weight = 0.30;
train_cfg.select_theta_ref_deg = 2.0;
train_cfg.turn_transition_weight = 1.25;
train_cfg.base_selection_start_epoch = min(10, max(1, cfg.max_epochs));
train_cfg.selection_start_epoch = min(64, max(1, cfg.max_epochs));
train_cfg.early_stop_min_epochs = min(75, max(1, cfg.max_epochs));
train_cfg.patience = 25;
train_cfg.print_every = 5;
train_cfg.log_dir = log_dir;
train_cfg.model_file = fullfile(cfg.node_dir, 'models', sprintf('TCN_model_%s.mat', run_name));
train_cfg.meta_file = fullfile(cfg.node_dir, 'models', sprintf('TCN_meta_%s.mat', run_name));
train_cfg.report_file = fullfile(log_dir, 'TCN_train_report.md');

row = local_run_train('TCN', 'tcn96_rawtheta_sym', train_cfg, cfg.skip_existing);
row.hidden_size = NaN;
row.num_layers = NaN;
row.num_blocks = train_cfg.num_blocks;
row.num_filters = train_cfg.num_filters;
row.kernel_size = train_cfg.kernel_size;
row.root = string(root);
end

function row = local_run_train(model_name, case_name, train_cfg, skip_existing)
row = local_empty_row();
row.model = string(model_name);
row.case_name = string(case_name);
row.seed = train_cfg.seed;
row.dataset_file = string(train_cfg.input_file);
row.model_file = string(train_cfg.model_file);
row.meta_file = string(train_cfg.meta_file);
row.report_file = string(train_cfg.report_file);
row.status = "failed";
try
    if skip_existing && exist(train_cfg.meta_file, 'file') == 2
        S = load(train_cfg.meta_file, 'meta');
        if isfield(S, 'meta') && isfield(S.meta, 'cfg') && ...
                isfield(S.meta.cfg, 'input_file') && ...
                strcmp(char(S.meta.cfg.input_file), char(train_cfg.input_file)) && ...
                isfield(S.meta.cfg, 'seed') && isequal(S.meta.cfg.seed, train_cfg.seed)
            row = local_row_from_meta(row, S.meta, "reused");
            return;
        end
    end
    if strcmpi(model_name, 'GRU')
        [~, meta] = GRU_train(train_cfg);
    else
        [~, meta] = TCN_train(train_cfg);
    end
    row = local_row_from_meta(row, meta, "trained");
catch ME
    row.status = "failed";
    row.error_message = string(ME.message);
    warning('stage1_train:TrainFailed', '%s seed=%d failed: %s', model_name, train_cfg.seed, ME.message);
end
end

function row = local_row_from_meta(row, meta, status)
row.status = string(status);
row.best_epoch = local_get_numeric(meta, 'best_epoch', NaN);
row.base_best_epoch = local_get_numeric(meta, 'base_best_epoch', NaN);
row.train_seconds = local_get_numeric(meta, 'train_seconds', NaN);
row.input_dim = 22;
row.train_windows = NaN;
row.loss_total = local_metric(meta.test_metrics, 'total');
row.acc_main = local_metric(meta.test_metrics, 'acc_main');
row.acc_turn = local_metric(meta.test_metrics, 'acc_turn');
row.acc_turn_transition = local_metric(meta.test_metrics, 'acc_turn_transition');
row.theta_mae_deg = rad2deg(local_metric(meta.test_metrics, 'mae_theta'));
row.theta_abs_le_10_p95_abs_err_deg = local_metric(meta.test_metrics, 'theta_abs_le_10_p95_abs_err_deg');
row.theta_flat_bias_deg = local_metric(meta.test_metrics, 'theta_flat_bias_deg');
row.flat_recall = local_vector_metric(meta.test_metrics, 'recall_main', 1);
row.stall_recall = local_vector_metric(meta.test_metrics, 'recall_main', 2);
row.slope_recall = local_vector_metric(meta.test_metrics, 'recall_main', 3);
row.error_message = "";
end

function local_check_dataset_contract(dataset_file)
if exist(dataset_file, 'file') ~= 2
    error('stage1_train:MissingDataset', 'Dataset not found: %s', dataset_file);
end
S = load(dataset_file, 'dataset');
dataset = S.dataset;
if size(dataset.X_train, 3) ~= 22
    error('stage1_train:BadInputDim', 'Expected input_dim=22.');
end
if any(~isfinite(dataset.X_train(:))) || any(~isfinite(dataset.X_val(:))) || any(~isfinite(dataset.X_test(:)))
    error('stage1_train:BadDatasetValues', 'Dataset contains NaN or Inf values.');
end
if ~isfield(dataset, 'meta') || ~isfield(dataset.meta, 'plant_revision') || ...
        ~strcmp(dataset.meta.plant_revision.id, 'agv_physics_v2_plantfix')
    error('stage1_train:BadPlantRevision', 'Dataset plant revision is missing or wrong.');
end
end

function row = local_empty_row()
row = struct( ...
    'model', "", 'case_name', "", 'seed', NaN, 'status', "", ...
    'input_dim', NaN, 'best_epoch', NaN, 'base_best_epoch', NaN, ...
    'train_seconds', NaN, 'loss_total', NaN, 'acc_main', NaN, ...
    'acc_turn', NaN, 'acc_turn_transition', NaN, 'theta_mae_deg', NaN, ...
    'theta_abs_le_10_p95_abs_err_deg', NaN, 'theta_flat_bias_deg', NaN, ...
    'flat_recall', NaN, 'stall_recall', NaN, 'slope_recall', NaN, ...
    'hidden_size', NaN, 'num_layers', NaN, 'num_blocks', NaN, ...
    'num_filters', NaN, 'kernel_size', NaN, 'train_windows', NaN, ...
    'dataset_file', "", 'model_file', "", 'meta_file', "", ...
    'report_file', "", 'error_message', "", 'root', "");
end

function value = local_metric(s, name)
if isstruct(s) && isfield(s, name)
    value = gather(s.(name));
else
    value = NaN;
end
end

function value = local_vector_metric(s, name, idx)
if isstruct(s) && isfield(s, name) && numel(s.(name)) >= idx
    value = gather(s.(name)(idx));
else
    value = NaN;
end
end

function value = local_get_numeric(s, name, default_value)
if isstruct(s) && isfield(s, name)
    value = s.(name);
else
    value = default_value;
end
end

function local_mkdir(path_in)
if exist(path_in, 'dir') ~= 7
    mkdir(path_in);
end
end
