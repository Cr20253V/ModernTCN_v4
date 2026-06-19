function result = run_p0_oracle_mpc_retuning(cfg)
%RUN_P0_ORACLE_MPC_RETUNING Retune oracle-slope LPV-MPC before Node 7.
%
% P0 scope:
%   - Tune/validate oracle-slope LPV-MPC on existing route MAT files.
%   - Do not regenerate training data.
%   - Do not overwrite canonical data/models/maps_best.mat.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();

timestamp = datestr(now, 'yyyymmdd_HHMMSS');
base_out_dir = local_cfg(cfg, 'out_dir', fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '06_mpc_retuning'));
run_dir = local_cfg(cfg, 'run_dir', fullfile(base_out_dir, ...
    ['p0_oracle_retuning_' timestamp]));
local_ensure_dir(run_dir);

mode = string(local_cfg(cfg, 'mode', 'all'));
target_rmse = local_cfg(cfg, 'target_ey_rmse', 0.10);
ideal_rmse = local_cfg(cfg, 'ideal_ey_rmse', 0.05);

db_file = local_cfg(cfg, 'db_file', fullfile(root, 'data', 'models', 'lin_agv_db.mat'));
maps_file = local_cfg(cfg, 'maps_file', fullfile(base_out_dir, ...
    'maps_best_agv_physics_v2_node06.mat'));
Sdb = load(db_file);
if isfield(Sdb, 'db')
    db = Sdb.db;
else
    db = Sdb;
end
Smaps = load(maps_file);
if ~isfield(Smaps, 'maps_best')
    error('p0_oracle:MissingMapsBest', 'Missing maps_best in %s.', maps_file);
end
base_maps = Smaps.maps_best;
node06 = local_node06_cfg(base_maps);

paths = local_paths(root);
rep_paths = local_cfg(cfg, 'representative_path_files', paths.representative);
all_paths = local_cfg(cfg, 'all_path_files', paths.all);

fprintf('\n[p0-oracle] run_dir: %s\n', run_dir);
fprintf('[p0-oracle] mode: %s\n', mode);
fprintf('[p0-oracle] db: %s\n', db_file);
fprintf('[p0-oracle] maps: %s\n', maps_file);
fprintf('[p0-oracle] representative paths: %d, all paths: %d\n\n', ...
    numel(rep_paths), numel(all_paths));

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.objective = 'P0 oracle-slope MPC retuning before Node 7';
result.node7_status = 'skipped';
result.run_dir = run_dir;
result.db_file = db_file;
result.maps_file = maps_file;
result.target_ey_rmse = target_rmse;
result.ideal_ey_rmse = ideal_rmse;
result.representative_path_files = rep_paths;
result.all_path_files = all_paths;
result.stageA = [];
result.stageB = [];
result.stageC = [];
result.stageB_gate = [];

if mode == "smoke"
    smoke_candidate = local_candidate('smoke_np60_nc15', "smoke", 60, 15, ...
        node06.Q, node06.R, node06.dR, node06.R(1), node06.dR(1));
    smoke_paths = rep_paths(1);
    stage = local_run_candidate_set("smoke", smoke_candidate, smoke_paths, ...
        db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg);
    result.smoke = stage;
    local_write_master_report(result);
    save(fullfile(run_dir, 'p0_oracle_retuning_result.mat'), 'result', '-v7.3');
    return;
end

stageA_candidates = local_stageA_candidates(node06, cfg);
result.stageA = local_run_candidate_set("stageA", stageA_candidates, rep_paths, ...
    db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg);
best_stageA = local_best_candidate(result.stageA.candidate_table);

if local_candidate_passes(best_stageA, target_rmse) || mode == "stageA"
    final_candidates = local_candidate_from_table(best_stageA, "stageA_final", node06);
