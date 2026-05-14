% ============================================================
% 文件名：eval_mamba_offline.m
% 版本：V1.0
% 日期：2026-04-03
%
% 功能描述：
%   Mamba2 基线量化评估脚本（离线模式）
%   从 Mamba_train_data_full.mat 中取若干 run，对每个 run 的 y_mamba
%   数据模拟在线滑窗推理（128步窗口，每5步调用一次 TCP 服务），
%   将推理结果与 GT 标签逐帧对比，输出量化指标。
%
% 前置条件：
%   - WSL 侧推理服务已启动（mamba2_online_infer.py --serve）
%   - Mamba_train_data_full.mat 已生成（运行过 Mamba_gen_train_data.m）
%
% 输出：
%   - 命令窗口：各头的分类指标汇总
%   - results/gru/ 目录下的 mamba_baseline_metrics.mat（量化结果存档）
%
% 用法：
%   直接运行此脚本（确保 addpath 到 src 目录）
% ============================================================

clear; clc;
root = project_root();
addpath(genpath(fullfile(root, 'src')));

%% ==================== 用户配置 ====================
cfg = struct();
cfg.data_file   = fullfile(root, 'data', 'mamba', 'Mamba_train_data_full.mat');
cfg.out_file    = fullfile(root, 'results', 'gru', 'mamba_baseline_metrics.mat');

% 评估的 Run 数量（从总库中随机抽取，减少总耗时）
cfg.max_runs     = 20;      % 建议 10~30；若想全量评估可改为 Inf
cfg.rand_seed    = 2026;    % 抽取随机种子（可重复）

% 推理参数
cfg.seq_len         = 128;
cfg.infer_interval  = 5;    % 与在线配置一致（每 5 步推理一次）

% 评估步长倍数：每 cfg.eval_stride 个推理触发才实际调用 TCP
% 设为 1 = 完整评估（慢），设为 5 = 每 0.25s 一次推理，速度 5x（推荐）
cfg.eval_stride  = 5;

% 坡度角标签化阈值（与 generate_mamba_labels 一致）
cfg.theta_slope_thresh = deg2rad(2.0);   % |theta| >= 2° 视为坡道

% 输出冗余度
cfg.verbose      = true;

%% ==================== 加载数据 ====================
fprintf('加载训练数据: %s\n', cfg.data_file);
if ~exist(cfg.data_file, 'file')
    error('找不到数据文件，请先运行 Mamba_gen_train_data.m');
end
raw = load(cfg.data_file);
runs = raw.data.runs;
N_total = numel(runs);
fprintf('共 %d 个 Run\n', N_total);

% 随机抽取
rng(cfg.rand_seed);
N_eval = min(cfg.max_runs, N_total);
sel_idx = randperm(N_total, N_eval);
fprintf('本次评估 %d 个 Run（随机索引：%s）\n\n', N_eval, mat2str(sort(sel_idx)));

%% ==================== 初始化累计缓冲 ====================
% 每个时间步只保留"推理帧"（infer_interval 倍处）的对齐样本
all_pred_main   = [];   % [M×1] int
all_gt_main     = [];
all_pred_turn   = [];   % [M×1] int  (-1/0/1)
all_gt_turn     = [];
all_pred_slip   = [];   % [M×1] int
all_gt_slip     = [];
all_pred_stall  = [];   % [M×1] int
all_gt_stall    = [];
all_pred_theta  = [];   % [M×1] double (经 LPF 后的 theta_hat)
all_gt_theta    = [];
all_pred_delta  = [];   % [M×1] double
all_gt_delta    = [];
all_run_ids     = [];   % 标记每个样本来自哪个 run

total_frames    = 0;
total_infer_ok  = 0;
total_infer_fail = 0;

%% ==================== 逐 Run 推理 ====================
params        = parameters();
params.ai_backend = 'tcp_service';   % 强制 TCP（与生产一致）
% eval_stride 倍数：实际推理间隔 = infer_interval × eval_stride
params.ai_infer_interval = cfg.infer_interval * cfg.eval_stride;
params.mamba_read_timeout = 5.0;     % 短超时：失效连接最多等 5s 而非 25s（兜底保护）
fprintf('推理间隔: %d 步 (%.2fs)，预计每 Run 耗时 ~%.0f min，共 %d Run ~%.0f min\n', ...
    params.ai_infer_interval, params.ai_infer_interval * 0.01, ...
    (15001 / params.ai_infer_interval) * 0.35 / 60, N_eval, ...
    N_eval * (15001 / params.ai_infer_interval) * 0.35 / 60);

