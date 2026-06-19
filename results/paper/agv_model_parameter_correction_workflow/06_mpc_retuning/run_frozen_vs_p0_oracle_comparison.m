function result = run_frozen_vs_p0_oracle_comparison(cfg)
%RUN_FROZEN_VS_P0_ORACLE_COMPARISON Compare historical frozen MPC maps vs P0.
%
% Scope:
%   - Re-evaluate existing 7 full-route oracle-slope paths.
%   - Use the repaired offline oracle replay in Cost_Function.m.
%   - Do not overwrite canonical data/models/maps_best.mat.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();
params = parameters();

timestamp = datestr(now, 'yyyymmdd_HHMMSS');
base_out_dir = local_cfg(cfg, 'out_dir', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning'));
run_dir = local_cfg(cfg, 'run_dir', fullfile(base_out_dir, ...
    ['frozen_vs_p0_oracle_' timestamp]));
if exist(run_dir, 'dir') ~= 7
    mkdir(run_dir);
end

db_file = local_cfg(cfg, 'db_file', fullfile(root, 'data', 'models', 'lin_agv_db.mat'));
legacy_maps_file = local_cfg(cfg, 'legacy_maps_file', fullfile(root, 'data', 'models', 'maps_best.mat'));
p0_maps_file = local_cfg(cfg, 'p0_maps_file', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning', ...
    'p0_oracle_retuning_20260602_033639', 'maps_best_agv_physics_v2_p0_oracle.mat'));

Sdb = load(db_file);
if isfield(Sdb, 'db')
    db = Sdb.db;
else
    db = Sdb;
end

paths = local_full_route_paths(root);
if isfield(cfg, 'path_files') && ~isempty(cfg.path_files)
    paths = cfg.path_files;
end
candidates = local_candidates(legacy_maps_file, p0_maps_file);
if isfield(cfg, 'candidate_ids') && ~isempty(cfg.candidate_ids)
    candidates = local_filter_candidates(candidates, cfg.candidate_ids);
end

fprintf('\n[frozen-vs-p0] run_dir: %s\n', run_dir);
fprintf('[frozen-vs-p0] paths: %d\n', numel(paths));
fprintf('[frozen-vs-p0] candidates: %d\n\n', numel(candidates));

path_rows = repmat(local_empty_path_row(), 0, 1);
candidate_rows = repmat(local_empty_candidate_row(), numel(candidates), 1);
reports = struct();

for i = 1:numel(candidates)
    cand = candidates(i);
    fprintf('[frozen-vs-p0] %d/%d %s Np=%d Nc=%d\n', ...
        i, numel(candidates), cand.id, cand.Np, cand.Nc);
    t0 = tic;
    [one_rows, one_reports] = local_eval_candidate(cand, paths, params, db, run_dir);
    candidate_rows(i) = local_aggregate_candidate(cand, one_rows, toc(t0));
    path_rows = [path_rows; one_rows(:)]; %#ok<AGROW>
    reports.(matlab.lang.makeValidName(cand.id)) = one_reports;
    local_write_outputs(run_dir, candidate_rows(1:i), path_rows, reports);
    fprintf('[frozen-vs-p0] %s max_ey=%.6g mean_ey=%.6g fail=%g pass=%d\n', ...
        cand.id, candidate_rows(i).max_ey_rmse, candidate_rows(i).mean_ey_rmse, ...
        candidate_rows(i).total_fail_count, candidate_rows(i).pass_0p10);
end

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.run_dir = run_dir;
result.db_file = db_file;
result.legacy_maps_file = legacy_maps_file;
result.p0_maps_file = p0_maps_file;
result.paths = paths;
result.candidate_table = struct2table(candidate_rows);
result.path_table = struct2table(path_rows);
result.reports = reports;
result.note = ['legacy_maps_best keeps the historical maps_best fields but is ' ...
    'completed with the current map interface before replay.'];

save(fullfile(run_dir, 'frozen_vs_p0_oracle_comparison.mat'), 'result', '-v7.3');
local_write_report(run_dir, result.candidate_table, result.path_table, candidates);

fprintf('\n[frozen-vs-p0] done: %s\n', run_dir);
fprintf('[frozen-vs-p0] report: %s\n', fullfile(run_dir, 'frozen_vs_p0_oracle_comparison_report.md'));
end

function candidates = local_filter_candidates(candidates, ids)
ids = string(ids);
keep = false(size(candidates));
for i = 1:numel(candidates)
    keep(i) = any(string(candidates(i).id) == ids);
