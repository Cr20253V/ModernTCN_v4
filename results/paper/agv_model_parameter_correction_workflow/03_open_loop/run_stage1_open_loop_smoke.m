function result = run_stage1_open_loop_smoke(cfg)
%RUN_STAGE1_OPEN_LOOP_SMOKE Minimal open-loop checks for the plantfix plant.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end
if exist('init_project', 'file') == 2
    init_project();
end

root = project_root();
node_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '03_open_loop');
if exist(node_dir, 'dir') ~= 7
    mkdir(node_dir);
end
if ~isfield(cfg, 'duration_sec') || isempty(cfg.duration_sec); cfg.duration_sec = 8.0; end
if ~isfield(cfg, 'beta_limit_deg') || isempty(cfg.beta_limit_deg); cfg.beta_limit_deg = 12.0; end
if ~isfield(cfg, 'omega_limit') || isempty(cfg.omega_limit); cfg.omega_limit = 2.5; end

params = parameters();
plant = agv_plant_revision(params);
cases = local_cases();
rows = repmat(local_row(), numel(cases), 1);
traces = struct();

for i = 1:numel(cases)
    c = cases(i);
    [t, x, u, theta] = local_sim_case(c, params, cfg.duration_sec);
    finite_ok = all(isfinite(t(:))) && all(isfinite(x(:))) && ...
        all(isfinite(u(:))) && all(isfinite(theta(:)));
    beta_peak_deg = max(abs(rad2deg(x(:, 8))));
    omega_peak = max(abs(x(:, 5)));
    v_min = min(x(:, 4));
    v_max = max(x(:, 4));
    pass = finite_ok && beta_peak_deg <= cfg.beta_limit_deg && ...
        omega_peak <= cfg.omega_limit && v_min > -0.05 && v_max < 3.0;

    rows(i).case_name = string(c.name);
    rows(i).theta_deg = rad2deg(c.theta);
    rows(i).omega_cmd = c.omega_cmd;
    rows(i).force_cmd = c.target_v;
    rows(i).finite_ok = finite_ok;
    rows(i).beta_peak_deg = beta_peak_deg;
    rows(i).omega_peak = omega_peak;
    rows(i).v_min = v_min;
    rows(i).v_max = v_max;
    rows(i).pass = pass;
    traces.(c.name) = struct('t', t, 'x', x, 'u', u, 'theta', theta);
end

T = struct2table(rows);
result = struct();
result.timestamp = char(datetime('now', 'Format', 'yyyy-MM-dd HH:mm:ss'));
result.plant_revision = plant;
result.cfg = cfg;
result.table = T;
result.pass = all(T.pass);
result.traces = traces;

writetable(T, fullfile(node_dir, 'stage1_open_loop_smoke_summary.csv'));
save(fullfile(node_dir, 'stage1_open_loop_smoke_result.mat'), 'result', '-v7.3');
local_write_report(node_dir, result);

if ~result.pass
    error('stage1_open_loop:Failed', 'Open-loop smoke failed. See stage1_open_loop_smoke_report.md.');
end
fprintf('[stage1 open-loop] PASS: %s\n', fullfile(node_dir, 'stage1_open_loop_smoke_report.md'));
end

function cases = local_cases()
cases = repmat(struct('name', '', 'target_v', 0, 'omega_cmd', 0, 'theta', 0), 4, 1);
cases(1) = struct('name', 'straight_flat', 'target_v', 0.8, 'omega_cmd', 0.00, 'theta', 0);
cases(2) = struct('name', 'turn_flat', 'target_v', 0.8, 'omega_cmd', 0.18, 'theta', 0);
cases(3) = struct('name', 'straight_slope', 'target_v', 0.8, 'omega_cmd', 0.00, 'theta', deg2rad(6));
cases(4) = struct('name', 'turn_slope', 'target_v', 0.8, 'omega_cmd', -0.18, 'theta', deg2rad(-6));
end

function [t, x_hist, u_hist, theta_hist] = local_sim_case(c, params, duration_sec)
Ts = params.Ts;
t = (0:Ts:duration_sec)';
x_hist = zeros(numel(t), 8);
x_hist(1, 4) = 0.6;
u_hist = zeros(numel(t), 2);
theta_hist = c.theta * ones(numel(t), 1);
for k = 1:numel(t)-1
    u = [local_force_for_speed_hold(x_hist(k, 4), c.target_v, c.theta, params); c.omega_cmd];
    x_hist(k+1, :) = state_eq(x_hist(k, :)', u, c.theta, params)';
    u_hist(k, :) = u';
end
last_idx = max(1, size(u_hist, 1) - 1);
u_hist(end, :) = u_hist(last_idx, :);
end

function row = local_row()
row = struct('case_name', "", 'theta_deg', NaN, 'omega_cmd', NaN, ...
    'force_cmd', NaN, 'finite_ok', false, 'beta_peak_deg', NaN, ...
    'omega_peak', NaN, 'v_min', NaN, 'v_max', NaN, 'pass', false);
end

function F_cmd = local_force_for_speed_hold(v, v_target, theta, params)
m = params.mass;
g = params.gravity;
c_r = params.rolling_resistance;
rho_air = params.air_density;
CdA = params.drag_coefficient_area;
r_wheel = params.wheel_radius;
n_gear = params.gear_ratio;
Jw = params.wheel_inertia;
Jm = params.motor_inertia;
m_eff = m + 2 * (Jw + Jm * n_gear^2) / max(r_wheel^2, 1e-6);
F_rolling = c_r * m * g * cos(theta);
F_aero = 0.5 * rho_air * CdA * max(v, 0)^2;
F_slope = m * g * sin(theta);
K_v = 1.2;
F_cmd = F_rolling + F_aero + F_slope + m_eff * K_v * (v_target - v);
F_cmd = min(max(F_cmd, -600), 600);
end

function local_write_report(node_dir, result)
file = fullfile(node_dir, 'stage1_open_loop_smoke_report.md');
fid = fopen(file, 'w');
if fid < 0; return; end
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# Stage 1 Open-Loop Smoke Report\n\n');
fprintf(fid, '- plant_revision: `%s`\n', result.plant_revision.id);
fprintf(fid, '- pass: `%d`\n\n', double(result.pass));
fprintf(fid, '| case | pass | beta peak deg | omega peak | v min | v max |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|\n');
for i = 1:height(result.table)
    fprintf(fid, '| `%s` | %d | %.4f | %.4f | %.4f | %.4f |\n', ...
        result.table.case_name(i), double(result.table.pass(i)), ...
        result.table.beta_peak_deg(i), result.table.omega_peak(i), ...
        result.table.v_min(i), result.table.v_max(i));
end
fprintf(fid, '\nNo NaN/Inf, bounded beta, bounded omega, and plausible velocity are required before full raw regeneration.\n');
end