for ei = 1:N_eval
    run_i  = sel_idx(ei);
    run_data = runs(run_i);

    y_mamba   = double(run_data.y_mamba);      % [N×10] 原始特征
    gt_main   = run_data.label_main(:);        % [N×1]
    gt_turn   = run_data.label_turn(:);        % [N×1] -1/0/1
    gt_slip   = run_data.label_slip(:);
    gt_stall  = run_data.label_stall(:);
    gt_theta  = double(run_data.y_theta_ground(:));
    gt_delta  = double(run_data.y_delta_vehicle(:));

    N = size(y_mamba, 1);
    total_frames = total_frames + N;

    if cfg.verbose
        fprintf('[Run %3d/%d] global_idx=%d, N=%d steps ... ', ei, N_eval, run_i, N);
    end

    % ---- 初始化该 run 的分类器（复用统一接口，自动建 TCP 连接）
    state = Mamba_state_classifier('init', params);

    pred_main  = nan(N, 1);
    pred_turn  = nan(N, 1);
    pred_slip  = nan(N, 1);
    pred_stall = nan(N, 1);
    pred_theta = nan(N, 1);
    pred_delta = nan(N, 1);
    infer_ok_vec = false(N, 1);

    for t = 1:N
        % 构造 34 维虚拟向量（仅填入 10 个通道位）
        y_raw_t = zeros(34, 1);
        y_raw_t(state.channel_idx) = y_mamba(t, :)';

        [state, out] = Mamba_state_classifier('update', state, y_raw_t);

        pred_main(t)  = out.label_main;
        pred_turn(t)  = out.label_turn;
        pred_slip(t)  = out.label_slip;
        pred_stall(t) = out.label_stall;
        pred_theta(t) = out.theta_hat;
        pred_delta(t) = out.delta_hat;
        infer_ok_vec(t) = out.infer_ok;
    end

    Mamba_state_classifier('close', state);

    % ---- 仅取"推理帧"（infer_ok=true 的样本）用于指标计算
    valid_mask = infer_ok_vec;
    n_ok   = sum(valid_mask);
    n_fail = sum(~valid_mask(cfg.seq_len:end));  % 序列满后的失败次数

    total_infer_ok   = total_infer_ok   + n_ok;
    total_infer_fail = total_infer_fail + n_fail;

    all_pred_main   = [all_pred_main;   pred_main(valid_mask)];   %#ok<AGROW>
    all_gt_main     = [all_gt_main;     gt_main(valid_mask)];
    all_pred_turn   = [all_pred_turn;   pred_turn(valid_mask)];
    all_gt_turn     = [all_gt_turn;     gt_turn(valid_mask)];
    all_pred_slip   = [all_pred_slip;   pred_slip(valid_mask)];
    all_gt_slip     = [all_gt_slip;     gt_slip(valid_mask)];
    all_pred_stall  = [all_pred_stall;  pred_stall(valid_mask)];
    all_gt_stall    = [all_gt_stall;    gt_stall(valid_mask)];
    all_pred_theta  = [all_pred_theta;  pred_theta(valid_mask)];
    all_gt_theta    = [all_gt_theta;    gt_theta(valid_mask)];
    all_pred_delta  = [all_pred_delta;  pred_delta(valid_mask)];
    all_gt_delta    = [all_gt_delta;    gt_delta(valid_mask)];
    all_run_ids     = [all_run_ids;     repmat(run_i, n_ok, 1)];

    if cfg.verbose
        fprintf('infer_ok=%d, fail=%d\n', n_ok, n_fail);
    end
end

M = numel(all_pred_main);
fprintf('\n====== 评估帧总数: %d（总步数 %d，推理成功率 %.1f%%）======\n\n', ...
    M, total_frames, 100 * total_infer_ok / max(total_frames, 1));

if M == 0
    error('没有有效推理帧，请检查 TCP 服务是否正常运行');
end

%% ==================== 计算指标 ====================

%% 1. label_main 混淆矩阵（3类：flat/stall/slope）
main_labels = [1, 2, 3];
main_names  = {'flat', 'stall', 'slope'};
cm_main = confmat3(all_gt_main, all_pred_main, main_labels);
[pr_main, rc_main, f1_main] = prf_from_cm(cm_main);
acc_main = sum(all_pred_main == all_gt_main) / M;

