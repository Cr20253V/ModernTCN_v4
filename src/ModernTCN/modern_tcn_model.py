"""ONNX 友好的 ModernTCN-small 多任务模型。

第一版不直接照搬官方 ModernTCN 的全部组件，而是保留其核心思想：
大核 depthwise temporal convolution + pointwise channel mixing + residual。
这样导出的 ONNX 主要由 Conv1d、BatchNorm、ReLU、Linear、Mean、Concat、
Reshape/Transpose 等标准算子构成，便于后续导入 MATLAB R2024b。
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Dict, Tuple

import torch
from torch import nn


@dataclass
class ModernTCNConfig:
    """ModernTCN-small 的默认训练与结构配置。"""

    input_dim: int = 22
    seq_len: int = 128
    channels: int = 64
    blocks: int = 5
    kernel_size: int = 31
    temporal_padding: str = "same"
    dropout: float = 0.15
    command_dropout_prob: float = 0.0
    command_dropout_start_index: int = -1
    command_dropout_feature_count: int = 0
    command_dropout_mode: str = "window_block"
    expansion: int = 2
    readout_input_stats: bool = True
    turn_head_source: str = "full"
    turn_feature_indices: Tuple[int, ...] = (0, 3, 4, 5, 6, 7, 8, 9, 13, 21)
    lambda_turn: float = 0.05
    lambda_theta: float = 0.35
    lambda_theta_flat: float = 0.20
    theta_flat_loss_mode: str = "near_zero"
    theta_flat_zero_tol_deg: float = 0.3
    lambda_theta_near_flat: float = 0.0
    theta_near_flat_deg: float = 0.5
    lambda_theta_error_excess: float = 0.0
    lambda_theta_flat_excess: float = 0.0
    lambda_theta_near_flat_excess: float = 0.0
    lambda_theta_true_zero_excess: float = 0.0
    lambda_theta_active_excess: float = 0.0
    lambda_theta_small_neg: float = 0.0
    lambda_theta_small_neg_excess: float = 0.0
    lambda_turn_release: float = 0.0
    lambda_false_turn_straight: float = 0.0
    theta_excess_target_deg: float = 1.0
    theta_flat_excess_target_deg: float = 0.5
    theta_true_zero_tol_deg: float = 1e-4
    theta_small_neg_min_deg: float = -4.0
    theta_small_neg_max_deg: float = -2.0
    theta_gate_mode: str = "none"
    theta_gate_power: float = 1.0
    theta_gate_floor: float = 0.0
    main_class_multipliers: Tuple[float, float, float] = (1.20, 1.00, 0.95)
    turn_class_multipliers: Tuple[float, float, float] = (1.00, 1.10, 1.00)
    main_class_weight_method: str = "sqrt_inverse"
    turn_class_weight_method: str = "sqrt_inverse"
    main_neg_slope_weight: float = 2.0
    main_pos_slope_weight: float = 1.0
    theta_neg_weight: float = 2.0
    theta_pos_weight: float = 1.0
    turn_transition_weight: float = 1.0
    select_turn_weight: float = 0.30
    select_turn_transition_weight: float = 1.00
    select_turn_transition_target: float = 0.75
    select_turn_left_weight: float = 0.00
    select_turn_left_target: float = 0.80
    select_turn_lr_weight: float = 0.00
    select_turn_lr_target: float = 0.80
    select_theta_weight: float = 0.15
    select_theta_ref_deg: float = 5.0
    select_theta_p95_weight: float = 0.0
    select_theta_p95_target_deg: float = 1.0
    select_theta_flat_p95_weight: float = 0.0
    select_theta_flat_p95_target_deg: float = 1.0
    select_theta_near_flat_p95_weight: float = 0.0
    select_theta_near_flat_p95_target_deg: float = 1.0
    select_theta_true_zero_p95_weight: float = 0.0
    select_theta_true_zero_p95_target_deg: float = 1.0
    select_theta_flat_peak_weight: float = 0.0
    select_theta_flat_peak_target_deg: float = 3.0
    select_theta_small_neg_p95_weight: float = 0.0
    select_theta_small_neg_p95_target_deg: float = 1.0
    select_theta_extreme_p95_weight: float = 0.0
    select_theta_extreme_p95_target_deg: float = 1.0
    select_theta_edge_p95_weight: float = 0.0
    select_theta_edge_p95_target_deg: float = 1.2
    select_theta_small_nonzero_p95_weight: float = 0.0
    select_theta_small_nonzero_p95_target_deg: float = 1.0
    select_theta_flat_bias_weight: float = 0.0
    select_theta_flat_bias_target_deg: float = 0.2

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


@dataclass
class ModernTCNFullConfig(ModernTCNConfig):
    """ModernTCNFull v0 的默认训练与结构配置。"""

    patch_size: int = 16
    patch_stride: int = 4
    dims: Tuple[int, ...] = (32, 64)
    stage_blocks: Tuple[int, ...] = (2, 2)
    large_kernels: Tuple[int, ...] = (15, 9)
    small_kernels: Tuple[int, ...] = (5, 3)
    ffn_ratio: int = 2
    layer_scale_init: float = 1e-2


class CausalDepthwiseConv1d(nn.Module):
    """Depthwise causal Conv1d with ONNX-friendly Conv + Slice semantics."""

    def __init__(self, channels: int, kernel_size: int) -> None:
        super().__init__()
        if kernel_size < 1:
            raise ValueError("kernel_size 必须 >= 1。")
        self.trim = kernel_size - 1
        self.conv = nn.Conv1d(
            channels,
            channels,
            kernel_size,
            padding=self.trim,
            groups=channels,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.conv(x)
        if self.trim == 0:
            return y
        return y[..., : x.size(-1)]


class ModernTCNBlock(nn.Module):
    """大核 depthwise conv + pointwise MLP 的残差块。"""

    def __init__(
        self,
        channels: int,
        kernel_size: int,
        dropout: float,
        expansion: int,
        temporal_padding: str = "same",
    ) -> None:
        super().__init__()
        hidden = int(channels * expansion)
        temporal_padding = str(temporal_padding).lower()
        if temporal_padding == "same":
            if kernel_size % 2 != 1:
                raise ValueError("same padding 模式下 kernel_size 必须为奇数。")
            padding = kernel_size // 2
            self.depthwise = nn.Conv1d(channels, channels, kernel_size, padding=padding, groups=channels)
        elif temporal_padding == "causal":
            self.depthwise = CausalDepthwiseConv1d(channels, kernel_size)
        else:
            raise ValueError(f"未知 temporal_padding: {temporal_padding}")
        self.temporal_padding = temporal_padding
        self.bn1 = nn.BatchNorm1d(channels)
        self.pw1 = nn.Conv1d(channels, hidden, kernel_size=1)
        self.pw2 = nn.Conv1d(hidden, channels, kernel_size=1)
        self.bn2 = nn.BatchNorm1d(channels)
        self.act = nn.ReLU(inplace=False)
        self.drop = nn.Dropout(dropout)
        # layer_scale 是常数形状参数，导出 ONNX 后只对应 Mul，MATLAB 侧更容易处理。
        self.layer_scale = nn.Parameter(torch.ones(1, channels, 1) * 1e-2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        y = self.depthwise(x)
        y = self.bn1(y)
        y = self.act(y)
        y = self.pw1(y)
        y = self.act(y)
        y = self.drop(y)
        y = self.pw2(y)
        y = self.bn2(y)
        y = self.drop(y)
        return residual + y * self.layer_scale


class ModernTCNSmall(nn.Module):
    """固定输入 `[batch, time=128, features=22]` 的三输出多任务网络。"""

    def __init__(self, cfg: ModernTCNConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.stem = nn.Sequential(
            nn.Conv1d(cfg.input_dim, cfg.channels, kernel_size=1),
            nn.BatchNorm1d(cfg.channels),
            nn.ReLU(inplace=False),
        )
        self.blocks = nn.ModuleList(
            [
                ModernTCNBlock(
                    cfg.channels,
                    cfg.kernel_size,
                    cfg.dropout,
                    cfg.expansion,
                    temporal_padding=cfg.temporal_padding,
                )
                for _ in range(cfg.blocks)
            ]
        )
        feature_dim = cfg.channels * 3
        if cfg.readout_input_stats:
            feature_dim += cfg.input_dim * 5
        input_stats_dim = cfg.input_dim * 5
        turn_source = cfg.turn_head_source.lower()
        if turn_source == "full":
            turn_dim = feature_dim
        elif turn_source == "inputstats":
            turn_dim = input_stats_dim
        elif turn_source == "kinematic_stats":
            turn_indices = self._make_turn_stats_indices(cfg.input_dim, cfg.turn_feature_indices)
            self.register_buffer("turn_stats_indices", turn_indices, persistent=False)
            turn_dim = int(turn_indices.numel())
        else:
            raise ValueError(f"未知 turn_head_source: {cfg.turn_head_source}")
        self.turn_head_source = turn_source

        # 三个任务头严格对应 MATLAB 端后处理契约。
        self.main_head = nn.Linear(feature_dim, 3)
        self.turn_head = nn.Sequential(
            nn.Linear(turn_dim, 64),
            nn.ReLU(inplace=False),
            nn.Linear(64, 3),
        )
        self.theta_head = nn.Linear(feature_dim, 1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # x: [B, T, F]；Conv1d 使用 [B, F, T]。
        x_ct = x.transpose(1, 2)
        z = self.stem(x_ct)
        for block in self.blocks:
            z = block(z)

        h_last = z[:, :, -1]
        h_mean = z.mean(dim=2)
        h_max = z.amax(dim=2)
        pieces = [h_last, h_mean, h_max]
        input_stats = self._input_stats(x_ct)
        if self.cfg.readout_input_stats:
            pieces.append(input_stats)
        h = torch.cat(pieces, dim=1)
        logits_main = self.main_head(h)
        if self.turn_head_source == "full":
            h_turn = h
        elif self.turn_head_source == "inputstats":
            h_turn = input_stats
        else:
            h_turn = input_stats.index_select(1, self.turn_stats_indices)
        logits_turn = self.turn_head(h_turn)
        theta_hat = self.theta_head(h)
        theta_hat = self._apply_theta_gate(theta_hat, logits_main)
        return logits_main, logits_turn, theta_hat

    def _apply_theta_gate(self, theta_hat: torch.Tensor, logits_main: torch.Tensor) -> torch.Tensor:
        """Optionally suppress theta when the main head is confident the window is flat/stall."""

        mode = str(getattr(self.cfg, "theta_gate_mode", "none")).lower()
        if mode in ("", "none"):
            return theta_hat
        if mode != "main_slope_prob":
            raise ValueError(f"未知 theta_gate_mode: {self.cfg.theta_gate_mode}")
        slope_prob = torch.softmax(logits_main, dim=1)[:, 2:3]
        floor = float(getattr(self.cfg, "theta_gate_floor", 0.0))
        power = float(getattr(self.cfg, "theta_gate_power", 1.0))
        gate = floor + (1.0 - floor) * torch.pow(torch.clamp(slope_prob, min=1e-6), power)
        return theta_hat * gate

    @staticmethod
    def _input_stats(x_ct: torch.Tensor) -> torch.Tensor:
        """复用窗口级统计线索，但仍只来自同一输入窗口。"""

        x_last = x_ct[:, :, -1]
        x_mean = x_ct.mean(dim=2)
        x_std = torch.sqrt(torch.mean((x_ct - x_mean.unsqueeze(2)) ** 2, dim=2) + 1e-8)
        x_max = x_ct.amax(dim=2)
        x_min = x_ct.amin(dim=2)
        return torch.cat([x_last, x_mean, x_std, x_max, x_min], dim=1)

    @staticmethod
    def _make_turn_stats_indices(input_dim: int, feature_indices: Tuple[int, ...]) -> torch.Tensor:
        """Return gather indices for [last, mean, std, max, min] input stats."""

        idx = []
        for stat_block in range(5):
            base = stat_block * input_dim
            idx.extend(base + int(i) for i in feature_indices)
        return torch.tensor(idx, dtype=torch.long)


class ModernTCNFullProjection(nn.Module):
    """对每个变量独立做 stage 之间的通道投影。"""

    def __init__(self, nvars: int, dim_in: int, dim_out: int) -> None:
        super().__init__()
        self.nvars = int(nvars)
        self.dim_in = int(dim_in)
        self.dim_out = int(dim_out)
        self.proj = nn.Conv1d(dim_in, dim_out, kernel_size=1)
        self.bn = nn.BatchNorm1d(dim_out)
        self.act = nn.ReLU(inplace=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        bsz, _, tokens = x.shape
        y = x.reshape(bsz, self.nvars, self.dim_in, tokens).reshape(bsz * self.nvars, self.dim_in, tokens)
        y = self.proj(y)
        y = self.bn(y)
        y = self.act(y)
        return y.reshape(bsz, self.nvars, self.dim_out, tokens).reshape(bsz, self.nvars * self.dim_out, tokens)


class ModernTCNFullBlock(nn.Module):
    """ModernTCNFull v0：大核时间卷积 + 变量内 FFN + 通道维 FFN。"""

    def __init__(
        self,
        nvars: int,
        dmodel: int,
        large_kernel: int,
        small_kernel: int,
        ffn_ratio: int,
        dropout: float,
        layer_scale_init: float,
    ) -> None:
        super().__init__()
        if large_kernel < 1 or large_kernel % 2 != 1:
            raise ValueError("large_kernel 必须为正奇数。")
        if small_kernel < 1 or small_kernel % 2 != 1:
            raise ValueError("small_kernel 必须为正奇数。")
        if ffn_ratio < 1:
            raise ValueError("ffn_ratio 必须 >= 1。")
        self.nvars = int(nvars)
        self.dmodel = int(dmodel)
        channels = self.nvars * self.dmodel
        var_hidden = self.nvars * self.dmodel * int(ffn_ratio)
        channel_hidden = self.dmodel * self.nvars * int(ffn_ratio)

        self.large_temporal = nn.Conv1d(
            channels,
            channels,
            kernel_size=large_kernel,
            padding=large_kernel // 2,
            groups=channels,
        )
        self.small_temporal = nn.Conv1d(
            channels,
            channels,
            kernel_size=small_kernel,
            padding=small_kernel // 2,
            groups=channels,
        )
        self.temporal_bn = nn.BatchNorm1d(channels)

        self.var_ffn_1 = nn.Conv1d(channels, var_hidden, kernel_size=1, groups=self.nvars)
        self.var_ffn_2 = nn.Conv1d(var_hidden, channels, kernel_size=1, groups=self.nvars)
        self.var_bn = nn.BatchNorm1d(channels)

        self.channel_ffn_1 = nn.Conv1d(channels, channel_hidden, kernel_size=1, groups=self.dmodel)
        self.channel_ffn_2 = nn.Conv1d(channel_hidden, channels, kernel_size=1, groups=self.dmodel)
        self.channel_bn = nn.BatchNorm1d(channels)

        self.act = nn.ReLU(inplace=False)
        self.drop = nn.Dropout(dropout)
        self.temporal_scale = nn.Parameter(torch.ones(1, channels, 1) * float(layer_scale_init))
        self.var_scale = nn.Parameter(torch.ones(1, channels, 1) * float(layer_scale_init))
        self.channel_scale = nn.Parameter(torch.ones(1, channels, 1) * float(layer_scale_init))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.large_temporal(x) + self.small_temporal(x)
        y = self.temporal_bn(y)
        y = self.act(y)
        y = self.drop(y)
        x = x + y * self.temporal_scale

        y = self.var_ffn_1(x)
        y = self.act(y)
        y = self.drop(y)
        y = self.var_ffn_2(y)
        y = self.var_bn(y)
        y = self.drop(y)
        x = x + y * self.var_scale

        y = self._var_major_to_channel_major(x)
        y = self.channel_ffn_1(y)
        y = self.act(y)
        y = self.drop(y)
        y = self.channel_ffn_2(y)
        y = self._channel_major_to_var_major(y)
        y = self.channel_bn(y)
        y = self.drop(y)
        return x + y * self.channel_scale

    def _var_major_to_channel_major(self, x: torch.Tensor) -> torch.Tensor:
        bsz, _, tokens = x.shape
        return (
            x.reshape(bsz, self.nvars, self.dmodel, tokens)
            .permute(0, 2, 1, 3)
            .contiguous()
            .reshape(bsz, self.dmodel * self.nvars, tokens)
        )

    def _channel_major_to_var_major(self, x: torch.Tensor) -> torch.Tensor:
        bsz, _, tokens = x.shape
        return (
            x.reshape(bsz, self.dmodel, self.nvars, tokens)
            .permute(0, 2, 1, 3)
            .contiguous()
            .reshape(bsz, self.nvars * self.dmodel, tokens)
        )


class ModernTCNFull(nn.Module):
    """ModernTCNFull v0，并行候选模型，输入输出契约与 small 保持一致。"""

    def __init__(self, cfg: ModernTCNFullConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self._validate_config(cfg)
        self.nvars = int(cfg.input_dim)
        self.dims = tuple(int(v) for v in cfg.dims)
        self.patch_stem = nn.Sequential(
            nn.Conv1d(1, self.dims[0], kernel_size=cfg.patch_size, stride=cfg.patch_stride),
            nn.BatchNorm1d(self.dims[0]),
            nn.ReLU(inplace=False),
        )

        stages = []
        prev_dim = self.dims[0]
        for stage_idx, dim in enumerate(self.dims):
            layers = []
            if stage_idx > 0 and prev_dim != dim:
                layers.append(ModernTCNFullProjection(self.nvars, prev_dim, dim))
            for _ in range(int(cfg.stage_blocks[stage_idx])):
                layers.append(
                    ModernTCNFullBlock(
                        self.nvars,
                        dim,
                        int(cfg.large_kernels[stage_idx]),
                        int(cfg.small_kernels[stage_idx]),
                        int(cfg.ffn_ratio),
                        float(cfg.dropout),
                        float(cfg.layer_scale_init),
                    )
                )
            stages.append(nn.Sequential(*layers))
            prev_dim = dim
        self.stages = nn.ModuleList(stages)

        feature_dim = self.nvars * self.dims[-1] * 3
        if cfg.readout_input_stats:
            feature_dim += cfg.input_dim * 5
        input_stats_dim = cfg.input_dim * 5
        turn_source = cfg.turn_head_source.lower()
        if turn_source == "full":
            turn_dim = feature_dim
        elif turn_source == "inputstats":
            turn_dim = input_stats_dim
        elif turn_source == "kinematic_stats":
            turn_indices = ModernTCNSmall._make_turn_stats_indices(cfg.input_dim, cfg.turn_feature_indices)
            self.register_buffer("turn_stats_indices", turn_indices, persistent=False)
            turn_dim = int(turn_indices.numel())
        else:
            raise ValueError(f"未知 turn_head_source: {cfg.turn_head_source}")
        self.turn_head_source = turn_source

        self.main_head = nn.Linear(feature_dim, 3)
        self.turn_head = nn.Sequential(
            nn.Linear(turn_dim, 64),
            nn.ReLU(inplace=False),
            nn.Linear(64, 3),
        )
        self.theta_head = nn.Linear(feature_dim, 1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if not torch.jit.is_tracing() and x.ndim != 3:
            raise ValueError(f"ModernTCNFull 期望输入 [B,T,F]，实际 ndim={x.ndim}")
        bsz, seq_len, nvars = x.shape
        if not torch.jit.is_tracing() and (seq_len != self.cfg.seq_len or nvars != self.cfg.input_dim):
            raise ValueError(
                f"ModernTCNFull 输入 shape 不匹配，期望 [B,{self.cfg.seq_len},{self.cfg.input_dim}]，"
                f"实际 {tuple(x.shape)}"
            )

        x_ct = x.transpose(1, 2)
        z = self.patch_stem(x_ct.reshape(bsz * self.nvars, 1, self.cfg.seq_len))
        tokens = z.size(-1)
        z = z.reshape(bsz, self.nvars, self.dims[0], tokens).reshape(bsz, self.nvars * self.dims[0], tokens)
        for stage in self.stages:
            z = stage(z)

        h_last = z[:, :, -1]
        h_mean = z.mean(dim=2)
        h_max = z.amax(dim=2)
        pieces = [h_last, h_mean, h_max]
        input_stats = ModernTCNSmall._input_stats(x_ct)
        if self.cfg.readout_input_stats:
            pieces.append(input_stats)
        h = torch.cat(pieces, dim=1)
        logits_main = self.main_head(h)
        if self.turn_head_source == "full":
            h_turn = h
        elif self.turn_head_source == "inputstats":
            h_turn = input_stats
        else:
            h_turn = input_stats.index_select(1, self.turn_stats_indices)
        logits_turn = self.turn_head(h_turn)
        theta_hat = self.theta_head(h)
        theta_hat = ModernTCNSmall._apply_theta_gate(self, theta_hat, logits_main)
        return logits_main, logits_turn, theta_hat

    @staticmethod
    def _validate_config(cfg: ModernTCNFullConfig) -> None:
        n_stage = len(cfg.dims)
        if n_stage == 0:
            raise ValueError("dims 至少需要一个 stage。")
        if len(cfg.stage_blocks) != n_stage or len(cfg.large_kernels) != n_stage or len(cfg.small_kernels) != n_stage:
            raise ValueError("dims/stage_blocks/large_kernels/small_kernels 长度必须一致。")
        if cfg.patch_size < 1 or cfg.patch_stride < 1:
            raise ValueError("patch_size 和 patch_stride 必须 >= 1。")
        if cfg.seq_len < cfg.patch_size:
            raise ValueError("seq_len 必须不小于 patch_size。")
        if any(int(d) < 1 for d in cfg.dims):
            raise ValueError("dims 中每个维度必须 >= 1。")


_TUPLE_CONFIG_FIELDS = {
    "main_class_multipliers",
    "turn_class_multipliers",
    "turn_feature_indices",
    "dims",
    "stage_blocks",
    "large_kernels",
    "small_kernels",
}


def normalize_model_family(model_family: object) -> str:
    """将 checkpoint/CLI 中的模型族名称规范化，缺省保持 small。"""

    family = str(model_family or "small").strip().lower()
    aliases = {
        "modern_tcn": "small",
        "moderntcn": "small",
        "modern_tcn_small": "small",
        "moderntcnsmall": "small",
        "modern_tcn_full": "full",
        "moderntcnfull": "full",
    }
    family = aliases.get(family, family)
    if family not in {"small", "full"}:
        raise ValueError(f"未知 model_family: {model_family}")
    return family


def _config_from_dict(cfg_cls, cfg_dict: Dict[str, object]):
    valid_fields = {f.name for f in fields(cfg_cls)}
    filtered = {k: v for k, v in dict(cfg_dict).items() if k in valid_fields}
    for key in _TUPLE_CONFIG_FIELDS:
        if key in filtered and filtered[key] is not None:
            filtered[key] = tuple(filtered[key])
    return cfg_cls(**filtered)


def build_model_from_config(cfg: ModernTCNConfig, model_family: object = "small") -> nn.Module:
    """根据模型族和配置实例化模型。"""

    family = normalize_model_family(model_family)
    if family == "full":
        if isinstance(cfg, ModernTCNFullConfig):
            full_cfg = cfg
        else:
            full_cfg = _config_from_dict(ModernTCNFullConfig, cfg.to_dict())
        return ModernTCNFull(full_cfg)
    if isinstance(cfg, ModernTCNFullConfig):
        small_cfg = _config_from_dict(ModernTCNConfig, cfg.to_dict())
    else:
        small_cfg = cfg
    return ModernTCNSmall(small_cfg)


def build_model_from_checkpoint_dict(ckpt: Dict[str, object]) -> nn.Module:
    """按 checkpoint 中的模型族和配置恢复模型结构。"""

    family = normalize_model_family(ckpt.get("model_family", "small"))
    cfg_cls = ModernTCNFullConfig if family == "full" else ModernTCNConfig
    cfg = _config_from_dict(cfg_cls, dict(ckpt["model_config"]))
    model = build_model_from_config(cfg, family)
    model.load_state_dict(ckpt["model_state"])
    return model
