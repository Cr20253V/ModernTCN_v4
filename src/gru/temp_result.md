PS C:\Users\15754\Desktop> cd E:\Matlab\Simulink\S-Function_16
PS E:\Matlab\Simulink\S-Function_16> matlab -batch "init_project; summary = run_GRU_train_theta10_v2_multi_seed();"
[init_project] Root: E:\Matlab\Simulink\S-Function_16
[init_project] Root: E:\Matlab\Simulink\S-Function_16
[GRU V4 dataset check] pass=1
  dataset: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  windows train/val/test: 18302 / 2607 / 3733
  seq_len=128 feat_dim=19
  train main counts [flat stall slope]=[3739 339 14224]
  train turn counts [right straight left]=[4013 9832 4457]
  theta train mask count=17963

[GRU theta10 V2] case=inputstats_hidden96_l2 seed=11 (1/5)
[init_project] Root: E:\Matlab\Simulink\S-Function_16

========== GRU 多任务训练 ==========
模式: physics_guided
输入: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
模型: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed11.mat
============================================

[数据]
  训练/验证/测试窗口数: 18302 / 2607 / 3733
  输入: feat_dim=19, seq_len=128
  执行环境: gpu
[模型]
  hidden=96, layers=2, dropout=0.20
  head pooling: last_mean_inputstats
  序列上下文: 128 steps (1.28 s)
轮次 001/140 | lr=1.00e-03 | 训练 0.8618 | 验证 0.7907 | 主类准确率 0.793 | 转弯准确率 0.611 | 坡度MAE 0.578 deg
轮次 005/140 | lr=9.98e-04 | 训练 0.4405 | 验证 0.4645 | 主类准确率 0.873 | 转弯准确率 0.635 | 坡度MAE 0.483 deg
轮次 010/140 | lr=9.90e-04 | 训练 0.2866 | 验证 0.3699 | 主类准确率 0.920 | 转弯准确率 0.694 | 坡度MAE 0.544 deg
轮次 015/140 | lr=9.76e-04 | 训练 0.2107 | 验证 0.2913 | 主类准确率 0.938 | 转弯准确率 0.675 | 坡度MAE 0.512 deg
轮次 020/140 | lr=9.55e-04 | 训练 0.1647 | 验证 0.2543 | 主类准确率 0.954 | 转弯准确率 0.695 | 坡度MAE 0.366 deg
轮次 025/140 | lr=9.29e-04 | 训练 0.1325 | 验证 0.2224 | 主类准确率 0.969 | 转弯准确率 0.697 | 坡度MAE 0.895 deg
轮次 030/140 | lr=8.98e-04 | 训练 0.1159 | 验证 0.1994 | 主类准确率 0.974 | 转弯准确率 0.700 | 坡度MAE 0.450 deg
轮次 035/140 | lr=8.61e-04 | 训练 0.0991 | 验证 0.2273 | 主类准确率 0.977 | 转弯准确率 0.679 | 坡度MAE 0.348 deg
轮次 040/140 | lr=8.20e-04 | 训练 0.0863 | 验证 0.1789 | 主类准确率 0.982 | 转弯准确率 0.698 | 坡度MAE 0.390 deg
轮次 045/140 | lr=7.75e-04 | 训练 0.0836 | 验证 0.2186 | 主类准确率 0.985 | 转弯准确率 0.712 | 坡度MAE 0.349 deg
轮次 050/140 | lr=7.27e-04 | 训练 0.0723 | 验证 0.1898 | 主类准确率 0.987 | 转弯准确率 0.709 | 坡度MAE 0.275 deg
轮次 055/140 | lr=6.76e-04 | 训练 0.0701 | 验证 0.2117 | 主类准确率 0.986 | 转弯准确率 0.724 | 坡度MAE 0.502 deg
轮次 060/140 | lr=6.22e-04 | 训练 0.0634 | 验证 0.1982 | 主类准确率 0.990 | 转弯准确率 0.712 | 坡度MAE 0.365 deg
轮次 065/140 | lr=5.67e-04 | 训练 0.0592 | 验证 0.2141 | 主类准确率 0.981 | 转弯准确率 0.730 | 坡度MAE 0.292 deg
轮次 070/140 | lr=5.11e-04 | 训练 0.0562 | 验证 0.1766 | 主类准确率 0.990 | 转弯准确率 0.702 | 坡度MAE 0.268 deg
轮次 075/140 | lr=4.55e-04 | 训练 0.0538 | 验证 0.2009 | 主类准确率 0.991 | 转弯准确率 0.710 | 坡度MAE 0.239 deg
轮次 080/140 | lr=4.00e-04 | 训练 0.0525 | 验证 0.1759 | 主类准确率 0.990 | 转弯准确率 0.710 | 坡度MAE 0.295 deg
轮次 085/140 | lr=3.45e-04 | 训练 0.0494 | 验证 0.1931 | 主类准确率 0.989 | 转弯准确率 0.708 | 坡度MAE 0.252 deg
轮次 090/140 | lr=2.93e-04 | 训练 0.0482 | 验证 0.1843 | 主类准确率 0.990 | 转弯准确率 0.726 | 坡度MAE 0.352 deg
轮次 095/140 | lr=2.44e-04 | 训练 0.0481 | 验证 0.1834 | 主类准确率 0.987 | 转弯准确率 0.707 | 坡度MAE 0.305 deg
[GRU] 第 99 轮早停，最佳轮次: 74

