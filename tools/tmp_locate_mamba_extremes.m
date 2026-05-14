clear; clc;

root = 'e:/Matlab/Simulink/S-Function_16';
cd(root);
addpath(pwd);
addpath(genpath(fullfile(pwd, 'src')));

cfg.window_size = 128;
cfg.stride = 64;
cfg.train_ratio = 0.80;
cfg.val_ratio = 0.10;

raw_file = fullfile(root, 'data', 'mamba', 'Mamba_train_data_full.mat');
exp_file = fullfile(root, 'data', 'mamba', 'Mamba_dataset_export.mat');

if ~exist(raw_file, 'file')
    error('Raw file not found: %s', raw_file);
end
if ~exist(exp_file, 'file')
    error('Export file not found: %s', exp_file);
end

raw = load(raw_file);
exp = load(exp_file, 'X_train', 'mu', 'sigma', 'channel_info');

if ~isfield(raw, 'data') || ~isfield(raw.data, 'runs')
    error('raw.data.runs missing in raw file.');
end
runs = raw.data.runs;
N_runs = numel(runs);

rng(42);
rand_idx = randperm(N_runs);
N_train = floor(N_runs * cfg.train_ratio);
run_idx_train = rand_idx(1:N_train);

X_train = exp.X_train;
mu = exp.mu;
sigma = exp.sigma;
if isfield(exp, 'channel_info')
    channel_info = exp.channel_info;
else
    channel_info = strings(1, size(X_train, 3));
    for i = 1:size(X_train, 3)
        channel_info(i) = "ch" + string(i);
    end
end

A = abs(X_train);
[max_abs, lin_idx] = max(A(:));
[sample_idx, t_idx, ch_idx] = ind2sub(size(X_train), lin_idx);

run_hit = NaN;
start_hit = NaN;
frame_hit = NaN;
scan_count = 0;
for ii = 1:numel(run_idx_train)
    r = run_idx_train(ii);
    N_frames = size(runs(r).y_mamba, 1);
    if N_frames < cfg.window_size
        continue;
    end
    starts = 1:cfg.stride:(N_frames - cfg.window_size + 1);
    n_win = numel(starts);
    if sample_idx <= scan_count + n_win
        local = sample_idx - scan_count;
        run_hit = r;
        start_hit = starts(local);
        frame_hit = start_hit + t_idx - 1;
        break;
    end
    scan_count = scan_count + n_win;
end

if isnan(run_hit)
    error('Failed to map sample_idx=%d back to train run/window.', sample_idx);
end

raw_val = single(runs(run_hit).y_mamba(frame_hit, ch_idx));
z_check = (raw_val - mu(ch_idx)) / sigma(ch_idx);

fprintf('================ Mamba Extreme Sample定位 ================\n');
fprintf('Train samples: %d, Window: %d, Channels: %d\n', size(X_train,1), size(X_train,2), size(X_train,3));
fprintf('Global max |z| in X_train: %.6f\n', max_abs);
fprintf('Location => sample=%d, t_in_window=%d, ch=%d (%s)\n', ...
    sample_idx, t_idx, ch_idx, string(channel_info(ch_idx)));
fprintf('Back-mapped => run=%d, start_idx=%d, frame_idx=%d\n', run_hit, start_hit, frame_hit);
fprintf('Raw y_mamba value: %.6f, mu: %.6f, sigma: %.6f, recomputed z: %.6f\n', ...
    raw_val, mu(ch_idx), sigma(ch_idx), z_check);

% Channel-wise max and percentile for diagnosis
C = size(X_train, 3);
fprintf('\n---------------- Channel-wise stats (Train, normalized) ----------------\n');
for c = 1:C
    vc = abs(reshape(X_train(:,:,c), [], 1));
    m = max(vc);
    p999 = prctile(vc, 99.9);
    p99 = prctile(vc, 99);
    fprintf('ch=%2d (%-12s) | max=%.4f | p99=%.4f | p99.9=%.4f\n', ...
        c, string(channel_info(c)), m, p99, p999);
end

% Top-K global extremes
K = 15;
[vals, idxs] = maxk(A(:), K);
fprintf('\n---------------- Top-%d global |z| points ----------------\n', K);
for k = 1:K
    [s_k, t_k, c_k] = ind2sub(size(X_train), idxs(k));

    run_k = NaN; start_k = NaN; frame_k = NaN;
    scan_count = 0;
    for ii = 1:numel(run_idx_train)
        r = run_idx_train(ii);
        N_frames = size(runs(r).y_mamba, 1);
        if N_frames < cfg.window_size
            continue;
        end
        starts = 1:cfg.stride:(N_frames - cfg.window_size + 1);
        n_win = numel(starts);
        if s_k <= scan_count + n_win
            local = s_k - scan_count;
            run_k = r;
            start_k = starts(local);
            frame_k = start_k + t_k - 1;
            break;
        end
        scan_count = scan_count + n_win;
    end

    fprintf('#%02d | |z|=%.5f | sample=%d t=%d ch=%d(%s) | run=%d start=%d frame=%d\n', ...
        k, vals(k), s_k, t_k, c_k, string(channel_info(c_k)), run_k, start_k, frame_k);
end

fprintf('==========================================================\n');
