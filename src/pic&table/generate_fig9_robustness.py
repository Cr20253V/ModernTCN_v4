"""Generate Fig. 9: Robustness under disturbance levels.

The figure reads the existing robustness aggregate CSV and plots only the
learning-based controllers. Aggregate values are validated against the
per-case robustness summary before figure export.
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


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
PROCESS_DIR = PROJECT / "src" / "pic&table"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROCESS_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig09_robustness"

ROBUST_DIR = PROJECT / "results" / "compare" / "robustness_closed_loop"
AGGREGATE_CSV = ROBUST_DIR / "robustness_closed_loop_aggregate.csv"
SUMMARY_CSV = ROBUST_DIR / "robustness_closed_loop_summary.csv"

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
    "modern": "#1565C0",
    "gru": "#E69F00",
    "tcn": "#7B3294",
}


@dataclass(frozen=True)
class MethodSpec:
    label: str
    csv_label: str
    color: str
    linestyle: object
    marker: str
    linewidth: float


METHODS = (
    MethodSpec("ModernTCN", "ModernTCN", C["modern"], "-", "o", 1.18),
    MethodSpec("GRU", "GRU", C["gru"], (0, (4.2, 2.0)), "s", 1.08),
    MethodSpec("TCN", "TCN", C["tcn"], (0, (4.4, 1.6, 1.2, 1.6)), "^", 1.08),
)
LEVELS = (0, 1, 2)


def parse_float(row: dict[str, str], key: str, source: Path) -> float:
    try:
        return float(row[key])
    except KeyError as exc:
        raise KeyError(f"Missing column '{key}' in {source}") from exc
    except ValueError as exc:
        raise ValueError(f"Column '{key}' contains non-numeric value {row.get(key)!r} in {source}") from exc


def load_aggregate(path: Path) -> dict[tuple[int, str], dict[str, float]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing robustness aggregate CSV: {path}")

    required = {
        "disturbance_level",
        "controller",
        "case_count",
        "overall_rank_mean",
        "overall_rank_worst",
        "ey_rmse_mean",
        "xy_rmse_mean",
        "j_du_mean",
        "viol_rate_mean",
        "main_acc_pct_mean",
        "turn_acc_pct_mean",
    }
    out: dict[tuple[int, str], dict[str, float]] = {}
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise KeyError(f"Aggregate CSV is missing columns: {sorted(missing)}")
        for row in reader:
            level = int(parse_float(row, "disturbance_level", path))
            controller = row["controller"]
            if controller not in {m.csv_label for m in METHODS}:
                continue
            key = (level, controller)
            if key in out:
                raise ValueError(f"Duplicate aggregate row for {key}.")
            out[key] = {name: parse_float(row, name, path) for name in required if name != "controller"}
            out[key]["disturbance_level"] = float(level)

    expected = {(level, method.csv_label) for level in LEVELS for method in METHODS}
    missing_keys = expected - set(out)
    if missing_keys:
        raise ValueError(f"Aggregate CSV is missing expected rows: {sorted(missing_keys)}")
    return out


def load_summary(path: Path) -> list[dict[str, float | str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing robustness summary CSV: {path}")
    required = {
        "path_tag",
        "disturbance_level",
        "controller",
        "zone",
        "ey_rmse",
        "xy_rmse",
        "j_du",
        "viol_rate",
    }
    rows: list[dict[str, float | str]] = []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise KeyError(f"Summary CSV is missing columns: {sorted(missing)}")
        for row in reader:
            if row["controller"] not in {m.csv_label for m in METHODS}:
                continue
            if row.get("zone", "") != "all":
                continue
            rows.append(
                {
                    "path_tag": row["path_tag"],
                    "disturbance_level": int(parse_float(row, "disturbance_level", path)),
                    "controller": row["controller"],
                    "ey_rmse": parse_float(row, "ey_rmse", path),
                    "xy_rmse": parse_float(row, "xy_rmse", path),
                    "j_du": parse_float(row, "j_du", path),
                    "viol_rate": parse_float(row, "viol_rate", path),
                }
            )
    if not rows:
        raise ValueError(f"Summary CSV has no matching 'all' rows: {path}")
    return rows


def validate_against_summary(
    aggregate: dict[tuple[int, str], dict[str, float]],
    summary_rows: list[dict[str, float | str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for level in LEVELS:
        for method in METHODS:
            subset = [
                row
                for row in summary_rows
                if row["disturbance_level"] == level and row["controller"] == method.csv_label
            ]
            if not subset:
                raise ValueError(f"No summary rows for d={level}, controller={method.csv_label}.")
            agg = aggregate[(level, method.csv_label)]
            computed = {
                "case_count": float(len(subset)),
                "ey_rmse_mean": float(np.mean([float(row["ey_rmse"]) for row in subset])),
                "xy_rmse_mean": float(np.mean([float(row["xy_rmse"]) for row in subset])),
                "j_du_mean": float(np.mean([float(row["j_du"]) for row in subset])),
                "viol_rate_mean": float(np.mean([float(row["viol_rate"]) for row in subset])),
            }
            for key, value in computed.items():
                reported = agg[key]
                if abs(value - reported) > max(1e-10, 1e-6 * abs(reported)):
                    raise ValueError(
                        f"Aggregate check failed for d={level}, {method.label}, {key}: "
                        f"computed={value:.12g}, reported={reported:.12g}"
                    )
            rows.append(
                {
                    "disturbance_level": level,
                    "controller": method.csv_label,
                    "summary_case_count": len(subset),
                    "aggregate_case_count": int(round(agg["case_count"])),
                    "summary_path_tags": ";".join(str(row["path_tag"]) for row in subset),
                    "ey_rmse_mean": f"{computed['ey_rmse_mean']:.10g}",
                    "xy_rmse_mean": f"{computed['xy_rmse_mean']:.10g}",
                    "j_du_mean": f"{computed['j_du_mean']:.10g}",
                    "viol_rate_mean": f"{computed['viol_rate_mean']:.10g}",
                    "overall_rank_mean": f"{agg['overall_rank_mean']:.10g}",
                    "overall_rank_worst": f"{agg['overall_rank_worst']:.10g}",
                }
            )
    return rows


def write_manifest(rows: list[dict[str, object]]) -> Path:
    manifest = PROCESS_DIR / f"{STEM}_source_manifest.csv"
    fieldnames = [
        "disturbance_level",
        "controller",
        "summary_case_count",
        "aggregate_case_count",
        "summary_path_tags",
        "aggregate_csv",
        "summary_csv",
        "ey_rmse_mean",
        "xy_rmse_mean",
        "j_du_mean",
        "viol_rate_mean",
        "overall_rank_mean",
        "overall_rank_worst",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "aggregate_csv": AGGREGATE_CSV, "summary_csv": SUMMARY_CSV})
    return manifest


def write_source_data(aggregate: dict[tuple[int, str], dict[str, float]]) -> Path:
    out = PROCESS_DIR / f"{STEM}_source_data.csv"
    fieldnames = [
        "disturbance_level",
        "controller",
        "case_count",
        "ey_rmse_mean",
        "xy_rmse_mean",
        "j_du_mean",
        "viol_rate_mean",
        "overall_rank_mean",
        "overall_rank_worst",
        "main_acc_pct_mean",
        "turn_acc_pct_mean",
    ]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for level in LEVELS:
            for method in METHODS:
                agg = aggregate[(level, method.csv_label)]
                writer.writerow(
                    {
                        "disturbance_level": level,
                        "controller": method.csv_label,
                        "case_count": int(round(agg["case_count"])),
                        "ey_rmse_mean": f"{agg['ey_rmse_mean']:.10g}",
                        "xy_rmse_mean": f"{agg['xy_rmse_mean']:.10g}",
                        "j_du_mean": f"{agg['j_du_mean']:.10g}",
                        "viol_rate_mean": f"{agg['viol_rate_mean']:.10g}",
                        "overall_rank_mean": f"{agg['overall_rank_mean']:.10g}",
                        "overall_rank_worst": f"{agg['overall_rank_worst']:.10g}",
                        "main_acc_pct_mean": f"{agg['main_acc_pct_mean']:.10g}",
                        "turn_acc_pct_mean": f"{agg['turn_acc_pct_mean']:.10g}",
                    }
                )
    return out


def write_per_case_source_data(summary_rows: list[dict[str, float | str]]) -> Path:
    out = PROCESS_DIR / f"{STEM}_per_case_source_data.csv"
    fieldnames = ["path_tag", "disturbance_level", "controller", "ey_rmse", "xy_rmse", "j_du", "viol_rate"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(summary_rows, key=lambda r: (int(r["disturbance_level"]), str(r["controller"]), str(r["path_tag"]))):
            writer.writerow(
                {
                    "path_tag": row["path_tag"],
                    "disturbance_level": row["disturbance_level"],
                    "controller": row["controller"],
                    "ey_rmse": f"{float(row['ey_rmse']):.10g}",
                    "xy_rmse": f"{float(row['xy_rmse']):.10g}",
                    "j_du": f"{float(row['j_du']):.10g}",
                    "viol_rate": f"{float(row['viol_rate']):.10g}",
                }
            )
    return out


def series(aggregate: dict[tuple[int, str], dict[str, float]], method: MethodSpec, key: str) -> np.ndarray:
    return np.asarray([aggregate[(level, method.csv_label)][key] for level in LEVELS], dtype=float)


def style_axes(ax: plt.Axes, ylabel: str, set_linear_locator: bool = True) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_xlabel(r"Disturbance level $d$", fontsize=8.35, labelpad=2.8)
    ax.set_ylabel(ylabel, fontsize=8.35, labelpad=2.8)
    ax.set_xlim(-0.12, 2.12)
    ax.set_xticks(LEVELS)
    ax.tick_params(axis="both", labelsize=7.25, length=3.0, pad=1.8)
    if set_linear_locator:
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


def plot_metric(
    ax: plt.Axes,
    aggregate: dict[tuple[int, str], dict[str, float]],
    metric: str,
    ylabel: str,
    log_scale: bool = False,
) -> None:
    x = np.asarray(LEVELS, dtype=float)
    all_values: list[float] = []
    for method in METHODS:
        y = series(aggregate, method, metric)
        all_values.extend(y.tolist())
        ax.plot(
            x,
            y,
            color=method.color,
            linestyle=method.linestyle,
            lw=method.linewidth,
            marker=method.marker,
            markersize=4.2,
            markerfacecolor="white",
            markeredgewidth=0.95,
            markeredgecolor=method.color,
            solid_capstyle="round",
            zorder=5,
        )

    if log_scale:
        ax.set_yscale("log")
        positive = np.asarray([value for value in all_values if value > 0], dtype=float)
        upper = max(2000.0, float(np.max(positive)) * 1.35)
        ax.set_ylim(max(1.0, float(np.min(positive)) * 0.55), upper)
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0,), numticks=5))
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1, numticks=50))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}" if value >= 1 else f"{value:.1g}"))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.grid(True, which="both", color=C["grid"], linewidth=0.42, alpha=0.50)
    else:
        upper = float(np.max(all_values)) * 1.18
        ax.set_ylim(0.0, upper)
    style_axes(ax, ylabel, set_linear_locator=not log_scale)


def build_figure(aggregate: dict[tuple[int, str], dict[str, float]]) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(7.16, 2.92))
    fig.subplots_adjust(left=0.078, right=0.992, bottom=0.210, top=0.750, wspace=0.380)

    plot_metric(axes[0], aggregate, "ey_rmse_mean", r"$e_y$ RMSE (m)")
    panel_label(axes[0], "(a)", "Lateral-error RMSE")

    plot_metric(axes[1], aggregate, "xy_rmse_mean", "XY RMSE (m)")
    panel_label(axes[1], "(b)", "XY-position RMSE")

    plot_metric(axes[2], aggregate, "j_du_mean", r"$J_{\Delta u}$ (log scale)", log_scale=True)
    panel_label(axes[2], "(c)", "Control smoothness cost")

    handles = [
        Line2D(
            [0],
            [0],
            color=method.color,
            lw=method.linewidth,
            linestyle=method.linestyle,
            marker=method.marker,
            markersize=4.2,
            markerfacecolor="white",
            markeredgewidth=0.95,
            markeredgecolor=method.color,
            label=method.label,
        )
        for method in METHODS
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=3,
        frameon=False,
        fontsize=7.35,
        handlelength=2.35,
        columnspacing=1.30,
        handletextpad=0.48,
        borderaxespad=0.0,
    )
    return fig


def main() -> None:
    aggregate = load_aggregate(AGGREGATE_CSV)
    summary_rows = load_summary(SUMMARY_CSV)
    manifest_rows = validate_against_summary(aggregate, summary_rows)

    manifest = write_manifest(manifest_rows)
    source_data = write_source_data(aggregate)
    per_case_data = write_per_case_source_data(summary_rows)

    fig = build_figure(aggregate)
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
    print(f"Saved: {per_case_data}")


if __name__ == "__main__":
    main()
