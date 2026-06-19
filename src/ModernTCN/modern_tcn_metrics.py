"""ModernTCN 第一阶段指标、损失和门槛判定。

指标定义和 `run_TCN_GRU_transition_rich_v3_baseline.m` 对齐：输出
acc_main、acc_turn、acc_turn_transition、theta_mae_deg、flat/stall/slope
recall、uphill/downhill recall。seed42 门槛只用于决定是否进入三 seed，
不用于训练集或验证集重划分。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np
import torch
import torch.nn.functional as F


@dataclass(frozen=True)
class GateThresholds:
    acc_main: float = 0.90
    flat_recall: float = 0.90
    slope_recall: float = 0.88
    acc_turn_transition: float = 0.75
    theta_mae_deg: float = 0.70


def multitask_loss(
    logits_main: torch.Tensor,
    logits_turn: torch.Tensor,
    theta_hat: torch.Tensor,
    batch: Dict[str, torch.Tensor],
    class_weights_main: torch.Tensor,
    class_weights_turn: torch.Tensor,
    cfg,
) -> Tuple[torch.Tensor, Dict[str, float]]:
    """计算与 MATLAB TCN/GRU baseline 对齐的多任务损失。"""

    y_main = batch["y_main"]
    y_turn = batch["y_turn"]
    theta = batch["y_theta"]
    mask_theta = batch["mask_theta"]

    main_sample_weight = batch["main_weight"] * _main_slope_sample_weight(y_main, theta, cfg)
    turn_sample_weight = batch["turn_weight"] * (
        1.0 + (cfg.turn_transition_weight - 1.0) * batch["turn_transition"].float()
    )
    theta_sample_weight = batch["theta_weight"] * _theta_sign_weight(theta, cfg)

    loss_main = _weighted_ce(logits_main, y_main, class_weights_main, main_sample_weight)
    loss_turn = _weighted_ce(logits_turn, y_turn, class_weights_turn, turn_sample_weight)
    theta_hat = theta_hat.reshape(-1)
    loss_theta = _masked_weighted_mse(theta_hat, theta, mask_theta, theta_sample_weight)
    near_flat_limit = torch.deg2rad(torch.tensor(float(getattr(cfg, "theta_near_flat_deg", 0.5)), device=theta.device))
    near_flat_mask = (torch.abs(theta) <= near_flat_limit).float() * mask_theta
    loss_theta_near_flat = _masked_weighted_mse(
        theta_hat, torch.zeros_like(theta), near_flat_mask, theta_sample_weight
    )
    true_zero_limit = torch.deg2rad(
        torch.tensor(float(getattr(cfg, "theta_true_zero_tol_deg", 1e-4)), device=theta.device)
    )
    true_zero_mask = (torch.abs(theta) <= true_zero_limit).float() * mask_theta
    flat_zero_mask = _theta_flat_zero_mask(theta, y_main, mask_theta, near_flat_mask, true_zero_mask, cfg)
    loss_theta_flat = _masked_weighted_mse(theta_hat, torch.zeros_like(theta), flat_zero_mask, theta_sample_weight)
    active_mask = (torch.abs(theta) >= torch.deg2rad(torch.tensor(2.0, device=theta.device))).float() * mask_theta
    small_neg_min = torch.deg2rad(
        torch.tensor(float(getattr(cfg, "theta_small_neg_min_deg", -4.0)), device=theta.device)
    )
    small_neg_max = torch.deg2rad(
        torch.tensor(float(getattr(cfg, "theta_small_neg_max_deg", -2.0)), device=theta.device)
    )
    small_neg_mask = ((theta >= small_neg_min) & (theta <= small_neg_max)).float() * mask_theta
    loss_theta_error_excess = _masked_weighted_abs_excess_mse(
        theta_hat, theta, mask_theta, theta_sample_weight, float(getattr(cfg, "theta_excess_target_deg", 1.0))
    )
    loss_theta_flat_excess = _masked_weighted_abs_excess_mse(
        theta_hat,
        torch.zeros_like(theta),
        flat_zero_mask,
        theta_sample_weight,
        float(getattr(cfg, "theta_flat_excess_target_deg", 0.5)),
    )
    loss_theta_near_flat_excess = _masked_weighted_abs_excess_mse(
        theta_hat,
        torch.zeros_like(theta),
        near_flat_mask,
        theta_sample_weight,
        float(getattr(cfg, "theta_flat_excess_target_deg", 0.5)),
    )
    loss_theta_true_zero_excess = _masked_weighted_abs_excess_mse(
        theta_hat,
        torch.zeros_like(theta),
        true_zero_mask,
        theta_sample_weight,
        float(getattr(cfg, "theta_flat_excess_target_deg", 0.5)),
    )
    loss_theta_active_excess = _masked_weighted_abs_excess_mse(
        theta_hat, theta, active_mask, theta_sample_weight, float(getattr(cfg, "theta_excess_target_deg", 1.0))
    )
    loss_theta_small_neg = _masked_weighted_mse(theta_hat, theta, small_neg_mask, theta_sample_weight)
    loss_theta_small_neg_excess = _masked_weighted_abs_excess_mse(
        theta_hat, theta, small_neg_mask, theta_sample_weight, float(getattr(cfg, "theta_excess_target_deg", 1.0))
    )
    loss_turn_release = _turn_straight_probability_penalty(
        logits_turn,
        y_turn,
        batch["turn_transition"].bool(),
        turn_sample_weight,
        transition_mask=True,
    )
    loss_false_turn_straight = _turn_straight_probability_penalty(
        logits_turn,
        y_turn,
        batch["turn_transition"].bool(),
        turn_sample_weight,
        transition_mask=False,
    )

    total = (
        loss_main
        + cfg.lambda_turn * loss_turn
        + cfg.lambda_theta * loss_theta
        + cfg.lambda_theta_flat * loss_theta_flat
        + float(getattr(cfg, "lambda_theta_near_flat", 0.0)) * loss_theta_near_flat
        + float(getattr(cfg, "lambda_theta_error_excess", 0.0)) * loss_theta_error_excess
        + float(getattr(cfg, "lambda_theta_flat_excess", 0.0)) * loss_theta_flat_excess
        + float(getattr(cfg, "lambda_theta_near_flat_excess", 0.0)) * loss_theta_near_flat_excess
        + float(getattr(cfg, "lambda_theta_true_zero_excess", 0.0)) * loss_theta_true_zero_excess
        + float(getattr(cfg, "lambda_theta_active_excess", 0.0)) * loss_theta_active_excess
        + float(getattr(cfg, "lambda_theta_small_neg", 0.0)) * loss_theta_small_neg
        + float(getattr(cfg, "lambda_theta_small_neg_excess", 0.0)) * loss_theta_small_neg_excess
        + float(getattr(cfg, "lambda_turn_release", 0.0)) * loss_turn_release
        + float(getattr(cfg, "lambda_false_turn_straight", 0.0)) * loss_false_turn_straight
    )
    parts = {
        "loss_total": float(total.detach().cpu()),
        "loss_main": float(loss_main.detach().cpu()),
        "loss_turn": float(loss_turn.detach().cpu()),
        "loss_theta": float(loss_theta.detach().cpu()),
        "loss_theta_flat": float(loss_theta_flat.detach().cpu()),
        "loss_theta_near_flat": float(loss_theta_near_flat.detach().cpu()),
        "loss_theta_error_excess": float(loss_theta_error_excess.detach().cpu()),
        "loss_theta_flat_excess": float(loss_theta_flat_excess.detach().cpu()),
        "loss_theta_near_flat_excess": float(loss_theta_near_flat_excess.detach().cpu()),
        "loss_theta_true_zero_excess": float(loss_theta_true_zero_excess.detach().cpu()),
        "loss_theta_active_excess": float(loss_theta_active_excess.detach().cpu()),
        "loss_theta_small_neg": float(loss_theta_small_neg.detach().cpu()),
        "loss_theta_small_neg_excess": float(loss_theta_small_neg_excess.detach().cpu()),
        "loss_turn_release": float(loss_turn_release.detach().cpu()),
        "loss_false_turn_straight": float(loss_false_turn_straight.detach().cpu()),
    }
    return total, parts


def _theta_flat_zero_mask(
    theta: torch.Tensor,
    y_main: torch.Tensor,
    mask_theta: torch.Tensor,
    near_flat_mask: torch.Tensor,
    true_zero_mask: torch.Tensor,
    cfg,
) -> torch.Tensor:
    """Return the samples where the auxiliary flat-theta loss may force zero.

    ``main_flat`` is kept for legacy reproduction. New balanced training uses
    ``near_zero`` so |theta|<2 deg can still be classified as flat without
    teaching the regression head to collapse those angles to zero.
    """

    mode = str(getattr(cfg, "theta_flat_loss_mode", "near_zero")).lower()
    if mode in ("", "none", "off"):
        return torch.zeros_like(mask_theta)
    if mode in ("main_flat", "flat", "legacy"):
        return (y_main == 0).float() * mask_theta
    if mode in ("near_flat", "theta_near_flat"):
        return near_flat_mask
    if mode in ("true_zero", "zero"):
        return true_zero_mask
    if mode in ("near_zero", "very_near_zero"):
        tol = torch.deg2rad(
            torch.tensor(float(getattr(cfg, "theta_flat_zero_tol_deg", 0.3)), device=theta.device)
        )
        return (torch.abs(theta) <= tol).float() * mask_theta
    raise ValueError(f"Unknown theta_flat_loss_mode: {mode}")


def compute_metrics(
    logits_main: np.ndarray,
    logits_turn: np.ndarray,
    theta_hat: np.ndarray,
    split,
    loss_total: float = float("nan"),
) -> Dict[str, object]:
    """根据完整 split 的预测结果计算评估指标。"""

    prob_main = _softmax_np(np.asarray(logits_main))
    prob_turn = _softmax_np(np.asarray(logits_turn))
    pred_main = prob_main.argmax(axis=1)
    pred_turn_cls = prob_turn.argmax(axis=1)
    pred_turn_raw = pred_turn_cls - 1
    y_main = split.y_main.reshape(-1)
    y_turn_raw = split.y_turn.reshape(-1) - 1
    theta_true = split.y_theta.reshape(-1)
    theta_hat = np.asarray(theta_hat).reshape(-1)
    main_confidence = prob_main.max(axis=1)
    turn_confidence = prob_turn.max(axis=1)

    cm_main = _confusion_matrix(y_main, pred_main, 3)
    cm_turn = _confusion_matrix(y_turn_raw + 1, pred_turn_raw + 1, 3)
    recall_main = np.diag(cm_main) / np.maximum(cm_main.sum(axis=1), 1)
    recall_turn = np.diag(cm_turn) / np.maximum(cm_turn.sum(axis=1), 1)
    transition_mask = split.turn_transition.astype(bool)
    pure_mask = np.isfinite(split.turn_purity) & (split.turn_purity >= 0.8) & (~transition_mask)
    slope_idx = np.where(split.mask_theta.reshape(-1) == 1)[0]

    metrics: Dict[str, object] = {
        "loss_total": float(loss_total),
        "acc_main": float(np.mean(pred_main == y_main)),
        "acc_turn": float(np.mean(pred_turn_raw == y_turn_raw)),
        "acc_turn_pure": _masked_acc(pred_turn_raw, y_turn_raw, pure_mask),
        "acc_turn_transition": _masked_acc(pred_turn_raw, y_turn_raw, transition_mask),
        "flat_recall": float(recall_main[0]),
        "stall_recall": float(recall_main[1]),
        "slope_recall": float(recall_main[2]),
        "recall_main": [float(x) for x in recall_main],
        "turn_right_recall": float(recall_turn[0]),
        "turn_straight_recall": float(recall_turn[1]),
        "turn_left_recall": float(recall_turn[2]),
        "recall_turn": [float(x) for x in recall_turn],
        "cm_turn": cm_turn.tolist(),
        "n_turn_transition": int(transition_mask.sum()),
        "n_turn_pure": int(pure_mask.sum()),
        "cm_main": cm_main.tolist(),
    }
    metrics.update(_confidence_summary("main", main_confidence, pred_main == y_main))
    metrics.update(_confidence_summary("turn", turn_confidence, pred_turn_raw == y_turn_raw))

    if slope_idx.size == 0:
        metrics.update(
            {
                "theta_mae_rad": 0.0,
                "theta_mae_deg": 0.0,
                "uphill_recall": float("nan"),
                "downhill_recall": float("nan"),
                "slope_sign_acc": float("nan"),
            }
        )
    else:
        theta_err = np.abs(theta_hat[slope_idx] - theta_true[slope_idx])
        uphill_idx = slope_idx[theta_true[slope_idx] > 0]
        downhill_idx = slope_idx[theta_true[slope_idx] < 0]
        metrics.update(
            {
                "theta_mae_rad": float(theta_err.mean()),
                "theta_mae_deg": float(np.rad2deg(theta_err.mean())),
                "uphill_recall": _slope_sub_recall(pred_main, uphill_idx),
                "downhill_recall": _slope_sub_recall(pred_main, downhill_idx),
                "slope_sign_acc": float(np.mean(np.sign(theta_hat[slope_idx]) == np.sign(theta_true[slope_idx]))),
            }
        )
    metrics.update(_theta_control_metrics(theta_hat, theta_true, y_main, y_turn_raw, split.mask_theta.reshape(-1)))
    return metrics


def selection_score(metrics: Dict[str, object], cfg=None) -> float:
    """验证集选模分数：主工况边界优先，兼顾转弯过渡和 theta。"""

    select_theta_weight = float(getattr(cfg, "select_theta_weight", 0.15))
    select_theta_ref_deg = max(float(getattr(cfg, "select_theta_ref_deg", 5.0)), 1e-6)
    theta_norm = float(metrics["theta_mae_deg"]) / select_theta_ref_deg
    flat_penalty = max(0.0, 0.90 - float(metrics["flat_recall"]))
    slope_penalty = max(0.0, 0.88 - float(metrics["slope_recall"]))
    turn_t = float(metrics["acc_turn_transition"])
    select_turn_weight = float(getattr(cfg, "select_turn_weight", 0.30))
    select_turn_t_weight = float(getattr(cfg, "select_turn_transition_weight", 1.00))
    select_turn_t_target = float(getattr(cfg, "select_turn_transition_target", 0.75))
    select_turn_left_weight = float(getattr(cfg, "select_turn_left_weight", 0.00))
    select_turn_left_target = float(getattr(cfg, "select_turn_left_target", 0.80))
    select_turn_lr_weight = float(getattr(cfg, "select_turn_lr_weight", 0.00))
    select_turn_lr_target = float(getattr(cfg, "select_turn_lr_target", 0.80))
    turn_t_penalty = 0.0 if np.isnan(turn_t) else max(0.0, select_turn_t_target - turn_t)
    turn_right = float(metrics.get("turn_right_recall", float("nan")))
    turn_left = float(metrics.get("turn_left_recall", float("nan")))
    turn_left_penalty = 0.0 if np.isnan(turn_left) else max(0.0, select_turn_left_target - turn_left)
    if np.isnan(turn_right) or np.isnan(turn_left):
        turn_lr_penalty = 0.0
    else:
        turn_lr_penalty = max(0.0, select_turn_lr_target - min(turn_right, turn_left))
    flat_p95 = float(metrics.get("theta_flat_abs_p95_deg", float("nan")))
    flat_p95_target = float(getattr(cfg, "select_theta_flat_p95_target_deg", 1.0))
    flat_p95_penalty = 0.0 if np.isnan(flat_p95) else max(0.0, flat_p95 - flat_p95_target) / 5.0
    theta_p95_penalty = _metric_excess_penalty(
        metrics, "theta_abs_le_8_p95_abs_err_deg", float(getattr(cfg, "select_theta_p95_target_deg", 1.0)), 5.0
    )
    near_flat_p95_penalty = _metric_excess_penalty(
        metrics,
        "theta_near_flat_abs_p95_deg",
        float(getattr(cfg, "select_theta_near_flat_p95_target_deg", 1.0)),
        5.0,
    )
    true_zero_p95_penalty = _metric_excess_penalty(
        metrics,
        "theta_true_zero_abs_p95_deg",
        float(getattr(cfg, "select_theta_true_zero_p95_target_deg", 1.0)),
        5.0,
    )
    flat_peak_penalty = _metric_excess_penalty(
        metrics,
        "theta_flat_abs_max_deg",
        float(getattr(cfg, "select_theta_flat_peak_target_deg", 3.0)),
        10.0,
    )
    small_neg_p95_penalty = _metric_excess_penalty(
        metrics,
        "theta_neg_4_2_p95_abs_err_deg",
        float(getattr(cfg, "select_theta_small_neg_p95_target_deg", 1.0)),
        5.0,
    )
    extreme_p95_penalty = 0.5 * (
        _metric_excess_penalty(
            metrics,
            "theta_neg_8_6_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_extreme_p95_target_deg", 1.0)),
            5.0,
        )
        + _metric_excess_penalty(
            metrics,
            "theta_pos_6_8_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_extreme_p95_target_deg", 1.0)),
            5.0,
        )
    )
    edge_p95_penalty = 0.5 * (
        _metric_excess_penalty(
            metrics,
            "theta_neg_10_8_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_edge_p95_target_deg", 1.2)),
            5.0,
        )
        + _metric_excess_penalty(
            metrics,
            "theta_pos_8_10_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_edge_p95_target_deg", 1.2)),
            5.0,
        )
    )
    small_nonzero_p95_penalty = 0.5 * (
        _metric_excess_penalty(
            metrics,
            "theta_neg_2_0p5_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_small_nonzero_p95_target_deg", 1.0)),
            5.0,
        )
        + _metric_excess_penalty(
            metrics,
            "theta_pos_0p5_2_p95_abs_err_deg",
            float(getattr(cfg, "select_theta_small_nonzero_p95_target_deg", 1.0)),
            5.0,
        )
    )
    flat_bias = abs(float(metrics.get("theta_flat_bias_deg", float("nan"))))
    flat_bias_target = float(getattr(cfg, "select_theta_flat_bias_target_deg", 0.2))
    flat_bias_penalty = 0.0 if np.isnan(flat_bias) else max(0.0, flat_bias - flat_bias_target) / 5.0
    return (
        float(metrics["loss_total"])
        + 1.00 * (1.0 - float(metrics["acc_main"]))
        + select_turn_weight * (1.0 - float(metrics["acc_turn"]))
        + select_theta_weight * theta_norm
        + 2.00 * flat_penalty
        + 2.00 * slope_penalty
        + select_turn_t_weight * turn_t_penalty
        + select_turn_left_weight * turn_left_penalty
        + select_turn_lr_weight * turn_lr_penalty
        + float(getattr(cfg, "select_theta_p95_weight", 0.0)) * theta_p95_penalty
        + float(getattr(cfg, "select_theta_flat_p95_weight", 0.0)) * flat_p95_penalty
        + float(getattr(cfg, "select_theta_near_flat_p95_weight", 0.0)) * near_flat_p95_penalty
        + float(getattr(cfg, "select_theta_true_zero_p95_weight", 0.0)) * true_zero_p95_penalty
        + float(getattr(cfg, "select_theta_flat_peak_weight", 0.0)) * flat_peak_penalty
        + float(getattr(cfg, "select_theta_small_neg_p95_weight", 0.0)) * small_neg_p95_penalty
        + float(getattr(cfg, "select_theta_extreme_p95_weight", 0.0)) * extreme_p95_penalty
        + float(getattr(cfg, "select_theta_edge_p95_weight", 0.0)) * edge_p95_penalty
        + float(getattr(cfg, "select_theta_small_nonzero_p95_weight", 0.0)) * small_nonzero_p95_penalty
        + float(getattr(cfg, "select_theta_flat_bias_weight", 0.0)) * flat_bias_penalty
    )


def seed42_gate(metrics: Dict[str, object], thresholds: GateThresholds = GateThresholds()) -> Tuple[bool, List[str]]:
    """判断 seed42 是否进入三 seed。"""

    checks = [
        ("acc_main", float(metrics["acc_main"]), ">=", thresholds.acc_main),
        ("flat_recall", float(metrics["flat_recall"]), ">=", thresholds.flat_recall),
        ("slope_recall", float(metrics["slope_recall"]), ">=", thresholds.slope_recall),
        ("acc_turn_transition", float(metrics["acc_turn_transition"]), ">=", thresholds.acc_turn_transition),
        ("theta_mae_deg", float(metrics["theta_mae_deg"]), "<=", thresholds.theta_mae_deg),
    ]
    failed: List[str] = []
    for name, value, op, threshold in checks:
        passed = value >= threshold if op == ">=" else value <= threshold
        if not passed:
            failed.append(f"{name} {op} {threshold:.4f} 未满足，实际 {value:.4f}")
    return len(failed) == 0, failed


def _metric_excess_penalty(metrics: Dict[str, object], key: str, target: float, scale: float) -> float:
    value = float(metrics.get(key, float("nan")))
    if np.isnan(value):
        return 0.0
    return max(0.0, value - target) / max(scale, 1e-6)


def metric_row(seed: int, best_epoch: int, metrics: Dict[str, object], paths: Dict[str, str]) -> Dict[str, object]:
    return {
        "model": "ModernTCN-small",
        "seed": seed,
        "best_epoch": best_epoch,
        "acc_main": metrics["acc_main"],
        "acc_turn": metrics["acc_turn"],
        "acc_turn_pure": metrics["acc_turn_pure"],
        "acc_turn_transition": metrics["acc_turn_transition"],
        "main_confidence_mean": metrics.get("main_confidence_mean", float("nan")),
        "main_low_conf_0p60_ratio": metrics.get("main_low_conf_0p60_ratio", float("nan")),
        "main_low_conf_0p70_ratio": metrics.get("main_low_conf_0p70_ratio", float("nan")),
        "turn_confidence_mean": metrics.get("turn_confidence_mean", float("nan")),
        "turn_low_conf_0p60_ratio": metrics.get("turn_low_conf_0p60_ratio", float("nan")),
        "turn_low_conf_0p70_ratio": metrics.get("turn_low_conf_0p70_ratio", float("nan")),
        "turn_right_recall": metrics["turn_right_recall"],
        "turn_straight_recall": metrics["turn_straight_recall"],
        "turn_left_recall": metrics["turn_left_recall"],
        "theta_mae_deg": metrics["theta_mae_deg"],
        "theta_abs_le_8_mae_deg": metrics.get("theta_abs_le_8_mae_deg", float("nan")),
        "theta_abs_le_8_rmse_deg": metrics.get("theta_abs_le_8_rmse_deg", float("nan")),
        "theta_abs_le_8_p95_abs_err_deg": metrics.get("theta_abs_le_8_p95_abs_err_deg", float("nan")),
        "theta_abs_le_8_max_abs_err_deg": metrics.get("theta_abs_le_8_max_abs_err_deg", float("nan")),
        "theta_abs_le_8_bias_deg": metrics.get("theta_abs_le_8_bias_deg", float("nan")),
        "theta_abs_le_10_mae_deg": metrics.get("theta_abs_le_10_mae_deg", float("nan")),
        "theta_abs_le_10_rmse_deg": metrics.get("theta_abs_le_10_rmse_deg", float("nan")),
        "theta_abs_le_10_p95_abs_err_deg": metrics.get("theta_abs_le_10_p95_abs_err_deg", float("nan")),
        "theta_abs_le_10_max_abs_err_deg": metrics.get("theta_abs_le_10_max_abs_err_deg", float("nan")),
        "theta_abs_le_10_bias_deg": metrics.get("theta_abs_le_10_bias_deg", float("nan")),
        "theta_pos_8_10_mae_deg": metrics.get("theta_pos_8_10_mae_deg", float("nan")),
        "theta_pos_8_10_rmse_deg": metrics.get("theta_pos_8_10_rmse_deg", float("nan")),
        "theta_pos_8_10_p95_abs_err_deg": metrics.get("theta_pos_8_10_p95_abs_err_deg", float("nan")),
        "theta_pos_8_10_max_abs_err_deg": metrics.get("theta_pos_8_10_max_abs_err_deg", float("nan")),
        "theta_pos_8_10_bias_deg": metrics.get("theta_pos_8_10_bias_deg", float("nan")),
        "theta_pos_8_10_n": metrics.get("theta_pos_8_10_n", float("nan")),
        "theta_neg_10_8_mae_deg": metrics.get("theta_neg_10_8_mae_deg", float("nan")),
        "theta_neg_10_8_rmse_deg": metrics.get("theta_neg_10_8_rmse_deg", float("nan")),
        "theta_neg_10_8_p95_abs_err_deg": metrics.get("theta_neg_10_8_p95_abs_err_deg", float("nan")),
        "theta_neg_10_8_max_abs_err_deg": metrics.get("theta_neg_10_8_max_abs_err_deg", float("nan")),
        "theta_neg_10_8_bias_deg": metrics.get("theta_neg_10_8_bias_deg", float("nan")),
        "theta_neg_10_8_n": metrics.get("theta_neg_10_8_n", float("nan")),
        "theta_pos_6_8_mae_deg": metrics.get("theta_pos_6_8_mae_deg", float("nan")),
        "theta_pos_6_8_rmse_deg": metrics.get("theta_pos_6_8_rmse_deg", float("nan")),
        "theta_pos_6_8_p95_abs_err_deg": metrics.get("theta_pos_6_8_p95_abs_err_deg", float("nan")),
        "theta_pos_6_8_max_abs_err_deg": metrics.get("theta_pos_6_8_max_abs_err_deg", float("nan")),
        "theta_pos_6_8_bias_deg": metrics.get("theta_pos_6_8_bias_deg", float("nan")),
        "theta_pos_6_8_n": metrics.get("theta_pos_6_8_n", float("nan")),
        "theta_neg_8_6_mae_deg": metrics.get("theta_neg_8_6_mae_deg", float("nan")),
        "theta_neg_8_6_rmse_deg": metrics.get("theta_neg_8_6_rmse_deg", float("nan")),
        "theta_neg_8_6_p95_abs_err_deg": metrics.get("theta_neg_8_6_p95_abs_err_deg", float("nan")),
        "theta_neg_8_6_max_abs_err_deg": metrics.get("theta_neg_8_6_max_abs_err_deg", float("nan")),
        "theta_neg_8_6_bias_deg": metrics.get("theta_neg_8_6_bias_deg", float("nan")),
        "theta_neg_8_6_n": metrics.get("theta_neg_8_6_n", float("nan")),
        "theta_active_abs_ge_2_mae_deg": metrics.get("theta_active_abs_ge_2_mae_deg", float("nan")),
        "theta_active_abs_ge_2_p95_abs_err_deg": metrics.get("theta_active_abs_ge_2_p95_abs_err_deg", float("nan")),
        "theta_neg_4_2_mae_deg": metrics.get("theta_neg_4_2_mae_deg", float("nan")),
        "theta_neg_4_2_p95_abs_err_deg": metrics.get("theta_neg_4_2_p95_abs_err_deg", float("nan")),
        "theta_neg_4_2_bias_deg": metrics.get("theta_neg_4_2_bias_deg", float("nan")),
        "theta_neg_2_0p5_mae_deg": metrics.get("theta_neg_2_0p5_mae_deg", float("nan")),
        "theta_neg_2_0p5_p95_abs_err_deg": metrics.get("theta_neg_2_0p5_p95_abs_err_deg", float("nan")),
        "theta_neg_2_0p5_bias_deg": metrics.get("theta_neg_2_0p5_bias_deg", float("nan")),
        "theta_pos_0p5_2_mae_deg": metrics.get("theta_pos_0p5_2_mae_deg", float("nan")),
        "theta_pos_0p5_2_p95_abs_err_deg": metrics.get("theta_pos_0p5_2_p95_abs_err_deg", float("nan")),
        "theta_pos_0p5_2_bias_deg": metrics.get("theta_pos_0p5_2_bias_deg", float("nan")),
        "theta_flat_abs_p95_deg": metrics.get("theta_flat_abs_p95_deg", float("nan")),
        "theta_flat_abs_max_deg": metrics.get("theta_flat_abs_max_deg", float("nan")),
        "theta_flat_bias_deg": metrics.get("theta_flat_bias_deg", float("nan")),
        "theta_near_flat_abs_p95_deg": metrics.get("theta_near_flat_abs_p95_deg", float("nan")),
        "theta_near_flat_abs_max_deg": metrics.get("theta_near_flat_abs_max_deg", float("nan")),
        "theta_near_flat_bias_deg": metrics.get("theta_near_flat_bias_deg", float("nan")),
        "theta_true_zero_mae_deg": metrics.get("theta_true_zero_mae_deg", float("nan")),
        "theta_true_zero_abs_p95_deg": metrics.get("theta_true_zero_abs_p95_deg", float("nan")),
        "theta_true_zero_abs_max_deg": metrics.get("theta_true_zero_abs_max_deg", float("nan")),
        "theta_true_zero_bias_deg": metrics.get("theta_true_zero_bias_deg", float("nan")),
        "theta_flat_turn_abs_p95_deg": metrics.get("theta_flat_turn_abs_p95_deg", float("nan")),
        "theta_flat_turn_abs_max_deg": metrics.get("theta_flat_turn_abs_max_deg", float("nan")),
        "flat_recall": metrics["flat_recall"],
        "stall_recall": metrics["stall_recall"],
        "slope_recall": metrics["slope_recall"],
        "uphill_recall": metrics["uphill_recall"],
        "downhill_recall": metrics["downhill_recall"],
        "checkpoint_file": paths.get("checkpoint_file", ""),
        "onnx_file": paths.get("onnx_file", ""),
        "report_file": paths.get("report_file", ""),
    }


def _weighted_ce(logits: torch.Tensor, labels: torch.Tensor, class_weights: torch.Tensor, sample_weights: torch.Tensor) -> torch.Tensor:
    class_weights = class_weights.to(logits.device)
    per_sample = F.cross_entropy(logits, labels, weight=class_weights, reduction="none")
    denom = (class_weights[labels] * sample_weights).sum().clamp_min(1e-8)
    return (per_sample * sample_weights).sum() / denom


def _masked_weighted_mse(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor, weight: torch.Tensor) -> torch.Tensor:
    wm = mask * weight
    return (((pred - target) ** 2) * wm).sum() / wm.sum().clamp_min(1e-8)


def _masked_weighted_abs_excess_mse(
    pred: torch.Tensor,
    target: torch.Tensor,
    mask: torch.Tensor,
    weight: torch.Tensor,
    target_deg: float,
) -> torch.Tensor:
    wm = mask * weight
    target_rad = torch.deg2rad(torch.tensor(float(target_deg), device=pred.device, dtype=pred.dtype))
    excess = torch.relu(torch.abs(pred - target) - target_rad)
    return ((excess ** 2) * wm).sum() / wm.sum().clamp_min(1e-8)


def _turn_straight_probability_penalty(
    logits_turn: torch.Tensor,
    y_turn: torch.Tensor,
    turn_transition: torch.Tensor,
    weight: torch.Tensor,
    transition_mask: bool,
) -> torch.Tensor:
    straight = y_turn == 1
    transition = turn_transition.bool()
    if transition_mask:
        mask = straight & transition
    else:
        mask = straight & ~transition
    mask_f = mask.float()
    prob_turn = torch.softmax(logits_turn, dim=1)
    non_straight_prob = prob_turn[:, 0] + prob_turn[:, 2]
    wm = mask_f * weight
    return ((non_straight_prob ** 2) * wm).sum() / wm.sum().clamp_min(1e-8)


def _main_slope_sample_weight(y_main: torch.Tensor, theta: torch.Tensor, cfg) -> torch.Tensor:
    w = torch.ones_like(theta)
    w = torch.where((y_main == 2) & (theta < 0), torch.full_like(w, cfg.main_neg_slope_weight), w)
    w = torch.where((y_main == 2) & (theta > 0), torch.full_like(w, cfg.main_pos_slope_weight), w)
    return w


def _theta_sign_weight(theta: torch.Tensor, cfg) -> torch.Tensor:
    w = torch.ones_like(theta)
    w = torch.where(theta < 0, torch.full_like(w, cfg.theta_neg_weight), w)
    w = torch.where(theta > 0, torch.full_like(w, cfg.theta_pos_weight), w)
    return w


def _confusion_matrix(truth: np.ndarray, pred: np.ndarray, num_classes: int) -> np.ndarray:
    cm = np.zeros((num_classes, num_classes), dtype=np.int64)
    for t, p in zip(truth.reshape(-1), pred.reshape(-1)):
        if 0 <= int(t) < num_classes and 0 <= int(p) < num_classes:
            cm[int(t), int(p)] += 1
    return cm


def _softmax_np(logits: np.ndarray) -> np.ndarray:
    logits = np.asarray(logits, dtype=np.float64)
    logits = logits - np.max(logits, axis=1, keepdims=True)
    exp_logits = np.exp(logits)
    return exp_logits / np.maximum(exp_logits.sum(axis=1, keepdims=True), 1e-12)


def _confidence_summary(prefix: str, confidence: np.ndarray, correct: np.ndarray) -> Dict[str, object]:
    confidence = np.asarray(confidence, dtype=np.float64).reshape(-1)
    correct = np.asarray(correct).reshape(-1).astype(bool)
    out: Dict[str, object] = {
        f"{prefix}_confidence_mean": float(np.mean(confidence)) if confidence.size else float("nan"),
        f"{prefix}_confidence_error_mean": float(np.mean(confidence[~correct])) if np.any(~correct) else float("nan"),
        f"{prefix}_low_conf_0p60_ratio": float(np.mean(confidence < 0.60)) if confidence.size else float("nan"),
        f"{prefix}_low_conf_0p70_ratio": float(np.mean(confidence < 0.70)) if confidence.size else float("nan"),
    }
    edges = np.array([0.0, 0.60, 0.70, 0.80, 0.90, 1.0000001], dtype=np.float64)
    bins = []
    for i in range(len(edges) - 1):
        lo = edges[i]
        hi = edges[i + 1]
        mask = (confidence >= lo) & (confidence < hi)
        n = int(mask.sum())
        bins.append(
            {
                "bin": f"[{lo:.2f},{min(hi, 1.0):.2f})",
                "n": n,
                "error_rate": float(np.mean(~correct[mask])) if n else float("nan"),
                "mean_confidence": float(np.mean(confidence[mask])) if n else float("nan"),
            }
        )
    out[f"{prefix}_confidence_bins"] = bins
    return out


def _masked_acc(pred: np.ndarray, truth: np.ndarray, mask: np.ndarray) -> float:
    mask = mask.astype(bool)
    if not np.any(mask):
        return float("nan")
    return float(np.mean(pred[mask] == truth[mask]))


def _slope_sub_recall(pred_main: np.ndarray, idx: Iterable[int]) -> float:
    idx = np.asarray(list(idx), dtype=np.int64)
    if idx.size == 0:
        return float("nan")
    return float(np.mean(pred_main[idx] == 2))


def _theta_control_metrics(
    theta_hat: np.ndarray,
    theta_true: np.ndarray,
    y_main: np.ndarray,
    y_turn_raw: np.ndarray,
    mask_theta: np.ndarray,
) -> Dict[str, float]:
    """Metrics for whether theta_hat is safe enough to be used by scheduling."""

    flat_mask = y_main == 0
    near_flat_mask = np.abs(theta_true) <= np.deg2rad(0.5)
    true_zero_mask = np.isclose(theta_true, 0.0, atol=np.deg2rad(1e-6))
    flat_turn_mask = flat_mask & near_flat_mask & (y_turn_raw != 0)
    slope_mask = np.asarray(mask_theta).reshape(-1).astype(bool)

    out: Dict[str, float] = {}
    out.update(_theta_zone("theta_flat", theta_hat, theta_true, flat_mask))
    out.update(_theta_zone("theta_near_flat", theta_hat, theta_true, near_flat_mask))
    out.update(_theta_zone("theta_true_zero", theta_hat, theta_true, true_zero_mask))
    out.update(_theta_zone("theta_flat_turn", theta_hat, theta_true, flat_turn_mask))
    out.update(_theta_zone("theta_slope_control", theta_hat, theta_true, slope_mask))
    theta_deg = np.rad2deg(theta_true)
    out.update(_theta_error_zone("theta_all", theta_hat, theta_true, slope_mask))
    out.update(_theta_error_zone("theta_active_abs_ge_2", theta_hat, theta_true, slope_mask & (np.abs(theta_deg) >= 2.0)))
    out.update(_theta_error_zone("theta_abs_le_8", theta_hat, theta_true, slope_mask & (np.abs(theta_deg) <= 8.0)))
    out.update(_theta_error_zone("theta_abs_le_10", theta_hat, theta_true, slope_mask & (np.abs(theta_deg) <= 10.0)))
    out.update(_theta_error_zone("theta_pos_8_10", theta_hat, theta_true, slope_mask & (theta_deg >= 8.0) & (theta_deg <= 10.0)))
    out.update(_theta_error_zone("theta_neg_10_8", theta_hat, theta_true, slope_mask & (theta_deg >= -10.0) & (theta_deg <= -8.0)))
    out.update(_theta_error_zone("theta_pos_6_8", theta_hat, theta_true, slope_mask & (theta_deg >= 6.0) & (theta_deg <= 8.0)))
    out.update(_theta_error_zone("theta_neg_8_6", theta_hat, theta_true, slope_mask & (theta_deg >= -8.0) & (theta_deg <= -6.0)))
    out.update(_theta_error_zone("theta_neg_4_2", theta_hat, theta_true, slope_mask & (theta_deg >= -4.0) & (theta_deg <= -2.0)))
    out.update(_theta_error_zone("theta_neg_2_0p5", theta_hat, theta_true, slope_mask & (theta_deg >= -2.0) & (theta_deg <= -0.5)))
    out.update(_theta_error_zone("theta_pos_0p5_2", theta_hat, theta_true, slope_mask & (theta_deg >= 0.5) & (theta_deg <= 2.0)))
    return out


def _theta_error_zone(prefix: str, theta_hat: np.ndarray, theta_true: np.ndarray, mask: np.ndarray) -> Dict[str, float]:
    mask = np.asarray(mask).reshape(-1).astype(bool)
    if not np.any(mask):
        return {
            f"{prefix}_mae_deg": float("nan"),
            f"{prefix}_rmse_deg": float("nan"),
            f"{prefix}_p95_abs_err_deg": float("nan"),
            f"{prefix}_max_abs_err_deg": float("nan"),
            f"{prefix}_bias_deg": float("nan"),
            f"{prefix}_n": 0.0,
        }
    err_deg = np.rad2deg(theta_hat[mask] - theta_true[mask])
    return {
        f"{prefix}_mae_deg": float(np.mean(np.abs(err_deg))),
        f"{prefix}_rmse_deg": float(np.sqrt(np.mean(err_deg ** 2))),
        f"{prefix}_p95_abs_err_deg": float(np.percentile(np.abs(err_deg), 95)),
        f"{prefix}_max_abs_err_deg": float(np.max(np.abs(err_deg))),
        f"{prefix}_bias_deg": float(np.mean(err_deg)),
        f"{prefix}_n": float(np.count_nonzero(mask)),
    }


def _theta_zone(prefix: str, theta_hat: np.ndarray, theta_true: np.ndarray, mask: np.ndarray) -> Dict[str, float]:
    mask = np.asarray(mask).reshape(-1).astype(bool)
    if not np.any(mask):
        return {
            f"{prefix}_mae_deg": float("nan"),
            f"{prefix}_abs_p95_deg": float("nan"),
            f"{prefix}_abs_max_deg": float("nan"),
            f"{prefix}_bias_deg": float("nan"),
            f"{prefix}_n": 0.0,
        }
    err = theta_hat[mask] - theta_true[mask]
    abs_theta_deg = np.abs(np.rad2deg(theta_hat[mask]))
    return {
        f"{prefix}_mae_deg": float(np.rad2deg(np.mean(np.abs(err)))),
        f"{prefix}_abs_p95_deg": float(np.percentile(abs_theta_deg, 95)),
        f"{prefix}_abs_max_deg": float(np.max(abs_theta_deg)),
        f"{prefix}_bias_deg": float(np.rad2deg(np.mean(err))),
        f"{prefix}_n": float(np.count_nonzero(mask)),
    }
