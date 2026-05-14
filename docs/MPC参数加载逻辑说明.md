# LPVMPC_AGV_simulink._GRU.slx 鎺у埗鍣ㄥ弬鏁板姞杞介€昏緫璇存槑

## 姒傝堪

鏈枃妗ｈ缁嗚鏄?**LPVMPC_AGV_simulink._GRU.slx** 杩愯鏃讹紝MPC 鎺у埗鍣ㄥ弬鏁扮殑**瀹屾暣鍔犺浇閾捐矾**锛屽寘鎷細
- 鍒濆鍖栭樁娈碉紙PreLoadFcn锛?- 鎺у埗鍣ㄥ垱寤猴紙mpc_setup_single_interp锛?- 鍦ㄧ嚎鍙傛暟鏇存柊锛坢pc_update_from_rho锛?
---

## 涓€銆佸弬鏁板姞杞芥祦绋嬫€昏

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                   Simulink 妯″瀷鍚姩                            鈹?鈹?                   PreLoadFcn 鎵ц                             鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ0锛氬熀纭€鍙傛暟鍔犺浇     鈹?    鈹? parameters.m           鈹?    鈹? 鈫?params 缁撴瀯浣?        鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ1锛歀PV 鏁版嵁搴撳姞杞?  鈹?    鈹? lin_agv_db.mat         鈹?    鈹? 鈫?db_rt 缁撴瀯浣?         鈹?    鈹? (A/B/C/D/E 缃戞牸琛?     鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ2锛氬垱寤烘€荤嚎绫诲瀷     鈹?    鈹? MPCPlantBus            鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ3锛氬姞杞戒紭鍖栧弬鏁?    鈹?    鈹? maps_best.mat          鈹?    鈹? 鈫?maps_best 缁撴瀯浣?     鈹?    鈹? (Q/R/dR鑼冨洿銆佺害鏉熺缉鏀? 鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ4锛氬垱寤?鍔犺浇 MPC 鎺у埗鍣?                鈹?    鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?    鈹? 鈹?浼樺厛锛氬姞杞?ctrl.mat                   鈹? 鈹?    鈹? 鈹?鍥為€€锛氳皟鐢?mpc_setup_single_interp    鈹? 鈹?    鈹? 鈹?      浣跨敤 maps_best 涓殑鏉冮噸         鈹? 鈹?    鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?    鈹? 鈫?ctrl 缁撴瀯浣?                             鈹?    鈹?   - ctrl.mpcobj (MATLAB MPC瀵硅薄)          鈹?    鈹?   - ctrl.maps   (鏉冮噸/绾︽潫鏄犲皠琛?          鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹? 姝ラ5锛氬彉閲忓啓鍏ュ伐浣滃尯   鈹?    鈹? base + Model Workspace 鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?                 鈻?       鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹? 妯″瀷浠跨湡杩愯    鈹?       鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                 鈹?       鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?鍦ㄧ嚎鍙傛暟鏇存柊锛堟瘡涓豢鐪熸锛?          鈹?       鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?       鈹?鈹?Adaptive MPC 鑷畾涔夋洿鏂板嚱鏁?     鈹?鈹?       鈹?鈹?鈫?mpc_update_from_rho(蟻,db,maps)鈹?鈹?       鈹?鈹?  杈撳叆锛毾?[v;蠅;胃]锛堟护娉㈠悗锛?     鈹?鈹?       鈹?鈹?  杈撳嚭锛欰/B/C/D/E + Q/R/dR       鈹?鈹?       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?       鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## 浜屻€丳reLoadFcn 璇︾粏姝ラ

### 姝ラ 0锛氬姞杞藉熀纭€鍙傛暟 `parameters.m`

**鐩殑**锛氬姞杞借溅杈嗙墿鐞嗗弬鏁般€佹帶鍒跺弬鏁般€侀噰鏍峰懆鏈熺瓑銆?
**鎵ц浠ｇ爜**锛?```matlab
params = parameters();
```

**鍏抽敭杈撳嚭鍙橀噺**锛?- `params.Ts`锛氶噰鏍峰懆鏈燂紙0.05 s锛?- `params.mass`锛氳溅杈嗚川閲忥紙100 kg锛?- `params.L`锛氳酱璺濓紙2.0 m锛?- `params.gravity`锛氶噸鍔涘姞閫熷害锛?.81 m/s虏锛?- 鍏朵粬锛氳疆鑳庛€佺數鏈恒€佹墽琛屽櫒銆侀樆鍔涘弬鏁扮瓑

**鍐欏叆浣嶇疆**锛?- Base Workspace锛歚params`
- Model Workspace锛歚params`, `ff_rt`锛堝墠棣堣绠楃敤锛夛紝`v_ff_nom`

---

### 姝ラ 1锛氬姞杞?LPV 鏁版嵁搴?
**鐩殑**锛氬姞杞界鏁ｆ椂闂寸嚎鎬у寲妯″瀷缃戞牸琛紙A/B/C/D/E 鐭╅樀锛夈€?
**鎵ц浠ｇ爜**锛?```matlab
% 灏濊瘯鍔犺浇锛堜紭鍏堢骇閫掑噺锛?dbFiles = {'lin_agv_db.mat','plant_grid_test.mat','plant_grid.mat'};
```

**鏁版嵁缁撴瀯妫€娴?*锛?- **鎯呭喌1锛堟爣鍑嗘牸寮忥級**锛歚S.db.A/B/C/D/E`锛堢粨鏋勪綋宓屽锛?- **鎯呭喌2锛堥《灞傛牸寮忥級**锛歚S.A/B/C/D/E`锛堢洿鎺ラ《灞傦級

**鍏抽敭杈撳嚭鍙橀噺**锛?- `db_rt.A`锛氱姸鎬佺煩闃电綉鏍?`[Nv脳Nw脳Nt脳4脳4]`
- `db_rt.B`锛氳緭鍏ョ煩闃电綉鏍?`[Nv脳Nw脳Nt脳4脳2]`锛圡V閮ㄥ垎锛?- `db_rt.C`锛氳緭鍑虹煩闃电綉鏍?`[Nv脳Nw脳Nt脳4脳4]`
- `db_rt.D`锛氱洿閫氱煩闃电綉鏍?`[Nv脳Nw脳Nt脳4脳2]`
- `db_rt.E`锛氭壈鍔ㄧ煩闃电綉鏍?`[Nv脳Nw脳Nt脳4脳1]`锛圡D閮ㄥ垎锛屽潯搴﹁胃锛?- `db_rt.grid`锛氱綉鏍煎畾涔?`{V, W, T}`锛堥€熷害銆佽閫熷害銆佸潯搴﹁锛?- `db_rt.Ts`锛氶噰鏍峰懆鏈燂紙涓?params.Ts 涓€鑷达級
- 缁村害淇℃伅锛歚nx=4, nu=2, ny=4, nd=1, Nv, Nw, Nt`

**缃戞牸鑼冨洿绀轰緥**锛?脳3脳3 榛樿缃戞牸锛夛細
- `V_grid = [0.8, 1.0, 1.2]` m/s
- `W_grid = [-0.2, 0.0, 0.2]` rad/s锛堟湁绗﹀彿锛岃礋涓哄彸杞紝姝ｄ负宸﹁浆锛?- `T_grid = [-0.2, 0.0, 0.2]` rad锛堝潯搴﹁锛屸増卤11.5掳锛?
**鍐欏叆浣嶇疆**锛?- Base Workspace锛歚db_rt`
- Model Workspace锛歚db_rt`

---

### 姝ラ 2锛氬垱寤?MPCPlantBus

**鐩殑**锛氫负 Adaptive MPC 鍧楀垱寤烘€荤嚎绫诲瀷瀹氫箟锛堢敤浜庢ā鍨嬬鍙ｏ級銆?
**鎵ц浠ｇ爜**锛?```matlab
nu_md = nu + nd;  % 3 (2 MV + 1 MD)
samplePlant = struct( ...
    'A',  zeros(nx, nx), ...     % 4x4
    'B',  zeros(nx, nu_md), ...  % 4x3锛堝惈MD鍒楋級
    'C',  zeros(ny, nx), ...     % 4x4
    'D',  zeros(ny, nu_md), ...  % 4x3
    'U',  zeros(nu_md, 1), ...   % 3x1锛? MV + 1 MD锛?    'X',  zeros(nx, 1), ...
    'Y',  zeros(ny, 1), ...
    'DX', zeros(nx, 1), ...
    'Ts', Ts );
info = Simulink.Bus.createObject(samplePlant);
```

**鍏抽敭杈撳嚭**锛?- `MPCPlantBus`锛歋imulink 鎬荤嚎绫诲瀷
- `plant_ic`锛氬垵濮嬫牱鏈粨鏋勪綋锛堢敤浜庡潡鍒濆鍖栵級

**娉ㄦ剰浜嬮」**锛?- `B` 鐭╅樀鍒楁暟 = `nu_md = 3`锛?涓狹V + 1涓狹D锛?- 鍦ㄧ嚎鏇存柊鏃讹紝绗?鍒楀皢濉厖 `E(蟻)`锛堝潯搴︽壈鍔ㄥ奖鍝嶏級

---

### 姝ラ 3锛氬姞杞戒紭鍖栧弬鏁?`maps_best.mat`

**鐩殑**锛氬姞杞借礉鍙舵柉浼樺寲寰楀埌鐨?*鏈€浼樻潈閲嶅拰绾︽潫鍙傛暟**銆?
**鎵ц浠ｇ爜**锛?```matlab
if exist('maps_best.mat','file')
    Tm = load('maps_best.mat');
    maps_best = Tm.maps_best;
end
```

**maps_best 缁撴瀯浣撳唴瀹?*锛?
#### 3.1 鏉冮噸鑼冨洿
- `Q_range`锛歚[2脳4]` 鐭╅樀锛堣1=鏈€灏忓€硷紝琛?=鏈€澶у€硷級
  - 鍒楅『搴忥細`[q_y, q_psi, q_v, q_omega]`
  - 绀轰緥锛歚Q_range = [15.0, 20.0, 3.5, 1.2; 22.0, 28.0, 5.5, 2.5]`
- `R_range`锛歚[2脳2]` 鐭╅樀
  - 鍒楅『搴忥細`[r_F, r_omega]`
  - 绀轰緥锛歚R_range = [0.0008, 0.0006; 0.0025, 0.0018]`
- `dR_range`锛歚[2脳2]` 鐭╅樀
  - 鍒楅『搴忥細`[r_dF, r_domega]`
  - 绀轰緥锛歚dR_range = [0.008, 0.006; 0.018, 0.015]`

#### 3.2 褰㈢姸鍙傛暟锛堟潈閲嶆彃鍊煎舰鐘舵帶鍒讹級
- `alpha_Q`锛歚[1脳4]`锛孮鍚勫垎閲忕殑涓嬮槇鍊硷紙褰掍竴鍖栧煙[0,1]锛?- `beta_Q`锛歚[1脳4]`锛孮鍚勫垎閲忕殑涓婇槇鍊硷紙婊¤冻 `alpha 鈮?beta`锛?- `alpha_R`銆乣beta_R`锛歚[1脳2]`锛堝悓涓婏紝閽堝R锛?- `alpha_dR`銆乣beta_dR`锛歚[1脳2]`锛堝悓涓婏紝閽堝dR锛?
**浣滅敤**锛氬湪 `[alpha, beta]` 鍖洪棿鍐呯嚎鎬ц繃娓℃潈閲嶏紝鍖洪棿澶栧す绱с€?
#### 3.3 绾︽潫缂╂斁鍙傛暟
- `scale_umin_lo`锛歚[1脳2]`锛寍蠅|=0 鏃剁殑 `umin` 缂╂斁绯绘暟
- `scale_umin_hi`锛歚[1脳2]`锛寍蠅|=max 鏃剁殑 `umin` 缂╂斁绯绘暟
- `scale_umax_lo/hi`锛氬悓涓婏紙閽堝 `umax`锛?
**浣滅敤**锛氭牴鎹閫熷害澶у皬鍔ㄦ€佽皟鏁磋緭鍏ョ害鏉燂紙渚嬪杞集鏃舵斁瀹藉姏绾︽潫锛夈€?
#### 3.4 鍏朵粬鍙傛暟
- `rho_min`銆乣rho_max`锛氳皟搴﹀彉閲忚寖鍥?`[3脳1]`锛堜笌缃戞牸绔偣涓€鑷达級
- `timestamp`锛氱敓鎴愭椂闂存埑
- `version`锛氱増鏈彿
- `note`锛氬娉ㄨ鏄?
**鍐欏叆浣嶇疆**锛?- 浠呬繚瀛樺湪鍐呭瓨锛坄maps_best` 鍙橀噺锛夛紝涓嶇洿鎺ュ啓鍏?Base Workspace

---

### 姝ラ 4锛氬垱寤?鍔犺浇 MPC 鎺у埗鍣?
#### 4.1 浼樺厛灏濊瘯鍔犺浇 `ctrl.mat`

**鎵ц浠ｇ爜**锛?```matlab
if exist('ctrl.mat','file')
    Tc = load('ctrl.mat');
    if isfield(Tc,'ctrl')
        ctrl = Tc.ctrl;
        ctrl_source = 'ctrl.mat';
    end
end
```

**閫傜敤鍦烘櫙**锛?- 宸茬粡绂荤嚎鍒涘缓骞朵繚瀛樹簡鎺у埗鍣?- 閬垮厤姣忔杩愯閮介噸鏂板垱寤猴紙鑺傜渷鏃堕棿锛?
#### 4.2 鍥為€€锛氬垱寤烘柊鎺у埗鍣?
**鎵ц浠ｇ爜**锛?```matlab
if isempty(ctrl) && exist('mpc_setup_single_interp','file')==2
    % 纭畾鏉冮噸鍙傛暟
    if maps_loaded && isfield(maps_best,'Q_range')
        Q_base = mean(maps_best.Q_range, 1);  % 鍙栬寖鍥翠腑鐐?        R_base = mean(maps_best.R_range, 1);
        dR_base = mean(maps_best.dR_range, 1);
    else
        % 浣跨敤榛樿鏉冮噸
        Q_base = [3, 8, 1, 1];
        R_base = [1e-3, 1e-3];
        dR_base = [1e-2, 1e-2];
    end
    
    mpc_opts = struct('Np',30,'Nc',10, ...
        'Q', Q_base, 'R', R_base, 'dR', dR_base);
    
    ctrl = mpc_setup_single_interp(db_rt, mpc_opts);
end
```

**鍏抽敭鍐崇瓥閫昏緫**锛?1. **鑻ユ湁 maps_best**锛氫娇鐢ㄤ紭鍖栫殑鏉冮噸鑼冨洿涓偣浣滀负鍩哄噯
2. **鑻ユ棤 maps_best**锛氫娇鐢ㄧ‖缂栫爜榛樿鍊硷紙淇濆畧绛栫暐锛?
#### 4.3 澶嶅埗 maps_best 鍙傛暟鍒?ctrl.maps

**鎵ц浠ｇ爜**锛?```matlab
if maps_loaded
    fields = {'Q_range','R_range','dR_range', ...
        'alpha_Q','beta_Q','alpha_R','beta_R','alpha_dR','beta_dR', ...
        'scale_umin_lo','scale_umin_hi','scale_umax_lo','scale_umax_hi'};
    
    for i = 1:length(fields)
        if isfield(maps_best, fields{i})
            ctrl.maps.(fields{i}) = maps_best.(fields{i});
        end
    end
end
```

**浣滅敤**锛?- 灏嗚礉鍙舵柉浼樺寲寰楀埌鐨勫弬鏁拌鐩栨帶鍒跺櫒鐨勯粯璁ゆ槧灏勮〃
- `ctrl.maps` 灏嗗湪鍚庣画鍦ㄧ嚎鏇存柊鏃朵娇鐢?
**鍐欏叆浣嶇疆**锛?- Base Workspace锛歚ctrl`

---

### 姝ラ 5锛欸RU 妯″瀷鍔犺浇锛堟柊澧烇級

**鎵ц浠ｇ爜**锛?```matlab
S_gru = load('GRU_model.mat');
if isfield(S_gru, 'model')
    assignin('base', 'gru_model', S_gru.model);
end
```

**鍏抽敭杈撳嚭**锛?- `gru_model`锛欸RU宸ュ喌璇嗗埆妯″瀷锛堢敤浜庝及璁″潯搴﹁ `胃_hat`锛?
---

## 涓夈€佹帶鍒跺櫒鍒涘缓璇﹁В锛歚mpc_setup_single_interp.m`

### 3.1 鍑芥暟绛惧悕

```matlab
function ctrl = mpc_setup_single_interp(db, opts)
```

**杈撳叆**锛?- `db`锛歀PV鏁版嵁搴擄紙鏉ヨ嚜 PreLoadFcn 鐨?`db_rt`锛?- `opts`锛氳璁￠€夐」
  - `Np`, `Nc`锛氶娴?鎺у埗鏃跺煙锛堟鏁帮級
  - `Q`, `R`, `dR`锛氭潈閲嶅悜閲?  - `umin`, `umax`, `dumin`, `dumax`锛氱害鏉?  - `ymin`, `ymax`锛氳緭鍑虹害鏉?  - `soft_weight_pos`, `soft_weight_yaw`锛氳蒋绾︽潫鎯╃綒

**杈撳嚭**锛?- `ctrl`锛氭帶鍒跺櫒缁撴瀯浣?  - `ctrl.mpcobj`锛歁ATLAB MPC瀵硅薄
  - `ctrl.db`锛氭暟鎹簱寮曠敤
  - `ctrl.opts`锛氳璁￠€夐」
  - `ctrl.maps`锛氭潈閲?绾︽潫鏄犲皠琛?  - `ctrl.meta`锛氬厓鏁版嵁

---

### 3.2 榛樿鍙傛暟锛堣嫢 opts 鏈寚瀹氾級

#### 鏃跺煙
```matlab
Np = round(1.5 / Ts);  % 棰勬祴鏃跺煙 鈮?1.5s锛?0姝Ts=0.05s锛?Nc = round(0.5 / Ts);  % 鎺у埗鏃跺煙 鈮?0.5s锛?0姝ワ級
```

#### 鏉冮噸
```matlab
Q  = [3, 8, 1, 1];      % [q_y, q_psi, q_v, q_omega]
R  = [1e-3, 1e-3];      % [r_F, r_omega]
dR = [1e-2, 1e-2];      % [r_dF, r_domega]
```

**璇存槑**锛?- `q_psi = 8`锛氳埅鍚戣宸潈閲嶆渶楂橈紙杞悜绮惧害浼樺厛锛?- `q_y = 3`锛氭í鍚戜綅缃宸涔?- `q_v`, `q_omega = 1`锛氶€熷害/瑙掗€熷害璇樊鏉冮噸杈冧綆
- `R` 寰堝皬锛氬厑璁歌緝澶ф帶鍒惰緭鍏ワ紙閬垮厤淇濆畧锛?- `dR` 涓瓑锛氬钩婊戞€х害鏉熼€備腑

#### 绾︽潫
```matlab
umin = [-300; -0.6];       % [F_min(N), omega_min(rad/s)]
umax = [300; 0.6];
dumin = [-400; -0.4];      % [螖F_min(N/姝?, 螖蠅_min((rad/s)/姝?]
dumax = [400; 0.4];
ymin = [-1.0; -0.5; -0.5; -0.3];  % [e_y, e_psi, e_v, e_omega]
ymax = [1.0; 0.5; 0.5; 0.3];
```

**璇存槑**锛?- 杈撳叆绾︽潫锛氬姏 卤300N锛岃閫熷害 卤0.6 rad/s锛堚増34掳/s锛?- 閫熺巼绾︽潫锛氶槻姝㈡帶鍒堕噺绐佸彉
- 杈撳嚭绾︽潫锛氳蒋绾︽潫锛堝厑璁歌繚鍙嶏紝浣嗘儵缃氾級
  - `e_y` 卤1.0 m锛堟í鍚戣宸級
  - `e_psi` 卤0.5 rad锛堚増29掳锛岃埅鍚戣宸級
  - `e_v`, `e_omega`锛氬疄闄呮湭绾︽潫锛堣涓?`[-Inf, Inf]`锛?
#### 杞害鏉熸儵缃?```matlab
soft_weight_pos = 1e4;  % e_y 杞害鏉熸潈閲?soft_weight_yaw = 1e4;  % e_psi 杞害鏉熸潈閲?```

**浣滅敤**锛?- 杞害鏉熷厑璁镐复鏃惰繚鍙嶈緭鍑虹害鏉?- 杩濆弽鏃跺湪浠ｄ环鍑芥暟涓鍔犳儵缃氶」锛歚penalty = weight * |violation|`
- 鏉冮噸 1e4 鎰忓懗鐫€杩濆弽浠ｄ环寰堥珮锛屼絾涓嶄細瀵艰嚧闂涓嶅彲琛?
---

### 3.3 鍩哄噯妯″瀷閫夋嫨

**閫夋嫨绛栫暐**锛氫娇鐢ㄧ綉鏍间腑蹇冪偣浣滀负鍩哄噯妯″瀷銆?
**鎵ц浠ｇ爜**锛?```matlab
i_center = ceil(Nv / 2);
j_center = ceil(Nw / 2);
k_center = ceil(Nt / 2);

A0 = squeeze(db.A(i_center, j_center, k_center, :, :));
B0 = squeeze(db.B(i_center, j_center, k_center, :, :));
C0 = squeeze(db.C(i_center, j_center, k_center, :, :));
D0 = squeeze(db.D(i_center, j_center, k_center, :, :));
E0 = squeeze(db.E(i_center, j_center, k_center, :, :));
```

**绀轰緥**锛?脳3脳3缃戞牸锛夛細
- 閫夋嫨绱㈠紩 `[2, 2, 2]`锛屽搴?`蟻 = [1.0 m/s, 0.0 rad/s, 0.0 rad]`
- 鍗筹細涓€熺洿琛屻€佸钩鍦?
**鍘熷洜**锛?- 涓績鐐归€氬父浠ｈ〃鏈€甯歌鐨勫伐鍐?- 淇濊瘉鍩哄噯妯″瀷绋冲畾锛堟瀬绔伐鍐电偣鍙兘涓嶇ǔ瀹氾級

---

### 3.4 鍒涘缓 MPC 瀵硅薄

#### 鎵╁睍杈撳叆鐭╅樀锛堟坊鍔燤D閫氶亾鍗犱綅锛?
```matlab
if has_md
    B_aug = [B0, zeros(nx, 1)];  % [4脳3]锛岀3鍒椾负MD鍗犱綅
    D_aug = [D0, zeros(ny, 1)];  % [4脳3]
else
    B_aug = B0;
    D_aug = D0;
end

plant = ss(A0, B_aug, C0, D_aug, Ts);
```

**鍏抽敭鐐?*锛?- MPC 瀵硅薄鍒涘缓鏃堕渶瑕佸０鏄?**杈撳叆閫氶亾鏁?*
- 绗?鍒楀垵濮嬩负闆讹紙鍚嶄箟妯″瀷涓璏D鏃犲奖鍝嶏級
- **鍦ㄧ嚎鏇存柊鏃?*锛岀3鍒楀皢琚?`E(蟻)` 鏇挎崲

#### 璁剧疆杈撳叆鍒嗙粍

```matlab
plant = setmpcsignals(plant, 'MV', [1 2], 'MD', 3);
```

**浣滅敤**锛?- 閫氶亾1-2锛氭搷绾靛彉閲忥紙Manipulated Variables锛孧V锛?  - `F_cmd`锛堥┍鍔ㄥ姏锛?  - `omega_cmd`锛堣閫熷害鎸囦护锛?- 閫氶亾3锛氭祴閲忔壈鍔紙Measured Disturbance锛孧D锛?  - `theta`锛堝潯搴﹁锛岀敱GRU浼拌锛?
#### 鍒涘缓 MPC 瀵硅薄

```matlab
mpcobj = mpc(plant, Ts, opts.Np, opts.Nc);
```

**閰嶇疆鏉冮噸**锛?```matlab
mpcobj.Weights.OutputVariables = opts.Q;
mpcobj.Weights.ManipulatedVariables = opts.R;
mpcobj.Weights.ManipulatedVariablesRate = opts.dR;
```

**閰嶇疆绾︽潫**锛?```matlab
% 杈撳叆骞呭€肩害鏉燂紙浠匨V锛?for i = 1:nu  % nu=2
    mpcobj.MV(i).Min = opts.umin(i);
    mpcobj.MV(i).Max = opts.umax(i);
    mpcobj.MV(i).RateMin = opts.dumin(i);
    mpcobj.MV(i).RateMax = opts.dumax(i);
end

% 杈撳嚭杞害鏉燂紙e_y, e_psi锛?mpcobj.OV(1).Min = opts.ymin(1);
mpcobj.OV(1).Max = opts.ymax(1);
mpcobj.OV(1).MinECR = opts.soft_weight_pos;
mpcobj.OV(1).MaxECR = opts.soft_weight_pos;

mpcobj.OV(2).Min = opts.ymin(2);
mpcobj.OV(2).Max = opts.ymax(2);
mpcobj.OV(2).MinECR = opts.soft_weight_yaw;
mpcobj.OV(2).MaxECR = opts.soft_weight_yaw;

% e_v, e_omega 涓嶇害鏉?mpcobj.OV(3).Min = -Inf;
mpcobj.OV(3).Max = Inf;
mpcobj.OV(4).Min = -Inf;
mpcobj.OV(4).Max = Inf;
```

---

### 3.5 鏋勫缓鏉冮噸/绾︽潫鏄犲皠琛?`ctrl.maps`

**鐩殑**锛氫负鍦ㄧ嚎鍙傛暟鎻掑€兼彁渚涢厤缃€?
#### 璋冨害鍙橀噺鑼冨洿
```matlab
maps.rho_min = [db.grid.V(1); db.grid.W(1); db.grid.T(1)];
maps.rho_max = [db.grid.V(end); db.grid.W(end); db.grid.T(end)];
```

#### 鏉冮噸鎻掑€艰寖鍥?```matlab
maps.Q_range = [opts.Q * 0.5; opts.Q * 1.5];  % [2脳4]
maps.R_range = [opts.R * 0.5; opts.R * 1.5];  % [2脳2]
maps.dR_range = [opts.dR * 0.5; opts.dR * 1.5];  % [2脳2]
```

**璇存槑**锛?- 鍒濆鑼冨洿涓哄熀鍑嗘潈閲嶇殑 卤50%
- **鑻?PreLoadFcn 杞藉叆浜?maps_best**锛屽皢瑕嗙洊姝よ寖鍥?
#### 褰㈢姸鍙傛暟锛堥粯璁わ細绾挎€ф彃鍊硷級
```matlab
maps.alpha_Q = zeros(1,4);    % [0,0,0,0]
maps.beta_Q  = ones(1,4);     % [1,1,1,1]
maps.alpha_R = zeros(1,2);
maps.beta_R  = ones(1,2);
maps.alpha_dR = zeros(1,2);
maps.beta_dR  = ones(1,2);
```

**璇存槑**锛?- `alpha=0, beta=1` 琛ㄧず鍦?`[0,1]` 鍖洪棿鍐呯嚎鎬ф彃鍊?- 鍙€氳繃璐濆彾鏂紭鍖栬皟鏁?`alpha/beta` 瀹炵幇闈炵嚎鎬у舰鐘?
#### 绾︽潫缂╂斁鍙傛暟
```matlab
maps.scale_umin_lo = ones(1,2);
maps.scale_umin_hi = ones(1,2);
maps.scale_umax_lo = ones(1,2);
maps.scale_umax_hi = ones(1,2);
```

**璇存槑**锛?- 鍒濆涓?锛堜笉缂╂斁锛?- 鍙牴鎹?`|蠅|` 鍔ㄦ€佽皟鏁达紙渚嬪杞集鏃舵斁瀹藉姏绾︽潫锛?
#### 鍦烘櫙鑷€傚簲鏉冮噸璋冨害鍙傛暟锛堟柟妗圔锛屾柊澧烇級
```matlab
maps.omega_threshold = 0.15;    % 瑙掗€熷害闃堝€?[rad/s]
maps.q_y_gain_max = 1.8;        % 杞集鏃?q_y 鏈€澶у鐩?maps.transition_width = 0.05;   % 杩囨浮甯﹀搴?[rad/s]
```

**浣滅敤**锛堝湪 `mpc_update_from_rho.m` 涓疄鐜帮級锛?- 褰?`|蠅| > 0.15` rad/s 鏃讹紝鑷姩鎻愰珮 `q_y`锛堟í鍚戣窡韪潈閲嶏級
- 鏈€澶у鐩?1.8 鍊嶏紙杞集鏃舵洿鍏虫敞妯悜绮惧害锛?- 杩囨浮甯﹀搴?0.05 rad/s锛堝钩婊戝垏鎹紝閬垮厤鎶栧姩锛?
#### 杈撳嚭绾︽潫涓婇檺
```matlab
maps.ey_max = abs(opts.ymax(1));      % 1.0 m
maps.epsi_max = abs(opts.ymax(2));    % 0.5 rad
maps.ev_max = abs(opts.ymax(3));      % 0.5 m/s
maps.eomega_max = abs(opts.ymax(4));  % 0.3 rad/s
```

#### 鏉冮噸鎻掑€煎紑鍏?```matlab
maps.enable_weight_interp = true;  % 鍚敤鍦ㄧ嚎鏉冮噸鎻掑€?```

**娉ㄦ剰**锛?- 鏉冮噸鎻掑€奸渶瑕?Simulink 涓?*鏄惧紡浣跨敤**锛堝澶栭儴鏉冮噸绔彛锛?- 鎴栧湪鑴氭湰浠跨湡涓€氳繃 `mpcobj.Weights.*` 鎵嬪姩搴旂敤

---

### 3.6 鍏冩暟鎹?
```matlab
ctrl.meta.version = 'V1.2';
ctrl.meta.generated_time = datestr(now, 'yyyy-mm-dd HH:MM:SS');
ctrl.meta.base_workpoint = [v_center, omega_center, theta_center];
ctrl.meta.Ts = Ts;
ctrl.meta.Np = opts.Np;
ctrl.meta.Nc = opts.Nc;
ctrl.meta.control_horizon_sec = opts.Nc * Ts;
ctrl.meta.prediction_horizon_sec = opts.Np * Ts;
ctrl.meta.has_md = true;
ctrl.meta.mv_signals = 'F_cmd[N], omega_cmd[rad/s]';
ctrl.meta.md_signals = 'theta[rad]';
```

---

## 鍥涖€佸湪绾垮弬鏁版洿鏂帮細`mpc_update_from_rho.m`

### 4.1 鍑芥暟绛惧悕

```matlab
function upd = mpc_update_from_rho(rho, db, maps)
```

**杈撳叆**锛?- `rho`锛氬綋鍓嶈皟搴﹀彉閲?`[v; omega; theta]` (3脳1)
  - `omega` 淇濈暀绗﹀彿锛堟=宸﹁浆锛岃礋=鍙宠浆锛?- `db`锛歀PV鏁版嵁搴擄紙`db_rt`锛?- `maps`锛氭潈閲?绾︽潫鏄犲皠琛紙`ctrl.maps`锛?
**杈撳嚭**锛?- `upd`锛氭洿鏂扮粨鏋勪綋
  - **妯″瀷鐭╅樀**锛歚A`, `B`, `C`, `D`, `E`, `Bv`, `Dv`
  - **鏉冮噸**锛歚Q`, `R`, `dR`
  - **绾︽潫**锛歚umin`, `umax`
  - **璋冭瘯淇℃伅**锛歚rho_n`, `indices`, `weights`

---

### 4.2 褰掍竴鍖栦笌杈圭晫楗卞拰

```matlab
v = max(min(rho(1), V_grid(end)), V_grid(1));
omega = max(min(rho(2), W_grid(end)), W_grid(1));
theta = max(min(rho(3), T_grid(end)), T_grid(1));

if Nv > 1
    v_n = (v - V_grid(1)) / (V_grid(end) - V_grid(1));
else
    v_n = 0;
end
% 鍚岀悊璁＄畻 w_n, t_n
rho_n = [v_n; w_n; t_n];  % 鈭?[0,1]^3
```

**浣滅敤**锛?- 楗卞拰鍒扮綉鏍艰寖鍥达紙閬垮厤澶栨帹锛?- 褰掍竴鍖栧埌 `[0,1]`锛堜究浜庢彃鍊艰绠楋級

---

### 4.3 瀹氫綅缃戞牸鍗曞厓锛堜笁绾挎€ф彃鍊硷級

**鐩爣**锛氭壘鍒板寘鍥村綋鍓?`蟻` 鐨?涓《鐐广€?
**鎵ц浠ｇ爜**锛堟敮鎸侀潪鍧囧寑缃戞牸锛夛細
```matlab
i_low = find(V_grid <= v, 1, 'last');
i_low = max(1, min(Nv-1, i_low));
i_high = min(i_low + 1, Nv);
% 鍚岀悊瀹氫綅 j_low, j_high, k_low, k_high
```

**璁＄畻灞€閮ㄥ潗鏍?* `尉, 畏, 味 鈭?[0,1]`锛?```matlab
if V_grid(i_high) > V_grid(i_low)
    xi = (v - V_grid(i_low)) / (V_grid(i_high) - V_grid(i_low));
else
    xi = 0;
end
% 鍚岀悊璁＄畻 eta, zeta
```

**涓夌嚎鎬ф彃鍊兼潈閲?*锛?涓《鐐癸級锛?```matlab
w(1) = (1-xi) * (1-eta) * (1-zeta);  % (i_low,  j_low,  k_low)
w(2) = xi * (1-eta) * (1-zeta);      % (i_high, j_low,  k_low)
w(3) = (1-xi) * eta * (1-zeta);      % (i_low,  j_high, k_low)
w(4) = xi * eta * (1-zeta);          % (i_high, j_high, k_low)
w(5) = (1-xi) * (1-eta) * zeta;      % (i_low,  j_low,  k_high)
w(6) = xi * (1-eta) * zeta;          % (i_high, j_low,  k_high)
w(7) = (1-xi) * eta * zeta;          % (i_low,  j_high, k_high)
w(8) = xi * eta * zeta;              % (i_high, j_high, k_high)

w = w / sum(w);  % 褰掍竴鍖栵紙鏁板€肩ǔ瀹氭€э級
```

---

### 4.4 鎻掑€兼ā鍨嬬煩闃?
```matlab
A_interp = zeros(4, 4);
B_interp = zeros(4, 2);
C_interp = zeros(4, 4);
D_interp = zeros(4, 2);
E_interp = zeros(4, 1);

for p = 1:8
    i = indices(p, 1);
    j = indices(p, 2);
    k = indices(p, 3);
    
    A_interp = A_interp + w(p) * squeeze(db.A(i, j, k, :, :));
    B_interp = B_interp + w(p) * squeeze(db.B(i, j, k, :, :));
    C_interp = C_interp + w(p) * squeeze(db.C(i, j, k, :, :));
    D_interp = D_interp + w(p) * squeeze(db.D(i, j, k, :, :));
    E_interp = E_interp + w(p) * squeeze(db.E(i, j, k, :, :));
end
```

---

### 4.5 鎻掑€兼潈閲嶏紙鎸夌淮搴︽槧灏勶級

#### 璋冨害鍥犲瓙璁＄畻

**绛栫暐**锛氭牴鎹?`蟻_n` 鐨勫悇鍒嗛噺锛屼负姣忎釜鏉冮噸鍏冪礌璁＄畻鐙珛鐨勮皟搴﹀洜瀛愩€?
**榛樿绾挎€х粍鍚?*锛堝彲閫氳繃 `maps.factor_*` 鑷畾涔夛級锛?```matlab
fy   = 0.3*rho_n(1) + 0.2*rho_n(2) + 0.5*rho_n(3);  % 褰卞搷 q_y
fpsi = 0.1*rho_n(1) + 0.7*rho_n(2) + 0.2*rho_n(3);  % 褰卞搷 q_psi
fv   = 0.8*rho_n(1) + 0.1*rho_n(2) + 0.1*rho_n(3);  % 褰卞搷 q_v
fomega = 0.2*rho_n(1) + 0.6*rho_n(2) + 0.2*rho_n(3);  % 褰卞搷 q_omega

fR_F   = 0.6*rho_n(1) + 0.3*rho_n(2) + 0.1*rho_n(3);  % 褰卞搷 r_F
fR_w   = 0.2*rho_n(1) + 0.7*rho_n(2) + 0.1*rho_n(3);  % 褰卞搷 r_omega

fdR_F  = 0.5*rho_n(1) + 0.3*rho_n(2) + 0.2*rho_n(3);  % 褰卞搷 r_dF
fdR_w  = 0.2*rho_n(1) + 0.6*rho_n(2) + 0.2*rho_n(3);  % 褰卞搷 r_domega
```

**瑙ｉ噴**锛?- `q_y`锛氬潯搴﹀奖鍝嶆渶澶э紙绯绘暟0.5锛夛紝閫熷害娆′箣锛?.3锛?- `q_psi`锛氳閫熷害褰卞搷鏈€澶э紙绯绘暟0.7锛夛紝杞集鏃惰埅鍚戞洿閲嶈
- `q_v`锛氶€熷害褰卞搷鏈€澶э紙绯绘暟0.8锛?- `r_omega`锛氳閫熷害褰卞搷鏈€澶э紙绯绘暟0.7锛?
#### 褰㈢姸鏄犲皠锛堝彲閫夛級

鑻ヨ缃簡 `maps.alpha_*` 鍜?`maps.beta_*`锛?```matlab
shape_map = @(x, a, b) max(0, min(1, (x - a) ./ max(b - a, eps)));

fy     = shape_map(fy,     maps.alpha_Q(1),  maps.beta_Q(1));
fpsi   = shape_map(fpsi,   maps.alpha_Q(2),  maps.beta_Q(2));
% 鍚岀悊澶勭悊 fv, fomega, fR_F, fR_w, fdR_F, fdR_w
```

**浣滅敤**锛氬湪 `[alpha, beta]` 鍖洪棿鍐呯嚎鎬ц繃娓★紝鍖洪棿澶栧す绱т负0鎴?銆?
#### 鏉冮噸鎻掑€?
```matlab
if enable_weight_interp && isfield(maps, 'Q_range')
    Q_min = maps.Q_range(1, :);
    Q_max = maps.Q_range(2, :);
    Q_interp = Q_min + [fy; fpsi; fv; fomega]' .* (Q_max - Q_min);
end

% 鍚岀悊鎻掑€?R_interp, dR_interp
```

**绀轰緥**锛?- `Q_range = [15, 20, 3.5, 1.2; 22, 28, 5.5, 2.5]`
- 鑻?`fy = 0.6`锛屽垯 `q_y = 15 + 0.6*(22-15) = 19.2`

---

### 4.6 鍦烘櫙鑷€傚簲鏉冮噸璋冨害锛堟柟妗圔锛?
**鐩殑**锛氳浆寮椂鑷姩鎻愰珮 `q_y`锛堟í鍚戣窡韪潈閲嶏級銆?
**鎵ц浠ｇ爜**锛?```matlab
omega_thresh = maps.omega_threshold;  % 0.15 rad/s
gain_max = maps.q_y_gain_max;        % 1.8
trans_width = maps.transition_width;  % 0.05 rad/s

omega_abs = abs(omega);

if omega_abs <= (omega_thresh - trans_width)
    q_y_gain = 1.0;  % 鐩寸嚎鍖哄煙
elseif omega_abs >= (omega_thresh + trans_width)
    q_y_gain = gain_max;  % 杞集鍖哄煙
else
    % 杩囨浮鍖哄煙锛氫笁娆?Hermite 骞虫粦鎻掑€?    s = (omega_abs - (omega_thresh - trans_width)) / (2 * trans_width);
    q_y_gain = 1.0 + (gain_max - 1.0) * (3*s^2 - 2*s^3);
end

Q_interp(1) = Q_interp(1) * q_y_gain;  % 搴旂敤澧炵泭鍒?q_y
```

**鏁堟灉**锛?- 鐩寸嚎锛坄|蠅|<0.10`锛夛細`q_y` 淇濇寔鍩哄噯鍊?- 鎬ヨ浆寮紙`|蠅|>0.20`锛夛細`q_y` 鏀惧ぇ 1.8 鍊?- 涓棿锛氬钩婊戣繃娓?
---

### 4.7 绾︽潫鎻掑€?
#### 鍩轰簬瑙掗€熷害鐨勭嚎鎬ф彃鍊?```matlab
omega_n = rho_n(2);  % 褰掍竴鍖栬閫熷害
umin_interp = (1-omega_n) * maps.umin_range(1,:)' + omega_n * maps.umin_range(2,:)';
umax_interp = (1-omega_n) * maps.umax_range(1,:)' + omega_n * maps.umax_range(2,:)';
```

#### 鍙犲姞缂╂斁鍥犲瓙
```matlab
scale_umin = (1-omega_n) * maps.scale_umin_lo + omega_n * maps.scale_umin_hi;
scale_umax = (1-omega_n) * maps.scale_umax_lo + omega_n * maps.scale_umax_hi;

umin_interp = umin_interp .* scale_umin;
umax_interp = umax_interp .* scale_umax;
```

**绀轰緥**锛?- 鑻?`scale_umax_hi = [1.2, 1.0]`
- 杞集鏃讹紙`omega_n=1`锛夛細`F_max` 鏀惧ぇ 1.2 鍊嶏紝鍏佽鏇村ぇ椹卞姩鍔?
---

### 4.8 缁勮杈撳嚭缁撴瀯浣?
```matlab
upd.A = A_interp;   % [4脳4]
upd.B = B_interp;   % [4脳2] MV閮ㄥ垎
upd.C = C_interp;   % [4脳4]
upd.D = D_interp;   % [4脳2]
upd.E = E_interp;   % [4脳1] MD閮ㄥ垎锛埼告壈鍔級
upd.Bv = E_interp;  % [4脳1] Adaptive MPC涓撶敤鍚嶇О
upd.Dv = zeros(ny, nd);  % [4脳1] MD鐩撮€氱煩闃碉紙閫氬父涓洪浂锛?
upd.Q = Q_interp;
upd.R = R_interp;
upd.dR = dR_interp;
upd.umin = umin_interp;
upd.umax = umax_interp;

upd.rho = [v; omega; theta];  % 楗卞拰鍚庣殑瀹為檯 蟻
upd.rho_n = rho_n;
upd.indices = indices;  % 8脳3 椤剁偣绱㈠紩
upd.weights = w;        % 8脳1 鎻掑€兼潈閲?```

---

## 浜斻€佷豢鐪熻繍琛屾椂鐨勫弬鏁版洿鏂版祦绋?
### 5.1 Simulink 鍧楁帴绾?
```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                   LPVMPC_AGV_simulink._GRU.slx                  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
  [Reference]                         [theta_ground]
      鈹?                                     鈹?      鈹?                                     鈻?      鈻?                             鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                     鈹?    Plant     鈹?鈹侾ath Error   鈹傗梹鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? (S-Function) 鈹?鈹侰alculator   鈹?                     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?                            鈹?       鈹?                                   鈹?y_raw [31脳1]
       鈹?[e_y, e_psi,                       鈹?       鈹? e_v, e_omega]                     鈻?       鈹?                             鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?                             鈹?    GRU      鈹?       鈹?                             鈹係tate Classify鈹?       鈹?                             鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?                                    鈹?theta_hat
       鈹?                                    鈹?       鈹?        鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?        鈹?       鈻?        鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?      Adaptive MPC              鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹? 鈹?鑷畾涔夋洿鏂板嚱鏁?             鈹?鈹?鈹? 鈹?mpc_update_from_rho        鈹?鈹?鈹? 鈹?  杈撳叆: rho_f=[v;蠅;胃_hat]  鈹?鈹?鈹? 鈹?  杈撳嚭: A,B,C,D,Bv         鈹?鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹?                                鈹?鈹? 杈撳叆绔彛:                       鈹?鈹? - mo (Measured Outputs): y    鈹?鈹? - ref (Reference): [0;0;0;0]  鈹?鈹? - md (Meas. Disturbance): 胃   鈹?鈹?                                鈹?鈹? 杈撳嚭: u = [F_cmd; omega_cmd]   鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?              鈹?              鈻?          [Plant]
```

---

### 5.2 姣忎釜浠跨湡姝ョ殑鎵ц娴佺▼

#### Step 1锛歅lant 杈撳嚭
```matlab
y_raw = output_eq_ref(x, u, theta_ground, params);  % [31脳1]
```

#### Step 2锛欸RU 鎺ㄧ悊
```matlab
[state_gru, out_gru] = GRU_state_classifier('update', state_gru, y_raw);
theta_hat = out_gru.theta_hat;  % 浼拌鐨勫潯搴﹁
```

#### Step 3锛氭瀯閫?蟻锛圧hoFilter 鍧楋級
```matlab
v = y_raw(4);
omega = y_raw(5);
rho_raw = [v; omega; theta_hat];

% 涓€闃朵綆閫氭护娉紙蟿=0.4s锛?alpha = Ts / (tau + Ts);
rho_f = alpha * rho_raw + (1 - alpha) * rho_f_prev;
```

#### Step 4锛歁PC 鑷畾涔夋洿鏂板嚱鏁?```matlab
upd = mpc_update_from_rho(rho_f, db_rt, ctrl.maps);

% 鏋勯€?plant_model锛堟洿鏂板悗鐨勬ā鍨嬶級
plant_model.A = upd.A;
plant_model.B = [upd.B, upd.E];  % [4脳3]锛堝惈MD鍒楋級
plant_model.C = upd.C;
plant_model.D = [upd.D, zeros(4,1)];  % [4脳3]
plant_model.Ts = db_rt.Ts;

% 鍙€夛細鏇存柊鏉冮噸锛堥渶澶栭儴绔彛鎴栧洖璋冿級
% mpcobj.Weights.OutputVariables = upd.Q;
% mpcobj.Weights.ManipulatedVariables = upd.R;
% mpcobj.Weights.ManipulatedVariablesRate = upd.dR;
```

#### Step 5锛歁PC 姹傝В
```matlab
y_meas = [e_y; e_psi; e_v; e_omega];  % 娴嬮噺杈撳嚭
r_ref = [0; 0; 0; 0];                 % 璇樊鍙傝€冿紙瓒嬮浂鎺у埗锛?md = theta_hat;                       % 娴嬮噺鎵板姩

[u_mpc, Info, xmpc_next] = mpcmoveAdaptive(mpcobj, xmpc, plant_model, Nominal, y_meas, r_ref, md);
```

**Nominal 缁撴瀯浣?*锛?```matlab
Nominal.U = zeros(3,1);  % [2 MV + 1 MD]
Nominal.X = zeros(4,1);
Nominal.Y = zeros(4,1);
Nominal.DX = zeros(4,1);
```

#### Step 6锛歅lant 鏇存柊
```matlab
u_plant = [u_mpc(1); u_mpc(2); theta_ground];  % [F_cmd; omega_cmd; theta_ground]
x_next = state_eq_ref(x, u_plant, theta_ground, params);
```

---

## 鍏€佸弬鏁颁紶閫掓€荤粨琛?
| 鍙傛暟绫诲瀷 | 鏉ユ簮 | 浼犻€掕矾寰?| 鏈€缁堝簲鐢ㄤ綅缃?| 鏇存柊棰戠巼 |
|---------|------|---------|-------------|---------|
| **鍩虹鍙傛暟** | `parameters.m` | PreLoadFcn 鈫?Base WS 鈫?Plant | Plant S-Function | 鍒濆鍖栦竴娆?|
| **LPV鏁版嵁搴?* | `lin_agv_db.mat` | PreLoadFcn 鈫?`db_rt` 鈫?MPC鏇存柊鍑芥暟 | `mpc_update_from_rho` | 鍒濆鍖栦竴娆?|
| **浼樺寲鏉冮噸鑼冨洿** | `maps_best.mat` | PreLoadFcn 鈫?`ctrl.maps` 鈫?鏇存柊鍑芥暟 | `mpc_update_from_rho` | 鍒濆鍖栦竴娆?|
| **MPC瀵硅薄** | `mpc_setup_single_interp` | PreLoadFcn 鈫?`ctrl.mpcobj` 鈫?Adaptive MPC鍧?| Adaptive MPC Controller | 鍒濆鍖栦竴娆?|
| **鏉冮噸鏄犲皠琛?* | `ctrl.maps` | 鎺у埗鍣ㄥ垱寤?鈫?鏇存柊鍑芥暟 | `mpc_update_from_rho` | 鍒濆鍖栦竴娆?|
| **妯″瀷鐭╅樀** | `db_rt.A/B/C/D/E` | 鍦ㄧ嚎鎻掑€?鈫?`plant_model` | Adaptive MPC姹傝В鍣?| 姣忎釜浠跨湡姝?|
| **鏉冮噸Q/R/dR** | `ctrl.maps.*_range` | 鍦ㄧ嚎鎻掑€?鈫?`upd.Q/R/dR` | 锛堝彲閫夛級MPC鏉冮噸绔彛 | 姣忎釜浠跨湡姝?|
| **绾︽潫umin/umax** | `ctrl.maps.scale_*` | 鍦ㄧ嚎鎻掑€?鈫?`upd.umin/umax` | 锛堝彲閫夛級MPC绾︽潫绔彛 | 姣忎釜浠跨湡姝?|
| **鍧″害瑙掍及璁?* | GRU鎺ㄧ悊 | `y_raw` 鈫?GRU 鈫?`theta_hat` | MPC鐨凪D绔彛 + `蟻` | 姣忎釜浠跨湡姝?|
| **璋冨害鍙橀噺** | `[v,蠅,胃_hat]` | Plant杈撳嚭 + GRU 鈫?RhoFilter 鈫?鏇存柊鍑芥暟 | `mpc_update_from_rho` | 姣忎釜浠跨湡姝?|

---

## 涓冦€佸叧閿璁″喅绛栦笌鐞嗙敱

### 7.1 涓轰粈涔堜娇鐢?鑼冨洿鎻掑€?鑰岄潪"鍥哄畾鏉冮噸"锛?
**闂**锛氫笉鍚屽伐鍐碉紙鐩磋/杞集/涓婂潯锛夊鎺у埗鎬ц兘瑕佹眰涓嶅悓銆?
**瑙ｅ喅鏂规**锛?- 鐩磋锛氫綆 `q_y`锛堟í鍚戣宸蹇嶅害楂橈級锛岄珮 `q_v`锛堥€熷害绮惧害浼樺厛锛?- 杞集锛氶珮 `q_y`銆乣q_psi`锛堟í鍚?鑸悜绮惧害浼樺厛锛?- 涓婂潯锛氶珮 `q_v`锛堢淮鎸侀€熷害锛夛紝鏀惧 `umax`锛堝厑璁稿ぇ椹卞姩鍔涳級

**瀹炵幇**锛?- 閫氳繃 `Q_range`銆乣R_range` 瀹氫箟鏉冮噸涓婁笅鐣?- 鏍规嵁 `蟻_n` 鎻掑€硷紙`fy`銆乣fpsi`绛夎皟搴﹀洜瀛愶級
- 璐濆彾鏂紭鍖栬嚜鍔ㄥ鎵炬渶浼樿寖鍥?
---

### 7.2 涓轰粈涔堝潯搴﹁ `胃` 杩涘叆 MD 閫氶亾鑰岄潪 MV锛?
**MD锛圡easured Disturbance锛塿s MV锛圡anipulated Variable锛?*锛?- **MV**锛氬彲鎺ц緭鍏ワ紙濡?`F_cmd`銆乣omega_cmd`锛?- **MD**锛氬彲娴嬮噺浣嗕笉鍙帶鐨勬壈鍔紙濡傚潯搴﹁銆侀閫燂級

**MPC 澶勭悊 MD 鐨勪紭鍔?*锛?- **鍓嶉琛ュ伩**锛氭彁鍓嶉娴嬫湭鏉?`Np` 姝ョ殑 `胃` 褰卞搷锛岄鍏堣皟鏁存帶鍒堕噺
- **闆舵粸鍚?*锛氭棤闇€绛夊埌璇樊鍑虹幇鎵嶅弽搴?- **椴佹鎬?*锛氬嵆浣?`胃` 浼拌鏈夊亸宸紝鍙嶉鎺у埗鍙ˉ鍋?
**瀹炵幇**锛?- `upd.Bv = E(蟻)`锛氭壈鍔ㄥ奖鍝嶇煩闃碉紙`胃` 濡備綍褰卞搷鐘舵€侊級
- MPC 鍦ㄤ紭鍖栨椂鑰冭檻锛歚x_{k+1} = A x_k + B u_k + Bv 胃_k`

---

### 7.3 涓轰粈涔堟潈閲嶉渶瑕?鎸夌淮搴︽槧灏?鑰岄潪缁熶竴缂╂斁锛?
**闂**锛?- `q_y`锛堟í鍚戣宸級涓?`q_v`锛堥€熷害璇樊锛夊涓嶅悓宸ュ喌鐨勬晱鎰熸€т笉鍚?- 缁熶竴缂╂斁锛堝 `Q *= 1.5`锛夋棤娉曚綋鐜板樊寮傚寲闇€姹?
**瑙ｅ喅鏂规**锛?- 姣忎釜鏉冮噸鍏冪礌鐙珛璋冨害锛坄fy`, `fpsi`, `fv`, `fomega`锛?- 褰㈢姸鍙傛暟锛坄alpha/beta`锛夋帶鍒堕潪绾挎€ц繃娓?- 鍥犲瓙鏉冮噸锛坄factor_y`, `factor_psi`绛夛級鍙嚜瀹氫箟 `蟻` 鍚勫垎閲忕殑褰卞搷姣斾緥

**绀轰緥**锛?- 杞集鏃讹細`fpsi = 0.1*v + 0.7*蠅 + 0.2*胃`
  - 涓昏鐢辫閫熷害 `蠅` 涓诲锛堢郴鏁?.7锛?  - 鑸悜璺熻釜鍦ㄨ浆寮椂鏇撮噸瑕?- 涓婂潯鏃讹細`fv = 0.8*v + 0.1*蠅 + 0.1*胃`
  - 涓昏鐢遍€熷害 `v` 涓诲锛堢郴鏁?.8锛?  - 缁存寔閫熷害鍦ㄧ埇鍧℃椂鏈€鍏抽敭

---

### 7.4 涓轰粈涔堥渶瑕?婊ゆ尝 蟻"锛?
**闂**锛?- 鍘熷 `蟻=[v, 蠅, 胃_hat]` 鍙兘鍖呭惈娴嬮噺鍣０
- 蹇€熻烦鍙樹細瀵艰嚧妯″瀷绐佸彉锛屽紩璧锋帶鍒堕渿鑽?
**瑙ｅ喅鏂规**锛?- 涓€闃朵綆閫氭护娉紙蟿=0.4s锛?- 骞虫粦 `蟻` 鐨勫彉鍖?
**瀹炵幇**锛?```matlab
alpha = Ts / (tau + Ts);
rho_f = alpha * rho_raw + (1 - alpha) * rho_f_prev;
```

**鏁堟灉**锛?- 閬垮厤妯″瀷鍙傛暟鎶栧姩
- 淇濇寔鎺у埗杩炵画鎬?
---

## 鍏€佹晠闅滄帓鏌ユ寚鍗?
### 闂 1锛歁PC 姹傝В澶辫触锛圛nfo.QPCode = 'infeasible'锛?
**鍙兘鍘熷洜**锛?1. 绾︽潫杩囦弗锛堣緭鍑虹害鏉?`ymin/ymax` 涓嶅彲琛岋級
2. 妯″瀷鐭╅樀鎻掑€奸敊璇紙`A` 涓嶇ǔ瀹氾級
3. 鏉冮噸璁剧疆涓嶅綋锛坄Q` 杩囧ぇ瀵艰嚧闂鍒氭€э級

**鎺掓煡姝ラ**锛?1. 妫€鏌?`upd.A` 鐨勭壒寰佸€硷細`max(abs(eig(upd.A)))`锛堝簲 <1锛?2. 涓存椂鏀惧杈撳嚭绾︽潫锛歚ymin=[-Inf;...], ymax=[Inf;...]`
3. 妫€鏌?`upd.Q/R/dR` 鏄惁寮傚父锛圢aN銆佽礋鍊笺€佽繃澶э級
4. 鏌ョ湅 `Info.Iterations` 鍜?`Info.Cost`

---

### 闂 2锛氭潈閲嶆湭鐢熸晥锛堟帶鍒舵€ц兘涓庨鏈熶笉绗︼級

**鍙兘鍘熷洜**锛?- Simulink Adaptive MPC 鍧楁湭杩炴帴澶栭儴鏉冮噸绔彛
- `maps.enable_weight_interp = false`锛堟潈閲嶆彃鍊艰绂佺敤锛?
**瑙ｅ喅鏂规**锛?1. 纭 `ctrl.maps.enable_weight_interp = true`
2. 鍦?Adaptive MPC 鍧椾腑鍚敤"External Weights"绔彛
3. 鎵嬪姩楠岃瘉锛氳剼鏈豢鐪熶腑鎵撳嵃 `upd.Q`锛岃瀵熸槸鍚﹂殢 `蟻` 鍙樺寲

---

### 闂 3锛氬潯搴﹁ˉ鍋挎棤鏁堬紙涓婂潯鎺夐€燂級

**鍙兘鍘熷洜**锛?1. GRU浼拌 `胃_hat` 涓嶅噯纭?2. `upd.E` 鐭╅樀閿欒锛堟壈鍔ㄥ奖鍝嶇煩闃碉級
3. MD 閫氶亾鏈纭繛鎺?
**鎺掓煡姝ラ**锛?1. 瀵规瘮 `theta_hat` 涓?`theta_ground`锛歚mean(abs(theta_hat - theta_ground))`锛堝簲 <2掳锛?2. 妫€鏌?`upd.E` 绗?琛岋紙绾靛悜鍔ㄥ姏瀛︼級鏄惁闈為浂
3. 纭 Adaptive MPC 鍧楃殑 `md` 绔彛宸茶繛鎺?`theta_hat`
4. 楠岃瘉鍓嶉鍔涜绠楋細`F_eq = m*g*sin(theta) + c_r*m*g*cos(theta) + F_aero`

---

### 闂 4锛氳浆寮椂妯悜璇樊杩囧ぇ

**鍙兘鍘熷洜**锛?1. `q_y` 鏉冮噸杩囦綆
2. 鍦烘櫙鑷€傚簲鏈惎鐢紙鏂规B锛?3. `omega_threshold` 璁剧疆杩囬珮锛堟湭瑙﹀彂澧炵泭锛?
**瑙ｅ喅鏂规**锛?1. 鎻愰珮 `maps.Q_range` 绗?鍒楋紙`q_y`锛?2. 纭 `maps.omega_threshold = 0.15`锛堝悎鐞嗛槇鍊硷級
3. 妫€鏌?`maps.q_y_gain_max = 1.8`锛堝鐩婅冻澶熷ぇ锛?4. 鎵撳嵃 `q_y_gain`锛岃瀵熻浆寮椂鏄惁鎻愰珮
5. 璋冩暣 `maps.transition_width`锛堣繃娓″甫瀹藉害锛?
---

## 涔濄€佹墿灞曢槄璇?
### 鐩稿叧鏂囨。
- `func.md`锛氬姛鑳芥ā鍧楀鑸紙鑴氭湰銆佹帴鍙ｃ€佷緷璧栵級
- `README_LPVMPC_Usage.md`锛歀PV-MPC浣跨敤鎸囧崡
- `README_GRU_Integration.md`锛欸RU宸ュ喌璇嗗埆闆嗘垚璇存槑
- `MPC鏉冮噸纭畾鏈哄埗璇存槑.md`锛氭潈閲嶈璁¤缁嗚鏄?- `change.md`锛氱増鏈洿鏂拌褰?
### 鍏抽敭鑴氭湰
- `parameters.m`锛氶泦涓弬鏁板畾涔?- `lin_agv_grid.m`锛歀PV鏁版嵁搴撶敓鎴?- `mpc_setup_single_interp.m`锛歁PC鎺у埗鍣ㄥ垱寤?- `mpc_update_from_rho.m`锛氬湪绾垮弬鏁版洿鏂?- `Cost_Function.m`锛歁PC闂幆璇勪及
- `Bayesian_Optimization.m`锛氭潈閲嶄紭鍖?
---

## 鍗併€佹€荤粨

### 鍙傛暟鍔犺浇閾捐矾绮剧偧鐗?
```
parameters.m 鈫?params
    鈫?lin_agv_db.mat 鈫?db_rt (A/B/C/D/E缃戞牸)
    鈫?maps_best.mat 鈫?maps_best (Q/R/dR鑼冨洿銆佺害鏉熺缉鏀?
    鈫?mpc_setup_single_interp 鈫?ctrl
    鈹溾攢 ctrl.mpcobj (MPC瀵硅薄锛屽熀鍑嗘ā鍨?鏉冮噸+绾︽潫)
    鈹斺攢 ctrl.maps (鏉冮噸/绾︽潫鏄犲皠琛紝鍙maps_best瑕嗙洊)
        鈫?姣忎釜浠跨湡姝ワ細
    Plant 鈫?y_raw 鈫?GRU 鈫?theta_hat
                      鈫?    [v, 蠅, theta_hat] 鈫?RhoFilter 鈫?rho_f
                                      鈫?    mpc_update_from_rho(rho_f, db_rt, ctrl.maps)
        鈹溾攢 涓夌嚎鎬ф彃鍊?A/B/C/D/E
        鈹溾攢 鎸夌淮搴︽彃鍊?Q/R/dR
        鈹溾攢 鍦烘櫙鑷€傚簲澧炵泭锛堣浆寮椂鎻愰珮q_y锛?        鈹斺攢 绾︽潫鎻掑€?umin/umax
            鈫?    Adaptive MPC 姹傝В锛堜娇鐢ㄦ洿鏂板悗鐨勬ā鍨?鏉冮噸+绾︽潫锛?        鈫?    鎺у埗杈撳嚭 [F_cmd, omega_cmd] 鈫?Plant
```

### 鏍稿績鐞嗗康

1. **鍒嗗眰璁捐**锛氬弬鏁扳啋鏁版嵁搴撯啋鎺у埗鍣ㄢ啋鍦ㄧ嚎鏇存柊
2. **鏅鸿兘璋冨害**锛氭牴鎹伐鍐碉紙`蟻`锛夎嚜閫傚簲璋冩暣妯″瀷鍜屽弬鏁?3. **璐濆彾鏂紭鍖?*锛氳嚜鍔ㄥ鎵炬渶浼樻潈閲嶈寖鍥?4. **鍦烘櫙鑷€傚簲**锛氳浆寮椂鑷姩鎻愰珮妯悜璺熻釜绮惧害
5. **鍓嶉琛ュ伩**锛氬潯搴﹁杩涘叆MD閫氶亾锛屾彁鍓嶉娴嬫壈鍔ㄥ奖鍝?
---

**鐗堟湰**锛歏1.0锛?025-11-06锛? 
**浣滆€?*锛欰uto-generated  
**缁存姢**锛氳 `change.md`


