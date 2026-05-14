PS C:\\Users\\15754\\Desktop> cd E:\\Matlab\\Simulink\\S-Function\_16

PS E:\\Matlab\\Simulink\\S-Function\_16> cd E:\\Matlab\\Simulink\\S-Function\_16

PS E:\\Matlab\\Simulink\\S-Function\_16> python .\\src\\ModernTCN\\run\_modern\_tcn\_theta10\_v2\_multiseed.py --seeds 11 21 42 73 101

\[ModernTCN V2 multi-seed]

&#x20; dataset: E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; seeds: \[11, 21, 42, 73, 101]

&#x20; theta\_gate\_mode: none

&#x20; theta\_flat\_loss\_mode: near\_zero, tol=0.3 deg



\[ModernTCN V2 multi-seed] seed 11 (1/5)

\[ModernTCN] 第一阶段训练开始

&#x20; seed=11, device=cuda, out=E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed11

&#x20; dataset=E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; train/val/test=18302/2607/3733

&#x20; model channels=64, blocks=5, kernel=31

&#x20; epoch 001 | train=0.7347 val=0.5429 main=0.8025 turn=0.6486 turnL=0.5843 turnT=0.4024 theta=2.9213 score=7.4726

&#x20; epoch 005 | train=0.1687 val=0.3429 main=0.9122 turn=0.7035 turnL=0.6111 turnT=0.4548 theta=1.6871 score=3.9692

&#x20; epoch 010 | train=0.1137 val=0.2130 main=0.9574 turn=0.6774 turnL=0.6245 turnT=0.4881 theta=1.3577 score=2.9626

&#x20; epoch 015 | train=0.0782 val=0.1842 main=0.9685 turn=0.6997 turnL=0.6743 turnT=0.4714 theta=1.2104 score=2.4517

&#x20; epoch 020 | train=0.0680 val=0.1890 main=0.9751 turn=0.6786 turnL=0.7318 turnT=0.5429 theta=1.6573 score=3.2431

&#x20; epoch 025 | train=0.0538 val=0.2028 main=0.9755 turn=0.6816 turnL=0.7989 turnT=0.4976 theta=0.9262 score=1.9224

&#x20; epoch 030 | train=0.0560 val=0.1853 main=0.9789 turn=0.7208 turnL=0.7567 turnT=0.5143 theta=0.6148 score=1.3686

&#x20; epoch 035 | train=0.0397 val=0.1914 main=0.9808 turn=0.7227 turnL=0.7471 turnT=0.5310 theta=0.8027 score=1.6948

&#x20; epoch 040 | train=0.0399 val=0.2457 main=0.9743 turn=0.7238 turnL=0.7567 turnT=0.5476 theta=0.8333 score=2.0812

&#x20; epoch 045 | train=0.0377 val=0.2006 main=0.9774 turn=0.7434 turnL=0.8027 turnT=0.5762 theta=0.5403 score=1.0353

&#x20; epoch 050 | train=0.0273 val=0.2322 main=0.9728 turn=0.7499 turnL=0.7356 turnT=0.5762 theta=0.4881 score=0.9867

&#x20; epoch 055 | train=0.0267 val=0.2092 main=0.9793 turn=0.7649 turnL=0.7280 turnT=0.5905 theta=0.3674 score=0.9592

&#x20; epoch 060 | train=0.0263 val=0.2370 main=0.9693 turn=0.7526 turnL=0.7989 turnT=0.5810 theta=0.3977 score=0.9420

&#x20; epoch 065 | train=0.0231 val=0.2525 main=0.9651 turn=0.7737 turnL=0.7644 turnT=0.5929 theta=0.5562 score=1.0769

&#x20; epoch 070 | train=0.0167 val=0.2400 main=0.9708 turn=0.7675 turnL=0.8065 turnT=0.6262 theta=0.3899 score=1.0280

&#x20; epoch 075 | train=0.0148 val=0.2459 main=0.9755 turn=0.7675 turnL=0.7989 turnT=0.6143 theta=0.3851 score=0.9448

