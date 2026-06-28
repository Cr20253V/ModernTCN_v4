try
    this_file = mfilename('fullpath');
    this_dir = fileparts(this_file);
    repo_root = this_dir;
    while exist(fullfile(repo_root, 'init_project.m'), 'file') ~= 2
        parent_dir = fileparts(repo_root);
        if strcmp(parent_dir, repo_root)
            error('manual_fill_baseline_lock:ProjectRootNotFound', ...
                'Could not find init_project.m above %s.', this_dir);
        end
        repo_root = parent_dir;
    end
    cd(repo_root);
    addpath(repo_root);
    addpath(genpath(fullfile(repo_root, 'src')));
    addpath(fullfile(repo_root, 'simulink'));
    addpath(this_dir);
    manual_fill_baseline_lock();
catch ME
    disp(getReport(ME, 'extended', 'hyperlinks', 'off'));
    exit(1);
end
exit(0);
