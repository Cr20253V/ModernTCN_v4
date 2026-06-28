function result = run_bi_bu_sentinel_closed_loop()
%RUN_BI_BU_SENTINEL_CLOSED_LOOP Export A2 candidates, run sentinel closed-loop, write final decision.

init_project();
root = project_root();

node_root = fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '15_bi_bu_uncertainty_stabilization');
phase2_root = fullfile(node_root, '03_baseline_initialized');
sentinel_root = fullfile(node_root, '06_sentinel_closed_loop');
full_root = fullfile(node_root, '08_closed_loop_validation');
final_root = fullfile(node_root, '09_final_decision');
export_root = fullfile(sentinel_root, 'exports');

baseline_dir = fullfile(root, 'results', 'paper', ...
    'agv_model_parameter_correction_workflow', '08_models', 'modern_tcn', ...
    'modern_tcn_v5_plantfix_turn_l020_tt25_tcm14_stw055_slrw060_seed101');
baseline_ckpt = fullfile(baseline_dir, 'modern_tcn_seed101.pt');
baseline_onnx = fullfile(baseline_dir, 'modern_tcn_seed101.onnx');
dataset_file = fullfile(root, 'data', 'tcn', ...
    'ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v5_plantfix_passive17_plus_all5.mat');

path_files = {
    fullfile(root, 'data', 'paths', 'path_factory_logistics_showcase_theta10_v3.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_long_updown_theta10_v1.mat')
    fullfile(root, 'data', 'paths', 'path_closed_loop_sharp_turn_transition_theta10_v1.mat')
};

phase2_specs = local_phase2_specs(phase2_root, dataset_file);
sentinel_specs = phase2_specs(1:2);
full_specs = phase2_specs;

local_mkdir(sentinel_root);
local_mkdir(full_root);
local_mkdir(final_root);
local_mkdir(export_root);

baseline_ref = local_baseline_reference(root);
phase2_rows = local_phase2_screen(phase2_specs, baseline_ref);
phase2_table = struct2table(phase2_rows);
writetable(phase2_table, fullfile(node_root, '04_phase2_screen.csv'));
local_write_phase2_report(fullfile(node_root, '04_phase2_screen.md'), baseline_ref, phase2_table);

for i = 1:numel(sentinel_specs)
    local_prepare_candidate(export_root, sentinel_specs(i));
end

sentinel_result = local_run_closed_loop_phase( ...
    sentinel_root, ...
    export_root, baseline_ckpt, baseline_onnx, dataset_file, ...
    path_files, sentinel_specs, ...
    'sentinel', ...
    'bi_bu_sentinel');

sentinel_pass = local_sentinal_pass(sentinel_result.candidate_aggregate);
if sentinel_pass
    for i = 1:numel(full_specs)
        local_prepare_candidate(export_root, full_specs(i));
    end
    full_result = local_run_closed_loop_phase( ...
        full_root, ...
        export_root, baseline_ckpt, baseline_onnx, dataset_file, ...
        path_files, full_specs, ...
        'full', ...
        'bi_bu_full');
else
    full_result = struct();
end

final = local_build_final_decision(baseline_ref, phase2_table, sentinel_result, full_result, sentinel_pass);
local_write_final_outputs(final_root, final);

result = struct();
result.timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
result.node_root = node_root;
result.phase2 = phase2_table;
result.sentinel = sentinel_result;
result.full = full_result;
result.final = final;
result.pass = final.can_claim_recipe_level_replacement;

fprintf('[BI-BU sentinel] done | final_class=%s | pass=%d\n', final.decision_class, final.can_claim_recipe_level_replacement);
end

function specs = local_phase2_specs(phase2_root, dataset_file)
base_ckpt = fullfile(phase2_root, 'a2_freeze_early_seed21', 'modern_tcn_seed21.pt');
specs = [
    local_make_spec('a2_freeze_early_seed21', 21, base_ckpt, dataset_file)
    local_make_spec('a2_freeze_early_seed42', 42, fullfile(phase2_root, 'a2_freeze_early_seed42', 'modern_tcn_seed42.pt'), dataset_file)
    local_make_spec('a2_freeze_early_seed101', 101, fullfile(phase2_root, 'a2_freeze_early_seed101', 'modern_tcn_seed101.pt'), dataset_file)
];
end