&#x20; epoch 080 | train=0.0196 val=0.2598 main=0.9728 turn=0.7990 turnL=0.7912 turnT=0.6429 theta=0.3133 score=0.8036

&#x20; epoch 085 | train=0.0149 val=0.2580 main=0.9751 turn=0.7710 turnL=0.7969 turnT=0.6214 theta=0.3321 score=0.8459

&#x20; epoch 090 | train=0.0123 val=0.2530 main=0.9708 turn=0.7883 turnL=0.7701 turnT=0.6190 theta=0.3305 score=0.8549

&#x20; epoch 095 | train=0.0123 val=0.2885 main=0.9689 turn=0.7814 turnL=0.7816 turnT=0.6095 theta=0.5360 score=0.9486

&#x20; epoch 100 | train=0.0128 val=0.2739 main=0.9747 turn=0.8040 turnL=0.7912 turnT=0.6381 theta=0.2997 score=0.8088

&#x20; epoch 105 | train=0.0086 val=0.2862 main=0.9739 turn=0.7829 turnL=0.7912 turnT=0.6286 theta=0.3308 score=0.8712

&#x20; epoch 110 | train=0.0086 val=0.2997 main=0.9743 turn=0.8013 turnL=0.7682 turnT=0.6381 theta=0.2682 score=0.8170

&#x20; epoch 115 | train=0.0088 val=0.2603 main=0.9762 turn=0.8082 turnL=0.7835 turnT=0.6405 theta=0.3098 score=0.8079

&#x20; epoch 120 | train=0.0068 val=0.2542 main=0.9735 turn=0.8120 turnL=0.7797 turnT=0.6405 theta=0.2668 score=0.8083

&#x20; epoch 125 | train=0.0072 val=0.2651 main=0.9735 turn=0.8059 turnL=0.7893 turnT=0.6429 theta=0.2600 score=0.7688

&#x20; epoch 130 | train=0.0063 val=0.3197 main=0.9712 turn=0.8040 turnL=0.7759 turnT=0.6476 theta=0.2981 score=0.8388

&#x20; epoch 135 | train=0.0061 val=0.2952 main=0.9716 turn=0.8182 turnL=0.7893 turnT=0.6881 theta=0.2337 score=0.7504

&#x20; epoch 140 | train=0.0052 val=0.3046 main=0.9728 turn=0.8078 turnL=0.7835 turnT=0.6405 theta=0.2496 score=0.8046

&#x20; epoch 145 | train=0.0048 val=0.2921 main=0.9728 turn=0.8166 turnL=0.7720 turnT=0.6524 theta=0.3091 score=0.8473

&#x20; epoch 150 | train=0.0049 val=0.2991 main=0.9747 turn=0.8048 turnL=0.7874 turnT=0.6429 theta=0.2387 score=0.7958

&#x20; epoch 155 | train=0.0047 val=0.2983 main=0.9731 turn=0.8201 turnL=0.7854 turnT=0.6595 theta=0.2600 score=0.7746

&#x20; epoch 160 | train=0.0042 val=0.2860 main=0.9724 turn=0.8182 turnL=0.7854 turnT=0.6643 theta=0.2369 score=0.7828

&#x20; epoch 165 | train=0.0042 val=0.3083 main=0.9728 turn=0.8147 turnL=0.7778 turnT=0.6571 theta=0.2345 score=0.7891

&#x20; epoch 170 | train=0.0038 val=0.2964 main=0.9728 turn=0.8147 turnL=0.7778 turnT=0.6524 theta=0.2305 score=0.7885

\[ModernTCN] 早停：epoch=170, best\_epoch=135

\[ModernTCN] 训练完成

&#x20; checkpoint: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed11\\modern\_tcn\_seed11.pt

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed11\\modern\_tcn\_seed11\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed11\\ModernTCN\_train\_report.md

