% =============================
% 文件名：GRU_gen_train_data.m
% 版本号：V4.8（强化 slip 可分性：新增轮速-地速失配判据 + 摩擦利用率）
% 最后修改时间：2025-11-22
% 作者：LPV-MPC Project
% 功能描述：
%   通过调用 Simulink 模型 GRU_DataGen.slx 生成 GRU 训练数据
%   支持路径参数随机化、打滑/堵转注入（通过InjectionWrapper）、自动标注
%   V4.2 新增：转弯场景轻度打滑、物理一致启发式(k_torque拟合)、阈值网格搜索
%
% 使用方法：
%   直接运行此脚本：run('GRU_gen_train_data.m') 或在命令行输入 GRU_gen_train_data
%   修改下方"配置区域"来调整参数
%
% 输出：
%   - data: 结构体，保存至 cfg.output_file（默认 GRU_train_data_full.mat）
%       .runs(k): 每回合数据（k=1..N_total）
%           .scene       : 场景名称（字符串）
%           .t           : 时间向量 [Nx1] [s]
%           .u           : 控制输入 [Nx2]=[F_cmd, omega_cmd] [N, rad/s]
%           .y_raw       : 原始输出 [Nx31]（来自 Simulink）
%           .label_main  : 主分类标签 [Nx1]∈{1,2,3,4} (flat/slip/stall/slope)
%           .label_turn  : 转弯状态标签 [Nx1]∈{-1,0,+1} (right/straight/left)
%
% 依赖：
%   - parameters.m
%   - gen_agv_ref_path.m
%   - GRU_DataGen.slx (Simulink 模型)
%
% 备注：
%   - 通过 Simulink 模型生成高保真数据，最大化还原仿真环境
%   - 打滑/堵转通过 InjectionWrapper 实现（不改 Plant/parameters.m）
%   - V4.2: 转弯场景可注入轻度打滑（低概率/低强度），提升泛化覆盖
%   - 标签采用事后计算（基于 y_raw 和注入窗口，优先级：stall→slip→slope→flat）
%   - 打滑启发式采用物理一致模型：accel_expected ≈ (k_torque·I_sum)/mass
%   - 阈值/驻留时间支持小网格搜索，最终值写入 data.meta
% =============================

%% ==================== 配置区域（用户可修改） ====================

root = project_root();
data_gru_dir = fullfile(root, 'data', 'gru');

% 场景列表
cfg.scenes = {'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'};  % 完整数据集（含左右转）
% cfg.scenes = {'straight', 'turn', 'straight_turn', 'slope', 'bumpy'};  % 旧版本：仅左转
% cfg.scenes = {'straight'};  % 快速测试：仅straight场景

% 全局配置
cfg.num_runs = 500;          % 完整数据集：每场景150次【V4.3改进：从100增至150以增加slip/stall样本】
% cfg.num_runs = 1;          % 快速测试：每场景1次
cfg.T_end = 20;              % 每回合仿真时长 [s]
cfg.Ts = 0.05;               % 采样周期 [s]（通常使用 parameters.m 中的值）
cfg.seed = 42;               % 全局随机种子
cfg.noise_on = true;         % 是否开启传感器噪声
cfg.output_file = fullfile(data_gru_dir, 'GRU_train_data_full.mat');  % 完整数据集输出文件
cfg.verbose = true;          % 是否打印进度
cfg.model_name = 'GRU_DataGen';  % Simulink 模型名称

% 噪声配置（V4.9：支持混合噪声策略，增强模型鲁棒性）
cfg.noise_profile = struct();
cfg.noise_profile.mode = 'mixed';      % 'match'：沿用cfg.noise_on；'mixed'：自动混合干净/多级噪声
cfg.noise_profile.clean_ratio = 0.3;   % 混合模式下，30%%回合使用干净数据（enable_noise=false）
cfg.noise_profile.noisy_scales = [1.0, 1.5];  % 噪声标准差缩放系数（>=0），默认含原始+放大噪声
cfg.noise_profile.noisy_probs = [0.6, 0.4];   % 对应概率，可留空=均匀

% 路径参数随机化配置
cfg.path_rand.v0_range = [0.8, 1.2];              % 初速度范围 [m/s]
cfg.path_rand.R_range = [8, 12];                  % 转弯半径范围 [m]
cfg.path_rand.theta_slope_range = [3, 7];        % 坡度角范围 [deg]（符号通过交替机制控制）【V4.7对齐目标路径±5°】
cfg.path_rand.bumpy_amp_range = [deg2rad(3), deg2rad(7)];  % 颠簸振幅范围 [rad]（≈3°~7°）【V4.7对齐目标路径±5°】
cfg.path_rand.turn_trans_range = [0.3, 0.6];     % 转弯过渡时间范围 [s]

% 打滑注入配置（通过InjectionWrapper，降低牵引效率）
% V4.8a: 略微提高打滑注入概率，以增加 slip 训练样本
cfg.slip_cfg.prob = 0.80;                % 打滑概率【从0.70提高到0.80，增强slip覆盖】
cfg.slip_cfg.t_start_range = [5, 12];   % 开始时间范围 [s]【V4.7避开GRU前5s缓冲区】
cfg.slip_cfg.duration_range = [2, 4];   % 持续时间范围 [s]
cfg.slip_cfg.gamma_range = [0.3, 0.7];  % 牵引系数范围（1=正常，<1=打滑）

% 转弯场景轻度打滑配置（V4.2新增）
cfg.slip_in_turn.prob = 0.25;           % 转弯场景打滑概率【V4.3改进：从0.15提高到0.25】
cfg.slip_in_turn.gamma_range = [0.65, 0.85];  % 轻度打滑（接近正常）

% 新版 slip 标注配置（V4.8新增：强化可分性）
cfg.slip_label.I_slip_high_ratio = 0.35;       % slip 高电流判据：I_sum > ratio × I_high_thresh（放宽至≈4A）
cfg.slip_label.accel_slip_small = 0.05;        % slip 加速度上限 [m/s²]（大于stall但明显小于正常）
cfg.slip_label.v_err_thresh = 0.15;            % 轮速-地速偏差阈值 [m/s]（放宽，允许轻度失配）
cfg.slip_label.tire_util_thresh = 0.55;        % 轮胎利用率阈值
cfg.slip_label.slip_min_dwell = 0.3;           % slip 最小持续时间 [s]（略放宽，提高召回）
cfg.slip_label.exclude_stall_margin = 0.2;     % 排除 stall 附近的边界 [s]