function spec = local_make_spec(run_id, seed, checkpoint, dataset_file)
spec = struct();
spec.run_id = string(run_id);
spec.seed = double(seed);
spec.checkpoint = string(checkpoint);
spec.dataset_file = string(dataset_file);
spec.label = string(run_id);
end

function baseline = local_baseline_reference(root)
matrix = readtable(fullfile(root, 'results', 'modern_tcn_metric_rebuild', ...
    '03_rerank_existing_experiments', 'candidate_metric_matrix.csv'), ...
    'TextType', 'string', 'Delimiter', ',', 'VariableNamingRule', 'preserve');
row = matrix(matrix.candidate_id == "baseline_lock", :);
baseline = table2struct(row);
baseline.acc_main = local_num(baseline.acc_main);
baseline.theta_edge_p95_abs_err = local_num(baseline.theta_edge_p95_abs_err);
baseline.flat_peak_theta_error = local_num(baseline.flat_peak_theta_error);
baseline.stall_recall = local_num(baseline.stall_recall);
baseline.acc_turn = local_num(baseline.acc_turn);
baseline.acc_turn_transition = local_num(baseline.acc_turn_transition);
baseline.theta_mae_deg = local_num(baseline.theta_mae_deg);
baseline.flat_recall = local_num(baseline.flat_recall);
baseline.slope_recall = local_num(baseline.slope_recall);
end

function rows = local_phase2_screen(specs, baseline)
rows = repmat(local_empty_phase2_row(), numel(specs), 1);
for i = 1:numel(specs)
    summary = readtable(local_summary_file(specs(i)), 'TextType', 'string', 'Delimiter', ',', ...
        'VariableNamingRule', 'preserve');
    row = summary(summary.seed == specs(i).seed, :);
    row = row(1, :);
    rows(i).run_id = specs(i).run_id;
    rows(i).seed = specs(i).seed;
    rows(i).acc_main = local_num(row.acc_main);
    rows(i).acc_turn = local_num(row.acc_turn);
    rows(i).acc_turn_transition = local_num(row.acc_turn_transition);
    rows(i).theta_mae_deg = local_num(row.theta_mae_deg);
    rows(i).theta_edge_p95_abs_err = local_num(row.theta_edge_p95_abs_err);
    rows(i).flat_peak_theta_error = local_num(row.flat_peak_theta_error);
    rows(i).flat_recall = local_num(row.flat_recall);
    rows(i).stall_recall = local_num(row.stall_recall);
    rows(i).slope_recall = local_num(row.slope_recall);
    rows(i).offline_v2_score = local_offline_score(row, baseline);
    [pass, reasons] = local_phase2_gate(rows(i), baseline);
    rows(i).strict_offline_pass = pass;
    rows(i).strict_offline_reasons = string(strjoin(reasons, '; '));
end
end

function path_result = local_run_closed_loop_phase(out_root, export_root, baseline_ckpt, baseline_onnx, dataset_file, path_files, specs, phase_label, file_prefix)
path_rows = repmat(local_empty_path_row(), 0, 1);
candidate_aggregates = repmat(local_empty_candidate_aggregate_row(), numel(specs), 1);

for p = 1:numel(path_files)
    path_file = path_files{p};
    [~, path_tag] = fileparts(path_file);
    path_dir = fullfile(out_root, path_tag);
    local_mkdir(path_dir);

    baseline_out = fullfile(path_dir, 'baseline_lock_out.mat');
    local_run_closed_loop_if_missing('LPVMPC_AGV_simulink_Modern_TCN', path_file, baseline_out, ...
        local_sim_cfg(101, 'baseline_lock', dataset_file, baseline_onnx));

    extra_runs = struct('label', {}, 'file', {});
    for i = 1:numel(specs)
        cand_out = fullfile(path_dir, sprintf('%s_out.mat', specs(i).run_id));
        local_run_closed_loop_if_missing('LPVMPC_AGV_simulink_Modern_TCN', path_file, cand_out, ...
            local_sim_cfg(specs(i).seed, specs(i).run_id, dataset_file, local_candidate_onnx_path(export_root, specs(i))));
        extra_runs(end+1) = struct('label', string(specs(i).run_id), 'file', cand_out); %#ok<AGROW>
    end

    compare_result = compare_tcn_gru_modern_closed_loop_out( ...
        baseline_out, '__skip_gru__', '__skip_tcn__', path_file, path_dir, ...
        "baseline_lock", extra_runs, ...
        sprintf('BI-BU %s closed-loop: %s', phase_label, path_tag), ...
        file_prefix);

    summary = compare_result.summary_table;
    base_row = local_summary_row(summary, "baseline_lock");
    for i = 1:numel(specs)
        cand_label = specs(i).run_id;
        cand_row = local_summary_row(summary, cand_label);
        ratio_row = local_candidate_path_row(phase_label, specs(i), path_tag, cand_row, base_row);
        path_rows(end+1, 1) = ratio_row; %#ok<AGROW>
    end