end
candidates = candidates(keep);
if isempty(candidates)
    error('frozen_vs_p0:NoCandidates', 'No requested candidate_ids matched.');
end
end

function candidates = local_candidates(legacy_maps_file, p0_maps_file)
Slegacy = load(legacy_maps_file);
legacy_maps = local_loaded_maps(Slegacy, legacy_maps_file);

Sp0 = load(p0_maps_file);
p0_maps = local_loaded_maps(Sp0, p0_maps_file);

legacy_Q = mean(legacy_maps.Q_range, 1);
legacy_R = mean(legacy_maps.R_range, 1);
legacy_dR = mean(legacy_maps.dR_range, 1);

candidates = repmat(local_candidate('', '', '', NaN, NaN, ...
    [NaN NaN NaN NaN], [NaN NaN], [NaN NaN], struct()), 4, 1);

candidates(1) = local_candidate( ...
    'legacy_maps_best', ...
    'Historical data/models/maps_best.mat', ...
    legacy_maps_file, ...
    150, 50, legacy_Q, legacy_R, legacy_dR, legacy_maps);

candidates(2) = local_candidate( ...
    'bo_frozen_base_initial', ...
    'BO frozen defaults with base initial Q/R/dR', ...
    '', ...
    150, 50, [10, 15, 2, 1], [1e-3, 1e-3], [1e-2, 1e-2], local_bo_frozen_maps());

candidates(3) = local_candidate( ...
    'p0_selected', ...
    'P0 selected oracle-MPC candidate', ...
    p0_maps_file, ...
    150, 30, [100, 100, 15, 3], [3e-5, 3e-5], [1e-3, 1e-3], p0_maps);

updateplant_maps = local_updateplantmodel_maps();
updateplant_Q = mean(updateplant_maps.Q_range, 1);
updateplant_R = mean(updateplant_maps.R_range, 1);
updateplant_dR = mean(updateplant_maps.dR_range, 1);
candidates(4) = local_candidate( ...
    'updateplantmodel_hardcoded_bo', ...
    'Current hardcoded BO maps in src/core/UpdatePlantModel.m', ...
    'src/core/UpdatePlantModel.m', ...
    150, 50, updateplant_Q, updateplant_R, updateplant_dR, updateplant_maps);
end

function cand = local_candidate(id, label, source_file, Np, Nc, Q, R, dR, maps)
cand = struct();
cand.id = char(id);
cand.label = string(label);
cand.source_file = string(source_file);
cand.Np = Np;
cand.Nc = Nc;
cand.Q = Q;
cand.R = R;
cand.dR = dR;
cand.maps = maps;
end

function maps = local_bo_frozen_maps()
maps = struct();
maps.alpha_Q = repmat(0.5, 1, 4);
maps.beta_Q = repmat(0.5, 1, 4);
maps.alpha_R = repmat(0.5, 1, 2);
maps.beta_R = repmat(0.5, 1, 2);
maps.alpha_dR = repmat(0.5, 1, 2);
maps.beta_dR = repmat(0.5, 1, 2);
maps.scale_umin_lo = [1, 1];
maps.scale_umin_hi = [1, 1];
maps.scale_umax_lo = [1, 1];
maps.scale_umax_hi = [1, 1];
maps.tau = 0.35;
maps.omega_threshold = 0.15;
maps.q_y_gain_max = 1.0;
maps.theta_threshold = 0.04;
maps.q_v_gain_max = 1.0;
maps.transition_width = 0.03;
maps.theta_transition_width = 0.02;
maps.R_F_gain_max_uphill = 1.0;
maps.R_F_gain_max_downhill = 1.0;
maps.dR_F_gain_max_uphill = 1.0;
maps.dR_F_gain_max_downhill = 1.0;
end

function maps = local_updateplantmodel_maps()
maps = struct();
maps.enable_weight_interp = true;
maps.Q_range = [ ...
    65.5231, 8.1684, 18.3989, 0.4160; ...
    196.5693, 24.5051, 55.1966, 1.2481];
maps.R_range = [ ...
    0.0015, 0.0058; ...
    0.0046, 0.0173];
maps.dR_range = [ ...
    0.0017, 0.1309; ...
    0.0050, 0.3927];