% 堵转注入配置（通过InjectionWrapper，施加外部负载）
cfg.stall_cfg.prob = 0.80;                 % 堵转概率【V4.3改进：从0.2提高到0.4，以后进一步提高到0.8增强stall覆盖】
cfg.stall_cfg.t_start_range = [12, 17];   % 开始时间范围 [s]【V4.7后移1s，减少与slip窗口重叠】
cfg.stall_cfg.duration_range = [1.5, 3];  % 持续时间范围 [s]
cfg.stall_cfg.load_range = [200, 300];    % 外部负载范围 [N]

% 打滑启发式配置（V4.2新增）
cfg.slip_heuristic.k_torque = [];  % 电机扭矩常数 [N/(A·kg)]，空=自动拟合
% V4.5d: 多场景统一拟合（全局最优）
cfg.slip_heuristic.fit_scenes = {'straight_turn', 'slope', 'bumpy'};  % 拟合场景列表
cfg.slip_heuristic.fit_runs_per_scene = 2;  % 每个场景回合数（总共2×3=6回合）

% 阈值网格搜索配置（V4.2新增，空=使用默认值）
cfg.label_search.enabled = false;   % 是否启用阈值搜索（耗时，首次运行建议false）
cfg.label_search.I_high_grid = [10, 12, 14];  % 高电流阈值候选 [A]
cfg.label_search.accel_stall_grid = [0.015, 0.02, 0.025];  % 堵转加速度阈值 [m/s²]
cfg.label_search.stall_dwell_grid = [0.8, 1.0, 1.2];  % 堵转驻留时间 [s]

%% ==================== 主程序（自动执行，无需修改） ====================

% 加载 AGV 参数
params = parameters();

% 将配置转换为 opts 结构体（兼容原有逻辑）
scenes = cfg.scenes;
opts = struct();
opts.num_runs = cfg.num_runs;
opts.T_end = cfg.T_end;
opts.Ts = cfg.Ts;
opts.seed = cfg.seed;
opts.noise_on = cfg.noise_on;
opts.path_rand = cfg.path_rand;
opts.slip_cfg = cfg.slip_cfg;
opts.slip_in_turn = cfg.slip_in_turn;  % V4.2
opts.stall_cfg = cfg.stall_cfg;
opts.slip_heuristic = cfg.slip_heuristic;  % V4.2
opts.label_search = cfg.label_search;  % V4.2
opts.save_path = cfg.output_file;
opts.verbose = cfg.verbose;
opts.model_name = cfg.model_name;
opts.noise_profile = cfg.noise_profile;

% V4.8a: 为向后兼容增加 slip_label 默认配置
if isfield(cfg, 'slip_label')
    opts.slip_label = cfg.slip_label;
else
    opts.slip_label = struct();
end

%% 参数处理与默认值（保留原有逻辑）

% 全局配置
num_runs = getFieldOrDefault(opts, 'num_runs', 10);
T_end = getFieldOrDefault(opts, 'T_end', 20.0);
Ts = getFieldOrDefault(opts, 'Ts', 0.05);
seed = getFieldOrDefault(opts, 'seed', 42);
noise_on = getFieldOrDefault(opts, 'noise_on', true);
save_path = getFieldOrDefault(opts, 'save_path', fullfile(data_gru_dir, 'GRU_train_data_full.mat'));
verbose = getFieldOrDefault(opts, 'verbose', true);
model_name = getFieldOrDefault(opts, 'model_name', 'GRU_DataGen');
noise_profile_cfg = getFieldOrDefault(opts, 'noise_profile', struct());
noise_profile_mode = getFieldOrDefault(noise_profile_cfg, 'mode', 'match');

% 路径参数随机化范围
path_rand = getFieldOrDefault(opts, 'path_rand', struct());
v0_range = getFieldOrDefault(path_rand, 'v0_range', [0.8, 1.2]);
R_range = getFieldOrDefault(path_rand, 'R_range', [8, 12]);
theta_slope_range = getFieldOrDefault(path_rand, 'theta_slope_range', [3, 7]);  % deg（幅值范围，符号由交替机制控制）【V4.7】
bumpy_amp_range = getFieldOrDefault(path_rand, 'bumpy_amp_range', [deg2rad(3), deg2rad(7)]);  % rad（≈3°~7°）【V4.7】
turn_trans_range = getFieldOrDefault(path_rand, 'turn_trans_range', [0.3, 0.6]);

% 打滑注入配置
slip_cfg = getFieldOrDefault(opts, 'slip_cfg', struct());
slip_prob = getFieldOrDefault(slip_cfg, 'prob', 0.3);
slip_t_start_range = getFieldOrDefault(slip_cfg, 't_start_range', [5, 12]);  % 避开GRU缓冲区【V4.7】
slip_duration_range = getFieldOrDefault(slip_cfg, 'duration_range', [2, 4]);
slip_gamma_range = getFieldOrDefault(slip_cfg, 'gamma_range', [0.3, 0.7]);  % 牵引系数（无量纲）

% 转弯场景轻度打滑配置（V4.2）
slip_in_turn = getFieldOrDefault(opts, 'slip_in_turn', struct());
slip_in_turn_prob = getFieldOrDefault(slip_in_turn, 'prob', 0.15);
slip_in_turn_gamma_range = getFieldOrDefault(slip_in_turn, 'gamma_range', [0.65, 0.85]);

% 堵转注入配置
stall_cfg = getFieldOrDefault(opts, 'stall_cfg', struct());
stall_prob = getFieldOrDefault(stall_cfg, 'prob', 0.2);
stall_t_start_range = getFieldOrDefault(stall_cfg, 't_start_range', [12, 17]);  % 后移减少窗口重叠【V4.7】
stall_duration_range = getFieldOrDefault(stall_cfg, 'duration_range', [1.5, 3]);
stall_load_range = getFieldOrDefault(stall_cfg, 'load_range', [200, 300]);  % N

% 打滑启发式配置（V4.2）
slip_heuristic = getFieldOrDefault(opts, 'slip_heuristic', struct());
k_torque = getFieldOrDefault(slip_heuristic, 'k_torque', []);  % 空=自动拟合
% V4.5d: 支持多场景拟合
fit_scenes = getFieldOrDefault(slip_heuristic, 'fit_scenes', {'straight_turn', 'slope', 'bumpy'});
fit_runs_per_scene = getFieldOrDefault(slip_heuristic, 'fit_runs_per_scene', 2);

% 阈值网格搜索配置（V4.2）
label_search = getFieldOrDefault(opts, 'label_search', struct());
search_enabled = getFieldOrDefault(label_search, 'enabled', false);
I_high_grid = getFieldOrDefault(label_search, 'I_high_grid', [10, 12, 14]);
accel_stall_grid = getFieldOrDefault(label_search, 'accel_stall_grid', [0.015, 0.02, 0.025]);
stall_dwell_grid = getFieldOrDefault(label_search, 'stall_dwell_grid', [0.8, 1.0, 1.2]);

