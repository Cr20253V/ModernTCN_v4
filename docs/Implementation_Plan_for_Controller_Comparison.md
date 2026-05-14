# 鎺у埗鍣ㄥ姣旀祴璇曞疄鐜拌鍒掞紙LPVMPC+GRU vs LPVMPC+IMU vs 闈炵嚎鎬PC锛?

鏃ユ湡锛?026-01-02

## 0.1 瀹為獙鍙栧悜澹版槑锛堝姣斿叕骞虫€т笌鐩爣锛?
鏈姣斿疄楠岀殑涓昏鐩爣鏄嚫鏄?**LPVMPC+GRU** 鍦ㄥ潯搴?宸ュ喌浼拌涓庨棴鐜帶鍒惰〃鐜颁笂鐨勪紭鍔裤€傚洜姝わ細

- **IMU 鍒嗘敮灏嗛噰鐢ㄢ€滃急鍩虹嚎鈥濆疄鐜?*锛氫娇鐢ㄦ渶灏忓伐绋嬮噺銆佸彲杩愯涓斿彲瑙ｉ噴鐨勫崟 IMU 鏂规锛岃€岄潪杩芥眰鏈€浼樼殑濮挎€佽瀺鍚?澶氫紶鎰熷櫒铻嶅悎銆?
- **鍘熷洜闇€瑕佸湪鎶ュ憡涓槑纭爣娉?*锛欼MU 浼拌鐞嗚涓婂彲浠ュ仛寰楁洿瀹屽杽锛堜緥濡傚姞鍏ユ洿瀹屾暣鐨勫Э鎬佽瀺鍚?婕傜Щ鎶戝埗锛夛紝浣嗘湰瀹為獙閫夋嫨寮卞熀绾挎槸涓轰簡绐佸嚭 GRU 鐨勪紭鍔夸笌宸ョ▼浠峰€笺€?
- **杈圭晫鏉′欢**锛氬急鍩虹嚎涓嶅簲琚仛鎴愨€滄槑鏄句笉鍚堢悊/鏃犳硶杩愯鈥濈殑绋昏崏浜猴紱搴斾繚璇佸悓涓€缁勮矾寰勪笅鑳界ǔ瀹氶棴鐜紝骞惰緭鍑哄畬鏁存棩蹇楀绾︺€?

璇ュ０鏄庡皢鐢ㄤ簬瑙ｉ噴锛欼MU 鍒嗘敮鍙兘瀛樺湪绱婕傜Щ绛夊眬闄愭€э紝杩欏睘浜庨鏈熺幇璞★紝涓嶄綔涓哄疄鐜扮己闄枫€?

## 0. 鑳屾櫙涓庣洰鏍?
褰撳墠宸ョ▼宸插疄鐜?**LPV-MPC + GRU** 鐢ㄤ簬 AGV 璺緞璺熻釜涓庡潯搴﹁浼拌/璋冨害锛圫imulink 妯″瀷锛歚simulink/LPVMPC_AGV_simulink._GRU.slx`锛夈€傚悗缁渶瑕佸紩鍏ワ細

- **LPVMPC + 鍗旾MU**锛堢敤 IMU 浼拌鍧″害/宸ュ喌锛屾浛浠?GRU 杈撳嚭鐨?`theta_hat`锛?
- **闈炵嚎鎬PC锛圢MPC锛?* 鎺у埗鍣?

骞惰姹傦細

- 鍦?**鐩稿悓鐩爣璺緞** 涓嬶紝瀵规瘮涓夌鎺у埗鏂瑰紡鐨?**鎬ц兘鎸囨爣**
- 瀵规瘮杩囩▼ **鍙鐜?*銆?*鍙壒閲忚繍琛?*銆?*鍙墿灞?*锛堟湭鏉ュ啀鍔犳帶鍒跺櫒涓嶉噸鍐欒瘎浼版鏋讹級


## 1. 鐜版湁宸ョ▼鍙鐢ㄥ熀纭€
宸ョ▼宸插叿澶団€滄壒閲忛棴鐜豢鐪?+ 鎸囨爣瑙ｆ瀽鈥濈殑鍏ュ彛锛?

- 闂幆璇勪及鍏ュ彛鑴氭湰锛歚src/tests/test_closed_loop_performance.m`
  - 鑳芥寜鍦烘櫙/璺緞鎵归噺浠跨湡骞朵粠 `logsout` 涓娊鍙栨寚鏍?
  - 褰撳墠鐢ㄤ簬鈥滃姣斾笉鍚?GRU 鎴栨帶鍒堕厤缃€?
- GRU 鍦ㄧ嚎鎺ㄧ悊灏佽锛歚src/gru/GRU_state_classifier.m`
  - 鑳戒粠 plant 杈撳嚭 `y_raw (31脳1)` 浼拌 `theta_hat`銆乣label_main`銆乣label_turn`
- MPC 鍒涘缓锛歚src/mpc/mpc_setup_single_interp.m`
  - 鍒涘缓 Adaptive MPC 鎺у埗鍣紙鍚彲閫?MD 閫氶亾 theta锛?

鍥犳锛屾湰璁″垝鐨勫叧閿笉鏄€滀粠闆跺啓璇勪及鈥濓紝鑰屾槸锛?

1) **閲囩敤鈥滀笁妯″瀷鍒嗗弶鈥?*锛氫负涓夌鎺у埗绛栫暐鍚勮嚜缁存姢涓€涓豢鐪熸ā鍨嬶紙鍑忓皯鑰﹀悎銆佷究浜庣嫭绔嬭皟鍙?璋冭瘯锛?
2) **缁熶竴鏃ュ織淇″彿濂戠害**锛氫笁涓ā鍨嬪繀椤昏緭鍑哄悓鍚?`logsout` 淇″彿锛屼繚璇佹寚鏍囪В鏋愯剼鏈彲澶嶇敤
3) **缁熶竴鎵归噺杩愯鍏ュ彛**锛氱敤涓€涓?MATLAB 鑴氭湰椹卞姩 model 脳 scenario 脳 repeat 鐨勬壒閲忎豢鐪燂紝骞朵骇鍑虹粺涓€ summary


## 2. 瀵规瘮娴嬭瘯鐨勬€讳綋鏋舵瀯锛堟帹鑽愶細妯″瀷涓夊垎鍙夛級
寤鸿鎶婂姣旀祴璇曟媶鎴愪笁灞傦細

### 2.1 妯″瀷灞傦紙Simulink锛氫笁鍒嗗弶锛?
鐩爣锛氫负涓夌鎺у埗绛栫暐鍒嗗埆缁存姢 3 涓豢鐪熸ā鍨嬶紙鍏ュ彛銆佹棩蹇楀绾︿竴鑷达級锛?

