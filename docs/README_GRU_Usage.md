# GRU 宸ュ喌璇嗗埆绠楁硶浣跨敤鎸囧崡

> **鐗堟湰**: V1.0  
> **鏈€鍚庢洿鏂?*: 2025-01-XX  
> **浣滆€?*: LPV-MPC Project

鏈枃妗ｈ缁嗚鏄?GRU 宸ュ喌璇嗗埆绠楁硶浠庢暟鎹敓鎴愬埌鍦ㄧ嚎鎺ㄧ悊鐨勫畬鏁存祦绋嬶紝浠ュ強鍚勯樁娈靛叧閿弬鏁扮殑璋冩暣绛栫暐銆?
---

## 馃搵 鐩綍

1. [绠楁硶姒傝堪](#绠楁硶姒傝堪)
2. [瀹屾暣宸ヤ綔娴佺▼](#瀹屾暣宸ヤ綔娴佺▼)
3. [闃舵涓€锛氭暟鎹敓鎴怾(#闃舵涓€鏁版嵁鐢熸垚)
4. [闃舵浜岋細鏁版嵁棰勫鐞哴(#闃舵浜屾暟鎹澶勭悊)
5. [闃舵涓夛細妯″瀷璁粌](#闃舵涓夋ā鍨嬭缁?
6. [闃舵鍥涳細妯″瀷鎺ㄧ悊](#闃舵鍥涙ā鍨嬫帹鐞?
7. [闃舵浜旓細娴嬭瘯楠岃瘉](#闃舵浜旀祴璇曢獙璇?
8. [鍏抽敭鍙傛暟褰卞搷鍒嗘瀽](#鍏抽敭鍙傛暟褰卞搷鍒嗘瀽)
9. [甯歌闂涓庤В鍐虫柟妗圿(#甯歌闂涓庤В鍐虫柟妗?
10. [蹇€熷弬鑰僝(#蹇€熷弬鑰?

---

## 绠楁硶姒傝堪

GRU 宸ュ喌璇嗗埆绠楁硶鐢ㄤ簬璇嗗埆 AGV 鐨勮椹跺伐鍐碉紝鍖呮嫭锛?
- **涓诲垎绫?*锛?绫伙級锛歠lat锛堝钩鍦帮級銆乻lip锛堟墦婊戯級銆乻tall锛堝牭杞級銆乻lope锛堝潯搴︼級
- **杞集鐘舵€?*锛?绫伙級锛歭eft锛堝乏杞級銆乻traight锛堢洿琛岋級銆乺ight锛堝彸杞級
- **鍧″害鍥炲綊**锛氫及璁″潯搴﹁ 胃虃 [rad]

绠楁硶閲囩敤**澶氫换鍔″涔?*鏋舵瀯锛岄€氳繃涓€涓?GRU 缃戠粶鍚屾椂瀹屾垚涓変釜浠诲姟锛屾彁楂樿绠楁晥鐜囥€?
---

## 瀹屾暣宸ヤ綔娴佺▼

### 娴佺▼鍥?
```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 闃舵涓€锛氭暟鎹敓鎴?(GRU_gen_train_data.m)                    鈹?鈹? 鈹斺攢> GRU_train_data_full.mat                                鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 闃舵浜岋細鏁版嵁棰勫鐞?(GRU_prepare_dataset.m)                 鈹?鈹? 鈹斺攢> GRU_dataset_processed.mat + GRU_scaler.mat            鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 闃舵涓夛細妯″瀷璁粌 (GRU_train.m)                              鈹?鈹? 鈹斺攢> GRU_model.mat + GRU_meta.mat + GRU_logs/             鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 闃舵鍥涳細鍦ㄧ嚎鎺ㄧ悊                                            鈹?鈹? 鈹溾攢 GRU_infer.m (鍗曟鎺ㄧ悊)                                  鈹?鈹? 鈹斺攢 GRU_state_classifier.m (鍦ㄧ嚎灏佽)                       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                          鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 闃舵浜旓細娴嬭瘯楠岃瘉 (test_GRU_workflow.m)                      鈹?鈹? 鈹斺攢> 娴嬭瘯鎶ュ憡鍜屽彲瑙嗗寲                                        鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

### 鍏稿瀷宸ヤ綔娴?
#### 棣栨璁粌
1. 杩愯 `GRU_gen_train_data.m` 鈫?鐢熸垚鍘熷鏁版嵁
2. 杩愯 `GRU_prepare_dataset.m` 鈫?棰勫鐞嗘暟鎹?3. 杩愯 `GRU_train.m` 鈫?璁粌妯″瀷
4. 杩愯 `test_GRU_workflow.m` 鈫?楠岃瘉妯″瀷

#### 鍦ㄧ嚎閮ㄧ讲
1. 鍦?Simulink 涓姞杞?`GRU_model.mat` 鍜?`parameters.m`
2. `GRU_State_Classifier` 妯″潡璋冪敤 `GRU_state_classifier.m`
3. 妯″潡鍐呴儴璋冪敤 `GRU_infer.m` 杩涜鎺ㄧ悊

---

## 闃舵涓€锛氭暟鎹敓鎴?
### 鎵ц鑴氭湰
**`GRU_gen_train_data.m`**

### 鍔熻兘璇存槑
- 閫氳繃璋冪敤 Simulink 妯″瀷 `GRU_DataGen.slx` 鐢熸垚楂樹繚鐪熻缁冩暟鎹?- 鏀寔璺緞鍙傛暟闅忔満鍖栵紙鍩熼殢鏈哄寲锛?- 鏀寔鎵撴粦/鍫佃浆娉ㄥ叆锛堥€氳繃 InjectionWrapper锛?- 鑷姩鏍囨敞锛坙abel_main, label_turn, theta锛?
### 渚濊禆鏂囦欢
- `parameters.m`锛堢郴缁熷弬鏁帮級
- `gen_agv_ref_path.m`锛堝弬鑰冭矾寰勭敓鎴愶級
- `GRU_DataGen.slx`锛圫imulink 浠跨湡妯″瀷锛?
### 鐢熸垚鏂囦欢
**`GRU_train_data_full.mat`**
```
data
鈹溾攢鈹€ runs(k): 姣忓洖鍚堟暟鎹?鈹?  鈹溾攢鈹€ .t [N脳1]: 鏃堕棿鍚戦噺 [s]
鈹?  鈹溾攢鈹€ .u [N脳2]: 鎺у埗杈撳叆 [F_cmd, omega_cmd]
鈹?  鈹溾攢鈹€ .y_raw [N脳31]: 鍘熷杈撳嚭锛堝惈浼犳劅鍣ㄦ暟鎹級
鈹?  鈹溾攢鈹€ .label_main [N脳1]: 涓诲垎绫?{1,2,3,4}
鈹?  鈹溾攢鈹€ .label_turn [N脳1]: 杞集鐘舵€?{-1,0,+1}
鈹?  鈹溾攢鈹€ .theta [N脳1]: 鍧″害瑙掔湡鍊?[rad]
鈹?  鈹斺攢鈹€ .meta: 鍏冩暟鎹紙鍙傛暟銆佺瀛愩€佹敞鍏ョ獥鍙ｏ級
鈹斺攢鈹€ .meta: 鍏ㄥ眬鍏冩暟鎹?```

### 鍏抽敭鍙傛暟

#### 鏁版嵁瑙勬ā鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.num_runs` | 150 | 姣忓満鏅洖鍚堟暟 | 澧炲ぇ鈫掓暟鎹噺鈫戯紝璁粌鏇村厖鍒嗭紝浣嗙敓鎴愭椂闂粹啈 |
| `cfg.T_end` | 20 s | 姣忓洖鍚堜豢鐪熸椂闀?| 澧炲ぇ鈫掑崟鍥炲悎鏍锋湰鈫戯紝瑕嗙洊鏇撮暱鏃跺簭 |
| `cfg.Ts` | 0.05 s | 閲囨牱鍛ㄦ湡 | 闇€涓庣郴缁熷弬鏁颁竴鑷?|

#### 鍦烘櫙閰嶇疆
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.scenes` | `{'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'}` | 鍦烘櫙鍒楄〃 | 瑕嗙洊涓嶅叏鈫掓ā鍨嬫棤娉曡瘑鍒湭璁粌鍦烘櫙 |

#### 鍩熼殢鏈哄寲鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.path_rand.v0_range` | [0.8, 1.2] m/s | 鍒濋€熷害鑼冨洿 | 鑼冨洿澶р啋娉涘寲鏇村ソ锛屼絾鍙兘寮曞叆寮傚父鏍锋湰 |
| `cfg.path_rand.R_range` | [8, 12] m | 杞集鍗婂緞鑼冨洿 | 褰卞搷杞集鍦烘櫙澶氭牱鎬?|
| `cfg.path_rand.theta_slope_range` | [-10, 10] deg | 鍧″害瑙掕寖鍥?| 鑼冨洿澶р啋瑕嗙洊鏇村箍鍧″害 |

#### 鎵撴粦娉ㄥ叆鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.slip_cfg.prob` | 0.70 | 鎵撴粦姒傜巼 | 澧炲ぇ鈫抯lip鏍锋湰鈫戯紝浣嗗彲鑳借繃搴?|
| `cfg.slip_cfg.gamma_range` | [0.3, 0.7] | 鐗靛紩绯绘暟鑼冨洿 | 鑼冨洿澶р啋鎵撴粦寮哄害鍙樺寲澶?|
| `cfg.slip_cfg.duration_range` | [2, 4] s | 鎸佺画鏃堕棿鑼冨洿 | 褰卞搷鎵撴粦浜嬩欢鐨勬椂搴忕壒寰?|

#### 鍫佃浆娉ㄥ叆鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.stall_cfg.prob` | 0.40 | 鍫佃浆姒傜巼 | 澧炲ぇ鈫抯tall鏍锋湰鈫?|
| `cfg.stall_cfg.load_range` | [200, 300] N | 澶栭儴璐熻浇鑼冨洿 | 褰卞搷鍫佃浆寮哄害 |

### 浣跨敤绀轰緥
```matlab
% 淇敼閰嶇疆鍖哄煙
cfg.num_runs = 150;          % 姣忓満鏅?50娆?cfg.scenes = {'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'};
cfg.slip_cfg.prob = 0.70;   % 鎵撴粦姒傜巼
cfg.stall_cfg.prob = 0.40;  % 鍫佃浆姒傜巼

% 杩愯鑴氭湰
GRU_gen_train_data;
```

---

### 鎵ц鑴氭湰
- **`test_GRU_workflow.m`**锛氬揩閫?sanity check锛屽鐢ㄦ棫娴佺▼銆?- **`test_gru_performance.m`**锛氱绾?鍦ㄧ嚎鎸囨爣涓€浣撳寲鑴氭湰锛岃褰曟贩娣嗙煩闃点€佄柑?MAE銆佸潯搴﹁瘑鍒欢杩熴€乺un 绾у埆鍑嗙‘鐜囩瓑锛岀粨鏋滀繚瀛樺埌 `GRU_logs/eval_reports/`銆?- **`test_closed_loop_performance.m`**锛氭壒閲?Simulink 浠跨湡锛岀粺璁￠€熷害璺熻釜銆佸Э鎬佽宸€丗_cmd 楗卞拰姣斾緥鍙?slope 寤惰繜锛岀粨鏋滀繚瀛樺埌 `GRU_logs/closed_loop_eval/`銆?
### 鍔熻兘璇存槑
1. **test_GRU_workflow**锛氭鏌ヤ緷璧?鈫?杩愯鍗曟/鍦ㄧ嚎鎺ㄧ悊 鈫?杈撳嚭绀烘剰鍥撅紝閫傚悎 smoke test銆?2. **test_gru_performance**锛?   - 鍔犺浇鏁版嵁闆嗗垏鍒嗭紙Train/Val/Test锛夊苟杩愯 GRU_infer锛岃緭鍑哄噯纭巼銆佺簿纭巼/鍙洖鐜囥€佹贩娣嗙煩闃点€佸潯搴?MAE銆?   - 鎸?run 鏁版嵁锛坄GRU_train_data_full.mat`锛夎繘琛岀湡瀹炲湪绾挎帹鐞嗭紝璇勪及椹荤暀鍚庣殑鍒嗙被鐜囥€佸潯搴﹀欢杩燂紝骞惰嚜鍔ㄧ粯鍥俱€?   - 缁熶竴淇濆瓨 `split_<name>_metrics.mat`銆乣online_eval_<scene>.png` 鍙?`GRU_eval_summary_<timestamp>.mat`銆?3. **test_closed_loop_performance**锛?   - 鑷姩鍔犺浇 `path_*.mat` 鍙傝€冭建杩瑰苟鎺ㄩ€佽嚦鍩虹宸ヤ綔鍖猴紝璋冪敤 `LPVMPC_AGV_simulink` 鎵归噺浠跨湡銆?   - 榛樿鐩戞帶淇″彿 `diag.*`锛堥€熷害銆佸Э鎬併€乼heta_hat銆乴abel_main銆丗_cmd 绛夛級锛岃绠?RMS/宄板€艰宸€乻teady-state 璇樊銆佸潯搴﹁瘑鍒欢杩熶笌鍛戒护楗卞拰姣斾緥銆?   - 鏀寔閫氳繃 `cfg.scenarios` 浼犲叆鑷畾涔夎矾寰勬垨缁撴瀯浣擄紙鍚?`path_file`, `name`, `stop_time`锛夛紝杈撳嚭 `timeseries_<scene>.mat` 涓?`closed_loop_summary_<tag>.mat`銆?
### 渚濊禆鏂囦欢
- `GRU_model.mat`
- `GRU_dataset_processed.mat`
- `GRU_train_data_full.mat`
- `GRU_infer.m`
- `GRU_state_classifier.m`
- `LPVMPC_AGV_simulink._GRU.slx` 鍙婂叾 `diag.*` 鏃ュ織淇″彿
- `parameters.m`

### 鐢熸垚鏂囦欢
- `GRU_logs/test_online_inference.png`
- `GRU_logs/eval_reports/split_<name>_metrics.mat`
- `GRU_logs/eval_reports/online_eval_<scene>.png`
- `GRU_logs/eval_reports/GRU_eval_summary_<timestamp>.mat`
- `GRU_logs/closed_loop_eval/timeseries_<scene>.mat`
- `GRU_logs/closed_loop_eval/closed_loop_summary_<tag>.mat`

### 浣跨敤绀轰緥
```matlab
% 鍩虹宸ヤ綔娴侊紙蹇€熸鏌ワ級
鈹溾攢鈹€ .mask_theta_train/val/test [N脳1]: slope鏍锋湰鎺╃爜

% GRU 鎬ц兘璇勪及锛堟寚瀹?run 绱㈠紩銆佸叧闂粯鍥撅級
鈹溾攢鈹€ .scaler: 褰掍竴鍖栫粺璁￠噺锛坢ean, std锛?鈹溾攢鈹€ .feat_names: 鐗瑰緛鍚嶇О鍒楄〃

% 闂幆璇勪及锛堜粎骞宠矾+鍧″害锛屼豢鐪?25 s锛?鈹斺攢鈹€ .meta: 鍏冩暟鎹?```
```

**`GRU_scaler.mat`**
```
scaler
鈹溾攢鈹€ .mean [1脳feat_dim]: 鍧囧€?鈹溾攢鈹€ .std [1脳feat_dim]: 鏍囧噯宸?鈹溾攢鈹€ .tau_diff: 閫熷害宸垎婊ゆ尝鍙傛暟
鈹斺攢鈹€ .tau_accel_lp: 鍔犻€熷害浣庨€氭护娉㈠弬鏁?```

### 鍏抽敭鍙傛暟

#### 搴忓垪鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.seq_len` | 48 | 搴忓垪闀垮害锛堚増2.4s锛?| 澧炲ぇ鈫掓崟鑾锋洿闀夸緷璧栵紝浣嗚绠楅噺鈫?|
| `cfg.stride` | 12 | 婊戠獥姝ラ暱锛堚増0.6s闂撮殧锛?| 澧炲ぇ鈫掓牱鏈暟鈫擄紝閲嶅彔灏?|

#### 鏁版嵁鍒嗗壊
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.train_ratio` | 0.7 | 璁粌闆嗘瘮渚?| 澧炲ぇ鈫掕缁冩暟鎹啈锛屼絾楠岃瘉/娴嬭瘯鏁版嵁鈫?|
| `cfg.val_ratio` | 0.15 | 楠岃瘉闆嗘瘮渚?| 鐢ㄤ簬鏃╁仠鍜岃秴鍙傝皟浼?|
| `cfg.test_ratio` | 0.15 | 娴嬭瘯闆嗘瘮渚?| 鐢ㄤ簬鏈€缁堣瘎浼?|

#### 鐗瑰緛婊ゆ尝鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.tau_accel_lp` | 0.4 s | 鍔犻€熷害浣庨€氭护娉㈡椂闂村父鏁?| 澧炲ぇ鈫掑钩婊戞洿寮猴紝浣嗗彲鑳戒涪澶卞揩閫熷彉鍖?|
| `cfg.tau_diff` | 0.3 s | 閫熷害宸垎婊ゆ尝鏃堕棿甯告暟 | 褰卞搷dv_hat_dt鐨勫钩婊戝害 |

### 浣跨敤绀轰緥
```matlab
% 淇敼閰嶇疆鍖哄煙
cfg.seq_len = 48;           % 搴忓垪闀垮害
cfg.stride = 12;             % 婊戠獥姝ラ暱
cfg.train_ratio = 0.7;       % 璁粌闆嗘瘮渚?cfg.tau_accel_lp = 0.4;      % 鍔犻€熷害婊ゆ尝鏃堕棿甯告暟

% 杩愯鑴氭湰
GRU_prepare_dataset;
```

---

## 闃舵涓夛細妯″瀷璁粌

### 鎵ц鑴氭湰
**`GRU_train.m`**

### 鍔熻兘璇存槑
1. 鍔犺浇棰勫鐞嗘暟鎹泦锛坄GRU_dataset_processed.mat`锛?2. 鏋勫缓涓夊ご GRU 缃戠粶
   - GRU 鐗瑰緛鎻愬彇灞傦紙2灞傦紝hidden=96, dropout=0.2锛?   - 涓诲垎绫诲ご锛圖ense(4) + softmax锛?   - 杞集鍒嗙被澶达紙Dense(3) + softmax锛?   - 鍧″害鍥炲綊澶达紙Dense(1)锛?3. 鑷畾涔夎缁冨惊鐜?   - 娣峰悎鎹熷け锛歀 = CE_main(鍔犳潈) + 位_turn路CE_turn + 位_theta路MSE_theta路mask_theta
   - 绫诲埆鏉冮噸骞宠　锛堟寜绫婚娆″弽姣旓級
   - 姊害瑁佸壀锛堥槇鍊?5.0锛?   - 瀛︿範鐜囪皟搴︼紙cosine/step锛?   - 鏃╁仠锛坧atience=20锛?4. 淇濆瓨妯″瀷鍜屽厓鏁版嵁

### 渚濊禆鏂囦欢
- `GRU_dataset_processed.mat`锛堥樁娈典簩浜х墿锛?- Deep Learning Toolbox锛圡ATLAB R2024b+锛?
### 鐢熸垚鏂囦欢
**`GRU_model.mat`**
```
model
鈹溾攢鈹€ .net_feature: GRU鐗瑰緛鎻愬彇缃戠粶锛坉lnetwork锛?鈹溾攢鈹€ .fc_main_weights/bias: 涓诲垎绫诲ご鏉冮噸/鍋忕疆
鈹溾攢鈹€ .fc_turn_weights/bias: 杞集鍒嗙被澶存潈閲?鍋忕疆
鈹溾攢鈹€ .fc_theta_weights/bias: 鍧″害鍥炲綊澶存潈閲?鍋忕疆
鈹溾攢鈹€ .scaler: 褰掍竴鍖栧弬鏁帮紙浠巇ataset澶嶅埗锛?鈹溾攢鈹€ .class_labels_main: 涓诲垎绫绘爣绛惧悕绉?鈹溾攢鈹€ .class_labels_turn: 杞集鏍囩鍚嶇О
鈹斺攢鈹€ .seq_len: 搴忓垪闀垮害
```

**`GRU_meta.mat`**
```
meta
鈹溾攢鈹€ .hyperparams: 瓒呭弬鏁伴厤缃?鈹溾攢鈹€ .train_history: 璁粌鍘嗗彶锛坙oss, acc绛夛級
鈹溾攢鈹€ .best_epoch: 鏈€浣宠疆娆?鈹斺攢鈹€ .metrics: 璇勪及鎸囨爣
```

**`GRU_logs/`**锛堢洰褰曪級
- `training_curves.png`: 璁粌鏇茬嚎鍥?- 鍏朵粬鏃ュ織鏂囦欢

### 鍏抽敭鍙傛暟

#### 妯″瀷鏋舵瀯鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.hidden_size` | 96 | GRU闅愯棌灞傚ぇ灏?| 澧炲ぇ鈫掑閲忊啈锛屼絾鍙兘杩囨嫙鍚堬紝璁＄畻閲忊啈 |
| `cfg.num_layers` | 2 | GRU灞傛暟 | 澧炲ぇ鈫掕〃杈捐兘鍔涒啈锛屼絾璁粌闅俱€佹槗杩囨嫙鍚?|
| `cfg.dropout` | 0.2 | Dropout姒傜巼 | 澧炲ぇ鈫掓鍒欏寲鈫戯紝浣嗗彲鑳芥瑺鎷熷悎 |

#### 璁粌瓒呭弬鏁?| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.batch_size` | 64 | 鎵归噺澶у皬 | 澧炲ぇ鈫掕缁冪ǔ瀹氾紝浣嗗唴瀛樺崰鐢ㄢ啈锛屽彲鑳芥硾鍖栧樊 |
| `cfg.max_epochs` | 150 | 鏈€澶ц缁冭疆鏁?| 澧炲ぇ鈫掕缁冨厖鍒嗭紝浣嗗彲鑳借繃鎷熷悎 |
| `cfg.initial_lr` | 1e-3 | 鍒濆瀛︿範鐜?| 杩囧ぇ鈫掕缁冧笉绋冲畾锛涜繃灏忊啋鏀舵暃鎱?|
| `cfg.lr_schedule` | 'cosine' | 瀛︿範鐜囪皟搴︾瓥鐣?| 'cosine'鈫掑钩婊戣“鍑忥紱'step'鈫掗樁姊“鍑?|

#### 鎹熷け鍑芥暟鏉冮噸
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.lambda_turn` | 0.3 | 杞集鍒嗙被鎹熷け鏉冮噸 | 澧炲ぇ鈫掓洿鍏虫敞杞集鍒嗙被锛屽彲鑳藉奖鍝嶄富鍒嗙被 |
| `cfg.lambda_theta` | 0.5 | 鍧″害鍥炲綊鎹熷け鏉冮噸 | 澧炲ぇ鈫掓洿鍏虫敞鍧″害鍥炲綊锛屽彲鑳藉奖鍝嶅垎绫?|

#### 姝ｅ垯鍖栧弬鏁?| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.grad_clip` | 5.0 | 姊害瑁佸壀闃堝€?| 澧炲ぇ鈫掑厑璁告洿澶ф搴︼紝鍙兘涓嶇ǔ瀹?|
| `cfg.patience` | 20 | 鏃╁仠鑰愬績鍊?| 澧炲ぇ鈫掑厑璁告洿澶氭棤鏀瑰杽杞锛屽彲鑳借繃鎷熷悎 |

#### 绫诲埆骞宠　鍙傛暟
| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `cfg.use_class_weights` | true | 鏄惁浣跨敤绫诲埆鏉冮噸 | 寮€鍚啋骞宠　绫诲埆锛屾彁鍗囧皯鏁扮被鎬ц兘 |
| `cfg.class_weight_method` | 'custom' | 绫诲埆鏉冮噸璁＄畻鏂规硶 | 涓嶅悓鏂规硶瀵圭被鍒钩琛℃晥鏋滀笉鍚?|

### 浣跨敤绀轰緥
```matlab
% 淇敼閰嶇疆鍖哄煙
cfg.hidden_size = 96;        % GRU闅愯棌灞傚ぇ灏?cfg.num_layers = 2;          % GRU灞傛暟
cfg.batch_size = 64;         % 鎵归噺澶у皬
cfg.max_epochs = 150;        % 鏈€澶ц缁冭疆鏁?cfg.initial_lr = 1e-3;       % 鍒濆瀛︿範鐜?cfg.lambda_turn = 0.3;      % 杞集鍒嗙被鎹熷け鏉冮噸
cfg.lambda_theta = 0.5;     % 鍧″害鍥炲綊鎹熷け鏉冮噸

% 杩愯鑴氭湰
GRU_train;
```

---

## 闃舵鍥涳細妯″瀷鎺ㄧ悊

### 4.1 鍗曟鎺ㄧ悊鎺ュ彛

#### 鎵ц鑴氭湰
**`GRU_infer.m`**

#### 鍔熻兘璇存槑
- 杈撳叆锛氬綊涓€鍖栧簭鍒?[seq_len, feat_dim]
- GRU 鍓嶅悜浼犳挱
- 涓夊ご杈撳嚭锛歭abel_main, label_turn, theta_hat
- 缃俊搴﹁緭鍑?
#### 渚濊禆鏂囦欢
- `GRU_model.mat`锛堥樁娈典笁浜х墿锛?
#### 浣跨敤绀轰緥
```matlab
load('GRU_model.mat', 'model');
x_seq = randn(48, 17);  % [seq_len, feat_dim]锛屽凡褰掍竴鍖?[label_main, label_turn, theta_hat, conf] = GRU_infer(x_seq, model);
```

---

### 4.2 鍦ㄧ嚎鎺ㄧ悊灏佽锛圫imulink闆嗘垚锛?
#### 鎵ц鑴氭湰
**`GRU_state_classifier.m`**

#### 鍔熻兘璇存槑
鎻愪緵搴忓垪缂撳啿銆佹渶灏忛┗鐣欐椂闂淬€佷綆閫氭护娉㈢瓑鍔熻兘锛岄€傜敤浜?Simulink 鍦ㄧ嚎鎺ㄧ悊銆?
**鍒濆鍖栨ā寮?*锛歚'init'`
- 鍒濆鍖栫姸鎬侊紙搴忓垪缂撳啿銆佹护娉㈠弬鏁扮瓑锛?
**鏇存柊妯″紡**锛歚'update'`
1. 鐗瑰緛鎻愬彇锛堜粠 y_raw [31脳1] 鎻愬彇 17 缁寸壒寰侊級
2. 搴忓垪缂撳啿锛團IFO锛岀淮鎶?seq_len 闀垮害锛?3. 褰掍竴鍖栵紙浣跨敤 model.scaler锛?4. 璋冪敤 GRU_infer 鎺ㄧ悊
5. 鏈€灏忛┗鐣欐椂闂村鐞嗭紙涓诲垎绫?0.20s锛岃浆寮?0.40s锛?6. theta_hat 浣庨€氭护娉紙tau=0.15s锛?7. 鏉′欢澶勭悊锛圴1.3 鏂板锛?   - 闈?slope 鍦烘櫙锛氬己鍒?theta_hat=0
   - slope 鍦烘櫙锛氭鍖哄鐞嗭紙闃堝€?0.02 rad锛?
#### 渚濊禆鏂囦欢
- `GRU_infer.m`锛堝崟姝ユ帹鐞嗘帴鍙ｏ級
- `GRU_model.mat`锛堥樁娈典笁浜х墿锛?- `parameters.m`

#### 鍏抽敭鍙傛暟

| 鍙傛暟 | 榛樿鍊?| 璇存槑 | 褰卞搷 |
|------|--------|------|------|
| `state.seq_len` | 48 | 搴忓垪闀垮害 | 闇€涓庤缁冩椂涓€鑷达紝鍚﹀垯鎬ц兘涓嬮檷 |
| `state.dwell_main` | 0.20 s | 涓诲垎绫婚┗鐣欐椂闂?| 澧炲ぇ鈫掓洿绋冲畾锛屼絾鍝嶅簲鎱?|
| `state.dwell_turn` | 0.40 s | 杞集鐘舵€侀┗鐣欐椂闂?| 澧炲ぇ鈫掓洿绋冲畾锛屼絾鍝嶅簲鎱?|
| `state.tau_theta` | 0.15 s | theta_hat 浣庨€氭护娉㈡椂闂村父鏁?| 澧炲ぇ鈫掓洿骞虫粦锛屼絾鍝嶅簲鎱?|
| `state.theta_deadzone` | 0.02 rad | theta_hat 姝诲尯闃堝€?| 澧炲ぇ鈫掓秷闄ゆ洿澶氬皬娉㈠姩锛屼絾鍙兘涓㈠け灏忓潯搴?|
| `state.tau_diff` | 0.3 s | 閫熷害宸垎婊ゆ尝 | 闇€涓庨澶勭悊涓€鑷?|
| `state.tau_accel_lp` | 0.4 s | 鍔犻€熷害浣庨€氭护娉?| 闇€涓庨澶勭悊涓€鑷?|

#### 浣跨敤绀轰緥
```matlab
% 鍒濆鍖?params = parameters();
load('GRU_model.mat', 'model');
state = GRU_state_classifier('init', params, model);

% 鍦ㄧ嚎寰幆
for t = 1:N
    y_raw_t = output_eq(x, u, theta, params);  % [31脳1]
    [state, out] = GRU_state_classifier('update', state, y_raw_t);
    fprintf('t=%.2f: %s, %s, 胃=%.2f掳\n', ...
        t*params.Ts, out.label_main_name, out.label_turn_name, rad2deg(out.theta_hat));
end
```

---

## 闃舵浜旓細娴嬭瘯楠岃瘉

### 鎵ц鑴氭湰
**`test_GRU_workflow.m`**

### 鍔熻兘璇存槑
1. 妫€鏌ヤ緷璧栨枃浠?2. 鍔犺浇妯″瀷鍜屾暟鎹泦
3. 娴嬭瘯鍗曟鎺ㄧ悊锛圙RU_infer锛?4. 娴嬭瘯鍦ㄧ嚎鎺ㄧ悊锛圙RU_state_classifier锛?5. 鍙鍖栫粨鏋?
### 渚濊禆鏂囦欢
- `GRU_model.mat`
- `GRU_dataset_processed.mat`
- `GRU_infer.m`
- `GRU_state_classifier.m`
- `parameters.m`

### 鐢熸垚鏂囦欢
- `GRU_logs/test_online_inference.png`锛堝彲瑙嗗寲缁撴灉锛?
### 浣跨敤绀轰緥
```matlab
% 鐩存帴杩愯
test_GRU_workflow;
```

---

## 鍏抽敭鍙傛暟褰卞搷鍒嗘瀽

### 鍙傛暟璋冩暣浼樺厛绾?
#### 鏁版嵁鐢熸垚闃舵
- **浼樺厛璋冩暣**锛歚num_runs`锛堟暟鎹噺锛夈€乣slip_cfg.prob`銆乣stall_cfg.prob`锛堢被鍒钩琛★級
- **娆¤璋冩暣**锛氬煙闅忔満鍖栬寖鍥达紙娉涘寲鑳藉姏锛?
#### 鏁版嵁棰勫鐞嗛樁娈?- **浼樺厛璋冩暣**锛歚seq_len`锛堟椂搴忓缓妯¤兘鍔涳級銆乣stride`锛堟牱鏈暟閲忥級
- **娆¤璋冩暣**锛氭护娉㈠弬鏁帮紙鐗瑰緛璐ㄩ噺锛?
#### 妯″瀷璁粌闃舵
- **浼樺厛璋冩暣**锛歚hidden_size`銆乣batch_size`銆乣initial_lr`锛堣缁冩晥鏋滐級
- **娆¤璋冩暣**锛氭崯澶辨潈閲嶃€佹棭鍋滃弬鏁帮紙澶氫换鍔″钩琛★級

#### 鍦ㄧ嚎鎺ㄧ悊闃舵
- **浼樺厛璋冩暣**锛氶┗鐣欐椂闂淬€佹护娉㈠弬鏁帮紙绋冲畾鎬т笌鍝嶅簲閫熷害锛?- **娆¤璋冩暣**锛氭鍖洪槇鍊硷紙娑堥櫎娉㈠姩锛?
### 鍙傛暟鑱斿姩鍏崇郴

1. **搴忓垪闀垮害涓€鑷存€?*锛氳缁冩椂鐨?`seq_len` 蹇呴』涓庡湪绾挎帹鐞嗘椂鐨?`state.seq_len` 涓€鑷?2. **婊ゆ尝鍙傛暟涓€鑷存€?*锛氶澶勭悊鏃剁殑 `tau_accel_lp`銆乣tau_diff` 蹇呴』涓庡湪绾挎帹鐞嗘椂涓€鑷?3. **褰掍竴鍖栦竴鑷存€?*锛氬湪绾挎帹鐞嗗繀椤讳娇鐢ㄨ缁冩椂鐨?`scaler` 杩涜褰掍竴鍖?
---

## 甯歌闂涓庤В鍐虫柟妗?
### 闂1锛氭ā鍨嬪湪 slip/stall 鍦烘櫙璇嗗埆鐜囦綆

**鍘熷洜**锛氬皯鏁扮被鏍锋湰涓嶈冻

**瑙ｅ喅鏂规**锛?- 澧炲ぇ `cfg.slip_cfg.prob`锛堝 0.5鈫?.7锛?- 澧炲ぇ `cfg.stall_cfg.prob`锛堝 0.2鈫?.4锛?- 澧炲ぇ `cfg.num_runs`锛堝 100鈫?50锛?- 浣跨敤绫诲埆鏉冮噸骞宠　锛坄cfg.use_class_weights = true`锛?
---

### 闂2锛氭ā鍨嬭繃鎷熷悎

**鍘熷洜**锛氭ā鍨嬪閲忚繃澶ф垨璁粌杞暟杩囧

**瑙ｅ喅鏂规**锛?- 澧炲ぇ `cfg.dropout`锛堝 0.2鈫?.3锛?- 鍑忓皬 `cfg.hidden_size`锛堝 96鈫?4锛?- 鍑忓皬 `cfg.num_layers`锛堝 2鈫?锛?- 澧炲ぇ `cfg.patience` 閰嶅悎鏃╁仠

---

### 闂3锛氬湪绾挎帹鐞嗘姈鍔?
**鍘熷洜**锛氶┗鐣欐椂闂磋繃鐭垨婊ゆ尝涓嶈冻

**瑙ｅ喅鏂规**锛?- 澧炲ぇ `state.dwell_main`锛堝 0.20鈫?.30s锛?- 澧炲ぇ `state.dwell_turn`锛堝 0.40鈫?.45s锛?- 澧炲ぇ `state.tau_theta`锛堝 0.15鈫?.20s锛?- 澧炲ぇ `state.theta_deadzone`锛堝 0.01鈫?.02 rad锛?
---

### 闂4锛氬搷搴旈€熷害鎱?
**鍘熷洜**锛氶┗鐣欐椂闂存垨婊ゆ尝鏃堕棿甯告暟杩囧ぇ

**瑙ｅ喅鏂规**锛?- 鍑忓皬椹荤暀鏃堕棿锛堥渶骞宠　绋冲畾鎬э級
- 鍑忓皬 `state.tau_theta`锛堥渶骞宠　骞虫粦搴︼級
- **娉ㄦ剰**锛氬搷搴旈€熷害涓庣ǔ瀹氭€ф槸鏉冭　鍏崇郴锛岄渶鏍规嵁瀹為檯闇€姹傝皟鏁?
---

### 闂5锛氬潯搴︿及璁′笉鍑?
**鍘熷洜**锛氭崯澶辨潈閲嶄笉骞宠　鎴栬缁冩暟鎹鐩栦笉瓒?
**瑙ｅ喅鏂规**锛?- 澧炲ぇ `cfg.lambda_theta`锛堝 0.3鈫?.5锛?- 妫€鏌ヨ缁冩暟鎹腑 slope 鍦烘櫙鐨勮鐩栬寖鍥?- 妫€鏌ョ壒寰佹护娉㈠弬鏁版槸鍚︿竴鑷达紙棰勫鐞嗕笌鍦ㄧ嚎鎺ㄧ悊锛?
---

### 闂6锛氬钩鍦板満鏅?theta_hat 娉㈠姩

**鍘熷洜**锛欸RU 鍦ㄩ潪 slope 鍦烘櫙涓嬩粛杈撳嚭闈為浂鍊?
**瑙ｅ喅鏂规**锛?- 宸插湪 V1.3 鐗堟湰涓慨澶嶏細闈?slope 鍦烘櫙寮哄埗 theta_hat=0
- 濡備粛鏈夋尝鍔紝鍙澶?`state.theta_deadzone`

---

## 蹇€熷弬鑰?
### 鏂囦欢娓呭崟

| 鏂囦欢 | 闃舵 | 浣滅敤 |
|------|------|------|
| `GRU_gen_train_data.m` | 鏁版嵁鐢熸垚 | 鐢熸垚鍘熷璁粌鏁版嵁 |
| `GRU_prepare_dataset.m` | 鏁版嵁棰勫鐞?| 棰勫鐞嗗拰鍒囩墖 |
| `GRU_train.m` | 妯″瀷璁粌 | 璁粌 GRU 妯″瀷 |
| `GRU_infer.m` | 鎺ㄧ悊 | 鍗曟鎺ㄧ悊鎺ュ彛 |
| `GRU_state_classifier.m` | 鎺ㄧ悊 | 鍦ㄧ嚎鎺ㄧ悊灏佽 |
| `test_GRU_workflow.m` | 娴嬭瘯 | 蹇€熺鍒扮妫€鏌?|
| `test_gru_performance.m` | 娴嬭瘯 | 绂荤嚎/鍦ㄧ嚎鎸囨爣璇勪及銆乺un 绾у埆瀵规瘮 |
| `test_closed_loop_performance.m` | 娴嬭瘯 | Simulink 闂幆鎵归噺璇勪及 |

### 浜х墿鏂囦欢娓呭崟

| 鏂囦欢 | 闃舵 | 鍐呭 |
|------|------|------|
| `GRU_train_data_full.mat` | 鏁版嵁鐢熸垚 | 鍘熷璁粌鏁版嵁 |
| `GRU_dataset_processed.mat` | 鏁版嵁棰勫鐞?| 棰勫鐞嗗悗鐨勬暟鎹泦 |
| `GRU_scaler.mat` | 鏁版嵁棰勫鐞?| 褰掍竴鍖栧弬鏁?|
| `GRU_model.mat` | 妯″瀷璁粌 | 璁粌濂界殑妯″瀷 |
| `GRU_meta.mat` | 妯″瀷璁粌 | 璁粌鍏冩暟鎹?|
| `GRU_logs/` | 妯″瀷璁粌 | 璁粌鏃ュ織鍜屽彲瑙嗗寲 |
| `GRU_logs/eval_reports/` | 娴嬭瘯 | GRU 鎸囨爣鎶ュ憡銆佸湪绾挎埅鍥?|
| `GRU_logs/closed_loop_eval/` | 娴嬭瘯 | 闂幆浠跨湡缁撴灉銆乻ummary |

### 鍏稿瀷鍙傛暟閰嶇疆

#### 蹇€熸祴璇曢厤缃?```matlab
% 鏁版嵁鐢熸垚
cfg.num_runs = 1;
cfg.scenes = {'straight'};

% 鏁版嵁棰勫鐞?cfg.seq_len = 48;
cfg.stride = 12;

% 妯″瀷璁粌
cfg.max_epochs = 10;
cfg.batch_size = 32;
```

#### 瀹屾暣璁粌閰嶇疆
```matlab
% 鏁版嵁鐢熸垚
cfg.num_runs = 150;
cfg.scenes = {'straight', 'turn_left', 'turn_right', 'straight_turn', 'slope', 'bumpy'};
cfg.slip_cfg.prob = 0.70;
cfg.stall_cfg.prob = 0.40;

% 鏁版嵁棰勫鐞?cfg.seq_len = 48;
cfg.stride = 12;
cfg.train_ratio = 0.7;

% 妯″瀷璁粌
cfg.hidden_size = 96;
cfg.num_layers = 2;
cfg.batch_size = 64;
cfg.max_epochs = 150;
cfg.initial_lr = 1e-3;
```

#### 鍦ㄧ嚎鎺ㄧ悊閰嶇疆
```matlab
% 鍦?GRU_state_classifier.m 涓?state.dwell_main = 0.20;     % 涓诲垎绫婚┗鐣欐椂闂?state.dwell_turn = 0.40;     % 杞集鐘舵€侀┗鐣欐椂闂?state.tau_theta = 0.15;      % theta_hat 婊ゆ尝鏃堕棿甯告暟
state.theta_deadzone = 0.02; % 姝诲尯闃堝€?```

---

## 鐗堟湰鍘嗗彶

- **V1.4**锛?025-11-26锛夛細缁熶竴鍦ㄧ嚎/绂荤嚎椹荤暀鏃堕棿锛?.20s/0.40s锛変笌 `tau_theta=0.15s`锛岄檷浣庤瘑鍒欢鏃?- **V1.3**锛?025-01-XX锛夛細闈?slope 鍦烘櫙寮哄埗 theta_hat=0锛屽鍔犳鍖哄鐞?- **V1.2**锛?025-11-04锛夛細鎭㈠椹荤暀鏃堕棿鑷?0.4s
- **V1.1**锛?025-11-01锛夛細鐗瑰緛璁＄畻涓庣绾垮榻愶紝澧炲姞 I_diff_signed 鐗瑰緛

---

## 鐩稿叧鏂囨。

- `README_GRU_Integration.md`锛欸RU 涓?MPC 闆嗘垚璇存槑
- `func.md`锛氬姛鑳藉鑸枃妗?- `change.md`锛氬彉鏇磋褰?
---

## 鑱旂郴鏂瑰紡

濡傛湁闂鎴栧缓璁紝璇峰弬鑰冮」鐩枃妗ｆ垨鑱旂郴寮€鍙戝洟闃熴€?

