# TCN Training Data Generation Report

- Generated: 2026-05-05 03:25:34
- Output: `E:\Matlab\Simulink\S-Function_16\data\tcn\ModernTCN_train_data_v4_industrial.mat`
- Model: `GRU_DataGen`
- Valid runs: 752
- Failed runs: 0
- Total samples: 2368752

## Label Distribution

| label | count | ratio |
|---|---:|---:|
| flat | 1570127 | 0.6628 |
| stall | 94656 | 0.0400 |
| slope | 703969 | 0.2972 |
| turn right | 349340 | 0.1475 |
| turn straight | 1684744 | 0.7112 |
| turn left | 334668 | 0.1413 |
| slip aux | 47307 | 0.0200 |
| stall aux | 94656 | 0.0400 |
| load_change aux | 84011 | 0.0355 |

## Transition Coverage

- Runs with dynamic windows: 752
- Dynamic window hits: 1840

## Event Coverage

- Runs with slip labels: 243
- Runs with stall labels: 383
- Runs with load-change labels: 339

## Paths

- `path_modern_tcn_v4_01_v4_flat_straight_v08`
- `path_modern_tcn_v4_02_v4_flat_straight_v09`
- `path_modern_tcn_v4_03_v4_flat_straight_v10`
- `path_modern_tcn_v4_04_v4_flat_straight_v11`
- `path_modern_tcn_v4_05_flat_turn_R_v08_R06`
- `path_modern_tcn_v4_06_flat_turn_L_v08_R06`
- `path_modern_tcn_v4_07_flat_turn_R_v08_R07`
- `path_modern_tcn_v4_08_flat_turn_L_v08_R07`
- `path_modern_tcn_v4_09_flat_turn_R_v08_R08`
- `path_modern_tcn_v4_100_v4_slope_straight_v10_thm01`
- `path_modern_tcn_v4_101_v4_slope_straight_v10_thp01`
- `path_modern_tcn_v4_102_v4_slope_straight_v10_thp02`
- `path_modern_tcn_v4_103_v4_slope_straight_v10_thp03`
- `path_modern_tcn_v4_104_v4_slope_straight_v10_thp04`
- `path_modern_tcn_v4_105_v4_slope_straight_v10_thp05`
- `path_modern_tcn_v4_106_v4_slope_straight_v10_thp06`
- `path_modern_tcn_v4_107_v4_slope_straight_v10_thp07`
- `path_modern_tcn_v4_108_v4_slope_straight_v10_thp08`
- `path_modern_tcn_v4_109_v4_slope_straight_v11_thm08`
- `path_modern_tcn_v4_10_flat_turn_L_v08_R08`
- `path_modern_tcn_v4_110_v4_slope_straight_v11_thm07`
- `path_modern_tcn_v4_111_v4_slope_straight_v11_thm06`
- `path_modern_tcn_v4_112_v4_slope_straight_v11_thm05`
- `path_modern_tcn_v4_113_v4_slope_straight_v11_thm04`
- `path_modern_tcn_v4_114_v4_slope_straight_v11_thm03`
- `path_modern_tcn_v4_115_v4_slope_straight_v11_thm02`
- `path_modern_tcn_v4_116_v4_slope_straight_v11_thm01`
- `path_modern_tcn_v4_117_v4_slope_straight_v11_thp01`
- `path_modern_tcn_v4_118_v4_slope_straight_v11_thp02`
- `path_modern_tcn_v4_119_v4_slope_straight_v11_thp03`
- `path_modern_tcn_v4_11_flat_turn_R_v08_R09`
- `path_modern_tcn_v4_120_v4_slope_straight_v11_thp04`
- `path_modern_tcn_v4_121_v4_slope_straight_v11_thp05`
- `path_modern_tcn_v4_122_v4_slope_straight_v11_thp06`
- `path_modern_tcn_v4_123_v4_slope_straight_v11_thp07`
- `path_modern_tcn_v4_124_v4_slope_straight_v11_thp08`
- `path_modern_tcn_v4_125_v4_slope_turn_entry_R_v08_R06_thm06`
- `path_modern_tcn_v4_126_v4_slope_turn_entry_L_v09_R07_thm06`
- `path_modern_tcn_v4_127_v4_slope_turn_entry_R_v09_R08_thm05`
- `path_modern_tcn_v4_128_v4_slope_turn_entry_L_v10_R09_thm05`
- `path_modern_tcn_v4_129_v4_slope_turn_entry_R_v10_R10_thm04`
- `path_modern_tcn_v4_12_flat_turn_L_v08_R09`
- `path_modern_tcn_v4_130_v4_slope_turn_entry_L_v11_R11_thm04`
- `path_modern_tcn_v4_131_v4_slope_turn_entry_R_v11_R12_thm03`
- `path_modern_tcn_v4_132_v4_slope_turn_entry_L_v08_R06_thm03`
- `path_modern_tcn_v4_133_v4_slope_turn_entry_R_v08_R07_thp03`
- `path_modern_tcn_v4_134_v4_slope_turn_entry_L_v09_R08_thp03`
- `path_modern_tcn_v4_135_v4_slope_turn_entry_R_v09_R09_thp04`
- `path_modern_tcn_v4_136_v4_slope_turn_entry_L_v10_R10_thp04`
- `path_modern_tcn_v4_137_v4_slope_turn_entry_R_v10_R11_thp05`
- `path_modern_tcn_v4_138_v4_slope_turn_entry_L_v11_R12_thp05`
- `path_modern_tcn_v4_139_v4_slope_turn_entry_R_v11_R06_thp06`
- `path_modern_tcn_v4_13_flat_turn_R_v08_R10`
- `path_modern_tcn_v4_140_v4_slope_turn_entry_L_v08_R07_thp06`
- `path_modern_tcn_v4_141_v4_slope_turn_middle_R_v09_R07_thm06`
- `path_modern_tcn_v4_142_v4_slope_turn_middle_L_v10_R08_thm06`
- `path_modern_tcn_v4_143_v4_slope_turn_middle_R_v10_R09_thm05`
- `path_modern_tcn_v4_144_v4_slope_turn_middle_L_v11_R10_thm05`
- `path_modern_tcn_v4_145_v4_slope_turn_middle_R_v11_R11_thm04`
- `path_modern_tcn_v4_146_v4_slope_turn_middle_L_v08_R12_thm04`
- `path_modern_tcn_v4_147_v4_slope_turn_middle_R_v08_R06_thm03`
- `path_modern_tcn_v4_148_v4_slope_turn_middle_L_v09_R07_thm03`
- `path_modern_tcn_v4_149_v4_slope_turn_middle_R_v09_R08_thp03`
- `path_modern_tcn_v4_14_flat_turn_L_v08_R10`
- `path_modern_tcn_v4_150_v4_slope_turn_middle_L_v10_R09_thp03`
- `path_modern_tcn_v4_151_v4_slope_turn_middle_R_v10_R10_thp04`
- `path_modern_tcn_v4_152_v4_slope_turn_middle_L_v11_R11_thp04`
- `path_modern_tcn_v4_153_v4_slope_turn_middle_R_v11_R12_thp05`
- `path_modern_tcn_v4_154_v4_slope_turn_middle_L_v08_R06_thp05`
- `path_modern_tcn_v4_155_v4_slope_turn_middle_R_v08_R07_thp06`
- `path_modern_tcn_v4_156_v4_slope_turn_middle_L_v09_R08_thp06`
- `path_modern_tcn_v4_157_v4_slope_turn_exit_R_v10_R08_thm06`
- `path_modern_tcn_v4_158_v4_slope_turn_exit_L_v11_R09_thm06`
- `path_modern_tcn_v4_159_v4_slope_turn_exit_R_v11_R10_thm05`
- `path_modern_tcn_v4_15_flat_turn_R_v08_R11`
- `path_modern_tcn_v4_160_v4_slope_turn_exit_L_v08_R11_thm05`
- `path_modern_tcn_v4_161_v4_slope_turn_exit_R_v08_R12_thm04`
- `path_modern_tcn_v4_162_v4_slope_turn_exit_L_v09_R06_thm04`
- `path_modern_tcn_v4_163_v4_slope_turn_exit_R_v09_R07_thm03`
- `path_modern_tcn_v4_164_v4_slope_turn_exit_L_v10_R08_thm03`
- `path_modern_tcn_v4_165_v4_slope_turn_exit_R_v10_R09_thp03`
- `path_modern_tcn_v4_166_v4_slope_turn_exit_L_v11_R10_thp03`
- `path_modern_tcn_v4_167_v4_slope_turn_exit_R_v11_R11_thp04`
- `path_modern_tcn_v4_168_v4_slope_turn_exit_L_v08_R12_thp04`
- `path_modern_tcn_v4_169_v4_slope_turn_exit_R_v08_R06_thp05`
- `path_modern_tcn_v4_16_flat_turn_L_v08_R11`
- `path_modern_tcn_v4_170_v4_slope_turn_exit_L_v09_R07_thp05`
- `path_modern_tcn_v4_171_v4_slope_turn_exit_R_v09_R08_thp06`
- `path_modern_tcn_v4_172_v4_slope_turn_exit_L_v10_R09_thp06`
- `path_modern_tcn_v4_173_v4_flat_s_curve_v08_R07`
- `path_modern_tcn_v4_174_v4_flat_s_curve_v08_R09`
- `path_modern_tcn_v4_175_v4_flat_s_curve_v08_R11`
- `path_modern_tcn_v4_176_v4_flat_s_curve_v09_R07`
- `path_modern_tcn_v4_177_v4_flat_s_curve_v09_R09`
- `path_modern_tcn_v4_178_v4_flat_s_curve_v09_R11`
- `path_modern_tcn_v4_179_v4_flat_s_curve_v10_R07`
- `path_modern_tcn_v4_17_flat_turn_R_v08_R12`
- `path_modern_tcn_v4_180_v4_flat_s_curve_v10_R09`
- `path_modern_tcn_v4_181_v4_flat_s_curve_v10_R11`
- `path_modern_tcn_v4_182_v4_flat_s_curve_v11_R07`
- `path_modern_tcn_v4_183_v4_flat_s_curve_v11_R09`
- `path_modern_tcn_v4_184_v4_flat_s_curve_v11_R11`
- `path_modern_tcn_v4_185_v4_theta_reversal_s_curve_thm05_R`
- `path_modern_tcn_v4_186_v4_theta_reversal_s_curve_thm05_L`
- `path_modern_tcn_v4_187_v4_theta_reversal_s_curve_thp05_R`
- `path_modern_tcn_v4_188_v4_theta_reversal_s_curve_thp05_L`
- `path_modern_tcn_v4_18_flat_turn_L_v08_R12`
- `path_modern_tcn_v4_19_flat_turn_R_v09_R06`
- `path_modern_tcn_v4_20_flat_turn_L_v09_R06`
- `path_modern_tcn_v4_21_flat_turn_R_v09_R07`
- `path_modern_tcn_v4_22_flat_turn_L_v09_R07`
- `path_modern_tcn_v4_23_flat_turn_R_v09_R08`
- `path_modern_tcn_v4_24_flat_turn_L_v09_R08`
- `path_modern_tcn_v4_25_flat_turn_R_v09_R09`
- `path_modern_tcn_v4_26_flat_turn_L_v09_R09`
- `path_modern_tcn_v4_27_flat_turn_R_v09_R10`
- `path_modern_tcn_v4_28_flat_turn_L_v09_R10`
- `path_modern_tcn_v4_29_flat_turn_R_v09_R11`
- `path_modern_tcn_v4_30_flat_turn_L_v09_R11`
- `path_modern_tcn_v4_31_flat_turn_R_v09_R12`
- `path_modern_tcn_v4_32_flat_turn_L_v09_R12`
- `path_modern_tcn_v4_33_flat_turn_R_v10_R06`
- `path_modern_tcn_v4_34_flat_turn_L_v10_R06`
- `path_modern_tcn_v4_35_flat_turn_R_v10_R07`
- `path_modern_tcn_v4_36_flat_turn_L_v10_R07`
- `path_modern_tcn_v4_37_flat_turn_R_v10_R08`
- `path_modern_tcn_v4_38_flat_turn_L_v10_R08`
- `path_modern_tcn_v4_39_flat_turn_R_v10_R09`
- `path_modern_tcn_v4_40_flat_turn_L_v10_R09`
- `path_modern_tcn_v4_41_flat_turn_R_v10_R10`
- `path_modern_tcn_v4_42_flat_turn_L_v10_R10`
- `path_modern_tcn_v4_43_flat_turn_R_v10_R11`
- `path_modern_tcn_v4_44_flat_turn_L_v10_R11`
- `path_modern_tcn_v4_45_flat_turn_R_v10_R12`
- `path_modern_tcn_v4_46_flat_turn_L_v10_R12`
- `path_modern_tcn_v4_47_flat_turn_R_v11_R06`
- `path_modern_tcn_v4_48_flat_turn_L_v11_R06`
- `path_modern_tcn_v4_49_flat_turn_R_v11_R07`
- `path_modern_tcn_v4_50_flat_turn_L_v11_R07`
- `path_modern_tcn_v4_51_flat_turn_R_v11_R08`
- `path_modern_tcn_v4_52_flat_turn_L_v11_R08`
- `path_modern_tcn_v4_53_flat_turn_R_v11_R09`
- `path_modern_tcn_v4_54_flat_turn_L_v11_R09`
- `path_modern_tcn_v4_55_flat_turn_R_v11_R10`
- `path_modern_tcn_v4_56_flat_turn_L_v11_R10`
- `path_modern_tcn_v4_57_flat_turn_R_v11_R11`
- `path_modern_tcn_v4_58_flat_turn_L_v11_R11`
- `path_modern_tcn_v4_59_flat_turn_R_v11_R12`
- `path_modern_tcn_v4_60_flat_turn_L_v11_R12`
- `path_modern_tcn_v4_61_v4_slope_straight_v08_thm08`
- `path_modern_tcn_v4_62_v4_slope_straight_v08_thm07`
- `path_modern_tcn_v4_63_v4_slope_straight_v08_thm06`
- `path_modern_tcn_v4_64_v4_slope_straight_v08_thm05`
- `path_modern_tcn_v4_65_v4_slope_straight_v08_thm04`
- `path_modern_tcn_v4_66_v4_slope_straight_v08_thm03`
- `path_modern_tcn_v4_67_v4_slope_straight_v08_thm02`
- `path_modern_tcn_v4_68_v4_slope_straight_v08_thm01`
- `path_modern_tcn_v4_69_v4_slope_straight_v08_thp01`
- `path_modern_tcn_v4_70_v4_slope_straight_v08_thp02`
- `path_modern_tcn_v4_71_v4_slope_straight_v08_thp03`
- `path_modern_tcn_v4_72_v4_slope_straight_v08_thp04`
- `path_modern_tcn_v4_73_v4_slope_straight_v08_thp05`
- `path_modern_tcn_v4_74_v4_slope_straight_v08_thp06`
- `path_modern_tcn_v4_75_v4_slope_straight_v08_thp07`
- `path_modern_tcn_v4_76_v4_slope_straight_v08_thp08`
- `path_modern_tcn_v4_77_v4_slope_straight_v09_thm08`
- `path_modern_tcn_v4_78_v4_slope_straight_v09_thm07`
- `path_modern_tcn_v4_79_v4_slope_straight_v09_thm06`
- `path_modern_tcn_v4_80_v4_slope_straight_v09_thm05`
- `path_modern_tcn_v4_81_v4_slope_straight_v09_thm04`
- `path_modern_tcn_v4_82_v4_slope_straight_v09_thm03`
- `path_modern_tcn_v4_83_v4_slope_straight_v09_thm02`
- `path_modern_tcn_v4_84_v4_slope_straight_v09_thm01`
- `path_modern_tcn_v4_85_v4_slope_straight_v09_thp01`
- `path_modern_tcn_v4_86_v4_slope_straight_v09_thp02`
- `path_modern_tcn_v4_87_v4_slope_straight_v09_thp03`
- `path_modern_tcn_v4_88_v4_slope_straight_v09_thp04`
- `path_modern_tcn_v4_89_v4_slope_straight_v09_thp05`
- `path_modern_tcn_v4_90_v4_slope_straight_v09_thp06`
- `path_modern_tcn_v4_91_v4_slope_straight_v09_thp07`
- `path_modern_tcn_v4_92_v4_slope_straight_v09_thp08`
- `path_modern_tcn_v4_93_v4_slope_straight_v10_thm08`
- `path_modern_tcn_v4_94_v4_slope_straight_v10_thm07`
- `path_modern_tcn_v4_95_v4_slope_straight_v10_thm06`
- `path_modern_tcn_v4_96_v4_slope_straight_v10_thm05`
- `path_modern_tcn_v4_97_v4_slope_straight_v10_thm04`
- `path_modern_tcn_v4_98_v4_slope_straight_v10_thm03`
- `path_modern_tcn_v4_99_v4_slope_straight_v10_thm02`