- `LPVMPC_AGV_simulink._GRU.slx`锛歀PVMPC + GRU锛堝熀绾匡級
- `LPVMPC_AGV_simulink_IMU.slx`锛歀PVMPC + 鍗旾MU锛堜粎鏇挎崲鍧″害浼拌閾捐矾锛?
- `LPVMPC_AGV_simulink_NMPC.slx`锛氶潪绾挎€PC锛堢嫭绔嬫帶鍒跺櫒瀛愮郴缁燂級

> 鍛藉悕寤鸿锛氫互涓婁负寤鸿鍛藉悕锛涗綘涔熷彲浠ヤ繚鐣欏師妯″瀷鍚嶏紝鐢?`_GRU/_IMU/_NMPC` 鍚庣紑寤虹珛鍓湰銆?

鍏抽敭瑕佹眰锛堝喅瀹氬姣旇兘鍚﹁嚜鍔ㄥ寲锛夛細
- 涓変釜妯″瀷蹇呴』杈撳嚭 **鍚屽悕** 鐨勪俊鍙峰埌 `logsout`锛堣瑙佺3鑺傗€滄棩蹇椾俊鍙峰绾︹€濓級
- 涓変釜妯″瀷蹇呴』鏀寔鍚屼竴濂椾豢鐪熸敞鍏ュ弬鏁帮細璺緞鍙橀噺 `ref`/`agv_ref_path`銆丼topTime銆佸櫔澹板紑鍏炽€侀殢鏈虹瀛愮瓑

鍙€夛紙闈炲繀椤伙級锛?
- 鏈潵濡傛灉缁存姢鎴愭湰杩囬珮锛屽彲鍐嶅洖鏀朵负鍗曟ā鍨?Variant/Switch锛涗絾棣栨湡浠ヤ笁鍒嗗弶涓轰富锛岄檷浣庤€﹀悎椋庨櫓銆?


### 2.2 杩愯灞傦紙MATLAB 鑴氭湰锛氱粺涓€椹卞姩涓夋ā鍨嬶級
鐩爣锛氭彁渚涚粺涓€鍏ュ彛锛屼竴閿窇瀹岋細

- 妯″瀷闆嗗悎锛堝缓璁敤 map 绠＄悊锛夛細
  - `lpvmpc_gru  -> simulink/LPVMPC_AGV_simulink_GRU`
  - `lpvmpc_imu  -> simulink/LPVMPC_AGV_simulink_IMU`
  - `nmpc        -> simulink/LPVMPC_AGV_simulink_NMPC`
- 璺緞闆嗗悎锛氭潵鑷?`data/paths/path_*.mat` 鎴栬嚜瀹氫箟
- 姣忔潯璺緞閲嶅娆℃暟 N锛堢敤浜庣粺璁″潎鍊?鏂瑰樊锛?

骞朵繚瀛橈細
- 姣忔浠跨湡鐨?`timeseries_*.mat`锛堝彲閫夛級
- 涓€浠藉彲瀵规瘮鐨?`summary.mat`锛堝甫 controller 缁村害锛?

瀹炵幇寤鸿锛堜笌鐜扮姸鑴氭湰鍏崇郴锛夛細
- 涓嶇洿鎺ュ湪 `src/tests/test_closed_loop_performance.m` 涓娾€滅‖鏀瑰埌搴曗€濓紝鑰屾槸浠ュ畠涓哄熀纭€鏂板缓涓€涓剼鏈紙渚嬪 `src/tests/run_controller_comparison_batch.m`锛夛紝鍙繚鐣欏彲澶嶇敤鐨勪俊鍙锋娊鍙栦笌缁撴灉缁撴瀯銆?
- `test_closed_loop_performance.m` 浣滀负鍙傝€?鍥炲綊鑴氭湰淇濈暀锛岄伩鍏嶅奖鍝嶆棦鏈夋祦绋嬨€?


### 2.3 璇勪及/鎶ュ憡灞傦紙鍚庡鐞嗚剼鏈級
鐩爣锛氳鍙栦竴涓垨澶氫釜 `summary.mat`锛岀敓鎴愶細

- 鎸囨爣瀵规瘮琛紙姣忔潯璺緞 脳 姣忕鎺у埗鍣級
- 姹囨€荤粺璁★紙鍧囧€?鏂瑰樊/鏈€宸€硷級
- 鍏抽敭鏇茬嚎瀵规瘮鍥撅紙鍚岃矾寰勫彔鍔狅級


## 3. 缁熶竴鈥滄棩蹇椾俊鍙峰绾︹€濓紙蹇呴』鍏堝喕缁擄級
瑕佸仛鍒拌嚜鍔ㄥ姣旓紝鏈€鍏抽敭鐨勬槸锛氫笁绉嶆帶鍒舵柟寮忚緭鍑哄悓涓€濂?`logsout` 淇″彿鍚嶃€?

鐜版湁 `test_closed_loop_performance.m` 鍐呴儴宸查€氳繃 `signal_names` 鏄犲皠鍋氫簡瑙ｆ瀽锛涘悗缁鎶婂畠鎻愬崌涓?*椤圭洰绾у绾?*銆?

鏈」鐩€夋嫨锛?*鍦?`logsout` 涓粺涓€璁板綍 `diag.*` 鍛藉悕绌洪棿淇″彿**锛堝嵆淇″彿鍚嶅甫 `diag.` 鍓嶇紑锛夈€?

杩欐牱鍋氱殑鍘熷洜锛?
- 浣犲綋鍓嶅凡鎸?`diag.X/diag.e_y/...` 鐨勬柟寮忔坊鍔犳棩蹇楋紝娌跨敤鍙噺灏戝悗缁弽澶嶆敼鍚?
- 璇婃柇淇″彿闆嗕腑鍦ㄥ悓涓€鍛藉悕绌洪棿锛屼究浜庤剼鏈壒閲忔娊鍙栦笌鐗堟湰婕旇繘

寤鸿缁熶竴鑷冲皯鍖呭惈锛?

### 3.1 璺熻釜鐩稿叧
- `diag.X, diag.Y, diag.psi, diag.v, diag.omega`锛堝疄闄呯姸鎬侊級
- `diag.X_ref, diag.Y_ref, diag.psi_ref, diag.v_ref, diag.omega_ref`锛堝弬鑰冿級
- `diag.e_y, diag.e_psi, diag.e_v, diag.e_omega`锛堣宸悜閲忥紝缁熶竴鏉ヨ嚜 Global2PathError锛?