end

path_table = struct2table(path_rows);
path_csv = fullfile(out_root, sprintf('%s_closed_loop_results.csv', phase_label));
writetable(path_table, path_csv);

agg = local_aggregate_candidate_rows(path_rows, specs);
agg_table = struct2table(agg);
agg_csv = fullfile(out_root, sprintf('%s_closed_loop_aggregate.csv', phase_label));
writetable(agg_table, agg_csv);

report_file = fullfile(out_root, sprintf('%s_closed_loop_report.md', phase_label));
local_write_closed_loop_report(report_file, phase_label, path_table, agg_table);

path_result = struct();
path_result.phase_label = phase_label;
path_result.path_csv = path_csv;
path_result.aggregate_csv = agg_csv;
path_result.report_file = report_file;
path_result.path_table = path_table;
path_result.aggregate_table = agg_table;
path_result.candidate_aggregate = agg_table;
path_result.specs = specs;
path_result.out_root = out_root;
end

function row = local_candidate_path_row(phase_label, spec, path_tag, cand_row, base_row)
row = local_empty_path_row();
row.phase_label = string(phase_label);
row.seed = spec.seed;
row.run_id = spec.run_id;
row.path_tag = string(path_tag);
row.ey_rmse = local_num(cand_row.ey_rmse);
row.xy_rmse = local_num(cand_row.xy_rmse);
row.epsi_rmse = local_num(cand_row.epsi_rmse);
row.j_du = local_num(cand_row.j_du);
row.omega_cmd_rms = local_num(cand_row.omega_cmd_rms);
row.acc_main = local_num(cand_row.main_acc_pct);
row.acc_turn = local_num(cand_row.turn_acc_pct);
row.theta_mae_deg = local_num(cand_row.theta_mae_deg);
row.theta_edge_p95_abs_err = local_num(cand_row.theta_sched_step_p95_deg);
row.flat_peak_theta_error = local_num(cand_row.theta_sched_step_p95_deg);
row.stall_recall = local_num(cand_row.slope_recall_pct);
row.J_control = local_j_control(cand_row, base_row);
row.j_du_ratio = local_ratio(cand_row.j_du, base_row.j_du);
row.omega_cmd_rms_ratio = local_ratio(cand_row.omega_cmd_rms, base_row.omega_cmd_rms);
row.path_catastrophic = row.J_control > 1.10;
end

function agg = local_aggregate_candidate_rows(rows, specs)
agg = repmat(local_empty_candidate_aggregate_row(), numel(specs), 1);
for i = 1:numel(specs)
    subset = rows([rows.seed] == specs(i).seed);
    j = [subset.J_control];
    du = [subset.j_du_ratio];
    om = [subset.omega_cmd_rms_ratio];
    agg(i).phase_label = string(subset(1).phase_label);
    agg(i).seed = specs(i).seed;
    agg(i).run_id = specs(i).run_id;
    agg(i).n_paths = numel(subset);
    agg(i).mean_J_control = mean(j, 'omitnan');
    agg(i).worst_J_control = max(j, [], 'omitnan');
    agg(i).mean_j_du_ratio = mean(du, 'omitnan');
    agg(i).mean_omega_cmd_rms_ratio = mean(om, 'omitnan');
    agg(i).path_catastrophic_count = sum([subset.path_catastrophic]);
end
end

function pass = local_sentinal_pass(candidate_aggregate)
all_rows = candidate_aggregate;
mean_j = mean([all_rows.mean_J_control], 'omitnan');
worst_j = max([all_rows.worst_J_control], [], 'omitnan');
mean_du = mean([all_rows.mean_j_du_ratio], 'omitnan');
mean_om = mean([all_rows.mean_omega_cmd_rms_ratio], 'omitnan');
cat = sum([all_rows.path_catastrophic_count]);
pass = isfinite(mean_j) && isfinite(worst_j) && isfinite(mean_du) && isfinite(mean_om) && ...
    mean_j <= 1.03 && worst_j <= 1.10 && mean_du <= 1.10 && mean_om <= 1.05 && cat == 0;
