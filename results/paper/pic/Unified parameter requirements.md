下面给你一份**适用于你这篇 IEEE Access 目标论文的图片制作总规范**。它结合 IEEE Author Center/IEEE Access 的硬性要求，以及 `nature-skills/nature-figure` 中强调的“claim-driven、非冗余、多面板证据层级”思路。IEEE 的硬性要求包括：图像常见尺寸为单栏 3.5 inch 或双栏 7.16 inch；非矢量彩色/灰度图应大于 300 dpi，黑白线图应大于 600 dpi；可接受 PS、EPS、PDF、PNG、TIFF 等格式；图中文字最终显示约 9–10 pt；EPS/PS/PDF 中字体应嵌入或转曲。([IEEE Author Center Conferences][1]) IEEE Access 最终稿要求 double-column、single-spaced 格式，且可提交 LaTeX/Word 与 PDF 终稿。([IEEE Access][2])

---

# 一、总体原则：每张图必须服务一个论文论点

每张图都应先回答三个问题：

1. **这张图证明什么？**
   例如 Fig. 3 证明“LPV-MPC 闭环性能受坡度调度失配影响”，Fig. 7 证明“ModernTCN 的 scheduled slope 更接近可用调度信息”。

2. **图中每个子图是否有独立作用？**
   不要把多个重复表达同一结论的曲线堆在一起。`nature-figure` 的核心思想之一就是多面板图应有证据层级，不同 panel 不应回答同一个科学问题。([GitHub][3])

3. **如果删掉这张图，论文结论是否会变弱？**
   如果不会明显变弱，这张图就应合并、简化或删除。

对你的论文而言，图片应围绕四类证据展开：

* 方法框架：overall framework、AGV model、ModernTCN estimator；
* 问题机理：scheduling mismatch；
* 闭环效果：trajectory/errors、scheduled slope、control smoothness；
* 方法论讨论：offline vs closed-loop mismatch。

---

# 二、图像格式与文件类型

## 1. 优先使用矢量图

对于 MATLAB 曲线图、框图、网络结构图、路径图，**优先导出 PDF/EPS/SVG 矢量图**。IEEE Author Center 明确推荐矢量图，因为矢量图在缩放时更清晰；可接受的矢量格式包括 PS、EPS、PDF。([IEEE Author Center Journals][4])

建议：

```text
首选：PDF / EPS
可编辑中间格式：SVG
不推荐：JPG 截图、低分辨率 PNG、PPT 截图
```

## 2. 位图只用于必要情况

如果是仿真界面截图、复杂热力图、照片类图像，可以用 PNG 或 TIFF。IEEE 接受 PS、EPS、PDF、PNG、TIFF；JPEG 通常只适合作者照片，不建议用于论文图。([IEEE Author Center Conferences][1])

## 3. 不要使用截图作为最终图

不建议：

```text
微信截图
屏幕截图
Simulink 截图后直接贴图
Word/PPT 截图
MATLAB figure 窗口截图
```

如果必须展示 Simulink 模型，也应导出为高分辨率 PNG/PDF，并重新整理标注。

---

# 三、分辨率要求

按照 IEEE 要求：

| 图像类型           |     最低要求 |            建议 |
| -------------- | -------: | ------------: |
| 彩色/灰度位图        | >300 dpi |   300–600 dpi |
| 黑白线图、曲线图、表格类线稿 | >600 dpi |   600 dpi 或矢量 |
| MATLAB 曲线图     |     矢量优先 |       PDF/EPS |
| 路径图、框图、网络结构图   |     矢量优先 |   PDF/EPS/SVG |
| 仿真截图/界面图       | >300 dpi | PNG/TIFF，尽量不用 |

IEEE 还提醒，后期单纯提高 dpi 不能真正改善原始低质量图像，所以图必须在生成时就按高分辨率或矢量格式导出。([IEEE Author Center Journals][4])

---

# 四、尺寸要求：单栏、双栏、跨栏

IEEE 常见图宽为：

| 类型  |                 宽度 |
| --- | -----------------: |
| 单栏图 | 3.5 inch / 88.9 mm |
| 双栏图 | 7.16 inch / 182 mm |