&#x20; test main=0.9794, turnT=0.7551, turnL=0.8716, theta=0.2700, flat=0.9670, slope=0.9976



\[ModernTCN V2 multi-seed] seed 21 (2/5)

\[ModernTCN] 第一阶段训练开始

&#x20; seed=21, device=cuda, out=E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21

&#x20; dataset=E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; train/val/test=18302/2607/3733

&#x20; model channels=64, blocks=5, kernel=31

&#x20; epoch 001 | train=0.7121 val=0.4525 main=0.8688 turn=0.6222 turnL=0.6877 turnT=0.3405 theta=2.8354 score=6.8137

&#x20; epoch 005 | train=0.1646 val=0.2477 main=0.9432 turn=0.7035 turnL=0.6686 turnT=0.4524 theta=1.5374 score=3.6659

&#x20; epoch 010 | train=0.1031 val=0.1623 main=0.9609 turn=0.7123 turnL=0.6820 turnT=0.4881 theta=1.1696 score=2.6108

&#x20; epoch 015 | train=0.0820 val=0.1839 main=0.9693 turn=0.7161 turnL=0.7510 turnT=0.5000 theta=1.3002 score=2.3431

&#x20; epoch 020 | train=0.0713 val=0.1881 main=0.9628 turn=0.6897 turnL=0.6724 turnT=0.5167 theta=0.9504 score=1.9870

&#x20; epoch 025 | train=0.0538 val=0.1826 main=0.9716 turn=0.7142 turnL=0.7912 turnT=0.5238 theta=0.8773 score=1.7138

&#x20; epoch 030 | train=0.0520 val=0.2434 main=0.9643 turn=0.7112 turnL=0.7912 turnT=0.5333 theta=1.6121 score=3.3928

&#x20; epoch 035 | train=0.0438 val=0.2321 main=0.9728 turn=0.7284 turnL=0.7203 turnT=0.5238 theta=1.5607 score=2.3303

&#x20; epoch 040 | train=0.0413 val=0.2290 main=0.9705 turn=0.7564 turnL=0.7854 turnT=0.5762 theta=0.8949 score=1.9215

&#x20; epoch 045 | train=0.0320 val=0.2866 main=0.9643 turn=0.7418 turnL=0.7720 turnT=0.5810 theta=0.5380 score=1.1006

&#x20; epoch 050 | train=0.0258 val=0.2760 main=0.9651 turn=0.7764 turnL=0.7989 turnT=0.6071 theta=0.4514 score=1.0745

&#x20; epoch 055 | train=0.0294 val=0.2408 main=0.9632 turn=0.7610 turnL=0.7874 turnT=0.6143 theta=0.5581 score=0.9813

&#x20; epoch 060 | train=0.0211 val=0.2624 main=0.9678 turn=0.7622 turnL=0.8276 turnT=0.5976 theta=0.5062 score=1.1135

&#x20; epoch 065 | train=0.0182 val=0.2419 main=0.9662 turn=0.7595 turnL=0.7893 turnT=0.6190 theta=0.4663 score=0.8703

&#x20; epoch 070 | train=0.0213 val=0.3491 main=0.9570 turn=0.7695 turnL=0.7893 turnT=0.6333 theta=0.4942 score=1.1851

&#x20; epoch 075 | train=0.0203 val=0.2878 main=0.9662 turn=0.7909 turnL=0.7797 turnT=0.6595 theta=0.4797 score=0.9266

&#x20; epoch 080 | train=0.0170 val=0.2712 main=0.9678 turn=0.7890 turnL=0.7663 turnT=0.6690 theta=0.3118 score=0.7390

&#x20; epoch 085 | train=0.0117 val=0.3204 main=0.9647 turn=0.7656 turnL=0.8276 turnT=0.6405 theta=0.3251 score=0.8566

&#x20; epoch 090 | train=0.0107 val=0.2857 main=0.9720 turn=0.8067 turnL=0.7950 turnT=0.6833 theta=0.3998 score=0.8110