maps.alpha_Q = [0.5, 0.5, 0.5, 0.5];
maps.beta_Q = [0.5, 0.5, 0.5, 0.5];
maps.alpha_R = [0.5, 0.5];
maps.beta_R = [0.5, 0.5];
maps.alpha_dR = [0.5, 0.5];
maps.beta_dR = [0.5, 0.5];
maps.scale_umin_lo = [1, 1];
maps.scale_umin_hi = [1, 1];
maps.scale_umax_lo = [1, 1];
maps.scale_umax_hi = [1, 1];
maps.rho_min = [0.02; -1.2; -0.1745];
maps.rho_max = [1.2; 1.2; 0.1745];
maps.tau = 0.35;
maps.omega_threshold = 0.139817184968;
maps.q_y_gain_max = 5.54865433581;
maps.transition_width = 0.03;
maps.theta_threshold = 0.125151060428;
maps.q_v_gain_max = 3.46559044719;
maps.theta_transition_width = 0.02;
maps.R_F_gain_max_uphill = 1.00755999315;
maps.R_F_gain_max_downhill = 1.0;
maps.dR_F_gain_max_uphill = 1.0;
maps.dR_F_gain_max_downhill = 1.0;
maps.umin_range = [-720, -1.44; -600, -1.2];
maps.umax_range = [600, 1.2; 720, 1.44];
end

function maps = local_loaded_maps(S, file_name)
if isfield(S, 'maps_best')
    maps = S.maps_best;
elseif isfield(S, 'maps')
    maps = S.maps;
else
    error('frozen_vs_p0:MissingMaps', 'No maps_best/maps in %s.', file_name);
end
end

function [path_rows, reports] = local_eval_candidate(cand, paths, params, db, run_dir)
ctrl = local_build_ctrl(cand, db);
path_rows = repmat(local_empty_path_row(), numel(paths), 1);
reports = struct();

for p = 1:numel(paths)
    path_file = paths{p};
    [~, path_tag] = fileparts(path_file);
    row = local_empty_path_row();
    row.candidate_id = string(cand.id);
    row.label = cand.label;
    row.path_tag = string(path_tag);
    row.path_file = string(path_file);
    row.Np = cand.Np;
    row.Nc = cand.Nc;
    row.q_y = cand.Q(1);
    row.q_psi = cand.Q(2);
    row.q_v = cand.Q(3);
    row.q_omega = cand.Q(4);
    row.r_F = cand.R(1);
    row.r_omega = cand.R(2);
    row.dR_F = cand.dR(1);
    row.dR_omega = cand.dR(2);
    t0 = tic;
    try
        Sref = load(path_file, 'ref');
        ref = Sref.ref;
        cfg_one = struct();
        cfg_one.ctrl = ctrl;
        cfg_one.ctrl_maps = ctrl.maps;
        cfg_one.path_file = path_file;
        cfg_one.zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
        cfg_one.report_zones = local_ref_zones(ref);
        cfg_one.tau = local_map_tau(ctrl.maps);
        cfg_one.ey_max = 1.0;
        cfg_one.epsi_max = 0.5;
        cfg_one.ev_max = 0.5;
        cfg_one.eomega_max = 0.3;
        cfg_one.dF_max = 400;
        cfg_one.dw_max = 0.9;
        cfg_one.debug = false;
        [J, report] = Cost_Function(params, db, cfg_one, struct('full_route', 1.0));
        rep = report.scene.full_route;
        row.status = local_status_from_report(report, rep);
        row.J = J;
        row.fail_count = report.fail_count;
        row.completion_ratio = local_get_nested(rep, {'steps', 'completion_ratio'}, NaN);
        row.duration_s = ref.t(end) - ref.t(1);
        row.n_samples = numel(ref.t);
        row.valid_steps = local_get_nested(rep, {'control', 'valid_steps'}, NaN);
        row.ey_rmse = local_get_nested(rep, {'RMSE', 'ey'}, NaN);
        row.ey_peak = local_get_nested(rep, {'peak', 'ey'}, NaN);
        row.epsi_rmse = local_get_nested(rep, {'RMSE', 'epsi'}, NaN);
        row.epsi_peak = local_get_nested(rep, {'peak', 'epsi'}, NaN);
        row.ev_rmse = local_get_nested(rep, {'RMSE', 'ev'}, NaN);
        row.eomega_rmse = local_get_nested(rep, {'RMSE', 'eomega'}, NaN);
        row.cons_L1 = local_get_nested(rep, {'cons', 'L1'}, NaN);
        row.cons_Linf = local_get_nested(rep, {'cons', 'Linf'}, NaN);
        row.cons_violation_rate = local_get_nested(rep, {'cons', 'violation_rate'}, NaN);
        row.F_peak = local_get_nested(rep, {'control', 'F_peak'}, NaN);
        row.omega_peak = local_get_nested(rep, {'control', 'omega_peak'}, NaN);
        row.F_sat_rate = local_get_nested(rep, {'control', 'F_sat_rate'}, NaN);
        row.omega_sat_rate = local_get_nested(rep, {'control', 'omega_sat_rate'}, NaN);
        row.solve_avg_ms = local_get_nested(rep, {'solve_ms', 'avg'}, NaN);
        row.solve_max_ms = local_get_nested(rep, {'solve_ms', 'max'}, NaN);
        row.first_fail_step = local_get_nested(rep, {'steps', 'first_fail_step'}, NaN);
        row.first_fail_reason = string(local_get_nested(rep, {'steps', 'first_fail_reason'}, ''));
        row.first_fail_qpcode = string(local_get_nested(rep, {'steps', 'first_fail_qpcode'}, ''));
        reports.(matlab.lang.makeValidName(path_tag)) = report;
    catch ME
        row.status = "error";
        row.message = string(ME.message);
        row.fail_count = 1;
    end
    row.elapsed_sec = toc(t0);
    path_rows(p) = row;
    local_write_live_candidate_paths(run_dir, cand.id, path_rows(1:p));
