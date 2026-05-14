# GRU妯″瀷闆嗘垚鍒癓PVMPC_AGV_simulink.slx鎸囧崡

## 姒傝堪

鏈枃妗ｈ缁嗕粙缁嶅浣曞皢GRU宸ュ喌璇嗗埆妯″瀷闆嗘垚鍒癓PVMPC_AGV_simulink.slx涓紝瀹炵幇鍦ㄧ嚎鍧″害瑙掍及璁★紙`theta_hat`锛夊苟娉ㄥ叆MPC鐨凪D锛圡easured Disturbance锛夐€氶亾銆?
## 鍓嶆彁鏉′欢

纭繚浠ヤ笅鏂囦欢瀛樺湪浜庨」鐩牴鐩綍锛?- 鉁?`GRU_model.mat` - 璁粌濂界殑GRU妯″瀷
- 鉁?`GRU_scaler.mat` - 褰掍竴鍖栧弬鏁?- 鉁?`GRU_state_classifier.m` - 鍦ㄧ嚎鎺ㄧ悊灏佽
- 鉁?`GRU_infer.m` - GRU鎺ㄧ悊鎺ュ彛
- 鉁?`LPVMPC_AGV_simulink._GRU.slx` - 鐜版湁Simulink妯″瀷
- 鉁?`parameters.m` - 绯荤粺鍙傛暟

---

## 闆嗘垚姝ラ

### 姝ラ1锛氭墦寮€Simulink妯″瀷

```matlab
% 鍦∕ATLAB鍛戒护绐楀彛鎵ц
open_system('LPVMPC_AGV_simulink._GRU.slx')
```

---

### 姝ラ2锛氭坊鍔燝RU宸ュ喌璇嗗埆瀛愮郴缁?
#### 2.1 鍒涘缓MATLAB Function鍧?
1. 鍦⊿imulink搴撴祻瑙堝櫒涓壘鍒?**User-Defined Functions 鈫?MATLAB Function**
2. 鎷栨嫿鍒版ā鍨嬬殑鍚堥€備綅缃紙寤鸿鏀惧湪Plant妯″潡闄勮繎锛?3. 鍙屽嚮璇ュ潡锛岄噸鍛藉悕涓?`GRU_State_Classifier`

#### 2.2 閰嶇疆MATLAB Function浠ｇ爜

鍙屽嚮 `GRU_State_Classifier` 鍧楋紝鍦ㄧ紪杈戝櫒涓緭鍏ヤ互涓嬩唬鐮侊細

```matlab
function [theta_hat, label_main, label_turn, conf_main] = GRU_State_Classifier(y_raw, reset)
%#codegen

% ========== 1. 澹版槑鎵€鏈?extrinsic 鍑芥暟锛堝繀椤诲湪椤跺眰锛屼换浣曡皟鐢ㄤ箣鍓嶏級==========
coder.extrinsic('evalin');
coder.extrinsic('assignin');
coder.extrinsic('GRU_state_classifier');

% ========== 2. 鎸佷箙鍙橀噺 ==========
persistent state is_initialized

% ========== 3. 鏄惧紡鎸囧畾杈撳嚭绫诲瀷鍜屽ぇ灏忥紙閬垮厤Simulink鎺ㄦ柇閿欒锛?=========
theta_hat = 0.0;      % [1脳1] double
label_main = 1.0;     % [1脳1] double
label_turn = 0.0;     % [1脳1] double
conf_main = 1.0;      % [1脳1] double

% ========== 4. 鍒濆鍖栵紙棣栨璋冪敤鎴杛eset=1锛?=========
if isempty(is_initialized)
    is_initialized = false;
end

if ~is_initialized || reset == 1
    % 浠嶣ase Workspace璇诲彇棰勫姞杞界殑鏁版嵁锛堝湪PreLoadFcn涓姞杞斤級
    model = evalin('base', 'gru_model');
    params = evalin('base', 'params');
    
    % 鍒濆鍖栧垎绫诲櫒鐘舵€?    state = GRU_state_classifier('init', params, model);
    
    is_initialized = true;
    
    % 鍒濆鍖栭樁娈佃繑鍥為粯璁ゅ€?    return;
end

% ========== 5. 瀹夊叏妫€鏌ワ細纭繚state宸插畾涔夛紙閬垮厤Coder閿欒锛?=========
if isempty(state)
    % 濡傛灉state鏈畾涔夛紙寮傚父鎯呭喌锛夛紝杩斿洖榛樿鍊?    return;
end

% ========== 6. 鍦ㄧ嚎鏇存柊锛堟瘡涓噰鏍峰懆鏈熻皟鐢級==========
[state, out] = GRU_state_classifier('update', state, y_raw);

% ========== 7. 鎻愬彇杈撳嚭锛堜娇鐢╡valin闂存帴璁块棶锛屾棤闇€澶栭儴鏂囦欢锛?=========
% 鏂规硶锛氬皢out涓存椂淇濆瓨鍒癰ase workspace锛岀劧鍚庣敤evalin鎻愬彇瀛楁
assignin('base', 'gru_out_temp', out);
theta_hat = evalin('base', 'double(gru_out_temp.theta_hat)');
label_main = evalin('base', 'double(gru_out_temp.label_main)');
label_turn = evalin('base', 'double(gru_out_temp.label_turn)');
conf_main = evalin('base', 'double(gru_out_temp.conf_main(1))');

end
```

