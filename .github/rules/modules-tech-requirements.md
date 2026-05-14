# 妯″潡鎶€鏈姹傦紙LPV-MPC + GRU锛?
> 闈㈠悜褰撳墠浠撳簱鐜扮姸锛堟牴鐩綍涓轰富锛夛紝鍦ㄤ笉鏀瑰彉鐩綍缁撴瀯鐨勫墠鎻愪笅锛岀粏鍖栧悇妯″潡鐨勬帴鍙ｃ€佹暟鎹€佺畻娉曚笌楠岃瘉鏍囧噯锛屼究浜庡悗缁皟璇曚笌淇敼銆?
## 2. 鍙傝€冭矾寰勭敓鎴愶紙gen_agv_ref_path.m锛?
### 2.1 鍏叡鎺ュ彛涓庡弬鏁?```matlab
function ref = gen_agv_ref_path(path_type, params)
% path_type 鈭?{'straight','turn','straight_turn','slope','bumpy'}
% params: 缁撴瀯浣擄紙浼樺厛浣跨敤 parameters() 杈撳嚭锛夛紝鍏抽敭瀛楁锛?%   .Ts (绉?        閲囨牱鍛ㄦ湡锛堝繀闇€锛?%   .T_end (绉?     杞ㄨ抗鏃堕暱锛堥粯璁?20锛?%   .R (绫?         杞集鍗婂緞锛堥粯璁?10锛?%   .v0 (m/s)       鍒濋€熷害锛堥粯璁?1锛?%   .theta0 (rad)   鍧″害甯稿€硷紙榛樿 0锛?```
杈撳嚭 `ref` 瀛楁涓庡崟浣嶏細
- `t [N脳1] (s)`锛沗X_ref, Y_ref [N脳1] (m)`锛沗psi_ref [rad]`锛沗v_ref [m/s]`锛沗omega_ref [rad/s]`锛沗theta_ref [rad]`
- 璇樊鍙傝€冿細`e_y_ref, e_psi_ref, e_v_ref [N脳1]`锛堥€氬父涓?0锛屼緵 MPC 鐢級
- 璋冨害锛歚rho [N脳3] = [v_ref, omega_ref, theta_ref]`锛堢粡涓€闃朵綆閫?蟿鈮?.3鈥?.5 s锛?
### 2.2 鐢熸垚涓庝繚瀛?1) `t = (0:Ts:T_end)'`锛?) 鎸夌被鍨嬬敓鎴愯建杩癸紙鐩寸嚎/杞集/鐩?寮?鍧″害/棰犵案锛夛紱3) 璁＄畻 `psi_ref, v_ref, omega_ref`锛?) 璇樊鍙傝€冪疆 0锛?) 鏋勯€犲苟婊ゆ尝 `rho`锛?) 杈撳嚭 `ref`锛?7) 淇濆瓨鑷虫牴鐩綍 `path_<type>.mat`锛屽寘鍚?`{ref, meta}`锛坢eta: 鐢熸垚鏃堕棿銆佸弬鏁般€佺増鏈€佷綔鑰咃級銆?
鐩寸嚎锛歚X=v0*t, Y=0`锛涜浆寮細`X=R*sin(蠅t), Y=R*(1-cos(蠅t))`锛涚洿+寮細鍓?10 m 鐩寸嚎鍚庢帴鍦嗗姬锛涘潯搴︾洿绾匡細鐩寸嚎+甯稿€?`theta0`锛涢绨哥洿绾匡細鐩寸嚎+`0.2*sin(t)` 鎵板姩銆?
### 2.5 璋冨害鍙橀噺婊ゆ尝璇存槑
璋冨害鍘熷鍚戦噺锛歚rho_raw = [v_ref, omega_ref, theta_ref]`銆備竴闃朵綆閫氾細\(\tau \dot{\rho}_f + \rho_f = \rho_{raw}\)銆傜鏁ｅ疄鐜帮細
```matlab
alpha = Ts/(tau+Ts);    % tau鈮?.3鈥?.5 s
rho_f(k,:) = rho_f(k-1,:) + alpha*(rho_raw(k,:) - rho_f(k-1,:));
```
褰掍竴鍖栵細`rho_n = (rho_f - rho_min)./(rho_max - rho_min)`骞惰鍓埌 `[0,1]`銆俙rho_min, rho_max` 鐢辩綉鏍?`V_grid,W_grid,T_grid` 鏈€鍊肩‘瀹氥€?
### 2.3 Simulink 瀵规帴锛團rom Workspace锛?- 璺緞鍏ㄥ眬鍙傝€冿紙鐢ㄤ簬蹇呰鐨勫彲瑙嗗寲/澶栭儴妯″潡锛夛細`[X Y psi v omega]` 鍏?5 璺€?- MPC 璇樊鍙傝€冪鍙ｅ疄闄呬负 4脳1锛屽搴?`[e_y,e_psi,e_v,e_omega]`锛屽父鐢ㄩ浂鍚戦噺鎴栬宸洰鏍囥€?- `ref_ts`: `time=t`, `signals.values` 鎸夌鍙ｅ昂瀵哥粍缁囷紱鑻ョ粰璇樊鍙傝€冨垯浠呮彁渚?4 鍒椼€?- 鍙洿鎺ュ皢 `ref` 瀵煎嚭鎴栫敓鎴?`ref_ts` 杈撳叆 `LPVMPC_AGV_simulink._GRU.slx`锛涚鍙ｅ昂瀵镐互妯″瀷涓哄噯銆?
### 2.4 楠屾敹涓庤嚜妫€
- 鑴氭湰锛歚test_gen_paths.m` 璺戦€氾紱
- 浜х墿锛氭洿鏂?瑕嗙洊鏍圭洰褰?`path_*.mat`锛?- 缁村害锛歚numel(t)` 涓€鑷达紝鏃?NaN/Inf锛沗rho` 缁忚繃婊ゆ尝銆?
---

## 3. 鍏稿瀷鐐圭嚎鎬у寲锛坙in_agv_grid.m / lin_agv_at_point.m锛?
### 3.1 鎺ュ彛涓庨粯璁ゅ弬鏁?```matlab
function db = lin_agv_grid(params, grid, opts)
% params: parameters() 缁撴瀯浣擄紙鐗╃悊/杞儙/閲囨牱绛夛級锛?% grid  : struct锛屽瓧娈?V_grid(Nv脳1), W_grid(Nw脳1), T_grid(Nt脳1)  % 蟻=[v,蠅,胃]
% opts  : .coord='path', .disc='zoh'|'foh', .keep_E=true,
%         .export_mat='plant_grid.mat'  % 鏍圭洰褰曪紝娌跨敤鐜版湁浜х墿鍛藉悕
```
榛樿绾﹀畾锛?- 宸ヤ綔鐐?`蟻*=[v*, 蠅*, 胃*]`锛屾洸鐜?`魏*=蠅*/max(v*,1e-3)`锛岃宸负 0锛?- 鐘舵€?`x=[e_y,e_psi,e_v,e_omega]^T (nx=4)`锛涜緭鍏?`u=[F_cmd,omega_cmd]^T (nu=2)`锛涜緭鍑?`y=[e_y,e_psi,e_v,e_omega]^T (ny=4)`锛涙壈鍔?`d=[theta]^T (nd=1)` 杩涘叆 `E(蟻)`锛堢旱鍚戯級銆?
### 3.2 鏁板涓庤繎浼?- 绾靛悜锛歚F_long = F_cmd - F_roll - F_aero(v) - m g sin(theta)`锛?- 妯悜锛氬皬瑙掍晶鍋忕嚎鎬?`F_y 鈮?C_alpha路alpha`锛?- 闈炵嚎鎬у紑鍏筹細鍦ㄥ伐浣滅偣闄勮繎绛夋晥绾挎€у寲锛岄伩鍏?A/B 鍑虹幇绂绘暎鍒囨崲銆?
### 3.3 绂绘暎鍖栦笌瀵煎嚭
- `(Ac,Bc,Cc,Dc,Ec) 鈫?sysd=c2d(ss(Ac,Bc,Cc,Dc),Ts,opts.disc)`锛?- 琛ㄧ粨鏋勶細`db.grid.(V/W/T), db.Ts, db.A/B/C/D/E(i,j,k,:,:)`锛?- 瀵煎嚭锛歚save(opts.export_mat,'-struct','db')`锛堟牴鐩綍 `plant_grid.mat`锛夈€?
### 3.4 楠岃瘉涓庡洖褰?- 鏋佺偣浣嶄簬鍗曚綅鍦嗗唴鎴栧彲琚?MPC 绋冲畾锛?- `C` 涓庤緭鍑洪€夋嫨涓€鑷达紱
- `v鈫?, 蠅鈫?, |胃|鈫抦ax` 鏁板€肩ǔ瀹氾紱
- 1鈥? 姝ラ娴嬩笌楂樹繚鐪?Plant 瀵规瘮璇樊 鈮?5%锛?- 蹇€熸鏌ワ細鑻ュ瓨鍦?`lin_agv_db.mat`/`plant_grid_test.mat`锛岀敤浠ュ姣旂淮搴︿笌閲囨牱鏃堕棿涓€鑷存€с€?
鏃ュ織寤鸿锛歚lin_log(i,j,k).rho=[v;蠅;胃]; lin_log(i,j,k).eig=eig(A);` 鐢ㄤ簬鍚庣画绋冲畾鎬х瓫閫夈€?
### 3.5 澶辫触涓庡洖閫€
- 鑻ユ煇宸ヤ綔鐐圭嚎鎬у寲缁撴灉鍚?NaN/Inf锛氳褰曞苟璺宠繃璇ョ偣锛涙彃鍊兼椂鑷姩鐢辩浉閭荤偣骞虫粦琛ュ伩銆?- 鑻ユ瀬鐐规ā鍊兼渶澶?`>1.05`锛氬彲鍋氳氨缂╂斁锛歚A = A * (0.99/max_abs_eig)`锛堜繚瀹堜慨姝ｏ級銆?- 鑻?E(蟻) 缁村害涓嶄竴鑷达細鎶涘嚭閿欒鑰岄潪闈欓粯缁х画銆?
---

## 4. 鑷€傚簲 MPC锛坢pc_setup_single_interp.m / mpc_update_from_rho.m锛?
### 4.1 鎺у埗鍣ㄥ垱寤烘帴鍙?```matlab
function ctrl = mpc_setup_single_interp(db, opts)
% 杈撳叆锛歞b锛堢嚎鎬у寲搴擄級锛宱pts锛圢p,Nc,Q,R,dR,绾︽潫銆佽蒋绾︽潫鈥︼級
% 娴佺▼锛氶€?蟻 涓績鐐瑰熀鍑嗘ā鍨?鈫?mpc(ss(...)) 鈫?璁剧疆 Weights/Constraints
% 杈撳嚭锛歝trl 缁撴瀯锛屽惈 mpcobj 涓庯紙鍙€夛級鏉冮噸/绾︽潫鏄犲皠 maps
```

### 4.2 鍦ㄧ嚎鎻掑€间笌妯″瀷鏇存柊鎺ュ彛
```matlab
function upd = mpc_update_from_rho(rho, db, maps)
% rho=[v;omega;theta]锛堟湁绗﹀彿锛屽墠缃竴闃舵护娉?蟿鈮?.3鈥?.5 s锛?% 姝ラ锛毾?褰掍竴鍖?鈫?瑙掔偣涓庢潈閲?鈫?A..E 涓夌嚎鎬ф彃鍊?鈫?锛堝彲閫夛級Q/R/绾︽潫鏄犲皠
% 杩斿洖锛歶pd.A,B,C,D,E 鍙婏紙鍙€夛級鏉冮噸/绾︽潫鏇存柊椤?```

### 4.3 Simulink 鎺ョ嚎锛圓daptive MPC锛?- 娴嬮噺杈撳嚭 mo锛歚[e_y,e_psi,e_v,e_omega]`锛?脳1锛夈€?- 鍙傝€?ref锛氬疄闄呬负 4脳1 闆跺悜閲忥紙璇樊瓒嬮浂锛夋垨璇樊鐩爣 `[e_y_ref,e_psi_ref,e_v_ref,e_omega_ref]`銆?- 娴嬮噺鎵板姩 md锛歚theta_hat`锛堝鍚敤 E(蟻)锛夈€?- Scheduling锛歚rho_f=[v_f;蠅_f;胃_f]`锛堜竴闃舵护娉㈠悗锛夈€?- 鑷畾涔夋洿鏂板嚱鏁板簲鐢?`upd.A..E`锛涙潈閲?绾︽潫鍙敱澶栭儴绔彛鎴栧洖璋冭鐩栥€?
### 4.4 璁捐榛樿鍊间笌瀹夊叏瑁佸壀
- 棰勬祴/鎺у埗鍩燂細`Np鈮?.0鈥?.0 s`锛宍Nc鈮?.5鈥?.0 s`锛?- 鏉冮噸锛歚Q=diag([3,8,1,1])`锛宍R=diag([1e-3,1e-3])`锛宍dR=diag([1e-2,1e-2])`锛?- 绾︽潫绀轰緥锛歚F鈭圼-Fmax,Fmax]`锛宍蠅鈭圼-0.6,0.6]`锛宍|螖F|鈮?00 N/姝锛宍|螖蠅|鈮?.4 rad/s/姝锛?- 灏忛噺淇濇姢锛歚v_sat=max(v,1e-3)`锛涙墍鏈夋潈閲?绾︽潫鍋氳竟鐣岃鍓槻鏁板€煎彂鏁ｃ€?
### 4.5 楠岃瘉娓呭崟
- 鍥哄畾 蟻 鍦ㄨ鐐瑰闂幆鍙ǔ瀹氾紱
- `straight鈫抰urn`锛圫 鏇茬嚎鈮? s锛変笌 `bumpy`锛埼?姝ｅ鸡锛夊満鏅垏鎹㈠钩婊戯紱
- 璁板綍 `rho, solve_time, slack, status`锛汸95 姹傝В鏃堕棿婊¤冻鐩爣銆?澶辫触鍏滃簳锛氭彃鍊煎悗鑻?A/B/C/D 浠绘剰鍑虹幇 NaN/Inf 鈫?浣跨敤涓婁竴鍛ㄦ湡棰勬祴妯″瀷骞堕€掑澶辫触璁℃暟锛涜繛缁?鈮? 娆¤繘鍏ュ畨鍏ㄦā寮忥紙杈撳嚭淇濇寔鎴栭檺骞咃級銆?
### 4.6 浠ｄ环鍑芥暟涓?API 鏄犲皠
$$
J = \sum_{i=1}^{N_p} (y_{k+i|k}-r_{k+i})^\top Q (y_{k+i|k}-r_{k+i})
 + \sum_{i=0}^{N_c-1} \Delta u_{k+i|k}^\top R_\Delta \Delta u_{k+i|k}
 + \sum_{i=0}^{N_c-1} u_{k+i|k}^\top R u_{k+i|k}
 + \lambda_s \sum_{i=1}^{N_p} \|\epsilon_{k+i}\|_1
 + (y_{k+N_p|k})^\top P y_{k+N_p|k}
$$
```matlab
mpcobj.Weights.OutputVariables = [q_y, q_psi, q_v, q_omega];
mpcobj.Weights.ManipulatedVariables = [r_F, r_omega];
mpcobj.Weights.ManipulatedVariablesRate = [r_dF, r_domega];
% MV/OV 涓婁笅鐣屼笌杞害鏉燂紙绀轰緥锛屾寜椤圭洰鐜板€兼浛鎹級
```

### 4.7 涓夌嚎鎬ф彃鍊兼潈閲?褰掍竴鍖栧潗鏍?`(尉,畏,味)鈭圼0,1]^3` 鍏鐐癸細
```
w000=(1-尉)*(1-畏)*(1-味)
w100=尉*(1-畏)*(1-味)
w010=(1-尉)*畏*(1-味)
w110=尉*畏*(1-味)
w001=(1-尉)*(1-畏)*味
w101=尉*(1-畏)*味
w011=(1-尉)*畏*味
w111=尉*畏*味
```
鎻掑€硷細`A = 危 w_ijk*A_ijk`锛圔,C,D,E 鍚岀悊锛夈€傛潈閲嶅仛锛歚w=abs(w); w=w/sum(w)` 闃插井璐熸紓绉汇€?
### 4.8 RhoFilter 涓庨┗鐣?婊ゆ尝锛歚alpha=Ts/(tau+Ts)`锛涢┗鐣欏垽瀹氾細鑻?`|rho_raw-rho_f|/max(|rho_raw|,1e-6)<1e-3` 杩炵画 鈮? 姝?鈫?鍙檷浣庢洿鏂伴鐜囥€?鏈€灏忛┗鐣欐椂闂?`T_stay鈮?.2鈥?.3 s` 閬垮厤鏇茬巼蹇€熼棯鍔ㄣ€?
---

## 6. 鍦ㄧ嚎鎺у埗涓庝豢鐪燂紙LPVMPC_AGV_simulink._GRU.slx锛?- 鍙傝€冧俊鍙凤細`ref=[X Y psi v omega]`锛堟垨璇樊鍙傝€冿紝渚濇ā鍨嬮厤缃級锛?- 鎵板姩锛歚md=theta_ground`锛堝潯搴︼級锛?- 鏃ュ織锛氭瘡姝ヨ褰?`rho, slack, solve_time, status`锛?- 鑷鑴氭湰锛歚test_lpvmpc_workflow.m`銆?### 6.1 瀹夊叏妯″紡
- MPC 姹傝В澶辫触鎴?`solve_time_ms>10` 鈫?浣跨敤 `u_prev` 骞舵爣璁?`status='fallback'`锛涜繛缁け璐?鈮? 娆?鈫?杩涘叆闄嶇骇锛歚u=[0;0]`銆?### 6.2 鏃ュ織瀛楁寤鸿
`t, rho_f, u_cmd, u_prev, solve_time_ms, status, slack, e_y, e_psi, e_v, e_omega`銆?
---

## 7. 璐濆彾鏂紭鍖栵紙Bayesian_Optimization.m / Cost_Function.m锛?
### 7.1 璇勪及鍑芥暟缁嗗寲
- 杈撳叆锛歚params`锛坄parameters()` 缁撴灉锛夈€乣db`锛堝彲涓虹┖鍒欏唴閮ㄦ瀯寤?3脳3脳3 榛樿缃戞牸锛夈€乣cfg`锛堟潈閲?鑼冨洿/婊ゆ尝/缃氬€?ctrl/maps锛夈€乣scenes`锛堥粯璁ゆ潈閲嶏細turn 0.35, slope 0.30, straight_turn 0.20, bumpy 0.10, straight 0.05锛夈€?- 娴佺▼锛氭瘡 `Ts` 璁＄畻璇樊 鈫?鏋勯€犲苟婊ゆ尝 `rho`锛埾?0.4锛夆啋 `mpc_update_from_rho` 鈫?鏇存柊 `MPCobj` 鈫?`mpcmoveAdaptive` 鈫?`state_eq_ref` 鎺ㄨ繘 鈫?璁板綍鎸囨爣锛?- 澶辫触鍗宠繑鍥?`1e6`锛涘睆钄芥帶鍒跺彴杈撳嚭锛坄evalc`锛夈€?
### 7.2 浼樺寲鑴氭湰缁嗗寲
- 鍙橀噺鑼冨洿涓庡舰鍙傛槧灏勬寜鐜版湁瀹炵幇锛堣浠撳簱鑴氭湰锛夛紱
- 璇勪及 鈮?60 娆″缓璁紱鍗曠嚎绋嬶紱
- 浜х墿锛氭牴鐩綍 `maps_best.mat`锛堝惈鑼冨洿/褰㈠弬銆乺ho_min/max銆乼imestamp銆乿ersion锛夛紝鍙€?`bo_report_*.mat`, `bo_history_*.mat`銆?#### 7.2.1 澶辫触澶勭悊
- 鍗曞満鏅け璐ワ紙NaN/Inf / mpc 澶辫触锛夆啋 璇ュ満鏅唬浠疯楂樼綒锛堝 2e6锛夛紱鑻?鈮?0% 鍦烘櫙澶辫触 鈫?鎻愬墠缁堟璇勪及杩斿洖 1e6銆?- 鎺у埗鍣ㄦ瀯寤哄紓甯革細鐩存帴杩斿洖 5e6 骞惰褰?`report.fail_reason`銆?#### 7.2.2 鎶ュ憡瀛楁寤鸿
`report.scenes(s).RMSE, RMS_du, violations, solve_time_mean, solve_time_max, status_flags`锛涙眹鎬伙細`report.J_total, J_components, failure_count`銆?
### 7.3 杩愯鍛戒护锛圵indows锛?```cmd
matlab -batch "run('start_bayesian.m')"
```
### 7.4 鐗堟湰鍖?- 淇濆瓨鏃х増鏈細`maps_best_<timestamp>.mat`锛?- 璁板綍 `meta.seed, meta.max_evals, meta.selection`锛?- 鑻?`J` 鏀瑰杽 <2% 鍙€夋嫨涓嶈鐩栦富鏂囦欢鍑忓皯 churn銆?
---

## 8. AI 宸ュ喌璇嗗埆锛圙RU_* 绯诲垪锛?
### 8.1 鏁版嵁鐢熸垚涓庨澶勭悊
- 鐢熸垚锛歚GRU_gen_train_data.m`锛堝彲璋冪敤 `GRU_DataGen.slx`锛夛紝鍦烘櫙浣跨敤 `gen_agv_ref_path`锛?- 棰勫鐞嗭細`GRU_prepare_dataset.m` 杈撳嚭 `GRU_dataset_processed.mat`锛堝惈 `X, y_main, y_turn, y_theta, mask_theta, scaler, feat_names`锛夈€?#### 8.1.1 鏁版嵁璐ㄩ噺
- NaN 姣斾緥 >1%锛氬簭鍒楀墧闄ゆ垨鎻掑€硷紱鏋佺鍊?|z|>6 瑁佸壀鍒?卤6锛?- 绫讳笉骞宠　锛氶噰鐢ㄧ被鏉冮噸鎴栬繃閲囨牱灏戞暟绫伙紙stall/slip锛夈€?
### 8.2 璁粌涓庢帹鐞?- 璁粌锛歚GRU_train.m` 鈫?浜х墿 `GRU_model.mat`, `GRU_scaler.mat`, `GRU_meta.mat`锛?- 鎺ㄧ悊锛歚GRU_infer.m`锛堝簭鍒楄緭鍏モ啋涓夊ご杈撳嚭锛夛紱鍦ㄧ嚎灏佽锛歚GRU_state_classifier.m`锛堥┗鐣?浣庨€?绋冲仴锛夈€?#### 8.2.1 璁粌寰幆绀轰緥
```matlab
for epoch = 1:opts.epochs
	[loss_main, loss_turn, loss_theta] = forward_pass(batch,...);
	loss = loss_main + opts.lambda_turn*loss_turn + opts.lambda_theta*loss_theta;
	backprop(loss);
	if mod(epoch,5)==0, evaluate_val(); end
	if early_stop_trigger, break; end
end
```
#### 8.2.2 浜х墿淇濆瓨
- `GRU_model.mat`: `net`, 鏈€浼?epoch, 鎸囨爣鎽樿锛?- `GRU_meta.mat`: `feat_names, class_weights, seq_len, stride, Ts, commit_SHA`锛堝彲閫夛級锛?- `GRU_scaler.mat`: `mean, std`銆?
### 8.3 璇勪及涓庣洰鏍?- 鎸囨爣锛氫富鍒嗙被 Acc/macro-F1锛岃浆寮?Acc锛屽潯搴?MAE/RMSE锛坉eg锛夛紱
- 鏃跺欢锛歁ATLAB 鎺ㄧ悊鍧囧€?P95 < 1 ms/姝ワ紱
- 鍘嬫祴锛氫綆 渭銆佸己鍣０銆侀暱鍧°€佹€ヨ浆+棰犵案銆佽繛缁墦婊戯紱
- 鑷锛歚test_GRU_workflow.m`锛涙棩蹇楄緭鍑鸿嚦 `GRU_logs/`銆?#### 8.3.1 鎸囨爣闃堝€煎缓璁?- `macro_F1_main >= 0.85`锛沗Acc_turn >= 0.85`锛沗MAE_theta_deg <= 1.5`锛?- 鎺ㄧ悊鏃跺欢锛歮ean <0.6 ms, P95 <1.0 ms锛?- 浣庝簬闃堝€奸渶鍦?`change.md` 璇存槑鍘熷洜涓庢敼杩涜鍒掋€?
---

## 9. 鍙樻洿鍚屾涓庢枃妗?- 淇敼/鏂板涓婅堪浠讳竴鑴氭湰鎴栨帴鍙ｏ紝椤诲悓姝ユ洿鏂版牴鐩綍 `func.md`锛堟潯鐩惈锛氳矾寰?鑱岃矗/绛惧悕/杈撳叆杈撳嚭/鍗曚綅/澶囨敞锛夛紱
- 鍦?`change.md` 鐣欑棔锛圕ontext/Changes/Impact/Verification/Artifacts/Migration/Refs锛夈€?### 9.1 func.md 鏉＄洰寤鸿瀛楁
- `deps`锛堜緷璧栬剼鏈垨 .mat锛夈€乣interfaces`锛堝嚱鏁扮鍚嶏級銆乣units`锛堝叧閿崟浣嶏級銆乣updated_at`銆乣status`(`stable|experimental|deprecated`)銆?### 9.2 CI 妫€鏌ヨ鐐?- 鏂板 `.m` 鏈洿鏂?`func.md` 鈫?闃绘柇锛?- 鎺ュ彛/缁村害鍙樺寲鏃?`BREAKING CHANGE` 澹版槑 鈫?闃绘柇锛?- GRU 鎴?MPC 鍏抽敭鎸囨爣浣庝簬闃堝€间笖鏃犺В閲?鈫?闃绘柇锛?- 鎻愪氦姝ｆ枃缂哄皯 `Context` 鎴?`Changes` 娈?鈫?璀﹀憡鎴栭樆鏂紙鎸夌瓥鐣ワ級銆?
