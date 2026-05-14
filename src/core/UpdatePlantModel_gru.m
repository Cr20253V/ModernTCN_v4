function [plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax] = UpdatePlantModel_gru(rho, db_rt, MPC_idx, ff_rt, v_ff_nom, gru_vec)
%#codegen
% GRU-specific adaptive plant update for LPV-MPC.
% Interface:
%   gru_vec = [label_main; label_turn; conf_main]
%   label_main: 1=flat, 2=stall, 3=slope
%   label_turn: -1=right, 0=straight, 1=left
%   conf_main : [0,1]

unused = MPC_idx; %#ok<NASGU>
unused = v_ff_nom; %#ok<NASGU>

%% Persistent states
persistent rho_omega_lpf stall_on stall_on_cnt stall_off_cnt slope_on slope_on_cnt slope_off_cnt

if isempty(rho_omega_lpf)
    rho_omega_lpf = rho(2);
end

if isempty(stall_on)
    stall_on = false;
    stall_on_cnt = 0;
    stall_off_cnt = 0;
end

if isempty(slope_on)
    slope_on = false;
    slope_on_cnt = 0;
    slope_off_cnt = 0;
end

%% Runtime maps (same LPV/MPC baseline as tuned controller)
Q_range_bo = [ ...
65.5231, 8.1684, 18.3989, 0.4160; ...
196.5693, 24.5051, 55.1966, 1.2481];

R_range_bo = [ ...
0.0015, 0.0058; ...
0.0046, 0.0173];

dR_range_bo = [ ...
0.0017, 0.1309; ...
0.0050, 0.3927];

maps_local = struct( ...
    'enable_weight_interp', true, ...
    'Q_range', Q_range_bo, ...
    'R_range', R_range_bo, ...
    'dR_range', dR_range_bo, ...
    'alpha_Q', [0.5, 0.5, 0.5, 0.5], ...
    'beta_Q', [0.5, 0.5, 0.5, 0.5], ...
    'alpha_R', [0.5, 0.5], ...
    'beta_R', [0.5, 0.5], ...
    'alpha_dR', [0.5, 0.5], ...
    'beta_dR', [0.5, 0.5], ...
    'scale_umin_lo', [1, 1], ...
    'scale_umin_hi', [1, 1], ...
    'scale_umax_lo', [1, 1], ...
    'scale_umax_hi', [1, 1], ...
    'rho_min', [0.02; -1.2; -0.1745], ...
    'rho_max', [1.2; 1.2; 0.1745], ...
    'tau', 0.35, ...
    'omega_threshold', 0.139817184968, ...
    'q_y_gain_max', 5.54865433581, ...
    'transition_width', 0.03, ...
    'theta_threshold', 0.125151060428, ...
    'q_v_gain_max', 3.46559044719, ...
    'theta_transition_width', 0.02, ...
    'R_F_gain_max_uphill', 1.00755999315, ...
    'R_F_gain_max_downhill', 1.0, ...
    'dR_F_gain_max_uphill', 1.0, ...
    'dR_F_gain_max_downhill', 1.0, ...
    'umin_range', [-720, -1.44; -600, -1.2], ...
    'umax_range', [ 600, 1.2; 720, 1.44] ...
);

%% Additional omega LPF
Ts_upm = 0.01;
tau_omega = 0.25;
alpha_omg = Ts_upm / (Ts_upm + tau_omega);
rho_omega_lpf = alpha_omg * rho(2) + (1.0 - alpha_omg) * rho_omega_lpf;
rho_upd = [rho(1); rho_omega_lpf; rho(3)];

%% LPV interpolation
upd = mpc_update_from_rho(rho_upd, db_rt, maps_local);

%% Decode GRU labels
lbl_main = 1;
lbl_turn = 0;
conf_main = 1.0;

if nargin >= 6 && ~isempty(gru_vec)
    gv = double(gru_vec(:));
    if numel(gv) >= 1
        lbl_main = round(gv(1));
    end
    if numel(gv) >= 2
        if gv(2) > 0.5
            lbl_turn = 1;
        elseif gv(2) < -0.5
            lbl_turn = -1;
        else
            lbl_turn = 0;
        end
    end
    if numel(gv) >= 3
        conf_main = max(0.0, min(1.0, gv(3)));
    end