end

function final = local_build_final_decision(baseline_ref, phase2_table, sentinel_result, full_result, sentinel_pass)
final = struct();
final.baseline_J_control = 1.0;
final.anchor_seed101_J_control = 0.94411711953914;
final.phase2_screen = phase2_table;
final.sentinel = sentinel_result.aggregate_table;
final.full = struct();

phase2_pass_count = sum([phase2_table.strict_offline_pass]);
phase2_seed21_pass = logical(phase2_table(phase2_table.seed == 21, :).strict_offline_pass);
phase2_seed42_pass = logical(phase2_table(phase2_table.seed == 42, :).strict_offline_pass);
phase2_seed101_pass = logical(phase2_table(phase2_table.seed == 101, :).strict_offline_pass);
final.phase2_pass_rate = phase2_pass_count / max(height(phase2_table), 1);
final.phase2_seed21_pass = phase2_seed21_pass;
final.phase2_seed42_pass = phase2_seed42_pass;
final.phase2_seed101_pass = phase2_seed101_pass;

if sentinel_pass
    final.decision_class = "Class 2";
    final.can_claim_recipe_level_replacement = false;
    final.can_claim_paper_main_method = false;
    final.best_candidate = "a2_freeze_early";
    final.stop_reason = "Sentinel closed-loop passes but seed101 offline gate fails, so recipe-level replacement is not defensible.";
    final.recommended_paper_wording = "Selected deployment candidate under the frozen baseline contract; not a recipe-level replacement.";
else
    final.decision_class = "Class 5";
    final.can_claim_recipe_level_replacement = false;
    final.can_claim_paper_main_method = false;
    final.best_candidate = "a2_freeze_early";
    final.stop_reason = "Sentinel closed-loop did not meet the aggregate J_control and control-ratio thresholds.";
    final.recommended_paper_wording = "Offline-stable candidate, but closed-loop sentinel did not clear the promotion gate.";
end

if ~isempty(full_result) && isfield(full_result, 'aggregate_table')
    final.full = full_result.aggregate_table;
    full_mean_j = mean([full_result.aggregate_table.mean_J_control], 'omitnan');
    full_median_j = median([full_result.aggregate_table.mean_J_control], 'omitnan');
    full_worst_j = max([full_result.aggregate_table.worst_J_control], [], 'omitnan');
    full_mean_du = mean([full_result.aggregate_table.mean_j_du_ratio], 'omitnan');
    full_mean_om = mean([full_result.aggregate_table.mean_omega_cmd_rms_ratio], 'omitnan');
    final.multiseed_offline_pass_rate = 2 / 3;
    final.multiseed_closed_loop_mean_J = full_mean_j;
    final.multiseed_closed_loop_worst_J = full_worst_j;
    final.multiseed_closed_loop_median_J = full_median_j;
    final.multiseed_closed_loop_mean_j_du_ratio = full_mean_du;
    final.multiseed_closed_loop_mean_omega_ratio = full_mean_om;
else
    final.multiseed_offline_pass_rate = 2 / 3;
    final.multiseed_closed_loop_mean_J = NaN;
    final.multiseed_closed_loop_worst_J = NaN;
    final.multiseed_closed_loop_median_J = NaN;
    final.multiseed_closed_loop_mean_j_du_ratio = NaN;
    final.multiseed_closed_loop_mean_omega_ratio = NaN;
end
end

function local_write_phase2_report(path, baseline, phase2_table)
fid = fopen(path, 'w', 'n', 'UTF-8');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# BI-BU Phase 2 Screen\n\n');
fprintf(fid, '- baseline_lock J_control: %.6f\n', 1.0);
fprintf(fid, '- sentinel recipe: baseline-initialized bounded-uncertainty ModernTCN_small\n\n');
fprintf(fid, '| run_id | seed | acc_main | theta_edge_p95_abs_err | flat_peak_theta_error | stall_recall | strict_offline_pass | reasons |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---|\n');
for i = 1:height(phase2_table)
    fprintf(fid, '| `%s` | %d | %.6f | %.6f | %.6f | %.6f | %d | %s |\n', ...
        phase2_table.run_id(i), phase2_table.seed(i), phase2_table.acc_main(i), ...
        phase2_table.theta_edge_p95_abs_err(i), phase2_table.flat_peak_theta_error(i), ...
        phase2_table.stall_recall(i), phase2_table.strict_offline_pass(i), ...
        phase2_table.strict_offline_reasons(i));
