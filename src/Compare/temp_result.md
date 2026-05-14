>> init_project;
root = project_root;
cfg = struct;
cfg.controllers = {'Mamba2','GRU','IMU'};
cfg.path_files = {fullfile(root,'data','paths','path_industrial.mat'), fullfile(root,'data','paths','path_s_curve.mat'), fullfile(root,'data','paths','path_slope.mat')};
cfg.disturbance_levels = [1 2];
cfg.seeds = [1 2];
cfg.save_timeseries = false;
cfg.mamba_ai_backend = 'tcp_service';
results = run_compare_mamba2_gru_imu_batch(cfg);
run_dir = results_dir(fullfile('compare','mamba2_gru_imu',results.run_id));
rep = check_compare_disturbance_effectiveness(struct('input_mat',fullfile(run_dir,'raw','case_rows.mat')));
[init_project] Root: E:\Matlab\Simulink\S-Function_16
[init_project] Root: E:\Matlab\Simulink\S-Function_16

[compare] run_id = compare_20260420_160426
[compare] output = E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260420_160426
[compare] total cases = 36

[   1/  36] Mamba2 | path_industrial | d=1 | seed=1

╔════════════════════════════════════════════════════════════╗
║     LPVMPC_AGV 模型初始化 (PreLoadFcn, V3.4, 2026-01-22)   ║
╚════════════════════════════════════════════════════════════╝

[init_project] Root: E:\Matlab\Simulink\S-Function_16
[步骤 0/5] 加载基础参数...
  ✓ parameters() 加载成功 (Ts=0.010s, m=200.0kg, L=2.00m)

[步骤 1/5] 加载 LPV 数据库...
  ✓ 文件加载成功: E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat
  → 使用 db 结构体格式
  ✓ 网格: 11×15×21 (总 3465 点), nx=4, nu=2, nd=1, Ts=0.010s

[步骤 2/5] 创建 MPCPlantBus...
  ✓ MPCPlantBus 创建成功 (nu_md=3 = 2 MV + 1 MD)

[步骤 3/5] 加载优化权重 / ctrl...
  ✓ 权重加载成功 (phase2_best)
  ✓ 从 ctrl.mat 加载控制器 (Np=150)
  → 已将 21 个优化参数注入 ctrl.maps

[步骤 4/5] 加载 GRU 模型...
  ✓ GRU_model 加载成功 (E:\Matlab\Simulink\S-Function_16\data\models\GRU_model.mat)
    - 序列长度: 128

[步骤 5/5] 初始化总结
  ════════════════════════════════════════════════
  ✓ 基础参数:     已加载 (Ts=0.010s)
  ✓ LPV 数据库:   E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat (11×15×21)
  ✓ MPCPlantBus:  已创建
  ✓ GRU 模型:     就绪
  ✓ 优化权重:     已加载 (phase2_best)
  ✓ MPC 控制器:   E:\Matlab\Simulink\S-Function_16\data\models\ctrl.mat (Np=150, Nc=50)
  ════════════════════════════════════════════════

✓ 初始化成功！使用优化权重与 GRU 调度

[PreLoadFcn] 完成

   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   2/  36] Mamba2 | path_industrial | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   3/  36] Mamba2 | path_industrial | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   4/  36] Mamba2 | path_industrial | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   5/  36] Mamba2 | path_s_curve | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   6/  36] Mamba2 | path_s_curve | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   7/  36] Mamba2 | path_s_curve | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   8/  36] Mamba2 | path_s_curve | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[   9/  36] Mamba2 | path_slope | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  10/  36] Mamba2 | path_slope | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  11/  36] Mamba2 | path_slope | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  12/  36] Mamba2 | path_slope | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  13/  36] GRU    | path_industrial | d=1 | seed=1

============================================================
LPVMPC_AGV preload (GRU standalone)
============================================================

[init_project] Root: E:\Matlab\Simulink\S-Function_16
[Step 0/5] Load basic parameters...
  OK parameters() (Ts=0.010s, m=200.0kg, L=2.00m)

[Step 1/5] Load LPV database...
  OK file loaded: E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat
  use db struct format
  OK grid 11 x 15 x 21, nx=4, nu=2, nd=1, Ts=0.010s

[Step 2/5] Create MPCPlantBus...
  OK MPCPlantBus created (nu_md=3 = 2 MV + 1 MD)

[Step 3/5] Load BO maps / ctrl...
  OK BO maps loaded (phase2_best)
  OK ctrl loaded (Np=150)
  copied 21 BO map fields to ctrl.maps