%% 初始化
rng(seed);  % 固定随机种子
N_scenes = length(scenes);
N_total = N_scenes * num_runs;

% 预分配
data.runs = struct('scene', {}, 't', {}, 'u', {}, 'y_raw', {}, ...
              'label_main', {}, 'label_turn', {}, 'theta', {}, 'meta', {});

% 检查 Simulink 模型
if ~bdIsLoaded(model_name)
    if verbose
        fprintf('正在加载 Simulink 模型: %s\n', model_name);
    end
    load_system(model_name);
end

%% V4.2: k_torque 自动拟合（如果未提供）
if isempty(k_torque)
    if verbose
        fprintf('\n========================================\n');
        fprintf('计算 k_torque（从物理参数）...\n');
        fprintf('========================================\n');
    end
    % V4.7: 使用物理参数直接计算（避免拟合误差）
    % 关键修复：k_torque应基于 F_drive（总驱动力），而非 F_net（净推进力）
    % 物理关系：F_drive = I_sum * (k_t * eta * n / r) 对于2个驱动轮
    k_t = params.motor_torque_constant;  % [N·m/A]
    eta = params.gear_efficiency;        % [-]
    n = params.gear_ratio;               % [-]
    r = params.wheel_radius;             % [m]
    k_torque = (k_t * eta * n) / r;      % [N/A] 单轮转换系数
    if verbose
        fprintf('✓ k_torque = %.6f [N/A]（单轮）\n', k_torque);
        fprintf('  物理参数: k_t=%.2f N·m/A, n=%.1f, eta=%.2f, r=%.3f m\n', ...
            k_t, n, eta, r);
        fprintf('  对于2个驱动轮: F_total = %.2f * I_sum [N]\n', k_torque);
    end
end

%% V4.2: 阈值网格搜索（如果启用）
best_thresholds = struct();
if search_enabled
    if verbose
        fprintf('\n========================================\n');
        fprintf('正在进行阈值网格搜索...\n');
        fprintf('网格大小: %d×%d×%d = %d 组合\n', ...
            length(I_high_grid), length(accel_stall_grid), length(stall_dwell_grid), ...
            length(I_high_grid)*length(accel_stall_grid)*length(stall_dwell_grid));
    fprintf('========================================\n');
    end
    best_thresholds = search_optimal_thresholds(...
        I_high_grid, accel_stall_grid, stall_dwell_grid, ...
        scenes, num_runs, params, T_end, Ts, ...
        v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
        slip_prob, slip_t_start_range, slip_duration_range, slip_gamma_range, ...
        slip_in_turn_prob, slip_in_turn_gamma_range, ...
        stall_prob, stall_t_start_range, stall_duration_range, stall_load_range, ...
        k_torque, model_name, verbose);
    if verbose
        fprintf('✓ 阈值搜索完成\n');
        fprintf('  最优 I_high_thresh: %.2f A\n', best_thresholds.I_high_thresh);
        fprintf('  最优 accel_stall_thresh: %.4f m/s²\n', best_thresholds.accel_stall_thresh);
        fprintf('  最优 stall_dwell: %.2f s\n', best_thresholds.stall_dwell);
    end
else
    % 使用默认阈值
    best_thresholds.I_high_thresh = 12.0;
    best_thresholds.accel_stall_thresh = 0.02;
    best_thresholds.stall_dwell = 1.0;
    
    % V4.8: 新增 slip 标注阈值（从配置读取）
    best_thresholds.I_slip_high_ratio = opts.slip_label.I_slip_high_ratio;
    best_thresholds.accel_slip_small = opts.slip_label.accel_slip_small;
    best_thresholds.v_err_thresh = opts.slip_label.v_err_thresh;
    best_thresholds.tire_util_thresh = opts.slip_label.tire_util_thresh;
    best_thresholds.slip_min_dwell = opts.slip_label.slip_min_dwell;
    best_thresholds.exclude_stall_margin = opts.slip_label.exclude_stall_margin;
end