淇″彿鏉ユ簮寤鸿锛堜笌褰撳墠 LPVMPC+GRU 妯″瀷瀵归綈锛夛細
- `diag.X, diag.Y, diag.psi, diag.v, diag.omega`锛氭潵鑷?plant 杈撳嚭鎬荤嚎 `C`锛屽叾椤哄簭鍥哄畾涓?`C=[X, Y, psi, v, omega]`
- `diag.e_y, diag.e_psi, diag.e_v, diag.e_omega`锛氱粺涓€鏉ヨ嚜 `Global2PathError` 杈撳嚭锛堝綋鍓嶅疄鐜颁负 4 缁达級

### 3.2 鎺у埗鐩稿叧
- `diag.F_cmd, diag.omega_cmd`锛堟帶鍒跺櫒杈撳嚭锛?
- `du` 鎴?`dF_cmd/domega_cmd`锛堣嫢鏈夛級
- `sat_flag` 鎴栭ケ鍜屾瘮渚嬶紙鑻ヨ兘璁板綍锛?

### 3.3 浼拌/璋冨害鐩稿叧
- `diag.theta_ground`锛堢湡鍊硷紱鐢ㄤ簬鍒嗘瀽锛屼笉涓€瀹氱粰鎺у埗鍣ㄧ敤锛?
- `diag.theta_hat`锛堟帶鍒跺櫒鏈€缁堜娇鐢ㄧ殑鍧″害浼拌锛涙棤璁烘潵鑷?GRU 杩樻槸 IMU锛岄兘鍙?`theta_hat`锛?
- `diag.rho_f`锛堣皟搴︽护娉㈣緭鍑猴紱褰撳墠妯″瀷涓?`rho_f=[v_f; omega_f; theta_f]`锛?
- `diag.rho_n`锛堝彲閫夛紝浠呯洃鎺?璋冭瘯鐢ㄧ殑褰掍竴鍖栭噺锛涗笉鍙備笌 UpdatePlantModel锛?
- `diag.y_wt, diag.u_wt, diag.du_wt, diag.umin, diag.umax`锛堝彲閫夛細鍦ㄧ嚎鏉冮噸/绾︽潫璋冨害杈撳嚭锛涚敤浜庤В閲婃€ц兘宸紓锛?
- `diag.F_limit`锛堝姏闄愬箙锛屼緵楗卞拰鍗犳瘮璁＄畻锛涜嫢涓婁笅闄愪笉瀵圭О锛屽缓璁悓鏃惰褰曟璐熼檺鎴栧彇缁濆鏈€澶у€硷級

### 3.4 璁＄畻鎬ц兘
- `diag.solve_time_ms`锛堟帶鍒跺櫒姹傝В鑰楁椂锛涘敖閲忔帴杩戜紭鍖栧櫒鏃堕棿锛?
- `diag.total_step_time_ms`锛堝彲閫夛細姣忔鎬昏€楁椂/澧欓挓鏃堕棿锛涘寘鍚ā鍨嬩笌 GRU 鐨勯澶栧紑閿€锛岀敤浜庤В閲婃暣浣撳疄鏃舵€э級

> 璇存槑锛?
> - 瀵逛簬 NMPC锛氶渶瑕佽緭鍑?`diag.solve_time_ms`锛涜嫢鍙涔熻緭鍑?`diag.total_step_time_ms`銆?
> - 瀵逛簬 LPVMPC锛氳嫢鏆傛椂鏃犳硶浠?Adaptive MPC Controller 鍧楃洿鎺ユ嬁鍒版眰瑙ｈ€楁椂锛屽彲鍏堝湪鑴氭湰渚ф祴閲忓苟鍐欏叆缁撴灉缁撴瀯锛涗絾 `diag.total_step_time_ms` 浠嶅彲浣滀负鈥滅鍒扮鑰楁椂鈥濆厛琛岃褰曘€?


## 4. 鎸囨爣浣撶郴锛堝缓璁鐗堝繀閫?+ 鍙€夋墿灞曪級
涓洪伩鍏嶆寚鏍囩垎鐐革紝寤鸿鍒嗕袱灞傘€?

### 4.1 棣栫増蹇呴€夛紙寤鸿瀵规瘮鏈€灏忛泦鍚堬級
**璺熻釜绮惧害**
- 妯悜璇樊 `e_y`锛歊MS銆佸嘲鍊硷紙Peak锛夈€佺ǔ鎬佸潎鍊硷紙鏈€鍚?10% 鏃堕棿绐楋級
- 鑸悜璇樊 `e_psi`锛歊MS銆佸嘲鍊?
- 閫熷害璇樊 `v_ref - v`锛歊MS銆佸嘲鍊?

**鎺у埗浠ｄ环/骞抽『鎬?*
- `|F_cmd|` 宄板€?
- `|omega_cmd|` 宄板€?
- 鎺у埗鍙樺寲鐜?RMS锛堜緥濡?`diff(F_cmd)/Ts`銆乣diff(omega_cmd)/Ts`锛?

**绾︽潫/椴佹鎬?*
- 楗卞拰鍗犳瘮锛歚|F_cmd| > 0.95*F_limit` 鐨勬椂闂存瘮渚?
- 浠跨湡澶辫触/姹傝В澶辫触娆℃暟锛坒easible/optimal 浠ュ瑙嗕负澶辫触锛?

**璁＄畻澶嶆潅搴?*
- 姹傝В鑰楁椂鍧囧€笺€?5鍒嗕綅銆佹渶澶у€?

### 4.2 鍙€夋墿灞曪紙绗簩闃舵鍐嶅姞锛?
- 鑳借€?鍔涘姛锛歚鈭?|F_cmd * v| dt` 鎴栬繎浼煎姛鑰?
- jerk/鑸掗€傛€э細`d虏u/dt虏` 鐨勭粺璁?
- 宸ュ喌璇嗗埆鍑嗙‘鐜囷紙瀵?GRU/IMU 鐨?label 涔熷彲瀵规瘮锛屼絾杩欏睘浜庘€滆瘑鍒郴缁熲€濊瘎浼帮級


## 5. 涓夌鎺у埗鏂瑰紡鐨勫疄鐜拌惤鐐?

### 5.1 LPVMPC + GRU锛堝凡瀛樺湪锛?
- GRU 杈撳嚭锛歚theta_hat`锛堟潵鑷?`GRU_State_Classifier` 鍧楋級
- MPC 浣跨敤锛歚md = theta_hat`锛宍rho=[v,omega,theta_hat]`锛堟垨鍏舵护娉㈢増鏈級

杩欎釜浣滀负鍩虹嚎锛屼笉寤鸿澶ф敼銆?

