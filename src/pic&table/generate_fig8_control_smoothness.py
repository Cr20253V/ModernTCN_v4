"""Generate Fig. 8: Control smoothness and constraint behavior.

The figure reads the existing main-route closed-loop comparison outputs. It
uses raw simulated control commands, computes input increments directly from
the logged commands, and validates the resulting metrics against the summary
CSV before exporting the figure and source data. Panel (c) reports the
dimensionless L2 increment norm after normalizing each input channel by its
rate limit; panel (d) reports the maximum channel-wise active-limit hit ratio
and the logged violation rate.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np
import scipy.io as sio


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
PROCESS_DIR = PROJECT / "src" / "pic&table"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESS_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig08_control_smoothness"

COMPARE_DIR = (
    PROJECT
    / "results"
    / "compare"
    / "lpvmpc_theta_baseline"
    / "path_factory_logistics_showcase_theta10_v3"
)
COMPARE_MAT = COMPARE_DIR / "tcn_gru_modern_lpvmpc_theta_baseline_compare.mat"
SUMMARY_CSV = COMPARE_DIR / "tcn_gru_modern_lpvmpc_theta_baseline_summary.csv"

# Default input-rate constraints from the LPV-MPC setup, used only to express
# the plotted input increment as a dimensionless fraction of the rate limits:
# ||[delta_F_cmd / DF_LIMIT, delta_omega_cmd / DOMEGA_LIMIT]||_2.
DF_LIMIT = 400.0
DOMEGA_LIMIT = 0.9
DU_NORM_DEFINITION = (
    f"sqrt((delta_F_cmd_N/{DF_LIMIT:g})^2 + "
    f"(delta_omega_cmd_rad_s/{DOMEGA_LIMIT:g})^2)"
)
LIMIT_HIT_DEFINITION = (
    "channel-wise samples within 1% of the active input limit; "
    "panel d uses max(F_cmd, omega_cmd)"
)
VIOLATION_DEFINITION = "samples outside the active input limits"

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
    "limit": "#111111",
    "limit_band": "#AEB8C2",
    "modern": "#1565C0",
    "gru": "#E69F00",
    "tcn": "#7B3294",
    "theta0": "#7A7F86",
    "imu": "#2E7D72",
    "oracle": "#C62828",
    "bar_aux": "#C6CDD5",
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
    MethodSpec("ModernTCN", "ModernTCN", C["modern"], "-", 1.13),
    MethodSpec("GRU", "GRU", C["gru"], (0, (4.2, 2.0)), 1.03),
    MethodSpec("TCN", "TCN", C["tcn"], (0, (4.4, 1.6, 1.2, 1.6)), 1.03),
    MethodSpec("LPV-MPC theta0", "LPV-MPC_theta0", C["theta0"], (0, (1.2, 1.9)), 0.98, 0.90),
    MethodSpec("LPV-MPC IMU theta", "LPV-MPC_IMU_theta", C["imu"], (0, (5.0, 2.2)), 0.98, 0.92),
    MethodSpec("LPV-MPC oracle theta", "LPV-MPC_oracle_theta", C["oracle"], "-", 1.03),
)


def as_1d(value: object, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size < 2:
        raise ValueError(f"{name} must contain at least two samples.")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values.")
    return arr


def as_limit_array(value: object, name: str, n: int) -> np.ndarray:
    arr = np.asarray(value, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != n or arr.shape[1] < 2:
        raise ValueError(f"{name} must have shape ({n}, >=2), got {arr.shape}.")
    if not np.all(np.isfinite(arr[:, :2])):
        raise ValueError(f"{name} contains non-finite values.")
    return arr[:, :2]


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


def compute_limit_metrics(
    F: np.ndarray, omega: np.ndarray, hi: np.ndarray, lo: np.ndarray
) -> tuple[float, float, float]:
    f_hi = hi[:, 0]
    f_lo = lo[:, 0]
    o_hi = hi[:, 1]
    o_lo = lo[:, 1]
    tol = 1e-8
    f_hit = float(np.mean((F >= 0.99 * f_hi) | (F <= 0.99 * f_lo)) * 100.0)
    o_hit = float(np.mean((omega >= 0.99 * o_hi) | (omega <= 0.99 * o_lo)) * 100.0)
    viol = float(np.mean((F > f_hi + tol) | (F < f_lo - tol) | (omega > o_hi + tol) | (omega < o_lo - tol)))
    return f_hit, o_hit, viol


def extract_run(run: object, method: MethodSpec, ref_time: np.ndarray | None) -> dict[str, np.ndarray | str]:
    if not hasattr(run, "signals"):
        raise KeyError(f"Run for {method.label} has no signals field.")
    sig = run.signals
    required = ("F_cmd", "omega_cmd", "F_limit_hi", "F_limit_lo")
    missing = [name for name in required if not hasattr(sig, name)]
    if missing:
        raise KeyError(f"Run for {method.label} is missing fields: {missing}")

    F = as_1d(getattr(sig, "F_cmd"), f"{method.label}.F_cmd")
    omega = as_1d(getattr(sig, "omega_cmd"), f"{method.label}.omega_cmd")
    if F.size != omega.size:
        raise ValueError(f"F_cmd and omega_cmd length mismatch for {method.label}.")
    n = F.size
    hi = as_limit_array(getattr(sig, "F_limit_hi"), f"{method.label}.F_limit_hi", n)
    lo = as_limit_array(getattr(sig, "F_limit_lo"), f"{method.label}.F_limit_lo", n)

    if ref_time is not None:
        if ref_time.size != n:
            raise ValueError(
                f"Reference time length ({ref_time.size}) does not match {method.label} signals ({n})."
            )
        time = ref_time.copy()
    else:
        time = np.arange(n, dtype=float) * 0.01

    dF = np.diff(F)
    domega = np.diff(omega)
    du_norm = np.sqrt((dF / DF_LIMIT) ** 2 + (domega / DOMEGA_LIMIT) ** 2)
    t_du = time[1:]

    return {
        "label": method.label,
        "csv_label": method.csv_label,
        "file": str(getattr(run, "file", "")),
        "t": time,
        "F_cmd": F,
        "omega_cmd": omega,
        "F_limit_hi": hi[:, 0],
        "F_limit_lo": lo[:, 0],
        "omega_limit_hi": hi[:, 1],
        "omega_limit_lo": lo[:, 1],
        "t_du": t_du,
        "dF": dF,
        "domega": domega,
        "du_norm": du_norm,
    }


def rms(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    if x.size == 0:
        return float("nan")
    return float(np.sqrt(np.mean(np.square(x))))


def peak_abs(x: np.ndarray) -> float:
    return float(np.nanmax(np.abs(x)))


def pct(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    if x.size == 0:
        return float("nan")
    return float(np.mean(x) * 100.0)


def validate_against_summary(
    runs: list[dict[str, np.ndarray | str]], summary: dict[str, dict[str, float]]
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for method, run in zip(METHODS, runs):
        csv_label = method.csv_label
        if csv_label not in summary:
            raise KeyError(f"Summary CSV has no row for {csv_label}.")
        t = np.asarray(run["t"], dtype=float)
        F = np.asarray(run["F_cmd"], dtype=float)
        omega = np.asarray(run["omega_cmd"], dtype=float)
        f_hi = np.asarray(run["F_limit_hi"], dtype=float)
        f_lo = np.asarray(run["F_limit_lo"], dtype=float)
        o_hi = np.asarray(run["omega_limit_hi"], dtype=float)
        o_lo = np.asarray(run["omega_limit_lo"], dtype=float)
        mask = t >= 0.5
        idx = np.flatnonzero(mask)
        if idx.size < 3:
            raise ValueError(f"Too few samples in validation interval for {method.label}.")

        dF = np.diff(F[idx])
        domega = np.diff(omega[idx])
        f_hit, o_hit, viol = compute_limit_metrics(
            F[mask], omega[mask], np.column_stack([f_hi[mask], o_hi[mask]]), np.column_stack([f_lo[mask], o_lo[mask]])
        )

        checks = {
            "F_rms": rms(F[mask]),
            "F_peak": peak_abs(F[mask]),
            "F_sat595_pct": pct(np.abs(F[mask]) >= 595.0),
            "F_limit_hit_pct": f_hit,
            "omega_cmd_rms": rms(omega[mask]),
            "omega_cmd_peak": peak_abs(omega[mask]),
            "omega_sat060_pct": pct(np.abs(omega[mask]) >= 0.60),
            "omega_limit_hit_pct": o_hit,
            "viol_rate": viol,
            "j_du": float(np.mean(dF**2 + domega**2)),
            "dF_rms": rms(dF),
            "domega_cmd_rms": rms(domega),
        }
        for key, computed in checks.items():
            reported = summary[csv_label].get(key, np.nan)
            if not np.isfinite(reported) or abs(computed - reported) > max(1e-8, 1e-6 * abs(reported)):
                raise ValueError(
                    f"Summary check failed for {method.label} {key}: "
                    f"computed={computed:.12g}, reported={reported:.12g}"
                )

        rows.append(
            {
                "controller": csv_label,
                "source_file": run["file"],
                "n_samples": int(t.size),
                "t_start_s": f"{float(t[0]):.3f}",
                "t_end_s": f"{float(t[-1]):.3f}",
                "F_cmd_min_N": f"{float(np.min(F)):.10g}",
                "F_cmd_max_N": f"{float(np.max(F)):.10g}",
                "omega_cmd_min_rad_s": f"{float(np.min(omega)):.10g}",
                "omega_cmd_max_rad_s": f"{float(np.max(omega)):.10g}",
                "du_norm_p95": f"{float(np.percentile(np.asarray(run['du_norm'], dtype=float), 95)):.10g}",
                "du_norm_p99": f"{float(np.percentile(np.asarray(run['du_norm'], dtype=float), 99)):.10g}",
                "du_norm_definition": DU_NORM_DEFINITION,
                "j_du": f"{checks['j_du']:.10g}",
                "dF_rms": f"{checks['dF_rms']:.10g}",
                "domega_cmd_rms": f"{checks['domega_cmd_rms']:.10g}",
                "F_limit_hit_pct": f"{checks['F_limit_hit_pct']:.10g}",
                "omega_limit_hit_pct": f"{checks['omega_limit_hit_pct']:.10g}",
                "limit_hit_definition": LIMIT_HIT_DEFINITION,
                "viol_rate": f"{checks['viol_rate']:.10g}",
                "violation_definition": VIOLATION_DEFINITION,
                "summary_j_du": f"{summary[csv_label]['j_du']:.10g}",
                "summary_viol_rate": f"{summary[csv_label]['viol_rate']:.10g}",
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
        "F_cmd_min_N",
        "F_cmd_max_N",
        "omega_cmd_min_rad_s",
        "omega_cmd_max_rad_s",
        "du_norm_p95",
        "du_norm_p99",
        "du_norm_definition",
        "j_du",
        "dF_rms",
        "domega_cmd_rms",
        "F_limit_hit_pct",
        "omega_limit_hit_pct",
        "limit_hit_definition",
        "viol_rate",
        "violation_definition",
        "summary_j_du",
        "summary_viol_rate",
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
        np.asarray(ref["F_limit_hi"], dtype=float),
        np.asarray(ref["F_limit_lo"], dtype=float),
        np.asarray(ref["omega_limit_hi"], dtype=float),
        np.asarray(ref["omega_limit_lo"], dtype=float),
    ]
    headers = [
        "time_s",
        "reference_F_limit_hi_N",
        "reference_F_limit_lo_N",
        "reference_omega_limit_hi_rad_s",
        "reference_omega_limit_lo_rad_s",
    ]
    for method, run in zip(METHODS, runs):
        prefix = method.csv_label.replace("LPV-MPC_", "LPV_MPC_").replace("-", "_")
        for key, suffix in (
            ("F_cmd", "F_cmd_N"),
            ("omega_cmd", "omega_cmd_rad_s"),
            ("F_limit_hi", "F_limit_hi_N"),
            ("F_limit_lo", "F_limit_lo_N"),
            ("omega_limit_hi", "omega_limit_hi_rad_s"),
            ("omega_limit_lo", "omega_limit_lo_rad_s"),
        ):
            columns.append(np.asarray(run[key], dtype=float))
            headers.append(f"{prefix}_{suffix}")
    data = np.column_stack(columns)
    np.savetxt(out, data, delimiter=",", header=",".join(headers), comments="", fmt="%.10g")

    du_out = PROCESS_DIR / f"{STEM}_input_increment_source_data.csv"
    du_columns = [np.asarray(ref["t_du"], dtype=float)]
    du_headers = ["time_s"]
    for method, run in zip(METHODS, runs):
        prefix = method.csv_label.replace("LPV-MPC_", "LPV_MPC_").replace("-", "_")
        for key, suffix in (
            ("dF", "delta_F_N"),
            ("domega", "delta_omega_rad_s"),
            ("du_norm", "delta_u_norm"),
        ):
            du_columns.append(np.asarray(run[key], dtype=float))
            du_headers.append(f"{prefix}_{suffix}")
    du_data = np.column_stack(du_columns)
    np.savetxt(du_out, du_data, delimiter=",", header=",".join(du_headers), comments="", fmt="%.10g")
    return out


def write_metric_table(summary: dict[str, dict[str, float]]) -> Path:
    out = PROCESS_DIR / f"{STEM}_metric_summary.csv"
    fieldnames = [
        "controller",
        "j_du",
        "dF_rms",
        "domega_cmd_rms",
        "F_sat595_pct",
        "F_limit_hit_pct",
        "omega_sat060_pct",
        "omega_limit_hit_pct",
        "limit_hit_max_pct",
        "limit_hit_max_channel",
        "limit_hit_definition",
        "viol_rate",
        "viol_rate_pct",
        "violation_definition",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for method in METHODS:
            row = summary[method.csv_label]
            if row["F_limit_hit_pct"] >= row["omega_limit_hit_pct"]:
                limit_hit_max = row["F_limit_hit_pct"]
                limit_hit_channel = "F_cmd"
            else:
                limit_hit_max = row["omega_limit_hit_pct"]
                limit_hit_channel = "omega_cmd"
            writer.writerow(
                {
                    "controller": method.csv_label,
                    "j_du": f"{row['j_du']:.10g}",
                    "dF_rms": f"{row['dF_rms']:.10g}",
                    "domega_cmd_rms": f"{row['domega_cmd_rms']:.10g}",
                    "F_sat595_pct": f"{row['F_sat595_pct']:.10g}",
                    "F_limit_hit_pct": f"{row['F_limit_hit_pct']:.10g}",
                    "omega_sat060_pct": f"{row['omega_sat060_pct']:.10g}",
                    "omega_limit_hit_pct": f"{row['omega_limit_hit_pct']:.10g}",
                    "limit_hit_max_pct": f"{limit_hit_max:.10g}",
                    "limit_hit_max_channel": limit_hit_channel,
                    "limit_hit_definition": LIMIT_HIT_DEFINITION,
                    "viol_rate": f"{row['viol_rate']:.10g}",
                    "viol_rate_pct": f"{100.0 * row['viol_rate']:.10g}",
                    "violation_definition": VIOLATION_DEFINITION,
                }
            )
    return out


def style_axes(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_xlabel(xlabel, fontsize=8.4, labelpad=2.5)
    ax.set_ylabel(ylabel, fontsize=8.4, labelpad=2.5)
    ax.tick_params(axis="both", labelsize=7.25, length=3.0, pad=1.8)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
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


def symmetric_ylim(values: np.ndarray, min_span: float = 1e-6, pad_frac: float = 0.08) -> tuple[float, float]:
    peak = float(np.nanmax(np.abs(values)))
    peak = max(peak, min_span)
    return -peak * (1.0 + pad_frac), peak * (1.0 + pad_frac)


def plot_command_panel(
    ax: plt.Axes,
    runs: list[dict[str, np.ndarray | str]],
    command_key: str,
    hi_key: str,
    lo_key: str,
    ylabel: str,
) -> None:
    t_ref = np.asarray(runs[0]["t"], dtype=float)
    hi_stack = np.vstack([np.asarray(run[hi_key], dtype=float) for run in runs])
    lo_stack = np.vstack([np.asarray(run[lo_key], dtype=float) for run in runs])
    hi_inner = np.min(hi_stack, axis=0)
    hi_outer = np.max(hi_stack, axis=0)
    lo_inner = np.max(lo_stack, axis=0)
    lo_outer = np.min(lo_stack, axis=0)

    ax.fill_between(t_ref, hi_inner, hi_outer, color=C["limit_band"], alpha=0.16, linewidth=0.0, zorder=1)
    ax.fill_between(t_ref, lo_outer, lo_inner, color=C["limit_band"], alpha=0.16, linewidth=0.0, zorder=1)
    ax.plot(t_ref, hi_outer, color=C["limit"], lw=0.98, ls=(0, (3.2, 2.0)), alpha=0.90, zorder=2)
    ax.plot(t_ref, lo_outer, color=C["limit"], lw=0.98, ls=(0, (3.2, 2.0)), alpha=0.90, zorder=2)

    for method, run in zip(METHODS, runs):
        t = np.asarray(run["t"], dtype=float)
        y = np.asarray(run[command_key], dtype=float)
        ax.plot(
            t,
            y,
            color=method.color,
            linestyle=method.linestyle,
            lw=method.linewidth,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=5 if "LPV-MPC" not in method.label else 4,
        )

    all_values = [np.asarray(run[command_key], dtype=float) for run in runs]
    all_values.extend([hi_outer, lo_outer])
    ax.set_xlim(t_ref[0], t_ref[-1])
    ax.set_ylim(*symmetric_ylim(np.concatenate(all_values)))
    style_axes(ax, "Time (s)", ylabel)


def plot_increment_panel(ax: plt.Axes, runs: list[dict[str, np.ndarray | str]]) -> None:
    for method, run in zip(METHODS, runs):
        ax.plot(
            np.asarray(run["t_du"], dtype=float),
            np.asarray(run["du_norm"], dtype=float),
            color=method.color,
            linestyle=method.linestyle,
            lw=method.linewidth,
            alpha=method.alpha,
            solid_capstyle="round",
            zorder=5 if "LPV-MPC" not in method.label else 4,
        )
    ax.axhline(1.0, color=C["limit"], lw=0.80, ls=(0, (3.2, 2.0)), alpha=0.82)
    ax.set_xlim(np.asarray(runs[0]["t"], dtype=float)[0], np.asarray(runs[0]["t"], dtype=float)[-1])
    ax.set_ylim(-0.05, 1.50)
    style_axes(ax, "Time (s)", "Normalized input increment\n" + r"$\|\Delta u_k^{norm}\|_2$")


def plot_metric_panel(
    ax: plt.Axes,
    summary: dict[str, dict[str, float]],
) -> None:
    x = np.arange(len(METHODS), dtype=float)
    j_vals = np.asarray([summary[m.csv_label]["j_du"] for m in METHODS], dtype=float)
    hit_vals = np.asarray(
        [
            max(summary[m.csv_label]["F_limit_hit_pct"], summary[m.csv_label]["omega_limit_hit_pct"])
            for m in METHODS
        ],
        dtype=float,
    )
    viol_pct = np.asarray([100.0 * summary[m.csv_label]["viol_rate"] for m in METHODS], dtype=float)

    width = 0.38
    ax.bar(
        x - width / 2,
        j_vals,
        width=width,
        color=[m.color for m in METHODS],
        edgecolor="white",
        linewidth=0.45,
        label=r"$J_{\Delta u}$",
        zorder=3,
    )
    ax.set_yscale("log")
    ax.set_ylim(0.035, max(j_vals) * 1.7)
    ax.set_ylabel("Smoothness cost\n" + r"$J_{\Delta u}$", fontsize=8.4, labelpad=2.5)
    ax.grid(True, axis="y", color=C["grid"], linewidth=0.45, alpha=0.55, which="both")
    ax.tick_params(axis="y", labelsize=7.25, length=3.0, pad=1.8)
    ax.spines["top"].set_visible(False)

    ax2 = ax.twinx()
    ax2.bar(
        x + width / 2,
        hit_vals,
        width=width,
        color=C["bar_aux"],
        edgecolor="#7C8792",
        linewidth=0.42,
        hatch="///",
        alpha=0.92,
        label="Max limit hit",
        zorder=2,
    )
    ax2.scatter(
        x + width / 2,
        viol_pct,
        s=13,
        marker="D",
        color=C["limit"],
        linewidths=0.0,
        zorder=4,
        label="Violation",
    )
    ax2.set_ylim(0, max(hit_vals) * 1.18)
    ax2.set_ylabel("Max limit hit / violation (%)", fontsize=8.4, labelpad=3.0)
    ax2.tick_params(axis="y", labelsize=7.25, length=3.0, pad=1.8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_linewidth(0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(
        ["ModernTCN", "GRU", "TCN", "theta0", "IMU", "oracle"],
        fontsize=6.25,
        rotation=18,
        ha="right",
        rotation_mode="anchor",
    )
    ax.tick_params(axis="x", length=0, pad=1.4)
    ax.set_xlabel("Controller", fontsize=8.4, labelpad=4.2)

    # Small labels on the largest constraint bars keep the secondary metric
    # readable without adding another legend row.
    for xi, hit, viol in zip(x, hit_vals, viol_pct):
        if hit > 1.0:
            ax2.text(
                xi + width / 2,
                hit + max(hit_vals) * 0.025,
                f"{hit:.1f}",
                ha="center",
                va="bottom",
                fontsize=5.85,
                color=C["muted"],
                rotation=0,
            )
        if viol > 1.0:
            ax2.text(
                xi + width / 2,
                viol + max(hit_vals) * 0.025,
                f"{viol:.1f}",
                ha="center",
                va="bottom",
                fontsize=5.85,
                color=C["muted"],
            )
    return ax2


def build_figure(
    runs: list[dict[str, np.ndarray | str]],
    summary: dict[str, dict[str, float]],
) -> plt.Figure:
    fig, axes = plt.subplots(2, 2, figsize=(7.16, 4.36))
    fig.subplots_adjust(left=0.078, right=0.922, bottom=0.145, top=0.815, wspace=0.330, hspace=0.480)

    plot_command_panel(axes[0, 0], runs, "F_cmd", "F_limit_hi", "F_limit_lo", r"Driving force $F_{cmd}$ (N)")
    panel_label(axes[0, 0], "(a)", "Driving force command")

    plot_command_panel(
        axes[0, 1],
        runs,
        "omega_cmd",
        "omega_limit_hi",
        "omega_limit_lo",
        r"Yaw-rate command $\omega_{cmd}$ (rad/s)",
    )
    panel_label(axes[0, 1], "(b)", "Yaw-rate command")

    plot_increment_panel(axes[1, 0], runs)
    panel_label(axes[1, 0], "(c)", "Input increment")

    metric_ax2 = plot_metric_panel(axes[1, 1], summary)
    panel_label(axes[1, 1], "(d)", "Smoothness and limits")

    handle_map = {
        "Limit": Line2D(
            [0],
            [0],
            color=C["limit"],
            lw=1.05,
            linestyle=(0, (3.2, 2.0)),
            label="Input-limit envelope",
        )
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
    handles = [
        handle_map["ModernTCN"],
        handle_map["LPV-MPC theta0"],
        handle_map["GRU"],
        handle_map["LPV-MPC IMU theta"],
        handle_map["TCN"],
        handle_map["LPV-MPC oracle theta"],
        handle_map["Limit"],
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.982),
        ncol=4,
        frameon=False,
        fontsize=7.0,
        handlelength=2.10,
        columnspacing=0.95,
        handletextpad=0.45,
        borderaxespad=0.0,
    )

    metric_handles = [
        Patch(facecolor="#AAB3BD", edgecolor="#7C8792", hatch="///", label="Max limit hit"),
        Line2D([0], [0], color=C["limit"], marker="D", linestyle="None", markersize=4.0, label="Violation"),
    ]
    axes[1, 1].legend(
        handles=metric_handles,
        loc="upper left",
        bbox_to_anchor=(0.005, 0.985),
        frameon=False,
        fontsize=6.55,
        handlelength=1.35,
        borderaxespad=0.0,
        labelspacing=0.25,
    )

    # Keep a reference to the secondary axis until save time.
    fig._fig8_metric_axis = metric_ax2  # type: ignore[attr-defined]
    return fig


def main() -> None:
    raw_runs, path_file = load_compare_runs(COMPARE_MAT)
    ref_time = load_reference_time(path_file)
    runs = [extract_run(run, method, ref_time) for run, method in zip(raw_runs, METHODS)]
    summary = load_summary(SUMMARY_CSV)
    manifest_rows = validate_against_summary(runs, summary)

    manifest = write_manifest(manifest_rows, path_file)
    source_data = write_source_data(runs)
    metric_summary = write_metric_table(summary)

    fig = build_figure(runs, summary)
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
    print(f"Saved: {PROCESS_DIR / (STEM + '_input_increment_source_data.csv')}")
    print(f"Saved: {metric_summary}")


if __name__ == "__main__":
    main()
