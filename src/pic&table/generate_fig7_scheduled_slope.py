"""Generate Fig. 7: Scheduled slope time histories.

The plotted learning-based slope is the third channel of ``rho_f`` from the
closed-loop comparison results, i.e. the scheduling signal used by LPV-MPC
after deployment-side conditioning. Values are converted from rad to deg only
for visualization.
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
STEM = "fig07_scheduled_slope"

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
    "true": "#111111",
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
    MethodSpec(r"ModernTCN $\theta^{sch}$", "ModernTCN", C["modern"], "-", 1.16),
    MethodSpec(r"GRU $\theta^{sch}$", "GRU", C["gru"], (0, (4.2, 2.0)), 1.06),
    MethodSpec(r"TCN $\theta^{sch}$", "TCN", C["tcn"], (0, (4.4, 1.6, 1.2, 1.6)), 1.06),
    MethodSpec("LPV-MPC theta0", "LPV-MPC_theta0", C["theta0"], (0, (1.2, 1.9)), 1.00, 0.92),
    MethodSpec("LPV-MPC IMU theta", "LPV-MPC_IMU_theta", C["imu"], (0, (5.0, 2.2)), 1.00, 0.92),
    MethodSpec("LPV-MPC oracle theta", "LPV-MPC_oracle_theta", C["oracle"], "-", 1.04),
)
FOCUS_METHODS = {"ModernTCN", "GRU", "TCN", "LPV-MPC_oracle_theta"}


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
    return runs, str(getattr(result, "path_file", ""))


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
    if not hasattr(run, "signals") or not hasattr(run, "truth"):
        raise KeyError(f"Run for {method.csv_label} is missing signals/truth fields.")
    sig = run.signals
    if not hasattr(sig, "rho_f"):
        raise KeyError(f"Run for {method.csv_label} is missing signals.rho_f.")
    rho = np.asarray(sig.rho_f, dtype=float)
    if rho.ndim != 2 or rho.shape[1] < 3:
        raise ValueError(f"Run for {method.csv_label} has invalid rho_f shape: {rho.shape}")

    truth_theta = as_1d(getattr(run.truth, "theta"), f"{method.csv_label}.truth.theta")
    theta_sch = as_1d(rho[:, 2], f"{method.csv_label}.rho_f[:,3]")
    if theta_sch.size != truth_theta.size:
        raise ValueError(f"theta_sch and truth length mismatch for {method.csv_label}.")

    if ref_time is not None:
        if ref_time.size != theta_sch.size:
            raise ValueError(
                f"Reference time length ({ref_time.size}) does not match {method.csv_label} ({theta_sch.size})."
            )
        time = ref_time.copy()
    else:
        time = np.arange(theta_sch.size, dtype=float) * 0.01

    return {
        "label": method.label,
        "csv_label": method.csv_label,
        "file": str(getattr(run, "file", "")),
        "t": time,
        "theta_sch_deg": np.rad2deg(theta_sch),
        "theta_true_deg": np.rad2deg(truth_theta),
        "theta_err_deg": np.rad2deg(theta_sch - truth_theta),
    }


def validate_against_summary(
    runs: list[dict[str, np.ndarray | str]], summary: dict[str, dict[str, float]]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for method, run in zip(METHODS, runs):
        csv_label = method.csv_label
        if csv_label not in summary:
            raise KeyError(f"Summary CSV has no row for {csv_label}.")

        t = np.asarray(run["t"], dtype=float)
        err = np.asarray(run["theta_err_deg"], dtype=float)
        theta = np.asarray(run["theta_sch_deg"], dtype=float)
        mask = t >= 0.5
        mae = float(np.mean(np.abs(err[mask])))
        peak = float(np.max(np.abs(err[mask])))
        step = float(np.percentile(np.abs(np.diff(theta[mask])), 95))

        checks = {
            "theta_sched_mae_deg": mae,
            "theta_sched_step_p95_deg": step,
        }
        for key, computed in checks.items():
            reported = summary[csv_label].get(key, np.nan)
            if not np.isfinite(reported) or abs(computed - reported) > max(1e-8, 1e-6 * abs(reported)):
                raise ValueError(
                    f"Summary check failed for {csv_label} {key}: "
                    f"computed={computed:.12g}, reported={reported:.12g}"
                )

        rows.append(
            {
                "controller": csv_label,
                "source_file": run["file"],
                "n_samples": int(t.size),
                "t_start_s": f"{float(t[0]):.3f}",
                "t_end_s": f"{float(t[-1]):.3f}",
                "theta_sch_min_deg": f"{float(np.min(theta)):.10g}",
                "theta_sch_max_deg": f"{float(np.max(theta)):.10g}",
                "theta_sched_mae_deg": f"{mae:.10g}",
                "theta_sched_peak_deg": f"{peak:.10g}",
                "theta_sched_step_p95_deg": f"{step:.10g}",
                "summary_theta_sched_mae_deg": f"{summary[csv_label]['theta_sched_mae_deg']:.10g}",
                "summary_theta_sched_step_p95_deg": f"{summary[csv_label]['theta_sched_step_p95_deg']:.10g}",
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
        "theta_sch_min_deg",
        "theta_sch_max_deg",
        "theta_sched_mae_deg",
        "theta_sched_peak_deg",
        "theta_sched_step_p95_deg",
        "summary_theta_sched_mae_deg",
        "summary_theta_sched_step_p95_deg",
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
        np.asarray(ref["theta_true_deg"], dtype=float),
    ]
    headers = ["time_s", "true_slope_deg"]
    for method, run in zip(METHODS, runs):
        prefix = method.csv_label.replace("LPV-MPC_", "LPV_MPC_").replace("-", "_")
        columns.append(np.asarray(run["theta_sch_deg"], dtype=float))
        headers.append(f"{prefix}_theta_sch_deg")
        columns.append(np.asarray(run["theta_err_deg"], dtype=float))
        headers.append(f"{prefix}_theta_error_deg")
    data = np.column_stack(columns)
    np.savetxt(out, data, delimiter=",", header=",".join(headers), comments="", fmt="%.10g")
    return out


def style_axes(ax: plt.Axes, ylabel: str) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_ylabel(ylabel, fontsize=8.1, labelpad=5.0, linespacing=0.95)
    ax.tick_params(axis="both", labelsize=7.3, length=3.0, pad=1.8)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))


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


def build_figure(runs: list[dict[str, np.ndarray | str]]) -> plt.Figure:
    fig, axes = plt.subplots(2, 1, figsize=(7.16, 3.72), sharex=True)
    fig.subplots_adjust(left=0.100, right=0.988, bottom=0.130, top=0.800, hspace=0.380)

    t = np.asarray(runs[0]["t"], dtype=float)
    truth = np.asarray(runs[0]["theta_true_deg"], dtype=float)

    axes[0].plot(t, truth, color=C["true"], lw=1.35, linestyle="-", label="True slope", zorder=6)
    for method, run in zip(METHODS, runs):
        axes[0].plot(
            t,
            np.asarray(run["theta_sch_deg"], dtype=float),
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=5 if method.csv_label in FOCUS_METHODS else 4,
        )
    axes[0].set_xlim(t[0], t[-1])
    axes[0].set_ylim(-9.0, 9.0)
    style_axes(axes[0], "Scheduled slope\n" + r"$\theta^{sch}$ (deg)")
    panel_label(axes[0], "(a)", "Scheduled slope comparison")

    for method, run in zip(METHODS, runs):
        axes[1].plot(
            t,
            np.asarray(run["theta_err_deg"], dtype=float),
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=5 if method.csv_label in FOCUS_METHODS else 4,
        )
    axes[1].axhline(0.0, color="#9AA5AF", lw=0.55, zorder=0)
    axes[1].set_ylim(-9.0, 9.0)
    axes[1].set_xlabel("Time (s)", fontsize=8.4, labelpad=2.5)
    style_axes(axes[1], "Scheduling error\n" + r"$\theta^{sch}-\theta^{true}$ (deg)")
    panel_label(axes[1], "(b)", "Slope scheduling error")

    handle_map = {
        "True slope": Line2D([0], [0], color=C["true"], lw=1.35, linestyle="-", label="True slope")
    }
    for method in METHODS:
        handle_map[method.csv_label] = Line2D(
            [0],
            [0],
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            alpha=method.alpha,
            label=method.label,
        )
    handles = [
        handle_map["True slope"],
        handle_map["LPV-MPC_theta0"],
        handle_map["ModernTCN"],
        handle_map["LPV-MPC_IMU_theta"],
        handle_map["GRU"],
        handle_map["LPV-MPC_oracle_theta"],
        handle_map["TCN"],
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.985),
        ncol=4,
        frameon=False,
        fontsize=7.05,
        handlelength=2.20,
        columnspacing=1.00,
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