#### 5.1.1 鍩虹嚎妯″瀷鈥滃叧閿ā鍧楁帴鍙ｂ€濓紙鍩轰簬浣犳彁渚涚殑鎺ョ嚎鍥?浠ｇ爜锛屽缓璁啓鍏ュ姣斿绾︼級
涓轰繚璇?IMU/NMPC 鍒嗗弶妯″瀷鑳藉仛鍒扳€滄渶灏忔敼鍔?+ 瀹屽叏鍙瘮鈥濓紝寤鸿鎶婁笅鍒楁帴鍙ｇ害瀹氭樉寮忓啓鍏ユ湰璁″垝锛屽苟鍦ㄤ笁涓ā鍨嬩腑灏介噺淇濇寔涓€鑷淬€?

**(1) RhoFilter锛堣皟搴﹀彉閲忔护娉級**
- 鍑芥暟绛惧悕锛歚[rho_f, rho_n] = RhoFilter(v_in, omega_in, theta_in, Ts, tau)`
- 杈撳嚭锛歚rho_f=[v_f; w_f; t_f]`锛屽叾涓?`v_f=max(v_in,0)`锛堥€熷害璐熷€艰鎴柇锛夛紝`rho_n` 浠呯敤浜庣洃鎺?
- 褰撳墠鎺ョ嚎纭锛歚theta_in` 浣跨敤 `theta_hat`锛堟潵鑷?GRU 鍦ㄧ嚎浼拌杈撳嚭锛夛紝鍥犳 `rho_f` 鐨勭涓夌淮鏄?`theta_hat` 鐨勪竴闃舵护娉㈠€?
- 瀵规瘮寤鸿锛?
  - 涓変釜妯″瀷缁熶竴璁板綍 `rho_f`锛堜互鍙婂彲閫?`rho_n`锛夛紝鏂逛究瑙ｉ噴鏉冮噸/绾︽潫璋冨害宸紓
  - 鑻ユ湭鏉ュ瓨鍦ㄥ€掕溅/璐熼€熷害鍦烘櫙锛岄渶瑕佽瘎浼?`max(v_in,0)` 鏄惁浼氬紩鍏ヤ笉鍙瘮鎬э紙褰撳墠瀵规瘮璺緞鑻ラ兘涓哄墠杩涳紝鍙厛涓嶆敼锛?

**(2) UpdatePlantModel锛圠PV 鍦ㄧ嚎鎻掑€?+ 鏉冮噸/绾︽潫璋冨害杈撳嚭锛?*
- 鍑芥暟绛惧悕锛歚[plant, y_wt, u_wt, du_wt, ecr_wt, umin, umax] = UpdatePlantModel(rho, db_rt, MPC_idx, ff_rt, v_ff_nom)`
- 鍏抽敭琛屼负锛?
  - `plant.B=[Bmv,Bmd]`锛屾妸鍧″害浣滀负 1 涓?MD 閫氶亾锛坄nd=1`锛?
  - 鍚屾椂杈撳嚭 `y_wt/u_wt/du_wt` 涓?`umin/umax` 渚?Adaptive MPC 浣跨敤
- 椋庨櫓/浼樺寲鐐癸紙浼氬奖鍝嶁€滃姣斿叕骞虫€р€濓級锛?
  - 浣犲綋鍓嶄唬鐮侀噷 `maps_local` 鏄嚱鏁板唴閮ㄧ‖缂栫爜锛坄enable_weight_interp=true`锛屼互鍙婂浐瀹?range/scale锛夈€傝€?PreLoadFcn 鍙堝姞杞戒簡 `maps_best` 骞跺啓鍏?`ctrl.maps`銆?
  - 寤鸿鍦ㄨ鍒掍腑鏄庣‘锛氬姣旂増鏈涔堚€滅粺涓€鐢?maps_best鈫抍trl.maps鈫抦pc_update_from_rho 鐨勮皟搴︹€濓紝瑕佷箞鈥滅粺涓€鐢?UpdatePlantModel 鍐呯疆 maps_local鈥濄€傞伩鍏?GRU/IMU/NMPC 涓夊閫昏緫涓嶄竴鑷村鑷翠笉鍙瘮銆?
  - 寤鸿鎶?`y_wt/u_wt/du_wt/umin/umax` 绾冲叆 `logsout`锛堣嚦灏戜繚瀛樼粺璁￠噺鎴栧叧閿椂鍒伙級锛岀敤浜庡鐩樷€滄€ц兘宸紓鏉ヨ嚜浼拌杩樻槸鏉ヨ嚜璋冨害鑼冨洿鈥濄€?

**(3) Global2PathError锛堣宸悜閲忥級**
- 浣犳彁渚涚殑瀹炵幇瀹為檯杈撳嚭涓?4 缁达細`y_e=[e_y; e_psi; e_v; e_omega]`锛堜唬鐮佹敞閲婇噷鎻愬埌 `e_s`锛屼絾褰撳墠鏈緭鍑猴級
- 瀵规瘮寤鸿锛?
  - 缁熶竴鎶?`e_y/e_psi/e_v/e_omega` 浣滀负鏃ュ織濂戠害鐨勮宸潵婧愶紙涓嶈鍦ㄤ笉鍚屾ā鍨嬮噷閲嶅瀹炵幇涓嶅悓璇樊瀹氫箟锛?
  - 鑻ュ悗缁‘瀹為渶瑕?`e_s`锛堣繘搴﹁宸級锛屽簲鍦ㄤ笁妯″瀷鍚屾澧炲姞骞剁撼鍏ュ绾?

