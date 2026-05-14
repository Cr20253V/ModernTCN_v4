# MPC 鍙傛暟鍔犺浇蹇€熷弬鑰冨崱鐗?
> 蹇€熸煡闃呯増鏈紝璇︾粏璇存槑瑙?`MPC鍙傛暟鍔犺浇閫昏緫璇存槑.md`

---

## 涓€銆佸垵濮嬪寲闃舵锛圥reLoadFcn锛屼粎杩愯涓€娆★級

| 姝ラ | 鏂囦欢/鍙橀噺 | 浣滅敤 | 杈撳嚭鍒?|
|-----|----------|------|-------|
| **0** | `parameters.m` | 鍔犺浇鐗╃悊鍙傛暟銆乀s | `params` (Base WS) |
| **1** | `lin_agv_db.mat` | 鍔犺浇LPV鏁版嵁搴擄紙A/B/C/D/E缃戞牸锛?| `db_rt` (Base WS) |
| **2** | 鍐呴儴鐢熸垚 | 鍒涘缓鎬荤嚎绫诲瀷 | `MPCPlantBus`, `plant_ic` |
| **3** | `maps_best.mat` | 鍔犺浇浼樺寲鏉冮噸/绾︽潫鍙傛暟 | `maps_best` (鍐呭瓨) |
| **4** | `mpc_setup_single_interp()` | 鍒涘缓MPC鎺у埗鍣ㄥ璞?| `ctrl` (Base WS) |
| **5** | `GRU_model.mat` | 鍔犺浇GRU宸ュ喌璇嗗埆妯″瀷 | `gru_model` (Base WS) |

### 鍏抽敭鍙橀噺缁撴瀯

#### `db_rt`锛圠PV鏁版嵁搴擄級
```matlab
db_rt.A     % [Nv脳Nw脳Nt脳4脳4] 鐘舵€佺煩闃?db_rt.B     % [Nv脳Nw脳Nt脳4脳2] 杈撳叆鐭╅樀锛圡V锛?db_rt.E     % [Nv脳Nw脳Nt脳4脳1] 鎵板姩鐭╅樀锛圡D锛?db_rt.grid  % {V, W, T} 缃戞牸瀹氫箟
db_rt.Ts    % 閲囨牱鍛ㄦ湡
```

#### `ctrl`锛圡PC鎺у埗鍣級
```matlab
ctrl.mpcobj  % MATLAB MPC瀵硅薄
ctrl.maps    % 鏉冮噸/绾︽潫鏄犲皠琛?  .Q_range     % [2脳4] 杈撳嚭鏉冮噸鑼冨洿
  .R_range     % [2脳2] 杈撳叆鏉冮噸鑼冨洿
  .dR_range    % [2脳2] 閫熺巼鏉冮噸鑼冨洿
  .alpha_Q/R/dR % 褰㈢姸鍙傛暟涓嬬晫
  .beta_Q/R/dR  % 褰㈢姸鍙傛暟涓婄晫
  .scale_umin/umax_lo/hi % 绾︽潫缂╂斁
  .omega_threshold  % 杞集鍒ゅ畾闃堝€?(0.15 rad/s)
  .q_y_gain_max     % 杞集鏃秖_y澧炵泭 (1.8)
```

#### `maps_best`锛堣礉鍙舵柉浼樺寲缁撴灉锛?```matlab
% 鐢?Bayesian_Optimization.m 鐢熸垚
% 鍦?PreLoadFcn 姝ラ4 涓鍒跺埌 ctrl.maps
maps_best.Q_range   % 瑕嗙洊榛樿鏉冮噸鑼冨洿
maps_best.alpha_Q   % 瑕嗙洊褰㈢姸鍙傛暟
maps_best.scale_*   % 瑕嗙洊绾︽潫缂╂斁
```

---

## 浜屻€佸湪绾挎洿鏂伴樁娈碉紙姣忎釜浠跨湡姝ワ級

```
Step 1: Plant 杈撳嚭
  鈫?y_raw [31脳1]
Step 2: GRU 鎺ㄧ悊
  鈫?theta_hat [rad]