这是 IEEE Author Center 和 IEEE 图表指南中给出的常见出版尺寸。([IEEE Author Center Journals][4])

## 你的论文中建议这样分配

| 图                                      | 建议宽度  | 原因                |
| -------------------------------------- | ----- | ----------------- |
| Overall framework                      | 双栏    | 模块多，单栏会拥挤         |
| AGV model                              | 单栏或双栏 | 若结构复杂用双栏，否则单栏     |
| Scheduling mismatch mechanism          | 单栏或双栏 | 简洁机制图可单栏          |
| Multi-task temporal estimator          | 双栏    | 输入窗口、网络、三任务输出需要空间 |
| Simulation routes                      | 双栏    | 三条路径并排展示          |
| Main closed-loop trajectory and errors | 双栏    | 多子图、多曲线           |
| Scheduled slope time histories         | 双栏    | 多方法曲线             |
| Control smoothness and constraints     | 双栏    | 控制输入、输入增量、约束触碰    |
| Offline vs closed-loop mismatch        | 单栏或双栏 | 如果是柱状图，单栏足够       |

## LaTeX 推荐

单栏：

```latex
\begin{figure}[!t]
\centering
\includegraphics[width=\columnwidth]{fig02_agv_model.pdf}
\caption{Configuration of the diagonal dual-steer AGV.}
\label{fig:agv_model}
\end{figure}
```

双栏：

```latex
\begin{figure*}[!t]
\centering
\includegraphics[width=\textwidth]{fig06_main_closed_loop.pdf}
\caption{Main-route closed-loop comparison: (a) XY trajectory, (b) lateral error, and (c) heading error.}
\label{fig:main_closed_loop}
\end{figure*}
```

---

# 五、文件命名规范

建议所有图片文件统一使用：

```text
fig01_overall_framework.pdf
fig02_agv_model.pdf
fig03_scheduling_mismatch.pdf
fig04_temporal_estimator.pdf
fig05_simulation_routes.pdf
fig06_main_closed_loop.pdf
fig07_scheduled_slope.pdf
fig08_control_smoothness.pdf
fig09_robustness.pdf
fig10_offline_closed_loop_mismatch.pdf
```

要求：

* 文件名只用英文小写、数字、下划线；
* 不使用中文；
* 不使用空格；
* 不使用 `final_final_v3.png` 这种临时命名；
* LaTeX `\label{}` 与文件名逻辑一致；
* 图片源文件单独保存，例如 `.fig`、`.m`、`.svg`、`.pptx`，便于后续修改。

建议建立目录：

```text
figures/
├── source/
│   ├── fig06_main_closed_loop.m
│   └── fig06_main_closed_loop.fig
├── export/
│   ├── fig06_main_closed_loop.pdf
│   └── fig06_main_closed_loop.png
└── README_figures.md
```

---

# 六、色彩模式与配色原则

## 1. 色彩模式

IEEE 文献模板说明彩色图可使用 RGB 或 CMYK，灰度图应使用 grayscale，线图可使用灰度或 bitmap 色彩空间。([arXiv][5]) 对你的论文而言，建议统一使用：

```text
屏幕投稿 / IEEE Xplore：RGB
黑白兼容检查：必须做
最终导出：PDF/EPS 矢量图优先
```

## 2. 配色原则

IEEE 图表指南强调不要过度依赖颜色传达信息，应使用高对比度颜色组合，并避免红绿这种色盲不友好的组合。([Proceedings of the IEEE][6])

建议你的论文采用固定颜色映射：

| 方法                          | 建议颜色/线型    |
| --------------------------- | ---------- |
| Reference path / true slope | 黑色实线       |
| ModernTCN                   | 蓝色实线       |
| GRU                         | 橙色虚线       |
| TCN                         | 紫色点划线      |
| LPV-MPC theta0              | 灰色虚线       |
| LPV-MPC IMU theta           | 绿色虚线或深青色   |
| LPV-MPC oracle theta        | 红色实线或黑色细实线 |

