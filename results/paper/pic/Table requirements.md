可以。当前论文中一共规划了 \*\*Table 1–Table 10\*\*。其中 Table 5–Table 8 已经基本成型，Table 1–Table 4、Table 9、Table 10 仍是 placeholder 或需要补全；Table 6–Table 8 虽已有数据，但也需要 Codex 按统一格式和数据源重新核验。



下面这份可以直接作为 \*\*Codex 补全全部表格的技术要求文档\*\* 使用。



\---



\# 论文表格补全总体要求



\## 1. 数据来源原则



所有表格必须从当前项目中的真实文件读取或由真实文件计算得到，不允许手工编造数值。



如果某个表格所需数据不存在，应当：



```text

1\. 不生成假数据；

2\. 在代码运行时明确报错；

3\. 输出缺失字段、缺失文件和建议补充路径；

4\. 不用随机数、示例值、占位值替代表格数据。

```



\---



\## 2. 表格 LaTeX 风格要求



所有表格使用 IEEE 双栏论文风格。优先使用：



```latex

\\begin{table}\[!t]

\\caption{...}

\\label{tab:...}

\\centering

\\footnotesize

\\begin{tabular}{...}

...

\\end{tabular}

\\end{table}

```



若表格过宽，使用：



```latex

\\begin{table\*}\[!t]

...

\\end{table\*}

```



统一要求：



```text

1\. 不使用竖线；

2\. 不使用过度复杂的多层表头；

3\. 数值保留 4 位小数，除非数值极小或需要科学计数法；

4\. 百分比保留 1–2 位小数；

5\. 科学计数法统一写成 5.277 × 10^{-5} 或 LaTeX 的 $5.277\\times10^{-5}$；

6\. 单位写在列名中，不要重复写在每个单元格；

7\. 方法名必须和图例、正文完全一致；

8\. 表格中的指标方向需要在表注或正文中说明，尤其是 accuracy 越大越好、RMSE/MAE/J\_{\\Delta u} 越小越好。

```



推荐使用的表格标签：



```latex

Table 1  \\label{tab:vehicle\_params}

Table 2  \\label{tab:mpc\_settings}

Table 3  \\label{tab:temporal\_task}

Table 4  \\label{tab:model\_configs}

Table 5  \\label{tab:baselines}

Table 6  \\label{tab:main\_results}

Table 7  \\label{tab:multi\_route\_results}

Table 8  \\label{tab:robustness\_results}

Table 9  \\label{tab:causal\_ablation}

Table 10 \\label{tab:computational\_cost}

```



正文中所有 `Table 6`、`Table 8` 等硬编码引用建议改成：



```latex

Table\~\\ref{tab:main\_results}

Table\~\\ref{tab:robustness\_results}

```



\---



\# Table 1. Vehicle parameters and model variables



\## 表格作用



说明 diagonal dual-steer AGV 的主要车辆参数、状态变量、控制输入和坡度变量。该表服务于 Section III-A 和 Fig. 2。



\## 推荐 caption



```latex

\\caption{Vehicle parameters and model variables of the diagonal dual-steer AGV.}

```



\## 推荐表格结构



建议使用如下列：



```text

Category | Symbol | Description | Value | Unit / Note

```



\## 必须包含内容



\### A. 车辆几何和物理参数



应从 Simulink 模型参数、MATLAB 参数脚本或配置文件中读取：



```text

m              vehicle mass

I\_z            yaw moment of inertia

L              vehicle length / wheelbase-related length

W              track width

h\_cg           center-of-gravity height, if used

r\_w            wheel radius, if used

mu             friction coefficient or tire-road coefficient, if used

C\_rr           rolling resistance coefficient, if used

C\_d or drag coefficient, if used

A\_f            frontal area, if used

g              gravitational acceleration

```



只列入模型中实际使用的参数。未使用的参数不要强行加入。



\### B. 状态变量



