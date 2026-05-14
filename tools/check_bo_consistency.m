function check_bo_consistency(n_runs)
% 一致性检查：重复评估同一 bestPoint 的代价
if nargin < 1 || isempty(n_runs)
    n_runs = 5;
end

root = project_root();
results_dir = fullfile(root, 'results', 'bo_results');
phase1_file = fullfile(results_dir, 'phase1_best.mat');

if ~exist(phase1_file, 'file')
    error('未找到 Phase1 结果: %s', phase1_file);
end

S = load(phase1_file, 'bestPoint');
if ~isfield(S, 'bestPoint')
    error('phase1_best.mat 中未找到 bestPoint');
end

% 读取参数与db
params = parameters();
Sdb = load(fullfile(root, 'data', 'models', 'lin_agv_db.mat'), 'db');
db = Sdb.db;

% 组装 options（沿用 Phase1 逻辑）
options = struct();
options.phase = 1;
options.UseParallel = false;
options.MaxObjectiveEvaluations = 1;
options.save_history = false;
options.path_file = fullfile(root, 'data', 'paths', 'path_industrial_lite.mat');
if exist(options.path_file, 'file')
    S_ref = load(options.path_file, 'ref');
    if isfield(S_ref, 'ref') && isfield(S_ref.ref, 'meta') && isfield(S_ref.ref.meta, 'zones')
        options.zones = S_ref.ref.meta.zones;
    else
        options.zones = struct(...
            'startup',      [0, 10], ...
            'golden_test',  [10, 50], ...
            'pure_turn',    [50, 72], ...
            'pure_slope',   [72, 92], ...
            'composite',    [92, 112], ...
            'closure',      [112, 150]);
    end
else
    options.zones = struct(...
        'startup',      [0, 10], ...
        'golden_test',  [10, 50], ...
        'pure_turn',    [50, 72], ...
        'pure_slope',   [72, 92], ...
        'composite',    [92, 112], ...
        'closure',      [112, 150]);
end
options.scenes = struct(...
    'startup',0.00, ...
    'golden_test',0.35, ...
    'pure_turn',0.40, ...
    'pure_slope',0.15, ...
    'composite',0.10, ...
    'closure',0.00);

J = zeros(n_runs,1);
X = S.bestPoint;
for i = 1:n_runs
    [J(i), ~] = evaluate_bo_point(X, params, db, options);
end

fprintf('一致性检查 (n=%d): mean=%.6f, std=%.6g, min=%.6f, max=%.6f\n', ...
    n_runs, mean(J), std(J), min(J), max(J));

end