注意：不要只靠颜色区分。每条曲线还应配合不同线型或 marker，例如：

```text
ModernTCN: solid
GRU: dashed
TCN: dash-dot
theta0: dotted
IMU: dashed with marker
oracle: solid with thinner line
```

这样即使打印成灰度，也能区分。

---

# 七、字体与字号

IEEE 建议图中文字最终显示约 9–10 pt，并建议使用 Helvetica、Times New Roman、Arial、Cambria、Symbol 等字体；EPS/PS/PDF 中字体需要嵌入或转曲。([IEEE Author Center Conferences][1])

建议你的论文统一：

| 元素                   |       建议字号 |
| -------------------- | ---------: |
| 坐标轴标题                |       9 pt |
| 坐标轴刻度                |       8 pt |
| 图例                   |       8 pt |
| 子图标签 `(a), (b), ...` | 9–10 pt，加粗 |
| 图中注释                 |       8 pt |
| 框图文字                 |     8–9 pt |

字体建议：

```text
Arial 或 Helvetica
数学符号使用 LaTeX 解释器或 Times 风格
全文所有图保持一致
```

MATLAB 中可以统一设置：

```matlab
set(gca, 'FontName', 'Arial', 'FontSize', 8);
xlabel('Time (s)', 'FontName', 'Arial', 'FontSize', 9);
ylabel('Lateral error (m)', 'FontName', 'Arial', 'FontSize', 9);
```

不要在一篇论文中混用宋体、微软雅黑、Times New Roman、Arial、Calibri。

---

# 八、线条、标记与曲线密度

## 1. 线宽

建议：

| 图类型   |         线宽 |
| ----- | ---------: |
| 普通曲线  | 1.0–1.2 pt |
| 参考轨迹  | 1.2–1.5 pt |
| 辅助网格线 | 0.3–0.5 pt |
| 框图边框  | 0.8–1.0 pt |
| 坐标轴线  | 0.8–1.0 pt |

不要使用过细的 0.25 pt 曲线，双栏缩放后会看不清。

## 2. 标记 marker

如果曲线很多，不要每个采样点都加 marker。建议：

```text
长时间序列：只用线型，不用密集 marker
柱状/散点：marker size 4–6 pt
少量关键点：可使用圆点、三角形、方块标记
```

## 3. 曲线数量

单个子图中建议最多 5–6 条曲线。超过这个数量时，应拆成子图或只保留关键方法：

* ModernTCN；
* GRU；
* TCN；
* theta0；
* IMU；
* oracle。

如果曲线太密，可以将 theta0/IMU 放在主图，learning-based 方法放在 inset 或单独子图。

---

# 九、图例 legend 要求

图例原则：

1. 图例不要遮挡关键曲线；
2. 图例文字尽量短；
3. 同一篇论文中方法名称保持一致；
4. 如果多个子图共用一组方法，尽量使用统一图例；
5. 多子图中不要重复放 4 次同样图例。

建议方法名称统一为：

```text
ModernTCN
GRU
TCN
LPV-MPC theta0
LPV-MPC IMU
LPV-MPC oracle
Reference
```

不要在不同图中混用：

```text
Modern-TCN
ModernTCN-small
MTcn
Proposed
```

正文可以说 proposed method，但图例中最好直接写 ModernTCN。

---

# 十、坐标轴、单位与刻度

## 1. 坐标轴必须有物理量和单位

正确写法：

```text
Time (s)
X (m)
Y (m)
Lateral error (m)
Heading error (rad)
Scheduled slope (deg)
Driving force command (N)
Yaw-rate command (rad/s)
```

不建议：

```text
time
error
theta
F
```

## 2. 单位统一

建议你的论文中：

| 变量            | 单位                  |
| ------------- | ------------------- |
| 位置 (X,Y)      | m                   |
| 横向误差 (e_y)    | m                   |
| 航向误差 (e_\psi) | rad                 |
| 坡度 (\theta)   | deg，若模型内部用 rad，图中注明 |
| 时间            | s                   |
| 驱动力           | N                   |
| 横摆角速度/命令      | rad/s               |
| 角度状态          | rad 或 deg，必须统一      |

