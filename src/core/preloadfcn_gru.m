function preloadfcn_gru(mode)
% PreLoadFcn - standalone learned-model preload.
% Design goal:
%   - Do not call preloadfcn_v2/preloadfcn_v1.
%   - Keep the same 0-5 initialization flow as v2.
%   - Only differ at Step 4 by selecting the frozen GRU or ModernTCN model.

if nargin < 1 || isempty(mode)
    mode = 'gru';
end
mode = lower(char(mode));
if ~ismember(mode, {'gru', 'modern_tcn'})
    error('preloadfcn_gru:BadMode', 'Unknown preload mode: %s', mode);
end

if strcmp(mode, 'modern_tcn')
    title_text = 'LPVMPC_AGV preload (ModernTCN standalone)';
else
    title_text = 'LPVMPC_AGV preload (GRU standalone)';
end

fprintf('\n');
fprintf('============================================================\n');
fprintf('%s\n', title_text);
fprintf('============================================================\n\n');

%% Bootstrap path + directory config
init_project();
root = project_root();
data_dir = fullfile(root, 'data');
data_models_dir = fullfile(data_dir, 'models');
data_paths_dir = fullfile(data_dir, 'paths');
data_gru_dir = fullfile(data_dir, 'gru');
results_root = results_dir('');
results_paths = struct( ...
    'root', results_root, ...
    'simulink', results_dir('simulink'), ...
    'closed_loop', results_dir('closed_loop'), ...
    'paths', results_dir('paths'), ...
    'gru_logs', results_dir('gru/sim'));
env_paths = struct('root', root, 'data', data_dir, 'models', data_models_dir, ...
    'paths', data_paths_dir, 'gru', data_gru_dir, 'results', results_paths);

assignin('base', 'results_paths', results_paths);
assignin('base', 'env_paths', env_paths);

mw = get_param(bdroot, 'ModelWorkspace');
assignin(mw, 'results_paths', results_paths);
assignin(mw, 'env_paths', env_paths);
% Do not save ModelWorkspace during PreLoadFcn; this can block load_system in batch mode.

%% Target horizons
TARGET_NP = 150;
TARGET_NC = 50;

%% Step 0: Load basic params
fprintf('[Step 0/5] Load basic parameters...\n');
try
    params = parameters();
    fprintf('  OK parameters() (Ts=%.3fs, m=%.1fkg, L=%.2fm)\n', ...
        params.Ts, params.mass, params.L);
catch ME
    warning('preloadfcn_gru:ParametersFailed', '%s', ME.message);
    params = struct('Ts',0.05,'mass',100,'gravity',9.81, ...
        'rolling_resistance',0.015,'air_density',1.225, ...
        'drag_coefficient_area',0.5,'L',2.0);
end
assignin('base','params',params);
assignin(mw,'params',params);

ff_rt = struct('m',params.mass,'g',params.gravity, ...
    'c_r',params.rolling_resistance,'rho',params.air_density, ...
    'CdA',params.drag_coefficient_area);
v_ff_nom = 1.0;
assignin('base','ff_rt',ff_rt);
assignin('base','v_ff_nom',v_ff_nom);
assignin(mw,'ff_rt',ff_rt);
assignin(mw,'v_ff_nom',v_ff_nom);
fprintf('\n');

%% Step 1: Load LPV database
fprintf('[Step 1/5] Load LPV database...\n');
base_names = {'lin_agv_db.mat', 'plant_grid_test.mat', 'plant_grid.mat'};
base_dirs = {data_models_dir, root, ''};
db_files = {};
for d = 1:numel(base_dirs)
    for n = 1:numel(base_names)
        if isempty(base_dirs{d})
            db_files{end+1} = base_names{n}; %#ok<AGROW>
        else
            db_files{end+1} = fullfile(base_dirs{d}, base_names{n}); %#ok<AGROW>
        end
    end
end
db_files = unique(db_files, 'stable');