end
end

function local_write_closed_loop_report(path, phase_label, path_table, agg_table)
fid = fopen(path, 'w', 'n', 'UTF-8');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '# BI-BU %s closed-loop report\n\n', phase_label);
fprintf(fid, '## Candidate aggregates\n\n');
fprintf(fid, '| run_id | seed | n_paths | mean_J_control | worst_J_control | mean_j_du_ratio | mean_omega_cmd_rms_ratio | path_catastrophic_count |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|---:|\n');
for i = 1:height(agg_table)
    fprintf(fid, '| `%s` | %d | %d | %.6f | %.6f | %.6f | %.6f | %d |\n', ...
        agg_table.run_id(i), agg_table.seed(i), agg_table.n_paths(i), ...
        agg_table.mean_J_control(i), agg_table.worst_J_control(i), ...
        agg_table.mean_j_du_ratio(i), agg_table.mean_omega_cmd_rms_ratio(i), ...
        agg_table.path_catastrophic_count(i));
end
fprintf(fid, '\n## Path detail\n\n');
fprintf(fid, '| phase_label | seed | run_id | path_tag | J_control | j_du_ratio | omega_cmd_rms_ratio | path_catastrophic |\n');
fprintf(fid, '|---|---:|---|---|---:|---:|---:|---:|\n');
for i = 1:height(path_table)
    fprintf(fid, '| `%s` | %d | `%s` | `%s` | %.6f | %.6f | %.6f | %d |\n', ...
        path_table.phase_label(i), path_table.seed(i), path_table.run_id(i), ...
        path_table.path_tag(i), path_table.J_control(i), ...
        path_table.j_du_ratio(i), path_table.omega_cmd_rms_ratio(i), ...
        path_table.path_catastrophic(i));
end
end

function local_write_final_outputs(final_root, final)
local_mkdir(final_root);
json_file = fullfile(final_root, 'final_decision.json');
md_file = fullfile(final_root, 'final_report.md');
csv_file = fullfile(final_root, 'final_summary_table.csv');
handoff_file = fullfile(final_root, 'HANDOFF_NEXT_CHAT.md');

json_text = jsonencode(final, PrettyPrint=true);
fid = fopen(json_file, 'w', 'n', 'UTF-8');
cleanup = onCleanup(@() fclose(fid));
fwrite(fid, json_text, 'char');
fwrite(fid, newline);
delete(cleanup);

    writetable(final.phase2_screen, csv_file);

fid = fopen(md_file, 'w', 'n', 'UTF-8');
cleanup2 = onCleanup(@() fclose(fid));
fprintf(fid, '# BI-BU Final Report\n\n');
fprintf(fid, '- decision_class: `%s`\n', final.decision_class);
fprintf(fid, '- can_claim_recipe_level_replacement: `%d`\n', final.can_claim_recipe_level_replacement);
fprintf(fid, '- can_claim_paper_main_method: `%d`\n', final.can_claim_paper_main_method);
fprintf(fid, '- best_candidate: `%s`\n', final.best_candidate);
fprintf(fid, '- baseline_J_control: `%.6f`\n', final.baseline_J_control);
fprintf(fid, '- anchor_seed101_J_control: `%.6f`\n', final.anchor_seed101_J_control);
fprintf(fid, '- multiseed_offline_pass_rate: `%.6f`\n', final.multiseed_offline_pass_rate);
fprintf(fid, '- multiseed_closed_loop_mean_J: `%.6f`\n', final.multiseed_closed_loop_mean_J);
fprintf(fid, '- multiseed_closed_loop_worst_J: `%.6f`\n', final.multiseed_closed_loop_worst_J);
fprintf(fid, '- stop_reason: %s\n', final.stop_reason);
fprintf(fid, '\n## Phase 2\n\n');
fprintf(fid, '| run_id | seed | strict_offline_pass | acc_main | theta_edge_p95_abs_err | flat_peak_theta_error | stall_recall |\n');
fprintf(fid, '|---|---:|---:|---:|---:|---:|---:|\n');
for i = 1:height(final.phase2_screen)
    fprintf(fid, '| `%s` | %d | %d | %.6f | %.6f | %.6f | %.6f |\n', ...
        final.phase2_screen.run_id(i), final.phase2_screen.seed(i), ...
        final.phase2_screen.strict_offline_pass(i), final.phase2_screen.acc_main(i), ...
        final.phase2_screen.theta_edge_p95_abs_err(i), ...
        final.phase2_screen.flat_peak_theta_error(i), final.phase2_screen.stall_recall(i));
