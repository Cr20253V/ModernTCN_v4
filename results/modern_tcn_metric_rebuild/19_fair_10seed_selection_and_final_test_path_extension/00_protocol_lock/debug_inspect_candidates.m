function debug_inspect_candidates()
root = local_project_root();
files = {
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_positive_slope_lr_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_balanced_mild_updown_lr_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_factory_like_buffered_lr_190_v1.mat')
    fullfile(root, 'data', 'paths', 'modern_tcn_showcase', 'candidates', 'path_modern_tcn_showcase_candidate_positive_slope_factory_loop_190_v1.mat')
};

for i = 1:numel(files)
    f = files{i};
    fprintf('\n=== %s ===\n', f);
    if exist(f, 'file') ~= 2
        fprintf('missing\n');
        continue;
    end
    info = whos('-file', f);
    fprintf('vars: %s\n', strjoin(string({info.name}), ', '));
    try
        S = load(f);
    catch ME
        fprintf('load error: %s\n', ME.message);
        continue;
    end
    fn = fieldnames(S);
    fprintf('top fields: %s\n', strjoin(string(fn), ', '));
    if isfield(S, 'ref')
        r = S.ref;
        fprintf('ref class: %s\n', class(r));
        if isstruct(r)
            fprintf('ref fields: %s\n', strjoin(string(fieldnames(r)), ', '));
            disp(r);
            if isfield(r, 'meta')
                rm = r.meta;
                fprintf('ref.meta class: %s\n', class(rm));
                if ischar(rm) || isstring(rm)
                    fprintf('ref.meta value: %s\n', string(rm));
                end
                if isstruct(rm)
                    fprintf('ref.meta fields: %s\n', strjoin(string(fieldnames(rm)), ', '));
                    if isfield(rm, 'constraints')
                        fprintf('constraints class: %s\n', class(rm.constraints));
                        disp(rm.constraints);
                    end
                    if isfield(rm, 'segments')
                        fprintf('segments count: %d\n', numel(rm.segments));
                    end
                    if isfield(rm, 'recommended_eval_windows')
                        fprintf('recommended_eval_windows count: %d\n', numel(rm.recommended_eval_windows));
                    end
                    disp(rm);
                end
            end
        end
    end
    if isfield(S, 'meta')
        m = S.meta;
        fprintf('meta class: %s\n', class(m));
        if ischar(m) || isstring(m)
            fprintf('meta value: %s\n', string(m));
        end
        if isstruct(m)
            fprintf('meta fields: %s\n', strjoin(string(fieldnames(m)), ', '));
            disp(m);
        end
    end
end
end

function root = local_project_root()
this_file = mfilename('fullpath');
this_dir = fileparts(this_file);
root = this_dir;
while exist(fullfile(root, 'init_project.m'), 'file') ~= 2
    parent_dir = fileparts(root);
    if strcmp(parent_dir, root)
        error('debug_inspect_candidates:ProjectRootNotFound', ...
            'Could not find init_project.m above %s.', this_dir);
    end
    root = parent_dir;
end
end