%% 批量生成数据
run_idx = 0;
for s_idx = 1:N_scenes
    scene = scenes{s_idx};
    
    if verbose
        fprintf('\n========================================\n');
        fprintf('场景 [%d/%d]: %s\n', s_idx, N_scenes, scene);
        fprintf('========================================\n');
    end
    
    for run = 1:num_runs
        run_idx = run_idx + 1;
        
        if verbose
            fprintf('  回合 [%d/%d] (总进度: %d/%d)... ', run, num_runs, run_idx, N_total);
        end
        
        try
            % 1. 生成参考路径和注入信号（不改theta_ref）
            [ref_path, inj_signal, inject_info] = generate_reference_path(...
                scene, params, T_end, Ts, ...
                v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
                slip_prob, slip_t_start_range, slip_duration_range, slip_gamma_range, ...
                slip_in_turn_prob, slip_in_turn_gamma_range, ...  % V4.2
                stall_prob, stall_t_start_range, stall_duration_range, stall_load_range);
            
            % 2. 配置 Simulink 模型
            [enable_noise_run, noise_std_scale, noise_variant] = resolveNoiseProfile( ...
                noise_profile_mode, noise_profile_cfg, noise_on);

            params_sim = params;
            params_sim.enable_noise = enable_noise_run;
            if enable_noise_run
                noise_std_scale = max(noise_std_scale, 0);
                params_sim.current_noise_std = params.current_noise_std * noise_std_scale;
                params_sim.wheel_speed_noise_std = params.wheel_speed_noise_std * noise_std_scale;
                params_sim.disturbance_noise_std = params.disturbance_noise_std * noise_std_scale;
            else
                noise_std_scale = 0;
            end
            
            % 设置仿真参数
            set_param(model_name, 'StopTime', num2str(T_end));
            set_param(model_name, 'FixedStep', num2str(Ts));
            
            % 将参数、路径和注入信号加载到 base workspace
            assignin('base', 'params', params_sim);
            assignin('base', 'ref_path', ref_path);
            assignin('base', 'inj_signal', inj_signal);
            
            % 3. 运行仿真（静默模式）
            warning('off', 'all');  % 临时关闭警告
            sim_out = sim(model_name, 'ReturnWorkspaceOutputs', 'on', ...
                         'SimulationMode', 'normal', 'CaptureErrors', 'on');
            warning('on', 'all');  % 恢复警告
            
            % 4. 提取数据（根据你的模型结构）
            % 从 SimulationOutput 对象中提取
            if isa(sim_out, 'Simulink.SimulationOutput')
                % 时间向量
                t = sim_out.tout;
                
                % y_raw (struct with signals)
                if isstruct(sim_out.y_raw) && isfield(sim_out.y_raw, 'signals')
                    y_raw = sim_out.y_raw.signals.values;
                else
                    error('y_raw 格式不正确');
                end
                
                % u (struct with signals)
                if isstruct(sim_out.u) && isfield(sim_out.u, 'signals')
                    u = sim_out.u.signals.values;
                else
                    error('u 格式不正确');
                end
                
                % theta (struct with signals)
                if isstruct(sim_out.theta) && isfield(sim_out.theta, 'signals')
                    theta = sim_out.theta.signals.values;
                else
                    error('theta 格式不正确');
                end
            else
                error('sim_out 类型不是 SimulationOutput');
            end
            
            % 5. 数据验证
            N = length(t);
            if size(y_raw, 1) ~= N || size(y_raw, 2) ~= 31
                error('y_raw 维度错误: 期望 [%d×31], 实际 [%d×%d]', N, size(y_raw,1), size(y_raw,2));
            end
            if size(u, 1) ~= N || size(u, 2) ~= 2
                error('u 维度错误: 期望 [%d×2], 实际 [%d×%d]', N, size(u,1), size(u,2));
            end
            if size(theta, 1) ~= N || size(theta, 2) ~= 1
                error('theta 维度错误: 期望 [%d×1], 实际 [%d×%d]', N, size(theta,1), size(theta,2));
            end
            
            % 6. 生成标签（事后计算）
            [label_main, label_turn] = generate_labels(...
                t, y_raw, theta, ref_path.omega_ref, inject_info, Ts, ...
                k_torque, params.mass, best_thresholds);  % V4.2
            
            % 7. 保存当前回合数据
            data.runs(run_idx).scene = scene;
            data.runs(run_idx).t = t;
            data.runs(run_idx).u = u;
            data.runs(run_idx).y_raw = y_raw;
            data.runs(run_idx).label_main = label_main;
            data.runs(run_idx).label_turn = label_turn;
            data.runs(run_idx).theta = theta;
            data.runs(run_idx).meta.inject_info = inject_info;
            data.runs(run_idx).meta.path_params = ref_path.meta;
            data.runs(run_idx).meta.noise_on = enable_noise_run;
            data.runs(run_idx).meta.noise = struct( ...
                'mode', noise_profile_mode, ...
                'enable_noise', enable_noise_run, ...
                'std_scale', noise_std_scale, ...
                'variant', noise_variant);
            data.runs(run_idx).meta.run_idx = run_idx;
            data.runs(run_idx).meta.seed = seed + run_idx;  % 每回合独立种子
            
            if verbose
                fprintf('✓ (N=%d, 主类别分布: flat=%d, slip=%d, stall=%d, slope=%d)\n', ...
                    N, sum(label_main==1), sum(label_main==2), sum(label_main==3), sum(label_main==4));
            end
            
        catch ME
            if verbose
                fprintf('✗ 失败: %s\n', ME.message);
            end
            warning('GRU_gen_train_data:SimFailed', ...
                '场景 %s 回合 %d 仿真失败: %s', scene, run, ME.message);
            continue;
        end
    end
end

%% 保存全局元数据
data.meta.generation_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
data.meta.version = 'V4.2';
data.meta.author = 'LPV-MPC Project';
data.meta.model_name = model_name;
data.meta.scenes = scenes;
data.meta.num_runs_per_scene = num_runs;
data.meta.T_end = T_end;
data.meta.Ts = Ts;
data.meta.seed = seed;
data.meta.noise_on = noise_on;
data.meta.noise_profile = struct('mode', noise_profile_mode, 'config', noise_profile_cfg);
data.meta.path_rand = path_rand;
data.meta.slip_cfg = slip_cfg;
data.meta.slip_in_turn = slip_in_turn;  % V4.2
data.meta.stall_cfg = stall_cfg;
data.meta.k_torque = k_torque;  % V4.2
data.meta.thresholds = best_thresholds;  % V4.2
data.meta.label_search_enabled = search_enabled;  % V4.2

%% 保存数据
if verbose
    fprintf('\n========================================\n');
    fprintf('数据生成完成！总回合数: %d\n', run_idx);
    fprintf('正在保存到: %s\n', save_path);
end

save(save_path, 'data', '-v7.3');

if verbose
    fprintf('✓ 保存成功！\n');
    fprintf('========================================\n');
end

%% ========== 子函数（内部使用） ==========

function [ref_path, inj_signal, inject_info] = generate_reference_path(...
    scene, params, T_end, Ts, ...
    v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
    slip_prob, slip_t_start_range, slip_duration_range, slip_gamma_range, ...
    slip_in_turn_prob, slip_in_turn_gamma_range, ...  % V4.2
    stall_prob, stall_t_start_range, stall_duration_range, stall_load_range)
% 生成参考路径和注入信号（不改theta_ref）
%
% 输出:
%   - ref_path: gen_agv_ref_path 返回的结构体（theta_ref保持原样）
%   - inj_signal: 注入信号时序（From Workspace格式）
%       .time: 时间向量 [Nx1]
%       .signals.values: [Nx2]=[slip_gamma, stall_load]
%   - inject_info: 注入信息结构体
%       .slip_injected: 是否注入打滑 (true/false)
%       .slip_window: [t_start, t_end] (如果注入)
%       .slip_gamma: 牵引系数 (如果注入)
%       .stall_injected: 是否注入堵转 (true/false)
%       .stall_window: [t_start, t_end] (如果注入)
%       .stall_load: 外部负载 [N] (如果注入)

% V4.6: 使用persistent变量强制slope场景正负坡度50-50平衡
persistent slope_sign_counter;
if isempty(slope_sign_counter)
    slope_sign_counter = 1;  % 初始化：1=正坡，-1=负坡
end

%% 路径参数随机化
opts = struct();
opts.T_end = T_end;
opts.v0 = v0_range(1) + (v0_range(2) - v0_range(1)) * rand();
opts.R = R_range(1) + (R_range(2) - R_range(1)) * rand();
opts.turn_transition = turn_trans_range(1) + (turn_trans_range(2) - turn_trans_range(1)) * rand();

