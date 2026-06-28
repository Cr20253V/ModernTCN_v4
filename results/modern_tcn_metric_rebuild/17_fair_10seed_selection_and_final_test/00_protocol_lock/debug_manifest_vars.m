try
    this_file = mfilename('fullpath');
    this_dir = fileparts(this_file);
    repo_root = this_dir;
    while exist(fullfile(repo_root, 'init_project.m'), 'file') ~= 2
        parent_dir = fileparts(repo_root);
        if strcmp(parent_dir, repo_root)
            error('debug_manifest_vars:ProjectRootNotFound', ...
                'Could not find init_project.m above %s.', this_dir);
        end
        repo_root = parent_dir;
    end
    cd(repo_root);
    addpath(repo_root);
    addpath(genpath(fullfile(repo_root, 'src')));
    addpath(fullfile(repo_root, 'simulink'));
    addpath(this_dir);

    path = fullfile(repo_root, 'results', 'modern_tcn_metric_rebuild', ...
        '17_fair_10seed_selection_and_final_test', '04_validation_sentinel_closed_loop', ...
        'sentinel_manifest.csv');
    opts = detectImportOptions(path, 'TextType', 'string', 'Delimiter', ',');
    opts.VariableNamingRule = 'preserve';
    T = readtable(path, opts);
    names = string(T.Properties.VariableNames);
    disp(names);
    fprintf('has_enter_validation_sentinel=%d\n', any(strcmp(names, 'enter_validation_sentinel')));
    fprintf('has_screen_exception_used=%d\n', any(strcmp(names, 'screen_exception_used')));
    for i = 1:numel(names)
        fprintf('name[%d]=<%s>\n', i, names(i));
    end
catch ME
    disp(getReport(ME, 'extended', 'hyperlinks', 'off'));
    exit(1);
end
exit(0);
