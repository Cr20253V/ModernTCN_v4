"""Generate Fig. 6: Main-route closed-loop trajectory and errors.

The figure reads the existing closed-loop comparison MAT/CSV outputs. It plots
the raw simulated trajectories and error time histories without smoothing,
manual edits, or synthetic data.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
import scipy.io as sio


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
PROCESS_DIR = PROJECT / "src" / "pic&table"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESS_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig06_main_closed_loop"

COMPARE_DIR = (
    PROJECT
    / "results"
    / "compare"
    / "lpvmpc_theta_baseline"
    / "path_factory_logistics_showcase_theta10_v3"
)
COMPARE_MAT = COMPARE_DIR / "tcn_gru_modern_lpvmpc_theta_baseline_compare.mat"
SUMMARY_CSV = COMPARE_DIR / "tcn_gru_modern_lpvmpc_theta_baseline_summary.csv"

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
    "reference": "#111111",
    "modern": "#1565C0",
    "gru": "#E69F00",
    "tcn": "#7B3294",
    "theta0": "#7A7F86",
    "imu": "#2E7D72",
    "oracle": "#C62828",
}


@dataclass(frozen=True)
class MethodSpec:
    label: str
    csv_label: str
    color: str
    linestyle: object
    linewidth: float
    alpha: float = 1.0


METHODS = (
    MethodSpec("ModernTCN", "ModernTCN", C["modern"], "-", 1.18),
    MethodSpec("GRU", "GRU", C["gru"], (0, (4.2, 2.0)), 1.08),
    MethodSpec("TCN", "TCN", C["tcn"], (0, (4.4, 1.6, 1.2, 1.6)), 1.08),
    MethodSpec("LPV-MPC theta0", "LPV-MPC_theta0", C["theta0"], (0, (1.2, 1.9)), 1.02, 0.90),
    MethodSpec("LPV-MPC IMU theta", "LPV-MPC_IMU_theta", C["imu"], (0, (5.0, 2.2)), 1.02, 0.92),
    MethodSpec("LPV-MPC oracle theta", "LPV-MPC_oracle_theta", C["oracle"], "-", 1.05),
)
LEARNING_PLUS_ORACLE = {"ModernTCN", "GRU", "TCN", "LPV-MPC oracle theta"}
ERROR_YLIMS = {
    "e_y": (-0.20, 0.45),
    "e_psi": (-0.85, 0.60),
}


def as_1d(value: object, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size < 2:
        raise ValueError(f"{name} must contain at least two samples.")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values.")
    return arr


def load_summary(path: Path) -> dict[str, dict[str, float]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing summary CSV: {path}")
    rows: dict[str, dict[str, float]] = {}
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            controller = row["controller"]
            rows[controller] = {}
            for key, value in row.items():
                if key == "controller" or value == "":
                    continue
                try:
                    rows[controller][key] = float(value)
                except ValueError:
                    pass
    return rows


def load_compare_runs(path: Path) -> tuple[np.ndarray, str]:
    if not path.exists():
        raise FileNotFoundError(f"Missing comparison MAT file: {path}")
    data = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    if "result" not in data:
        raise KeyError(f"MAT file does not contain variable 'result': {path}")
    result = data["result"]
    if not hasattr(result, "runs"):
        raise KeyError(f"result has no field 'runs': {path}")
    runs = np.atleast_1d(result.runs)
    if runs.size != len(METHODS):
        raise ValueError(f"Expected {len(METHODS)} runs, found {runs.size}: {path}")
    path_file = str(getattr(result, "path_file", ""))
    return runs, path_file


def load_reference_time(path_file: str) -> np.ndarray | None:
    if not path_file:
        return None
    path = Path(path_file)
    if not path.exists():
        return None
    data = sio.loadmat(path, squeeze_me=True, struct_as_record=False)
    if "ref" not in data or not hasattr(data["ref"], "t"):
        return None
    return as_1d(getattr(data["ref"], "t"), "ref.t")


def extract_run(run: object, method: MethodSpec, ref_time: np.ndarray | None) -> dict[str, np.ndarray | str]:
    if not hasattr(run, "signals"):
        raise KeyError(f"Run for {method.label} has no signals field.")
    sig = run.signals
    required = ("e_y", "e_psi", "X", "Y", "X_ref", "Y_ref")
    missing = [name for name in required if not hasattr(sig, name)]
    if missing:
        raise KeyError(f"Run for {method.label} is missing fields: {missing}")

    out = {
        "label": method.label,
        "csv_label": method.csv_label,
        "file": str(getattr(run, "file", "")),
    }
    for name in required:
        out[name] = as_1d(getattr(sig, name), f"{method.label}.{name}")

    n = len(out["e_y"])
    if not all(len(out[name]) == n for name in required):
        raise ValueError(f"Run for {method.label} has inconsistent signal lengths.")
    if ref_time is not None:
        if ref_time.size != n:
            raise ValueError(
                f"Reference time length ({ref_time.size}) does not match {method.label} signals ({n})."
            )
        out["t"] = ref_time.copy()
    else:
        out["t"] = np.arange(n, dtype=float) * 0.01
    return out


def rmse(x: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(x[np.isfinite(x)]))))


def peak_abs(x: np.ndarray) -> float:
    return float(np.nanmax(np.abs(x)))


def validate_against_summary(
    runs: list[dict[str, np.ndarray | str]], summary: dict[str, dict[str, float]]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for method, run in zip(METHODS, runs):
        if method.csv_label not in summary:
            raise KeyError(f"Summary CSV has no row for {method.csv_label}.")
        t = np.asarray(run["t"], dtype=float)
        ey = np.asarray(run["e_y"], dtype=float)
        epsi = np.asarray(run["e_psi"], dtype=float)
        mask = t >= 0.5

        checks = {
            "ey_rmse": rmse(ey[mask]),
            "ey_peak": peak_abs(ey[mask]),
            "epsi_rmse": rmse(epsi[mask]),
            "epsi_peak": peak_abs(epsi[mask]),
        }
        for key, computed in checks.items():
            reported = summary[method.csv_label].get(key, np.nan)
            if not np.isfinite(reported) or abs(computed - reported) > max(1e-8, 1e-6 * abs(reported)):
                raise ValueError(
                    f"Summary check failed for {method.label} {key}: "
                    f"computed={computed:.12g}, reported={reported:.12g}"
                )

        rows.append(
            {
                "controller": method.label,
                "source_file": run["file"],
                "n_samples": int(t.size),
                "t_start_s": f"{float(t[0]):.3f}",
                "t_end_s": f"{float(t[-1]):.3f}",
                "x_min_m": f"{float(np.min(np.asarray(run['X'], dtype=float))):.10g}",
                "x_max_m": f"{float(np.max(np.asarray(run['X'], dtype=float))):.10g}",
                "y_min_m": f"{float(np.min(np.asarray(run['Y'], dtype=float))):.10g}",
                "y_max_m": f"{float(np.max(np.asarray(run['Y'], dtype=float))):.10g}",
                "ey_rmse": f"{summary[method.csv_label]['ey_rmse']:.10g}",
                "ey_peak": f"{summary[method.csv_label]['ey_peak']:.10g}",
                "epsi_rmse": f"{summary[method.csv_label]['epsi_rmse']:.10g}",
                "epsi_peak": f"{summary[method.csv_label]['epsi_peak']:.10g}",
                "xy_rmse": f"{summary[method.csv_label].get('xy_rmse', np.nan):.10g}",
                "xy_peak": f"{summary[method.csv_label].get('xy_peak', np.nan):.10g}",
            }
        )
    return rows


def write_manifest(rows: list[dict[str, object]], path_file: str) -> Path:
    manifest = PROCESS_DIR / f"{STEM}_source_manifest.csv"
    fieldnames = [
        "controller",
        "source_file",
        "path_file",
        "n_samples",
        "t_start_s",
        "t_end_s",
        "x_min_m",
        "x_max_m",
        "y_min_m",
        "y_max_m",
        "ey_rmse",
        "ey_peak",
        "epsi_rmse",
        "epsi_peak",
        "xy_rmse",
        "xy_peak",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "path_file": path_file})
    return manifest


def write_source_data(runs: list[dict[str, np.ndarray | str]]) -> Path:
    out = PROCESS_DIR / f"{STEM}_source_data.csv"
    ref = runs[0]
    columns = [
        np.asarray(ref["t"], dtype=float),
        np.asarray(ref["X_ref"], dtype=float),
        np.asarray(ref["Y_ref"], dtype=float),
    ]
    headers = ["time_s", "reference_X_m", "reference_Y_m"]
    for method, run in zip(METHODS, runs):
        prefix = method.label.replace("LPV-MPC ", "LPV_MPC_").replace(" ", "_").replace("-", "_")
        for key, suffix in (("X", "X_m"), ("Y", "Y_m"), ("e_y", "e_y_m"), ("e_psi", "e_psi_rad")):
            columns.append(np.asarray(run[key], dtype=float))
            headers.append(f"{prefix}_{suffix}")
    data = np.column_stack(columns)
    np.savetxt(out, data, delimiter=",", header=",".join(headers), comments="", fmt="%.10g")
    return out


def style_axes(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_xlabel(xlabel, fontsize=8.4, labelpad=2.5)
    ax.set_ylabel(ylabel, fontsize=8.4, labelpad=2.5)
    ax.tick_params(axis="both", labelsize=7.3, length=3.0, pad=1.8)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))


def set_equal_limits(ax: plt.Axes, x_arrays: list[np.ndarray], y_arrays: list[np.ndarray]) -> tuple[float, float, float, float]:
    x = np.concatenate(x_arrays)
    y = np.concatenate(y_arrays)
    xmin, xmax = float(np.nanmin(x)), float(np.nanmax(x))
    ymin, ymax = float(np.nanmin(y)), float(np.nanmax(y))
    xmid, ymid = 0.5 * (xmin + xmax), 0.5 * (ymin + ymax)
    span = max(xmax - xmin, ymax - ymin, 1e-6) * 1.10
    ax.set_xlim(xmid - 0.5 * span, xmid + 0.5 * span)
    ax.set_ylim(ymid - 0.5 * span, ymid + 0.5 * span)
    ax.set_aspect("equal", adjustable="box")
    ax.set_anchor("N")
    return ax.get_xlim()[0], ax.get_xlim()[1], ax.get_ylim()[0], ax.get_ylim()[1]


def panel_label(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        0.0,
        1.035,
        f"{label} {title}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8.4,
        fontweight="bold",
        color=C["text"],
        clip_on=False,
    )


def plot_xy(ax: plt.Axes, runs: list[dict[str, np.ndarray | str]]) -> None:
    ref = runs[0]
    ax.plot(
        np.asarray(ref["X_ref"], dtype=float),
        np.asarray(ref["Y_ref"], dtype=float),
        color=C["reference"],
        lw=1.35,
        linestyle="-",
        label="Reference",
        zorder=7,
    )
    x_arrays = [np.asarray(ref["X_ref"], dtype=float)]
    y_arrays = [np.asarray(ref["Y_ref"], dtype=float)]
    for method, run in zip(METHODS, runs):
        x = np.asarray(run["X"], dtype=float)
        y = np.asarray(run["Y"], dtype=float)
        ax.plot(
            x,
            y,
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=5 if "LPV-MPC" not in method.label else 4,
        )
        x_arrays.append(x)
        y_arrays.append(y)
    set_equal_limits(ax, x_arrays, y_arrays)
    style_axes(ax, "X (m)", "Y (m)")


def plot_error(
    ax: plt.Axes,
    runs: list[dict[str, np.ndarray | str]],
    signal_name: str,
    labels_to_plot: set[str] | None = None,
    ylim: tuple[float, float] | None = None,
) -> None:
    for method, run in zip(METHODS, runs):
        if labels_to_plot is not None and method.label not in labels_to_plot:
            continue
        ax.plot(
            np.asarray(run["t"], dtype=float),
            np.asarray(run[signal_name], dtype=float),
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=4 if "LPV-MPC" not in method.label else 3,
    )
    ax.axhline(0.0, color="#9AA5AF", lw=0.55, zorder=0)
    ax.set_xlim(0, np.asarray(runs[0]["t"], dtype=float)[-1])
    if ylim is not None:
        ax.set_ylim(*ylim)
    else:
        selected = [
            np.asarray(run[signal_name], dtype=float)
            for method, run in zip(METHODS, runs)
            if labels_to_plot is None or method.label in labels_to_plot
        ]
        values = np.concatenate(selected)
        pad = 0.06 * max(np.nanmax(values) - np.nanmin(values), 1e-6)
        ax.set_ylim(float(np.nanmin(values) - pad), float(np.nanmax(values) + pad))


def build_figure(runs: list[dict[str, np.ndarray | str]]) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(7.16, 4.12))
    fig.subplots_adjust(left=0.070, right=0.990, bottom=0.145, top=0.810, wspace=0.340)

    plot_xy(axes[0], runs)
    panel_label(axes[0], "(a)", "XY trajectory")

    plot_error(axes[1], runs, "e_y", LEARNING_PLUS_ORACLE, ERROR_YLIMS["e_y"])
    style_axes(axes[1], "Time (s)", r"Lateral error $e_y$ (m)")
    panel_label(axes[1], "(b)", "Lateral error")

    plot_error(axes[2], runs, "e_psi", LEARNING_PLUS_ORACLE, ERROR_YLIMS["e_psi"])
    style_axes(axes[2], "Time (s)", r"Heading error $e_\psi$ (rad)")
    panel_label(axes[2], "(c)", "Heading error")

    handle_map = {
        "Reference": Line2D([0], [0], color=C["reference"], lw=1.45, linestyle="-", label="Reference")
    }
    for method in METHODS:
        handle_map[method.label] = Line2D(
            [0],
            [0],
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            label=method.label,
        )
    # Matplotlib fills multi-column legends by column; this order makes the
    # visible rows consistent with Fig. 7: Reference, ModernTCN, GRU, TCN /
    # theta0, IMU theta, oracle theta.
    handles = [
        handle_map["Reference"],
        handle_map["LPV-MPC theta0"],
        handle_map["ModernTCN"],
        handle_map["LPV-MPC IMU theta"],
        handle_map["GRU"],
        handle_map["LPV-MPC oracle theta"],
        handle_map["TCN"],
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.975),
        ncol=4,
        frameon=False,
        fontsize=7.0,
        handlelength=2.10,
        columnspacing=0.95,
        handletextpad=0.45,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    raw_runs, path_file = load_compare_runs(COMPARE_MAT)
    ref_time = load_reference_time(path_file)
    runs = [extract_run(run, method, ref_time) for run, method in zip(raw_runs, METHODS)]
    summary = load_summary(SUMMARY_CSV)
    manifest_rows = validate_against_summary(runs, summary)

    manifest = write_manifest(manifest_rows, path_file)
    source_data = write_source_data(runs)

    fig = build_figure(runs)
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
    print(f"Saved: {source_data}")


if __name__ == "__main__":
    main()