S = [];
loaded_db_file = '';
for i = 1:numel(db_files)
    if exist(db_files{i}, 'file')
        try
            S = load(db_files{i});
            loaded_db_file = db_files{i};
            fprintf('  OK file loaded: %s\n', db_files{i});
            break;
        catch ME
            fprintf('  WARN load failed %s: %s\n', db_files{i}, ME.message);
        end
    end
end

if isempty(S)
    error('[PreLoadFcn] LPV database not found.');
end

if isfield(S,'db') && isstruct(S.db)
    db_data = S.db;
    fprintf('  use db struct format\n');
elseif all(isfield(S, {'A','B','C','D','E'}))
    db_data = S;
    fprintf('  use top-level field format\n');
else
    error('[PreLoadFcn] Unrecognized DB format (fields: %s)', strjoin(fieldnames(S), ', '));
end

req = {'A','B','C','D','E','Ts','grid'};
missing = req(~isfield(db_data, req));
if ~isempty(missing)
    error('[PreLoadFcn] DB missing fields: %s', strjoin(missing, ', '));
end

A=db_data.A; B=db_data.B; C=db_data.C; D=db_data.D; E=db_data.E;
Ts=db_data.Ts; grid=db_data.grid;
nx=size(A,4); nu=size(B,5); ny=size(C,4); nd=size(E,5);
Nv=size(A,1); Nw=size(A,2); Nt=size(A,3);

fprintf('  OK grid %d x %d x %d, nx=%d, nu=%d, nd=%d, Ts=%.3fs\n', ...
    Nv, Nw, Nt, nx, nu, nd, Ts);

db_rt = struct('A',A,'B',B,'C',C,'D',D,'E',E, ...
    'grid',grid,'Ts',Ts,'nx',nx,'nu',nu,'ny',ny,'nd',nd, ...
    'Nv',Nv,'Nw',Nw,'Nt',Nt);
assignin('base','db_rt',db_rt);
assignin(mw,'db_rt',db_rt);
fprintf('\n');

%% Step 2: Create MPCPlantBus
fprintf('[Step 2/5] Create MPCPlantBus...\n');
nu_md = nu + nd;
samplePlant = struct('A',zeros(nx,nx),'B',zeros(nx,nu_md), ...
    'C',zeros(ny,nx),'D',zeros(ny,nu_md),'U',zeros(nu_md,1), ...
    'X',zeros(nx,1),'Y',zeros(ny,1),'DX',zeros(nx,1),'Ts',Ts);
info = Simulink.Bus.createObject(samplePlant);
assignin('base','MPCPlantBus', evalin('base', info.busName));
if ~strcmp(info.busName,'MPCPlantBus')
    evalin('base', sprintf('clear %s;', info.busName));
end
assignin('base','plant_ic', samplePlant);
fprintf('  OK MPCPlantBus created (nu_md=%d = %d MV + %d MD)\n\n', nu_md, nu, nd);

%% Step 3: Load BO maps / build ctrl
fprintf('[Step 3/5] Load BO maps / ctrl...\n');
bo_results_dir = fullfile(results_root, 'bo_results');
base_dirs_mb = {bo_results_dir, data_models_dir, root, ''};
maps_names = {'phase2_best.mat', 'phase1_best.mat'};

maps_files = {};
for d = 1:numel(base_dirs_mb)
    for n = 1:numel(maps_names)
        if isempty(base_dirs_mb{d})
            maps_files{end+1} = maps_names{n}; %#ok<AGROW>
        else
            maps_files{end+1} = fullfile(base_dirs_mb{d}, maps_names{n}); %#ok<AGROW>
        end
    end
end
maps_files = unique(maps_files, 'stable');