&#x20; epoch 095 | train=0.0107 val=0.3137 main=0.9632 turn=0.7829 turnL=0.8161 turnT=0.6524 theta=0.5048 score=0.9422

&#x20; epoch 100 | train=0.0089 val=0.2639 main=0.9743 turn=0.7890 turnL=0.8276 turnT=0.6667 theta=0.2761 score=0.7414

&#x20; epoch 105 | train=0.0090 val=0.2975 main=0.9643 turn=0.8067 turnL=0.8084 turnT=0.6786 theta=0.3509 score=0.8045

&#x20; epoch 110 | train=0.0076 val=0.2633 main=0.9739 turn=0.8147 turnL=0.8065 turnT=0.6976 theta=0.2750 score=0.6940

&#x20; epoch 115 | train=0.0072 val=0.3156 main=0.9697 turn=0.7944 turnL=0.8142 turnT=0.6714 theta=0.2568 score=0.7848

&#x20; epoch 120 | train=0.0073 val=0.2712 main=0.9755 turn=0.8147 turnL=0.8142 turnT=0.7071 theta=0.2759 score=0.6790

&#x20; epoch 125 | train=0.0065 val=0.2870 main=0.9724 turn=0.8151 turnL=0.8180 turnT=0.6905 theta=0.2808 score=0.7638

&#x20; epoch 130 | train=0.0056 val=0.2789 main=0.9728 turn=0.8270 turnL=0.8142 turnT=0.7143 theta=0.2687 score=0.7227

&#x20; epoch 135 | train=0.0058 val=0.2871 main=0.9735 turn=0.8216 turnL=0.8103 turnT=0.6929 theta=0.2918 score=0.7142

&#x20; epoch 140 | train=0.0054 val=0.2616 main=0.9751 turn=0.8186 turnL=0.8142 turnT=0.7024 theta=0.2604 score=0.6990

&#x20; epoch 145 | train=0.0049 val=0.2821 main=0.9708 turn=0.8232 turnL=0.8046 turnT=0.6976 theta=0.3221 score=0.7898

&#x20; epoch 150 | train=0.0046 val=0.2934 main=0.9731 turn=0.8193 turnL=0.8161 turnT=0.6976 theta=0.2448 score=0.7383

&#x20; epoch 155 | train=0.0043 val=0.2787 main=0.9747 turn=0.8197 turnL=0.8199 turnT=0.7048 theta=0.2585 score=0.7079

&#x20; epoch 160 | train=0.0043 val=0.2759 main=0.9751 turn=0.8205 turnL=0.8103 turnT=0.7095 theta=0.2417 score=0.6941

&#x20; epoch 165 | train=0.0041 val=0.2702 main=0.9751 turn=0.8189 turnL=0.8142 turnT=0.7000 theta=0.2319 score=0.6705

&#x20; epoch 170 | train=0.0047 val=0.2743 main=0.9751 turn=0.8182 turnL=0.8161 turnT=0.7048 theta=0.2401 score=0.7033

&#x20; epoch 175 | train=0.0041 val=0.2760 main=0.9766 turn=0.8197 turnL=0.8218 turnT=0.7048 theta=0.2360 score=0.7031

&#x20; epoch 180 | train=0.0040 val=0.2842 main=0.9747 turn=0.8178 turnL=0.8161 turnT=0.6976 theta=0.2337 score=0.7241

\[ModernTCN] 训练完成

&#x20; checkpoint: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21\\modern\_tcn\_seed21.pt

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21\\modern\_tcn\_seed21\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed21\\ModernTCN\_train\_report.md

&#x20; test main=0.9807, turnT=0.7757, turnL=0.8743, theta=0.2519, flat=0.9657, slope=0.9965



\[ModernTCN V2 multi-seed] seed 42 (3/5)

\[ModernTCN] 第一阶段训练开始

&#x20; seed=42, device=cuda, out=E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed42

&#x20; dataset=E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; train/val/test=18302/2607/3733

&#x20; model channels=64, blocks=5, kernel=31