**(4) GRU_State_Classifier锛堝湪绾垮潯搴?宸ュ喌璇嗗埆锛?*
- 褰撳墠 MATLAB Function 閫氳繃 `coder.extrinsic + evalin/assignin` 涓庡熀纭€宸ヤ綔鍖轰氦浜掞紙姣忔鍐?`gru_out_temp` 鍐嶈瀛楁锛夈€?
- 椋庨櫓/浼樺寲鐐癸紙瀵规壒閲忎豢鐪熷奖鍝嶅緢澶э級锛?
  - **骞惰浠跨湡涓嶅畨鍏?*锛歚assignin('base',...)` 浼氬鑷翠笉鍚?worker/涓嶅悓 run 涔嬮棿鐩镐簰瑕嗙洊锛屽熀鏈棤娉曠敤 `parsim` 鍋氬苟琛屻€?
  - **浠跨湡鎬ц兘寮€閿€**锛氶绻?`evalin/assignin` 浼氭樉钁楁嫋鎱豢鐪燂紝褰卞搷鈥滆绠楄€楁椂鈥濇寚鏍囩殑鍏钩瀵规瘮銆?
  - 璁″垝寤鸿锛?
    - 棣栫増瀵规瘮鑻ュ彧鍋氫覆琛?batch锛屽彲鍏堜繚鐣欑幇鐘讹紝浣嗚鍦ㄦ姤鍛婇噷璇存槑鈥淕RU 鍒嗘敮鍖呭惈棰濆 MATLAB 宸ヤ綔鍖哄紑閿€鈥濄€?
    - 鑻ヨ鍋氬叕骞崇殑璁＄畻鑰楁椂瀵规瘮锛屽缓璁妸 GRU block 鏀逛负鈥滄棤 base workspace 鍓綔鐢ㄢ€濈殑杈撳嚭璺緞锛堜緥濡傜洿鎺ヤ粠 `out` 缁撴瀯浣撴彁鍙栨暟鍊硷紝鎴栧皢鎺ㄧ悊灏佽鍒颁笉渚濊禆 base ws 鐨勫嚱鏁版帴鍙ｏ級锛岃繖鏍锋墠鑳藉惎鐢?`parsim` 骞跺噺灏戦澶栧紑閿€銆?

**(5) PreLoadFcn锛堝垵濮嬪寲/鏁版嵁鍔犺浇锛?*
- 褰撳墠 PreLoadFcn 璐熻矗锛歚init_project()`銆佸姞杞?`params/db_rt/ctrl/maps_best/gru_model`銆佸垱寤?`MPCPlantBus`銆?
- 瀵规瘮寤鸿锛?
  - 涓夊垎鍙夋ā鍨嬭淇濇寔鈥滅浉鍚岀殑鍒濆鍖栬涔夆€濓紙灏ゅ叾 `db_rt/ctrl/maps_best`锛夛紝鍚﹀垯鍑虹幇鈥滄ā鍨婣鐢ㄧ殑鏄棫鏁版嵁搴?鏃ф潈閲嶁€濈殑涓嶅彲澶嶇幇闂銆?
  - 鎵归噺浠跨湡鑴氭湰寤鸿閲囩敤锛歚load_system` 涓€娆?+ 灏藉彲鑳戒娇鐢?Fast Restart锛堝墠鎻愭槸妯″瀷缁撴瀯涓嶅彉涓斿彉閲忔敞鍏ユ柟寮忕ǔ瀹氾級銆?


### 5.2 LPVMPC + 鍗旾MU锛堟帹鑽愪綔涓虹涓€姝ユ柊澧烇級
鐩爣锛氫粎鏇挎崲 `theta_hat` 鏉ユ簮锛屼娇瀵规瘮灏藉彲鑳解€滄帶鍒跺彉閲忔硶鈥濄€?

**鍋氭硶寤鸿锛堝急鍩虹嚎锛屾渶灏忓彲琛岋級**锛?
- 閲囩敤鈥滈檧铻虹Н鍒?+ 杞诲井娉勬紡/浣庨€氣€濈殑鏈€绠€ IMU 浼拌锛堝埢鎰忎笉寮曞叆鏇村畬鏁寸殑濮挎€佽瀺鍚堬級锛屼互鍑告樉 GRU 鐨勪紭鍔裤€?
- 鍏蜂綋褰㈠紡鍙部鐢ㄥ伐绋嬩腑宸叉湁鎬濊矾锛堢ず鎰忥級锛?
  - `theta_hat = (1-伪)*theta_hat_prev + 伪*(theta_hat_prev + gyro_y*Ts)`
  - 鎴?`theta_hat = 位*theta_hat_prev + gyro_y*Ts`锛堝甫娉勬紡椤?位<1锛?
  - 鍏朵腑 `gyro_y` 鏉ヨ嚜 `y_raw(10)`锛堝伐绋嬪凡鏈夊畾涔夛級
- 鍦?Simulink IMU 鍒嗗弶妯″瀷鍐呮柊澧炶交閲?`IMU_Theta_Estimator`锛圡ATLAB Function锛夎緭鍑猴細
  - `theta_hat`锛堝崟浣?rad锛涘懡鍚嶄繚鎸佷笌 GRU 鍒嗘敮涓€鑷达紝渚夸簬澶嶇敤 UpdatePlantModel/RhoFilter/鏃ュ織濂戠害锛?

**棰勬湡灞€闄愭€э紙闇€鍦ㄦ姤鍛婁腑鏍囨敞鍘熷洜锛?*锛?
- 浠呴檧铻虹Н鍒嗕細瀛樺湪绱婕傜Щ锛涙湰瀹為獙鎺ュ彈璇ョ幇璞★紝鍥犱负鐩爣鏄獊鍑?GRU 鐨勪紭鍔裤€?
- 鑻ユ紓绉诲鑷撮棴鐜笉绋冲畾锛屽彲寮曞叆鈥滄渶灏忓繀瑕佺殑宸ョ▼鎬х害鏉熲€濓紙浠嶄繚鎸佸急鍩虹嚎瀹氫綅锛夛細
  - `theta_hat` 闄愬箙锛堜緥濡?卤10掳 鎴栨寜妯″瀷瀹為檯鍧″害鑼冨洿璁惧畾锛?
  - 璧峰/鍒嗘閲嶇疆绛栫暐锛堜緥濡傛瘡鏉¤矾寰?run 鍒濆閲嶇疆涓?0锛?
  - 鍙€夛細闈炲父寮辩殑鍥為浂椤癸紙閬垮厤鏃犵晫婕傜Щ锛夛紝浣嗕笉鍋氬鏉傝瀺鍚?

閲嶈绾︽潫锛?
- 瀵规瘮鏃朵繚鎸?MPC 鍙傛暟锛圦/R/dR/绾︽潫绛夛級涓€鑷达紝閬垮厤鎶娾€滀及璁″樊寮傗€濆拰鈥滄帶鍒跺櫒璋冨弬宸紓鈥濇贩鍦ㄤ竴璧枫€?


### 5.3 闈炵嚎鎬PC锛堝疄鐜拌矾绾垮彇鍐充簬宸ュ叿绠憋級
杩欓噷鍒嗕袱鏉¤矾绾匡紝寤鸿鍏堢‘璁や綘鏈満鏄惁鏈?Nonlinear MPC Toolbox锛?

**璺嚎A锛氭湁 Nonlinear MPC Toolbox锛堥閫夛級**
- 鍦?Simulink 涓娇鐢?Nonlinear MPC Controller 鍧楁垨 MATLAB 涓?`nlmpc` 瀵硅薄
- 鐘舵€佹ā鍨嬬敤宸ョ▼鐜版湁鐨?`state_eq.m`锛堟垨 `state_eq_ref.m`锛?
- 杈撳嚭/鍙傝€冧笌绾︽潫鏄犲皠鍒?`F_cmd, omega_cmd`

**璺嚎B锛氭棤宸ュ叿绠憋紙MVP 鏂规锛?*
- 鍏堝湪 MATLAB 鑴氭湰灞傚疄鐜扳€滅绾?浠跨湡寮?NMPC鈥濓紙姣忔 `fmincon` 姹傝В锛?
- 鐢熸垚鍚屾牱鏍煎紡鐨?`sim_out` 鎴栬嚦灏戠敓鎴愭寚鏍囨墍闇€鏃跺簭
- 寰呭彲鐢ㄥ悗锛屽啀鍐冲畾鏄惁闆嗘垚鍥?Simulink

鏃犺鍝潯璺嚎锛屽繀椤绘弧瓒筹細
- 缁熶竴鏃ュ織锛氳緭鍑?`F_cmd, omega_cmd, solve_time_ms, e_y, e_psi, v` 绛?
- 缁熶竴绾︽潫锛氳緭鍏ラ檺骞呫€佸彉鍖栫巼闄愬箙锛堝敖閲忓榻?LPVMPC锛?


## 6. 鎵归噺瀵规瘮鑴氭湰鐨勬敼閫犳柟妗?
寤鸿浠?`src/tests/test_closed_loop_performance.m` 涓哄熀纭€锛屾柊寤鸿剼鏈疄鐜扳€滃妯″瀷椹卞姩鈥濈殑鎵归噺璇勪及鍏ュ彛锛堥伩鍏嶅奖鍝嶇幇鏈夎剼鏈殑鍘嗗彶鐢ㄩ€旓級銆?

寤鸿鑴氭湰鍚嶏細`src/tests/run_controller_comparison_batch.m`锛堝彲璋冩暣锛?

### 6.1 cfg 缁撴瀯浣撴墿灞?
鏂板瀛楁寤鸿锛?
- `cfg.controller_variants`锛氫緥濡?`{'lpvmpc_gru','lpvmpc_imu','nmpc'}`锛堥€昏緫鏍囩锛岀敤浜庣储寮曟ā鍨嬩笌缁撴灉锛?
- `cfg.model_map`锛氫緥濡?`struct('lpvmpc_gru','LPVMPC_AGV_simulink_GRU', 'lpvmpc_imu','LPVMPC_AGV_simulink_IMU', 'nmpc','LPVMPC_AGV_simulink_NMPC')`
- `cfg.seed`锛氶殢鏈虹瀛愶紙淇濊瘉鍣０涓€鑷达級
- `cfg.enable_noise`锛氭槸鍚﹀惎鐢ㄦ祴閲忓櫔澹?
- `cfg.save_timeseries`锛氭瘡娆′豢鐪熸槸鍚︿繚瀛樺畬鏁?`sim_out`

骞跺缓璁柊澧烇紙鐢ㄤ簬鍙鐜颁笌鍏钩瀵规瘮锛夛細
- `cfg.rng_policy`锛氶殢鏈虹瀛愮瓥鐣ワ紙鍥哄畾/娲剧敓锛涜绗?鑺傦級
- `cfg.metrics_window.steady_ratio`锛氱ǔ鎬佺獥鍙ｆ瘮渚嬶紙榛樿 0.10锛?
- `cfg.metrics.enable_core_tracking_metrics`锛氭槸鍚﹁绠?`e_y/e_psi` 绛夋牳蹇冩寚鏍囷紙榛樿 true锛?

### 6.2 澶栧眰寰幆鏀逛负 model(controller) 脳 scenario
鐜扮姸锛氬彧寰幆 scenarios锛堜笖鍙潰鍚戝崟妯″瀷锛夈€?
鏀归€犲悗锛?
1) 寰幆 controller锛堟爣绛撅級
2) 鐢?`cfg.model_map(controller)` 瑙ｆ瀽鍑哄搴旂殑 **Simulink 妯″瀷鍚?*锛屽垎鍒皟鐢?`sim()`
3) 寰幆 scenario锛堝惈閲嶅娆℃暟锛?
4) 姣忔浠跨湡鍓嶆敞鍏?base workspace 鍙橀噺锛堢粺涓€娉ㄥ叆锛屼笁妯″瀷閮借鍏煎锛夛紝渚嬪锛?
  - `ref` / `agv_ref_path`锛堝弬鑰冭矾寰勭粨鏋勪綋锛?
  - `params.enable_noise`锛堟垨鍗曠嫭鐨?`enable_noise`锛?
  - `rng(cfg.seed)`锛堟垨姣忔 run 鍥哄畾 seed 娲剧敓锛?
  - GRU 妯″瀷锛氱‘淇?`gru_model` 宸插姞杞斤紱IMU/NMPC 妯″瀷鍙拷鐣ヨ鍙橀噺浣嗕笉搴旀姤閿?

琛ュ厖寤鸿锛堜笌褰撳墠 GRU block 瀹炵幇鐩稿叧锛夛細
- 濡傛灉鏈潵甯屾湜鍚敤 `parsim` 骞惰锛氬敖閲忛伩鍏嶅湪妯″瀷杩愯杩囩▼涓 base workspace 鍋?`assignin/evalin`锛堣嚦灏戣鎶?GRU/IMU 鐨勫湪绾夸及璁￠摼璺敼涓衡€滄棤鍓綔鐢ㄢ€濓級銆?
- 鑻ュ厛閲囩敤涓茶 batch锛氬缓璁槑纭?`cfg.run_mode='serial'`锛屽苟灏嗏€淕RU鍒嗘敮鐨勯澶?MATLAB 寮€閿€鈥濅笌鈥滄帶鍒跺櫒姹傝В鑰楁椂鈥濆尯鍒嗚褰曪紙渚嬪鍚屾椂璁板綍 `mpc_solve_time_ms` 涓?`total_step_time_ms`锛夈€?

### 6.3 缁撴灉缁撴瀯缁熶竴
寤鸿 summary 鐨勬牳蹇冪粨鏋勶細
- `summary.controllers(i).name`
- `summary.controllers(i).reports{j}`锛堟瘡鏉¤矾寰?閲嶅涓€娆＄殑 report锛?
- `summary.controllers(i).stats`锛堝姣忔潯璺緞涓庢€讳綋鐨勮仛鍚堢粺璁★級

杩欐牱鍚庡鐞嗚剼鏈彧闇€瑕侀亶鍘?`summary.controllers`銆?


## 7. 鎶ュ憡鑴氭湰锛坈ompare_controller_performance.m锛?
寤鸿鏂板锛歚src/tests/compare_controller_performance.m`锛岃亴璐ｏ細