maps_best = [];
maps_loaded = false;
maps_source_file = '';
for i = 1:numel(maps_files)
    if exist(maps_files{i}, 'file')
        try
            Tm = load(maps_files{i});

            if isfield(Tm, 'best')
                if isfield(Tm.best, 'ctrl_maps')
                    maps_best = Tm.best.ctrl_maps;
                    maps_best.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
                    [~, fname, ~] = fileparts(maps_files{i});
                    maps_best.version = fname;
                elseif isfield(Tm.best, 'Q_range')
                    maps_best = Tm.best;
                end
            elseif isfield(Tm, 'maps_best')
                maps_best = Tm.maps_best;
            end

            if ~isempty(maps_best)
                maps_loaded = true;
                maps_source_file = maps_files{i};
                [~, fname, ~] = fileparts(maps_files{i});
                fprintf('  OK BO maps loaded (%s)\n', fname);
                break;
            end
        catch ME
            fprintf('  WARN map load failed %s: %s\n', maps_files{i}, ME.message);
        end
    end
end
if ~maps_loaded
    fprintf('  WARN no phase2_best/phase1_best found, use defaults\n');
end

ctrl = [];
ctrl_source = 'not created';
ctrl_file_path = fullfile(data_models_dir, 'ctrl.mat');

if exist(ctrl_file_path, 'file')
    try
        Tc = load(ctrl_file_path);
        if isfield(Tc, 'ctrl')
            if isfield(Tc.ctrl, 'meta') && isfield(Tc.ctrl.meta, 'Np')
                old_Np = Tc.ctrl.meta.Np;
                if old_Np == TARGET_NP
                    ctrl = Tc.ctrl;
                    ctrl_source = ctrl_file_path;
                    fprintf('  OK ctrl loaded (Np=%d)\n', old_Np);
                else
                    fprintf('  WARN old ctrl Np=%d, rebuild target Np=%d\n', old_Np, TARGET_NP);
                end
            else
                fprintf('  WARN ctrl.meta.Np missing, rebuild\n');
            end
        end
    catch ME
        fprintf('  WARN ctrl load failed: %s\n', ME.message);
    end
end

if isempty(ctrl) && exist('mpc_setup_single_interp','file')==2
    fprintf('  create new ctrl (Np=%d, Nc=%d)...\n', TARGET_NP, TARGET_NC);

    if maps_loaded && all(isfield(maps_best, {'Q_range','R_range','dR_range'}))
        Q_base = mean(maps_best.Q_range, 1);
        R_base = mean(maps_best.R_range, 1);
        dR_base = mean(maps_best.dR_range, 1);
        fprintf('    use optimized BO weights\n');
    else
        Q_base = [10, 15, 5, 1];
        R_base = [1e-3, 1e-3];
        dR_base = [1e-2, 1e-2];
        fprintf('    use default weights\n');
    end

    mpc_opts = struct('Np', TARGET_NP, 'Nc', TARGET_NC, ...
                      'Q', Q_base, 'R', R_base, 'dR', dR_base);

    ctrl = mpc_setup_single_interp(db_rt, mpc_opts);
    ctrl_source = 'created';
    fprintf('  OK ctrl created (P=%.2fs, M=%.2fs)\n', ...
        ctrl.meta.prediction_horizon_sec, ctrl.meta.control_horizon_sec);

    try
        save(ctrl_file_path, 'ctrl');
        fprintf('  saved ctrl.mat\n');
    catch ME
        fprintf('  WARN save ctrl.mat failed: %s\n', ME.message);
    end
end

if maps_loaded && ~isempty(ctrl)
    fields = {'Q_range','R_range','dR_range','alpha_Q','beta_Q', ...
        'alpha_R','beta_R','alpha_dR','beta_dR', ...
        'scale_umin_lo','scale_umin_hi','scale_umax_lo','scale_umax_hi', ...
        'omega_threshold', 'q_y_gain_max', 'theta_threshold', 'q_v_gain_max', ...
        'R_F_gain_max_uphill', 'R_F_gain_max_downhill', ...
        'transition_width', 'theta_transition_width'};

    copied = 0;
    for i = 1:numel(fields)
        if isfield(maps_best, fields{i})
            ctrl.maps.(fields{i}) = maps_best.(fields{i});
            copied = copied + 1;
        end
    end
    fprintf('  copied %d BO map fields to ctrl.maps\n', copied);