&#x20; epoch 001 | train=0.7401 val=0.4257 main=0.8631 turn=0.6437 turnL=0.6724 turnT=0.3476 theta=2.7497 score=6.9382

&#x20; epoch 005 | train=0.1768 val=0.2987 main=0.9421 turn=0.6816 turnL=0.6935 turnT=0.4357 theta=1.5181 score=3.7722

&#x20; epoch 010 | train=0.1058 val=0.2607 main=0.9605 turn=0.6632 turnL=0.7548 turnT=0.4595 theta=1.3360 score=3.1514

&#x20; epoch 015 | train=0.0844 val=0.3192 main=0.9536 turn=0.6977 turnL=0.7261 turnT=0.4690 theta=1.3193 score=2.8644

&#x20; epoch 020 | train=0.0688 val=0.2291 main=0.9540 turn=0.7307 turnL=0.7203 turnT=0.5262 theta=0.8539 score=2.1020

&#x20; epoch 025 | train=0.0598 val=0.2264 main=0.9666 turn=0.7453 turnL=0.6724 turnT=0.5500 theta=0.9254 score=1.7778

&#x20; epoch 030 | train=0.0514 val=0.2771 main=0.9616 turn=0.7353 turnL=0.6954 turnT=0.5429 theta=2.3160 score=4.0994

&#x20; epoch 035 | train=0.0414 val=0.2221 main=0.9639 turn=0.7476 turnL=0.6954 turnT=0.5357 theta=0.7175 score=1.4717

&#x20; epoch 040 | train=0.0466 val=0.2928 main=0.9609 turn=0.7514 turnL=0.7759 turnT=0.5452 theta=0.6470 score=1.2620

&#x20; epoch 045 | train=0.0305 val=0.3251 main=0.9582 turn=0.7840 turnL=0.7605 turnT=0.5881 theta=0.4440 score=1.0543

&#x20; epoch 050 | train=0.0380 val=0.4444 main=0.9551 turn=0.7737 turnL=0.7816 turnT=0.5929 theta=0.4286 score=1.1905

&#x20; epoch 055 | train=0.0284 val=0.2850 main=0.9601 turn=0.7871 turnL=0.7663 turnT=0.5952 theta=0.5861 score=1.2618

&#x20; epoch 060 | train=0.0244 val=0.2705 main=0.9666 turn=0.7994 turnL=0.7931 turnT=0.5976 theta=0.3639 score=0.8754

&#x20; epoch 065 | train=0.0243 val=0.2839 main=0.9712 turn=0.7833 turnL=0.7510 turnT=0.6310 theta=0.4188 score=0.8430

&#x20; epoch 070 | train=0.0181 val=0.3325 main=0.9720 turn=0.7894 turnL=0.7625 turnT=0.6024 theta=0.3419 score=0.9264

&#x20; epoch 075 | train=0.0177 val=0.3888 main=0.9586 turn=0.7979 turnL=0.7682 turnT=0.6405 theta=0.5471 score=1.2568

&#x20; epoch 080 | train=0.0147 val=0.3369 main=0.9655 turn=0.7975 turnL=0.7682 turnT=0.6310 theta=0.5886 score=1.1513

&#x20; epoch 085 | train=0.0151 val=0.3097 main=0.9601 turn=0.8059 turnL=0.8065 turnT=0.6310 theta=0.2903 score=0.9099

&#x20; epoch 090 | train=0.0129 val=0.3637 main=0.9616 turn=0.8274 turnL=0.7989 turnT=0.6405 theta=0.3783 score=0.9357

&#x20; epoch 095 | train=0.0114 val=0.3001 main=0.9655 turn=0.8051 turnL=0.7797 turnT=0.6262 theta=0.2988 score=0.8329

&#x20; epoch 100 | train=0.0119 val=0.3400 main=0.9639 turn=0.8120 turnL=0.7912 turnT=0.6214 theta=0.3204 score=0.8829