else
    stageB_candidates = local_stageB_candidates(best_stageA, cfg);
    if mode == "stageB_fast" || local_cfg(cfg, 'stageB_fast', false)
        if isfield(cfg, 'stageB_gate_path_files') && ~isempty(cfg.stageB_gate_path_files)
            gate_paths = cfg.stageB_gate_path_files;
        else
            gate_paths = rep_paths(min(2, numel(rep_paths)));
        end
        result.stageB_gate = local_run_candidate_set("stageB_gate", stageB_candidates, gate_paths, ...
            db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg);
        gate_top_n = local_cfg(cfg, 'stageB_gate_top_n', 12);
        gateTop = local_top_candidates(result.stageB_gate.candidate_table, gate_top_n);
        stageB_candidates = local_candidates_from_table(gateTop, "stageB_gate_top", node06);
    end
    result.stageB = local_run_candidate_set("stageB", stageB_candidates, rep_paths, ...
        db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg);
    top_n = local_cfg(cfg, 'stageC_top_n', 5);
    topB = local_top_candidates(result.stageB.candidate_table, top_n);
    final_candidates = local_candidates_from_table(topB, "stageB_top", node06);
end

if mode ~= "stageA" && ~isempty(final_candidates)
    result.stageC = local_run_candidate_set("stageC", final_candidates, all_paths, ...
        db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg);
    best_final = local_best_candidate(result.stageC.candidate_table);
    result.best = best_final;
    local_save_best_maps(best_final, base_maps, run_dir);
else
    result.best = best_stageA;
end

local_write_master_report(result);
save(fullfile(run_dir, 'p0_oracle_retuning_result.mat'), 'result', '-v7.3');

fprintf('\n[p0-oracle] done: %s\n', run_dir);
fprintf('[p0-oracle] report: %s\n', fullfile(run_dir, 'p0_oracle_retuning_report.md'));
end

function stage = local_run_candidate_set(stage_name, candidates, path_files, db, base_maps, node06, run_dir, target_rmse, ideal_rmse, cfg)
stage_dir = fullfile(run_dir, char(stage_name));
local_ensure_dir(stage_dir);
candidate_rows = repmat(local_empty_candidate_row(), numel(candidates), 1);
path_rows = repmat(local_empty_path_row(), 0, 1);
stage_reports = struct();

for i = 1:numel(candidates)
    candidate = candidates(i);
    fprintf('[p0-oracle:%s] candidate %d/%d %s Np=%d Nc=%d\n', ...
        stage_name, i, numel(candidates), candidate.id, candidate.Np, candidate.Nc);
    t0 = tic;
    try
        [one_path_rows, one_reports] = local_eval_candidate(candidate, path_files, ...
            db, base_maps, node06, cfg);
        cand_row = local_aggregate_candidate(candidate, one_path_rows, toc(t0), ...
            target_rmse, ideal_rmse);
        path_rows = [path_rows; one_path_rows(:)]; %#ok<AGROW>
        stage_reports.(matlab.lang.makeValidName(candidate.id)) = one_reports;
    catch ME
        cand_row = local_candidate_error_row(candidate, toc(t0), ME);
    end
    candidate_rows(i) = cand_row;
    local_write_stage_files(stage_dir, stage_name, candidate_rows(1:i), path_rows, stage_reports);
    fprintf('[p0-oracle:%s] %s status=%s max_ey=%.6g mean_ey=%.6g fail=%g\n', ...
        stage_name, candidate.id, cand_row.status, cand_row.max_ey_rmse, ...
        cand_row.mean_ey_rmse, cand_row.total_fail_count);
end

stage = struct();
stage.stage_name = char(stage_name);
stage.stage_dir = stage_dir;
stage.candidate_table = struct2table(candidate_rows);
stage.path_table = struct2table(path_rows);
stage.reports = stage_reports;
stage.candidate_file = fullfile(stage_dir, [char(stage_name) '_candidate_summary.csv']);
stage.path_file = fullfile(stage_dir, [char(stage_name) '_path_summary.csv']);
stage.mat_file = fullfile(stage_dir, [char(stage_name) '_result.mat']);
local_write_stage_report(stage, target_rmse, ideal_rmse);
end

function [path_rows, reports] = local_eval_candidate(candidate, path_files, db, base_maps, node06, cfg)
ctrl = local_build_ctrl(candidate, db, base_maps, node06);
params = parameters();
path_rows = repmat(local_empty_path_row(), numel(path_files), 1);
reports = struct();

