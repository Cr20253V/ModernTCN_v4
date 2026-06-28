% Manual MATLAB validation sentinel entrypoint

init_project;
cfg = struct();
cfg.path_split = 'validation_sentinel';
cfg.reuse_existing = true;
run_fair10_closed_loop(cfg);