至少包括论文式 (1) 中的状态：



```text

X              global x-position

Y              global y-position

ψ              heading angle

v              longitudinal velocity

ω              yaw rate

δ\_lf           LF steering angle

δ\_rr           RR steering angle

β              sideslip angle

```



\### C. 控制输入



包括论文式 (2) 中的输入：



```text

F\_cmd          driving force command

ω\_cmd          yaw-rate command

```



\### D. 坡度变量



包括：



```text

θ              true road slope / road grade angle

θ\_k^{sch}      scheduled slope used by LPV-MPC

\\hat{θ}\_k      slope-related estimate from temporal estimator

```



\## 注意事项



```text

1\. 如果参数值无法从项目中定位，不要编造；

2\. 如果表格过长，可以只列关键车辆参数，把状态和输入变量作为“model variables”列入；

3\. Value 列对于状态变量可写 “state variable”，对于输入变量可写 “control input”，不要写假数值；

4\. 单位必须统一：m, kg, kg·m^2, rad, rad/s, N, m/s。

```



\---



\# Table 2. LPV-MPC settings and constraints



\## 表格作用



说明 LPV-MPC 的采样时间、预测/控制时域、权重矩阵、输入约束、输入增量约束和求解器设置。该表服务于 Section III-D 和 Fig. 3。



\## 推荐 caption



```latex

\\caption{LPV-MPC settings and constraints used in the closed-loop simulations.}

```



\## 推荐表格结构



```text

Item | Symbol | Value | Unit / Description

```



\## 必须包含内容



\### A. 时域和采样参数



```text

Sampling time             T\_s

Prediction horizon        N\_p

Control horizon           N\_c

```



其中 (T\_s) 应与全文一致：



```text

T\_s = 0.01 s

```



\### B. 权重矩阵



从 MPC 配置文件读取：



```text

Tracking weight           Q

Input weight              R

Input-increment weight    R\_\\Delta

```



如果矩阵太长，不要把完整矩阵塞入表格。可写成：



```latex

diag(...)

```



或者将主要对角元素列出。



\### C. 输入约束



至少包括：



```text

F\_cmd lower / upper

ω\_cmd lower / upper

```



单位：



```text

F\_cmd: N

ω\_cmd: rad/s

```



\### D. 输入增量约束



必须和 Fig. 8 及式 (23) 保持一致：



```text

ΔF\_max = 400 N

Δω\_max = 0.9 rad/s

```



如果项目中同时有 lower / upper rate limit，则表格写成：



```text

\-ΔF\_max ≤ ΔF\_cmd ≤ ΔF\_max

\-Δω\_max ≤ Δω\_cmd ≤ Δω\_max

```



\### E. 求解器和实现设置



如项目中存在，应列入：



```text

QP solver / MPC solver

Optimization update rate

Constraint handling mode

Warm start setting, if used

```



\## 注意事项



```text

1\. Table 2 必须和 Fig. 8 中 input-limit envelope、normalized input increment 的定义一致；

2\. 不要把训练参数写进 Table 2；

3\. 不要写硬件实时性结论，计算时间应放在 Table 10。

```



\---



\# Table 3. Temporal perception input and task definition



\## 表格作用



说明 ModernTCN / GRU / TCN 使用的输入窗口、输入维度、采样时间、归一化方式和三任务定义。该表服务于 Section IV-B、Fig. 4。



\## 推荐 caption



```latex

\\caption{Temporal perception input window and multi-task output definition.}

```



\## 推荐表格结构



```text

Component | Symbol / Setting | Value | Description

```



\## 必须包含内容



\### A. 输入窗口设置



```text

Window length              L = 128

Input dimension            F = 19

Sampling time              T\_s = 0.01 s

Window duration            1.28 s

Input tensor               Z\_k ∈ R^{128×19}

Normalization              train-set scaler

Split policy               run-level split

```



\### B. 输入特征类别