end

if ~isempty(ctrl)
    assignin('base', 'ctrl', ctrl);
else
    warning('[PreLoadFcn] Unable to create/load ctrl');
end
fprintf('\n');

%% Step 4: Load/configure learned model
if strcmp(mode, 'modern_tcn')
    fprintf('[Step 4/5] Configure ModernTCN model...\n');
    modern_tcn_cfg = ModernTCN_default_config(root);
    if exist(modern_tcn_cfg.dataset_file, 'file') ~= 2
        error('[PreLoadFcn] ModernTCN dataset not found: %s', modern_tcn_cfg.dataset_file);
    end
    if exist(modern_tcn_cfg.onnx_file, 'file') ~= 2
        error('[PreLoadFcn] ModernTCN ONNX not found: %s', modern_tcn_cfg.onnx_file);
    end

    assignin('base', 'modern_tcn_sim_cfg', modern_tcn_cfg);
    assignin('base', 'modern_tcn_default_cfg', modern_tcn_cfg);
    assignin(mw, 'modern_tcn_sim_cfg', modern_tcn_cfg);
    assignin(mw, 'modern_tcn_default_cfg', modern_tcn_cfg);

    info = struct();
    info.seed = modern_tcn_cfg.seed;
    info.run_tag = modern_tcn_cfg.run_tag;
    info.dataset_file = modern_tcn_cfg.dataset_file;
    info.onnx_file = modern_tcn_cfg.onnx_file;
    info.time = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
    assignin('base', 'modern_tcn_preload_info', info);
    assignin(mw, 'modern_tcn_preload_info', info);
    active_model_label = 'ModernTCN model';
    fprintf('  OK ModernTCN config frozen: seed=%d\n', modern_tcn_cfg.seed);
    fprintf('  ONNX: %s\n', modern_tcn_cfg.onnx_file);
    fprintf('  dataset: %s\n', modern_tcn_cfg.dataset_file);