[GRU] 训练完成。
  最佳轮次: 74
  测试主类/转弯准确率: 0.974 / 0.769
  测试坡度 MAE: 0.338 deg
  模型已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed11.mat
  元信息已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed11.mat

[GRU theta10 V2] case=inputstats_hidden96_l2 seed=21 (2/5)
[init_project] Root: E:\Matlab\Simulink\S-Function_16

========== GRU 多任务训练 ==========
模式: physics_guided
输入: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
模型: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed21.mat
============================================

[数据]
  训练/验证/测试窗口数: 18302 / 2607 / 3733
  输入: feat_dim=19, seq_len=128
  执行环境: gpu
[模型]
  hidden=96, layers=2, dropout=0.20
  head pooling: last_mean_inputstats
  序列上下文: 128 steps (1.28 s)
轮次 001/140 | lr=1.00e-03 | 训练 0.8679 | 验证 0.7670 | 主类准确率 0.786 | 转弯准确率 0.631 | 坡度MAE 0.714 deg
轮次 005/140 | lr=9.98e-04 | 训练 0.4373 | 验证 0.4512 | 主类准确率 0.865 | 转弯准确率 0.684 | 坡度MAE 0.567 deg
轮次 010/140 | lr=9.90e-04 | 训练 0.2689 | 验证 0.3178 | 主类准确率 0.929 | 转弯准确率 0.673 | 坡度MAE 0.394 deg
轮次 015/140 | lr=9.76e-04 | 训练 0.1954 | 验证 0.2731 | 主类准确率 0.948 | 转弯准确率 0.668 | 坡度MAE 0.432 deg
轮次 020/140 | lr=9.55e-04 | 训练 0.1562 | 验证 0.2387 | 主类准确率 0.962 | 转弯准确率 0.677 | 坡度MAE 0.446 deg
轮次 025/140 | lr=9.29e-04 | 训练 0.1280 | 验证 0.2118 | 主类准确率 0.962 | 转弯准确率 0.685 | 坡度MAE 0.468 deg
轮次 030/140 | lr=8.98e-04 | 训练 0.1090 | 验证 0.2153 | 主类准确率 0.963 | 转弯准确率 0.680 | 坡度MAE 0.429 deg
轮次 035/140 | lr=8.61e-04 | 训练 0.0987 | 验证 0.2299 | 主类准确率 0.983 | 转弯准确率 0.669 | 坡度MAE 0.514 deg
轮次 040/140 | lr=8.20e-04 | 训练 0.0858 | 验证 0.1795 | 主类准确率 0.980 | 转弯准确率 0.689 | 坡度MAE 0.441 deg
轮次 045/140 | lr=7.75e-04 | 训练 0.0789 | 验证 0.1662 | 主类准确率 0.985 | 转弯准确率 0.698 | 坡度MAE 0.500 deg
轮次 050/140 | lr=7.27e-04 | 训练 0.0710 | 验证 0.2148 | 主类准确率 0.975 | 转弯准确率 0.698 | 坡度MAE 0.509 deg
轮次 055/140 | lr=6.76e-04 | 训练 0.0668 | 验证 0.2296 | 主类准确率 0.984 | 转弯准确率 0.689 | 坡度MAE 0.296 deg
轮次 060/140 | lr=6.22e-04 | 训练 0.0614 | 验证 0.2177 | 主类准确率 0.982 | 转弯准确率 0.694 | 坡度MAE 0.311 deg
轮次 065/140 | lr=5.67e-04 | 训练 0.0590 | 验证 0.1893 | 主类准确率 0.987 | 转弯准确率 0.681 | 坡度MAE 0.465 deg
轮次 070/140 | lr=5.11e-04 | 训练 0.0569 | 验证 0.2044 | 主类准确率 0.984 | 转弯准确率 0.701 | 坡度MAE 0.304 deg
[GRU] 第 70 轮早停，最佳轮次: 45

