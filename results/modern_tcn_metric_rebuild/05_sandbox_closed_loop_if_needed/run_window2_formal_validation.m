function result = run_window2_formal_validation(cfg)
%RUN_WINDOW2_FORMAL_VALIDATION Run post-sandbox formal validation.
%
% This runner uses the same path set as the frozen baseline aggregate and
% writes only under modern_tcn_metric_rebuild/05_sandbox.../03_formal_validation.

if nargin < 1 || ~isstruct(cfg)
    cfg = struct();
end

init_project();
root = project_root();
out_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '05_sandbox_closed_loop_if_needed');
formal_root = fullfile(out_root, '03_formal_validation');
manifest_file = fullfile(out_root, 'sandbox_candidate_manifest.csv');
status_file = fullfile(out_root, 'sandbox_preflight_status.json');

if exist(manifest_file, 'file') ~= 2
    error('window2_formal:MissingManifest', ...
        'Missing sandbox candidate manifest: %s', manifest_file);
end
if exist(status_file, 'file') ~= 2
    error('window2_formal:MissingStatus', ...
        'Missing sandbox preflight status: %s', status_file);
end
if exist(formal_root, 'dir') ~= 7
    mkdir(formal_root);
end

status = jsondecode(fileread(status_file));
manifest = readtable(manifest_file, 'TextType', 'string', ...
    'Delimiter', ',', 'ReadVariableNames', true, ...
    'VariableNamingRule', 'preserve');
ready_mask = local_bool_column(manifest, 'selected_for_sandbox') & ...
    local_bool_column(manifest, 'consistency_pass');
candidates = manifest(ready_mask, :);
if height(candidates) == 0
    error('window2_formal:NoReadyCandidates', ...
        'No candidate has a passing ONNXRuntime preflight.');
end

path_files = local_cfg(cfg, 'path_files', local_default_path_files(root));
if isstring(path_files)
    path_files = cellstr(path_files);
elseif ischar(path_files)
    path_files = {path_files};
end
stop_time_override = local_cfg(cfg, 'stop_time_override', []);
reuse_existing = logical(local_cfg(cfg, 'reuse_existing', false));

rows = repmat(local_empty_row(), numel(path_files), 1);
for p = 1:numel(path_files)
    path_file = path_files{p};
    [~, path_tag] = fileparts(path_file);
    path_dir = fullfile(formal_root, path_tag);
    if exist(path_dir, 'dir') ~= 7
        mkdir(path_dir);
    end

    fprintf('[window2 formal] path %d/%d: %s\n', p, numel(path_files), path_tag);
    baseline_out = fullfile(path_dir, 'baseline_lock_out.mat');
    sim_cfg = local_sim_cfg(status.baseline, stop_time_override);
    if ~(reuse_existing && exist(baseline_out, 'file') == 2)
        run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
            path_file, baseline_out, sim_cfg);
    end

    extra_runs = struct('label', {}, 'file', {});
    candidate_files = strings(height(candidates), 1);
    for i = 1:height(candidates)
        candidate_id = char(candidates.candidate_id(i));
        candidate_out = fullfile(path_dir, sprintf('%s_out.mat', candidate_id));
        cand_info = struct();
        cand_info.seed = double(candidates.seed(i));
        cand_info.dataset_file = status.baseline.dataset_file;
        cand_info.onnx_file = char(candidates.onnx_file(i));
        cand_info.candidate_id = candidate_id;
        cand_info.run_tag = candidate_id;
        cand_cfg = local_sim_cfg(cand_info, stop_time_override);
        if ~(reuse_existing && exist(candidate_out, 'file') == 2)
            run_closed_loop_model_once('LPVMPC_AGV_simulink_Modern_TCN', ...
                path_file, candidate_out, cand_cfg);
        end
        extra_runs(end+1) = struct('label', string(candidate_id), 'file', candidate_out); %#ok<AGROW>
        candidate_files(i) = string(candidate_out);
    end

    compare_tcn_gru_modern_closed_loop_out( ...
        baseline_out, '__skip_gru__', '__skip_tcn__', path_file, path_dir, ...
        "baseline_lock", extra_runs, ...
        sprintf('Window 2 formal validation: %s', path_tag), ...
        'window2_formal');

    rows(p).path_tag = string(path_tag);
    rows(p).path_file = string(path_file);
    rows(p).out_dir = string(path_dir);
    rows(p).baseline_file = string(baseline_out);
    rows(p).candidate_files = strjoin(candidate_files, ';');
    rows(p).summary_file = string(fullfile(path_dir, 'window2_formal_summary.csv'));
    rows(p).rank_file = string(fullfile(path_dir, 'window2_formal_rank.csv'));
    rows(p).report_file = string(fullfile(path_dir, 'window2_formal_report.md'));
    rows(p).status = "ok";