for p = 1:numel(path_files)
    path_file = path_files{p};
    [~, path_tag] = fileparts(path_file);
    row = local_empty_path_row();
    row.candidate_id = string(candidate.id);
    row.stage = candidate.stage;
    row.path_tag = string(path_tag);
    row.path_file = string(path_file);
    row.Np = candidate.Np;
    row.Nc = candidate.Nc;
    row.q_y = candidate.Q(1);
    row.q_psi = candidate.Q(2);
    row.q_v = candidate.Q(3);
    row.q_omega = candidate.Q(4);
    row.r_scalar = candidate.r_scalar;
    row.dr_scalar = candidate.dr_scalar;
    t0 = tic;
    try
        Sref = load(path_file, 'ref');
        ref = Sref.ref;
        zones = local_ref_zones(ref);
        cfg_one = struct();
        cfg_one.ctrl = ctrl;
        cfg_one.ctrl_maps = ctrl.maps;
        cfg_one.path_file = path_file;
        cfg_one.zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
        cfg_one.report_zones = zones;
        cfg_one.tau = local_cfg(cfg, 'tau', 0.35);
        cfg_one.ey_max = 1.0;
        cfg_one.epsi_max = 0.5;
        cfg_one.ev_max = 0.5;
        cfg_one.eomega_max = 0.3;
        cfg_one.dF_max = 400;
        cfg_one.dw_max = 0.9;
        cfg_one.debug = local_cfg(cfg, 'debug', false);
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
    end
    row.elapsed_sec = toc(t0);
    path_rows(p) = row;
end
end

function ctrl = local_build_ctrl(candidate, db, base_maps, node06)
opts = struct();
opts.Np = candidate.Np;
opts.Nc = candidate.Nc;
opts.Q = candidate.Q;
opts.R = candidate.R;
opts.dR = candidate.dR;
opts.umin = [-600; -1.2];
opts.umax = [600; 1.2];
opts.dumin = [-400; -0.9];
opts.dumax = [400; 0.9];
opts.ymin = [-1.0; -0.5; -0.5; -0.3];
opts.ymax = [1.0; 0.5; 0.5; 0.3];
opts.soft_weight_pos = local_cfg(node06, 'soft_weight_pos', 3e3);
opts.soft_weight_yaw = local_cfg(node06, 'soft_weight_yaw', 3e3);
evalc('ctrl = mpc_setup_single_interp(db, opts);');
maps = base_maps;
maps.Q_range = [candidate.Q * 0.5; candidate.Q * 1.5];
maps.R_range = [candidate.R * 0.5; candidate.R * 1.5];
maps.dR_range = [candidate.dR * 0.5; candidate.dR * 1.5];
maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];
maps.node06_best_cfg = rmfield_if_exists(node06, {'soft_weight_pos', 'soft_weight_yaw'});
maps.p0_candidate_cfg = struct('id', candidate.id, 'stage', candidate.stage, ...
    'Np', candidate.Np, 'Nc', candidate.Nc, 'Q', candidate.Q, ...
    'R', candidate.R, 'dR', candidate.dR);
ctrl.maps = maps;
end

function candidates = local_stageA_candidates(node06, cfg)
Np_grid = local_cfg(cfg, 'Np_grid', [60, 80, 100]);
Nc_grid = local_cfg(cfg, 'Nc_grid', [15, 20]);
candidates = repmat(local_candidate('', "stageA", NaN, NaN, node06.Q, node06.R, node06.dR, NaN, NaN), 0, 1);
for i = 1:numel(Np_grid)
    for j = 1:numel(Nc_grid)
        id = sprintf('stageA_np%d_nc%d', Np_grid(i), Nc_grid(j));
        candidates(end + 1) = local_candidate(id, "stageA", Np_grid(i), Nc_grid(j), ...
            node06.Q, node06.R, node06.dR, node06.R(1), node06.dR(1)); %#ok<AGROW>
    end
end
end