else
    fprintf('[Step 4/5] Load GRU model...\n');
    gru_cfg = GRU_default_config(root);
    model_candidates = {
        gru_cfg.model_file
        fullfile(data_models_dir, 'GRU_model_gru_v4_industrial_inputstats_hidden96_seed101.mat')
        fullfile(data_models_dir, 'GRU_model_gru_v4_industrial_inputstats_hidden96_seed21.mat')
        fullfile(data_models_dir, 'GRU_model_gru_v4_industrial_inputstats_hidden96_seed42.mat')
        fullfile(data_models_dir, 'GRU_model_mamba_control_strict.mat')
        fullfile(data_models_dir, 'GRU_model_mamba_control.mat')
        fullfile(data_models_dir, 'GRU_model.mat')
        fullfile(data_gru_dir, 'GRU_model.mat')
        fullfile(root, 'GRU_model.mat')
    };
    model_candidates = unique(model_candidates, 'stable');

    meta_candidates = {
        gru_cfg.meta_file
        fullfile(data_models_dir, 'GRU_meta_gru_v4_industrial_inputstats_hidden96_seed101.mat')
        fullfile(data_models_dir, 'GRU_meta_gru_v4_industrial_inputstats_hidden96_seed21.mat')
        fullfile(data_models_dir, 'GRU_meta_gru_v4_industrial_inputstats_hidden96_seed42.mat')
        fullfile(data_models_dir, 'GRU_meta_mamba_control_strict.mat')
        fullfile(data_models_dir, 'GRU_meta_mamba_control.mat')
        fullfile(data_models_dir, 'GRU_meta.mat')
    };
    meta_candidates = unique(meta_candidates, 'stable');

    scaler_candidates = {
        fullfile(data_gru_dir, 'GRU_scaler.mat')
        fullfile(data_models_dir, 'GRU_scaler.mat')
        fullfile(root, 'GRU_scaler.mat')
    };
    scaler_candidates = unique(scaler_candidates, 'stable');

    model_file = pick_first_existing(model_candidates);
    if isempty(model_file)
        error('[PreLoadFcn] No GRU model file found.');
    end

    Sg = load(model_file);
    gru_model = extract_preferred_field(Sg, {'gru_model', 'model', 'net'});
    assignin('base', 'gru_model', gru_model);
    assignin(mw, 'gru_model', gru_model);
    fprintf('  OK GRU model loaded: %s\n', model_file);

    meta_file = pick_first_existing(meta_candidates);
    if ~isempty(meta_file)
        Sm = load(meta_file);
        gru_meta = extract_preferred_field(Sm, {'gru_meta', 'meta'});
        assignin('base', 'gru_meta', gru_meta);
        assignin(mw, 'gru_meta', gru_meta);
        fprintf('  OK GRU meta loaded: %s\n', meta_file);
    end

    gru_scaler = [];
    if isstruct(gru_model) && isfield(gru_model, 'scaler')
        gru_scaler = gru_model.scaler;
    end
    if isempty(gru_scaler)
        scaler_file = pick_first_existing(scaler_candidates);
        if ~isempty(scaler_file)
            Ss = load(scaler_file);
            if isfield(Ss, 'scaler')
                gru_scaler = Ss.scaler;
                fprintf('  OK GRU scaler loaded: %s\n', scaler_file);
            end
        end
    end
    if ~isempty(gru_scaler)
        assignin('base', 'gru_scaler', gru_scaler);
        assignin(mw, 'gru_scaler', gru_scaler);
    end

    info = struct();
    info.seed = gru_cfg.seed;
    info.case_name = gru_cfg.case_name;
    info.model_file = model_file;
    info.meta_file = meta_file;
    info.time = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
    assignin('base', 'gru_preload_info', info);
    assignin(mw, 'gru_preload_info', info);
    active_model_label = 'GRU model';
end
fprintf('\n');

%% Step 5: Summary
fprintf('[Step 5/5] Summary\n');
fprintf('  ================================================\n');
fprintf('  basic params:   loaded (Ts=%.3fs)\n', params.Ts);
fprintf('  LPV database:   %s (%d x %d x %d)\n', loaded_db_file, Nv, Nw, Nt);
fprintf('  MPCPlantBus:    created\n');
fprintf('  %-15s ready\n', [active_model_label ':']);

if maps_loaded
    [~, fname, ~] = fileparts(maps_source_file);
    fprintf('  BO maps:        loaded (%s)\n', fname);
else
    fprintf('  BO maps:        not loaded (defaults used)\n');
end

if ~isempty(ctrl)
    fprintf('  MPC controller: %s (Np=%d, Nc=%d)\n', ctrl_source, ctrl.meta.Np, ctrl.meta.Nc);
else
    fprintf('  MPC controller: not created\n');
end
fprintf('  ================================================\n');

if maps_loaded && ~isempty(ctrl)
    fprintf('\nInitialization completed (optimized BO maps + %s).\n', active_model_label);
elseif ~isempty(ctrl)
    fprintf('\nInitialization completed (default weights + %s).\n', active_model_label);
else
    fprintf('\nInitialization failed: check logs above.\n');
end

fprintf('\n[preloadfcn_%s] done\n\n', mode);
end

function path_out = pick_first_existing(candidates)
    path_out = '';
    for i = 1:numel(candidates)
        if exist(candidates{i}, 'file') == 2
            path_out = candidates{i};
            return;
        end
    end
end

function value = extract_preferred_field(s, preferred_names)
    for i = 1:numel(preferred_names)
        key = preferred_names{i};
        if isfield(s, key)
            value = s.(key);
            return;
        end
    end

    names = fieldnames(s);
    if isempty(names)
        error('preloadfcn_gru:EmptyMat', 'MAT file has no variables.');
    end
    value = s.(names{1});
end