- 杈撳叆锛氫竴涓垨澶氫釜 `closed_loop_summary_*.mat`
- 杈撳嚭锛?
  - 瀵规瘮琛紙.mat + .csv锛?
  - 鏇茬嚎鍥撅紙.png锛?
  - 姹囨€昏鏄庯紙.md 鎴?.txt锛?

鎺ㄨ崘淇濆瓨鐩綍锛歚results/compare/<timestamp>/`銆?


## 8. 閲岀▼纰戜笌楠屾敹鏍囧噯锛堝己鐑堝缓璁寜姝ゆ帹杩涳級

### M0锛氬伐鍏风涓庤矾绾跨‘璁わ紙0.1澶╋級
- 鐩殑锛氭彁鍓嶉攣瀹?NMPC 璺嚎锛岄伩鍏嶅悗鏈熻鍒掑ぇ鏀?
- 寤鸿鎵ц锛?
  - `ver('mpc')`
  - `exist('nlmpc','file')` 鎴?`which nlmpc`锛堟鏌?`nlmpc` 鍑芥暟鏄惁鍙敤锛?
- 楠屾敹锛氭槑纭槸鍚﹀叿澶?Nonlinear MPC Toolbox锛涜嫢缂哄け鍒欑洿鎺ラ噰鐢ㄨ矾绾緽骞跺湪璁″垝涓皟鏁?M5 宸ユ湡棰勬湡

### M1锛氬喕缁撴棩蹇楀绾︼紙1澶╋級
- 楠屾敹锛氬熀绾?`lpvmpc_gru` 鑳借緭鍑哄绾﹀唴鍏ㄩ儴 `logsout` 淇″彿

骞惰鎺ㄨ繘锛堝缓璁悓 M1 瀹屾垚锛夛細
- 鎸囨爣璁＄畻鍑芥暟鍚屾琛ラ綈鏍稿績璺熻釜鎸囨爣锛歚e_y_rms/e_y_peak/e_psi_rms`锛屼互鍙婃帶鍒跺彉鍖栫巼 RMS锛坄diff(F_cmd)/Ts`銆乣diff(omega_cmd)/Ts`锛?
- 鏄庣‘闅忔満绉嶅瓙鏈哄埗骞惰惤鍒?`cfg` 涓?`summary`锛堣绗?鑺傦級

