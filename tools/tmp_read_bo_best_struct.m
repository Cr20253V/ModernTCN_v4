root = 'e:/Matlab/Simulink/S-Function_16';
p1 = fullfile(root,'results','bo_results','phase1_best.mat');
p2 = fullfile(root,'results','bo_results','phase2_best.mat');
S1 = load(p1); S2 = load(p2);

fprintf('=== S1.best fields ===\n'); disp(fieldnames(S1.best));
if isfield(S1.best,'ctrl_maps')
  cm = S1.best.ctrl_maps;
  fprintf('S1.best.ctrl_maps fields:\n'); disp(fieldnames(cm));
  if isfield(cm,'Q_range'), fprintf('Q_range=\n'); disp(cm.Q_range); end
  if isfield(cm,'R_range'), fprintf('R_range=\n'); disp(cm.R_range); end
  if isfield(cm,'dR_range'), fprintf('dR_range=\n'); disp(cm.dR_range); end
  if isfield(cm,'rho_min'), fprintf('rho_min=\n'); disp(cm.rho_min); end
  if isfield(cm,'rho_max'), fprintf('rho_max=\n'); disp(cm.rho_max); end
  f = {'tau','omega_threshold','q_y_gain_max','transition_width','theta_threshold','q_v_gain_max','theta_transition_width','R_F_gain_max_uphill','R_F_gain_max_downhill','dR_F_gain_max_uphill','dR_F_gain_max_downhill'};
  for i=1:numel(f)
    if isfield(cm,f{i}), fprintf('%s=%.12g\n', f{i}, cm.(f{i})); end
  end
end

fprintf('=== S2.best fields ===\n'); disp(fieldnames(S2.best));
if isfield(S2.best,'ctrl_maps')
  cm2 = S2.best.ctrl_maps;
  fprintf('S2.best.ctrl_maps fields:\n'); disp(fieldnames(cm2));
  if isfield(cm2,'Q_range'), fprintf('Q_range=\n'); disp(cm2.Q_range); end
  if isfield(cm2,'R_range'), fprintf('R_range=\n'); disp(cm2.R_range); end
  if isfield(cm2,'dR_range'), fprintf('dR_range=\n'); disp(cm2.dR_range); end
  f = {'tau','omega_threshold','q_y_gain_max','transition_width','theta_threshold','q_v_gain_max','theta_transition_width','R_F_gain_max_uphill','R_F_gain_max_downhill','dR_F_gain_max_uphill','dR_F_gain_max_downhill'};
  for i=1:numel(f)
    if isfield(cm2,f{i}), fprintf('%s=%.12g\n', f{i}, cm2.(f{i})); end
  end
end

fprintf('=== bestPoint S1 ===\n'); disp(S1.bestPoint);
fprintf('=== bestPoint S2 ===\n'); disp(S2.bestPoint);
