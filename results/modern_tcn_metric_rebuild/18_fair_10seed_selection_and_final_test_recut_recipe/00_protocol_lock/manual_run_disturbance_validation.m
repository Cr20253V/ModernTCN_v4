% Manual MATLAB disturbance validation entrypoint

init_project;
cfg = struct();
cfg.path_split = 'disturbance_validation';
cfg.reuse_existing = true;
cfg.disturbance_mode = 'hybrid';
cfg.disturbance_seed = 20260625;
cfg.disturbance_levels = [0, 1, 2];
run_fair10_closed_loop(cfg);