\[ModernTCN] 早停：epoch=103, best\_epoch=68

\[ModernTCN] 训练完成

&#x20; checkpoint: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed42\\modern\_tcn\_seed42.pt

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed42\\modern\_tcn\_seed42\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed42\\ModernTCN\_train\_report.md

&#x20; test main=0.9788, turnT=0.7121, turnL=0.8689, theta=0.3428, flat=0.9683, slope=0.9930

&#x20; seed42 gate pass=0

&#x20;   - acc\_turn\_transition >= 0.7500 未满足，实际 0.7121



\[ModernTCN V2 multi-seed] seed 73 (4/5)

\[ModernTCN] 第一阶段训练开始

&#x20; seed=73, device=cuda, out=E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed73

&#x20; dataset=E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; train/val/test=18302/2607/3733

&#x20; model channels=64, blocks=5, kernel=31

&#x20; epoch 001 | train=0.7052 val=0.4868 main=0.8247 turn=0.6022 turnL=0.6935 turnT=0.3381 theta=2.8967 score=6.6692

&#x20; epoch 005 | train=0.1673 val=0.2562 main=0.9440 turn=0.6709 turnL=0.7126 turnT=0.4333 theta=1.7658 score=3.7142

&#x20; epoch 010 | train=0.1092 val=0.2168 main=0.9647 turn=0.7058 turnL=0.6801 turnT=0.4810 theta=2.5824 score=4.4027

&#x20; epoch 015 | train=0.0907 val=0.2103 main=0.9697 turn=0.7173 turnL=0.6475 turnT=0.4976 theta=2.1485 score=3.7982

&#x20; epoch 020 | train=0.0689 val=0.2312 main=0.9636 turn=0.6977 turnL=0.8027 turnT=0.4667 theta=1.0826 score=2.1788

&#x20; epoch 025 | train=0.0608 val=0.2116 main=0.9636 turn=0.7484 turnL=0.6992 turnT=0.5357 theta=1.0311 score=2.3107

&#x20; epoch 030 | train=0.0587 val=0.2278 main=0.9590 turn=0.7257 turnL=0.7011 turnT=0.5262 theta=1.3565 score=2.5311

&#x20; epoch 035 | train=0.0451 val=0.2449 main=0.9670 turn=0.7587 turnL=0.7989 turnT=0.5548 theta=0.7214 score=1.5321

&#x20; epoch 040 | train=0.0396 val=0.2435 main=0.9678 turn=0.7369 turnL=0.8295 turnT=0.5595 theta=0.5139 score=1.0851

&#x20; epoch 045 | train=0.0406 val=0.2544 main=0.9662 turn=0.7503 turnL=0.7222 turnT=0.5905 theta=0.5243 score=1.1907

&#x20; epoch 050 | train=0.0340 val=0.2700 main=0.9590 turn=0.7679 turnL=0.7088 turnT=0.6095 theta=1.0626 score=1.5058

&#x20; epoch 055 | train=0.0238 val=0.3321 main=0.9567 turn=0.7622 turnL=0.7893 turnT=0.5738 theta=0.3792 score=1.0891

&#x20; epoch 060 | train=0.0274 val=0.2861 main=0.9685 turn=0.7802 turnL=0.7912 turnT=0.6000 theta=0.3553 score=0.9469

&#x20; epoch 065 | train=0.0243 val=0.2757 main=0.9609 turn=0.7909 turnL=0.7586 turnT=0.6119 theta=0.5099 score=1.0002

&#x20; epoch 070 | train=0.0193 val=0.3151 main=0.9574 turn=0.7863 turnL=0.7299 turnT=0.6548 theta=0.6564 score=1.1921

&#x20; epoch 075 | train=0.0154 val=0.3654 main=0.9547 turn=0.7886 turnL=0.8238 turnT=0.6143 theta=0.6102 score=1.0926

&#x20; epoch 080 | train=0.0171 val=0.3491 main=0.9639 turn=0.8074 turnL=0.8008 turnT=0.6357 theta=0.3534 score=0.9426

