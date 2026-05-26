这版 Fig. 10 **总体方向是正确的，基本符合当前论文中 causal ModernTCN ablation 的叙事目标**：离线指标与默认 ModernTCN 接近，但闭环指标显著恶化，主路径横向误差也出现明显发散。因此，它可以作为 “offline–closed-loop mismatch” 的核心图来使用。

## 1. 内容是否符合当前项目实际？

**基本符合。**

图中三部分逻辑很清楚：

* **(a) Offline perception**：默认 ModernTCN 和 causal ModernTCN 的离线感知指标接近；
* **(b) Closed-loop metrics**：causal ModernTCN 的闭环指标相对默认模型显著恶化；
* **(c) Main-route lateral error**：causal ModernTCN 在主路径横向误差上出现明显偏离，而默认 ModernTCN 保持较小误差。

这与当前论文中 “offline perception metrics are not enough” 和 “causal ModernTCN ablation” 两节的论点一致：**离线分类/回归指标接近，并不能保证闭环控制性能接近**。

但这里有一个需要特别注意的点：Fig. 10 不能被解释成 “causal convolution 一定不适合控制”。它只能说明：**当前这组 causal ModernTCN 改动和训练设置下，离线指标接近默认模型，但闭环表现显著退化**。这一点你正文中已经有类似表述，后续图注也应保持这种谨慎说法。

---

## 2. 是否符合制图技术要求？

**整体符合，但还需要几个关键小修。**

### 优点

1. **结构合理。**
   三个子图分别对应离线指标、闭环指标、时域横向误差，逻辑递进非常清楚。

2. **对比对象简洁。**
   只比较 default ModernTCN 和 causal ModernTCN，没有再加入 GRU/TCN，这样焦点很集中。

3. **颜色选择合理。**
   Default ModernTCN 继续使用蓝色，和前面 Fig. 6–Fig. 9 的 ModernTCN 颜色一致。Causal ModernTCN 使用棕红色虚线，与默认模型区分明显。

4. **Panel (b) 使用 log scale 是合理的。**
   由于 causal closed-loop degradation ratio 跨越几十倍到上百倍，log scale 能避免小柱被完全压扁。

---

## 3. 当前还需要修改的地方

### 3.1 Panel (a) 的指标方向需要说明

Panel (a) 里包含：

* Main acc.
* Turn acc.
* Trans. turn
* Slope MAE

前三个是 accuracy，**越大越好**；但 Slope MAE 是误差，**越小越好**。现在统一写成：

```text
Offline metric (relative to default)
```

读者可能会误以为所有柱子大于 1 都代表更好，或者小于 1 都代表更差。

建议在 x 轴标签或图注中明确方向：

```text
Main acc. ↑
Turn acc. ↑
Trans.-turn acc. ↑
Slope MAE ↓
```

或者在图注中写：

```latex
For offline metrics, larger values are better for the accuracy metrics, while smaller values are better for slope MAE.
```

这是 Fig. 10 最需要补充说明的地方之一。

---

### 3.2 Panel (b) 的 y 轴名称建议修改

当前 panel (b) 的纵轴写的是：

```text
Closed-loop cost (relative to default)
```

但其中包括：

* (e_y) RMSE
* (e_\psi) RMSE
* XY RMSE
* (J_{\Delta u})

前三个是 tracking error metrics，不严格叫 cost。建议改成：

```text
Closed-loop metric
(relative to default)
```

或者更明确：

```text
Closed-loop degradation ratio
(default = 1)
```

我更推荐：

```text
Closed-loop metric
(relative to default)
```

因为它最稳妥。

---

### 3.3 Panel (b) 的最高柱可能贴近顶部

Causal ModernTCN 的 (e_y) RMSE 相对默认模型接近 (10^3)，柱子已经接近 y 轴上边界，而且这个柱子的数值标注似乎不明显。建议：

* y 轴上限稍微提高，比如到 (1.5\times 10^3) 或 (2\times 10^3)；
* 给最高柱添加清晰标注，例如 `1.0e3` 或具体倍率；
* 可以只给 causal bars 标数值，默认 bars 已经有 dashed baseline 表示 1，不一定每个都标 `1`。

这样 panel (b) 会更清楚。

---

### 3.4 `Default baseline` 建议改名

顶部 legend 中有：

```text
Default baseline
```

但图里已经有：

```text
Default ModernTCN
```

二者容易混淆。黑色虚线实际上表示 relative ratio = 1，而不是一个额外控制器。建议改成：

```text
Default ratio (=1)
```

或者：

```text
Default reference (=1)
```

我建议用：

```text
Default reference (=1)
```

这样读者更容易理解它是 panel (a)(b) 的归一化参考线。

---

### 3.5 Panel (c) 可加零误差参考线，但不是必须

Panel (c) 展示横向误差 (e_y)。如果想让横向误差偏离更明显，可以加一条很细的 (e_y=0) 水平参考线。但当前图中默认 ModernTCN 基本贴近零，causal ModernTCN 的偏离已经很明显，不加也可以。

如果加，不建议放入 legend，避免图例更复杂。

---

## 4. 图注建议

建议 Fig. 10 的 caption 写成：

```latex
\caption{Offline--closed-loop mismatch of the causal ModernTCN ablation:
(a) offline perception metrics normalized by the default ModernTCN, 
(b) closed-loop metrics normalized by the default ModernTCN on a logarithmic scale, 
and (c) main-route lateral error. The dashed horizontal line in (a) and (b) denotes 
the default reference ratio of one. For offline metrics, larger values are better 
for the accuracy metrics, whereas smaller values are better for slope MAE.}
```

如果想更强调结论，可以加一句：

```latex
The causal variant remains close to the default model in offline perception metrics, 
but its closed-loop performance deteriorates substantially.
```

不过图注太长的话，这句话放正文更合适。

---

## 5. 正文需要配合说明的内容

在 Section VI-H 或 “Offline perception metrics are not enough” 后面，可以加一句类似：

```latex
Fig.~\ref{fig:offline_closed_loop_mismatch} shows that the causal ModernTCN variant 
has offline perception metrics close to the default ModernTCN, but its closed-loop 
tracking and smoothness metrics deteriorate substantially. This result indicates 
that the tested causal modification changes the feedback behavior of the scheduler, 
even though the window-level perception metrics remain competitive.
```

再补一句避免过度泛化：

```latex
This observation should not be interpreted as a general limitation of causal 
temporal convolution; it only reflects the particular causalization and training 
setting evaluated in this study.
```

你论文当前已经有这个意思，后续插入 Fig. 10 后可以保持这类谨慎表述。

---

## 6. 最终判断

Fig. 10 **可以作为论文插图使用**，但正式插入前建议做四个小修：

1. Panel (a) 标清指标方向，尤其是 `Slope MAE` 是越小越好；
2. Panel (b) y 轴从 `Closed-loop cost` 改成 `Closed-loop metric` 或 `Closed-loop degradation ratio`；
3. `Default baseline` 改成 `Default reference (=1)`；
4. Panel (b) 顶部留出更多空间，并给最高 causal bar 添加清晰倍率标注。

完成这些后，Fig. 10 的图像逻辑会非常清楚：**离线指标接近不代表闭环行为接近**。