[GRU] 训练完成。
  最佳轮次: 45
  测试主类/转弯准确率: 0.972 / 0.757
  测试坡度 MAE: 0.535 deg
  模型已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed21.mat
  元信息已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed21.mat

[GRU theta10 V2] case=inputstats_hidden96_l2 seed=42 (3/5)
[init_project] Root: E:\Matlab\Simulink\S-Function_16

========== GRU 多任务训练 ==========
模式: physics_guided
输入: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
模型: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed42.mat
============================================

[数据]
  训练/验证/测试窗口数: 18302 / 2607 / 3733
  输入: feat_dim=19, seq_len=128
  执行环境: gpu
[模型]
  hidden=96, layers=2, dropout=0.20
  head pooling: last_mean_inputstats
  序列上下文: 128 steps (1.28 s)
轮次 001/140 | lr=1.00e-03 | 训练 0.8595 | 验证 0.7735 | 主类准确率 0.787 | 转弯准确率 0.632 | 坡度MAE 0.794 deg
轮次 005/140 | lr=9.98e-04 | 训练 0.4227 | 验证 0.4369 | 主类准确率 0.879 | 转弯准确率 0.689 | 坡度MAE 0.490 deg
轮次 010/140 | lr=9.90e-04 | 训练 0.2519 | 验证 0.3052 | 主类准确率 0.932 | 转弯准确率 0.696 | 坡度MAE 0.596 deg
轮次 015/140 | lr=9.76e-04 | 训练 0.1768 | 验证 0.2224 | 主类准确率 0.961 | 转弯准确率 0.656 | 坡度MAE 0.426 deg
轮次 020/140 | lr=9.55e-04 | 训练 0.1409 | 验证 0.1943 | 主类准确率 0.970 | 转弯准确率 0.687 | 坡度MAE 0.533 deg
轮次 025/140 | lr=9.29e-04 | 训练 0.1211 | 验证 0.2237 | 主类准确率 0.967 | 转弯准确率 0.689 | 坡度MAE 0.589 deg
轮次 030/140 | lr=8.98e-04 | 训练 0.1051 | 验证 0.1725 | 主类准确率 0.974 | 转弯准确率 0.680 | 坡度MAE 0.492 deg
轮次 035/140 | lr=8.61e-04 | 训练 0.0943 | 验证 0.1930 | 主类准确率 0.983 | 转弯准确率 0.699 | 坡度MAE 0.361 deg
轮次 040/140 | lr=8.20e-04 | 训练 0.0839 | 验证 0.1872 | 主类准确率 0.985 | 转弯准确率 0.685 | 坡度MAE 0.314 deg
轮次 045/140 | lr=7.75e-04 | 训练 0.0769 | 验证 0.1866 | 主类准确率 0.982 | 转弯准确率 0.688 | 坡度MAE 0.397 deg
轮次 050/140 | lr=7.27e-04 | 训练 0.0720 | 验证 0.1982 | 主类准确率 0.990 | 转弯准确率 0.689 | 坡度MAE 0.415 deg
轮次 055/140 | lr=6.76e-04 | 训练 0.0659 | 验证 0.1879 | 主类准确率 0.989 | 转弯准确率 0.695 | 坡度MAE 0.523 deg
轮次 060/140 | lr=6.22e-04 | 训练 0.0631 | 验证 0.1700 | 主类准确率 0.991 | 转弯准确率 0.687 | 坡度MAE 0.303 deg
轮次 065/140 | lr=5.67e-04 | 训练 0.0609 | 验证 0.1810 | 主类准确率 0.992 | 转弯准确率 0.680 | 坡度MAE 0.293 deg
轮次 070/140 | lr=5.11e-04 | 训练 0.0563 | 验证 0.1424 | 主类准确率 0.990 | 转弯准确率 0.690 | 坡度MAE 0.263 deg
轮次 075/140 | lr=4.55e-04 | 训练 0.0539 | 验证 0.1819 | 主类准确率 0.992 | 转弯准确率 0.689 | 坡度MAE 0.372 deg
轮次 080/140 | lr=4.00e-04 | 训练 0.0539 | 验证 0.1786 | 主类准确率 0.992 | 转弯准确率 0.694 | 坡度MAE 0.535 deg
轮次 085/140 | lr=3.45e-04 | 训练 0.0511 | 验证 0.1637 | 主类准确率 0.991 | 转弯准确率 0.709 | 坡度MAE 0.308 deg
轮次 090/140 | lr=2.93e-04 | 训练 0.0499 | 验证 0.1793 | 主类准确率 0.993 | 转弯准确率 0.707 | 坡度MAE 0.344 deg
轮次 095/140 | lr=2.44e-04 | 训练 0.0477 | 验证 0.1785 | 主类准确率 0.993 | 转弯准确率 0.696 | 坡度MAE 0.268 deg
[GRU] 第 95 轮早停，最佳轮次: 70

