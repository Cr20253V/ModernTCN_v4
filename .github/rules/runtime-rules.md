# 椤圭洰杩愯瑙勫垯锛堣繍琛屾椂/寮€鍙戦€氱敤瑙勮寖锛?
> 闈㈠悜鏈粨搴撶殑鏃ュ父寮€鍙戙€佽仈璋冧笌浜や粯鐨勭粺涓€绾︽潫锛氳瑷€銆佷唬鐮侀鏍笺€佹敞閲娿€佹帴鍙ｄ笌鐩綍銆佹彁浜や笌鏂囨。銆?
## 1. 璇█涓庢矡閫?- 鍥炵瓟涓庢敞閲婏細涓枃涓轰富锛屽繀瑕佹椂琛ヨ嫳鏂囨湳璇€?- 鍗曚綅缁熶竴锛歮, m/s, rad锛涢噰鏍峰懆鏈?`Ts` 鐢?`parameters.m` 鎻愪緵銆?- 浠ｇ悊/鍗忎綔锛氳嫢鎵ц涓瓨鍦ㄤ笉纭畾鎬ф垨缂哄皯淇℃伅锛岄渶绔嬪嵆鍚戜綔鑰呮彁闂苟鏍囨敞鈥滃亣璁?鍙€夆€濄€?
## 2. 璇█鏍堜笌鏂囦欢绫诲瀷
- 棣栭€夛細MATLAB锛?m锛変笌 Simulink锛?slx锛夈€?- 绂佹鐩存帴淇敼/鎻愪氦鐨勬瀯寤轰骇鐗╀笌缂撳瓨锛歚slprj/`, `*_grt_rtw/`, `*.slxc`, `*.autosave`, `GRU_logs/`銆?- 棣栭€夋柊澧?淇敼锛歚.m`, `.md` 涓庨《灞?`.mat` 浜х墿銆?
## 3. 浠ｇ爜椋庢牸锛圡ATLAB锛?- 鍑芥暟鍖栦紭鍏堬細姣忎釜鏍稿績鍔熻兘鐙珛鍑芥暟鏂囦欢锛宍function ... end`銆?- 鍛藉悕璇箟鍖栵細閬垮厤鍗曞瓧姣嶏紱濡?`x_ref`, `u_mpc`, `rho_grid`銆?- 鍚戦噺鍖栦笌棰勫垎閰嶏細閬垮厤涓嶅繀瑕佸惊鐜笌鍔ㄦ€佹墿瀹广€?- I/O 绾﹀畾锛氳鍐?`.mat` 浣跨敤娓呮櫚鍙橀噺鍚嶏紝蹇呰鏃惰鏄庣淮搴︿笌鍗曚綅銆?- 杈撳嚭鏈€灏忓彲杩愯绀轰緥锛屽苟缁欏嚭 `matlab -batch` 鍛戒护鑼冧緥銆?
绀轰緥锛?```matlab
function y = saturate(u, umin, umax)
%SATURATE Clamp u into [umin, umax]
    y = min(max(u, umin), umax);
end
```

## 4. 娉ㄩ噴瑙勮寖锛堣剼鏈?鍑芥暟澶存ā鏉匡級
```matlab
% =============================
% 鏂囦欢鍚嶏細xxx.m
% 鐗堟湰鍙凤細V1.0
% 鏈€鍚庝慨鏀规椂闂达細YYYY-MM-DD
% 浣滆€咃細xxx
% 鍔熻兘鎻忚堪锛?% 杈撳叆鍙傛暟锛?%   - xxx锛氱被鍨嬶紝鍗曚綅锛岃鏄?% 杈撳嚭鍙傛暟锛?%   - xxx锛氱被鍨嬶紝鍗曚綅锛岃鏄?% 渚濊禆锛?% 澶囨敞锛?% =============================
```

