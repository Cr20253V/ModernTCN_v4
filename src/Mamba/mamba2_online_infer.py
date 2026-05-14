"""
脚本名称: mamba2_online_infer.py
版本: V1.0
最后修改时间: 2026-04-01

功能概述:
    Mamba-2 多任务模型的在线推理封装，供 MATLAB Simulink 仿真调用。
    核心类 Mamba2OnlineInfer 封装了模型加载、归一化与前向推理逻辑；
    同时提供模块级函数 infer_window() 供 MATLAB py.* 接口直接调用；
    以及 CLI 入口，便于脱离 Simulink 的命令行验证。

============================================================
一、接口规范
============================================================

1. 输入窗口格式
   - shape : [128, 10]，numpy float32 或 float64
   - 128   : 时间步数（序列长度，与训练时 L=128 一致）
   - 10    : 通道数，**通道顺序不可改变**

   通道索引与物理含义
   ----------------------------------------------------------------
   索引  名称          单位     物理含义
   ----  ----------    ------   --------------------------------
   [0]   accel_x       m/s²     纵向（前进方向）加速度
   [1]   gyro_y        rad/s    IMU 俯仰轴角速度
   [2]   gyro_z        rad/s    IMU 偏航轴角速度
   [3]   I_lf          A        左前轮电机相电流（有效值）
   [4]   I_rr          A        右后轮电机相电流（有效值）
   [5]   omega_w_lf    rad/s    左前轮轮速（角速度）
   [6]   omega_w_rr    rad/s    右后轮轮速（角速度）
   [7]   slip_lf       -        左前轮纵向滑移率（离线计算）
   [8]   slip_rr       -        右后轮纵向滑移率（离线计算）
   [9]   accel_y       m/s²     横向加速度

   注意：在线仿真时，slip_lf / slip_rr 若无法实时获取，
         可先用 0.0 填充，但须知这会降低分类头精度。

2. 归一化参数来源
   mu / sigma 存储于训练数据集文件 Mamba_dataset_export.mat（HDF5格式）
   的 'mu'/'sigma' 键下，shape 均为 [10]，对应 10 个输入通道。
   建议初始化前先调用 static 方法 extract_and_save_mu_sigma() 将
   mu/sigma 导出为独立的 mu_sigma.npz 文件，避免推理时依赖完整数据集。

3. 模型结构参数（来自 agv_mamba2_baseline 训练配置）
   ----------------------------------------------------------------
   参数          值      含义
   ---------     ---     ----------------------------------------
   model_name    mamba2  骨干网络类型
   input_dim     10      输入通道数
   d_model       128     隐层宽度
   n_layers      4       Mamba2 块数量
   dropout       0.1     训练时 Dropout（推理时自动关闭）
   d_state       64      SSM 状态维数
   d_conv        4       卷积核长度
   expand        2       扩展因子

4. 输出格式（dict）
   ----------------------------------------------------------------
   键             类型     含义
   ---------      ------   ----------------------------------------
   theta_hat      float    坡度角估计 [rad]，取序列末端时间步
   delta_hat      float    曲率倒数估计 [1/m]，取序列末端时间步
   label_main     int      主工况  ∈ {1, 2, 3}
                           1=平路(flat)  2=堵转(stall)  3=坡道(slope)
   label_turn     int      转弯状态 ∈ {-1, 0, 1}
                           -1=右转  0=直行  1=左转
   label_slip     int      打滑标签 ∈ {0, 1}
                           0=正常  1=打滑
   label_stall    int      堵转标签 ∈ {0, 1}
                           0=正常  1=堵转
   prob_main      list[3]  主工况 softmax 概率 [P(flat), P(stall), P(slope)]
   prob_turn      list[3]  转弯  softmax 概率 [P(right), P(straight), P(left)]
   prob_slip      list[2]  打滑  softmax 概率 [P(0), P(1)]
   prob_stall     list[2]  堵转  softmax 概率 [P(0), P(1)]

5. 标签映射（与训练代价函数保持严格一致）
   - label_main = argmax(logits_main[-1]) + 1   # 训练时 y_main-1 作为类别索引
   - label_turn = argmax(logits_turn[-1]) - 1   # 训练时 y_turn+1 作为类别索引
   - label_slip = argmax(logits_slip[-1])        # 直接使用
   - label_stall= argmax(logits_stall[-1])       # 直接使用
   取 [-1] 表示取序列最末时间步的预测，即对当前窗口最后一帧的状态估计。

============================================================
二、典型调用方式
============================================================

方式 A — Python 模块导入（推荐用于 WSL / Windows 纯 Python 测试）:
    from mamba2_online_infer import Mamba2OnlineInfer
    infer = Mamba2OnlineInfer(
        checkpoint_path="results/mamba/train/agv_mamba2_baseline/best.pt",
        mu_sigma_path="results/mamba/train/agv_mamba2_baseline/mu_sigma.npz",
        device="cpu",
    )
    window = np.zeros((128, 10), dtype=np.float32)  # 实际替换为真实传感器数据
    result = infer.infer(window)
    print(result["theta_hat"], result["label_main"])

方式 B — MATLAB py.* 调用（要求 Windows Python 已安装 mamba_ssm 及依赖）:
    % MATLAB 示例（在 Mamba_state_classifier.m 中封装此逻辑）
    persistent mamba_infer
    if isempty(mamba_infer)
        mamba_infer = py.mamba2_online_infer.Mamba2OnlineInfer( ...
            py.str(ckpt_path), py.str(mu_sigma_path), py.str('cpu'));
    end
    flat_list  = py.list(reshape(window_128x10, 1, [])');  % 1280×1
    result_py  = mamba_infer.infer_flat(flat_list);             % 返回 Python dict
    theta_hat  = double(result_py{'theta_hat'});

方式 C — 命令行 JSON 接口（脱 Simulink 集成验证）:
    python mamba2_online_infer.py \\
        --checkpoint results/mamba/train/agv_mamba2_baseline/best.pt \\
        --mu-sigma   results/mamba/train/agv_mamba2_baseline/mu_sigma.npz \\
        --input      window_test.npy

    # 输入文件 window_test.npy: shape [128, 10]，np.float32
    # 输出: JSON 字符串打印到 stdout

方式 D — 导出归一化参数（首次部署前执行一次）:
    python mamba2_online_infer.py \\
        --extract-scaler \\
        --dataset  data/mamba/Mamba_dataset_export.mat \\
        --mu-sigma results/mamba/train/agv_mamba2_baseline/mu_sigma.npz

============================================================
三、MATLAB/Python 环境要求
============================================================

Windows 侧 Python 直接调用时需要：
    * Python 3.9+ (与 MATLAB 版本兼容, 验证命令: pyenv)
    * torch >= 2.0  (CPU 版本即可)
    * numpy, h5py, scipy
    * mamba_ssm 本地源码（位于 src/Mamba/model/mamba/）已在 sys.path 中
      注意: mamba2 的 SSM scan 在纯 CPU 模式下使用 PyTorch 原生实现，
            无需 CUDA / Triton，Windows CPU 可正常运行。

WSL Python 间接调用时：
    * 在 WSL 中运行的 Python 具备完整 CUDA/Triton 环境
    * MATLAB 通过 TCP socket 与 WSL Python 通信
    * 请参考 Mamba_state_classifier.m 中的 socket 桥接模式说明

============================================================
四、依赖文件清单
============================================================

    文件路径（相对 src/Mamba/）
    ----------------------------------------------------------------
    results/mamba/train/agv_mamba2_baseline/best.pt    必须存在
    results/mamba/train/agv_mamba2_baseline/mu_sigma.npz
            或 data/mamba/Mamba_dataset_export.mat（HDF5，用于提取 mu/sigma）
    model/mamba/mamba_ssm/modules/mamba2.py            必须可 import
    model/mamba/mamba_ssm/modules/mamba_simple.py      （同上）
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path
from types import MethodType
from typing import Dict, List, Union

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange


# ──────────────────────────────────────────────────────────────
#  确保本地 mamba_ssm 源码包可被 import
# ──────────────────────────────────────────────────────────────
_THIS_DIR = Path(__file__).resolve().parent
_MAMBA_PKG_ROOT = _THIS_DIR / "model" / "mamba"
if str(_MAMBA_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_MAMBA_PKG_ROOT))


def _mamba2_cpu_token_step(layer: nn.Module, conv_state: torch.Tensor, ssm_state: torch.Tensor,
                           zxbcdt_t: torch.Tensor) -> torch.Tensor:
    """Mamba2 单步纯 PyTorch 参考实现，仅用于 CPU 在线推理。"""

    from mamba_ssm.ops.triton.layernorm_gated import rms_norm_ref  # type: ignore

    dtype = zxbcdt_t.dtype
    d_mlp = (zxbcdt_t.shape[-1] - 2 * layer.d_ssm - 2 * layer.ngroups * layer.d_state - layer.nheads) // 2
    z0, x0, z, xBC, dt = torch.split(
        zxbcdt_t,
        [d_mlp, d_mlp, layer.d_ssm, layer.d_ssm + 2 * layer.ngroups * layer.d_state, layer.nheads],
        dim=-1,
    )

    conv_state.copy_(torch.roll(conv_state, shifts=-1, dims=-1))
    conv_state[:, :, -1] = xBC
    xBC = torch.sum(conv_state * rearrange(layer.conv1d.weight, "d 1 w -> d w"), dim=-1)
    if layer.conv1d.bias is not None:
        xBC = xBC + layer.conv1d.bias
    xBC = layer.act(xBC).to(dtype=dtype)

    x, B, C = torch.split(xBC, [layer.d_ssm, layer.ngroups * layer.d_state, layer.ngroups * layer.d_state], dim=-1)
    A = -torch.exp(layer.A_log.float())

    if layer.ngroups != 1:
        raise RuntimeError(f"CPU fallback 暂只支持 ngroups=1，当前为 {layer.ngroups}")

    dt = F.softplus(dt + layer.dt_bias.to(dtype=dt.dtype))
    dA = torch.exp(dt * A)
    x = rearrange(x, "b (h p) -> b h p", p=layer.headdim)
    dBx = torch.einsum("bh,bn,bhp->bhpn", dt, B, x)
    ssm_state.copy_(ssm_state * rearrange(dA, "b h -> b h 1 1") + dBx)
    y = torch.einsum("bhpn,bn->bhp", ssm_state.to(dtype), C)
    y = y + rearrange(layer.D.to(dtype), "h -> h 1") * x
    y = rearrange(y, "b h p -> b (h p)")

    if layer.rmsnorm:
        y = rms_norm_ref(
            y,
            layer.norm.weight,
            None,
            z=z,
            eps=layer.norm.eps,
            group_size=layer.d_ssm // layer.ngroups,
            norm_before_gate=layer.norm_before_gate,
        )
    else:
        y = y * layer.act(z)

    if d_mlp > 0:
        y = torch.cat([F.silu(z0) * x0, y], dim=-1)
    return layer.out_proj(y)


def _mamba2_cpu_forward(layer: nn.Module, u: torch.Tensor, seqlen=None, seq_idx=None,
                        cu_seqlens=None, inference_params=None):
    """Mamba2 的纯 CPU 前向实现，按时间步扫描以避开 CUDA/Triton 专用算子。"""

    if seqlen is not None or seq_idx is not None or cu_seqlens is not None or inference_params is not None:
        raise NotImplementedError("CPU fallback 仅支持标准前向: input shape [B, L, D]")

    batch, seqlen, _ = u.shape
    zxbcdt = layer.in_proj(u)
    conv_state = torch.zeros(batch, layer.conv1d.weight.shape[0], layer.d_conv, device=u.device, dtype=u.dtype)
    ssm_state = torch.zeros(batch, layer.nheads, layer.headdim, layer.d_state, device=u.device, dtype=u.dtype)
    outputs = []
    for t in range(seqlen):
        y_t = _mamba2_cpu_token_step(layer, conv_state, ssm_state, zxbcdt[:, t, :])
        outputs.append(y_t.unsqueeze(1))
    return torch.cat(outputs, dim=1)


def _enable_cpu_fallback_if_needed(model: nn.Module, device: torch.device) -> bool:
    """在 CPU 上为 Mamba2 层打补丁，替换为纯 PyTorch 前向。"""

    if device.type != "cpu":
        return False

    patched = 0
    for blk in getattr(model, "blocks", []):
        layer = getattr(blk, "layer", None)
        if layer is None:
            continue
        if layer.__class__.__name__ != "Mamba2":
            continue
        layer.forward = MethodType(_mamba2_cpu_forward, layer)
        patched += 1
    return patched > 0


# ──────────────────────────────────────────────────────────────
#  模型定义（与 train_agv_mamba.py 保持严格一致）
# ──────────────────────────────────────────────────────────────

class ResidualMambaBlock(nn.Module):
    """PreNorm + Residual 封装层，适配 Mamba1/2/3。"""

    def __init__(self, d_model: int, layer: nn.Module, dropout: float = 0.0):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.layer = layer
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.layer(self.norm(x))
        y = self.dropout(y)
        return x + y


class AGVMambaMultiTaskModel(nn.Module):
    """
    AGV 时序多任务模型，骨干为 mamba2。

    输入:  x  [B, L, input_dim]
    输出:  dict，各 key 对应逐时间步预测
    """

    def __init__(
        self,
        model_name: str,
        input_dim: int,
        d_model: int,
        n_layers: int,
        dropout: float,
        d_state: int,
        d_conv: int,
        expand: int,
        # mamba3 相关参数保留以便从 checkpoint args 中兼容加载
        mamba3_headdim: int = 64,
        mamba3_mimo: bool = False,
        mamba3_mimo_rank: int = 4,
    ):
        super().__init__()
        self.model_name = model_name.lower()

        if self.model_name == "mamba1":
            from mamba_ssm.modules.mamba_simple import Mamba  # type: ignore
            layer_cls = lambda i: Mamba(d_model=d_model, d_state=d_state, d_conv=d_conv, expand=expand, layer_idx=i)
        elif self.model_name == "mamba2":
            from mamba_ssm.modules.mamba2 import Mamba2  # type: ignore
            layer_cls = lambda i: Mamba2(d_model=d_model, d_state=d_state, d_conv=d_conv, expand=expand, layer_idx=i)
        else:
            raise ValueError(f"推理脚本仅支持 mamba1/mamba2，当前: {model_name}")

        self.in_proj = nn.Linear(input_dim, d_model)
        self.blocks = nn.ModuleList([
            ResidualMambaBlock(d_model=d_model, layer=layer_cls(i), dropout=dropout)
            for i in range(n_layers)
        ])
        self.out_norm = nn.LayerNorm(d_model)

        # 回归头
        self.head_theta = nn.Linear(d_model, 1)
        self.head_delta = nn.Linear(d_model, 1)

        # 分类头
        self.head_main  = nn.Linear(d_model, 3)   # flat/stall/slope
        self.head_turn  = nn.Linear(d_model, 3)   # right/straight/left
        self.head_slip  = nn.Linear(d_model, 2)   # 0/1
        self.head_stall = nn.Linear(d_model, 2)   # 0/1

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        h = self.in_proj(x)
        for blk in self.blocks:
            h = blk(h)
        h = self.out_norm(h)
        return {
            "theta": self.head_theta(h).squeeze(-1),   # [B, L]
            "delta": self.head_delta(h).squeeze(-1),   # [B, L]
            "main":  self.head_main(h),                # [B, L, 3]
            "turn":  self.head_turn(h),                # [B, L, 3]
            "slip":  self.head_slip(h),                # [B, L, 2]
            "stall": self.head_stall(h),               # [B, L, 2]
        }


# ──────────────────────────────────────────────────────────────
#  核心推理类
# ──────────────────────────────────────────────────────────────

class Mamba2OnlineInfer:
    """
    Mamba-2 在线推理封装。

    使用示例:
        infer = Mamba2OnlineInfer(
            checkpoint_path="results/mamba/train/agv_mamba2_baseline/best.pt",
            mu_sigma_path="results/mamba/train/agv_mamba2_baseline/mu_sigma.npz",
            device="cpu",
        )
        result = infer.infer(window_128x10_np)

    线程安全性:
        单个实例非线程安全，每个线程请创建独立实例。
    """

    #: 与训练完全一致的通道名称，顺序不可修改
    CHANNEL_NAMES: List[str] = [
        "accel_x", "gyro_y", "gyro_z",
        "I_lf", "I_rr",
        "omega_w_lf", "omega_w_rr",
        "slip_lf", "slip_rr",
        "accel_y",
    ]

    SEQ_LEN: int = 128   # 时间窗口长度，与训练时一致
    N_CHANNELS: int = 10  # 输入通道数

    def __init__(
        self,
        checkpoint_path: Union[str, Path],
        mu_sigma_path: Union[str, Path],
        device: str = "cpu",
    ) -> None:
        """
        初始化推理器。

        参数:
            checkpoint_path : best.pt 路径，来自 agv_mamba2_baseline 训练目录
            mu_sigma_path   : mu_sigma.npz 路径，由 extract_and_save_mu_sigma() 生成
                              或 Mamba_dataset_export.mat (HDF5) 路径，自动提取
            device          : "cpu" 或 "cuda"；MATLAB 调用时建议 "cpu"

        异常:
            FileNotFoundError : checkpoint 或 mu_sigma 文件不存在
            RuntimeError      : 模型加载失败（结构不匹配等）
        """
        self.device = torch.device(device)
        self._eps = 1e-8

        # ── 1. 加载 mu/sigma ──────────────────────────────────────
        mu_sigma_path = Path(mu_sigma_path)
        if not mu_sigma_path.exists():
            raise FileNotFoundError(f"mu/sigma 文件不存在: {mu_sigma_path}")

        if mu_sigma_path.suffix in (".mat", ""):
            # HDF5 格式（Mamba_dataset_export.mat）
            self.mu, self.sigma = self._load_mu_sigma_from_hdf5(mu_sigma_path)
        elif mu_sigma_path.suffix == ".npz":
            data = np.load(str(mu_sigma_path))
            self.mu    = data["mu"].astype(np.float32).reshape(1, 1, -1)   # [1,1,10]
            self.sigma = data["sigma"].astype(np.float32).reshape(1, 1, -1)
        else:
            raise ValueError(
                f"mu_sigma_path 须为 .npz 或 .mat 文件，当前: {mu_sigma_path.suffix}"
            )

        if self.mu.shape[-1] != self.N_CHANNELS:
            raise RuntimeError(
                f"mu 维度与通道数不符：期望 {self.N_CHANNELS}，实际 {self.mu.shape[-1]}"
            )

        # ── 2. 加载 checkpoint ─────────────────────────────────────
        checkpoint_path = Path(checkpoint_path)
        if not checkpoint_path.exists():
            raise FileNotFoundError(f"checkpoint 不存在: {checkpoint_path}")

        ckpt = torch.load(str(checkpoint_path), map_location=self.device, weights_only=False)
        train_args: dict = ckpt["args"]

        # ── 3. 重建模型结构 ────────────────────────────────────────
        self.model = AGVMambaMultiTaskModel(
            model_name = train_args["model"],
            input_dim  = 10,
            d_model    = train_args["d_model"],
            n_layers   = train_args["n_layers"],
            dropout    = train_args["dropout"],
            d_state    = train_args["d_state"],
            d_conv     = train_args["d_conv"],
            expand     = train_args["expand"],
            mamba3_headdim   = train_args.get("mamba3_headdim",   64),
            mamba3_mimo      = train_args.get("mamba3_mimo",      False),
            mamba3_mimo_rank = train_args.get("mamba3_mimo_rank", 4),
        )
        self.model.load_state_dict(ckpt["model"])
        self.model.to(self.device)
        self.model.eval()

        self._cpu_fallback_enabled = _enable_cpu_fallback_if_needed(self.model, self.device)

        self._model_name = train_args["model"]
        print(
            f"[Mamba2OnlineInfer] 加载完成 | 模型={self._model_name} | "
            f"epoch={ckpt.get('epoch','?')} | device={self.device} | "
            f"mu={self.mu.flatten()[:3]}..."
        )
        if self._cpu_fallback_enabled:
            print("[Mamba2OnlineInfer] 已启用 Mamba2 CPU fallback（纯 PyTorch，速度较慢但可在线推理）")

    # ──────────────────────────────────────────────────────────
    #  主推理接口
    # ──────────────────────────────────────────────────────────

    @torch.no_grad()
    def infer(self, window: np.ndarray) -> Dict:
        """
        对一个完整窗口执行多任务推理，取序列最后一步作为输出。

        参数:
            window : numpy 数组, shape [128, 10], float32 或 float64
                     原始（未归一化）传感器数据

        返回:
            dict，包含:
                theta_hat (float),  delta_hat (float)
                label_main (int ∈{1,2,3}),  label_turn (int ∈{-1,0,1})
                label_slip (int ∈{0,1}),     label_stall (int ∈{0,1})
                prob_main (list[3]), prob_turn (list[3])
                prob_slip (list[2]), prob_stall (list[2])

        异常:
            ValueError : 窗口 shape 不符合 [128, 10]
        """
        window = np.asarray(window, dtype=np.float32)
        if window.shape != (self.SEQ_LEN, self.N_CHANNELS):
            raise ValueError(
                f"窗口 shape 应为 ({self.SEQ_LEN}, {self.N_CHANNELS})，"
                f"实际 {window.shape}"
            )

        # 归一化: x_norm = (x - mu) / (sigma + eps)
        x_norm = (window - self.mu.reshape(self.N_CHANNELS)) / (
            self.sigma.reshape(self.N_CHANNELS) + self._eps
        )

        # [1, L, D]
        x_t = torch.from_numpy(x_norm).unsqueeze(0).to(self.device)

        outputs = self.model(x_t)

        return self._decode_outputs(outputs)

    def infer_flat(self, flat_data: Union[List[float], np.ndarray]) -> Dict:
        """
        接受长度 1280（128×10）的一维列表或数组，重塑后执行推理。
        设计用于 MATLAB py.* 调用，避免 MATLAB→Python numpy 维度转换问题。

        参数:
            flat_data : 长度 1280 的可迭代对象（行优先，先行后列）
                        即 window 按 window.reshape(-1) 顺序展平

        返回:
            同 infer()
        """
        arr = np.array(list(flat_data), dtype=np.float32).reshape(
            self.SEQ_LEN, self.N_CHANNELS
        )
        return self.infer(arr)

    # ──────────────────────────────────────────────────────────
    #  内部辅助方法
    # ──────────────────────────────────────────────────────────

    def _decode_outputs(self, outputs: Dict[str, torch.Tensor]) -> Dict:
        """将模型输出张量解码为 Python 原生类型字典（取最末时间步）。"""

        def prob(logit_1d: torch.Tensor) -> List[float]:
            """logit_1d: [C]，返回 softmax 概率列表"""
            return F.softmax(logit_1d, dim=-1).cpu().tolist()

        # 取最末时间步  (batch=0, step=-1)
        theta_hat = float(outputs["theta"][0, -1].cpu())
        delta_hat = float(outputs["delta"][0, -1].cpu())

        main_logit  = outputs["main"][0, -1]   # [3]
        turn_logit  = outputs["turn"][0, -1]   # [3]
        slip_logit  = outputs["slip"][0, -1]   # [2]
        stall_logit = outputs["stall"][0, -1]  # [2]

        # 标签映射（需与训练时 compute_multitask_loss 中的偏移对称还原）
        label_main  = int(torch.argmax(main_logit).item())  + 1  # 0/1/2 → 1/2/3
        label_turn  = int(torch.argmax(turn_logit).item())  - 1  # 0/1/2 → -1/0/+1
        label_slip  = int(torch.argmax(slip_logit).item())       # 0/1
        label_stall = int(torch.argmax(stall_logit).item())      # 0/1

        return {
            "theta_hat":  theta_hat,
            "delta_hat":  delta_hat,
            "label_main":  label_main,
            "label_turn":  label_turn,
            "label_slip":  label_slip,
            "label_stall": label_stall,
            "prob_main":   prob(main_logit),
            "prob_turn":   prob(turn_logit),
            "prob_slip":   prob(slip_logit),
            "prob_stall":  prob(stall_logit),
        }

    @staticmethod
    def _load_mu_sigma_from_hdf5(mat_path: Path):
        """从 Mamba_dataset_export.mat（HDF5）中提取 mu/sigma。"""
        try:
            import h5py  # type: ignore
        except ImportError as e:
            raise ImportError("从 HDF5 加载 mu/sigma 需要 h5py 库") from e

        with h5py.File(str(mat_path), "r") as f:
            mu    = np.array(f["mu"]).squeeze().astype(np.float32)
            sigma = np.array(f["sigma"]).squeeze().astype(np.float32)
        return mu, sigma

    # ──────────────────────────────────────────────────────────
    #  静态工具方法
    # ──────────────────────────────────────────────────────────

    @staticmethod
    def extract_and_save_mu_sigma(
        dataset_hdf5_path: Union[str, Path],
        output_npz_path:   Union[str, Path],
    ) -> None:
        """
        从训练数据集 HDF5 文件中提取 mu/sigma 并保存为 .npz 文件。

        推荐在首次部署前执行一次：
            python mamba2_online_infer.py \\
                --extract-scaler \\
                --dataset  data/mamba/Mamba_dataset_export.mat \\
                --mu-sigma results/mamba/train/agv_mamba2_baseline/mu_sigma.npz

        参数:
            dataset_hdf5_path : Mamba_dataset_export.mat 路径
            output_npz_path   : 输出 mu_sigma.npz 路径
        """
        try:
            import h5py  # type: ignore
        except ImportError as e:
            raise ImportError("提取 mu/sigma 需要 h5py 库") from e

        with h5py.File(str(dataset_hdf5_path), "r") as f:
            mu    = np.array(f["mu"]).squeeze()
            sigma = np.array(f["sigma"]).squeeze()

        np.savez(str(output_npz_path), mu=mu, sigma=sigma)
        print(f"[extract_and_save_mu_sigma] 已保存 -> {output_npz_path}")
        print(f"  mu    = {mu}")
        print(f"  sigma = {sigma}")


# ──────────────────────────────────────────────────────────────
#  模块级函数（供 MATLAB py.* 调用的无状态接口）
# ──────────────────────────────────────────────────────────────

_global_infer_instance: "Mamba2OnlineInfer | None" = None


def get_or_create_infer(
    checkpoint_path: str,
    mu_sigma_path:   str,
    device:          str = "cpu",
) -> "Mamba2OnlineInfer":
    """
    全局单例推理器获取/创建函数，避免 MATLAB 在每个仿真步骤重新加载模型。

    MATLAB 调用示例:
        % 首次调用时自动初始化并缓存
        infer_obj = py.mamba2_online_infer.get_or_create_infer(ckpt, mu_sigma, 'cpu');
        result    = infer_obj.infer_flat(flat_window);
    """
    global _global_infer_instance
    if _global_infer_instance is None:
        _global_infer_instance = Mamba2OnlineInfer(checkpoint_path, mu_sigma_path, device)
    return _global_infer_instance


def reset_global_infer() -> None:
    """释放全局推理器（用于仿真结束后释放内存）。"""
    global _global_infer_instance
    _global_infer_instance = None


# ──────────────────────────────────────────────────────────────
#  命令行入口
# ──────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────
#  TCP 推理服务端（WSL 侧常驻进程，供 MATLAB 通过 socket 调用）
# ──────────────────────────────────────────────────────────────

def _serve(
    infer: "Mamba2OnlineInfer",
    host: str = "127.0.0.1",
    port: int = 5009,
) -> None:
    """
    启动 TCP 推理服务，监听来自 MATLAB 的请求。

    协议说明（纯文本/JSON，换行符分隔）:
    ──────────────────────────────────────────────────────────────
    请求格式（MATLAB → WSL）:
        单行 JSON，以 '\\n' 结尾
        {
          "window": [[f0, f1, ..., f9], ...],  // 128×10 二维列表，行优先
          "request_id": <任意整数或字符串>       // 可选，用于调试对账
        }

    响应格式（WSL → MATLAB）:
        单行 JSON，以 '\\n' 结尾
        成功:
        {
          "ok": true,
          "request_id": ...,        // 原样回传
          "theta_hat":  <float>,
          "delta_hat":  <float>,
          "label_main":  <int>,     // 1/2/3
          "label_turn":  <int>,     // -1/0/1
          "label_slip":  <int>,     // 0/1
          "label_stall": <int>,     // 0/1
          "prob_main":   [f, f, f],
          "prob_turn":   [f, f, f],
          "prob_slip":   [f, f],
          "prob_stall":  [f, f]
        }
        失败:
        {
          "ok": false,
          "request_id": ...,
          "error": "<错误信息>"
        }

    服务行为:
        - 每个连接独立处理，完成后不关闭连接，而是继续读取下一条请求
          （即一次 TCP 连接内可发多次请求，避免频繁建连开销）
        - 遇到连接断开（EOF）或 JSON 解码失败时关闭当前连接，继续接受新连接
        - 遇到模型推理内部错误时返回 ok=false，连接不中断

    MATLAB 客户端调用示例（见 Mamba_state_classifier.m）:
        % 建立连接
        t = tcpclient('127.0.0.1', 5009);
        % 发送请求
        req = jsonencode(struct('window', {window_cell}, 'request_id', 1));
        write(t, uint8([req, newline]));
        % 读取响应
        raw = readline(t);
        resp = jsondecode(raw);
    ──────────────────────────────────────────────────────────────
    """
    import socket
    import threading

    def handle_client(conn: socket.socket, addr) -> None:
        buf = b""
        print(f"[Server] 新连接: {addr}")
        try:
            while True:
                chunk = conn.recv(65536)
                if not chunk:
                    break  # 客户端主动断开
                buf += chunk

                # 每次收到完整的一行（以 \n 为边界）就处理
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    request_id = None
                    try:
                        req = json.loads(line.decode("utf-8"))
                        request_id = req.get("request_id", None)
                        window_list = req["window"]
                        window = np.array(window_list, dtype=np.float32)
                        result = infer.infer(window)
                        if not isinstance(result, dict):
                            raise TypeError(
                                f"infer.infer(window) 应返回 dict，实际为 {type(result).__name__}"
                            )
                        resp = {"ok": True, "request_id": request_id}
                        resp.update(result)
                    except Exception as e:
                        print(f"[Server] 请求处理失败 request_id={request_id}: {e}")
                        traceback.print_exc()
                        resp = {
                            "ok": False,
                            "request_id": request_id,
                            "error": str(e),
                        }

                    try:
                        conn.sendall(
                            (json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8")
                        )
                    except OSError:
                        break
        except Exception as e:
            print(f"[Server] 连接 {addr} 异常: {e}")
        finally:
            conn.close()
            print(f"[Server] 连接 {addr} 已关闭")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(4)
        print(f"[Server] Mamba-2 推理服务已启动 @ {host}:{port}")
        print(f"[Server] 模型={infer._model_name}, device={infer.device}")
        print("[Server] 等待连接... (Ctrl+C 退出)")
        try:
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(
                    target=handle_client, args=(conn, addr), daemon=True
                )
                t.start()
        except KeyboardInterrupt:
            print("[Server] 服务已停止")


# ──────────────────────────────────────────────────────────────
#  命令行入口
# ──────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Mamba-2 在线推理 — 命令行验证接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 导出归一化参数（部署前执行一次）
  python mamba2_online_infer.py \\
      --extract-scaler \\
      --dataset  data/mamba/Mamba_dataset_export.mat \\
      --mu-sigma results/mamba/train/agv_mamba2_baseline/mu_sigma.npz

  # 对单个窗口文件推理
  python mamba2_online_infer.py \\
      --checkpoint results/mamba/train/agv_mamba2_baseline/best.pt \\
      --mu-sigma   results/mamba/train/agv_mamba2_baseline/mu_sigma.npz \\
      --input      window_test.npy

  # 随机输入冒烟测试
  python mamba2_online_infer.py \\
      --checkpoint results/mamba/train/agv_mamba2_baseline/best.pt \\
      --mu-sigma   results/mamba/train/agv_mamba2_baseline/mu_sigma.npz \\
      --smoke-test

  # 启动 WSL 常驻推理服务（供 MATLAB tcpclient 调用）
  python mamba2_online_infer.py \\
      --checkpoint results/mamba/train/agv_mamba2_baseline/best.pt \\
      --mu-sigma   results/mamba/train/agv_mamba2_baseline/mu_sigma.npz \\
      --serve [--host 127.0.0.1] [--port 5009]
""",
    )

    p.add_argument("--checkpoint", type=str, default="", help="best.pt 路径")
    p.add_argument(
        "--mu-sigma",
        type=str,
        default="",
        help=".npz 归一化参数路径或 .mat 数据集路径",
    )
    p.add_argument("--device",   type=str, default="cpu",  help="torch device (cpu/cuda)")
    p.add_argument("--input",    type=str, default="",     help="输入窗口 .npy 文件（shape [128,10]）")
    p.add_argument(
        "--extract-scaler",
        action="store_true",
        help="从 HDF5 数据集提取 mu/sigma 并保存，不执行推理",
    )
    p.add_argument("--dataset",    type=str, default="", help="--extract-scaler 模式下的数据集 .mat 路径")
    p.add_argument("--smoke-test", action="store_true",  help="用全零输入做冒烟测试")
    # ── 服务端参数 ─────────────────────────────────────────────
    p.add_argument("--serve",  action="store_true", help="启动 TCP 推理服务（WSL 常驻模式）")
    p.add_argument("--host",   type=str, default="127.0.0.1", help="TCP 服务监听地址（默认 127.0.0.1）")
    p.add_argument("--port",   type=int, default=5009,       help="TCP 服务端口（默认 5009）")

    return p.parse_args()


