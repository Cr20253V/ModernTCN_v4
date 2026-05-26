"""Generate Fig. 10: Offline vs closed-loop mismatch for causal ablation.

The figure compares default ModernTCN with its causal ablation. It reads
offline perception summaries and closed-loop evaluation outputs, then exports
normalized panel source data plus the raw lateral-error time histories used in
the trajectory/response panel.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, LogLocator, MaxNLocator, NullFormatter
import numpy as np
import scipy.io as sio


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
PROCESS_DIR = PROJECT / "src" / "pic&table"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESS_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig10_offline_closed_loop_mismatch"

DEFAULT_OFFLINE_CSV = (
    PROJECT
    / "results"
    / "modern_tcn"
    / "modern_tcn_theta10_uniform_h0_v2_seed21"
    / "modern_tcn_seed21_summary.csv"
)
CAUSAL_OFFLINE_CSV = (
    PROJECT
    / "results"
    / "modern_tcn"
    / "modern_tcn_causal_theta10_uniform_h0_v2_seed11"
    / "modern_tcn_seed11_summary.csv"
)
CAUSAL_COMPARE_DIR = (
    PROJECT
    / "results"
    / "compare"
    / "causal_modern_tcn_closed_loop"
    / "path_factory_logistics_showcase_theta10_v3"
)
CLOSED_LOOP_SUMMARY_CSV = CAUSAL_COMPARE_DIR / "causal_tcn_gru_modern_closed_loop_summary.csv"
DEFAULT_COMPARE_MAT = (
    PROJECT
    / "results"
    / "compare"
    / "tcn_gru_modern_closed_loop"
    / "path_factory_logistics_showcase_theta10_v3"
    / "tcn_gru_modern_closed_loop_compare.mat"
)
CAUSAL_COMPARE_MAT = CAUSAL_COMPARE_DIR / "tcn_gru_modern_closed_loop_compare.mat"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 600,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.major.width": 0.75,
        "ytick.major.width": 0.75,
        "mathtext.default": "it",
    }
)


C = {
    "text": "#1A1A1A",
    "muted": "#546E7A",
    "grid": "#D7DEE5",
    "default": "#1565C0",
    "causal": "#8D3C3C",
    "reference": "#111111",
}


@dataclass(frozen=True)
class VariantSpec:
    label: str
    source_label: str
    color: str
    hatch: str | None


VARIANTS = (
    VariantSpec("Default ModernTCN", "ModernTCN", C["default"], None),
    VariantSpec("Causal ModernTCN", "ModernTCN_causal", C["causal"], "///"),
)

OFFLINE_METRICS = (
    ("acc_main", "Main\nacc.", "accuracy"),
    ("acc_turn", "Turn\nacc.", "accuracy"),
    ("acc_turn_transition", "Trans.\nturn", "accuracy"),
    ("theta_mae_deg", "Slope\nMAE", "error"),
)
CLOSED_LOOP_METRICS = (
    ("ey_rmse", "$e_y$\nRMSE", "error"),
    ("epsi_rmse", "$e_\\psi$\nRMSE", "error"),
    ("xy_rmse", "XY\nRMSE", "error"),
    ("j_du", "$J_{\\Delta u}$", "error"),
)


def read_single_row_csv(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV file: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one row in {path}, found {len(rows)}.")
    return rows[0]


def read_table(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV file: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def fnum(row: dict[str, str], key: str, source: Path) -> float:
    if key not in row:
        raise KeyError(f"Missing column '{key}' in {source}")
    try:
        return float(row[key])
    except ValueError as exc:
        raise ValueError(f"Non-numeric value in column '{key}' of {source}: {row[key]!r}") from exc


def load_offline_metrics() -> dict[str, dict[str, float]]:
    default_row = read_single_row_csv(DEFAULT_OFFLINE_CSV)
    causal_row = read_single_row_csv(CAUSAL_OFFLINE_CSV)
    out = {
        "ModernTCN": {},
        "ModernTCN_causal": {},
    }
    for key, _label, _kind in OFFLINE_METRICS:
        out["ModernTCN"][key] = fnum(default_row, key, DEFAULT_OFFLINE_CSV)
        out["ModernTCN_causal"][key] = fnum(causal_row, key, CAUSAL_OFFLINE_CSV)
    return out


def load_closed_loop_metrics() -> dict[str, dict[str, float]]:
    rows = read_table(CLOSED_LOOP_SUMMARY_CSV)
    selected: dict[str, dict[str, float]] = {}
    for row in rows:
        controller = row.get("controller", "")
        if controller not in {"ModernTCN", "ModernTCN_causal"}:
            continue
        if row.get("zone", "") != "all":
            continue
        selected[controller] = {key: fnum(row, key, CLOSED_LOOP_SUMMARY_CSV) for key, _label, _kind in CLOSED_LOOP_METRICS}
        selected[controller].update(
            {
                "main_acc_pct": fnum(row, "main_acc_pct", CLOSED_LOOP_SUMMARY_CSV),
                "turn_acc_pct": fnum(row, "turn_acc_pct", CLOSED_LOOP_SUMMARY_CSV),
                "theta_sched_mae_deg": fnum(row, "theta_sched_mae_deg", CLOSED_LOOP_SUMMARY_CSV),
            }
        )
    missing = {"ModernTCN", "ModernTCN_causal"} - set(selected)
    if missing:
        raise ValueError(f"Closed-loop summary is missing controller rows: {sorted(missing)}")
    return selected


def as_1d(value: object, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size < 2:
        raise ValueError(f"{name} must contain at least two samples.")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values.")
    return arr


def load_reference_time(path_file: str, n: int) -> np.ndarray:
    if path_file:
        path = Path(path_file)
        if path.exists():
            data = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
            if "ref" in data and hasattr(data["ref"], "t"):
                t = as_1d(getattr(data["ref"], "t"), "ref.t")
                if t.size == n:
                    return t
    return np.arange(n, dtype=float) * 0.01


def load_run_from_compare(path: Path, controller: str) -> tuple[dict[str, np.ndarray | str], str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing comparison MAT file: {path}")
    data = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    if "result" not in data or not hasattr(data["result"], "runs"):
        raise KeyError(f"MAT file does not contain result.runs: {path}")
    result = data["result"]
    runs = np.atleast_1d(result.runs)
    for run in runs:
        if not hasattr(run, "summary") or not hasattr(run, "signals"):
            continue
        summary = run.summary
        summary_controller = ""
        if hasattr(summary, "controller"):
            raw = getattr(summary, "controller")
            summary_controller = str(raw) if isinstance(raw, str) else ""
        # scipy cannot decode MATLAB string objects in this file reliably, so
        # select by the source file name and by known run order when needed.
        file_text = str(getattr(run, "file", ""))
        is_default = controller == "ModernTCN" and "ModernTCN_out.mat" in file_text and "causal" not in file_text
        is_causal = controller == "ModernTCN_causal" and "ModernTCN_causal" in file_text
        if summary_controller == controller or is_default or is_causal:
            sig = run.signals
            required = ("X", "Y", "X_ref", "Y_ref", "e_y", "e_psi")
            missing = [name for name in required if not hasattr(sig, name)]
            if missing:
                raise KeyError(f"Run for {controller} is missing fields: {missing}")
            e_y = as_1d(getattr(sig, "e_y"), f"{controller}.e_y")
            n = e_y.size
            t = load_reference_time(str(getattr(result, "path_file", "")), n)
            out = {
                "controller": controller,
                "file": file_text,
                "t": t,
                "X": as_1d(getattr(sig, "X"), f"{controller}.X"),
                "Y": as_1d(getattr(sig, "Y"), f"{controller}.Y"),
                "X_ref": as_1d(getattr(sig, "X_ref"), f"{controller}.X_ref"),
                "Y_ref": as_1d(getattr(sig, "Y_ref"), f"{controller}.Y_ref"),
                "e_y": e_y,
                "e_psi": as_1d(getattr(sig, "e_psi"), f"{controller}.e_psi"),
            }
            if not all(np.asarray(out[name]).size == n for name in ("X", "Y", "X_ref", "Y_ref", "e_psi")):
                raise ValueError(f"Run for {controller} has inconsistent signal lengths.")
            return out, str(getattr(result, "path_file", ""))
    raise ValueError(f"Could not find controller {controller} in {path}")


def rmse(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x[np.isfinite(x)]))))


def validate_runs_against_summary(
    runs: dict[str, dict[str, np.ndarray | str]],
    closed_loop: dict[str, dict[str, float]],
) -> None:
    for controller, run in runs.items():
        t = np.asarray(run["t"], dtype=float)
        mask = t >= 0.5
        if not np.any(mask):
            raise ValueError(f"No samples after 0.5 s for {controller}.")
        checks = {
            "ey_rmse": rmse(np.asarray(run["e_y"], dtype=float)[mask]),
            "epsi_rmse": rmse(np.asarray(run["e_psi"], dtype=float)[mask]),
        }
        x = np.asarray(run["X"], dtype=float)
        y = np.asarray(run["Y"], dtype=float)
        xr = np.asarray(run["X_ref"], dtype=float)
        yr = np.asarray(run["Y_ref"], dtype=float)
        checks["xy_rmse"] = rmse(np.hypot(x[mask] - xr[mask], y[mask] - yr[mask]))
        for key, computed in checks.items():
            reported = closed_loop[controller][key]
            if abs(computed - reported) > max(1e-8, 1e-6 * abs(reported)):
                raise ValueError(
                    f"Run validation failed for {controller} {key}: "
                    f"computed={computed:.12g}, reported={reported:.12g}"
                )


def write_manifest(
    offline: dict[str, dict[str, float]],
    closed_loop: dict[str, dict[str, float]],
    runs: dict[str, dict[str, np.ndarray | str]],
    path_file: str,
) -> Path:
    out = PROCESS_DIR / f"{STEM}_source_manifest.csv"
    fieldnames = [
        "variant",
        "offline_csv",
        "closed_loop_summary_csv",
        "trajectory_mat",
        "path_file",
        "n_samples",
        "t_start_s",
        "t_end_s",
        "offline_acc_main",
        "offline_acc_turn",
        "offline_acc_turn_transition",
        "offline_theta_mae_deg",
        "closed_loop_ey_rmse",
        "closed_loop_epsi_rmse",
        "closed_loop_xy_rmse",
        "closed_loop_j_du",
    ]
    source_map = {
        "ModernTCN": DEFAULT_OFFLINE_CSV,
        "ModernTCN_causal": CAUSAL_OFFLINE_CSV,
    }
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for variant in VARIANTS:
            run = runs[variant.source_label]
            t = np.asarray(run["t"], dtype=float)
            writer.writerow(
                {
                    "variant": variant.source_label,
                    "offline_csv": source_map[variant.source_label],
                    "closed_loop_summary_csv": CLOSED_LOOP_SUMMARY_CSV,
                    "trajectory_mat": DEFAULT_COMPARE_MAT
                    if variant.source_label == "ModernTCN"
                    else CAUSAL_COMPARE_MAT,
                    "path_file": path_file,
                    "n_samples": int(t.size),
                    "t_start_s": f"{float(t[0]):.3f}",
                    "t_end_s": f"{float(t[-1]):.3f}",
                    "offline_acc_main": f"{offline[variant.source_label]['acc_main']:.10g}",
                    "offline_acc_turn": f"{offline[variant.source_label]['acc_turn']:.10g}",
                    "offline_acc_turn_transition": f"{offline[variant.source_label]['acc_turn_transition']:.10g}",
                    "offline_theta_mae_deg": f"{offline[variant.source_label]['theta_mae_deg']:.10g}",
                    "closed_loop_ey_rmse": f"{closed_loop[variant.source_label]['ey_rmse']:.10g}",
                    "closed_loop_epsi_rmse": f"{closed_loop[variant.source_label]['epsi_rmse']:.10g}",
                    "closed_loop_xy_rmse": f"{closed_loop[variant.source_label]['xy_rmse']:.10g}",
                    "closed_loop_j_du": f"{closed_loop[variant.source_label]['j_du']:.10g}",
                }
            )
    return out


def write_metric_source_data(
    offline: dict[str, dict[str, float]],
    closed_loop: dict[str, dict[str, float]],
) -> Path:
    out = PROCESS_DIR / f"{STEM}_metric_source_data.csv"
    fieldnames = ["domain", "metric", "metric_label", "metric_kind", "variant", "raw_value", "relative_to_default"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key, label, kind in OFFLINE_METRICS:
            base = offline["ModernTCN"][key]
            for variant in VARIANTS:
                value = offline[variant.source_label][key]
                writer.writerow(
                    {
                        "domain": "offline",
                        "metric": key,
                        "metric_label": label,
                        "metric_kind": kind,
                        "variant": variant.source_label,
                        "raw_value": f"{value:.10g}",
                        "relative_to_default": f"{value / base:.10g}",
                    }
                )
        for key, label, kind in CLOSED_LOOP_METRICS:
            base = closed_loop["ModernTCN"][key]
            for variant in VARIANTS:
                value = closed_loop[variant.source_label][key]
                writer.writerow(
                    {
                        "domain": "closed_loop",
                        "metric": key,
                        "metric_label": label,
                        "metric_kind": kind,
                        "variant": variant.source_label,
                        "raw_value": f"{value:.10g}",
                        "relative_to_default": f"{value / base:.10g}",
                    }
                )
    return out


def write_time_source_data(runs: dict[str, dict[str, np.ndarray | str]]) -> Path:
    out = PROCESS_DIR / f"{STEM}_time_history_source_data.csv"
    default = runs["ModernTCN"]
    causal = runs["ModernTCN_causal"]
    t_default = np.asarray(default["t"], dtype=float)
    t_causal = np.asarray(causal["t"], dtype=float)
    if t_default.size != t_causal.size or np.max(np.abs(t_default - t_causal)) > 1e-9:
        raise ValueError("Default and causal time axes do not match.")
    data = np.column_stack(
        [
            t_default,
            np.asarray(default["e_y"], dtype=float),
            np.asarray(causal["e_y"], dtype=float),
            np.asarray(default["e_psi"], dtype=float),
            np.asarray(causal["e_psi"], dtype=float),
            np.asarray(default["X"], dtype=float),
            np.asarray(default["Y"], dtype=float),
            np.asarray(causal["X"], dtype=float),
            np.asarray(causal["Y"], dtype=float),
            np.asarray(default["X_ref"], dtype=float),
            np.asarray(default["Y_ref"], dtype=float),
        ]
    )
    headers = [
        "time_s",
        "ModernTCN_e_y_m",
        "ModernTCN_causal_e_y_m",
        "ModernTCN_e_psi_rad",
        "ModernTCN_causal_e_psi_rad",
        "ModernTCN_X_m",
        "ModernTCN_Y_m",
        "ModernTCN_causal_X_m",
        "ModernTCN_causal_Y_m",
        "reference_X_m",
        "reference_Y_m",
    ]
    np.savetxt(out, data, delimiter=",", header=",".join(headers), comments="", fmt="%.10g")
    return out


def style_axes(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_xlabel(xlabel, fontsize=8.25, labelpad=2.5)
    ax.set_ylabel(ylabel, fontsize=8.25, labelpad=2.5)
    ax.tick_params(axis="both", labelsize=7.2, length=3.0, pad=1.8)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))


def panel_label(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        0.0,
        1.040,
        f"{label} {title}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.35,
        fontweight="bold",
        color=C["text"],
        clip_on=False,
    )


def plot_grouped_relative_bars(
    ax: plt.Axes,
    metrics: tuple[tuple[str, str, str], ...],
    values: dict[str, dict[str, float]],
    ylabel: str,
    ylim: tuple[float, float],
    add_log: bool = False,
) -> None:
    x = np.arange(len(metrics), dtype=float)
    width = 0.34
    offsets = (-width / 2, width / 2)
    for variant, offset in zip(VARIANTS, offsets):
        rel = [values[variant.source_label][key] / values["ModernTCN"][key] for key, _label, _kind in metrics]
        bars = ax.bar(
            x + offset,
            rel,
            width=width,
            color=variant.color,
            edgecolor=variant.color if variant.hatch else "white",
            linewidth=0.65,
            hatch=variant.hatch,
            alpha=0.93,
            zorder=4,
            label=variant.label,
        )
        for bar, ratio in zip(bars, rel):
            if add_log and variant.source_label == "ModernTCN":
                continue
            if add_log:
                label_y = ratio * 1.16
                if label_y >= ylim[1] * 0.92:
                    label_y = ratio * 0.72
                    va = "top"
                else:
                    va = "bottom"
                label = f"{ratio:.1e}" if ratio >= 100 else f"{ratio:.2g}"
            else:
                if ratio >= ylim[1] * 0.72 or ratio <= ylim[0] * 1.15:
                    continue
                label_y = ratio + (ylim[1] - ylim[0]) * 0.025
                va = "bottom"
                label = f"{ratio:.2g}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                label_y,
                label,
                ha="center",
                va=va,
                fontsize=6.1,
                color=C["muted"],
                rotation=0,
            )
    ax.axhline(1.0, color=C["reference"], lw=0.75, linestyle=(0, (3.2, 2.0)), alpha=0.78, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels([label for _key, label, _kind in metrics], fontsize=6.65)
    ax.set_ylim(*ylim)
    if add_log:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=5))
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=50))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}" if value >= 1 else f"{value:.1g}"))
        ax.yaxis.set_minor_formatter(NullFormatter())
    style_axes(ax, "", ylabel)
    if add_log:
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=5))
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=50))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}" if value >= 1 else f"{value:.1g}"))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.grid(True, which="both", color=C["grid"], linewidth=0.42, alpha=0.50)
    ax.set_xlabel("")


def plot_error_history(ax: plt.Axes, runs: dict[str, dict[str, np.ndarray | str]]) -> None:
    for variant in VARIANTS:
        run = runs[variant.source_label]
        ax.plot(
            np.asarray(run["t"], dtype=float),
            np.asarray(run["e_y"], dtype=float),
            color=variant.color,
            lw=1.08 if variant.source_label == "ModernTCN" else 1.02,
            linestyle="-" if variant.source_label == "ModernTCN" else (0, (4.2, 1.8)),
            alpha=0.98,
            solid_capstyle="round",
            zorder=4,
        )
    ax.axhline(0.0, color="#9AA5AF", lw=0.60, zorder=1)
    t = np.asarray(runs["ModernTCN"]["t"], dtype=float)
    ax.set_xlim(t[0], t[-1])
    values = np.concatenate([np.asarray(runs[v.source_label]["e_y"], dtype=float) for v in VARIANTS])
    pad = 0.06 * max(np.nanmax(values) - np.nanmin(values), 1e-6)
    ax.set_ylim(float(np.nanmin(values) - pad), float(np.nanmax(values) + pad))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    style_axes(ax, "Time (s)", r"Lateral error $e_y$ (m)")


def build_figure(
    offline: dict[str, dict[str, float]],
    closed_loop: dict[str, dict[str, float]],
    runs: dict[str, dict[str, np.ndarray | str]],
) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(7.16, 3.15))
    fig.subplots_adjust(left=0.087, right=0.992, bottom=0.245, top=0.765, wspace=0.455)

    plot_grouped_relative_bars(
        axes[0],
        OFFLINE_METRICS,
        offline,
        "Offline metric\n(relative to default)",
        (0.86, 1.06),
    )
    panel_label(axes[0], "(a)", "Offline perception")

    plot_grouped_relative_bars(
        axes[1],
        CLOSED_LOOP_METRICS,
        closed_loop,
        "Closed-loop metric\n(relative to default)",
        (0.45, 2000.0),
        add_log=True,
    )
    panel_label(axes[1], "(b)", "Closed-loop metrics")

    plot_error_history(axes[2], runs)
    panel_label(axes[2], "(c)", "Main-route lateral error")

    handles = [
        Line2D(
            [0],
            [0],
            color=variant.color,
            lw=1.35,
            linestyle="-" if variant.source_label == "ModernTCN" else (0, (4.2, 1.8)),
            label=variant.label,
        )
        for variant in VARIANTS
    ]
    handles.append(
        Line2D(
            [0],
            [0],
            color=C["reference"],
            lw=0.75,
            linestyle=(0, (3.2, 2.0)),
            label="Default reference (=1)",
        )
    )
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.968),
        ncol=3,
        frameon=False,
        fontsize=7.25,
        handlelength=2.20,
        columnspacing=1.10,
        handletextpad=0.48,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    offline = load_offline_metrics()
    closed_loop = load_closed_loop_metrics()

    default_run, path_file = load_run_from_compare(DEFAULT_COMPARE_MAT, "ModernTCN")
    causal_run, causal_path_file = load_run_from_compare(CAUSAL_COMPARE_MAT, "ModernTCN_causal")
    if path_file and causal_path_file and Path(path_file) != Path(causal_path_file):
        raise ValueError(f"Default and causal runs use different path files: {path_file} vs {causal_path_file}")
    runs = {"ModernTCN": default_run, "ModernTCN_causal": causal_run}
    validate_runs_against_summary(runs, closed_loop)

    manifest = write_manifest(offline, closed_loop, runs, path_file or causal_path_file)
    metric_data = write_metric_source_data(offline, closed_loop)
    time_data = write_time_source_data(runs)

    fig = build_figure(offline, closed_loop, runs)
    pdf_file = OUT_DIR / f"{STEM}.pdf"
    svg_file = OUT_DIR / f"{STEM}.svg"
    png_file = OUT_DIR / f"{STEM}.png"
    fig.savefig(pdf_file)
    fig.savefig(svg_file)
    fig.savefig(png_file, dpi=600)
    plt.close(fig)

    print(f"Saved: {pdf_file}")
    print(f"Saved: {svg_file}")
    print(f"Saved: {png_file}")
    print(f"Saved: {manifest}")
    print(f"Saved: {metric_data}")
    print(f"Saved: {time_data}")


if __name__ == "__main__":
    main()