不要列出 19 个具体特征名称，除非项目中有明确 feature list。建议列类别：



```text

Longitudinal acceleration

Yaw rate

Steering angles

Wheel speeds

Motor-current-related quantities

Velocity-related quantities

Pitch-related estimates

Diagnostic / derived features

```



\### C. 任务定义



```text

Main-condition classification:

flat / stall / slope



Steering-direction classification:

right / straight / left



Slope-related regression:

\\hat{θ}\_k

```



\### D. 控制接口



```text

\\hat{θ}\_k is processed by S(\\cdot) to generate θ\_k^{sch}

Only θ\_k^{sch} enters LPV-MPC scheduler directly

Classification outputs are auxiliary multi-task representation outputs

```



\## 注意事项



```text

1\. 必须明确 classification outputs 不是直接控制量；

2\. 必须明确网络不直接输出 F\_cmd 或 ω\_cmd；

3\. 表格应和 Fig. 4 完全一致：128 steps、19 features、T\_s=0.01 s。

```



\---



\# Table 4. Model configurations of GRU, TCN and ModernTCN



\## 表格作用



说明三种 temporal estimator 的核心结构配置，保证学习模型对比公平。该表服务于 Section IV-F。



\## 推荐 caption



```latex

\\caption{Model configurations of GRU, TCN, and ModernTCN.}

```



\## 推荐表格结构



```text

Model | Temporal encoder | Main configuration | Output heads | Notes

```



或者更细：



```text

Model | Hidden / channels | Layers / blocks | Kernel size | Causal | Parameters | Output heads

```



\## 必须包含模型



```text

GRU

TCN

ModernTCN

```



Causal ModernTCN 不建议放在 Table 4，应该放在 Table 9，因为它是 ablation。



\## 必须包含配置项



从训练配置或模型配置文件读取：



```text

Sequence length

Input dimension

Hidden size / channel number

Number of layers / blocks

Kernel size, if applicable

Dropout, if used

Causal / non-causal setting

Number of parameters

Output heads

Training seed, if fixed

```



\## 输出 heads



三种模型都应使用相同任务输出：



```text

Main-condition classification

Steering-direction classification

Slope-related regression

```



\## 注意事项



```text

1\. 不要声称 ModernTCN 是新网络结构，只说 adapted / used as estimator；

2\. 不要把性能指标写进 Table 4；

3\. 参数量如果项目没有计算脚本，Codex 应自动从 PyTorch model 统计 trainable parameters；

4\. 若某模型没有 kernel size，如 GRU，则填 “--”。

```



\---



\# Table 5. Baseline controllers and estimators



\## 表格作用



说明本文比较的控制器和估计器类别。该表当前已经基本完整，但可以进一步规范。该表服务于 Section V-B。



\## 推荐 caption



```latex

\\caption{Baseline controllers and estimators used for closed-loop comparison.}

```



\## 推荐表格结构



```text

Category | Method | Scheduled slope source | Role

```



\## 推荐内容



```text

No-slope baseline

LPV-MPC theta0

θ\_k^{sch}=0

Nominal zero-slope scheduling



Sensor baseline

LPV-MPC IMU theta

θ\_k^{sch}=θ\_k^{imu}

Simplified sensor-based scheduling



Oracle baseline

LPV-MPC oracle theta

θ\_k^{sch}=θ\_k^{true}

True-slope scheduling upper bound



Learning baseline

GRU

θ\_k^{sch}=S(\\hat{θ}\_k^{GRU})

Recurrent temporal estimator



Learning baseline

TCN

θ\_k^{sch}=S(\\hat{θ}\_k^{TCN})

Conventional convolutional estimator



Proposed method

ModernTCN

θ\_k^{sch}=S(\\hat{θ}\_k^{ModernTCN})

Multi-task temporal scheduling estimator



Ablation

Causal ModernTCN

θ\_k^{sch}=S(\\hat{θ}\_k^{causal})

Offline–closed-loop mismatch analysis

```