function candidates = local_stageB_candidates(best_stageA, cfg)
q_y_grid = local_cfg(cfg, 'q_y_grid', [50, 100, 200, 400]);
q_psi_grid = local_cfg(cfg, 'q_psi_grid', [50, 100, 200]);
q_v_grid = local_cfg(cfg, 'q_v_grid', [5, 15, 40]);
q_omega_grid = local_cfg(cfg, 'q_omega_grid', [1, 3, 8]);
r_grid = local_cfg(cfg, 'R_grid', [1e-4, 3e-4, 1e-3]);
dr_grid = local_cfg(cfg, 'dR_grid', [1e-3, 3e-3, 1e-2, 3e-2]);
max_candidates = local_cfg(cfg, 'stageBMaxCandidates', Inf);
candidates = repmat(local_candidate('', "stageB", NaN, NaN, [0 0 0 0], [0 0], [0 0], NaN, NaN), 0, 1);
count = 0;
for a = 1:numel(q_y_grid)
    for b = 1:numel(q_psi_grid)
        for c = 1:numel(q_v_grid)
            for d = 1:numel(q_omega_grid)
                for e = 1:numel(r_grid)
                    for f = 1:numel(dr_grid)
                        count = count + 1;
                        if count > max_candidates
                            return;
                        end
                        Q = [q_y_grid(a), q_psi_grid(b), q_v_grid(c), q_omega_grid(d)];
                        R = [r_grid(e), r_grid(e)];
                        dR = [dr_grid(f), dr_grid(f)];
                        id = sprintf('stageB_%04d_np%d_nc%d_q%g_%g_%g_%g_r%g_dr%g', ...
                            count, best_stageA.Np, best_stageA.Nc, Q(1), Q(2), Q(3), Q(4), R(1), dR(1));
                        candidates(end + 1) = local_candidate(id, "stageB", best_stageA.Np, best_stageA.Nc, ...
                            Q, R, dR, r_grid(e), dr_grid(f)); %#ok<AGROW>
                    end
                end
            end
        end
    end
end
end

function c = local_candidate(id, stage, Np, Nc, Q, R, dR, r_scalar, dr_scalar)
c = struct();
c.id = char(id);
c.stage = string(stage);
c.Np = Np;
c.Nc = Nc;
c.Q = Q;
c.R = R;
c.dR = dR;
c.r_scalar = r_scalar;
c.dr_scalar = dr_scalar;
end

function row = local_aggregate_candidate(candidate, path_rows, elapsed_sec, target_rmse, ideal_rmse)
row = local_empty_candidate_row();
row.candidate_id = string(candidate.id);
row.stage = candidate.stage;
row.status = "ok";
row.Np = candidate.Np;
row.Nc = candidate.Nc;
row.q_y = candidate.Q(1);
row.q_psi = candidate.Q(2);
row.q_v = candidate.Q(3);
row.q_omega = candidate.Q(4);
row.r_scalar = candidate.r_scalar;
row.dr_scalar = candidate.dr_scalar;
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
row.pass_0p10 = row.total_fail_count == 0 && row.min_completion_ratio >= 1 && row.max_ey_rmse < target_rmse;
row.pass_0p05 = row.total_fail_count == 0 && row.min_completion_ratio >= 1 && row.max_ey_rmse < ideal_rmse;
row.sort_key_fail = double(~row.pass_0p10);
end

function row = local_candidate_error_row(candidate, elapsed_sec, ME)
row = local_empty_candidate_row();
row.candidate_id = string(candidate.id);
row.stage = candidate.stage;
row.status = "error";
row.message = string(ME.message);
row.Np = candidate.Np;
row.Nc = candidate.Nc;
row.q_y = candidate.Q(1);
row.q_psi = candidate.Q(2);
row.q_v = candidate.Q(3);
row.q_omega = candidate.Q(4);
row.r_scalar = candidate.r_scalar;
row.dr_scalar = candidate.dr_scalar;
row.elapsed_sec = elapsed_sec;
row.sort_key_fail = 1;
end

