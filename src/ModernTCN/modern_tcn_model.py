"""ONNX 友好的 ModernTCN-small 多任务模型。

第一版不直接照搬官方 ModernTCN 的全部组件，而是保留其核心思想：
大核 depthwise temporal convolution + pointwise channel mixing + residual。
这样导出的 ONNX 主要由 Conv1d、BatchNorm、ReLU、Linear、Mean、Concat、
Reshape/Transpose 等标准算子构成，便于后续导入 MATLAB R2024b。
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple

import torch
from torch import nn


@dataclass
class ModernTCNConfig:
    """ModernTCN-small 的默认训练与结构配置。"""

    input_dim: int = 19
    seq_len: int = 128
    channels: int = 64
    blocks: int = 5
    kernel_size: int = 31
    dropout: float = 0.15
    expansion: int = 2
    readout_input_stats: bool = True
    turn_head_source: str = "full"
    turn_feature_indices: Tuple[int, ...] = (1, 4, 5, 6, 7, 9, 10, 11, 16)
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


class ModernTCNBlock(nn.Module):
    """大核 depthwise conv + pointwise MLP 的残差块。"""

    def __init__(self, channels: int, kernel_size: int, dropout: float, expansion: int) -> None:
        super().__init__()
        if kernel_size % 2 != 1:
            raise ValueError("kernel_size 必须为奇数，以便 Conv1d 使用固定 symmetric padding。")
        hidden = int(channels * expansion)
        padding = kernel_size // 2
        self.depthwise = nn.Conv1d(channels, channels, kernel_size, padding=padding, groups=channels)
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
    """固定输入 `[batch, time=128, features=19]` 的三输出多任务网络。"""

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
                ModernTCNBlock(cfg.channels, cfg.kernel_size, cfg.dropout, cfg.expansion)
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
        """复用窗口级统计线索，但仍只来自同一 19 维输入窗口。"""

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


def build_model_from_checkpoint_dict(ckpt: Dict[str, object]) -> ModernTCNSmall:
    """按 checkpoint 中的配置恢复模型结构。"""

    cfg_dict = dict(ckpt["model_config"])
    cfg_dict["main_class_multipliers"] = tuple(cfg_dict["main_class_multipliers"])
    cfg_dict["turn_class_multipliers"] = tuple(cfg_dict["turn_class_multipliers"])
    if "turn_feature_indices" in cfg_dict:
        cfg_dict["turn_feature_indices"] = tuple(cfg_dict["turn_feature_indices"])
    cfg = ModernTCNConfig(**cfg_dict)
    model = ModernTCNSmall(cfg)
    model.load_state_dict(ckpt["model_state"])
    return model