% 根据场景设置特定参数
switch lower(scene)
    case 'slope'
        % V4.7: 强制正负坡度交替，范围调整为 [3,7]° 对齐目标路径 ±5°
        % 坡度范围确保绝对值 >= 3° (高于slope标注阈值2°)
        theta_abs = theta_slope_range(1) + (theta_slope_range(2) - theta_slope_range(1)) * rand();  % [3, 7]°
        theta_sign = slope_sign_counter;  % 使用计数器决定符号，不再随机
        theta_deg = theta_sign * theta_abs;
        opts.theta_slope = deg2rad(theta_deg);
        % 交替符号（下次生成相反坡度）
        slope_sign_counter = -slope_sign_counter;
    case 'bumpy'
        opts.bumpy_amp = bumpy_amp_range(1) + (bumpy_amp_range(2) - bumpy_amp_range(1)) * rand();
    case {'turn_left', 'turn'}
        % 左转（逆时针）：omega_ref > 0（默认行为）
        opts.turn_direction = 'left';  % 标记为左转（可选）
    case 'turn_right'
        % 右转（顺时针）：需要传递给 gen_agv_ref_path
        opts.turn_direction = 'right';  % 标记为右转
    otherwise
        % straight, straight_turn: 使用默认值
end

%% 打滑/堵转注入决策
inject_info = struct();
inject_info.slip_injected = false;
inject_info.stall_injected = false;

% 判断是否为转弯场景
is_turn_scene = strcmpi(scene, 'turn') || contains(lower(scene), 'turn');

% 打滑注入（V4.2: 转弯场景使用轻度打滑，非转弯场景使用常规打滑）
if is_turn_scene
    % 转弯场景：轻度打滑（低概率、低强度）
    if rand() < slip_in_turn_prob
        inject_info.slip_injected = true;
        t_start = slip_t_start_range(1) + (slip_t_start_range(2) - slip_t_start_range(1)) * rand();
        duration = slip_duration_range(1) + (slip_duration_range(2) - slip_duration_range(1)) * rand();
        inject_info.slip_window = [t_start, min(t_start + duration, T_end - 1)];
        inject_info.slip_gamma = slip_in_turn_gamma_range(1) + ...
            (slip_in_turn_gamma_range(2) - slip_in_turn_gamma_range(1)) * rand();
    end
else
    % 非转弯场景：常规打滑
    if rand() < slip_prob
        inject_info.slip_injected = true;
        t_start = slip_t_start_range(1) + (slip_t_start_range(2) - slip_t_start_range(1)) * rand();
        duration = slip_duration_range(1) + (slip_duration_range(2) - slip_duration_range(1)) * rand();
        inject_info.slip_window = [t_start, min(t_start + duration, T_end - 1)];
        inject_info.slip_gamma = slip_gamma_range(1) + (slip_gamma_range(2) - slip_gamma_range(1)) * rand();
    end
end

% 堵转注入（所有场景均可）
if rand() < stall_prob
    inject_info.stall_injected = true;
    t_start = stall_t_start_range(1) + (stall_t_start_range(2) - stall_t_start_range(1)) * rand();
    duration = stall_duration_range(1) + (stall_duration_range(2) - stall_duration_range(1)) * rand();
    inject_info.stall_window = [t_start, min(t_start + duration, T_end - 1)];
    inject_info.stall_load = stall_load_range(1) + (stall_load_range(2) - stall_load_range(1)) * rand();
    
    % 如果堵转和打滑时间窗口冲突，取消打滑
    if inject_info.slip_injected
        if ~(inject_info.slip_window(2) < inject_info.stall_window(1) || ...
             inject_info.slip_window(1) > inject_info.stall_window(2))
            inject_info.slip_injected = false;  % 冲突，取消打滑
        end
        end
    end
    
%% 生成基础路径（不修改theta_ref）
% 将 turn_left/turn_right 映射为 turn（gen_agv_ref_path统一处理turn场景）
scene_for_path = scene;
if strcmpi(scene, 'turn_left') || strcmpi(scene, 'turn_right')
    scene_for_path = 'turn';
end
ref_path = gen_agv_ref_path(scene_for_path, params, opts);

%% 生成注入信号时序
t = ref_path.t;
N = length(t);

% 初始化注入信号（默认值：slip_gamma=1.0, stall_load=0.0）
slip_gamma_vec = ones(N, 1);     % 1.0 = 正常牵引
stall_load_vec = zeros(N, 1);    % 0.0 = 无外部负载

% 打滑注入：在窗口内降低牵引系数
if inject_info.slip_injected
    for i = 1:N
        if t(i) >= inject_info.slip_window(1) && t(i) <= inject_info.slip_window(2)
            slip_gamma_vec(i) = inject_info.slip_gamma;
        end
    end
end

% 堵转注入：在窗口内施加外部负载
if inject_info.stall_injected
    for i = 1:N
        if t(i) >= inject_info.stall_window(1) && t(i) <= inject_info.stall_window(2)
            stall_load_vec(i) = inject_info.stall_load;
        end
    end
end

% 构建 From Workspace 格式
inj_signal.time = t;
inj_signal.signals.values = [slip_gamma_vec, stall_load_vec];  % [Nx2]
inj_signal.signals.dimensions = 2;

end


function [label_main, label_turn] = generate_labels(...
    t, y_raw, theta, omega_ref, inject_info, Ts, ...
    k_torque, mass, thresholds)  % V4.2
% 事后生成标签
%
% 输入:
%   - t: 时间向量 [Nx1]
%   - y_raw: 原始输出 [Nx31]
%   - theta: 坡度角真值 [Nx1]
%   - omega_ref: 参考角速度 [Nx1]
%   - inject_info: 注入信息
%   - Ts: 采样周期
%   - k_torque: 电机扭矩常数 [N/(A·kg)] (V4.2)
%   - mass: 车辆质量 [kg] (V4.2)
%   - thresholds: 阈值结构体 (V4.2)
%
% 输出:
%   - label_main: 主分类标签 [Nx1]∈{1,2,3,4}
%       1: flat, 2: slip, 3: stall, 4: slope
%   - label_turn: 转弯状态标签 [Nx1]∈{-1,0,+1}
%       -1: right, 0: straight, +1: left

N = length(t);

%% 主分类标注（优先级递减：stall → slip → slope → flat）
label_main = ones(N, 1);  % 默认 flat

% 阈值定义（V4.2: 从 thresholds 结构体获取）
theta_slope_thresh = deg2rad(2);     % 坡度阈值 2°
I_high_thresh = thresholds.I_high_thresh;        % 高电流阈值 [A]
omega_wheel_stall_thresh = 0.1;      % 堵转轮速阈值 [rad/s]
accel_stall_thresh = thresholds.accel_stall_thresh;  % 堵转加速度阈值 [m/s²]
stall_duration_thresh = thresholds.stall_dwell;  % 堵转最小持续时间 [s]
dwell_time = 0.5;                    % 最小驻留时间 [s]
dwell_steps = max(1, round(dwell_time / Ts));
stall_dwell_steps = max(1, round(stall_duration_thresh / Ts));