## 5. 鎺ュ彛涓庢暟鎹害瀹?- 璺緞鍏ㄥ眬鍙傝€冿紙鐢ㄤ簬鍙鍖?澶栭儴妯″潡锛夛細`ref_global=[X Y psi v omega]`锛? 鍒楋級銆?- MPC 璇樊鐘舵€侊細`x_err=[e_y,e_psi,e_v,e_omega]^T`锛汳PC 鍙傝€冪鍙ｅ疄闄呬负 4脳1锛堥浂鍚戦噺鎴栬瀹氳宸洰鏍囷級銆?- 璋冨害鍙橀噺锛歚rho=[v, omega, theta]`锛涚粡涓€闃舵护娉紙蟿鈮?.3鈥?.5 s锛夈€?- From Workspace锛氱粨鏋?`time` + `signals.values`锛岃嫢椹卞姩 MPC 璇樊鍙傝€冿紝浠呮彁渚?4 鍒椼€?
## 6. 褰撳墠椤圭洰缁撴瀯涓庣害鏉燂紙涓庣幇鐘跺榻愶級
- 鏍圭洰褰曚负涓伙紙flat锛夛紝鏍稿績鑴氭湰涓庝骇鐗╅泦涓湪浠撳簱鏍癸細
    - 妯″瀷/鏂圭▼锛歚parameters.m`, `state_eq.m`, `state_eq_ref.m`, `output_eq.m`, `output_eq_ref.m` 鍙?`*_ref_train_data.m`
    - 绾挎€у寲锛歚lin_agv_at_point.m`, `lin_agv_grid.m`锛涗骇鐗╋細`plant_grid.mat`, `plant_grid_test.mat`, `lin_agv_db.mat`
    - MPC锛歚mpc_setup_single_interp.m`, `mpc_update_from_rho.m`
    - 鍙傝€冭建杩癸細`gen_agv_ref_path.m`锛涗骇鐗╋細`path_straight.mat`, `path_turn.mat`, `path_straight_turn.mat`, `path_slope.mat`, `path_bumpy.mat`
    - GRU锛歚GRU_*.m` 绯诲垪鑴氭湰涓?`GRU_*.mat` 浜х墿
    - 浼樺寲锛歚Bayesian_Optimization.m`, `Cost_Function.m`, `start_bayesian.m`锛涗骇鐗╋細`maps_best.mat`
    - Simulink锛歚LPVMPC_AGV_simulink._GRU.slx`, `GRU_DataGen.slx`, `test.slx`
    - 鏂囨。锛歚docs/`锛堟湰鏂囦欢鎵€鍦級
- 鑷姩/涓棿浜х墿鐩綍锛歚slprj/`, `*_grt_rtw/`, `*.slxc`, `*.autosave`, `GRU_logs/` 鈥?绂佹鎵嬫敼銆佺姝㈡彁浜よ嚜瀹氫箟鍐呭銆?- 鏂板杈呭姪鑴氭湰涓庨厤缃細浠嶆斁缃簬鏍圭洰褰曪紙涓庣幇鐘朵竴鑷达級銆傚闇€鏂板缓瀛愮洰褰曪紝闇€璇勫鍚庣粺涓€杩佺Щ銆?- 鏂颁骇鐗╁懡鍚嶄笌浣嶇疆闇€寤剁画鐜版湁鎯緥锛?    - 绾挎€у寲搴擄細`plant_grid.mat`锛堝彲娣诲姞鐗堟湰灏剧紑锛夛紱
    - 鍙傝€冭矾寰勶細`path_<type>.mat`锛?    - 浼樺寲缁撴灉锛歚maps_best.mat`锛?    - 鍏朵綑 `.mat` 浜х墿鏀炬牴鐩綍骞跺惈 `meta` 瀛楁锛堢敓鎴愭椂闂淬€佸弬鏁般€佺増鏈€佷綔鑰咃級銆?
## 7. 鏂囨。涓庘€滀唬鐮佸鑸€濆崗浣滐紙func.md锛?- 鐢熸垚/淇敼涓氬姟浠ｇ爜鍓嶏紝蹇呴』鍏堥槄璇绘牴鐩綍 `func.md`銆?- 鏂板鎴栦慨鏀逛换鎰?Service/Manager/鑴氭湰/鎺ュ彛锛屽繀椤诲悓姝ユ洿鏂?`func.md` 鏉＄洰锛氬眰绾?璺緞/鑱岃矗/绛惧悕/杈撳叆杈撳嚭/澶囨敞銆?- CI 寤鸿锛氳嫢鏂板 `.m` 浣嗘湭鏇存柊 `func.md`锛岄樆鏂悎鍏ャ€?
## 8. 鎻愪氦涓庣暀鐥曪紙Git 瑙勮寖瑕佺偣锛?- 鎻愪氦鏍囬锛歚<type>(<module>): <绠€瑕佹弿杩?`锛屽 `feat(mpc): 鏀寔 蟻 涓夌嚎鎬ф彃鍊糮銆?- 绫诲瀷锛歚feat|fix|refactor|doc|test|chore|style|perf`锛涚牬鍧忔€т慨鏀圭敤 `!` 鎴?`BREAKING CHANGE:` 娈点€?- 鎻愪氦姝ｆ枃搴斿寘鍚細Context/Changes/Impact/Verification/Artifacts/Migration/Refs 绛夌粨鏋勫寲娈碉紙璇﹁ `docs/change.md` 妯℃澘锛夈€?
## 9. 浜や粯娓呭崟
- 浠ｇ爜锛堝惈娉ㄩ噴涓庣増鏈ご锛夈€?- `.mat` 浜х墿锛堝惈 `meta` 瀛楁锛夈€?- `func.md` 瀵艰埅鏇存柊銆?- 鎶ュ憡锛堝浘琛ㄨ剼鏈敓鎴愶紝淇濊瘉鍙鐜帮級銆?
## 10. 鏁板€间笌绋冲仴鎬ч€氱敤绾﹀畾
- 灏忛噺淇濇姢锛歚v_sat=max(v,1e-3)` 鍙備笌鏇茬巼涓庨櫎娉曘€?- 杩囨护涓庨┗鐣欙細璋冨害閲忎笌鍒嗙被鍣ㄨ緭鍑轰娇鐢ㄤ竴闃舵护娉笌鏈€灏忛┗鐣欐椂闂翠互鎶戝埗鎶栧姩銆?- 澶辫触鍏滃簳锛氫竴鏃﹀嚭鐜?NaN/Inf 鎴栨眰瑙ｅけ璐ワ紝绔嬪嵆缁堟璇ュ洖鍚堝苟杩斿洖澶т唬浠风敤浜庤皟鍙傛祦绋嬨€?
## 11. 鎵╁睍琛ュ厖锛堝彲閫夊寮鸿鑼冿級
- MATLAB 鐗堟湰涓庡吋瀹癸細寤鸿鍦?`parameters.m` 椤堕儴娉ㄦ槑娴嬭瘯鐗堟湰锛堢ず渚嬶細R2023b锛夛紱鍑虹幇鐗堟湰鐩稿叧宸紓闇€鍦?`change.md` 鏍囪銆?
- `.mat` 浜х墿鍏冧俊鎭細缁熶竴浣跨敤 `meta` 瀛楁锛歚meta.version`, `meta.generated_at`, `meta.source_script`, `meta.params_hash`锛堝彲鐢?`DataHash` 鑻ュ畨瑁咃級锛宍meta.author`銆傜己澶变笉闃绘柇锛屼絾浼樺寲/璋冭瘯浼樺厛銆?
- 閿欒澶勭悊锛氭墍鏈夋牳蹇冨叆鍙ｈ剼鏈紙`mpc_setup_single_interp.m`, `lin_agv_grid.m`, `GRU_train.m`, `Cost_Function.m`锛夊湪杈撳叆鏍￠獙澶辫触鏃朵娇鐢?`error(...)` 鑰岄潪闈欓粯杩斿洖锛涜皟鍙傚満鏅彲鐢?`warning` + 缁х画銆?
- 鏃ュ織鏍煎紡寤鸿锛堟枃鏈垨 MAT锛夛細缁撴瀯鏁扮粍瀛楁锛歚t, rho, u, status, solve_time_ms, slack, e_y, e_psi, e_v, e_omega`锛屼究浜庣粺涓€鍒嗘瀽銆?
- 鎬ц兘鍩虹嚎锛氬崟姝?MPC 姹傝В P95 < 2 ms锛堝綋鍓嶇洰鏍囷級鑻ヨ秴杩囬渶璁板綍 `change.md` 骞惰Е鍙戜紭鍖栦换鍔°€?
- 鍛藉悕鍓嶇紑锛氳皟搴︾浉鍏冲彉閲忕粺涓€鍓嶇紑 `rho_`锛堝 `rho_raw`, `rho_f`, `rho_n`锛夛紱鏉冮噸鏄犲皠浣跨敤 `maps.Q_range`, `maps.R_range` 绛夈€?
- 鏂█涓庢暟鍊煎崼澹細鎺ㄨ崘鍦ㄦ洿鏂版ā鍨嬪墠娣诲姞锛歚assert(all(isfinite(upd.A(:))), 'A contains NaN/Inf')` 绛夛紝璋冭瘯闃舵鍙殏鐢ㄣ€?
- 鍙拷婧€э細閲嶈鑴氭湰鏈熬鍙啓鍏?`fprintf('[TRACE] %s generated %s\n', mfilename, out_file);` 渚涙棩蹇楄仛鍚堛€?