### M2锛氬垱寤轰笁鍒嗗弶妯″瀷楠ㄦ灦锛?.5~1澶╋級
- 楠屾敹锛氫笁涓ā鍨嬮兘鑳藉姞杞藉悓涓€璺緞骞惰窇閫氬埌缁撴潫锛涗笁鑰?`logsout` 鑷冲皯鍖呭惈濂戠害涓€滈鐗堝繀闇€鈥濈殑淇″彿闆嗗悎

### M3锛氬疄鐜?LPVMPC+IMU锛?.5~1澶╋級
- 楠屾敹锛欼MU 鍒嗗弶妯″瀷鍦ㄥ悓涓€璺緞涓嬭兘璺戦€氾紝骞惰緭鍑哄悓鍚?`theta_hat`

### M4锛氭墿灞曟壒閲忎豢鐪熻剼鏈负涓夋帶鍒跺櫒锛?澶╋級
- 楠屾敹锛氫竴鏉″懡浠ゅ彲璺戝畬 controllers脳scenarios脳repeat锛屽苟杈撳嚭 summary

### M5锛氬紩鍏?NMPC锛?~5澶╋紝鍙栧喅浜庡伐鍏风涓庢眰瑙ｇǔ瀹氭€э級
- 楠屾敹锛歂MPC 鍦ㄨ嚦灏?straight + turn 涓ょ被璺緞涓婄ǔ瀹氳繍琛岋紝涓旇€楁椂缁熻鍙緭鍑?

### M6锛氭姤鍛婁笌蹇祴锛?澶╋級
- 楠屾敹锛氳嚜鍔ㄧ敓鎴愬姣旇〃涓庡浘锛涙彁渚?quick config锛堢煭StopTime銆佸皯璺緞锛夊彲蹇€熷洖褰?


## 9. 宸茬‘瀹氬弬鏁?vs 寰呯‘瀹氬弬鏁帮紙鍏堝啓姝绘鏋讹紝渚夸簬鍚庣画钀藉湴锛?

### 9.1 宸茬‘瀹氾紙褰撳墠淇℃伅瓒冲锛屽彲鐩存帴鍐欏叆瀹炵幇锛?
- **plant 杈撳嚭椤哄簭**锛歚C=[X, Y, psi, v, omega]`
- **璋冨害鍙橀噺婊ゆ尝杈撳叆**锛歚RhoFilter.theta_in = theta_hat`
- **璇樊瀹氫箟鏉ユ簮**锛歚Global2PathError` 杈撳嚭 `y_e=[e_y; e_psi; e_v; e_omega]`
- **妯″瀷鍒濆鍖栧叆鍙?*锛歅reLoadFcn 璐熻矗鍔犺浇 `params/db_rt/ctrl/maps_best/gru_model` 涓庡垱寤?`MPCPlantBus`

### 9.2 寰呯‘瀹氾紙闇€瑕佷綘鍚庣画缁欏嚭鏁板€?绛栫暐锛屼絾鐜板湪鍏堟妸瀛楁鍐欒繘璁″垝涓?cfg锛?
- **IMU 寮卞熀绾垮弬鏁?*锛?
  - 娉勬紡/浣庨€氱郴鏁帮細`位` 鎴?`伪`锛堥粯璁?TBD锛?
  - 闄愬箙鑼冨洿锛歚theta_hat` 鐨勬渶灏?鏈€澶у€硷紙榛樿 TBD锛屽缓璁笌鏁版嵁闆?宸ュ喌鑼冨洿涓€鑷达級
  - 閲嶇疆绛栫暐锛氭瘡涓?run 鍒濆鍖栨槸鍚﹀己鍒?`theta_hat=0`锛堥粯璁?TBD锛?
- **鍣０鍙傛暟**锛?
  - `cfg.enable_noise`銆佸櫔澹板己搴︼紙榛樿 TBD锛涗絾蹇呴』鍚?seed 缁戝畾骞惰褰曪級
- **闅忔満绉嶅瓙鏈哄埗锛堝繀椤诲喕缁擄級**锛?
  - `cfg.seed_base`锛堥粯璁?TBD锛?
  - seed 娲剧敓瑙勫垯锛氬缓璁?`seed = seed_base + hash(controller,scenario,repeat)` 鎴栧彲澶嶇幇鐨勬暣鏁版槧灏勶紙榛樿 TBD锛?
  - `summary` 蹇呴』璁板綍姣忔 run 鐨?seed 涓庡櫔澹板紑鍏?