end
end

function local_write_live_candidate_paths(run_dir, candidate_id, path_rows)
safe_id = matlab.lang.makeValidName(candidate_id);
live_file = fullfile(run_dir, ['live_' safe_id '_path_summary.csv']);
writetable(struct2table(path_rows), live_file);
end

function ctrl = local_build_ctrl(cand, db)
opts = struct();
opts.Np = cand.Np;
opts.Nc = cand.Nc;
opts.Q = cand.Q;
opts.R = cand.R;
opts.dR = cand.dR;
opts.umin = [-600; -1.2];
opts.umax = [600; 1.2];
opts.dumin = [-400; -0.9];
opts.dumax = [400; 0.9];
opts.ymin = [-1.0; -0.5; -0.5; -0.3];
opts.ymax = [1.0; 0.5; 0.5; 0.3];
opts.soft_weight_pos = 3e3;
opts.soft_weight_yaw = 3e3;
evalc('ctrl_tmp = mpc_setup_single_interp(db, opts);');
ctrl = ctrl_tmp;

maps = ctrl.maps;
incoming = cand.maps;
if ~isempty(fieldnames(incoming))
    fns = fieldnames(incoming);
    for i = 1:numel(fns)
        maps.(fns{i}) = incoming.(fns{i});
    end
end
maps.Q_range = [cand.Q * 0.5; cand.Q * 1.5];
maps.R_range = [cand.R * 0.5; cand.R * 1.5];
maps.dR_range = [cand.dR * 0.5; cand.dR * 1.5];
if isfield(incoming, 'Q_range') && ~isempty(incoming.Q_range)
    maps.Q_range = incoming.Q_range;
end
if isfield(incoming, 'R_range') && ~isempty(incoming.R_range)
    maps.R_range = incoming.R_range;
end
if isfield(incoming, 'dR_range') && ~isempty(incoming.dR_range)
    maps.dR_range = incoming.dR_range;
end
maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];
ctrl.maps = maps;
end

function row = local_aggregate_candidate(cand, path_rows, elapsed_sec)
row = local_empty_candidate_row();
row.candidate_id = string(cand.id);
row.label = cand.label;
row.source_file = cand.source_file;
row.status = "ok";
if any([path_rows.status] == "error")
    row.status = "error";
end
row.Np = cand.Np;
row.Nc = cand.Nc;
row.q_y = cand.Q(1);
row.q_psi = cand.Q(2);
row.q_v = cand.Q(3);
row.q_omega = cand.Q(4);
row.r_F = cand.R(1);
row.r_omega = cand.R(2);
row.dR_F = cand.dR(1);
row.dR_omega = cand.dR(2);
row.num_paths = numel(path_rows);
row.total_fail_count = sum([path_rows.fail_count], 'omitnan');
row.min_completion_ratio = min([path_rows.completion_ratio], [], 'omitnan');
row.max_ey_rmse = max([path_rows.ey_rmse], [], 'omitnan');
row.mean_ey_rmse = mean([path_rows.ey_rmse], 'omitnan');
row.max_ey_peak = max([path_rows.ey_peak], [], 'omitnan');
row.max_epsi_rmse = max([path_rows.epsi_rmse], [], 'omitnan');
row.max_cons_Linf = max([path_rows.cons_Linf], [], 'omitnan');
row.max_cons_violation_rate = max([path_rows.cons_violation_rate], [], 'omitnan');
row.max_F_sat_rate = max([path_rows.F_sat_rate], [], 'omitnan');
row.max_omega_sat_rate = max([path_rows.omega_sat_rate], [], 'omitnan');
row.mean_solve_avg_ms = mean([path_rows.solve_avg_ms], 'omitnan');
row.max_solve_max_ms = max([path_rows.solve_max_ms], [], 'omitnan');
row.elapsed_sec = elapsed_sec;
row.pass_0p10 = row.total_fail_count == 0 && row.min_completion_ratio >= 1 && row.max_ey_rmse < 0.10;
row.pass_0p05 = row.total_fail_count == 0 && row.min_completion_ratio >= 1 && row.max_ey_rmse < 0.05;
end