%% 2. label_turn 混淆矩阵（3类：right/straight/left）
turn_labels = [-1, 0, 1];
turn_names  = {'right', 'straight', 'left'};
cm_turn = confmat3(all_gt_turn, all_pred_turn, turn_labels);
[pr_turn, rc_turn, f1_turn] = prf_from_cm(cm_turn);
acc_turn = sum(all_pred_turn == all_gt_turn) / M;

%% 3. label_slip F1（二值）
[pr_slip_0, rc_slip_0, f1_slip_0] = binf1(all_gt_slip, all_pred_slip, 0);
[pr_slip_1, rc_slip_1, f1_slip_1] = binf1(all_gt_slip, all_pred_slip, 1);
acc_slip = sum(all_pred_slip == all_gt_slip) / M;

%% 4. label_stall F1（二值）
[pr_stall_0, rc_stall_0, f1_stall_0] = binf1(all_gt_stall, all_pred_stall, 0);
[pr_stall_1, rc_stall_1, f1_stall_1] = binf1(all_gt_stall, all_pred_stall, 1);
acc_stall = sum(all_pred_stall == all_gt_stall) / M;

%% 5. theta_hat RMSE / MAE（与 GT 坡度角对比）
theta_err    = all_pred_theta - all_gt_theta;
theta_rmse   = sqrt(mean(theta_err .^ 2));
theta_mae    = mean(abs(theta_err));
theta_bias   = mean(theta_err);
% 仅坡道帧上的误差（|gt_theta| >= thresh）
slope_mask   = abs(all_gt_theta) >= cfg.theta_slope_thresh;
if any(slope_mask)
    theta_rmse_slope = sqrt(mean(theta_err(slope_mask) .^ 2));
    theta_mae_slope  = mean(abs(theta_err(slope_mask)));
else
    theta_rmse_slope = NaN;
    theta_mae_slope  = NaN;
end

%% 6. delta_hat RMSE / MAE
delta_err  = all_pred_delta - all_gt_delta;
delta_rmse = sqrt(mean(delta_err .^ 2));
delta_mae  = mean(abs(delta_err));
delta_bias = mean(delta_err);

%% ==================== 打印汇总 ====================
fprintf('╔══════════════════════════════════════════════════════════╗\n');
fprintf('║              Mamba2 基线量化评估报告 V1.0                ║\n');
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  评估 Run 数: %-3d       评估帧数: %-8d              ║\n', N_eval, M);
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [label_main]  Acc=%.3f                                ║\n', acc_main);
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f                ║\n', main_names{1}, pr_main(1), rc_main(1), f1_main(1));
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f                ║\n', main_names{2}, pr_main(2), rc_main(2), f1_main(2));
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f                ║\n', main_names{3}, pr_main(3), rc_main(3), f1_main(3));
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [label_turn]  Acc=%.3f                                ║\n', acc_turn);
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f  ← 右转漏检  ║\n', turn_names{1}, pr_turn(1), rc_turn(1), f1_turn(1));
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f                ║\n', turn_names{2}, pr_turn(2), rc_turn(2), f1_turn(2));
fprintf('║    %-10s  P=%.3f  R=%.3f  F1=%.3f                ║\n', turn_names{3}, pr_turn(3), rc_turn(3), f1_turn(3));
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [label_slip]  Acc=%.3f\n', acc_slip);
fprintf('║    normal(0)   P=%.3f  R=%.3f  F1=%.3f                ║\n', pr_slip_0, rc_slip_0, f1_slip_0);
fprintf('║    slip  (1)   P=%.3f  R=%.3f  F1=%.3f                ║\n', pr_slip_1, rc_slip_1, f1_slip_1);
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [label_stall] Acc=%.3f\n', acc_stall);
fprintf('║    normal(0)   P=%.3f  R=%.3f  F1=%.3f                ║\n', pr_stall_0, rc_stall_0, f1_stall_0);
fprintf('║    stall (1)   P=%.3f  R=%.3f  F1=%.3f                ║\n', pr_stall_1, rc_stall_1, f1_stall_1);
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [theta_hat]  RMSE=%.4f rad  MAE=%.4f rad  Bias=%.4f rad\n', theta_rmse, theta_mae, theta_bias);
fprintf('║  (坡道帧)    RMSE=%.4f rad  MAE=%.4f rad\n', theta_rmse_slope, theta_mae_slope);
fprintf('╠══════════════════════════════════════════════════════════╣\n');
fprintf('║  [delta_hat]  RMSE=%.4f rad  MAE=%.4f rad  Bias=%.4f rad\n', delta_rmse, delta_mae, delta_bias);
fprintf('╚══════════════════════════════════════════════════════════╝\n\n');

