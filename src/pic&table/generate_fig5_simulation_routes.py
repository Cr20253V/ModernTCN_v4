"""Generate Fig. 5: Closed-loop simulation routes.

The figure reads the existing closed-loop route MAT files and plots only the
reference paths, start/end markers, and travel direction arrows.
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
STEM = "fig05_simulation_routes"

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
    "path": "#111111",
    "start": "#2E7D72",
    "end": "#C62828",
    "arrow": "#1565C0",
}


@dataclass(frozen=True)
class RouteSpec:
    panel: str
    title: str
    mat_file: Path
    arrow_fracs: tuple[float, ...]
    x_pad_left_frac: float = 0.08
    x_pad_right_frac: float = 0.08
    y_pad_frac: float = 0.08


ROUTES = (
    RouteSpec(
        "(a)",
        "Factory logistics showcase",
        PROJECT / "data" / "paths" / "path_factory_logistics_showcase_theta10_v3.mat",
        (0.12, 0.34, 0.58, 0.82),
        x_pad_right_frac=0.18,
    ),
    RouteSpec(
        "(b)",
        "Long up/down slope",
        PROJECT / "data" / "paths" / "path_closed_loop_long_updown_theta10_v1.mat",
        (0.18, 0.50, 0.78),
    ),
    RouteSpec(
        "(c)",
        "Sharp turn transition",
        PROJECT / "data" / "paths" / "path_closed_loop_sharp_turn_transition_theta10_v1.mat",
        (0.17, 0.48, 0.77),
    ),
)


def as_1d(value: object, name: str) -> np.ndarray:
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size < 2:
        raise ValueError(f"{name} must contain at least two samples.")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values.")
    return arr


def load_route(spec: RouteSpec) -> dict[str, np.ndarray]:
    if not spec.mat_file.exists():
        raise FileNotFoundError(f"Missing route MAT file: {spec.mat_file}")

    data = sio.loadmat(spec.mat_file, squeeze_me=True, struct_as_record=False)
    if "ref" not in data:
        raise KeyError(f"MAT file does not contain variable 'ref': {spec.mat_file}")

    ref = data["ref"]
    required = ("t", "X_ref", "Y_ref")
    missing = [name for name in required if not hasattr(ref, name)]
    if missing:
        raise KeyError(f"ref is missing required fields {missing}: {spec.mat_file}")

    t = as_1d(getattr(ref, "t"), "ref.t")
    x = as_1d(getattr(ref, "X_ref"), "ref.X_ref")
    y = as_1d(getattr(ref, "Y_ref"), "ref.Y_ref")
    if not (t.size == x.size == y.size):
        raise ValueError(f"Route arrays have inconsistent lengths: {spec.mat_file}")

    distance = np.sum(np.hypot(np.diff(x), np.diff(y)))
    return {"t": t, "x": x, "y": y, "distance": np.array([distance])}


def cumulative_distance(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    ds = np.hypot(np.diff(x), np.diff(y))
    return np.r_[0.0, np.cumsum(ds)]


def add_direction_arrows(
    ax: plt.Axes,
    x: np.ndarray,
    y: np.ndarray,
    fractions: tuple[float, ...],
    length_frac: float = 0.028,
) -> None:
    s = cumulative_distance(x, y)
    total = float(s[-1])
    if total <= 0:
        return

    for frac in fractions:
        start_s = np.clip(frac, 0.0, 0.98) * total
        end_s = min(start_s + length_frac * total, total)
        i = int(np.searchsorted(s, start_s, side="left"))
        j = int(np.searchsorted(s, end_s, side="left"))
        if j <= i:
            j = min(i + 8, x.size - 1)
        if j <= i or np.hypot(x[j] - x[i], y[j] - y[i]) <= 1e-9:
            continue

        ax.annotate(
            "",
            xy=(x[j], y[j]),
            xytext=(x[i], y[i]),
            arrowprops=dict(
                arrowstyle="-|>",
                color=C["arrow"],
                lw=1.05,
                shrinkA=0,
                shrinkB=0,
                mutation_scale=8.5,
            ),
            zorder=5,
        )


BOX_ASPECT = 0.66  # height / width. Keeps equal data aspect while avoiding tall, sparse panels.
TARGET_ASPECT = 1.0 / BOX_ASPECT


def set_equal_limits(ax: plt.Axes, spec: RouteSpec, x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float]:
    xmin, xmax = float(np.min(x)), float(np.max(x))
    ymin, ymax = float(np.min(y)), float(np.max(y))
    xspan = max(xmax - xmin, 1e-6)
    yspan = max(ymax - ymin, 1e-6)

    xlo = xmin - spec.x_pad_left_frac * xspan
    xhi = xmax + spec.x_pad_right_frac * xspan
    ylo = ymin - spec.y_pad_frac * yspan
    yhi = ymax + spec.y_pad_frac * yspan

    padded_xspan = max(xhi - xlo, 1e-6)
    padded_yspan = max(yhi - ylo, 1e-6)
    if padded_xspan / padded_yspan < TARGET_ASPECT:
        needed_xspan = padded_yspan * TARGET_ASPECT
        extra = needed_xspan - padded_xspan
        xlo -= 0.5 * extra
        xhi += 0.5 * extra
    else:
        needed_yspan = padded_xspan / TARGET_ASPECT
        extra = needed_yspan - padded_yspan
        ylo -= 0.5 * extra
        yhi += 0.5 * extra

    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    ax.set_box_aspect(BOX_ASPECT)
    ax.set_aspect("equal", adjustable="box")
    return xlo, xhi, ylo, yhi


def style_axes(ax: plt.Axes) -> None:
    ax.grid(True, color=C["grid"], linewidth=0.45, alpha=0.55)
    ax.set_xlabel("X (m)", fontsize=8.5, labelpad=2.5)
    ax.set_ylabel("Y (m)", fontsize=8.5, labelpad=2.5)
    ax.tick_params(axis="both", labelsize=7.2, length=3.0, pad=1.8)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))


def write_manifest(rows: list[dict[str, object]]) -> Path:
    manifest = PROCESS_DIR / f"{STEM}_source_manifest.csv"
    fieldnames = [
        "panel",
        "title",
        "path_file",
        "duration_s",
        "n_samples",
        "distance_m",
        "x_min_m",
        "x_max_m",
        "y_min_m",
        "y_max_m",
        "xlim_min_m",
        "xlim_max_m",
        "ylim_min_m",
        "ylim_max_m",
        "box_aspect_h_over_w",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return manifest


def save_with_fallback(fig: plt.Figure, path: Path, **kwargs) -> Path:
    try:
        fig.savefig(path, **kwargs)
        return path
    except PermissionError:
        fallback = path.with_name(f"{path.stem}_updated{path.suffix}")
        fig.savefig(fallback, **kwargs)
        print(f"Locked, saved fallback: {fallback}")
        return fallback


def main() -> None:
    route_data = [load_route(spec) for spec in ROUTES]

    fig, axes = plt.subplots(1, 3, figsize=(7.16, 2.66))
    fig.subplots_adjust(left=0.065, right=0.992, bottom=0.185, top=0.835, wspace=0.280)
    fig.canvas.draw()

    manifest_rows: list[dict[str, object]] = []
    for ax, spec, data in zip(axes, ROUTES, route_data):
        x, y, t = data["x"], data["y"], data["t"]

        ax.plot(x, y, color=C["path"], lw=1.22, solid_capstyle="round", zorder=3)
        ax.scatter(x[0], y[0], s=32, marker="o", color=C["start"], edgecolor="white", linewidth=0.55, zorder=6)
        ax.scatter(x[-1], y[-1], s=34, marker="s", color=C["end"], edgecolor="white", linewidth=0.55, zorder=6)
        add_direction_arrows(ax, x, y, spec.arrow_fracs)
        xlo, xhi, ylo, yhi = set_equal_limits(ax, spec, x, y)
        style_axes(ax)

        ax.text(
            0.0,
            1.055,
            f"{spec.panel} {spec.title}",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=8.1,
            fontweight="bold",
            color=C["text"],
            clip_on=False,
        )

        manifest_rows.append(
            {
                "panel": spec.panel,
                "title": spec.title,
                "path_file": str(spec.mat_file),
                "duration_s": f"{t[-1] - t[0]:.3f}",
                "n_samples": int(t.size),
                "distance_m": f"{float(data['distance'][0]):.3f}",
                "x_min_m": f"{float(np.min(x)):.3f}",
                "x_max_m": f"{float(np.max(x)):.3f}",
                "y_min_m": f"{float(np.min(y)):.3f}",
                "y_max_m": f"{float(np.max(y)):.3f}",
                "xlim_min_m": f"{xlo:.3f}",
                "xlim_max_m": f"{xhi:.3f}",
                "ylim_min_m": f"{ylo:.3f}",
                "ylim_max_m": f"{yhi:.3f}",
                "box_aspect_h_over_w": f"{BOX_ASPECT:.3f}",
            }
        )

    legend_handles = [
        Line2D([0], [0], color=C["path"], lw=1.22, label="Reference path"),
        Line2D(
            [0],
            [0],
            marker="o",
            linestyle="None",
            markerfacecolor=C["start"],
            markeredgecolor="white",
            markeredgewidth=0.55,
            markersize=5.8,
            label="Start",
        ),
        Line2D(
            [0],
            [0],
            marker="s",
            linestyle="None",
            markerfacecolor=C["end"],
            markeredgecolor="white",
            markeredgewidth=0.55,
            markersize=5.8,
            label="End",
        ),
        Line2D([0], [0], color=C["arrow"], lw=1.05, marker=">", markevery=[1], markersize=5.0, label="Travel direction"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.965),
        ncol=4,
        frameon=False,
        fontsize=7.0,
        handlelength=1.48,
        columnspacing=1.05,
        handletextpad=0.45,
    )

    pdf_file = OUT_DIR / f"{STEM}.pdf"
    svg_file = OUT_DIR / f"{STEM}.svg"
    png_file = OUT_DIR / f"{STEM}.png"
    saved_pdf = save_with_fallback(fig, pdf_file)
    saved_svg = save_with_fallback(fig, svg_file)
    saved_png = save_with_fallback(fig, png_file, dpi=600)
    plt.close(fig)

    manifest = write_manifest(manifest_rows)
    print(f"Saved: {saved_pdf}")
    print(f"Saved: {saved_svg}")
    print(f"Saved: {saved_png}")
    print(f"Saved: {manifest}")


if __name__ == "__main__":
    main()