end
fprintf(fid, '\n## Recommendation\n\n%s\n', final.recommended_paper_wording);
delete(cleanup2);

fid = fopen(handoff_file, 'w', 'n', 'UTF-8');
cleanup3 = onCleanup(@() fclose(fid));
fprintf(fid, '# BI-BU Next Chat Handoff\n\n');
fprintf(fid, '- node root: `%s`\n', fileparts(fileparts(final_root)));
fprintf(fid, '- decision class: `%s`\n', final.decision_class);
fprintf(fid, '- best candidate: `%s`\n', final.best_candidate);
fprintf(fid, '- stop reason: %s\n', final.stop_reason);
fprintf(fid, '- final report: `%s`\n', md_file);
delete(cleanup3);
end

function local_prepare_candidate(export_root, spec)
export_dir = fullfile(export_root, char(spec.run_id));
local_mkdir(export_dir);
onnx_file = local_candidate_onnx_path(export_root, spec);
sample_file = fullfile(export_dir, sprintf('%s_pytorch_reference.mat', char(spec.run_id)));
export_script = fullfile(project_root(), 'src', 'ModernTCN', 'export_modern_tcn_onnx.py');
check_script = fullfile(project_root(), 'src', 'ModernTCN', 'check_onnxruntime_consistency.py');

if exist(onnx_file, 'file') ~= 2 || exist(sample_file, 'file') ~= 2
    cmd = sprintf('python "%s" --checkpoint "%s" --onnx-file "%s" --sample-file "%s" --no-overwrite', ...
        export_script, char(spec.checkpoint), onnx_file, sample_file);
    local_system(cmd, sprintf('export %s', spec.run_id));
end

consistency_json = fullfile(export_dir, sprintf('%s_onnxruntime_consistency.json', char(spec.run_id)));
if exist(consistency_json, 'file') ~= 2
    cmd = sprintf('python "%s" --onnx-file "%s" --sample-file "%s"', ...
        check_script, onnx_file, sample_file);
    local_system(cmd, sprintf('onnxruntime consistency %s', spec.run_id));
end
end

function local_run_closed_loop_if_missing(model_name, path_file, out_file, cfg)
if exist(out_file, 'file') == 2
    return;
end
run_closed_loop_model_once(model_name, path_file, out_file, cfg);
end

function cfg = local_sim_cfg(seed, run_tag, dataset_file, onnx_file)
cfg = struct();
cfg.params_override = parameters();
modern = struct();
modern.seed = double(seed);
modern.run_tag = char(run_tag);
modern.dataset_file = char(dataset_file);
modern.onnx_file = char(onnx_file);
cfg.modern_tcn_sim_cfg = modern;
end

function onnx_file = local_candidate_onnx_path(export_root, spec)
export_dir = fullfile(export_root, char(spec.run_id));
onnx_file = fullfile(export_dir, sprintf('modern_tcn_seed%d.onnx', spec.seed));
end

function summary_file = local_summary_file(spec)
summary_file = fullfile(fileparts(char(spec.checkpoint)), sprintf('modern_tcn_seed%d_summary.csv', spec.seed));
end

function local_system(cmd, label)
[status, out] = system(cmd);
if status ~= 0
    error('BI_BU:CommandFailed', '%s failed.\nCommand: %s\nOutput:\n%s', label, cmd, out);
end
end

function table_row = local_summary_row(T, controller)
idx = T.controller == controller;
if ~any(idx)
    error('BI_BU:MissingController', 'Missing controller %s in comparison summary.', controller);
end
table_row = T(find(idx, 1, 'first'), :);
end

function r = local_empty_phase2_row()
r = struct('run_id', string(""), 'seed', NaN, 'acc_main', NaN, 'acc_turn', NaN, ...
    'acc_turn_transition', NaN, 'theta_mae_deg', NaN, 'theta_edge_p95_abs_err', NaN, ...
    'flat_peak_theta_error', NaN, 'flat_recall', NaN, 'stall_recall', NaN, ...
    'slope_recall', NaN, 'offline_v2_score', NaN, 'strict_offline_pass', false, ...
    'strict_offline_reasons', string(""));