- **鎸囨爣璁＄畻绐楀彛**锛?
  - 绋虫€佺獥鍙ｆ瘮渚?`steady_ratio`锛堝缓璁粯璁?0.10锛岃嫢浣犳湁鍋忓ソ鍙敼锛?
- **璁＄畻鑰楁椂鍙ｅ緞**锛?
  - 璁板綍 `mpc_solve_time_ms`锛堟帶鍒跺櫒姹傝В鑰楁椂锛変笌鍙€?`total_step_time_ms`锛堝惈妯″瀷/GRU 寮€閿€锛夋槸鍚﹂兘闇€瑕侊紙榛樿 TBD锛?


## 9. 椋庨櫓涓庡绛?
- **NMPC 姹傝В鑰楁椂/涓嶅彲琛?*锛氬厛鍋氱煭棰勬祴鍩熴€佷繚瀹堢害鏉熴€佽缃秴鏃朵笌澶辫触鎯╃綒锛涗紭鍏堣窇 straight 鍐嶆墿灞曘€?
- **鏃ュ織淇″彿涓嶉綈瀵艰嚧鑴氭湰鎶ラ敊**锛氬厛鍐荤粨濂戠害鍐嶅紑鍙戞帶鍒跺櫒锛岀己澶变俊鍙峰繀椤诲湪妯″瀷鍐呰ˉ榻愬苟淇濇寔鍚屽悕銆?
- **鍏钩鎬ч棶棰橈紙璋冨弬宸紓锛?*锛氱涓€闃舵寮哄埗浣跨敤鍚屼竴濂楄緭鍏ラ檺骞?鍙樺寲鐜囬檺骞咃紱NMPC 鑻ラ渶瑕佷笉鍚屾潈閲嶏紝蹇呴』鍦ㄦ姤鍛婁腑娉ㄦ槑銆?
- **闅忔満鍣０褰卞搷鍙鐜?*锛氱粺涓€璁剧疆 `rng(cfg.seed)`锛屽苟鍦?summary 涓褰?seed 涓庡櫔澹板紑鍏炽€?


## 10. 寤鸿鐨勪笅涓€姝ワ紙鏈€灏忓彲璺戠増鏈級
浼樺厛鍋氾細
1) 澶嶅埗鐜版湁妯″瀷褰㈡垚涓夊垎鍙夛細`*_GRU / *_IMU / *_NMPC`锛堝厛淇濇寔鍏朵綑閮ㄥ垎涓€鑷达級
2) 鍦ㄤ笁涓ā鍨嬩腑瀵归綈骞堕獙璇佲€滄棩蹇椾俊鍙峰绾︹€濓紙鍏堣鐩栭鐗堝繀閫変俊鍙凤級
3) 鍦ㄦ柊鑴氭湰 `run_controller_comparison_batch.m` 涓疄鐜?`cfg.model_map`锛屾寜 controller 閫夋嫨涓嶅悓妯″瀷鎵归噺杩愯
4) 鍏堣窇 `straight`銆乺epeat=1锛岄獙璇佷笁妯″瀷閮借兘浜у嚭鍙В鏋愮殑 summary

璺戦€氬悗鍐嶅紩鍏?NMPC銆?

---

## 闄勫綍锛氬疄鏂借繘搴︽棩蹇?

### 2026-01-03

#### M0锛氬伐鍏风涓庤矾绾跨‘璁?鉁?
- [x] 妫€鏌?MPC Toolbox 鍙敤鎬?鈥?**鍙敤**
- [x] 妫€鏌?Nonlinear MPC 鍙敤鎬э紙`nlmpc` 鍑芥暟瀛樺湪鎬?鍙皟鐢ㄦ€э級鈥?**鍙敤**
- [x] 纭畾 NMPC 瀹炵幇璺嚎 鈥?**璺嚎A锛堝伐鍏风锛?*

#### M1锛氬喕缁撴棩蹇楀绾︼紙杩涜涓級

**宸窛鍒嗘瀽瀹屾垚**锛?
- 鐜版湁 `test_closed_loop_performance.m` 鐨?`default_signal_names()` 浠呮槧灏?**7 涓?*淇″彿锛?
  - `v`, `v_ref`, `theta_hat`, `theta_ground`, `theta_ref`, `label_main`, `F_cmd`
- 瀵规瘮璁″垝濂戠害闇€琛ラ綈绾?**15 涓?*淇″彿

**Simulink 淇″彿鏃ュ織宸叉坊鍔?*锛?
- [x] 璺熻釜鐘舵€侊細`diag.X`, `diag.Y`, `diag.psi`, `diag.v`, `diag.omega`
- [x] 璺緞璇樊锛歚diag.e_y`, `diag.e_psi`, `diag.e_v`, `diag.e_omega`
- [x] 鍙傝€冨€硷細`diag.X_ref`, `diag.Y_ref`, `diag.psi_ref`, `diag.v_ref`, `diag.omega_ref`
- [x] 鎺у埗杈撳嚭锛歚diag.F_cmd`, `diag.omega_cmd`
- [x] 浼拌/璋冨害锛歚diag.theta_hat`, `diag.theta_ground`, `diag.label_main`
- [ ] 姹傝В鑰楁椂锛歚diag.solve_time_ms` 鈥?**鏆傛湭瀹炵幇**锛堜紭鍏堝湪鑴氭湰灞傞潰娴嬮噺/璁板綍锛?
- [ ] 姣忔鎬昏€楁椂锛歚diag.total_step_time_ms` 鈥?**鏆傛湭瀹炵幇**锛堣剼鏈眰闈㈡洿鏄撳厛琛屽疄鐜帮紝鐢ㄤ簬绔埌绔疄鏃舵€у姣旓級

**寰呭畬鎴?*锛?
- [ ] 鏂板缓 `run_controller_comparison_batch.m`锛堝惈鏂扮殑 `default_signal_names()` 鍜?`analyze_results`锛?
- [ ] 鎵╁睍鎸囨爣璁＄畻鏀寔 `e_y_rms`, `e_psi_rms`, 鎺у埗鍙樺寲鐜?RMS

**鎶€鏈喅绛栬褰?*锛?
1. 鎸夎鍒?2.2 鑺傦紝鏂板缓鐙珛鑴氭湰鑰岄潪淇敼 `test_closed_loop_performance.m`
2. 姹傝В鑰楁椂棣栫増璁句负鍙€夛紝绛変笁绉嶆帶鍒跺櫒璺戦€氬悗鍐嶇粺涓€琛ュ厖