[Step 4/5] Load GRU model...
  OK GRU model loaded: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_mamba_control_strict.mat
  OK GRU meta loaded: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_mamba_control_strict.mat

[Step 5/5] Summary
  ================================================
  basic params:   loaded (Ts=0.010s)
  LPV database:   E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat (11 x 15 x 21)
  MPCPlantBus:    created
  GRU model:      ready
  BO maps:        loaded (phase2_best)
  MPC controller: E:\Matlab\Simulink\S-Function_16\data\models\ctrl.mat (Np=150, Nc=50)
  ================================================

Initialization completed (optimized BO maps + GRU).

[preloadfcn_gru] done

   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  14/  36] GRU    | path_industrial | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  15/  36] GRU    | path_industrial | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  16/  36] GRU    | path_industrial | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  17/  36] GRU    | path_s_curve | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  18/  36] GRU    | path_s_curve | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  19/  36] GRU    | path_s_curve | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  20/  36] GRU    | path_s_curve | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  21/  36] GRU    | path_slope | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  22/  36] GRU    | path_slope | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  23/  36] GRU    | path_slope | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  24/  36] GRU    | path_slope | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  25/  36] IMU    | path_industrial | d=1 | seed=1

╔════════════════════════════════════════════════════════════╗
║     LPVMPC_AGV 模型初始化 (PreLoadFcn, V3.4, 2026-01-22)   ║
╚════════════════════════════════════════════════════════════╝

[init_project] Root: E:\Matlab\Simulink\S-Function_16
[步骤 0/5] 加载基础参数...
  ✓ parameters() 加载成功 (Ts=0.010s, m=200.0kg, L=2.00m)

[步骤 1/5] 加载 LPV 数据库...
  ✓ 文件加载成功: E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat
  → 使用 db 结构体格式
  ✓ 网格: 11×15×21 (总 3465 点), nx=4, nu=2, nd=1, Ts=0.010s

[步骤 2/5] 创建 MPCPlantBus...
  ✓ MPCPlantBus 创建成功 (nu_md=3 = 2 MV + 1 MD)

[步骤 3/5] 加载优化权重 / ctrl...
  ✓ 权重加载成功 (phase2_best)
  ✓ 从 ctrl.mat 加载控制器 (Np=150)
  → 已将 21 个优化参数注入 ctrl.maps

[步骤 4/5] 加载 GRU 模型...
  ✓ GRU_model 加载成功 (E:\Matlab\Simulink\S-Function_16\data\models\GRU_model.mat)
    - 序列长度: 128

[步骤 5/5] 初始化总结
  ════════════════════════════════════════════════
  ✓ 基础参数:     已加载 (Ts=0.010s)
  ✓ LPV 数据库:   E:\Matlab\Simulink\S-Function_16\data\models\lin_agv_db.mat (11×15×21)
  ✓ MPCPlantBus:  已创建
  ✓ GRU 模型:     就绪
  ✓ 优化权重:     已加载 (phase2_best)
  ✓ MPC 控制器:   E:\Matlab\Simulink\S-Function_16\data\models\ctrl.mat (Np=150, Nc=50)
  ════════════════════════════════════════════════

✓ 初始化成功！使用优化权重与 GRU 调度

[PreLoadFcn] 完成

   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  26/  36] IMU    | path_industrial | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  27/  36] IMU    | path_industrial | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  28/  36] IMU    | path_industrial | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  29/  36] IMU    | path_s_curve | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  30/  36] IMU    | path_s_curve | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  31/  36] IMU    | path_s_curve | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  32/  36] IMU    | path_s_curve | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  33/  36] IMU    | path_slope | d=1 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  34/  36] IMU    | path_slope | d=1 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  35/  36] IMU    | path_slope | d=2 | seed=1
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.
[  36/  36] IMU    | path_slope | d=2 | seed=2
   Assuming no disturbance added to measured output #1.
-->Assuming output disturbance added to measured output #2 is integrated white noise.
-->Assuming output disturbance added to measured output #3 is integrated white noise.
-->Assuming output disturbance added to measured output #4 is integrated white noise.
-->"Model.Noise" is empty. Assuming white noise on each measured output.

[compare] done: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260420_160426\raw\case_rows.mat
[init_project] Root: E:\Matlab\Simulink\S-Function_16

[dist-check] input: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260420_160426\raw\case_rows.mat
[dist-check] checked rows: 75, flagged invariant rows: 0
[dist-check] report: E:\Matlab\Simulink\S-Function_16\results\compare\mamba2_gru_imu\compare_20260420_160426\analysis\disturbance_effectiveness_report.md
>>  