Step 3: 鏋勯€?蟻锛圧hoFilter锛?  鈫?rho_f = [v; 蠅; 胃_hat]锛堟护娉紝蟿=0.4s锛?Step 4: 妯″瀷/鏉冮噸鎻掑€?  mpc_update_from_rho(rho_f, db_rt, ctrl.maps)
  鈫?upd.{A,B,C,D,E,Q,R,dR,umin,umax}
Step 5: MPC 姹傝В
  mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md)
  鈫?u_mpc = [F_cmd; omega_cmd]
Step 6: Plant 鏇存柊
  state_eq_ref(x, u, theta_ground, params)
  鈫?x_next
```

---

## 涓夈€佸叧閿嚱鏁版帴鍙ｉ€熸煡

### `mpc_setup_single_interp(db, opts)`
**杈撳叆**锛?- `db`锛歀PV鏁版嵁搴擄紙鏉ヨ嚜 `db_rt`锛?- `opts`锛氳璁￠€夐」锛圢p, Nc, Q, R, dR, 绾︽潫绛夛級

**杈撳嚭**锛?- `ctrl`锛氭帶鍒跺櫒缁撴瀯浣?  - `ctrl.mpcobj`锛歁PC瀵硅薄
  - `ctrl.maps`锛氭潈閲?绾︽潫鏄犲皠琛?
**榛樿鍙傛暟**锛?```matlab
Np = round(1.5/Ts);      % 棰勬祴鏃跺煙 鈮?.5s (30姝?
Nc = round(0.5/Ts);      % 鎺у埗鏃跺煙 鈮?.5s (10姝?
Q  = [3, 8, 1, 1];       % [e_y, e_psi, e_v, e_omega]
R  = [1e-3, 1e-3];       % [F_cmd, omega_cmd]
dR = [1e-2, 1e-2];       % 閫熺巼鏉冮噸
umin = [-300; -0.6];     % 杈撳叆涓嬬晫
umax = [300; 0.6];
```

---

### `mpc_update_from_rho(rho, db, maps)`
**杈撳叆**锛?- `rho`锛氳皟搴﹀彉閲?`[v; omega; theta]` (3脳1)
- `db`锛歀PV鏁版嵁搴?- `maps`锛氭潈閲?绾︽潫鏄犲皠琛?
**杈撳嚭**锛?- `upd`锛氭洿鏂扮粨鏋勪綋
  - `A/B/C/D`锛氭彃鍊煎悗鐨勬ā鍨嬬煩闃?  - `E/Bv`锛氭壈鍔ㄥ奖鍝嶇煩闃碉紙鍧″害瑙掞級
  - `Q/R/dR`锛氭彃鍊煎悗鐨勬潈閲?  - `umin/umax`锛氭彃鍊煎悗鐨勭害鏉?
**鏍稿績绠楁硶**锛?1. 褰掍竴鍖?`蟻` 鍒?`[0,1]^3`
2. 瀹氫綅8涓《鐐癸紙涓夌嚎鎬ф彃鍊硷級
3. 璁＄畻鎻掑€兼潈閲?`w = [w1,...,w8]`
4. 鎻掑€兼ā鍨嬶細`A = 危 w_i * A_i`
5. 鎻掑€兼潈閲嶏細鎸夌淮搴︽槧灏勶紙`fy, fpsi, fv, fomega`锛?6. 鍦烘櫙鑷€傚簲锛氳浆寮椂鎻愰珮 `q_y`

---

## 鍥涖€佹潈閲嶈皟搴︾瓥鐣?
### 鏂规A锛氭寜缁村害鏄犲皠锛堥粯璁わ級
姣忎釜鏉冮噸鍏冪礌鐙珛璋冨害锛?```matlab
% 璋冨害鍥犲瓙锛堥粯璁ょ嚎鎬х粍鍚堬級
fy   = 0.3*v_n + 0.2*蠅_n + 0.5*胃_n  % 褰卞搷 q_y
fpsi = 0.1*v_n + 0.7*蠅_n + 0.2*胃_n  % 褰卞搷 q_psi
fv   = 0.8*v_n + 0.1*蠅_n + 0.1*胃_n  % 褰卞搷 q_v
fomega = 0.2*v_n + 0.6*蠅_n + 0.2*胃_n  % 褰卞搷 q_omega

% 鏉冮噸鎻掑€?q_y = Q_min(1) + fy * (Q_max(1) - Q_min(1))
```

### 鏂规B锛氬満鏅嚜閫傚簲锛堝彔鍔狅級
杞集鏃惰嚜鍔ㄦ彁楂?`q_y`锛?```matlab
if |蠅| < 蠅_thresh - 螖蠅:
    q_y_gain = 1.0          % 鐩寸嚎鍖哄煙
elseif |蠅| > 蠅_thresh + 螖蠅:
    q_y_gain = gain_max     % 杞集鍖哄煙 (1.8脳)
else:
    q_y_gain = smooth_interp  % 骞虫粦杩囨浮

q_y_final = q_y * q_y_gain
```

**鍙傛暟**锛堝湪 `ctrl.maps` 涓級锛?- `omega_threshold = 0.15` rad/s
- `q_y_gain_max = 1.8`
- `transition_width = 0.05` rad/s

---

## 浜斻€佺害鏉熻皟搴︾瓥鐣?
### 鍩轰簬瑙掗€熷害鐨勭嚎鎬ф彃鍊?```matlab
蠅_n = (蠅 - 蠅_min) / (蠅_max - 蠅_min)  % 褰掍竴鍖?
umin = (1-蠅_n) * umin_lo + 蠅_n * umin_hi
umax = (1-蠅_n) * umax_lo + 蠅_n * umax_hi
```

### 缂╂斁鍥犲瓙锛堝彔鍔狅級
```matlab
scale_umin = (1-蠅_n) * scale_lo + 蠅_n * scale_hi
umin_final = umin * scale_umin
```

**绀轰緥**锛?- 鐩寸嚎锛坄蠅_n=0`锛夛細浣跨敤 `umin_lo`, `scale_lo`
- 杞集锛坄蠅_n=1`锛夛細浣跨敤 `umin_hi`, `scale_hi`锛堝彲鏀惧绾︽潫锛?
---

## 鍏€佽礉鍙舵柉浼樺寲娴佺▼

```
Bayesian_Optimization(params, db, options)
  鈹溾攢 绗竴闃舵锛氬叏灞€鎼滅储锛?00娆¤瘎浼帮紝榛樿锛?  鈹?  鈹溾攢 浼樺寲鍙橀噺锛歲_y, q_psi, ..., tau (19涓?
  鈹?  鈹溾攢 鐩爣鍑芥暟锛欳ost_Function
  鈹?  鈹?  鈹溾攢 鍦烘櫙锛歵urn, slope, straight_turn, bumpy, straight
  鈹?  鈹?  鈹斺攢 浠ｄ环锛欽 = 危 w_s * J_scene
  鈹?  鈹斺攢 杈撳嚭锛氬叏灞€鏈€浼樼偣
  鈹?  鈹溾攢 绗簩闃舵锛氬眬閮ㄧ簿缁嗘悳绱紙30娆¤瘎浼帮紝榛樿锛?  鈹?  鈹溾攢 浼樺寲鑼冨洿锛氬叏灞€鏈€浼樼偣 卤20%
  鈹?  鈹斺攢 杈撳嚭锛氬眬閮ㄦ渶浼樼偣
  鈹?  鈹斺攢 淇濆瓨缁撴灉锛歮aps_best.mat锛堟牴鐩綍锛?      鈹溾攢 Q_range, R_range, dR_range
      鈹溾攢 alpha_Q/R/dR, beta_Q/R/dR
      鈹溾攢 scale_umin/umax_lo/hi
      鈹斺攢 timestamp, version
```

**鍚姩鑴氭湰**锛歚start_bayesian.m`

---

## 涓冦€佹晠闅滄帓鏌ラ€熸煡

| 鐥囩姸 | 鍙兘鍘熷洜 | 妫€鏌ラ」 | 瑙ｅ喅鏂规 |
|-----|---------|-------|---------|
| **MPC姹傝В澶辫触** | 绾︽潫杩囦弗 | `Info.QPCode` | 鏀惧杈撳嚭绾︽潫 `ymin/ymax` |
| | 妯″瀷涓嶇ǔ瀹?| `max(abs(eig(A)))` | 妫€鏌ョ嚎鎬у寲缃戞牸鑼冨洿 |
| | 鏉冮噸杩囧ぇ | `upd.Q` | 妫€鏌?`Q_range` 涓婄晫 |
| **鏉冮噸鏈敓鏁?* | 澶栭儴绔彛鏈繛鎺?| Simulink鍧楅厤缃?| 鍚敤"External Weights" |
| | 鎻掑€艰绂佺敤 | `ctrl.maps.enable_weight_interp` | 璁句负 `true` |
| **鍧″害琛ュ伩鏃犳晥** | GRU浼拌涓嶅噯 | `abs(胃_hat - 胃_ground)` | 妫€鏌RU妯″瀷鎬ц兘 |
| | MD閫氶亾閿欒 | `upd.E(3,:)` | 纭绗?琛岄潪闆?|
| | MD鏈繛鎺?| Simulink鎺ョ嚎 | 妫€鏌?`md` 绔彛 |
| **杞集e_y杩囧ぇ** | `q_y` 杩囦綆 | `upd.Q(1)` | 鎻愰珮 `Q_range(1)` |
| | 鍦烘櫙鑷€傚簲鏈惎鐢?| `q_y_gain` | 妫€鏌?`omega_threshold` |
| | 澧炵泭杩囧皬 | `q_y_gain_max` | 璋冩暣涓?1.8~2.5 |

---

## 鍏€佽皟璇曟妧宸?
### 1. 鎵撳嵃褰撳墠 蟻 涓庢彃鍊肩粨鏋?```matlab
fprintf('蟻 = [%.3f, %.3f, %.3f]\n', rho(1), rho(2), rho(3));
upd = mpc_update_from_rho(rho, db_rt, ctrl.maps);
fprintf('Q = [%.2f, %.2f, %.2f, %.2f]\n', upd.Q);
fprintf('鎻掑€奸《鐐? [%d,%d,%d] 鑷?[%d,%d,%d]\n', ...
    upd.debug.i_range(1), upd.debug.j_range(1), upd.debug.k_range(1), ...
    upd.debug.i_range(2), upd.debug.j_range(2), upd.debug.k_range(2));
```

### 2. 楠岃瘉妯″瀷鐭╅樀鎻掑€?```matlab
% 妫€鏌ョ壒寰佸€硷紙绋冲畾鎬э級
eig_A = eig(upd.A);
fprintf('max|位(A)| = %.3f (搴?< 1.0)\n', max(abs(eig_A)));

% 妫€鏌ユ壈鍔ㄥ奖鍝嶏紙鍧″害瑙掞級
fprintf('E(绾靛悜) = %.6f (搴旈潪闆?\n', upd.E(3,1));
```

### 3. 瑙傚療鍦烘櫙鑷€傚簲鏁堟灉
```matlab
omega_abs = abs(rho(2));
fprintf('|蠅| = %.3f rad/s\n', omega_abs);
fprintf('q_y_gain = %.2f (闃堝€? %.3f)\n', ...
    q_y_gain, ctrl.maps.omega_threshold);
```

### 4. 妫€鏌ユ潈閲嶈寖鍥村姞杞?```matlab
fprintf('Q_range:\n');
disp(ctrl.maps.Q_range);
fprintf('鍩哄噯Q: [%.2f, %.2f, %.2f, %.2f]\n', ...
    mean(ctrl.maps.Q_range, 1));
```

---

## 涔濄€佹枃浠舵竻鍗?
| 鏂囦欢鍚?| 浣嶇疆 | 浣滅敤 |
|-------|------|------|
| `parameters.m` | 鏍圭洰褰?| 闆嗕腑鍙傛暟瀹氫箟 |
| `lin_agv_db.mat` | 鏍圭洰褰?| LPV鏁版嵁搴擄紙绂荤嚎鐢熸垚锛?|
| `maps_best.mat` | 鏍圭洰褰?| 浼樺寲鏉冮噸/绾︽潫锛堣礉鍙舵柉浼樺寲浜х墿锛?|
| `ctrl.mat` | 鏍圭洰褰?| 棰勫垱寤虹殑鎺у埗鍣紙鍙€夛紝鑺傜渷鏃堕棿锛?|
| `GRU_model.mat` | 鏍圭洰褰?| GRU宸ュ喌璇嗗埆妯″瀷 |
| `mpc_setup_single_interp.m` | 鏍圭洰褰?| MPC鎺у埗鍣ㄥ垱寤?|
| `mpc_update_from_rho.m` | 鏍圭洰褰?| 鍦ㄧ嚎鍙傛暟鏇存柊 |
| `Cost_Function.m` | 鏍圭洰褰?| MPC闂幆璇勪及 |
| `Bayesian_Optimization.m` | 鏍圭洰褰?| 璐濆彾鏂紭鍖栭┍鍔?|
| `start_bayesian.m` | 鏍圭洰褰?| 浼樺寲鍚姩鑴氭湰 |
| `LPVMPC_AGV_simulink._GRU.slx` | 鏍圭洰褰?| Simulink浠跨湡妯″瀷 |

---

## 鍗併€佸父鐢ㄥ懡浠ら€熸煡

### 鐢熸垚LPV鏁版嵁搴?```matlab
params = parameters();
grid.V_grid = [0.8; 1.0; 1.2];
grid.W_grid = [-0.2; 0.0; 0.2];
grid.T_grid = [-0.2; 0.0; 0.2];
lin_opts = struct('coord','path','disc','zoh','keep_E',true,'export_mat','lin_agv_db.mat');
db = lin_agv_grid(params, grid, lin_opts);
```

### 鍒涘缓MPC鎺у埗鍣?```matlab
params = parameters();
db = load('lin_agv_db.mat', 'db').db;
ctrl = mpc_setup_single_interp(db, struct());
save('ctrl.mat', 'ctrl');
```

### 杩愯璐濆彾鏂紭鍖?```matlab
params = parameters();
db = load('lin_agv_db.mat', 'db').db;
options.MaxObjectiveEvaluations = 100;
[best, boResults] = Bayesian_Optimization(params, db, options);
% 鑷姩鐢熸垚 maps_best.mat
```

### 杩愯Simulink浠跨湡
```matlab
% 纭繚 PreLoadFcn 宸查厤缃?open_system('LPVMPC_AGV_simulink._GRU.slx');
sim('LPVMPC_AGV_simulink._GRU');
```

### 妫€鏌ヤ紭鍖栫粨鏋?```matlab
load('maps_best.mat');
fprintf('浼樺寲鏉冮噸鍩哄噯:\n');
fprintf('  Q_base = [%.2f, %.2f, %.2f, %.2f]\n', mean(maps_best.Q_range,1));
fprintf('  R_base = [%.6f, %.6f]\n', mean(maps_best.R_range,1));
fprintf('  dR_base = [%.6f, %.6f]\n', mean(maps_best.dR_range,1));
```

---

## 鍗佷竴銆佹牳蹇冭璁＄悊蹇?
1. **鍒嗗眰璁捐**锛氬弬鏁?鈫?鏁版嵁搴?鈫?鎺у埗鍣?鈫?鍦ㄧ嚎鏇存柊
2. **鏅鸿兘璋冨害**锛氭牴鎹伐鍐?`蟻` 鑷€傚簲璋冩暣妯″瀷鍜屽弬鏁?3. **鎸夌淮搴︽槧灏?*锛氭瘡涓潈閲嶅厓绱犵嫭绔嬭皟搴︼紙闈炵粺涓€缂╂斁锛?4. **鍦烘櫙鑷€傚簲**锛氳浆寮椂鑷姩鎻愰珮妯悜璺熻釜绮惧害
5. **鍓嶉琛ュ伩**锛氬潯搴﹁杩涘叆MD閫氶亾锛屾彁鍓嶉娴嬫壈鍔?6. **璐濆彾鏂紭鍖?*锛氳嚜鍔ㄥ鎵炬渶浼樻潈閲嶈寖鍥?7. **鏁板€肩ǔ鍋?*锛氳竟鐣岄ケ鍜屻€佹护娉€佸綊涓€鍖栦繚璇佺ǔ瀹氭€?
---

**鐗堟湰**锛歏1.0锛?025-11-06锛? 
**閰嶅鏂囨。**锛歚MPC鍙傛暟鍔犺浇閫昏緫璇存槑.md`锛堣缁嗙増锛? 
**缁存姢璁板綍**锛氳 `change.md`