def main() -> None:
    args = _parse_args()

    # 模式一：导出 mu/sigma
    if args.extract_scaler:
        if not args.dataset or not args.mu_sigma:
            print("[错误] --extract-scaler 模式需要同时提供 --dataset 和 --mu-sigma")
            sys.exit(1)
        Mamba2OnlineInfer.extract_and_save_mu_sigma(args.dataset, args.mu_sigma)
        return

    # 以下模式均需要 checkpoint 和 mu_sigma
    if not args.checkpoint or not args.mu_sigma:
        print("[错误] 推理模式需要 --checkpoint 和 --mu-sigma")
        sys.exit(1)

    infer = Mamba2OnlineInfer(args.checkpoint, args.mu_sigma, args.device)

    # 模式二：TCP 服务
    if args.serve:
        print("[Server] 服务启动前预热一次模型（首次 GPU/Triton 编译可能较慢）...")
        warmup_window = np.zeros((128, 10), dtype=np.float32)
        warmup_result = infer.infer(warmup_window)
        if torch.cuda.is_available() and str(infer.device).startswith("cuda"):
            torch.cuda.synchronize(infer.device)
        print(
            "[Server] 预热完成 | "
            f"theta_hat={warmup_result['theta_hat']:.6f} | "
            f"label_main={warmup_result['label_main']}"
        )
        _serve(infer, host=args.host, port=args.port)
        return

    # 模式三：冒烟测试
    if args.smoke_test:
        window = np.zeros((128, 10), dtype=np.float32)
        print("[冒烟测试] 全零输入推理...")
        result = infer.infer(window)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # 模式四：单文件推理
    if args.input:
        window = np.load(args.input).astype(np.float32)
        result = infer.infer(window)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("[提示] 未指定 --input、--smoke-test 或 --serve，退出。")


if __name__ == "__main__":
    main()