function row = local_empty_candidate_row()
row = struct('candidate_id', "", 'stage', "", 'status', "pending", 'message', "", ...
    'Np', NaN, 'Nc', NaN, 'q_y', NaN, 'q_psi', NaN, 'q_v', NaN, 'q_omega', NaN, ...
    'r_scalar', NaN, 'dr_scalar', NaN, 'num_paths', NaN, 'total_fail_count', NaN, ...
    'min_completion_ratio', NaN, 'max_ey_rmse', NaN, 'mean_ey_rmse', NaN, ...
    'max_ey_peak', NaN, 'max_epsi_rmse', NaN, 'max_cons_Linf', NaN, ...
    'max_cons_violation_rate', NaN, 'max_F_sat_rate', NaN, 'max_omega_sat_rate', NaN, ...
    'mean_solve_avg_ms', NaN, 'max_solve_max_ms', NaN, 'pass_0p10', false, ...
    'pass_0p05', false, 'sort_key_fail', 1, 'elapsed_sec', NaN);
end

function row = local_empty_path_row()
row = struct('candidate_id', "", 'stage', "", 'path_tag', "", 'path_file', "", ...
    'status', "pending", 'message', "", 'Np', NaN, 'Nc', NaN, ...
    'q_y', NaN, 'q_psi', NaN, 'q_v', NaN, 'q_omega', NaN, ...
    'r_scalar', NaN, 'dr_scalar', NaN, 'duration_s', NaN, 'n_samples', NaN, ...
    'valid_steps', NaN, 'completion_ratio', NaN, 'J', NaN, 'fail_count', NaN, ...
    'ey_rmse', NaN, 'ey_peak', NaN, 'epsi_rmse', NaN, 'epsi_peak', NaN, ...
    'ev_rmse', NaN, 'eomega_rmse', NaN, 'cons_L1', NaN, 'cons_Linf', NaN, ...
    'cons_violation_rate', NaN, 'F_peak', NaN, 'omega_peak', NaN, ...
    'F_sat_rate', NaN, 'omega_sat_rate', NaN, 'solve_avg_ms', NaN, ...
    'solve_max_ms', NaN, 'first_fail_step', NaN, 'first_fail_reason', "", ...
    'first_fail_qpcode', "", 'elapsed_sec', NaN);
end

function local_write_stage_files(stage_dir, stage_name, candidate_rows, path_rows, stage_reports)
candidate_table = struct2table(candidate_rows);
path_table = struct2table(path_rows);
writetable(candidate_table, fullfile(stage_dir, [char(stage_name) '_candidate_summary.csv']));
writetable(path_table, fullfile(stage_dir, [char(stage_name) '_path_summary.csv']));
save(fullfile(stage_dir, [char(stage_name) '_result.mat']), ...
    'candidate_table', 'path_table', 'stage_reports', '-v7.3');
end

function local_write_stage_report(stage, target_rmse, ideal_rmse)
report_file = fullfile(stage.stage_dir, [stage.stage_name '_report.md']);
T = stage.candidate_table;
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# P0 Oracle Retuning %s\n\n', stage.stage_name);
fprintf(fid, '- Target: `max e_y RMSE < %.3f m`\n', target_rmse);
fprintf(fid, '- Ideal: `max e_y RMSE < %.3f m`\n\n', ideal_rmse);
fprintf(fid, '| candidate | status | Np | Nc | max e_y RMSE | mean e_y RMSE | max e_y peak | max cons Linf | fail | pass <0.1 | pass <0.05 | elapsed s |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n');
for i = 1:height(T)
    fprintf(fid, '| `%s` | %s | %.0f | %.0f | %.6g | %.6g | %.6g | %.6g | %.0f | %.0f | %.0f | %.1f |\n', ...
        T.candidate_id(i), T.status(i), T.Np(i), T.Nc(i), T.max_ey_rmse(i), ...
        T.mean_ey_rmse(i), T.max_ey_peak(i), T.max_cons_Linf(i), ...
        T.total_fail_count(i), T.pass_0p10(i), T.pass_0p05(i), T.elapsed_sec(i));