&#x20; epoch 085 | train=0.0129 val=0.3276 main=0.9601 turn=0.7979 turnL=0.8046 turnT=0.6333 theta=0.3263 score=0.8763

&#x20; epoch 090 | train=0.0113 val=0.3856 main=0.9540 turn=0.8078 turnL=0.8257 turnT=0.6619 theta=0.2976 score=1.0084

&#x20; epoch 095 | train=0.0115 val=0.3817 main=0.9567 turn=0.8078 turnL=0.7912 turnT=0.6595 theta=0.2776 score=0.9383

&#x20; epoch 100 | train=0.0137 val=0.3283 main=0.9620 turn=0.8289 turnL=0.7950 turnT=0.6810 theta=0.3298 score=0.8489

\[ModernTCN] 早停：epoch=103, best\_epoch=68

\[ModernTCN] 训练完成

&#x20; checkpoint: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed73\\modern\_tcn\_seed73.pt

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed73\\modern\_tcn\_seed73\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed73\\ModernTCN\_train\_report.md

&#x20; test main=0.9796, turnT=0.7178, turnL=0.8934, theta=0.3281, flat=0.9630, slope=0.9969



\[ModernTCN V2 multi-seed] seed 101 (5/5)

\[ModernTCN] 第一阶段训练开始

&#x20; seed=101, device=cuda, out=E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed101

&#x20; dataset=E:\\Matlab\\Simulink\\S-Function\_16\\data\\tcn\\ModernTCN\_dataset\_agv\_dualsteer\_theta10\_uniform\_conf\_h0\_v2.mat

&#x20; train/val/test=18302/2607/3733

&#x20; model channels=64, blocks=5, kernel=31

&#x20; epoch 001 | train=0.7348 val=0.4772 main=0.8527 turn=0.6030 turnL=0.6916 turnT=0.3571 theta=3.1988 score=7.1835

&#x20; epoch 005 | train=0.1790 val=0.2488 main=0.9317 turn=0.6816 turnL=0.6130 turnT=0.4333 theta=1.6048 score=3.9213

&#x20; epoch 010 | train=0.1063 val=0.2566 main=0.9448 turn=0.6782 turnL=0.6992 turnT=0.4714 theta=1.1745 score=2.8403

&#x20; epoch 015 | train=0.0804 val=0.2135 main=0.9689 turn=0.6878 turnL=0.8008 turnT=0.4714 theta=1.3352 score=2.8386

&#x20; epoch 020 | train=0.0711 val=0.2068 main=0.9662 turn=0.7407 turnL=0.6552 turnT=0.5500 theta=0.8682 score=2.0076

&#x20; epoch 025 | train=0.0570 val=0.1761 main=0.9662 turn=0.7269 turnL=0.6877 turnT=0.5405 theta=0.7721 score=1.4237

&#x20; epoch 030 | train=0.0560 val=0.2120 main=0.9616 turn=0.7307 turnL=0.6935 turnT=0.5619 theta=1.0061 score=1.7934

&#x20; epoch 035 | train=0.0468 val=0.2285 main=0.9632 turn=0.7465 turnL=0.6973 turnT=0.5857 theta=0.6273 score=1.2424

&#x20; epoch 040 | train=0.0357 val=0.2492 main=0.9662 turn=0.7495 turnL=0.6973 turnT=0.5905 theta=0.4666 score=1.0351

&#x20; epoch 045 | train=0.0362 val=0.2497 main=0.9643 turn=0.7622 turnL=0.7337 turnT=0.5929 theta=0.5283 score=1.2772

&#x20; epoch 050 | train=0.0281 val=0.2889 main=0.9551 turn=0.7817 turnL=0.7203 turnT=0.6024 theta=0.6281 score=1.2018

&#x20; epoch 055 | train=0.0293 val=0.2749 main=0.9689 turn=0.7656 turnL=0.7567 turnT=0.6000 theta=0.4581 score=0.9583