坡度图中如果用 deg，公式中用 rad，需要在正文或图注说明：

```text
The slope angle is expressed in degrees for visualization.
```

## 3. 坐标范围

同类图应保持一致坐标范围，尤其是对比图：

* 同一指标、不同方法：统一 y 轴范围；
* 同一方法、不同扰动等级：统一 y 轴范围；
* 多路径轨迹图：可以独立范围，但要保证比例不误导。

建议路径图使用：

```text
axis equal
```

否则轨迹形状可能变形。

---

# 十一、子图 panel 规范

多子图建议使用：

```text
(a), (b), (c), (d)
```

并且：

* 子图标签放左上角；
* 字号 9–10 pt；
* 加粗；
* 不要使用中文子图标签；
* 图注中逐一解释每个 panel。

例如：

```latex
\caption{Main-route closed-loop comparison: (a) XY trajectory, (b) lateral error, (c) heading error, and (d) scheduled slope.}
```

对于你的论文，推荐的多子图结构：

| 图                      | 子图建议                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Main closed-loop       | (a) XY trajectory, (b) lateral error, (c) heading error                                       |
| Scheduled slope        | (a) true/scheduled slope, (b) slope error, optional (c) zoomed transition                     |
| Control smoothness     | (a) driving force command, (b) yaw-rate command, (c) input increment, (d) violation indicator |
| Robustness             | (a) (e_y) RMSE, (b) XY RMSE, (c) (J_{\Delta u}), optional (d) rank                            |
| Offline vs closed-loop | (a) offline metric, (b) closed-loop tracking, (c) causal failure trajectory                   |

---

# 十二、图注 caption 要求

IEEE/IEEE Access 模板要求图注放在图下方，表题放在表上方；不要把 caption 放进图片内部，也不要在图片外加边框。([arXiv][7]) IEEE 图表指南还建议图注应清晰简洁，并定义图中所有符号、缩写和颜色编码。([Proceedings of the IEEE][6])

图注应包含：

1. 图展示的对象；
2. 子图含义；
3. 关键缩写解释；
4. 必要单位；
5. 不重复正文的大段结论。

不建议图注写成：

```text
The result of the experiment.
```

推荐：

```latex
\caption{Main-route closed-loop comparison. 
(a) XY trajectory, (b) lateral error, and (c) heading error. 
All controllers are evaluated on the same nonlinear AGV plant and LPV-MPC settings.}
```

---

# 十三、图中是否使用网格线

建议：

* 曲线图可以使用浅灰色网格线；
* 网格线不要比曲线更突出；
* 框图、结构图不使用网格背景；
* 轨迹图可以保留浅网格，便于判断位置；
* 最终投稿前检查灰度打印效果。

MATLAB 推荐：

```matlab
grid on
ax.GridAlpha = 0.15;
ax.LineWidth = 0.8;
```

如果图过于拥挤，可以去掉 minor grid。

---

# 十四、误差图和结果图的统一要求

针对你的论文，建议统一如下：

## 1. 轨迹图

* 参考路径：黑色实线；
* 起点：绿色圆点；
* 终点：红色方块；
* 行进方向：蓝色箭头；
* 学习方法轨迹：不同颜色/线型；
* 坐标轴：(X) (m), (Y) (m)；
* 使用 `axis equal`。

## 2. 误差时间曲线

* 横轴统一 `Time (s)`；
* 纵轴标明误差单位；
* 使用相同时间范围；
* 若 theta0/IMU 误差过大，可使用 inset 展示 learning-based 与 oracle 的细节；
* inset 需要在图注中说明。

## 3. scheduled slope 曲线

* true slope/oracle 应清楚；
* 如果 (\theta^{sch}) 经过 dead-zone 或 rate limit，图注中说明是 scheduled slope 而非 raw output；
* 用 deg 可读性更好，但要和正文说明一致。

## 4. control smoothness 图

至少包括：

* (F_{cmd})；
* (\omega_{cmd})；
* (\Delta u) 或 (J_{\Delta u})；
* 约束边界可用黑色虚线表示。

