function result = run_stage1_lpv_rebuild(cfg)
%RUN_STAGE1_LPV_REBUILD Rebuild versioned LPV database for plantfix.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '04_lpv_database');
if exist(node_dir, 'dir') ~= 7; mkdir(node_dir); end
if ~isfield(cfg, 'mode') || isempty(cfg.mode); cfg.mode = 'preflight'; end
if ~isfield(cfg, 'write_canonical') || isempty(cfg.write_canonical); cfg.write_canonical = false; end

params = parameters();
plant = agv_plant_revision(params);
grid = local_grid();
versioned_db_file = fullfile(node_dir, 'lin_agv_db_agv_physics_v2_plantfix.mat');
canonical_db_file = fullfile(root, 'data', 'models', 'lin_agv_db.mat');

result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.mode = cfg.mode;
result.plant_revision = plant;
result.versioned_db_file = versioned_db_file;
result.canonical_db_file = canonical_db_file;
result.write_canonical = cfg.write_canonical;

if strcmpi(cfg.mode, 'preflight')
    result.status = 'preflight_ok';
else
    opts = struct('coord', 'path', 'disc', 'zoh', 'keep_E', true, ...
        'export_mat', versioned_db_file);
    db = lin_agv_grid(params, grid, opts); %#ok<NASGU>
    db.meta.plant_revision = plant;
    save(versioned_db_file, 'db', '-v7.3');
    if cfg.write_canonical
        save(canonical_db_file, 'db', '-v7.3');
    end
    result.status = 'rebuilt';
    result.db_meta = db.meta;
end

save(fullfile(node_dir, 'stage1_lpv_rebuild_result.mat'), 'result', '-v7.3');
local_write_report(node_dir, result);
fprintf('[stage1 LPV] status=%s report=%s\n', result.status, fullfile(node_dir, 'stage1_lpv_rebuild_report.md'));
end

function grid = local_grid()
grid = struct();
grid.V_grid = [0.02 0.04 0.06 0.08 0.10 0.14 0.20 0.35 0.60 1.00 1.20]';
grid.W_grid = linspace(-1.20, 1.20, 15)';
grid.T_grid = deg2rad((-12:1:12)');
end

function local_write_report(node_dir, result)
file = fullfile(node_dir, 'stage1_lpv_rebuild_report.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 LPV Rebuild Report\n\n');
fprintf(fid, '- status: `%s`\n', result.status);
fprintf(fid, '- plant_revision: `%s`\n', result.plant_revision.id);
fprintf(fid, '- versioned db: `%s`\n', result.versioned_db_file);
fprintf(fid, '- canonical db write: `%d`\n', double(result.write_canonical));
fprintf(fid, '- canonical db: `%s`\n\n', result.canonical_db_file);
fprintf(fid, 'The versioned database is the stage artifact. Canonical overwrite is explicit via `write_canonical=true`.\n');
end