**鏂规2鐨勪紭鐐?*锛?- 鉁?涓嶉渶瑕?`extract_gru_output.m` 澶栭儴鏂囦欢
- 鉁?鎵€鏈変唬鐮佸湪涓€涓嚱鏁板唴
- 鉁?鍚屾牱瑙ｅ喅浜?mxArray 璁块棶闂

**鏂规2鐨勭己鐐?*锛?- 鈿狅笍 姣忔璋冪敤 4 娆?`evalin`锛堢◢鎱紝浣嗗彲鎺ュ彈锛?- 鈿狅笍 涓存椂鍙橀噺 `gru_out_temp` 鍗犵敤 base workspace锛堝緢灏忥級

**閲嶈鎻愮ず**锛氫笂杩颁唬鐮佸寘鍚?`coder.extrinsic` 澹版槑锛岃繖鎰忓懗鐫€锛?- 鉁?**浠跨湡妯″紡**锛氬畬鍏ㄦ敮鎸侊紝璋冪敤MATLAB瑙ｉ噴鍣ㄦ墽琛?- 鈿狅笍 **浠ｇ爜鐢熸垚妯″紡**锛氶渶瑕佺壒娈婂鐞嗭紙瑙佷笅鏂?浠ｇ爜鐢熸垚浼樺寲"锛?
#### 2.3 閰嶇疆杈撳叆杈撳嚭绔彛

鍦∕ATLAB Function缂栬緫鍣ㄧ殑 **Edit Data** 鎸夐挳锛堟垨Ctrl+Shift+M锛夐厤缃鍙ｏ細

**杈撳叆绔彛**锛?| 鍚嶇О | 绫诲瀷 | 缁村害 | 璇存槑 |
|------|------|------|------|
| `y_raw` | double | [31脳1] | Plant杈撳嚭锛堟潵鑷猳utput_eq锛?|
| `reset` | double | [1脳1] | 閲嶇疆淇″彿锛?=姝ｅ父, 1=閲嶇疆锛?|

**杈撳嚭绔彛**锛?| 鍚嶇О | 绫诲瀷 | 缁村害 | 璇存槑 |
|------|------|------|------|
| `theta_hat` | double | [1脳1] | 鍧″害瑙掍及璁?[rad] |
| `label_main` | double | [1脳1] | 涓诲垎绫?{1,2,3,4} |
| `label_turn` | double | [1脳1] | 杞集鐘舵€?{-1,0,+1} |
| `conf_main` | double | [1脳1] | 涓诲垎绫荤疆淇″害 [0,1] |

---

### 姝ラ3锛氳繛鎺ヤ俊鍙风嚎

#### 3.1 杩炴帴GRU杈撳叆锛圥lant杈撳嚭 鈫?GRU锛?
鎵惧埌鐜版湁鐨?**Plant妯″潡**锛圓GV_Model S-Function锛夛紝瀹冭緭鍑?`y_raw [31脳1]`锛?
```
Plant (AGV_Model) 杈撳嚭绔彛
   鈫?   鈹溾攢鈫?GRU_State_Classifier 鐨?y_raw 杈撳叆
   鈹斺攢鈫?锛堢幇鏈夎繛鎺ワ紝淇濇寔涓嶅彉锛?```

