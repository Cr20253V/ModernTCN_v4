% Manual MATLAB final test entrypoint

init_project;
cfg = struct();
cfg.path_split = 'final_test';
cfg.reuse_existing = true;
run_fair10_closed_loop(cfg);