% 提取关键通道
I_lf = y_raw(:, 12);          % y12: I_meas_lf
I_rr = y_raw(:, 13);          % y13: I_meas_rr
I_sum = abs(I_lf) + abs(I_rr);
omega_wheel_lf = y_raw(:, 17); % y17: omega_wheel_lf
omega_wheel_rr = y_raw(:, 18); % y18: omega_wheel_rr
accel_x = y_raw(:, 9);        % y9: accel_x_meas

% 1) Stall 标注（最高优先级）
% 方法1: 基于注入窗口
if inject_info.stall_injected
    t_start = inject_info.stall_window(1);
    t_end = inject_info.stall_window(2);
    for i = 1:N
        if t(i) >= t_start && t(i) <= t_end
            label_main(i) = 3;  % stall
        end
    end
end

% 方法2: 基于启发式（I_sum 高 + omega_wheel 低 + accel_x 低 + 持续时间足够长）
stall_heuristic = (I_sum > I_high_thresh) & ...
                  (abs(omega_wheel_lf) < omega_wheel_stall_thresh) & ...
                  (abs(omega_wheel_rr) < omega_wheel_stall_thresh) & ...
                  (abs(accel_x) < accel_stall_thresh);
% 使用更长的驻留时间（1.0s）避免瞬态误判
stall_heuristic = apply_dwell_time(stall_heuristic, stall_dwell_steps);
for i = 1:N
    if stall_heuristic(i) && label_main(i) == 1
        label_main(i) = 3;  % stall
    end
end

% 2) Slip 标注（次高优先级）
% V4.8: 新增强约束 slip 判定（宁少勿滥）
%
% 核心思路：
%   1. 注入窗口作为候选区间（初步筛选）
%   2. 轮速-地速失配（v_hat - v_true > thresh）
%   3. 高驱动但低加速度（I_sum 高 + accel_x_lp 低）
%   4. 轮胎利用率接近饱和（tire_util > thresh）
%   5. 排除 stall 边界，避免与 stall 混淆
%   6. 最小持续时间筛选，过滤短促噪声
%
% 目标：让 slip 类样本在特征空间中明显偏离 flat/slope

% 提取 slip 判定所需的额外通道
v_true = y_raw(:, 4);                % y4: 车辆真实纵向速度 [m/s]
r = 0.075;                           % 轮半径 [m]（从 parameters.m 读取）
v_hat = r * (abs(omega_wheel_lf) + abs(omega_wheel_rr)) / 2;
v_err = v_hat - v_true;              % 轮速-地速偏差

tire_util_lf = y_raw(:, 22);         % y22: 左前轮摩擦利用率
tire_util_rr = y_raw(:, 23);         % y23: 右后轮摩擦利用率
tire_util_max = max(tire_util_lf, tire_util_rr);

% 计算 accel_x_lp（平滑加速度，与特征提取一致）
alpha_lp = Ts / (0.4 + Ts);
accel_x_lp = zeros(N, 1);
accel_x_lp(1) = accel_x(1);
for i = 2:N
    accel_x_lp(i) = alpha_lp * accel_x(i) + (1 - alpha_lp) * accel_x_lp(i-1);
end

% slip 判据阈值（从 thresholds 获取）
I_slip_high = thresholds.I_slip_high_ratio * I_high_thresh;  % 例如 0.6 × 12A = 7.2A
accel_slip_small = thresholds.accel_slip_small;              % 0.05 m/s²
v_err_thresh = thresholds.v_err_thresh;                      % 0.3 m/s
tire_util_thresh = thresholds.tire_util_thresh;              % 0.75
slip_min_dwell_steps = max(1, round(thresholds.slip_min_dwell / Ts));
exclude_margin_steps = max(1, round(thresholds.exclude_stall_margin / Ts));

% 构建 slip 候选掩码（多条件联合）
slip_candidate = false(N, 1);

% 条件1：在注入窗口内（粗筛）
if inject_info.slip_injected
    t_start = inject_info.slip_window(1);
    t_end = inject_info.slip_window(2);
    for i = 1:N
        if t(i) >= t_start && t(i) <= t_end
            slip_candidate(i) = true;
        end
    end
end

% 条件2：在候选区间内进一步检查物理特征
for i = 1:N
    if ~slip_candidate(i)
        continue;  % 跳过非候选点
    end
    
    % 2a) 轮速-地速失配（打滑核心特征）
    v_mismatch = (v_err(i) > v_err_thresh);
    
    % 2b) 高驱动但低加速度（动力-加速度失配）
    power_mismatch = (I_sum(i) > I_slip_high) && (abs(accel_x_lp(i)) < accel_slip_small);
    
    % 2c) 轮胎利用率接近饱和（摩擦力接近极限）
    tire_saturated = (tire_util_max(i) > tire_util_thresh);
    
    % 2d) 非堵转条件（轮速不能太低）
    not_stalled = (abs(omega_wheel_lf(i)) > omega_wheel_stall_thresh) && ...
                  (abs(omega_wheel_rr(i)) > omega_wheel_stall_thresh);
    
    % 综合判定：至少满足 v_mismatch + (power_mismatch OR tire_saturated) + not_stalled
    if v_mismatch && (power_mismatch || tire_saturated) && not_stalled
        % 继续保持候选
    else
        slip_candidate(i) = false;  % 不满足物理特征，排除
    end
end

% 条件3：排除 stall 边界附近（避免混淆）
if inject_info.stall_injected
    stall_start_idx = find(t >= inject_info.stall_window(1), 1);
    stall_end_idx = find(t <= inject_info.stall_window(2), 1, 'last');
    if ~isempty(stall_start_idx) && ~isempty(stall_end_idx)
        exclude_range = max(1, stall_start_idx - exclude_margin_steps) : ...
                        min(N, stall_end_idx + exclude_margin_steps);
        slip_candidate(exclude_range) = false;
    end
end

% 条件4：应用最小驻留时间（过滤短促噪声）
slip_candidate = apply_dwell_time(slip_candidate, slip_min_dwell_steps);

% Fallback: 若已注入但无样本通过物理判据，则退化为窗口内全标注
if inject_info.slip_injected && ~any(slip_candidate)
    in_window = (t >= inject_info.slip_window(1)) & (t <= inject_info.slip_window(2));
    slip_candidate(in_window) = true;
end

% 最终标注：只标记满足所有条件且当前为 flat 的样本
for i = 1:N
    if slip_candidate(i) && label_main(i) == 1
        label_main(i) = 2;  % slip
    end
end

% 3) Slope 标注（第三优先级，不会覆盖stall/slip）
for i = 1:N
    if abs(theta(i)) >= theta_slope_thresh && label_main(i) == 1
        label_main(i) = 4;  % slope
    end