\## 注意事项



```text

1\. oracle 必须解释为 upper-bound reference，不是可实际部署方法；

2\. IMU baseline 应说明是 simplified sensor-based baseline；

3\. Causal ModernTCN 只用于 ablation，不参与所有主对比。

```



\---



\# Table 6. Main closed-loop results on the factory logistics showcase path



\## 表格作用



量化主路径闭环结果，支撑 Fig. 6、Fig. 7、Fig. 8。当前表格已有数据，但需要 Codex 重新核验数据来源和格式。



\## 推荐 caption



```latex

\\caption{Main closed-loop results on the factory logistics showcase path.}

```



\## 推荐列



```text

Controller

e\_y RMSE (m)

e\_ψ RMSE (rad)

XY RMSE (m)

J\_{\\Delta u}

Violation rate

θ^{sch} MAE (deg)

```



\## 必须包含方法



顺序建议保持当前论文：



```text

ModernTCN

GRU

TCN

LPV-MPC theta0

LPV-MPC IMU theta

LPV-MPC oracle theta

```



\## 数据计算要求



\### Tracking metrics



从主路径闭环结果读取：



```text

e\_y RMSE

e\_ψ RMSE

XY RMSE

```



\### Control smoothness



```text

J\_{\\Delta u}

```



必须与 Fig. 8(d) 中的 smoothness cost 一致。



\### Violation rate



必须与 Fig. 8(d) 中 black diamond marker 的定义一致。



\### Scheduled-slope MAE



必须使用实际进入 LPV-MPC 的 scheduled slope：



```text

signals.rho\_f\[:, 2]

```



即 conditioning 后的调度信号，不是 raw network output。



计算：



```latex

MAE(θ\_k^{sch} - θ\_k^{true})

```



单位应与 Fig. 7 一致，建议使用 deg。



\## 注意事项



```text

1\. GRU 的 θ^{sch} MAE 可能小于 ModernTCN，但闭环指标更差；表格必须如实保留；

2\. 不要为了突出 ModernTCN 修改排序或删除指标；

3\. Violation rate 很小时使用科学计数法；

4\. 如果 Table 6 和 Fig. 8 的 J\_{\\Delta u} 不一致，必须优先检查计算脚本。

```



\---



\# Table 7. Aggregate closed-loop results over three routes



\## 表格作用



说明多路径泛化结果，支撑 Section VI-C。



\## 推荐 caption



```latex

\\caption{Aggregate closed-loop results over three routes.}

```



\## 推荐列



```text

Controller

Paths

e\_y RMSE mean

e\_ψ RMSE mean

XY RMSE mean

J\_{\\Delta u} mean

Overall rank mean

```



\## 路径范围



必须包含三条路线：



```text

factory logistics showcase

long up/down slope

sharp turn transition

```



`Paths` 列应为：



```text

3

```



\## 方法范围



建议包含：



```text

ModernTCN

LPV-MPC oracle theta

GRU

TCN

LPV-MPC IMU theta

LPV-MPC theta0

```



当前表格按 overall rank 排序，这种排序可以保留。



\## Overall rank mean 计算要求



Codex 必须使用项目现有脚本或结果文件中的 rank 定义，不要重新发明 rank 规则。



如果没有现成 rank，需要在代码中明确：



```text

For each route, rank controllers by selected metrics where lower is better.

Average the ranks across routes and metrics.

```



但最好与项目已有 summary 文件保持一致。



\## 注意事项



```text

1\. 不要把 robustness 结果混入 Table 7；

2\. Table 7 是三路线 aggregate，不是扰动 aggregate；

3\. Table 7 应和 Fig. 5 的三条路线对应。

```



\---



\# Table 8. Robustness aggregate results under disturbance levels



\## 表格作用



量化扰动等级 (d=0,1,2) 下三种 learning-based controllers 的鲁棒性结果，支撑 Fig. 9。