---

# 十五、图表与正文的一致性

所有图片必须满足：

1. 正文首次提到后再出现；
2. 使用 `Fig.~\ref{}` 引用；
3. 不要写 “the figure below/above”；
4. 不要手动写死图号；
5. 图号按出现顺序排列；
6. 图中变量名与正文公式一致；
7. 图例方法名与表格方法名一致；
8. 图中数据必须来自项目结果，不手动修饰或伪造。

IEEE Access 最终文件还会检查图表和正文对应关系，因此每个图表都应在正文中被明确引用。([IEEE Access][2])

---

# 十六、禁止事项清单

你的论文图片中应避免：

* 使用中文标注；
* 使用截图作为最终图；
* 图中放标题，例如 “Main Closed-Loop Results”；
* 图外加黑色边框；
* 图注写进图像内部；
* 使用红绿作为唯一对比；
* 曲线颜色过浅；
* 字号小于最终 7 pt；
* 图例遮挡曲线；
* 坐标轴没有单位；
* 同一图中方法名称不一致；
* 多个图重复表达同一结论；
* 为了美观平滑曲线而改变数据；
* 对不同方法使用不同坐标范围造成误导。

---

# 十七、建议你这篇论文采用的统一默认参数

如果后面你让我帮你生成 MATLAB 绘图代码，建议统一按下面规范执行：

```text
图像格式：PDF 矢量图优先，另存 PNG 300 dpi 预览
单栏宽度：3.5 inch
双栏宽度：7.16 inch
字体：Arial
坐标轴字号：8 pt
坐标轴标题：9 pt
图例字号：8 pt
线宽：1.1–1.3 pt
marker size：4–5 pt
网格线：浅灰，alpha 约 0.15
背景：白色
颜色：色盲友好，颜色 + 线型双重区分
图中语言：英文
单位：全部写入坐标轴
输出目录：figures/export/
源文件目录：figures/source/
```

---

# 十八、最终投稿前检查表

投稿前每张图逐项检查：

| 检查项                            | 是否通过 |
| ------------------------------ | ---- |
| 是否能说明一个明确论文论点？                 |      |
| 是否已在正文中首次引用？                   |      |
| 图号是否按顺序？                       |      |
| 文件名是否规范？                       |      |
| 是否为 PDF/EPS 矢量图或高分辨率 PNG/TIFF？ |      |
| 若为位图，是否达到 300/600 dpi？         |      |
| 单栏/双栏缩放后文字是否仍清楚？               |      |
| 坐标轴是否有单位？                      |      |
| 图例是否遮挡曲线？                      |      |
| 颜色是否灰度可区分？                     |      |
| 曲线颜色和线型是否全篇一致？                 |      |
| 子图标签是否统一为 (a), (b), ...？       |      |
| 图注是否解释所有缩写、符号和颜色？              |      |
| 图中是否没有中文、标题、截图边框？              |      |
| 数据是否与表格和项目结果一致？                |      |

这套规范后续可以作为你所有图的制作标准。对你当前这篇论文，最重要的是：**矢量输出、双栏适配、英文标注、统一配色、坐标单位完整、图表不重复、每张图都服务一个核心结论。**

[1]: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/improve-your-graphics/ "Improve Your Graphics - IEEE Author Center Conferences"
[2]: https://ieeeaccess.ieee.org/authors/post-acceptance-guide/ "IEEE Access | Post Acceptance Guide for Authors"
[3]: https://github.com/Yuan1z0825/nature-skills "GitHub - Yuan1z0825/nature-skills: 符合nature论文学术表达和科研绘图的Skill · GitHub"
[4]: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/ "Resolution and Size - IEEE Author Center Journals"
[5]: https://arxiv.org/html/2507.02979v1?utm_source=chatgpt.com "Preparation of Papers for IEEE ACCESS"
[6]: https://proceedingsoftheieee.ieee.org/resources/guidelines-for-figures-and-tables/ "Proceedings of the IEEE"
[7]: https://arxiv.org/html/2503.00384v1 "Preparation of Papers for IEEE ACCESS"