end

if lbl_main < 1 || lbl_main > 3
    lbl_main = 1;
end

%% Hysteresis on main label (lighter than Mamba due GRU dwell already enabled)
STALL_ON_THRESH = 10;
STALL_OFF_THRESH = 25;
SLOPE_ON_THRESH = 15;
SLOPE_OFF_THRESH = 35;

if lbl_main == 2 && conf_main >= 0.55
    stall_on_cnt = stall_on_cnt + 1;
    stall_off_cnt = 0;
    if stall_on_cnt >= STALL_ON_THRESH
        stall_on = true;
    end
else
    stall_off_cnt = stall_off_cnt + 1;
    stall_on_cnt = 0;
    if stall_off_cnt >= STALL_OFF_THRESH
        stall_on = false;
    end
end

if lbl_main == 3 && conf_main >= 0.55
    slope_on_cnt = slope_on_cnt + 1;
    slope_off_cnt = 0;
    if slope_on_cnt >= SLOPE_ON_THRESH
        slope_on = true;
    end
else
    slope_off_cnt = slope_off_cnt + 1;
    slope_on_cnt = 0;
    if slope_off_cnt >= SLOPE_OFF_THRESH
        slope_on = false;
    end
end

lbl_main_eff = lbl_main;
if stall_on
    lbl_main_eff = 2;
elseif slope_on && lbl_main_eff == 1
    lbl_main_eff = 3;
end

%% GRU-driven constraint shaping
% Stall: allow more traction command, but less aggressive than Mamba profile.
if lbl_main_eff == 2
    stall_f_scale = 1.25;
    upd.umin(1) = upd.umin(1) * stall_f_scale;
    upd.umax(1) = upd.umax(1) * stall_f_scale;
end

% Turn state from GRU/ModernTCN: apply a conservative flat-turn profile.
% Limit the intervention to flat-mode turns so occasional turn false positives
% on slope segments do not perturb slope handling. The current path is not
% omega-bound limited, so the primary control lever is a small tracking-weight
% bias rather than effort/slew reduction.
if abs(lbl_turn) == 1 && lbl_main_eff == 1
    turn_w_scale = 1.15;
    upd.umin(2) = upd.umin(2) * turn_w_scale;
    upd.umax(2) = upd.umax(2) * turn_w_scale;
    upd.Q(1) = upd.Q(1) * 1.30;   % e_y
    upd.Q(2) = upd.Q(2) * 1.05;   % e_psi
    upd.Q(4) = upd.Q(4) * 1.05;   % e_omega
end

% Low confidence fallback: avoid overreacting to uncertain class outputs.
if conf_main < 0.45
    upd.umin(1) = 0.9 * upd.umin(1);
    upd.umax(1) = 0.9 * upd.umax(1);
end

%% Assemble plant with MD column
nx = size(upd.A, 1);
ny = size(upd.C, 1);

plant.A = upd.A;
hasE = isfield(upd, 'E') && ~isempty(upd.E);
if hasE
    E_col = upd.E;
else
    E_col = zeros(nx, 1);
end

plant.B = [upd.B, E_col];
plant.C = upd.C;
plant.D = [upd.D, zeros(ny,1)];

% Gravity + rolling nominal feedforward
m_agv = ff_rt.m;
g_acc = ff_rt.g;
c_roll = ff_rt.c_r;
theta_meas = rho(3);
F_eq = m_agv * g_acc * (sin(theta_meas) + c_roll * cos(theta_meas));

plant.U = [F_eq; 0; 0];
plant.X = zeros(nx,1);
plant.Y = zeros(ny,1);
plant.DX = zeros(nx,1);
plant.Ts = db_rt.Ts;

%% MPC outputs
y_wt = upd.Q(:);
u_wt = upd.R(:);
du_wt = upd.dR(:);
ecr_wt = 1e4;
umin = upd.umin(:);
umax = upd.umax(:);

end