[GRU] 训练完成。
  最佳轮次: 70
  测试主类/转弯准确率: 0.975 / 0.765
  测试坡度 MAE: 0.322 deg
  模型已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed42.mat
  元信息已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed42.mat

[GRU theta10 V2] case=inputstats_hidden96_l2 seed=73 (4/5)
[init_project] Root: E:\Matlab\Simulink\S-Function_16

========== GRU 多任务训练 ==========
模式: physics_guided
输入: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
模型: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed73.mat
============================================

[数据]
  训练/验证/测试窗口数: 18302 / 2607 / 3733
  输入: feat_dim=19, seq_len=128
  执行环境: gpu
[模型]
  hidden=96, layers=2, dropout=0.20
  head pooling: last_mean_inputstats
  序列上下文: 128 steps (1.28 s)
轮次 001/140 | lr=1.00e-03 | 训练 0.8612 | 验证 0.7681 | 主类准确率 0.783 | 转弯准确率 0.632 | 坡度MAE 0.611 deg
轮次 005/140 | lr=9.98e-04 | 训练 0.4257 | 验证 0.4800 | 主类准确率 0.876 | 转弯准确率 0.677 | 坡度MAE 0.433 deg
轮次 010/140 | lr=9.90e-04 | 训练 0.2662 | 验证 0.3526 | 主类准确率 0.928 | 转弯准确率 0.694 | 坡度MAE 0.417 deg
轮次 015/140 | lr=9.76e-04 | 训练 0.2006 | 验证 0.3055 | 主类准确率 0.939 | 转弯准确率 0.685 | 坡度MAE 0.545 deg
轮次 020/140 | lr=9.55e-04 | 训练 0.1652 | 验证 0.2626 | 主类准确率 0.950 | 转弯准确率 0.672 | 坡度MAE 0.442 deg
轮次 025/140 | lr=9.29e-04 | 训练 0.1418 | 验证 0.2274 | 主类准确率 0.961 | 转弯准确率 0.677 | 坡度MAE 0.380 deg
轮次 030/140 | lr=8.98e-04 | 训练 0.1197 | 验证 0.2090 | 主类准确率 0.964 | 转弯准确率 0.695 | 坡度MAE 0.548 deg
轮次 035/140 | lr=8.61e-04 | 训练 0.1044 | 验证 0.1772 | 主类准确率 0.969 | 转弯准确率 0.699 | 坡度MAE 0.453 deg
轮次 040/140 | lr=8.20e-04 | 训练 0.0944 | 验证 0.2330 | 主类准确率 0.973 | 转弯准确率 0.727 | 坡度MAE 0.681 deg
轮次 045/140 | lr=7.75e-04 | 训练 0.0848 | 验证 0.1755 | 主类准确率 0.979 | 转弯准确率 0.704 | 坡度MAE 0.530 deg
轮次 050/140 | lr=7.27e-04 | 训练 0.0812 | 验证 0.1873 | 主类准确率 0.980 | 转弯准确率 0.715 | 坡度MAE 0.299 deg
轮次 055/140 | lr=6.76e-04 | 训练 0.0736 | 验证 0.1935 | 主类准确率 0.981 | 转弯准确率 0.707 | 坡度MAE 0.435 deg
轮次 060/140 | lr=6.22e-04 | 训练 0.0676 | 验证 0.2004 | 主类准确率 0.984 | 转弯准确率 0.702 | 坡度MAE 0.309 deg
轮次 065/140 | lr=5.67e-04 | 训练 0.0640 | 验证 0.1742 | 主类准确率 0.985 | 转弯准确率 0.717 | 坡度MAE 0.226 deg
轮次 070/140 | lr=5.11e-04 | 训练 0.0609 | 验证 0.2017 | 主类准确率 0.984 | 转弯准确率 0.689 | 坡度MAE 0.348 deg
轮次 075/140 | lr=4.55e-04 | 训练 0.0585 | 验证 0.1968 | 主类准确率 0.990 | 转弯准确率 0.703 | 坡度MAE 0.390 deg
轮次 080/140 | lr=4.00e-04 | 训练 0.0540 | 验证 0.1776 | 主类准确率 0.988 | 转弯准确率 0.704 | 坡度MAE 0.432 deg
轮次 085/140 | lr=3.45e-04 | 训练 0.0515 | 验证 0.1840 | 主类准确率 0.988 | 转弯准确率 0.715 | 坡度MAE 0.382 deg
轮次 090/140 | lr=2.93e-04 | 训练 0.0502 | 验证 0.1696 | 主类准确率 0.990 | 转弯准确率 0.722 | 坡度MAE 0.307 deg
轮次 095/140 | lr=2.44e-04 | 训练 0.0484 | 验证 0.1887 | 主类准确率 0.988 | 转弯准确率 0.697 | 坡度MAE 0.288 deg
轮次 100/140 | lr=1.97e-04 | 训练 0.0497 | 验证 0.1955 | 主类准确率 0.988 | 转弯准确率 0.709 | 坡度MAE 0.476 deg
轮次 105/140 | lr=1.54e-04 | 训练 0.0465 | 验证 0.1903 | 主类准确率 0.991 | 转弯准确率 0.711 | 坡度MAE 0.250 deg
[GRU] 第 107 轮早停，最佳轮次: 82