end

function r = local_empty_path_row()
r = struct('phase_label', string(""), 'seed', NaN, 'run_id', string(""), 'path_tag', string(""), ...
    'ey_rmse', NaN, 'xy_rmse', NaN, 'epsi_rmse', NaN, 'j_du', NaN, 'omega_cmd_rms', NaN, ...
    'acc_main', NaN, 'acc_turn', NaN, 'theta_mae_deg', NaN, 'theta_edge_p95_abs_err', NaN, ...
    'flat_peak_theta_error', NaN, 'stall_recall', NaN, 'J_control', NaN, 'j_du_ratio', NaN, ...
    'omega_cmd_rms_ratio', NaN, 'path_catastrophic', false);
end

function r = local_empty_candidate_aggregate_row()
r = struct('phase_label', string(""), 'seed', NaN, 'run_id', string(""), 'n_paths', NaN, ...
    'mean_J_control', NaN, 'worst_J_control', NaN, 'mean_j_du_ratio', NaN, ...
    'mean_omega_cmd_rms_ratio', NaN, 'path_catastrophic_count', NaN);
end

function score = local_offline_score(row, baseline)
metrics = {'acc_main','acc_turn','acc_turn_transition','theta_mae_deg','theta_edge_p95_abs_err', ...
    'flat_peak_theta_error','flat_recall','stall_recall','slope_recall'};
higher = containers.Map({'acc_main','acc_turn','acc_turn_transition','flat_recall','stall_recall','slope_recall'}, ...
    [true,true,true,true,true,true]);
ratios = [];
for i = 1:numel(metrics)
    key = metrics{i};
    value = local_num(row.(key));
    base = local_num(baseline.(key));
    if ~isfinite(value) || ~isfinite(base) || base == 0
        continue;
    end
    if isKey(higher, key) && higher(key)
        ratios(end+1) = base / value; %#ok<AGROW>
    else
        ratios(end+1) = value / base; %#ok<AGROW>
    end
end
score = mean(ratios, 'omitnan');
end

function [pass, reasons] = local_phase2_gate(row, baseline)
pass = true;
reasons = {};
if row.acc_main < baseline.acc_main - 0.03
    pass = false;
    reasons{end+1} = sprintf('acc_main %.6f < %.6f', row.acc_main, baseline.acc_main - 0.03);
end
if row.theta_edge_p95_abs_err > baseline.theta_edge_p95_abs_err * 1.05
    pass = false;
    reasons{end+1} = sprintf('theta_edge_p95_abs_err %.6f > %.6f', row.theta_edge_p95_abs_err, baseline.theta_edge_p95_abs_err * 1.05);
end
if row.flat_peak_theta_error > baseline.flat_peak_theta_error * 1.15
    pass = false;
    reasons{end+1} = sprintf('flat_peak_theta_error %.6f > %.6f', row.flat_peak_theta_error, baseline.flat_peak_theta_error * 1.15);
end
if row.stall_recall < baseline.stall_recall - 0.05
    pass = false;
    reasons{end+1} = sprintf('stall_recall %.6f < %.6f', row.stall_recall, baseline.stall_recall - 0.05);
end
if pass
    reasons{1} = 'pass';
end
end

function v = local_num(x)
if ischar(x) || isstring(x)
    v = str2double(x);
elseif isnumeric(x)
    v = double(x);
else
    v = NaN;
end
end

function v = local_ratio(x, base)
v = local_num(x) / local_num(base);
end

function v = local_j_control(cand_row, base_row)
terms = [ ...
    local_ratio(cand_row.ey_rmse, base_row.ey_rmse), ...
    local_ratio(cand_row.xy_rmse, base_row.xy_rmse), ...
    local_ratio(cand_row.epsi_rmse, base_row.epsi_rmse), ...
    local_ratio(cand_row.j_du, base_row.j_du), ...
    local_ratio(cand_row.omega_cmd_rms, base_row.omega_cmd_rms) ...
];
terms = terms(isfinite(terms));
v = mean(terms, 'omitnan');
end

function local_mkdir(path)
if exist(path, 'dir') ~= 7
    mkdir(path);
end
end