\## 推荐 caption



```latex

\\caption{Robustness aggregate results under disturbance levels.}

```



\## 推荐列



```text

Level

Controller

Cases

e\_y RMSE mean

XY RMSE mean

J\_{\\Delta u} mean

Overall rank mean

```



\## 方法范围



只包含：



```text

ModernTCN

GRU

TCN

```



不建议加入 theta0、IMU、oracle，因为 Fig. 9 和 robustness 小节聚焦 learning-based controllers。



\## 扰动等级



必须包含：



```text

d = 0

d = 1

d = 2

```



\## Cases 定义



当前论文中每个 disturbance level 包含两条路线：



```text

long up/down slope

sharp turn transition

```



所以：



```text

Cases = 2

```



\## 数据一致性要求



Table 8 必须与 Fig. 9 完全一致：



```text

Fig. 9(a) 使用 e\_y RMSE mean

Fig. 9(b) 使用 XY RMSE mean

Fig. 9(c) 使用 J\_{\\Delta u} mean

```



\## 注意事项



```text

1\. GRU 的 J\_{\\Delta u} 可能非单调，不要修正；

2\. ModernTCN 不一定每个 smoothness cost 最小，但 overall rank 最好；

3\. Fig. 9(c) 使用 log scale，表格仍保留原始数值。

```



\---



\# Table 9. Offline perception and causal ablation results



\## 表格作用



支撑 Section VI-H 和 Fig. 10，说明 causal ModernTCN 的离线指标接近 default ModernTCN，但闭环指标显著恶化。



当前 Table 9 仍是 placeholder，需要重点补全。



\## 推荐 caption



```latex

\\caption{Offline perception and causal ModernTCN ablation results.}

```



\## 推荐表格形式



建议使用双栏表 `table\*`，因为指标较多。



推荐列：



```text

Metric group

Metric

Direction

Default ModernTCN

Causal ModernTCN

Causal / Default

```



\## 必须包含两类指标



\### A. Offline perception metrics



```text

Main-condition accuracy

Steering-direction accuracy

Transition-window turn accuracy

Slope MAE

```



推荐写法：



```text

Main acc. (%)

Turn acc. (%)

Trans.-turn acc. (%)

Slope MAE (deg)

```



Direction：



```text

accuracy metrics: ↑

Slope MAE: ↓

```



\### B. Closed-loop metrics on main route



至少包含：



```text

e\_y RMSE (m)

e\_ψ RMSE (rad)

XY RMSE (m)

J\_{\\Delta u}

```



可选加入：



```text

Violation rate

θ^{sch} MAE (deg)

```



Direction：



```text

RMSE / J\_{\\Delta u} / violation / MAE: ↓

```



\## 数据来源要求



Offline metrics 从 offline evaluation 结果读取：



```text

default ModernTCN offline metrics

causal ModernTCN offline metrics

```



Closed-loop metrics 从 causal ablation 主路径闭环结果读取：



```text

default ModernTCN main-route closed-loop summary

causal ModernTCN main-route closed-loop summary

```



\## 与 Fig. 10 的一致性



Fig. 10 中的 normalized ratio 必须来自 Table 9 的 raw values：



```latex

ratio = causal / default

```



对于 accuracy，若 normalized ratio 接近 1，表示离线精度接近。

对于 Slope MAE 和 closed-loop error，ratio 越大表示越差。



\## 注意事项



```text

1\. 不要把 causal ModernTCN 的差闭环表现解释为 causal convolution 一般无效；

2\. Caption 或正文应说明该结果只针对当前 causalization 和训练设置；

3\. Table 9 最好同时给 raw value 和 ratio，否则 Fig. 10 缺少可追溯数据；

4\. 若某 offline metric 不存在，不要编造，删除该行并同步修改 Fig. 10。

```



\---



\# Table 10. Computational feasibility check



\## 表格作用