function local_write_outputs(run_dir, candidate_rows, path_rows, reports)
candidate_table = struct2table(candidate_rows);
path_table = struct2table(path_rows);
writetable(candidate_table, fullfile(run_dir, 'frozen_vs_p0_candidate_summary.csv'));
writetable(path_table, fullfile(run_dir, 'frozen_vs_p0_path_summary.csv'));
save(fullfile(run_dir, 'frozen_vs_p0_partial.mat'), ...
    'candidate_table', 'path_table', 'reports', '-v7.3');
end

function local_write_report(run_dir, candidate_table, path_table, candidates)
report_file = fullfile(run_dir, 'frozen_vs_p0_oracle_comparison_report.md');
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));

fprintf(fid, '# Frozen vs P0 Oracle-MPC Comparison\n\n');
fprintf(fid, '- Timestamp: `%s`\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
fprintf(fid, '- Target: `max e_y RMSE < 0.100 m`; ideal `< 0.050 m`\n');
fprintf(fid, '- Paths: `%d` full routes with `ref.meta.zones`\n', height(path_table) / max(height(candidate_table), 1));
fprintf(fid, '- Node 7 status: `not run`\n\n');

fprintf(fid, '## Candidate Definitions\n\n');
fprintf(fid, '| candidate | source | Np | Nc | Q | R | dR |\n');
fprintf(fid, '|---|---|---:|---:|---|---|---|\n');
for i = 1:numel(candidates)
    c = candidates(i);
    fprintf(fid, '| `%s` | %s | %d | %d | `%s` | `%s` | `%s` |\n', ...
        c.id, local_md_escape(char(c.label)), c.Np, c.Nc, ...
        local_vec(c.Q), local_vec(c.R), local_vec(c.dR));
end

fprintf(fid, '\n## Overall Summary\n\n');
fprintf(fid, '| candidate | pass <0.1 | pass <0.05 | fail | min completion | max e_y RMSE | mean e_y RMSE | max e_y peak | max cons Linf | omega sat max | avg solve ms |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n');
for i = 1:height(candidate_table)
    r = candidate_table(i, :);
    fprintf(fid, '| `%s` | %d | %d | %.0f | %.3f | %.6f | %.6f | %.6f | %.6f | %.6f | %.3f |\n', ...
        r.candidate_id, r.pass_0p10, r.pass_0p05, r.total_fail_count, ...
        r.min_completion_ratio, r.max_ey_rmse, r.mean_ey_rmse, r.max_ey_peak, ...
        r.max_cons_Linf, r.max_omega_sat_rate, r.mean_solve_avg_ms);
end

fprintf(fid, '\n## Per-Path e_y RMSE\n\n');
ids = string(candidate_table.candidate_id);
paths = unique(string(path_table.path_tag), 'stable');
fprintf(fid, '| path |');
for i = 1:numel(ids)
    fprintf(fid, ' %s |', char(ids(i)));
end
fprintf(fid, '\n|---|');
for i = 1:numel(ids)
    fprintf(fid, '---:|');
end
fprintf(fid, '\n');
for p = 1:numel(paths)
    fprintf(fid, '| `%s` |', paths(p));
    for i = 1:numel(ids)
        mask = string(path_table.path_tag) == paths(p) & string(path_table.candidate_id) == ids(i);
        if any(mask)
            fprintf(fid, ' %.6f |', path_table.ey_rmse(find(mask, 1)));
        else
            fprintf(fid, ' NaN |');
        end
    end
    fprintf(fid, '\n');
end

fprintf(fid, '\n## Interpretation\n\n');
[~, best_idx] = min(candidate_table.max_ey_rmse);
best_id = string(candidate_table.candidate_id(best_idx));
fprintf(fid, '- Best max-route RMSE in this replay: `%s`.\n', best_id);
fprintf(fid, '- `legacy_maps_best` uses the historical BO maps from `data/models/maps_best.mat`, completed with the current map interface only where older fields are missing.\n');
fprintf(fid, '- `bo_frozen_base_initial` is the BO frozen/base initial controller from `Bayesian_Optimization.m` before any optimized Q/R/dR selection.\n');
fprintf(fid, '- `p0_selected` is the P0 candidate from the repaired oracle replay.\n');
end

function rows = local_empty_candidate_row()
rows = struct( ...
    'candidate_id', string(""), ...
    'label', string(""), ...
    'source_file', string(""), ...
    'status', string(""), ...
    'Np', NaN, 'Nc', NaN, ...
    'q_y', NaN, 'q_psi', NaN, 'q_v', NaN, 'q_omega', NaN, ...
    'r_F', NaN, 'r_omega', NaN, 'dR_F', NaN, 'dR_omega', NaN, ...
    'num_paths', NaN, 'total_fail_count', NaN, 'min_completion_ratio', NaN, ...
    'max_ey_rmse', NaN, 'mean_ey_rmse', NaN, 'max_ey_peak', NaN, ...
    'max_epsi_rmse', NaN, 'max_cons_Linf', NaN, ...
    'max_cons_violation_rate', NaN, 'max_F_sat_rate', NaN, ...
    'max_omega_sat_rate', NaN, 'mean_solve_avg_ms', NaN, ...
    'max_solve_max_ms', NaN, 'elapsed_sec', NaN, ...
    'pass_0p10', false, 'pass_0p05', false);
end

function rows = local_empty_path_row()
rows = struct( ...
    'candidate_id', string(""), ...
    'label', string(""), ...
    'path_tag', string(""), ...
    'path_file', string(""), ...
    'status', string(""), ...
    'message', string(""), ...
    'Np', NaN, 'Nc', NaN, ...
    'q_y', NaN, 'q_psi', NaN, 'q_v', NaN, 'q_omega', NaN, ...
    'r_F', NaN, 'r_omega', NaN, 'dR_F', NaN, 'dR_omega', NaN, ...
    'duration_s', NaN, 'n_samples', NaN, 'valid_steps', NaN, ...
    'completion_ratio', NaN, 'J', NaN, 'fail_count', NaN, ...
    'ey_rmse', NaN, 'ey_peak', NaN, 'epsi_rmse', NaN, 'epsi_peak', NaN, ...
    'ev_rmse', NaN, 'eomega_rmse', NaN, ...
    'cons_L1', NaN, 'cons_Linf', NaN, 'cons_violation_rate', NaN, ...
    'F_peak', NaN, 'omega_peak', NaN, 'F_sat_rate', NaN, ...
    'omega_sat_rate', NaN, 'solve_avg_ms', NaN, 'solve_max_ms', NaN, ...
    'first_fail_step', NaN, 'first_fail_reason', string(""), ...
    'first_fail_qpcode', string(""), 'elapsed_sec', NaN);
end

function paths = local_full_route_paths(root)
names = { ...
    'path_closed_loop_long_updown_theta10_v1.mat'
    'path_closed_loop_sharp_turn_transition_theta10_v1.mat'
    'path_factory_logistics_showcase_theta10_v10.mat'
    'path_factory_logistics_showcase_theta10_v3.mat'
    'path_industrial_lite.mat'
    'path_modern_tcn_demo_loop_v1.mat'
    'path_modern_tcn_demo_loop_v2.mat'};
paths = cell(numel(names), 1);
for i = 1:numel(names)
    paths{i} = fullfile(root, 'data', 'paths', names{i});
end
end

function zones = local_ref_zones(ref)
if isfield(ref, 'meta') && isfield(ref.meta, 'zones') && isstruct(ref.meta.zones)
    zones = ref.meta.zones;
else
    zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
end
end

function tau = local_map_tau(maps)
if isfield(maps, 'tau') && ~isempty(maps.tau) && isfinite(maps.tau)
    tau = maps.tau;
else
    tau = 0.35;
end
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

function txt = local_vec(x)
txt = strjoin(arrayfun(@(v) sprintf('%.6g', v), x(:).', 'UniformOutput', false), ', ');
txt = ['[', txt, ']'];
end

function txt = local_md_escape(txt)
txt = strrep(txt, '|', '\|');
end