% 重点提示右转问题
if f1_turn(1) < 0.5
    fprintf('⚠  右转头 F1=%.3f < 0.50，右转漏检问题确认，需关注训练标签分布。\n\n', f1_turn(1));
end

%% ==================== 混淆矩阵详细打印 ====================
fprintf('--- label_main 混淆矩阵 (行=GT, 列=Pred) ---\n');
print_cm(cm_main, main_names);

fprintf('--- label_turn 混淆矩阵 (行=GT, 列=Pred) ---\n');
print_cm(cm_turn, turn_names);

%% ==================== 保存结果 ====================
metrics = struct();
metrics.date          = datestr(now, 'yyyy-mm-dd HH:MM:SS');
metrics.N_eval_runs   = N_eval;
metrics.sel_run_idx   = sel_idx;
metrics.M_frames      = M;
metrics.acc_main      = acc_main;
metrics.cm_main       = cm_main;
metrics.pr_main       = pr_main;  metrics.rc_main = rc_main;  metrics.f1_main = f1_main;
metrics.acc_turn      = acc_turn;
metrics.cm_turn       = cm_turn;
metrics.pr_turn       = pr_turn;  metrics.rc_turn = rc_turn;  metrics.f1_turn = f1_turn;
metrics.acc_slip      = acc_slip;
metrics.f1_slip_1     = f1_slip_1;
metrics.acc_stall     = acc_stall;
metrics.f1_stall_1    = f1_stall_1;
metrics.theta_rmse    = theta_rmse;  metrics.theta_mae = theta_mae;  metrics.theta_bias = theta_bias;
metrics.theta_rmse_slope = theta_rmse_slope;
metrics.delta_rmse    = delta_rmse;  metrics.delta_mae = delta_mae;  metrics.delta_bias = delta_bias;
metrics.pred_theta    = all_pred_theta;
metrics.gt_theta      = all_gt_theta;
metrics.pred_turn     = all_pred_turn;
metrics.gt_turn       = all_gt_turn;
metrics.run_ids       = all_run_ids;

out_dir = fileparts(cfg.out_file);
if ~exist(out_dir, 'dir'); mkdir(out_dir); end
save(cfg.out_file, 'metrics');
fprintf('量化结果已保存至: %s\n', cfg.out_file);


%% ==================== 本地辅助函数 ====================

function cm = confmat3(gt, pred, labels)
%CONFMAT3 构建 3类混淆矩阵，cm(i,j) = GT=labels(i), Pred=labels(j) 的帧数
    n = numel(labels);
    cm = zeros(n, n);
    for i = 1:n
        for j = 1:n
            cm(i,j) = sum(gt == labels(i) & pred == labels(j));
        end
    end
end

function [pr, rc, f1] = prf_from_cm(cm)
%PRF_FROM_CM 从混淆矩阵计算每类 Precision / Recall / F1
    n  = size(cm, 1);
    pr = zeros(n, 1);
    rc = zeros(n, 1);
    f1 = zeros(n, 1);
    for k = 1:n
        tp = cm(k, k);
        fp = sum(cm(:, k)) - tp;
        fn = sum(cm(k, :)) - tp;
        pr(k) = tp / max(tp + fp, 1);
        rc(k) = tp / max(tp + fn, 1);
        f1(k) = 2 * pr(k) * rc(k) / max(pr(k) + rc(k), 1e-9);
    end
end

function [pr, rc, f1] = binf1(gt, pred, pos_label)
%BINF1 二值分类 F1，pos_label 为正类标签
    tp = sum(gt == pos_label & pred == pos_label);
    fp = sum(gt ~= pos_label & pred == pos_label);
    fn = sum(gt == pos_label & pred ~= pos_label);
    pr = tp / max(tp + fp, 1);
    rc = tp / max(tp + fn, 1);
    f1 = 2 * pr * rc / max(pr + rc, 1e-9);
end

function print_cm(cm, names)
%PRINT_CM 以对齐格式打印混淆矩阵
    n = numel(names);
    header = sprintf('%12s', '');
    for j = 1:n; header = [header, sprintf('%10s', names{j})]; end %#ok<AGROW>
    fprintf('%s\n', header);
    for i = 1:n
        row = sprintf('%12s', names{i});
        for j = 1:n; row = [row, sprintf('%10d', cm(i,j))]; end %#ok<AGROW>
        fprintf('%s\n', row);
    end
    fprintf('\n');
end
