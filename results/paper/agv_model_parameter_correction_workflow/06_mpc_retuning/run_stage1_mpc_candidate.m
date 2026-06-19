function result = run_stage1_mpc_candidate(cfg)
%RUN_STAGE1_MPC_CANDIDATE Create a versioned plantfix MPC candidate.
%
% This does not change plant damping. It only records controller weights,
% horizons, and maps for explicit runtime override.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning');
if exist(node_dir, 'dir') ~= 7; mkdir(node_dir); end

if ~isfield(cfg, 'id') || isempty(cfg.id); cfg.id = 'stage1_plantfix_p0'; end
if ~isfield(cfg, 'Np') || isempty(cfg.Np); cfg.Np = 150; end
if ~isfield(cfg, 'Nc') || isempty(cfg.Nc); cfg.Nc = 30; end
if ~isfield(cfg, 'Q') || isempty(cfg.Q); cfg.Q = [100, 100, 15, 3]; end
if ~isfield(cfg, 'R') || isempty(cfg.R); cfg.R = [3e-5, 3e-5]; end
if ~isfield(cfg, 'dR') || isempty(cfg.dR); cfg.dR = [1e-3, 1e-3]; end
if ~isfield(cfg, 'write_canonical') || isempty(cfg.write_canonical); cfg.write_canonical = false; end

plant = agv_plant_revision(parameters());
db_file = fullfile(root, 'data', 'models', 'lin_agv_db.mat');
versioned_db_file = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '04_lpv_database', ...
    'lin_agv_db_agv_physics_v2_plantfix.mat');
if exist(versioned_db_file, 'file') == 2
    db_file = versioned_db_file;
end
S = load(db_file, 'db');
if ~isfield(S, 'db')
    error('stage1_mpc:MissingDb', 'DB file has no db variable: %s', db_file);
end
db = S.db;

opts = struct('Np', cfg.Np, 'Nc', cfg.Nc, 'Q', cfg.Q, 'R', cfg.R, 'dR', cfg.dR);
ctrl = mpc_setup_single_interp(db, opts);
maps_best = ctrl.maps;
maps_best.id = cfg.id;
maps_best.plant_revision = plant;
maps_best.Np = cfg.Np;
maps_best.Nc = cfg.Nc;
maps_best.Q = cfg.Q;
maps_best.R = cfg.R;
maps_best.dR = cfg.dR;
maps_best.Q_range = [cfg.Q; cfg.Q];
maps_best.R_range = [cfg.R; cfg.R];
maps_best.dR_range = [cfg.dR; cfg.dR];
maps_best.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
maps_best.version = 'stage1_plantfix_candidate';
maps_best.db_file = db_file;

versioned_maps_file = fullfile(node_dir, 'maps_best_agv_physics_v2_plantfix_stage1.mat');
save(versioned_maps_file, 'maps_best', 'ctrl', 'opts', 'db_file', '-v7.3');
canonical_maps_file = fullfile(root, 'data', 'models', 'maps_best.mat');
if cfg.write_canonical
    save(canonical_maps_file, 'maps_best', '-v7.3');
end

result = struct();
result.timestamp = maps_best.timestamp;
result.status = 'candidate_created';
result.plant_revision = plant;
result.db_file = db_file;
result.versioned_maps_file = versioned_maps_file;
result.canonical_maps_file = canonical_maps_file;
result.write_canonical = cfg.write_canonical;
result.opts = opts;
save(fullfile(node_dir, 'stage1_mpc_candidate_result.mat'), 'result', '-v7.3');
local_write_report(node_dir, result);
fprintf('[stage1 MPC] candidate=%s\n', versioned_maps_file);
end

function local_write_report(node_dir, result)
file = fullfile(node_dir, 'stage1_mpc_candidate_report.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 MPC Candidate Report\n\n');
fprintf(fid, '- status: `%s`\n', result.status);
fprintf(fid, '- plant_revision: `%s`\n', result.plant_revision.id);
fprintf(fid, '- db_file: `%s`\n', result.db_file);
fprintf(fid, '- maps file: `%s`\n', result.versioned_maps_file);
fprintf(fid, '- canonical maps write: `%d`\n\n', double(result.write_canonical));
fprintf(fid, '## Controller\n\n');
fprintf(fid, '- Np: `%d`\n', result.opts.Np);
fprintf(fid, '- Nc: `%d`\n', result.opts.Nc);
fprintf(fid, '- Q: `%s`\n', mat2str(result.opts.Q));
fprintf(fid, '- R: `%s`\n', mat2str(result.opts.R));
fprintf(fid, '- dR: `%s`\n', mat2str(result.opts.dR));
fprintf(fid, '\nPlant damping is not changed by this runner.\n');
end