end

%% 转弯状态标注
label_turn = zeros(N, 1);  % 默认 straight

omega_turn_thresh = 0.05;  % 转弯角速度阈值 [rad/s]
turn_dwell_steps = max(1, round(0.40 / Ts));  % 转弯驻留时间 0.40s（与在线推理一致）

% 基于 omega_ref 判定
turn_left = omega_ref > omega_turn_thresh;
turn_right = omega_ref < -omega_turn_thresh;

% 应用驻留时间
turn_left = apply_dwell_time(turn_left, turn_dwell_steps);
turn_right = apply_dwell_time(turn_right, turn_dwell_steps);

for i = 1:N
    if turn_left(i)
        label_turn(i) = 1;   % left (逆时针)
    elseif turn_right(i)
        label_turn(i) = -1;  % right (顺时针)
    end
end

end


function signal_filtered = apply_dwell_time(signal, dwell_steps)
% 应用最小驻留时间滤波
% 输入:
%   - signal: 布尔向量 [Nx1]
%   - dwell_steps: 最小驻留步数
% 输出:
%   - signal_filtered: 滤波后的布尔向量 [Nx1]

N = length(signal);
signal_filtered = signal;

% 前向遍历：去除短暂的高电平脉冲
in_state = false;
state_count = 0;

for i = 1:N
    if signal(i)
        if ~in_state
            in_state = true;
            state_start = i;
            state_count = 1;
        else
            state_count = state_count + 1;
        end
    else
        if in_state
            % 状态结束，检查持续时间
            if state_count < dwell_steps
                % 持续时间不足，清零
                signal_filtered(state_start:i-1) = false;
            end
            in_state = false;
            state_count = 0;
        end
    end
end

% 处理末尾未结束的状态
if in_state && state_count < dwell_steps
    signal_filtered(state_start:end) = false;
end

end


function [enable_noise, noise_std_scale, variant] = resolveNoiseProfile(mode, cfg, default_noise_on)
% 根据噪声配置决定当前回合的噪声开关与强度
if nargin < 3 || isempty(default_noise_on)
    default_noise_on = true;
end

if nargin < 2 || isempty(cfg)
    cfg = struct();
end

if nargin < 1 || isempty(mode)
    mode = 'match';
end