end
end

function local_write_master_report(result)
report_file = fullfile(result.run_dir, 'p0_oracle_retuning_report.md');
fid = fopen(report_file, 'w');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# P0 Oracle-MPC Ceiling Repair Report\n\n');
fprintf(fid, '- Timestamp: `%s`\n', result.timestamp);
fprintf(fid, '- Node 7 status: `%s`\n', result.node7_status);
fprintf(fid, '- Target: `max e_y RMSE < %.3f m`; ideal `< %.3f m`\n', ...
    result.target_ey_rmse, result.ideal_ey_rmse);
fprintf(fid, '- Run directory: `%s`\n\n', result.run_dir);

local_write_master_stage(fid, 'Stage A', result.stageA);
if isfield(result, 'stageB_gate')
    local_write_master_stage(fid, 'Stage B gate', result.stageB_gate);
end
local_write_master_stage(fid, 'Stage B', result.stageB);
local_write_master_stage(fid, 'Stage C', result.stageC);

if isfield(result, 'best') && ~isempty(result.best)
    b = result.best;
    fprintf(fid, '\n## Decision\n\n');
    fprintf(fid, '- Best candidate: `%s`\n', b.candidate_id);
    fprintf(fid, '- Max e_y RMSE: `%.6g m`\n', b.max_ey_rmse);
    fprintf(fid, '- Mean e_y RMSE: `%.6g m`\n', b.mean_ey_rmse);
    fprintf(fid, '- Fail count: `%.0f`\n', b.total_fail_count);
    if b.pass_0p10
        fprintf(fid, '- Verdict: PASS. Node 7 may proceed after Simulink-entry synchronization.\n');
    else
        fprintf(fid, '- Verdict: FAIL. Do not enter Node 7; oracle ceiling is still above 0.1 m.\n');
    end
end
end

function local_write_master_stage(fid, title, stage)
if isempty(stage)
    return;
end
fprintf(fid, '## %s\n\n', title);
T = stage.candidate_table;
if isempty(T)
    fprintf(fid, '- No candidates were run.\n\n');
    return;
end
best = local_best_candidate(T);
fprintf(fid, '- Candidates: `%d`\n', height(T));
fprintf(fid, '- Best: `%s`, max e_y RMSE `%.6g m`, pass<0.1=`%d`\n', ...
    best.candidate_id, best.max_ey_rmse, best.pass_0p10);
fprintf(fid, '- Candidate CSV: `%s`\n', stage.candidate_file);
fprintf(fid, '- Path CSV: `%s`\n\n', stage.path_file);
end

function local_save_best_maps(best, base_maps, run_dir)
maps_best = base_maps;
maps_best.Q_range = [[best.q_y, best.q_psi, best.q_v, best.q_omega] * 0.5; ...
    [best.q_y, best.q_psi, best.q_v, best.q_omega] * 1.5];
R = [best.r_scalar, best.r_scalar];
dR = [best.dr_scalar, best.dr_scalar];
if any(isnan(R))
    R = mean(base_maps.R_range, 1);
end
if any(isnan(dR))
    dR = mean(base_maps.dR_range, 1);
end
maps_best.R_range = [R * 0.5; R * 1.5];
maps_best.dR_range = [dR * 0.5; dR * 1.5];
maps_best.version = 'agv_physics_v2_p0_oracle';
maps_best.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
maps_best.p0_best = best;
save(fullfile(run_dir, 'maps_best_agv_physics_v2_p0_oracle.mat'), 'maps_best');
end

function best = local_best_candidate(T)
if isempty(T)
    best = [];
    return;
end
T = sortrows(T, {'sort_key_fail', 'max_ey_rmse', 'mean_ey_rmse', ...
    'max_cons_Linf', 'max_F_sat_rate', 'max_omega_sat_rate', 'mean_solve_avg_ms'});
best = T(1, :);
best = table2struct(best);
end

function rows = local_top_candidates(T, n)
T = sortrows(T, {'sort_key_fail', 'max_ey_rmse', 'mean_ey_rmse', ...
    'max_cons_Linf', 'max_F_sat_rate', 'max_omega_sat_rate', 'mean_solve_avg_ms'});