[GRU] 训练完成。
  最佳轮次: 82
  测试主类/转弯准确率: 0.980 / 0.776
  测试坡度 MAE: 0.277 deg
  模型已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed73.mat
  元信息已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed73.mat

[GRU theta10 V2] case=inputstats_hidden96_l2 seed=101 (5/5)
[init_project] Root: E:\Matlab\Simulink\S-Function_16

========== GRU 多任务训练 ==========
模式: physics_guided
输入: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
模型: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat
============================================

[数据]
  训练/验证/测试窗口数: 18302 / 2607 / 3733
  输入: feat_dim=19, seq_len=128
  执行环境: gpu
[模型]
  hidden=96, layers=2, dropout=0.20
  head pooling: last_mean_inputstats
  序列上下文: 128 steps (1.28 s)
轮次 001/140 | lr=1.00e-03 | 训练 0.8650 | 验证 0.7937 | 主类准确率 0.786 | 转弯准确率 0.601 | 坡度MAE 0.846 deg
轮次 005/140 | lr=9.98e-04 | 训练 0.4404 | 验证 0.4950 | 主类准确率 0.836 | 转弯准确率 0.672 | 坡度MAE 0.389 deg
轮次 010/140 | lr=9.90e-04 | 训练 0.2643 | 验证 0.3560 | 主类准确率 0.913 | 转弯准确率 0.661 | 坡度MAE 0.375 deg
轮次 015/140 | lr=9.76e-04 | 训练 0.1892 | 验证 0.2992 | 主类准确率 0.943 | 转弯准确率 0.686 | 坡度MAE 0.352 deg
轮次 020/140 | lr=9.55e-04 | 训练 0.1554 | 验证 0.2619 | 主类准确率 0.957 | 转弯准确率 0.693 | 坡度MAE 0.836 deg
轮次 025/140 | lr=9.29e-04 | 训练 0.1256 | 验证 0.2366 | 主类准确率 0.969 | 转弯准确率 0.710 | 坡度MAE 0.369 deg
轮次 030/140 | lr=8.98e-04 | 训练 0.1143 | 验证 0.2634 | 主类准确率 0.964 | 转弯准确率 0.695 | 坡度MAE 0.480 deg
轮次 035/140 | lr=8.61e-04 | 训练 0.1013 | 验证 0.1913 | 主类准确率 0.976 | 转弯准确率 0.693 | 坡度MAE 0.488 deg
轮次 040/140 | lr=8.20e-04 | 训练 0.0857 | 验证 0.1844 | 主类准确率 0.980 | 转弯准确率 0.703 | 坡度MAE 0.482 deg
轮次 045/140 | lr=7.75e-04 | 训练 0.0812 | 验证 0.2009 | 主类准确率 0.980 | 转弯准确率 0.658 | 坡度MAE 0.299 deg
轮次 050/140 | lr=7.27e-04 | 训练 0.0749 | 验证 0.1858 | 主类准确率 0.983 | 转弯准确率 0.693 | 坡度MAE 0.452 deg
轮次 055/140 | lr=6.76e-04 | 训练 0.0666 | 验证 0.1642 | 主类准确率 0.987 | 转弯准确率 0.715 | 坡度MAE 0.361 deg
轮次 060/140 | lr=6.22e-04 | 训练 0.0626 | 验证 0.1922 | 主类准确率 0.987 | 转弯准确率 0.711 | 坡度MAE 0.311 deg
轮次 065/140 | lr=5.67e-04 | 训练 0.0584 | 验证 0.1993 | 主类准确率 0.980 | 转弯准确率 0.701 | 坡度MAE 0.260 deg
轮次 070/140 | lr=5.11e-04 | 训练 0.0570 | 验证 0.1718 | 主类准确率 0.988 | 转弯准确率 0.700 | 坡度MAE 0.361 deg
轮次 075/140 | lr=4.55e-04 | 训练 0.0549 | 验证 0.1698 | 主类准确率 0.989 | 转弯准确率 0.690 | 坡度MAE 0.248 deg
轮次 080/140 | lr=4.00e-04 | 训练 0.0523 | 验证 0.1642 | 主类准确率 0.988 | 转弯准确率 0.707 | 坡度MAE 0.286 deg
轮次 085/140 | lr=3.45e-04 | 训练 0.0508 | 验证 0.1819 | 主类准确率 0.991 | 转弯准确率 0.701 | 坡度MAE 0.330 deg
轮次 090/140 | lr=2.93e-04 | 训练 0.0493 | 验证 0.1869 | 主类准确率 0.991 | 转弯准确率 0.700 | 坡度MAE 0.270 deg
轮次 095/140 | lr=2.44e-04 | 训练 0.0491 | 验证 0.1937 | 主类准确率 0.990 | 转弯准确率 0.705 | 坡度MAE 0.336 deg
[GRU] 第 98 轮早停，最佳轮次: 73

