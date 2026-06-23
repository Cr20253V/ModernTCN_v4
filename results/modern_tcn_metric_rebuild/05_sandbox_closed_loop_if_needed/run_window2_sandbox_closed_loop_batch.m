try
    this_file = mfilename('fullpath');
    this_dir = fileparts(this_file);
    repo_root = this_dir;
    while exist(fullfile(repo_root, 'init_project.m'), 'file') ~= 2
        parent_dir = fileparts(repo_root);
        if strcmp(parent_dir, repo_root)
            error('window2_sandbox:ProjectRootNotFound', ...
                'Could not find init_project.m above %s.', this_dir);
        end
        repo_root = parent_dir;
    end
    cd(repo_root);
    addpath(repo_root);
    addpath(this_dir);
    cfg = struct();
    cfg.reuse_existing = false;
    run_window2_sandbox_closed_loop(cfg);
catch ME
    disp(getReport(ME, 'extended', 'hyperlinks', 'off'));
    exit(1);
end
exit(0);
