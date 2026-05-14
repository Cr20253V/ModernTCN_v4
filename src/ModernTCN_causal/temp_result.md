PS E:\Matlab\Simulink\S-Function_16> python src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py `
>>   --dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat `
>>   --run-tag-prefix modern_tcn_causal_theta10_uniform_h0_v2 `
>>   --seeds 11 21 42 73 101 `
>>   --temporal-padding causal `
>>   --dry-run
[ModernTCN V2 multi-seed]
  dataset: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  seeds: [11, 21, 42, 73, 101]
  temporal_padding: causal
  theta_gate_mode: none
  theta_flat_loss_mode: near_zero, tol=0.3 deg

[ModernTCN V2 multi-seed] seed 11 (1/5)
[ModernTCN dry-run] 数据和模型前向检查通过
  X: (4, 128, 19)
  logits_main/logits_turn/theta: [(4, 3), (4, 3), (4, 1)]
[ModernTCN V2 multi-seed] dry-run finished.
PS E:\Matlab\Simulink\S-Function_16> python src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py `
>>   --dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat `
>>   --run-tag-prefix modern_tcn_causal_theta10_uniform_h0_v2 `
>>   --seeds 11 21 42 73 101 `
>>   --temporal-padding causal `
>>   --epochs 180 `
>>   --batch-size 256 `
>>   --lr 1e-3 `
>>   --weight-decay 1e-4 `
>>   --patience 35 `
>>   --min-epochs 50
[ModernTCN V2 multi-seed]
  dataset: E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  seeds: [11, 21, 42, 73, 101]
  temporal_padding: causal
  theta_gate_mode: none
  theta_flat_loss_mode: near_zero, tol=0.3 deg

[ModernTCN V2 multi-seed] seed 11 (1/5)
[ModernTCN] 第一阶段训练开始
  seed=11, device=cuda, out=E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11
  dataset=E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  train/val/test=18302/2607/3733
  model channels=64, blocks=5, kernel=31, temporal_padding=causal
  epoch 001 | train=0.7264 val=0.5175 main=0.8262 turn=0.6548 turnL=0.6130 turnT=0.4143 theta=2.6312 score=6.7153
  epoch 005 | train=0.1650 val=0.3327 main=0.9287 turn=0.6893 turnL=0.6341 turnT=0.4405 theta=1.4463 score=3.5963
  epoch 010 | train=0.1131 val=0.2309 main=0.9474 turn=0.6954 turnL=0.6169 turnT=0.4857 theta=1.4766 score=3.0986
  epoch 015 | train=0.0794 val=0.2666 main=0.9471 turn=0.7173 turnL=0.6360 turnT=0.5024 theta=1.4519 score=2.8577
  epoch 020 | train=0.0761 val=0.2257 main=0.9662 turn=0.7081 turnL=0.6648 turnT=0.5214 theta=1.1492 score=2.3045
  epoch 025 | train=0.0590 val=0.2363 main=0.9655 turn=0.7188 turnL=0.6743 turnT=0.5476 theta=1.1180 score=2.5761
  epoch 030 | train=0.0532 val=0.1921 main=0.9659 turn=0.6951 turnL=0.7759 turnT=0.5310 theta=1.1112 score=2.3099
  epoch 035 | train=0.0455 val=0.2290 main=0.9689 turn=0.7112 turnL=0.7241 turnT=0.5333 theta=1.2572 score=2.0605
  epoch 040 | train=0.0437 val=0.3063 main=0.9636 turn=0.7633 turnL=0.7165 turnT=0.6000 theta=1.6561 score=2.4246
  epoch 045 | train=0.0379 val=0.2658 main=0.9682 turn=0.7637 turnL=0.7165 turnT=0.5929 theta=0.5293 score=1.0746
  epoch 050 | train=0.0292 val=0.2968 main=0.9639 turn=0.7691 turnL=0.7337 turnT=0.5667 theta=0.5438 score=1.0451
  epoch 055 | train=0.0282 val=0.2640 main=0.9659 turn=0.7825 turnL=0.7529 turnT=0.6167 theta=0.4243 score=0.9321
  epoch 060 | train=0.0238 val=0.2784 main=0.9655 turn=0.7817 turnL=0.8065 turnT=0.6381 theta=0.5583 score=0.9772
  epoch 065 | train=0.0247 val=0.3420 main=0.9586 turn=0.7898 turnL=0.7682 turnT=0.6286 theta=0.4505 score=1.0022
  epoch 070 | train=0.0191 val=0.3510 main=0.9574 turn=0.7840 turnL=0.8352 turnT=0.6310 theta=0.3723 score=0.9640
  epoch 075 | train=0.0143 val=0.2853 main=0.9651 turn=0.7898 turnL=0.8008 turnT=0.6405 theta=0.3420 score=0.8423
  epoch 080 | train=0.0181 val=0.2827 main=0.9651 turn=0.7956 turnL=0.8142 turnT=0.6238 theta=0.4058 score=0.9374
  epoch 085 | train=0.0149 val=0.2993 main=0.9651 turn=0.7967 turnL=0.8123 turnT=0.6214 theta=0.3493 score=0.9353
  epoch 090 | train=0.0131 val=0.2939 main=0.9670 turn=0.8094 turnL=0.7931 turnT=0.6690 theta=0.3609 score=0.8267
  epoch 095 | train=0.0126 val=0.2798 main=0.9655 turn=0.8101 turnL=0.8238 turnT=0.6595 theta=0.8749 score=1.2433
  epoch 100 | train=0.0167 val=0.3231 main=0.9655 turn=0.8044 turnL=0.8065 turnT=0.6548 theta=0.2911 score=0.8515
  epoch 105 | train=0.0098 val=0.3249 main=0.9613 turn=0.7990 turnL=0.8352 turnT=0.6619 theta=0.3254 score=0.8471
  epoch 110 | train=0.0102 val=0.3092 main=0.9651 turn=0.8170 turnL=0.8218 turnT=0.6857 theta=0.2610 score=0.8008
  epoch 115 | train=0.0091 val=0.3165 main=0.9674 turn=0.8182 turnL=0.8276 turnT=0.6762 theta=0.2893 score=0.7841
  epoch 120 | train=0.0079 val=0.3265 main=0.9678 turn=0.8147 turnL=0.8008 turnT=0.6857 theta=0.2615 score=0.7965
  epoch 125 | train=0.0083 val=0.3304 main=0.9659 turn=0.8105 turnL=0.8276 turnT=0.6857 theta=0.3269 score=0.8105
  epoch 130 | train=0.0070 val=0.3871 main=0.9586 turn=0.8209 turnL=0.8142 turnT=0.6833 theta=0.2828 score=0.8585
  epoch 135 | train=0.0075 val=0.3318 main=0.9651 turn=0.8209 turnL=0.8008 turnT=0.6881 theta=0.2855 score=0.7957
  epoch 140 | train=0.0055 val=0.3399 main=0.9674 turn=0.8105 turnL=0.8142 turnT=0.6476 theta=0.3165 score=0.8500
  epoch 145 | train=0.0057 val=0.3457 main=0.9651 turn=0.8178 turnL=0.8103 turnT=0.6833 theta=0.2870 score=0.8178
  epoch 150 | train=0.0050 val=0.3451 main=0.9639 turn=0.8209 turnL=0.8065 turnT=0.6833 theta=0.2827 score=0.7845
  epoch 155 | train=0.0058 val=0.3490 main=0.9662 turn=0.8201 turnL=0.8123 turnT=0.6952 theta=0.2804 score=0.7891
  epoch 160 | train=0.0046 val=0.3229 main=0.9678 turn=0.8243 turnL=0.8142 turnT=0.6905 theta=0.2347 score=0.7408
  epoch 165 | train=0.0048 val=0.3498 main=0.9659 turn=0.8228 turnL=0.8123 turnT=0.6905 theta=0.2404 score=0.7730
  epoch 170 | train=0.0042 val=0.3470 main=0.9666 turn=0.8174 turnL=0.8027 turnT=0.6762 theta=0.2397 score=0.7854
  epoch 175 | train=0.0044 val=0.3431 main=0.9670 turn=0.8239 turnL=0.8142 turnT=0.6952 theta=0.2446 score=0.7561
  epoch 180 | train=0.0048 val=0.3415 main=0.9674 turn=0.8213 turnL=0.8046 turnT=0.6833 theta=0.2376 score=0.7655
[ModernTCN] 训练完成
  checkpoint: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11.pt
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\modern_tcn_seed11_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed11\ModernTCN_train_report.md
  test main=0.9783, turnT=0.7907, turnL=0.9016, theta=0.2507, flat=0.9590, slope=0.9948

[ModernTCN V2 multi-seed] seed 21 (2/5)
[ModernTCN] 第一阶段训练开始
  seed=21, device=cuda, out=E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed21
  dataset=E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  train/val/test=18302/2607/3733
  model channels=64, blocks=5, kernel=31, temporal_padding=causal
  epoch 001 | train=0.7159 val=0.4567 main=0.8542 turn=0.6433 turnL=0.6820 turnT=0.3476 theta=3.4944 score=8.4487
  epoch 005 | train=0.1543 val=0.2300 main=0.9432 turn=0.6970 turnL=0.6590 turnT=0.4429 theta=1.6227 score=3.4642
  epoch 010 | train=0.1075 val=0.2377 main=0.9509 turn=0.7031 turnL=0.5977 turnT=0.4881 theta=1.1610 score=2.7720
  epoch 015 | train=0.0834 val=0.2285 main=0.9593 turn=0.7046 turnL=0.6782 turnT=0.4929 theta=1.0788 score=2.3506
  epoch 020 | train=0.0750 val=0.2614 main=0.9605 turn=0.6916 turnL=0.7107 turnT=0.4762 theta=0.8865 score=2.1077
  epoch 025 | train=0.0557 val=0.2774 main=0.9632 turn=0.7265 turnL=0.7759 turnT=0.5286 theta=0.9170 score=2.0856
  epoch 030 | train=0.0584 val=0.2493 main=0.9655 turn=0.7315 turnL=0.7471 turnT=0.5405 theta=1.1783 score=2.4505
  epoch 035 | train=0.0438 val=0.2258 main=0.9678 turn=0.7246 turnL=0.7126 turnT=0.5357 theta=1.3896 score=2.4679
  epoch 040 | train=0.0410 val=0.2601 main=0.9655 turn=0.7449 turnL=0.7778 turnT=0.5833 theta=0.5102 score=1.1431
  epoch 045 | train=0.0335 val=0.2969 main=0.9620 turn=0.7549 turnL=0.7739 turnT=0.5690 theta=0.6316 score=1.2668
  epoch 050 | train=0.0277 val=0.2903 main=0.9659 turn=0.7660 turnL=0.7567 turnT=0.5810 theta=0.5099 score=1.0377
  epoch 055 | train=0.0279 val=0.2923 main=0.9620 turn=0.7695 turnL=0.8046 turnT=0.6024 theta=0.5861 score=1.2185
  epoch 060 | train=0.0248 val=0.2974 main=0.9685 turn=0.7687 turnL=0.8295 turnT=0.6190 theta=0.4739 score=0.9702
  epoch 065 | train=0.0242 val=0.3623 main=0.9620 turn=0.7649 turnL=0.8008 turnT=0.6048 theta=0.7500 score=1.4831
  epoch 070 | train=0.0198 val=0.3295 main=0.9701 turn=0.7675 turnL=0.7835 turnT=0.6190 theta=0.4880 score=1.0865
  epoch 075 | train=0.0199 val=0.3071 main=0.9720 turn=0.7971 turnL=0.7414 turnT=0.6357 theta=0.4294 score=0.9545
  epoch 080 | train=0.0152 val=0.3136 main=0.9693 turn=0.7936 turnL=0.7395 turnT=0.6643 theta=0.6800 score=1.1632
  epoch 085 | train=0.0182 val=0.3388 main=0.9666 turn=0.8048 turnL=0.7816 turnT=0.6405 theta=0.3623 score=0.9081
  epoch 090 | train=0.0111 val=0.4095 main=0.9651 turn=0.8063 turnL=0.7989 turnT=0.6619 theta=0.2984 score=0.9026
  epoch 095 | train=0.0123 val=0.3989 main=0.9643 turn=0.7944 turnL=0.7701 turnT=0.6714 theta=0.3130 score=0.8949
  epoch 100 | train=0.0090 val=0.3695 main=0.9689 turn=0.7975 turnL=0.7969 turnT=0.6714 theta=0.2775 score=0.8197
  epoch 105 | train=0.0097 val=0.4144 main=0.9655 turn=0.7959 turnL=0.7701 turnT=0.6833 theta=0.3393 score=0.9109
  epoch 110 | train=0.0079 val=0.4108 main=0.9624 turn=0.8147 turnL=0.7759 turnT=0.7000 theta=0.3494 score=0.8755
  epoch 115 | train=0.0077 val=0.4175 main=0.9639 turn=0.8117 turnL=0.8046 turnT=0.7000 theta=0.2879 score=0.8875
[ModernTCN] 早停：epoch=117, best_epoch=82
[ModernTCN] 训练完成
  checkpoint: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed21\modern_tcn_seed21.pt
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed21\modern_tcn_seed21_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed21\ModernTCN_train_report.md
  test main=0.9759, turnT=0.7477, turnL=0.8893, theta=0.3624, flat=0.9709, slope=0.9892

[ModernTCN V2 multi-seed] seed 42 (3/5)
[ModernTCN] 第一阶段训练开始
  seed=42, device=cuda, out=E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed42
  dataset=E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  train/val/test=18302/2607/3733
  model channels=64, blocks=5, kernel=31, temporal_padding=causal
  epoch 001 | train=0.7369 val=0.4338 main=0.8504 turn=0.6444 turnL=0.6705 turnT=0.3524 theta=2.9543 score=6.7926
  epoch 005 | train=0.1640 val=0.2980 main=0.9367 turn=0.6674 turnL=0.7337 turnT=0.4333 theta=2.4122 score=5.1565
  epoch 010 | train=0.1083 val=0.2367 main=0.9532 turn=0.6843 turnL=0.6858 turnT=0.4786 theta=1.6130 score=3.2612
  epoch 015 | train=0.0837 val=0.2910 main=0.9471 turn=0.7100 turnL=0.6935 turnT=0.4952 theta=1.2520 score=3.0001
  epoch 020 | train=0.0696 val=0.3181 main=0.9494 turn=0.7296 turnL=0.6705 turnT=0.5238 theta=1.2176 score=2.3127
  epoch 025 | train=0.0596 val=0.2969 main=0.9563 turn=0.7146 turnL=0.6188 turnT=0.4976 theta=0.7886 score=1.8715
  epoch 030 | train=0.0499 val=0.3967 main=0.9432 turn=0.7131 turnL=0.7337 turnT=0.5167 theta=0.7492 score=1.9101
  epoch 035 | train=0.0396 val=0.4124 main=0.9467 turn=0.7349 turnL=0.7031 turnT=0.5381 theta=0.6520 score=1.4349
  epoch 040 | train=0.0458 val=0.3340 main=0.9540 turn=0.7484 turnL=0.7529 turnT=0.5381 theta=0.4752 score=1.2046
  epoch 045 | train=0.0334 val=0.3094 main=0.9743 turn=0.7702 turnL=0.7701 turnT=0.5524 theta=0.4416 score=1.1131
  epoch 050 | train=0.0358 val=0.2755 main=0.9701 turn=0.7534 turnL=0.7835 turnT=0.5667 theta=0.5895 score=1.2984
  epoch 055 | train=0.0284 val=0.2693 main=0.9620 turn=0.7733 turnL=0.7778 turnT=0.5524 theta=0.4629 score=0.9798
  epoch 060 | train=0.0243 val=0.3213 main=0.9639 turn=0.7722 turnL=0.7759 turnT=0.5786 theta=0.3503 score=0.9492
  epoch 065 | train=0.0242 val=0.3023 main=0.9609 turn=0.7748 turnL=0.7395 turnT=0.6095 theta=0.3660 score=0.8684
  epoch 070 | train=0.0228 val=0.3888 main=0.9586 turn=0.7840 turnL=0.7759 turnT=0.5714 theta=0.3466 score=1.0707
  epoch 075 | train=0.0203 val=0.3178 main=0.9636 turn=0.7860 turnL=0.7969 turnT=0.5786 theta=0.3009 score=0.8915
  epoch 080 | train=0.0142 val=0.3584 main=0.9639 turn=0.7817 turnL=0.7739 turnT=0.6048 theta=0.4752 score=1.2029
  epoch 085 | train=0.0157 val=0.3631 main=0.9651 turn=0.7837 turnL=0.7950 turnT=0.6024 theta=0.3244 score=1.0046
  epoch 090 | train=0.0127 val=0.4128 main=0.9624 turn=0.7979 turnL=0.7893 turnT=0.6286 theta=0.3511 score=0.9700
  epoch 095 | train=0.0118 val=0.3644 main=0.9643 turn=0.7871 turnL=0.7931 turnT=0.6214 theta=0.3131 score=0.9168
  epoch 100 | train=0.0126 val=0.3819 main=0.9662 turn=0.8009 turnL=0.7969 turnT=0.6119 theta=0.2977 score=0.9398
  epoch 105 | train=0.0098 val=0.3685 main=0.9601 turn=0.7936 turnL=0.7854 turnT=0.6190 theta=0.2655 score=0.8839
  epoch 110 | train=0.0093 val=0.3962 main=0.9628 turn=0.8182 turnL=0.7969 turnT=0.6571 theta=0.4153 score=0.9206
  epoch 115 | train=0.0077 val=0.3787 main=0.9639 turn=0.8028 turnL=0.7969 turnT=0.6119 theta=0.2661 score=0.9047
[ModernTCN] 早停：epoch=116, best_epoch=81
[ModernTCN] 训练完成
  checkpoint: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed42\modern_tcn_seed42.pt
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed42\modern_tcn_seed42_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed42\ModernTCN_train_report.md
  test main=0.9759, turnT=0.7383, turnL=0.9057, theta=0.3353, flat=0.9590, slope=0.9927
  seed42 gate pass=0
    - acc_turn_transition >= 0.7500 未满足，实际 0.7383

[ModernTCN V2 multi-seed] seed 73 (4/5)
[ModernTCN] 第一阶段训练开始
  seed=73, device=cuda, out=E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed73
  dataset=E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  train/val/test=18302/2607/3733
  model channels=64, blocks=5, kernel=31, temporal_padding=causal
  epoch 001 | train=0.7002 val=0.4527 main=0.8466 turn=0.6137 turnL=0.6897 turnT=0.3381 theta=2.8616 score=6.3106
  epoch 005 | train=0.1580 val=0.2644 main=0.9440 turn=0.6809 turnL=0.7778 turnT=0.4429 theta=1.8255 score=4.2317
  epoch 010 | train=0.0983 val=0.2160 main=0.9651 turn=0.6958 turnL=0.6916 turnT=0.4881 theta=1.1453 score=2.7594
  epoch 015 | train=0.0899 val=0.2482 main=0.9582 turn=0.7135 turnL=0.7184 turnT=0.5238 theta=1.8081 score=3.7489
  epoch 020 | train=0.0701 val=0.2596 main=0.9563 turn=0.7372 turnL=0.6264 turnT=0.5429 theta=1.0258 score=2.3445
  epoch 025 | train=0.0593 val=0.2181 main=0.9678 turn=0.7399 turnL=0.7011 turnT=0.5833 theta=0.8115 score=1.5775
  epoch 030 | train=0.0596 val=0.2400 main=0.9582 turn=0.7572 turnL=0.6571 turnT=0.5667 theta=0.7903 score=1.6094
  epoch 035 | train=0.0448 val=0.2306 main=0.9705 turn=0.7288 turnL=0.8352 turnT=0.5143 theta=0.6939 score=1.4073
  epoch 040 | train=0.0392 val=0.2273 main=0.9674 turn=0.7557 turnL=0.7625 turnT=0.5786 theta=1.3008 score=2.2904
  epoch 045 | train=0.0366 val=0.2572 main=0.9628 turn=0.7622 turnL=0.7529 turnT=0.5619 theta=0.4626 score=1.1070
  epoch 050 | train=0.0335 val=0.2901 main=0.9628 turn=0.7637 turnL=0.6513 turnT=0.6167 theta=0.7261 score=1.2238
  epoch 055 | train=0.0268 val=0.2707 main=0.9666 turn=0.7718 turnL=0.7854 turnT=0.6024 theta=0.3567 score=0.9366
  epoch 060 | train=0.0281 val=0.2419 main=0.9689 turn=0.7756 turnL=0.7874 turnT=0.6095 theta=0.3633 score=0.9268
  epoch 065 | train=0.0216 val=0.2507 main=0.9605 turn=0.7791 turnL=0.7778 turnT=0.5976 theta=0.3774 score=0.9550
  epoch 070 | train=0.0215 val=0.2702 main=0.9613 turn=0.7932 turnL=0.6839 turnT=0.6429 theta=0.3444 score=0.8873
  epoch 075 | train=0.0194 val=0.2580 main=0.9639 turn=0.7886 turnL=0.8008 turnT=0.6500 theta=0.4547 score=0.9683
  epoch 080 | train=0.0172 val=0.2765 main=0.9647 turn=0.7986 turnL=0.7778 turnT=0.6524 theta=0.3805 score=0.8543
  epoch 085 | train=0.0158 val=0.2675 main=0.9693 turn=0.8101 turnL=0.7625 turnT=0.6619 theta=0.3908 score=0.8680
  epoch 090 | train=0.0124 val=0.2781 main=0.9628 turn=0.8143 turnL=0.8065 turnT=0.6548 theta=0.4065 score=0.8762
  epoch 095 | train=0.0132 val=0.2745 main=0.9689 turn=0.8086 turnL=0.7835 turnT=0.6595 theta=0.2947 score=0.8345
  epoch 100 | train=0.0117 val=0.2852 main=0.9678 turn=0.8159 turnL=0.7950 turnT=0.6643 theta=0.3657 score=0.8576
  epoch 105 | train=0.0127 val=0.3058 main=0.9639 turn=0.8094 turnL=0.7912 turnT=0.6667 theta=0.3038 score=0.8131
  epoch 110 | train=0.0084 val=0.3752 main=0.9574 turn=0.8170 turnL=0.8008 turnT=0.6714 theta=0.3862 score=0.9553
  epoch 115 | train=0.0080 val=0.3155 main=0.9647 turn=0.8239 turnL=0.8218 turnT=0.6667 theta=0.2837 score=0.8378
  epoch 120 | train=0.0090 val=0.3196 main=0.9651 turn=0.8059 turnL=0.7950 turnT=0.6476 theta=0.2740 score=0.8633
  epoch 125 | train=0.0067 val=0.3005 main=0.9662 turn=0.8262 turnL=0.8008 turnT=0.7095 theta=0.3031 score=0.7448
  epoch 130 | train=0.0069 val=0.3327 main=0.9666 turn=0.8220 turnL=0.8027 turnT=0.6952 theta=0.3109 score=0.8283
  epoch 135 | train=0.0062 val=0.3366 main=0.9655 turn=0.8220 turnL=0.8123 turnT=0.6881 theta=0.2861 score=0.8149
  epoch 140 | train=0.0061 val=0.3165 main=0.9670 turn=0.8274 turnL=0.8046 turnT=0.6952 theta=0.2600 score=0.7714
  epoch 145 | train=0.0055 val=0.3215 main=0.9670 turn=0.8343 turnL=0.8123 turnT=0.7071 theta=0.2496 score=0.7459
  epoch 150 | train=0.0057 val=0.3342 main=0.9682 turn=0.8278 turnL=0.8008 turnT=0.6857 theta=0.2546 score=0.7923
  epoch 155 | train=0.0050 val=0.3182 main=0.9678 turn=0.8293 turnL=0.8084 turnT=0.6857 theta=0.2610 score=0.7772
  epoch 160 | train=0.0049 val=0.3316 main=0.9636 turn=0.8282 turnL=0.8027 turnT=0.6905 theta=0.2628 score=0.7924
  epoch 165 | train=0.0041 val=0.3197 main=0.9666 turn=0.8297 turnL=0.8103 turnT=0.7000 theta=0.2529 score=0.7576
  epoch 170 | train=0.0047 val=0.3168 main=0.9670 turn=0.8282 turnL=0.8084 turnT=0.6952 theta=0.2498 score=0.7563
  epoch 175 | train=0.0046 val=0.3250 main=0.9662 turn=0.8297 turnL=0.8103 turnT=0.6952 theta=0.2510 score=0.7675
  epoch 180 | train=0.0048 val=0.3143 main=0.9670 turn=0.8270 turnL=0.8084 turnT=0.7000 theta=0.2527 score=0.7570
[ModernTCN] 训练完成
  checkpoint: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed73\modern_tcn_seed73.pt
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed73\modern_tcn_seed73_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed73\ModernTCN_train_report.md
  test main=0.9770, turnT=0.7888, turnL=0.9194, theta=0.2682, flat=0.9564, slope=0.9951

[ModernTCN V2 multi-seed] seed 101 (5/5)
[ModernTCN] 第一阶段训练开始
  seed=101, device=cuda, out=E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed101
  dataset=E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
  train/val/test=18302/2607/3733
  model channels=64, blocks=5, kernel=31, temporal_padding=causal
  epoch 001 | train=0.7249 val=0.4847 main=0.8408 turn=0.6038 turnL=0.6897 turnT=0.3500 theta=3.0010 score=7.8566
  epoch 005 | train=0.1654 val=0.2532 main=0.9336 turn=0.6989 turnL=0.6628 turnT=0.4548 theta=1.9237 score=3.9994
  epoch 010 | train=0.1063 val=0.2326 main=0.9379 turn=0.6935 turnL=0.6858 turnT=0.5071 theta=1.4734 score=3.5298
  epoch 015 | train=0.0830 val=0.2033 main=0.9609 turn=0.6878 turnL=0.7510 turnT=0.5167 theta=2.3753 score=4.0417
  epoch 020 | train=0.0671 val=0.2534 main=0.9582 turn=0.7296 turnL=0.7011 turnT=0.5452 theta=1.0508 score=2.3094
  epoch 025 | train=0.0568 val=0.1914 main=0.9655 turn=0.7430 turnL=0.7203 turnT=0.5452 theta=0.8324 score=1.8088
  epoch 030 | train=0.0493 val=0.2532 main=0.9601 turn=0.7300 turnL=0.7107 turnT=0.5786 theta=0.7876 score=1.7316
  epoch 035 | train=0.0462 val=0.2511 main=0.9647 turn=0.7534 turnL=0.7663 turnT=0.6071 theta=0.5585 score=1.3533
  epoch 040 | train=0.0356 val=0.2791 main=0.9624 turn=0.7618 turnL=0.7529 turnT=0.6095 theta=0.4607 score=1.0951
  epoch 045 | train=0.0321 val=0.2450 main=0.9682 turn=0.7748 turnL=0.7356 turnT=0.6024 theta=0.4406 score=0.9518
  epoch 050 | train=0.0250 val=0.2853 main=0.9662 turn=0.7672 turnL=0.7682 turnT=0.5810 theta=0.9858 score=1.6354
  epoch 055 | train=0.0255 val=0.2971 main=0.9632 turn=0.7668 turnL=0.8180 turnT=0.5762 theta=0.4671 score=1.0763
  epoch 060 | train=0.0208 val=0.2267 main=0.9778 turn=0.7710 turnL=0.8046 turnT=0.6262 theta=0.3799 score=0.8109
  epoch 065 | train=0.0207 val=0.2353 main=0.9685 turn=0.7637 turnL=0.7931 turnT=0.6262 theta=0.3511 score=0.8563
  epoch 070 | train=0.0172 val=0.3161 main=0.9590 turn=0.7706 turnL=0.7816 turnT=0.6143 theta=0.4639 score=1.0748
  epoch 075 | train=0.0175 val=0.3157 main=0.9655 turn=0.7952 turnL=0.7625 turnT=0.6476 theta=0.4117 score=1.0105
  epoch 080 | train=0.0150 val=0.3137 main=0.9624 turn=0.7875 turnL=0.8027 turnT=0.6262 theta=0.4168 score=1.0073
  epoch 085 | train=0.0153 val=0.2715 main=0.9674 turn=0.8021 turnL=0.7701 turnT=0.6714 theta=0.5233 score=0.8547
  epoch 090 | train=0.0108 val=0.3281 main=0.9662 turn=0.7909 turnL=0.7912 turnT=0.6667 theta=0.2946 score=0.8188
  epoch 095 | train=0.0108 val=0.2905 main=0.9712 turn=0.8051 turnL=0.8103 turnT=0.6548 theta=0.5434 score=0.9248
  epoch 100 | train=0.0090 val=0.3354 main=0.9643 turn=0.8044 turnL=0.8161 turnT=0.6595 theta=0.3260 score=0.8362
  epoch 105 | train=0.0091 val=0.3856 main=0.9590 turn=0.8178 turnL=0.7816 turnT=0.6857 theta=0.2968 score=0.8871
  epoch 110 | train=0.0095 val=0.3463 main=0.9651 turn=0.8097 turnL=0.8046 turnT=0.6595 theta=0.3385 score=0.8253
  epoch 115 | train=0.0096 val=0.3591 main=0.9620 turn=0.8132 turnL=0.8008 turnT=0.6833 theta=0.3068 score=0.8273
  epoch 120 | train=0.0071 val=0.3441 main=0.9655 turn=0.8151 turnL=0.8084 turnT=0.6929 theta=0.2666 score=0.7683
  epoch 125 | train=0.0069 val=0.3403 main=0.9674 turn=0.8193 turnL=0.8161 turnT=0.6714 theta=0.2654 score=0.7999
  epoch 130 | train=0.0058 val=0.3276 main=0.9678 turn=0.8224 turnL=0.8103 turnT=0.6643 theta=0.3550 score=0.9381
[ModernTCN] 早停：epoch=132, best_epoch=97
[ModernTCN] 训练完成
  checkpoint: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed101\modern_tcn_seed101.pt
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed101\modern_tcn_seed101_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_seed101\ModernTCN_train_report.md
  test main=0.9772, turnT=0.7421, turnL=0.9262, theta=0.2918, flat=0.9590, slope=0.9962

[ModernTCN V2 multi-seed] all seeds finished
  summary: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_multiseed_summary.csv
  report: E:\Matlab\Simulink\S-Function_16\results\modern_tcn\modern_tcn_causal_theta10_uniform_h0_v2_multiseed_report.md