end

path_table = struct2table(rows);
path_runs_file = fullfile(formal_root, 'formal_path_runs.csv');
writetable(path_table, path_runs_file);

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.formal_root = formal_root;
result.manifest_file = manifest_file;
result.status_file = status_file;
result.path_table = path_table;
result.path_runs_file = path_runs_file;
result.summary_file = fullfile(formal_root, 'formal_validation_execution_summary.md');
result.mat_file = fullfile(formal_root, 'formal_validation_result.mat');
save(result.mat_file, 'result', '-v7.3');
local_write_summary(result, candidates);

fprintf('[window2 formal] path runs: %s\n', result.path_runs_file);
fprintf('[window2 formal] summary:   %s\n', result.summary_file);
end

function path_files = local_default_path_files(root)
path_files = {
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v3.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
};
end

function sim_cfg = local_sim_cfg(info, stop_time_override)
sim_cfg = struct();
if ~isempty(stop_time_override)
    sim_cfg.stop_time_override = stop_time_override;
end
sim_cfg.params_override = parameters();
modern_cfg = struct();
modern_cfg.seed = double(info.seed);
modern_cfg.run_tag = char(info.run_tag);
modern_cfg.dataset_file = char(info.dataset_file);
modern_cfg.onnx_file = char(info.onnx_file);
sim_cfg.modern_tcn_sim_cfg = modern_cfg;
end

function v = local_cfg(cfg, name, default_value)
if isstruct(cfg) && isfield(cfg, name) && ~isempty(cfg.(name))
    v = cfg.(name);
else
    v = default_value;
end
end

function mask = local_bool_column(T, name)
v = T.(name);
if islogical(v)
    mask = v;
elseif isnumeric(v)
    mask = v ~= 0;
else
    s = lower(strtrim(string(v)));
    mask = ismember(s, ["true", "1", "yes"]);
end
end

function row = local_empty_row()
row = struct('path_tag', "", 'path_file', "", 'out_dir', "", ...
    'baseline_file', "", 'candidate_files', "", 'summary_file', "", ...
    'rank_file', "", 'report_file', "", 'status', "");
end

function local_write_summary(result, candidates)
fid = fopen(result.summary_file, 'w');
if fid < 0
    warning('window2_formal:SummaryWriteFailed', ...
        'Cannot write summary: %s', result.summary_file);
    return;
end
cleanup = onCleanup(@() fclose(fid));

fprintf(fid, '# Window 2 Formal Validation Execution Summary\n\n');
fprintf(fid, '- scope: post-sandbox formal closed-loop validation\n');
fprintf(fid, '- candidates: ');
for i = 1:height(candidates)
    if i > 1
        fprintf(fid, ', ');
    end
    fprintf(fid, '`%s`', candidates.candidate_id(i));
end
fprintf(fid, '\n');
fprintf(fid, '- path runs: `%s`\n\n', result.path_runs_file);
fprintf(fid, '## Outputs\n\n');
fprintf(fid, '| path | status | summary | report |\n');
fprintf(fid, '|---|---|---|---|\n');
for i = 1:height(result.path_table)
    fprintf(fid, '| `%s` | %s | `%s` | `%s` |\n', ...
        result.path_table.path_tag(i), result.path_table.status(i), ...
        result.path_table.summary_file(i), result.path_table.report_file(i));
end
fprintf(fid, '\n');
fprintf(fid, 'Formal Class C eligibility must be decided by the aggregated validation report, not by this execution summary alone.\n');
end