&#x20; epoch 060 | train=0.0198 val=0.2211 main=0.9693 turn=0.7794 turnL=0.7835 turnT=0.6214 theta=0.3466 score=0.7955

&#x20; epoch 065 | train=0.0216 val=0.2113 main=0.9735 turn=0.7906 turnL=0.7854 turnT=0.6357 theta=0.4203 score=0.7974

&#x20; epoch 070 | train=0.0189 val=0.2896 main=0.9628 turn=0.7944 turnL=0.7893 turnT=0.6405 theta=0.5604 score=1.0258

&#x20; epoch 075 | train=0.0190 val=0.2507 main=0.9678 turn=0.7921 turnL=0.7854 turnT=0.6357 theta=0.5503 score=1.2258

&#x20; epoch 080 | train=0.0145 val=0.2896 main=0.9586 turn=0.7959 turnL=0.8123 turnT=0.6143 theta=0.3274 score=0.9015

&#x20; epoch 085 | train=0.0155 val=0.2828 main=0.9628 turn=0.8174 turnL=0.7893 turnT=0.6810 theta=0.5395 score=0.9529

&#x20; epoch 090 | train=0.0122 val=0.2580 main=0.9670 turn=0.8040 turnL=0.8084 turnT=0.6357 theta=0.2940 score=0.8054

&#x20; epoch 095 | train=0.0126 val=0.2695 main=0.9655 turn=0.8170 turnL=0.7989 turnT=0.6595 theta=0.3500 score=0.7821

&#x20; epoch 100 | train=0.0089 val=0.2888 main=0.9620 turn=0.8170 turnL=0.8199 turnT=0.6405 theta=0.4292 score=0.9169

&#x20; epoch 105 | train=0.0095 val=0.2607 main=0.9689 turn=0.8159 turnL=0.7931 turnT=0.6738 theta=0.3054 score=0.8429

&#x20; epoch 110 | train=0.0098 val=0.2746 main=0.9647 turn=0.8239 turnL=0.8084 turnT=0.6452 theta=0.3104 score=0.7521

&#x20; epoch 115 | train=0.0086 val=0.3365 main=0.9643 turn=0.8166 turnL=0.8084 turnT=0.6667 theta=0.3019 score=0.7940

&#x20; epoch 120 | train=0.0081 val=0.3025 main=0.9662 turn=0.8140 turnL=0.7893 turnT=0.6643 theta=0.2581 score=0.8008

&#x20; epoch 125 | train=0.0063 val=0.3105 main=0.9682 turn=0.8220 turnL=0.8123 turnT=0.6643 theta=0.3717 score=0.8547

&#x20; epoch 130 | train=0.0057 val=0.2972 main=0.9678 turn=0.8282 turnL=0.8084 turnT=0.6595 theta=0.3737 score=0.8246

&#x20; epoch 135 | train=0.0061 val=0.2983 main=0.9651 turn=0.8270 turnL=0.8084 turnT=0.6738 theta=0.2865 score=0.7556

&#x20; epoch 140 | train=0.0053 val=0.3108 main=0.9639 turn=0.8262 turnL=0.8276 turnT=0.6833 theta=0.3515 score=0.8483

\[ModernTCN] 早停：epoch=143, best\_epoch=108

\[ModernTCN] 训练完成

&#x20; checkpoint: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed101\\modern\_tcn\_seed101.pt

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed101\\modern\_tcn\_seed101\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_seed101\\ModernTCN\_train\_report.md

&#x20; test main=0.9743, turnT=0.7495, turnL=0.9003, theta=0.2820, flat=0.9577, slope=0.9920



\[ModernTCN V2 multi-seed] all seeds finished

&#x20; summary: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_multiseed\_summary.csv

&#x20; report: E:\\Matlab\\Simulink\\S-Function\_16\\results\\modern\_tcn\\modern\_tcn\_theta10\_uniform\_h0\_v2\_multiseed\_report.md

