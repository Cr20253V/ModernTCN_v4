root = 'e:/Matlab/Simulink/S-Function_16';
addpath(root);
addpath(fullfile(root,'src'));
addpath(genpath(fullfile(root,'src')));

p1 = fullfile(root,'results','bo_results','phase1_best.mat');
p2 = fullfile(root,'results','bo_results','phase2_best.mat');

if ~exist(p1,'file'), error('missing phase1_best.mat'); end
if ~exist(p2,'file'), error('missing phase2_best.mat'); end

S1 = load(p1);
S2 = load(p2);

fprintf('=== phase1 fields ===\n'); disp(fieldnames(S1));
fprintf('=== phase2 fields ===\n'); disp(fieldnames(S2));

if isfield(S1,'maps_best')
  mb = S1.maps_best;
  fprintf('P1 maps_best.Q_range=\n'); disp(mb.Q_range);
  fprintf('P1 maps_best.R_range=\n'); disp(mb.R_range);
  fprintf('P1 maps_best.dR_range=\n'); disp(mb.dR_range);
end

if isfield(S2,'combined')
  c = S2.combined;
  fprintf('P2 combined fields=\n'); disp(fieldnames(c));
  if isfield(c,'omega_threshold'), fprintf('omega_threshold=%.12g\n', c.omega_threshold); end
  if isfield(c,'q_y_gain_max'), fprintf('q_y_gain_max=%.12g\n', c.q_y_gain_max); end
  if isfield(c,'theta_threshold'), fprintf('theta_threshold=%.12g\n', c.theta_threshold); end
  if isfield(c,'q_v_gain_max'), fprintf('q_v_gain_max=%.12g\n', c.q_v_gain_max); end
  if isfield(c,'R_F_gain_max_uphill'), fprintf('R_F_gain_max_uphill=%.12g\n', c.R_F_gain_max_uphill); end
  if isfield(c,'R_F_gain_max_downhill'), fprintf('R_F_gain_max_downhill=%.12g\n', c.R_F_gain_max_downhill); end
  if isfield(c,'dR_F_gain_max_uphill'), fprintf('dR_F_gain_max_uphill=%.12g\n', c.dR_F_gain_max_uphill); end
  if isfield(c,'dR_F_gain_max_downhill'), fprintf('dR_F_gain_max_downhill=%.12g\n', c.dR_F_gain_max_downhill); end
  if isfield(c,'transition_width'), fprintf('transition_width=%.12g\n', c.transition_width); end
  if isfield(c,'theta_transition_width'), fprintf('theta_transition_width=%.12g\n', c.theta_transition_width); end
  if isfield(c,'tau'), fprintf('tau=%.12g\n', c.tau); end
  if isfield(c,'Q_range'), fprintf('P2 combined.Q_range=\n'); disp(c.Q_range); end
  if isfield(c,'R_range'), fprintf('P2 combined.R_range=\n'); disp(c.R_range); end
  if isfield(c,'dR_range'), fprintf('P2 combined.dR_range=\n'); disp(c.dR_range); end
end

if isfield(S2,'maps_best')
  mb2 = S2.maps_best;
  fprintf('P2 maps_best fields=\n'); disp(fieldnames(mb2));
end