鎿嶄綔姝ラ锛?1. 浣跨敤 **Mux** 鎴?**Bus Selector** 鎻愬彇Plant鐨勫畬鏁?1缁磋緭鍑?2. 杩炴帴鍒?`GRU_State_Classifier` 鐨?`y_raw` 绔彛

#### 3.2 娣诲姞Reset淇″彿锛堝彲閫夛級

濡傛灉闇€瑕佸湪浠跨湡寮€濮嬫椂閲嶇疆GRU鐘舵€侊細
```
Constant (鍊?0)
   鈫?GRU_State_Classifier 鐨?reset 杈撳叆
```

鎴栬€呬娇鐢?**Compare To Zero** 鍧楁娴嬩豢鐪熸椂闂达細
```
Clock 鈫?Compare (t==0) 鈫?GRU reset
```

#### 3.3 杩炴帴GRU杈撳嚭鍒癕PC鐨凪D閫氶亾

鎵惧埌 **Adaptive MPC Controller** 鍧楁垨 **MPC鎺у埗鍣?*妯″潡锛?
```
GRU_State_Classifier 鐨?theta_hat 杈撳嚭
   鈫?Adaptive MPC Controller 鐨?md (Measured Disturbance) 杈撳叆
```

**鍏抽敭閰嶇疆**锛?- MPC鍧楃殑 **Measured Disturbances** 绔彛搴斿惎鐢?- 杈撳叆缁村害锛歚[1脳1]`锛堜粎theta锛?- 鍗曚綅锛歳ad锛堜笌LPV鏁版嵁搴撶殑T_grid涓€鑷达級

#### 3.4 杩炴帴璇婃柇杈撳嚭锛堝彲閫夛級

灏?`label_main`, `label_turn`, `conf_main` 杩炴帴鍒?**Scope** 鎴?**To Workspace** 鍧椾互鐩戞帶宸ュ喌璇嗗埆锛?
```
label_main 鈫?Scope (鏄剧ず flat/slip/stall/slope)
label_turn 鈫?Scope (鏄剧ず right/straight/left)
conf_main  鈫?Scope (鏄剧ず缃俊搴?
```

---

### 姝ラ4锛氶厤缃甊hoFilter锛堣皟搴﹀彉閲忔护娉級

GRU鐨?`theta_hat` 闇€瑕佷笌MPC鐨勮皟搴﹀彉閲?`rho=[v; omega; theta]` 涓€璧锋护娉€?
#### 4.1 淇敼鐜版湁RhoFilter MATLAB Function

濡傛灉妯″瀷涓凡鏈?`RhoFilter` 鍧楋紝淇敼鍏朵唬鐮侊細

```matlab
function rho_f = RhoFilter(v, omega, theta_hat, Ts, tau)
% 涓€闃朵綆閫氭护娉細rho_f = [v_f; omega_f; theta_hat_f]
% tau: 婊ゆ尝鏃堕棿甯告暟 [s]锛堥粯璁?.4s锛?
persistent rho_prev

if isempty(rho_prev)
    rho_prev = [v; omega; theta_hat];  % 鍒濆鍖?end

alpha = Ts / (tau + Ts);
rho_f = alpha * [v; omega; theta_hat] + (1 - alpha) * rho_prev;
rho_prev = rho_f;

end
```

#### 4.2 杩炴帴淇″彿

```
v (閫熷害)     鈹€鈹€鈹€鈹€鈹?omega (瑙掗€熷害) 鈹€鈹€鈹?theta_hat 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈫?RhoFilter 鈹€鈫?rho_f [3脳1] 鈹€鈫?MPC Scheduling 绔彛
Ts (甯告暟) 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?tau (甯告暟) 鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

**鍙傛暟鍊?*锛?- `Ts = 0.01` 锛堟潵鑷猵arameters.m锛?- `tau = 0.4` 锛堟帹鑽愬€硷紝鍙湪 0.3鈥?.5 s 鑼冨洿璋冩暣锛?
---

### 姝ラ5锛氶厤缃瓵daptive MPC鍧?
#### 5.1 鎵惧埌Adaptive MPC Controller鍧?
鍦ㄦā鍨嬩腑鎵惧埌 **Adaptive MPC Controller** 鍧楋紝鍙屽嚮鎵撳紑閰嶇疆闈㈡澘銆?
#### 5.2 閰嶇疆绔彛

| 绔彛鍚嶇О | 璇存槑 | 杩炴帴 |
|---------|------|------|
| **mo** (Measured Outputs) | 娴嬮噺杈撳嚭 [4脳1] | `[e_y; e_psi; e_v; e_omega]` |
| **ref** (Reference) | 鍙傝€冭建杩?[4脳1] | `[0; 0; 0; 0]`锛堣宸秼闆讹級|
| **md** (Measured Disturbance) | 娴嬮噺鎵板姩 [1脳1] | `theta_hat`锛堟潵鑷狦RU锛墊
| **mv** (Manipulated Variables) | 鎺у埗杈撳嚭 [2脳1] | `[F_cmd; omega_cmd]` |

#### 5.3 鍚敤鑷畾涔夋ā鍨嬫洿鏂板嚱鏁?
鍦?**Adaptive MPC** 鍧楀弬鏁板璇濇锛?1. 鍕鹃€?**Use custom state estimation function**锛堝鏋滈渶瑕侊級
2. 鍕鹃€?**Use custom update function**
3. 璁剧疆 **Scheduling signals** 涓?`rho_f`锛堟潵鑷猂hoFilter锛?
#### 5.4 閰嶇疆鑷畾涔夋洿鏂板嚱鏁?
鍦ㄥ潡鍙傛暟涓寚瀹氭洿鏂板嚱鏁帮細
```
Function name: mpc_update_from_rho
```

纭繚Simulink鑳芥壘鍒拌鍑芥暟锛?```matlab
% 鍦∕ATLAB鍛戒护绐楀彛妫€鏌?which mpc_update_from_rho
% 搴旇繑鍥烇細E:\Matlab\Simulink\S-Function_14\mpc_update_from_rho.m
```

---

### 姝ラ6锛氶厤缃豢鐪熷弬鏁?
#### 6.1 鍔犺浇蹇呰鏁版嵁鍒癇ase Workspace 猸?
**閲嶈**锛欸RU_State_Classifier鍧楅渶瑕佷粠Base Workspace璇诲彇棰勫姞杞界殑鏁版嵁銆?
鍦ㄦā鍨嬬殑 **PreLoadFcn** 鍥炶皟涓坊鍔狅細

```matlab
% 妯″瀷鍒濆鍖栬剼鏈紙File 鈫?Model Properties 鈫?Callbacks 鈫?PreLoadFcn锛?
fprintf('姝ｅ湪鍒濆鍖栨ā鍨?..\n');

% ========== 蹇呴』椤癸細GRU渚濊禆 ==========
% 鍔犺浇绯荤粺鍙傛暟锛圙RU_State_Classifier浼氱敤evalin璇诲彇锛?params = parameters();
fprintf('  鉁?鍔犺浇params\n');

% 鍔犺浇GRU妯″瀷锛圙RU_State_Classifier浼氱敤evalin璇诲彇锛?if ~exist('gru_model', 'var')
    load('GRU_model.mat', 'model');
    gru_model = model;
    clear model;  % 閬垮厤鍙橀噺鍚嶅啿绐?    fprintf('  鉁?鍔犺浇gru_model\n');
end

% ========== 鍙€夐」锛歁PC鍜屽弬鑰冭建杩?==========
% 鍔犺浇LPV鏁版嵁搴?if exist('lin_agv_db.mat', 'file')
    load('lin_agv_db.mat', 'db');
    fprintf('  鉁?鍔犺浇db (LPV鏁版嵁搴?\n');
end

% 鍒涘缓MPC鎺у埗鍣?if exist('db', 'var') && ~exist('ctrl', 'var')
    ctrl = mpc_setup_single_interp(db, struct());
    fprintf('  鉁?鍒涘缓ctrl (MPC鎺у埗鍣?\n');
end

% 鍔犺浇鍙傝€冭建杩癸紙绀轰緥锛氳浆寮満鏅級
if ~exist('ref', 'var')
    ref = gen_agv_ref_path('turn', params);
    fprintf('  鉁?鐢熸垚ref (鍙傝€冭建杩?\n');
end

fprintf('鉁?妯″瀷鍒濆鍖栧畬鎴怽n\n');
```

**閰嶇疆PreLoadFcn鐨勬楠?*锛?1. 鍦⊿imulink涓紝鐐瑰嚮鑿滃崟鏍?**File 鈫?Model Properties 鈫?Callbacks**
2. 鍦ㄥ乏渚у垪琛ㄩ€夋嫨 **PreLoadFcn**
3. 鍦ㄥ彸渚х紪杈戝櫒涓矘璐翠笂杩颁唬鐮?4. 鐐瑰嚮 **OK** 淇濆瓨

#### 6.2 璁剧疆姹傝В鍣?
鍦ㄦā鍨嬮厤缃弬鏁帮紙Ctrl+E锛変腑锛?- **Solver**: `ode4` (Runge-Kutta) 鎴?`ode5` (Dormand-Prince)
- **Fixed-step size**: `0.01` (涓巔arams.Ts涓€鑷?
- **Stop time**: `20` (涓庡弬鑰冭建杩规椂闀夸竴鑷?

---

### 姝ラ7锛氭祴璇曢泦鎴?
#### 7.1 缂栬瘧妫€鏌?
```matlab
% 鍦∕ATLAB鍛戒护绐楀彛
open_system('LPVMPC_AGV_simulink._GRU.slx')
set_param('LPVMPC_AGV_simulink._GRU', 'SimulationCommand', 'update')
```

妫€鏌ユ槸鍚︽湁缂栬瘧閿欒锛堢孩鑹叉尝娴嚎锛夈€?
#### 7.2 鐭椂浠跨湡娴嬭瘯

```matlab
% 杩愯2绉掍豢鐪熸祴璇?set_param('LPVMPC_AGV_simulink._GRU', 'StopTime', '2')
sim('LPVMPC_AGV_simulink._GRU')

% 妫€鏌ヨ緭鍑?disp('GRU theta_hat 鍓?0姝?')
disp(theta_hat(1:10))  % 鍋囪宸茶繛鎺ュ埌To Workspace鍧?```

#### 7.3 瀹屾暣鍦烘櫙娴嬭瘯

```matlab
% 鍔犺浇娴嬭瘯鑴氭湰
test_lpvmpc_with_gru_workflow
```

---

## 淇″彿娴佹€昏

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? LPVMPC_AGV_simulink._GRU.slx 淇″彿娴侊紙闆嗘垚GRU鍚庯級                      鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鍙傝€冭建杩?(From Workspace)
   鈹?   鈹? [X_ref, Y_ref, psi_ref, v_ref, omega_ref, theta_ref]
   鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?Path Error   鈹? 璁＄畻璺緞鍧愭爣绯昏宸?鈹?Calculator   鈹? 鈫?[e_y, e_psi, e_v, e_omega]
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?       鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?                        鈹?       鈫?                        鈫?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?Adaptive MPC 鈹?鈫愨攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?RhoFilter    鈹?鈹?Controller   鈹?  rho_f  鈹?[v,蠅,胃_hat]  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?                        鈫?       鈹? [F_cmd, omega_cmd]     鈹?theta_hat
       鈫?                        鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?Plant        鈹?鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫掆攤 GRU_State    鈹?鈹?(S-Function) 鈹? y_raw    鈹?Classifier   鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹? [31脳1]  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?                        鈹?       鈫?                        鈫?    [X,Y,蠄,v,蠅,...]      [label_main, label_turn, conf]
       鈹?                        鈹?       鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                     鈫?              Scopes & Logging
```

---

## 鏁呴殰鎺掓煡

### 闂0锛氱紪璇戦敊璇?"鏃犳硶浠庣被鍨嬩负 mxArray 鐨勫彉閲忎腑鎻愬彇瀛楁" 猸愨瓙

杩欐槸MATLAB Coder鐨勬牳蹇冮檺鍒讹紝鏈変袱绉嶆儏鍐碉細

#### 鎯呭喌A锛氭棤娉曡闂?`load()` 杩斿洖鐨勭粨鏋勪綋瀛楁

**閿欒淇℃伅**锛?```
鏃犳硶浠庣被鍨嬩负 mxArray 鐨勫彉閲忎腑鎻愬彇瀛楁 model锛屽洜涓烘鍙橀噺涓嶆槸缁撴瀯浣撱€?鍑芥暟 'GRU_State_Classifier'锛岃 XX: "model_data"
```

**鍘熷洜**锛歚coder.extrinsic('load')` 杩斿洖 `mxArray` 绫诲瀷锛屾棤娉曡闂?`.model` 瀛楁

**瑙ｅ喅鏂规**锛歅reLoadFcn棰勫姞杞?+ evalin璇诲彇
```matlab
% PreLoadFcn涓細
load('GRU_model.mat', 'model');
gru_model = model;

% MATLAB Function涓細
coder.extrinsic('evalin');
model = evalin('base', 'gru_model');  % 鉁?鍙互璁块棶
```

---

#### 鎯呭喌B锛氭棤娉曡闂?extrinsic 鍑芥暟杩斿洖鐨勭粨鏋勪綋瀛楁 猸?
**閿欒淇℃伅**锛?```
鏃犳硶浠庣被鍨嬩负 mxArray 鐨勫彉閲忎腑鎻愬彇瀛楁 theta_hat锛屽洜涓烘鍙橀噺涓嶆槸缁撴瀯浣撱€?鍑芥暟 'GRU_State_Classifier'锛岃 XX: "out"
```

**鍘熷洜**锛?- `GRU_state_classifier` 琚０鏄庝负 `coder.extrinsic`
- 瀹冪殑杩斿洖鍊?`out` 涔熸槸 `mxArray` 绫诲瀷
- 鏃犳硶璁块棶 `out.theta_hat` 绛夊瓧娈?
**瑙ｅ喅鏂规**锛堚渽 宸插湪涓婃枃浠ｇ爜涓慨姝ｏ級锛?鍒涘缓杈呭姪鍑芥暟 `extract_gru_output.m` 鏉ユ彁鍙栧瓧娈碉細

```matlab
% 1) 鍒涘缓 extract_gru_output.m锛堟牴鐩綍锛?function [theta_hat, label_main, label_turn, conf_main] = extract_gru_output(out)
    theta_hat = double(out.theta_hat);
    label_main = double(out.label_main);
    label_turn = double(out.label_turn);
    conf_main = double(out.conf_main(1));
end

% 2) 鍦∕ATLAB Function涓０鏄庡苟璋冪敤
coder.extrinsic('extract_gru_output');  % 椤跺眰澹版槑

[state, out] = GRU_state_classifier('update', state, y_raw);
[theta_hat, label_main, label_turn, conf_main] = extract_gru_output(out);  % 鉁?鍙互璁块棶
```

**鍏抽敭瑕佺偣**锛?- 鉂?涓嶈兘鐩存帴璁块棶 extrinsic 鍑芥暟杩斿洖鐨勭粨鏋勪綋瀛楁
- 鉁?鍒涘缓鍙︿竴涓?extrinsic 杈呭姪鍑芥暟鏉ユ彁鍙栧瓧娈?- 鉁?杈呭姪鍑芥暟涔熷繀椤诲湪椤跺眰澹版槑

---

### 闂0.5锛氱紪璇戦敊璇?"鎸佷箙鍙橀噺鍦ㄦ煇浜涙墽琛岃矾寰勪腑鏈畾涔? 猸?
**閿欒淇℃伅**锛?```
鎸佷箙鍙橀噺 state 鍦ㄦ煇浜涙墽琛岃矾寰勪腑鏈畾涔夈€傝杩涜浠ｇ爜鐢熸垚锛屾墍鏈夊彉閲忓湪浣跨敤鍓嶉兘蹇呴』瀹屽叏瀹氫箟銆?鍑芥暟 'GRU_State_Classifier'锛岃 35: "state"
```

**鍘熷洜**锛?- MATLAB Coder杩涜闈欐€佸垎鏋愭椂锛屾棤娉曚繚璇?`state` 鍦ㄧ35琛屼娇鐢ㄦ椂涓€瀹氬凡瀹氫箟
- 铏界劧閫昏緫涓婇娆¤皟鐢ㄤ細鍒濆鍖?`state`锛屼絾Coder瑕佹眰鎵€鏈変唬鐮佽矾寰勯兘鏄庣‘瀹氫箟鍙橀噺

**瑙ｅ喅鏂规**锛堚渽 宸插湪涓婃枃浠ｇ爜涓慨姝ｏ級锛?鍦ㄤ娇鐢?`state` 涔嬪墠娣诲姞瀹夊叏妫€鏌ワ細

```matlab
% 鍒濆鍖栧悗return
if ~is_initialized || reset == 1
    state = GRU_state_classifier('init', params, model);
    is_initialized = true;
    return;
end

% 猸?瀹夊叏妫€鏌ワ細纭繚state宸插畾涔?if isempty(state)
    return;  % 寮傚父鎯呭喌锛氳繑鍥為粯璁ゅ€?end

% 鐜板湪鍙互瀹夊叏浣跨敤state
[state, out] = GRU_state_classifier('update', state, y_raw);
```

---

### 闂0.6锛氱紪璇戦敊璇?"瀵?coder.extrinsic 鐨勮皟鐢ㄥ彲鑳藉彧鍑虹幇鍦ㄩ《灞?

**閿欒淇℃伅**锛?```
瀵?coder.extrinsic 鐨勮皟鐢ㄥ彲鑳藉彧鍑虹幇鍦ㄩ《灞傘€?鍑芥暟 'GRU_state_classifier' 鍦ㄤ娇鐢ㄥ悗鏍囪浜?coder.extrinsic銆?```

**鍘熷洜**锛?- `coder.extrinsic` 澹版槑蹇呴』鍦ㄥ嚱鏁?*鏈€椤跺眰**锛堜笉鑳藉湪if璇彞鍐咃級
- 蹇呴』鍦?*浠讳綍璋冪敤涔嬪墠**澹版槑

**瑙ｅ喅鏂规**锛氬皢鎵€鏈?`coder.extrinsic` 鏀惧湪鍑芥暟寮€澶达細
```matlab
function [theta_hat, ...] = GRU_State_Classifier(y_raw, reset)
%#codegen

% 鉁?姝ｇ‘锛氬湪鍑芥暟椤跺眰锛屾墍鏈夎皟鐢ㄤ箣鍓嶅０鏄?coder.extrinsic('evalin');
coder.extrinsic('GRU_state_classifier');
coder.extrinsic('extract_gru_output');
% ...
end
```

---

### 闂1锛氱紪璇戦敊璇?"Undefined function 'GRU_state_classifier'"

**鍘熷洜**锛歁ATLAB Function鍧楁棤娉曟壘鍒板閮ㄥ嚱鏁?
**瑙ｅ喅鏂规**锛?1. 纭繚 `GRU_state_classifier.m` 鍦∕ATLAB璺緞涓細
   ```matlab
   addpath(pwd)  % 娣诲姞褰撳墠鐩綍
   ```
2. 妫€鏌ユ枃浠舵槸鍚﹀瓨鍦細
   ```matlab
   which GRU_state_classifier
   % 搴旇繑鍥炲畬鏁磋矾寰?   ```

### 闂2锛氫豢鐪熷崱椤挎垨寰堟參

**鍘熷洜**锛欸RU鎺ㄧ悊璁＄畻閲忓ぇ

**瑙ｅ喅鏂规**锛?1. 闄嶄綆閲囨牱棰戠巼锛堝湪GRU鍧楀墠鍔?**Rate Transition**锛屼緥濡傞檷鑷?0 Hz锛?2. 妫€鏌RU妯″瀷鏄惁鍦℅PU涓婏紙绉诲埌CPU锛夛細
   ```matlab
   model.net_feature = gatherFromGPUToHost(model.net_feature);
   ```

### 闂3锛歵heta_hat杈撳嚭鍏ㄤ负0

**鍘熷洜**锛欸RU搴忓垪缂撳啿鏈弧锛堝墠48姝ワ級

**瑙ｅ喅鏂规**锛?- 姝ｅ父鐜拌薄锛屽簭鍒楁弧鍚庯紙绾?绉掞級寮€濮嬭緭鍑烘湁鏁堝€?- 鍙湪 `GRU_state_classifier.m` 鐨?`initClassifier` 涓濉厖鍒濆鍊?
### 闂4锛歁PC姹傝В澶辫触

**鍘熷洜**锛歵heta_hat璺冲彉杩囧ぇ

**瑙ｅ喅鏂规**锛?1. 澧炲ぇRhoFilter鐨?`tau`锛堜緥濡?.5s锛?2. 鍦╰heta_hat杈撳嚭鍚庢坊鍔?**Rate Limiter** 鍧楋紙闄愬埗 卤0.1 rad/s锛?
### 闂5锛氫唬鐮佺敓鎴愬け璐?
**鍘熷洜**锛歚coder.extrinsic` 涓嶆敮鎸佸祵鍏ュ紡鐩爣

**瑙ｅ喅鏂规**锛氳涓嬭妭"浠ｇ爜鐢熸垚浼樺寲"

---

## 浠ｇ爜鐢熸垚浼樺寲锛堢敤浜庡祵鍏ュ紡鐩爣锛?
濡傛灉闇€瑕佺敓鎴怌浠ｇ爜锛堜緥濡傜敤浜庣‖浠跺湪鐜疕IL锛夛紝闇€瑕佸皢GRU鎺ㄧ悊閲嶅啓涓哄彲浠ｇ爜鐢熸垚鐨勭増鏈€?
### 鏂规1锛氫娇鐢∕ATLAB Coder鏀寔鐨勬繁搴﹀涔犲眰

灏?`dlnetwork` 杞崲涓?`network` 瀵硅薄锛堜粎鏀寔閮ㄥ垎灞傦級锛?```matlab
% 鍦℅RU_train.m璁粌鍚庢墽琛?net_codegen = coder.loadDeepLearningNetwork('GRU_model.mat', 'model');
```

### 鏂规2锛氫娇鐢⊿imulink Deep Learning Toolbox

灏咷RU鏀逛负 **Stateful Predict** 鍧楋紙鏀寔浠ｇ爜鐢熸垚锛夛細
1. 瀵煎嚭GRU涓篛NNX锛?   ```matlab
   exportONNXNetwork(model.net_feature, 'gru_feature.onnx')
   ```
2. 鍦⊿imulink涓娇鐢?**ONNX Predict** 鍧?
### 鏂规3锛氭墜鍔ㄥ疄鐜癎RU锛堝畬鍏ㄥ彲浠ｇ爜鐢熸垚锛?
鍙傝€?`GRU_state_classifier.m` 鐨勭壒寰佹彁鍙栭€昏緫锛屽皢GRU灞傚睍寮€涓虹煩闃佃繍绠楋紙宸ヤ綔閲忓ぇ锛夈€?
---

## 鎬ц兘鎸囨爣

闆嗘垚鍚庣殑棰勬湡鎬ц兘锛?
| 鎸囨爣 | 鐩爣鍊?| 璇存槑 |
|------|--------|------|
| **GRU鎺ㄧ悊寤惰繜** | < 1 ms/姝?| 鍦╥7-10浠PU涓?|
| **MPC姹傝В鏃堕棿** | < 5 ms/姝?| P95鐧惧垎浣?|
| **theta_hat绮惧害** | MAE < 2掳 | 瀵规瘮theta_ground |
| **涓诲垎绫诲噯纭巼** | > 85% | 鍦ㄧ嚎鎺ㄧ悊锛堝惈椹荤暀鏃堕棿锛?|
| **杞集鍒嗙被鍑嗙‘鐜?* | > 95% | 鍦ㄧ嚎鎺ㄧ悊 |

---

## 涓嬩竴姝?
1. **闂幆楠岃瘉**锛氳繍琛屽畬鏁?0s浠跨湡锛屽姣旀湁/鏃燝RU鐨凪PC鎬ц兘
2. **鍘嬪姏娴嬭瘯**锛氭祴璇曟瀬绔伐鍐碉紙杩炵画鍧″害銆佹€ヨ浆寮?棰犵案锛?3. **鍙傛暟璋冧紭**锛氳皟鏁碦hoFilter鐨則au銆丟RU椹荤暀鏃堕棿
4. **纭欢閮ㄧ讲**锛氬闇€瑕侊紝鎵ц浠ｇ爜鐢熸垚浼樺寲

---

## 鍙傝€冩枃妗?
- `func.md` - 鍔熻兘瀵艰埅锛圙RU妯″潡璇︾粏鎺ュ彛锛?- `README_LPVMPC_Usage.md` - LPV-MPC浣跨敤鎸囧崡
- `.cursor/rules/lpvmpc.mdc` - 璁捐瑙勮寖锛堢8鑺傦細AI宸ュ喌璇嗗埆锛?- `test_GRU_workflow.m` - GRU绂荤嚎娴嬭瘯绀轰緥

---

**鐗堟湰**锛歏1.0  
**鏈€鍚庢洿鏂?*锛?025-11-05  
**浣滆€?*锛歀PV-MPC Project