switch lower(mode)
    case 'match'
        enable_noise = logical(default_noise_on);
        if enable_noise
            noise_std_scale = 1.0;
            variant = 'match-default';
        else
            noise_std_scale = 0;
            variant = 'clean';
        end
    case 'mixed'
        clean_ratio = getFieldOrDefault(cfg, 'clean_ratio', 0.3);
        clean_ratio = min(max(clean_ratio, 0), 1);

        noisy_scales = getFieldOrDefault(cfg, 'noisy_scales', 1.0);
        if isempty(noisy_scales)
            noisy_scales = 1.0;
        end
        noisy_scales = max(noisy_scales(:)', 0);

        noisy_probs = getFieldOrDefault(cfg, 'noisy_probs', []);
        if isempty(noisy_probs) || numel(noisy_probs) ~= numel(noisy_scales)
            noisy_probs = ones(size(noisy_scales));
        else
            noisy_probs = noisy_probs(:)';
        end
        prob_sum = sum(noisy_probs);
        if prob_sum <= 0
            noisy_probs = ones(size(noisy_scales));
            prob_sum = sum(noisy_probs);
        end
        noisy_probs = noisy_probs / prob_sum;

        if rand() < clean_ratio
            enable_noise = false;
            noise_std_scale = 0;
            variant = 'clean';
        else
            enable_noise = true;
            r = rand();
            cdf = cumsum(noisy_probs);
            idx = find(r <= cdf, 1, 'first');
            if isempty(idx)
                idx = numel(noisy_scales);
            end
            noise_std_scale = noisy_scales(idx);
            variant = sprintf('noisy_x%.2f', noise_std_scale);
        end
    otherwise
        warning('GRU_gen_train_data:UnknownNoiseMode', ...
            '未知噪声模式 "%s"，回退到 match 行为。', mode);
        [enable_noise, noise_std_scale, variant] = resolveNoiseProfile('match', cfg, default_noise_on);
end
end


function value = getFieldOrDefault(s, fieldname, default_value)
% 安全获取结构体字段，若不存在则返回默认值
if isfield(s, fieldname)
    value = s.(fieldname);
else
    value = default_value;
end
end


function k_torque = fit_k_torque_from_sim(scenes, runs_per_scene, params, T_end, Ts, ...
    v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
    model_name, verbose)
% V4.5d: 通过多场景仿真数据拟合 k_torque（电机扭矩常数）
%
% 策略：从多个场景（straight_turn, slope, bumpy）收集数据，统一最小二乘拟合
%       获得全局最优k_torque，适用于所有工况
%
% 输入：
%   scenes: cell array, 场景列表（如{'straight_turn', 'slope', 'bumpy'}）
%   runs_per_scene: 每个场景的回合数
%
% 输出：k_torque [N/(A·kg)]（全局最优）

% 收集数据（从所有场景）
I_sum_all = [];
accel_x_all = [];

% 遍历所有场景
for scene_idx = 1:length(scenes)
    scene = scenes{scene_idx};
    if verbose
        fprintf('  [场景 %d/%d] %s: 生成 %d 回合无注入数据...\n', ...
            scene_idx, length(scenes), scene, runs_per_scene);
    end
    
    % 每个场景生成 runs_per_scene 回合
    for run = 1:runs_per_scene
        % 生成无注入路径
        [ref_path, inj_signal, ~] = generate_reference_path(...
            scene, params, T_end, Ts, ...
        v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
        0, [0,0], [0,0], [1,1], ...  % 无打滑注入 (slip_prob, t_start, duration, gamma)
        0, [1,1], ...                % 无轻度打滑 (slip_in_turn_prob, gamma_range)
        0, [0,0], [0,0], [0,0]);     % 无堵转注入 (stall_prob, t_start, duration, load)
    
    % 运行仿真
    params_sim = params;
    params_sim.enable_noise = false;  % 关闭噪声以提高拟合精度
    
    set_param(model_name, 'StopTime', num2str(T_end));
    set_param(model_name, 'FixedStep', num2str(Ts));
    
    assignin('base', 'params', params_sim);
    assignin('base', 'ref_path', ref_path);
    assignin('base', 'inj_signal', inj_signal);
    
    warning('off', 'all');
    sim_out = sim(model_name, 'ReturnWorkspaceOutputs', 'on', ...
                 'SimulationMode', 'normal', 'CaptureErrors', 'on');
    warning('on', 'all');
    
    % 提取数据
    y_raw = sim_out.y_raw.signals.values;
    I_lf = y_raw(:, 12);
    I_rr = y_raw(:, 13);
    I_sum = abs(I_lf) + abs(I_rr);
    accel_x = y_raw(:, 9);
    
    % 过滤：仅保留有效动力学样本（V4.5: 放宽阈值以适应低电流场景）
    % 要求：I_sum > 0.5A（排除停车/滑行）且 |accel_x| > 0.05 m/s²（有加速度变化）
    valid_idx = (I_sum > 0.5) & (abs(accel_x) > 0.05);
    I_sum_all = [I_sum_all; I_sum(valid_idx)];
    accel_x_all = [accel_x_all; accel_x(valid_idx)];
    end  % 结束 runs_per_scene 循环
end  % 结束 scenes 循环

% 线性回归：accel_x = k_torque·I_sum/mass（所有场景数据统一拟合）
% 即：accel_x·mass = k_torque·I_sum
% 使用最小二乘法：k_torque = (I_sum' * I_sum)^-1 * (I_sum' * (accel_x·mass))
mass = params.mass;
y = accel_x_all * mass;  % [N]
X = I_sum_all;           % [A]

if length(X) > 0
    k_torque = (X' * X) \ (X' * y);  % [N/A] 或 [N/(A·kg)] 取决于单位
else
    % 兜底：如果样本数为0，使用经验值
    k_torque = 0.5;  % [N/A] 典型值（根据电机型号调整）
    if verbose
        warning('k_torque拟合失败（样本数为0），使用默认值: %.2f [N/A]', k_torque);
    end
end

if verbose
    fprintf('  拟合样本数: %d\n', length(I_sum_all));
    if isnan(k_torque) || isinf(k_torque)
        warning('  k_torque = NaN/Inf，使用默认值 0.5 [N/A]');
        k_torque = 0.5;
    end
    fprintf('  k_torque = %.6f [N/(A·kg)]\n', k_torque);
end

end


function best = search_optimal_thresholds(...
    I_high_grid, accel_stall_grid, stall_dwell_grid, ...
    scenes, num_runs, params, T_end, Ts, ...
    v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
    slip_prob, slip_t_start_range, slip_duration_range, slip_gamma_range, ...
    slip_in_turn_prob, slip_in_turn_gamma_range, ...
    stall_prob, stall_t_start_range, stall_duration_range, stall_load_range, ...
    k_torque, model_name, verbose)
% V4.2: 阈值网格搜索（小规模，早停）
%
% 策略：生成少量数据，尝试不同阈值组合，选择标注质量最优的组合
% 评价指标：注入窗口与启发式标注的一致性（F1-score）
%
% 输出：best.I_high_thresh, best.accel_stall_thresh, best.stall_dwell

if verbose
    fprintf('  生成小规模验证数据集...\n');
end

% 生成验证数据（每场景1回合）
val_data = cell(length(scenes), 1);
for s_idx = 1:length(scenes)
    scene = scenes{s_idx};
    [ref_path, inj_signal, inject_info] = generate_reference_path(...
        scene, params, T_end, Ts, ...
        v0_range, R_range, theta_slope_range, bumpy_amp_range, turn_trans_range, ...
        slip_prob, slip_t_start_range, slip_duration_range, slip_gamma_range, ...
        slip_in_turn_prob, slip_in_turn_gamma_range, ...
        stall_prob, stall_t_start_range, stall_duration_range, stall_load_range);
    
    params_sim = params;
    params_sim.enable_noise = false;
    
    set_param(model_name, 'StopTime', num2str(T_end));
    set_param(model_name, 'FixedStep', num2str(Ts));
    
    assignin('base', 'params', params_sim);
    assignin('base', 'ref_path', ref_path);
    assignin('base', 'inj_signal', inj_signal);
    
    warning('off', 'all');
    sim_out = sim(model_name, 'ReturnWorkspaceOutputs', 'on', ...
                 'SimulationMode', 'normal', 'CaptureErrors', 'on');
    warning('on', 'all');
    
    val_data{s_idx}.t = sim_out.tout;
    val_data{s_idx}.y_raw = sim_out.y_raw.signals.values;
    val_data{s_idx}.theta = sim_out.theta.signals.values;
    val_data{s_idx}.omega_ref = ref_path.omega_ref;
    val_data{s_idx}.inject_info = inject_info;
end

if verbose
    fprintf('  开始网格搜索...\n');
end

% 网格搜索
best_score = -inf;
best_combo = [];

for i = 1:length(I_high_grid)
    for j = 1:length(accel_stall_grid)
        for k = 1:length(stall_dwell_grid)
            thresholds = struct();
            thresholds.I_high_thresh = I_high_grid(i);
            thresholds.accel_stall_thresh = accel_stall_grid(j);
            thresholds.stall_dwell = stall_dwell_grid(k);
            
            % 对所有验证数据标注
            score_sum = 0;
            for s_idx = 1:length(val_data)
                [label_main, ~] = generate_labels(...
                    val_data{s_idx}.t, val_data{s_idx}.y_raw, val_data{s_idx}.theta, ...
                    val_data{s_idx}.omega_ref, val_data{s_idx}.inject_info, Ts, ...
                    k_torque, params.mass, thresholds);
                
                % 计算与注入窗口的一致性（简化：stall/slip 召回率）
                inject_info = val_data{s_idx}.inject_info;
                t = val_data{s_idx}.t;
                
                % Stall 召回率
                if inject_info.stall_injected
                    in_window = (t >= inject_info.stall_window(1)) & (t <= inject_info.stall_window(2));
                    stall_recall = sum((label_main == 3) & in_window) / max(sum(in_window), 1);
                else
                    stall_recall = 1.0;  % 无注入则不惩罚
                end
                
                % Slip 召回率
                if inject_info.slip_injected
                    in_window = (t >= inject_info.slip_window(1)) & (t <= inject_info.slip_window(2));
                    slip_recall = sum((label_main == 2) & in_window) / max(sum(in_window), 1);
                else
                    slip_recall = 1.0;
                end
                
                score_sum = score_sum + stall_recall + slip_recall;
            end
            
            avg_score = score_sum / length(val_data);
            
            if avg_score > best_score
                best_score = avg_score;
                best_combo = [i, j, k];
            end
        end
    end
end

% 返回最优组合
best = struct();
best.I_high_thresh = I_high_grid(best_combo(1));
best.accel_stall_thresh = accel_stall_grid(best_combo(2));
best.stall_dwell = stall_dwell_grid(best_combo(3));
best.score = best_score;

if verbose
    fprintf('  最优得分: %.4f\n', best_score);
end

end