量化 temporal estimator inference time 和 MPC solve time，仅作为 simulation/desktop feasibility indicator，不作为硬件部署验证。



当前 Table 10 仍是 placeholder，需要补全。



\## 推荐 caption



```latex

\\caption{Computational feasibility check.}

```



\## 推荐表格结构



```text

Component

Metric

Mean

P95

Max

Unit

Platform / Note

```



或者如果数据较少：



```text

Component

Mean time

Maximum time

Unit

Note

```



\## 必须包含内容



\### A. Temporal estimator inference time



建议包括：



```text

ModernTCN core inference

GRU core inference

TCN core inference

Causal ModernTCN core inference, if measured

```



单位：



```text

ms / step

```



\### B. MPC solve time



包括：



```text

LPV-MPC solve time

```



单位：



```text

ms / step

```



\### C. Simulation wrapper overhead



如果项目中有记录，可以列：



```text

MATLAB/Simulink wrapper overhead

Total closed-loop step time

```



但必须和 core inference / MPC solve time 分开，避免误导。



\### D. Sampling time reference



建议加入一行：



```text

Control sampling period T\_s = 10 ms

```



或者在表注中说明。



\## 平台信息



表格或表注中必须说明：



```text

CPU / GPU

MATLAB version or Python/PyTorch version, if available

Operating system, if available

```



如果平台信息不可得，不要编造。可以写：



```text

Desktop simulation platform

```



但不要声称 embedded real-time capability。



\## 注意事项



```text

1\. 不要写 “real-time deployment validated”；

2\. 不要突出 ONNX；

3\. 只说 computational feasibility indicator；

4\. 如果 core inference time 小于采样时间，也只能说 “small compared with simulation sampling period”，不能说已完成硬件实时验证；

5\. Table 10 应与正文 limitations 中 “no HIL or physical AGV experiment” 保持一致。

```



\---



\# Codex 补表执行顺序建议



建议按下面顺序补全：



```text

1\. Table 1：车辆参数和变量

2\. Table 2：LPV-MPC 设置和约束

3\. Table 3：输入窗口和任务定义

4\. Table 4：模型配置

5\. Table 9：offline / causal ablation

6\. Table 10：计算时间

7\. 重新核验 Table 6–Table 8 与图 6–图 10 的一致性

8\. 最后统一更新所有 \\label{} 和正文 \\ref{}

```



\---



\# 最终交付要求



Codex 最终应输出：



```text

1\. 一个 LaTeX 表格文件，例如 tables\_generated.tex；

2\. 一个数据核验脚本，例如 scripts/generate\_tables.py 或 scripts/generate\_tables.m；

3\. 一个日志文件，列出每张表的数据来源文件；

4\. 如果缺少数据，输出 missing\_table\_data\_report.md。

```



`missing\_table\_data\_report.md` 应包含：



```text

Table number

Missing field

Expected source file

Search paths checked

Suggested fix

```



\---



\# 最重要的核验关系



补表后必须检查这些一致性：



```text

Table 3 ↔ Fig. 4:

128 steps, 19 features, T\_s = 0.01 s



Table 6 ↔ Fig. 6:

主路径闭环结果一致



Table 6 ↔ Fig. 7:

θ^{sch} MAE 使用 conditioning 后的 scheduled slope



Table 6 ↔ Fig. 8:

J\_{\\Delta u}、violation rate 与 Fig. 8(d) 一致



Table 7 ↔ Fig. 5:

三条路线一致



Table 8 ↔ Fig. 9:

d=0,1,2 下 e\_y RMSE、XY RMSE、J\_{\\Delta u} 一致



Table 9 ↔ Fig. 10:

normalized ratio 来自 raw values



Table 10 ↔ Section VI-I:

只作为 computational feasibility check，不作为部署验证

```



整体原则是：\*\*表格只补充真实可追溯数据，不额外创造新实验结论。\*\*