rows = T(1:min(n, height(T)), :);
end

function tf = local_candidate_passes(row, target_rmse)
tf = ~isempty(row) && row.total_fail_count == 0 && row.min_completion_ratio >= 1 && row.max_ey_rmse < target_rmse;
end

function c = local_candidate_from_table(row, id_suffix, node06)
if istable(row)
    row = table2struct(row);
end
if nargin < 3 || ~isstruct(node06)
    node06 = struct('R', [NaN, NaN], 'dR', [NaN, NaN]);
end
r_scalar = row.r_scalar;
dr_scalar = row.dr_scalar;
if isnan(r_scalar)
    r_scalar = node06.R(1);
end
if isnan(dr_scalar)
    dr_scalar = node06.dR(1);
end
c = local_candidate(sprintf('%s_%s', char(row.candidate_id), id_suffix), "stageC", ...
    row.Np, row.Nc, [row.q_y, row.q_psi, row.q_v, row.q_omega], ...
    local_scalar_pair(r_scalar), local_scalar_pair(dr_scalar), r_scalar, dr_scalar);
end

function candidates = local_candidates_from_table(T, id_suffix, node06)
if nargin < 3
    node06 = struct();
end
candidates = repmat(local_candidate('', "stageC", NaN, NaN, [0 0 0 0], [0 0], [0 0], NaN, NaN), 0, 1);
for i = 1:height(T)
    candidates(end + 1) = local_candidate_from_table(T(i, :), sprintf('%s_%02d', id_suffix, i), node06); %#ok<AGROW>
end
end

function x = local_scalar_pair(v)
if isnan(v)
    x = [NaN, NaN];
else
    x = [v, v];
end
end

function zones = local_ref_zones(ref)
if isfield(ref, 'meta') && isfield(ref.meta, 'zones') && isstruct(ref.meta.zones)
    zones = ref.meta.zones;
else
    zones = struct('full_route', [ref.t(1), ref.t(end) + eps(ref.t(end))]);
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

function paths = local_paths(root)
names_rep = { ...
    'path_closed_loop_long_updown_theta10_v1.mat'
    'path_closed_loop_sharp_turn_transition_theta10_v1.mat'
    'path_industrial_lite.mat'};
rep = cell(numel(names_rep), 1);
for i = 1:numel(names_rep)
    rep{i} = fullfile(root, 'data', 'paths', names_rep{i});
end

files = dir(fullfile(root, 'data', 'paths', '*.mat'));
all = {};
for i = 1:numel(files)
    candidate = fullfile(files(i).folder, files(i).name);
    try
        S = load(candidate, 'ref');
        if isfield(S, 'ref') && isfield(S.ref, 'meta') && isfield(S.ref.meta, 'zones')
            all{end + 1, 1} = candidate; %#ok<AGROW>
        end
    catch
    end
end
paths = struct('representative', {rep}, 'all', {sort(all)});
end

function node06 = local_node06_cfg(base_maps)
if isfield(base_maps, 'node06_best_cfg')
    node06 = base_maps.node06_best_cfg;
else
    node06 = struct();
end
node06.Np = local_cfg(node06, 'Np', 30);
node06.Nc = local_cfg(node06, 'Nc', 10);
node06.Q = local_cfg(node06, 'Q', [15.293, 28.737, 5.076, 2.9918]);
node06.R = local_cfg(node06, 'R', [1e-3, 1e-3]);
node06.dR = local_cfg(node06, 'dR', [1e-2, 1e-2]);
node06.soft_weight_pos = local_cfg(node06, 'soft_weight_pos', 3e3);
node06.soft_weight_yaw = local_cfg(node06, 'soft_weight_yaw', 3e3);
end

function s = rmfield_if_exists(s, names)
for i = 1:numel(names)
    if isfield(s, names{i})
        s = rmfield(s, names{i});
    end
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

function local_ensure_dir(d)
if exist(d, 'dir') ~= 7
    mkdir(d);
end
end