[GRU] 训练完成。
  最佳轮次: 73
  测试主类/转弯准确率: 0.977 / 0.768
  测试坡度 MAE: 0.260 deg
  模型已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_model_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat
  元信息已保存: E:\Matlab\Simulink\S-Function_16\data\models\GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat

[GRU theta10 V2] done
  per-seed: E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_theta10_uniform_h0_v2\GRU_theta10_v2_multi_seed_summary.csv
  group   : E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_theta10_uniform_h0_v2\GRU_theta10_v2_group_summary.csv
  report  : E:\Matlab\Simulink\S-Function_16\results\gru\train_logs_theta10_uniform_h0_v2\GRU_theta10_v2_multi_seed_report.md
           case_name            n    acc_main_mean    acc_main_std    acc_turn_mean    acc_turn_std    acc_turn_pure_mean    acc_turn_pure_std    acc_turn_transition_mean    acc_turn_transition_std    turn_right_recall_mean    turn_right_recall_std    turn_left_recall_mean    turn_left_recall_std    theta_mae_deg_mean    theta_mae_deg_std    theta_abs_le_10_p95_abs_err_deg_mean    theta_abs_le_10_p95_abs_err_deg_std    theta_neg_10_8_p95_abs_err_deg_mean    theta_neg_10_8_p95_abs_err_deg_std    theta_pos_8_10_p95_abs_err_deg_mean    theta_pos_8_10_p95_abs_err_deg_std    theta_neg_2_0p5_p95_abs_err_deg_mean    theta_neg_2_0p5_p95_abs_err_deg_std    theta_pos_0p5_2_p95_abs_err_deg_mean    theta_pos_0p5_2_p95_abs_err_deg_std    flat_recall_mean    flat_recall_std    stall_recall_mean    stall_recall_std    slope_recall_mean    slope_recall_std    uphill_recall_mean    uphill_recall_std    downhill_recall_mean    downhill_recall_std    flat_as_slope_mean    flat_as_slope_std
    ________________________    _    _____________    ____________    _____________    ____________    __________________    _________________    ________________________    _______________________    ______________________    _____________________    _____________________    ____________________    __________________    _________________    ____________________________________    ___________________________________    ___________________________________    __________________________________    ___________________________________    __________________________________    ____________________________________    ___________________________________    ____________________________________    ___________________________________    ________________    _______________    _________________    ________________    _________________    ________________    __________________    _________________    ____________________    ___________________    __________________    _________________

    "inputstats_hidden96_l2"    5       0.97552        0.0028889         0.76678        0.0069303           0.80775              0.0087789                0.52187                    0.0097483                  0.75523                  0.022106                  0.77596                 0.029427               0.34646               0.10987                        1.0314                                 0.23055                                0.90924                               0.47325                                0.89168                               0.30487                                0.83085                                 0.17865                                 1.4137                                 0.26349                       0.9609            0.0038058            0.67179             0.015526             0.99182            0.0036901             0.80662              0.0023172              0.77799                0.0052125              0.036724             0.002541