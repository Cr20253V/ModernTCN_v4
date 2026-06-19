function result = run_node06_full_route_oracle_validation(cfg)
%RUN_NODE06_FULL_ROUTE_ORACLE_VALIDATION Validate Node 6 MPC on existing routes.
%
% This supplemental workflow uses the Node 6 candidate controller
% (Np=30, Nc=10) with oracle slope scheduling from ref.theta_ref. It does
% not generate Node 7 training data.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();

out_dir = local_cfg(cfg, 'out_dir', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning'));
if exist(out_dir, 'dir') ~= 7
    mkdir(out_dir);
end

db_file = local_cfg(cfg, 'db_file', fullfile(root, 'data', 'models', 'lin_agv_db.mat'));
maps_file = local_cfg(cfg, 'maps_file', fullfile(out_dir, ...
    'maps_best_agv_physics_v2_node06.mat'));
path_files = local_cfg(cfg, 'path_files', local_default_path_files(root));
path_files = path_files(:);
path_limit = local_cfg(cfg, 'path_limit', 0);
if path_limit > 0
    path_files = path_files(1:min(path_limit, numel(path_files)));
end
if isempty(path_files)
    error('node06_full_route:NoPaths', 'No path files were configured.');
end

fprintf('\n[node06-full-route] db:    %s\n', db_file);
fprintf('[node06-full-route] maps:  %s\n', maps_file);
fprintf('[node06-full-route] paths: %d\n\n', numel(path_files));

Sdb = load(db_file);
if isfield(Sdb, 'db')
    db = Sdb.db;
else
    db = Sdb;
end

Smaps = load(maps_file);
if ~isfield(Smaps, 'maps_best')
    error('node06_full_route:MissingMapsBest', ...
        'Missing maps_best in %s.', maps_file);
end
maps_best = Smaps.maps_best;
if isfield(maps_best, 'node06_best_cfg')
    node06 = maps_best.node06_best_cfg;
else
    node06 = struct();
end
opts = local_node06_opts(node06);
assert(opts.Np == 30 && opts.Nc == 10, ...
    'Expected Node 6 Np=30/Nc=10, got Np=%d/Nc=%d.', opts.Np, opts.Nc);

ctrl = mpc_setup_single_interp(db, opts);
ctrl.maps = maps_best;
cfg_cost = struct();
cfg_cost.ctrl = ctrl;
cfg_cost.ctrl_maps = maps_best;
cfg_cost.tau = local_cfg(cfg, 'tau', 0.35);
cfg_cost.ey_max = 1.0;
cfg_cost.epsi_max = 0.5;
cfg_cost.ev_max = 0.5;
cfg_cost.eomega_max = 0.3;
cfg_cost.dF_max = 400;
cfg_cost.dw_max = 0.9;
cfg_cost.debug = local_cfg(cfg, 'debug', false);

params = parameters();
rows = repmat(local_empty_row(), numel(path_files), 1);
path_reports = struct();

for i = 1:numel(path_files)
    path_file = path_files{i};
    [~, path_tag] = fileparts(path_file);
    fprintf('[node06-full-route] %d/%d %s\n', i, numel(path_files), path_tag);

    row = local_empty_row();
    row.path_tag = string(path_tag);
    row.path_file = string(path_file);
    row.status = "running";
    row.elapsed_sec = NaN;
    row.Np = opts.Np;
    row.Nc = opts.Nc;

    t0 = tic;
    try
        Sref = load(path_file, 'ref');
        if ~isfield(Sref, 'ref')
            error('node06_full_route:MissingRef', ...
                'Path file has no ref variable: %s', path_file);
        end
        ref = Sref.ref;
        if ~isfield(ref, 'meta')
            ref.meta = struct();
        end
        if ~isfield(ref.meta, 'zones')
            ref.meta.zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
        end

        cfg_one = cfg_cost;
        cfg_one.path_file = path_file;
        cfg_one.zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
        scenes = struct('full_route', 1.0);

        [J, report] = Cost_Function(params, db, cfg_one, scenes);
        rep = report.scene.full_route;

        row.status = local_status_from_report(report, rep);
        row.J = J;
        row.fail_count = report.fail_count;
        row.duration_s = ref.t(end) - ref.t(1);
        row.n_samples = numel(ref.t);
        row.valid_steps = local_get_nested(rep, {'control', 'valid_steps'}, NaN);
        row.completion_ratio = local_get_nested(rep, {'steps', 'completion_ratio'}, NaN);
        row.ey_rmse = local_get_nested(rep, {'RMSE', 'ey'}, NaN);
        row.epsi_rmse = local_get_nested(rep, {'RMSE', 'epsi'}, NaN);
        row.ev_rmse = local_get_nested(rep, {'RMSE', 'ev'}, NaN);
        row.eomega_rmse = local_get_nested(rep, {'RMSE', 'eomega'}, NaN);
        row.cons_L1 = local_get_nested(rep, {'cons', 'L1'}, NaN);
        row.cons_Linf = local_get_nested(rep, {'cons', 'Linf'}, NaN);
        row.F_peak = local_get_nested(rep, {'control', 'F_peak'}, NaN);
        row.omega_peak = local_get_nested(rep, {'control', 'omega_peak'}, NaN);
        row.F_sat_rate = local_get_nested(rep, {'control', 'F_sat_rate'}, NaN);
        row.omega_sat_rate = local_get_nested(rep, {'control', 'omega_sat_rate'}, NaN);
        row.dF_peak = local_get_nested(rep, {'control', 'dF_peak'}, NaN);
        row.domega_peak = local_get_nested(rep, {'control', 'domega_peak'}, NaN);
        row.solve_avg_ms = local_get_nested(rep, {'solve_ms', 'avg'}, NaN);
        row.solve_max_ms = local_get_nested(rep, {'solve_ms', 'max'}, NaN);
        row.first_fail_step = local_get_nested(rep, {'steps', 'first_fail_step'}, NaN);
        row.first_fail_reason = string(local_get_nested(rep, {'steps', 'first_fail_reason'}, ''));
        row.first_fail_qpcode = string(local_get_nested(rep, {'steps', 'first_fail_qpcode'}, ''));
        row.elapsed_sec = toc(t0);
        path_reports.(matlab.lang.makeValidName(path_tag)) = report;
    catch ME
        row.status = "error";
        row.message = string(ME.message);
        row.elapsed_sec = toc(t0);
        fprintf('[node06-full-route] ERROR %s: %s\n', path_tag, ME.message);
    end

    rows(i) = row;
    fprintf('[node06-full-route] %s elapsed=%.1fs J=%.6g fail=%g cons_Linf=%.6g\n', ...
        path_tag, row.elapsed_sec, row.J, row.fail_count, row.cons_Linf);
end

summary_table = struct2table(rows);
timestamp = datestr(now, 'yyyymmdd_HHMMSS');
summary_file = fullfile(out_dir, ['node06_full_route_oracle_summary_' timestamp '.csv']);
mat_file = fullfile(out_dir, ['node06_full_route_oracle_validation_' timestamp '.mat']);
report_file = fullfile(out_dir, ['node06_full_route_oracle_report_' timestamp '.md']);
writetable(summary_table, summary_file);

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.objective = 'Node 6 Np=30/Nc=10 full-route oracle-slope validation; Node 7 skipped.';
result.db_file = db_file;
result.maps_file = maps_file;
result.path_files = path_files;
result.opts = opts;
result.cost_cfg = cfg_cost;
result.summary_table = summary_table;
result.path_reports = path_reports;
result.summary_file = summary_file;
result.mat_file = mat_file;
result.report_file = report_file;
save(mat_file, 'result', '-v7.3');
local_write_report(report_file, result);

fprintf('\n[node06-full-route] summary: %s\n', summary_file);
fprintf('[node06-full-route] report:  %s\n', report_file);
fprintf('[node06-full-route] mat:     %s\n', mat_file);
end

function opts = local_node06_opts(node06)
opts = struct();
opts.Np = local_cfg(node06, 'Np', 30);
opts.Nc = local_cfg(node06, 'Nc', 10);
opts.Q = local_cfg(node06, 'Q', [15.293, 28.737, 5.076, 2.9918]);
opts.R = local_cfg(node06, 'R', [1e-3, 1e-3]);
opts.dR = local_cfg(node06, 'dR', [1e-2, 1e-2]);
opts.umin = [-600; -1.2];
opts.umax = [600; 1.2];
opts.dumin = [-400; -0.9];
opts.dumax = [400; 0.9];
opts.ymin = [-1.0; -0.5; -0.5; -0.3];
opts.ymax = [1.0; 0.5; 0.5; 0.3];
opts.soft_weight_pos = local_cfg(node06, 'soft_weight_pos', 3e3);
opts.soft_weight_yaw = local_cfg(node06, 'soft_weight_yaw', 3e3);
end

function path_files = local_default_path_files(root)
files = dir(fullfile(root, 'data', 'paths', '*.mat'));
path_files = {};
for i = 1:numel(files)
    candidate = fullfile(files(i).folder, files(i).name);
    try
        S = load(candidate, 'ref');
        if isfield(S, 'ref') && isfield(S.ref, 'meta') && isfield(S.ref.meta, 'zones')
            path_files{end + 1, 1} = candidate; %#ok<AGROW>
        end
    catch
        % Ignore non-reference MAT files in data/paths.
    end
end
path_files = sort(path_files);
end

function row = local_empty_row()
row = struct( ...
    'path_tag', "", 'path_file', "", 'status', "pending", 'message', "", ...
    'Np', NaN, 'Nc', NaN, 'duration_s', NaN, 'n_samples', NaN, ...
    'valid_steps', NaN, 'completion_ratio', NaN, ...
    'J', NaN, 'fail_count', NaN, ...
    'ey_rmse', NaN, 'epsi_rmse', NaN, 'ev_rmse', NaN, 'eomega_rmse', NaN, ...
    'cons_L1', NaN, 'cons_Linf', NaN, ...
    'F_peak', NaN, 'omega_peak', NaN, ...
    'F_sat_rate', NaN, 'omega_sat_rate', NaN, ...
    'dF_peak', NaN, 'domega_peak', NaN, ...
    'solve_avg_ms', NaN, 'solve_max_ms', NaN, ...
    'first_fail_step', NaN, 'first_fail_reason', "", 'first_fail_qpcode', "", ...
    'elapsed_sec', NaN);
end

function status = local_status_from_report(report, rep)
if isfield(report, 'failed') && report.failed
    status = "failed";
elseif isfield(rep, 'failed') && rep.failed
    status = "failed";
else
    status = "ok";
end
end

function v = local_cfg(cfg, name, default_value)
if isstruct(cfg) && isfield(cfg, name) && ~isempty(cfg.(name))
    v = cfg.(name);
else
    v = default_value;
end
end

function v = local_get_nested(s, names, default_value)
v = default_value;
cur = s;
for i = 1:numel(names)
    name = names{i};
    if ~isstruct(cur) || ~isfield(cur, name)
        return;
    end
    cur = cur.(name);
end
v = cur;
end

function local_write_report(report_file, result)
T = result.summary_table;
fid = fopen(report_file, 'w');
if fid < 0
    error('node06_full_route:ReportOpenFailed', ...
        'Cannot open report for writing: %s', report_file);
end
cleanup = onCleanup(@() fclose(fid));

fprintf(fid, '# Node 6 Full-Route Oracle-Slope MPC Validation\n\n');
fprintf(fid, '- Timestamp: `%s`\n', result.timestamp);
fprintf(fid, '- Scope: `Np=30`, `Nc=10`, oracle slope from `ref.theta_ref`.\n');
fprintf(fid, '- Node 7 status: skipped; no training data regeneration was run.\n');
fprintf(fid, '- LPV database: `%s`\n', result.db_file);
fprintf(fid, '- Node 6 maps: `%s`\n', result.maps_file);
fprintf(fid, '- Summary CSV: `%s`\n', result.summary_file);
fprintf(fid, '- MAT result: `%s`\n\n', result.mat_file);

fprintf(fid, '| path | status | fail | completion | J | e_y RMSE | e_psi RMSE | e_v RMSE | e_omega RMSE | cons Linf | F peak | omega peak | F sat %% | omega sat %% | avg solve ms | elapsed s |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n');
for i = 1:height(T)
    fprintf(fid, '| `%s` | %s | %.0f | %.4f | %.6g | %.6g | %.6g | %.6g | %.6g | %.6g | %.6g | %.6g | %.3f | %.3f | %.3f | %.1f |\n', ...
        T.path_tag(i), T.status(i), T.fail_count(i), T.completion_ratio(i), T.J(i), ...
        T.ey_rmse(i), T.epsi_rmse(i), T.ev_rmse(i), T.eomega_rmse(i), ...
        T.cons_Linf(i), T.F_peak(i), T.omega_peak(i), ...
        100 * T.F_sat_rate(i), 100 * T.omega_sat_rate(i), ...
        T.solve_avg_ms(i), T.elapsed_sec(i));
end

bad = T(T.status ~= "ok", :);
if ~isempty(bad)
    fprintf(fid, '\n## Non-OK Runs\n\n');
    fprintf(fid, '| path | status | first fail step | qpcode | reason | message |\n');
    fprintf(fid, '|---|---:|---:|---|---|---|\n');
    for i = 1:height(bad)
        fprintf(fid, '| `%s` | %s | %.0f | `%s` | %s | %s |\n', ...
            bad.path_tag(i), bad.status(i), bad.first_fail_step(i), ...
            bad.first_fail_qpcode(i), bad.first_fail_reason(i), bad.message(i));
    end
end
end
