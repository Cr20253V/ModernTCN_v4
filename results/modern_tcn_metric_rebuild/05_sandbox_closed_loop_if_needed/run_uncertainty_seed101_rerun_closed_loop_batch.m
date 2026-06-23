try
    this_file = mfilename('fullpath');
    this_dir = fileparts(this_file);
    repo_root = this_dir;
    while exist(fullfile(repo_root, 'init_project.m'), 'file') ~= 2
        parent_dir = fileparts(repo_root);
        if strcmp(parent_dir, repo_root)
            error('uncertainty_rerun:ProjectRootNotFound', ...
                'Could not find init_project.m above %s.', this_dir);
        end
        repo_root = parent_dir;
    end
    cd(repo_root);
    addpath(repo_root);
    addpath(this_dir);
    run_uncertainty_seed101_rerun_closed_loop();
catch ME
    disp(getReport(ME, 'extended', 'hyperlinks', 'off'));
    exit(1);
end
exit(0);
