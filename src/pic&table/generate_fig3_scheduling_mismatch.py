"""Generate Fig. 3: Scheduling mismatch mechanism in LPV-MPC."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
OUT_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig03_scheduling_mismatch"

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
        "mathtext.default": "it",
    }
)


C = {
    "text": "#1A1A1A",
    "muted": "#546E7A",
    "stroke": "#2F3F46",
    "arrow": "#2F3F46",
    "blue": "#1565C0",
    "green": "#2E7D72",
    "red": "#C62828",
    "gray": "#7A7F86",
    "zero_fill": "#F2F4F6",
    "imu_fill": "#EAF5F2",
    "oracle_fill": "#FCEAEA",
    "learned_fill": "#EAF2FC",
    "model_fill": "#E8E2F2",
    "plant_fill": "#F7F8FA",
    "chain_fill": "#FFF0D4",
    "footer_fill": "#F4F7FA",
}


def add_box(
    ax,
    x,
    y,
    w,
    h,
    title,
    lines=(),
    fc="#FFFFFF",
    ec=None,
    title_color=None,
    lw=1.05,
    title_size=8.3,
    body_size=7.6,
    title_pad=0.030,
    body_top_pad=None,
    body_bottom_pad=0.026,
    title_linespacing=0.92,
    body_linespacing=1.02,
    ls="-",
    z=2,
):
    patch = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        transform=ax.transAxes,
        linewidth=lw,
        linestyle=ls,
        edgecolor=ec or C["stroke"],
        facecolor=fc,
        zorder=z,
    )
    ax.add_patch(patch)

    if lines:
        ax.text(
            x + w / 2,
            y + h - title_pad,
            title,
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=title_size,
            fontweight="bold",
            color=title_color or C["text"],
            linespacing=title_linespacing,
            zorder=z + 1,
        )
        default_top_pad = 0.118 if "\n" in title else 0.068
        top = y + h - (body_top_pad if body_top_pad is not None else default_top_pad)
        bottom = y + body_bottom_pad
        if len(lines) == 1:
            yy = [(top + bottom) / 2]
        else:
            yy = [top - i * (top - bottom) / (len(lines) - 1) for i in range(len(lines))]
        for line, ly in zip(lines, yy):
            ax.text(
                x + w / 2,
                ly,
                line,
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=body_size,
                color=C["muted"] if "$" not in line else C["text"],
                linespacing=body_linespacing,
                zorder=z + 1,
            )
    else:
        ax.text(
            x + w / 2,
            y + h / 2,
            title,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=title_size,
            fontweight="bold",
            color=title_color or C["text"],
            zorder=z + 1,
        )
    return patch


def add_arrow(
    ax,
    start,
    end,
    color=None,
    lw=1.05,
    ls="-",
    ms=9.5,
    text=None,
    text_xy=None,
    text_color=None,
    text_size=7.5,
    rad=0.0,
    z=5,
):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops=dict(
            arrowstyle="-|>",
            color=color or C["arrow"],
            lw=lw,
            linestyle=ls,
            shrinkA=3,
            shrinkB=3,
            mutation_scale=ms,
            connectionstyle=f"arc3,rad={rad}",
        ),
        zorder=z,
    )
    if text:
        tx, ty = text_xy if text_xy else ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(
            tx,
            ty,
            text,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=text_size,
            color=text_color or C["muted"],
            zorder=z + 1,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.88),
        )


def add_group_label(ax, x, y, text):
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=8.3,
        fontweight="bold",
        color=C["muted"],
        zorder=6,
    )


fig, ax = plt.subplots(figsize=(7.16, 3.25))
fig.subplots_adjust(left=0.016, right=0.986, bottom=0.060, top=0.955)
ax.set_axis_off()


# Core figure contract: scheduling source determines the LPV local model;
# deviation from the true grade creates prediction mismatch and closed-loop penalties.
add_group_label(ax, 0.172, 0.925, "Compared scheduling sources")
add_group_label(ax, 0.525, 0.925, "LPV-MPC local prediction")
add_group_label(ax, 0.842, 0.925, "Mismatch propagation")


source_x = 0.035
source_w = 0.250
source_h = 0.104
sources = [
    (0.760, "Zero-slope", r"$\theta_k^{sch}=0$", C["gray"], C["zero_fill"], (0, (1.4, 2.0))),
    (0.620, "IMU-based", r"$\theta_k^{sch}=\theta_k^{imu}$", C["green"], C["imu_fill"], (0, (5.0, 2.2))),
    (0.480, "Oracle", r"$\theta_k^{sch}=\theta_k^{true}$", C["red"], C["oracle_fill"], "-"),
    (0.340, "Learned + conditioning", r"$\theta_k^{sch}=\mathcal{S}(\hat{\theta}_k)$", C["blue"], C["learned_fill"], "-"),
]
bus_x = 0.325
for y, title, formula, color, fill, linestyle in sources:
    add_box(
        ax,
        source_x,
        y,
        source_w,
        source_h,
        title,
        [formula],
        fc=fill,
        ec=color,
        title_color=color,
        lw=1.05,
        title_size=8.1,
        body_size=7.7,
    )
    mid_y = y + source_h / 2
    ax.plot(
        [source_x + 0.009, source_x + 0.009],
        [y + 0.018, y + source_h - 0.018],
        transform=ax.transAxes,
        color=color,
        lw=2.3,
        linestyle=linestyle,
        solid_capstyle="round",
        zorder=5,
    )
    add_arrow(
        ax,
        (source_x + source_w, mid_y),
        (bus_x, mid_y),
        color=color,
        lw=1.05,
        ls=linestyle,
        ms=8.5,
    )

ax.plot([bus_x, bus_x], [0.390, 0.810], transform=ax.transAxes, color=C["arrow"], lw=1.0, zorder=4)
ax.text(
    bus_x + 0.013,
    0.600,
    r"scheduled slope $\theta_k^{sch}$",
    transform=ax.transAxes,
    ha="left",
    va="center",
    fontsize=7.6,
    color=C["muted"],
    rotation=90,
    zorder=6,
    bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.90),
)


model_x, model_y, model_w, model_h = 0.410, 0.535, 0.235, 0.285
add_box(
    ax,
    model_x,
    model_y,
    model_w,
    model_h,
    "LPV-MPC\nprediction model",
    [
        r"$A(\rho_k),\ B(\rho_k),\ E(\rho_k)$",
        r"$\rho_k=[v_k,\ \omega_k,\ \theta_k^{sch}]^T$",
        "used by the optimizer",
    ],
    fc=C["model_fill"],
    ec="#665A8F",
    title_size=8.0,
    body_size=7.2,
    body_top_pad=0.136,
    body_bottom_pad=0.030,
)
add_arrow(ax, (bus_x, 0.600), (model_x, 0.665), color=C["arrow"], lw=1.08, ms=9.5)


plant_x, plant_y, plant_w, plant_h = 0.410, 0.175, 0.235, 0.205
add_box(
    ax,
    plant_x,
    plant_y,
    plant_w,
    plant_h,
    "True nonlinear\nAGV plant",
    [
        r"grade condition: $\theta_k^{true}$",
        "measured states close the loop",
    ],
    fc=C["plant_fill"],
    ec=C["stroke"],
    title_size=7.8,
    body_size=7.2,
    body_top_pad=0.126,
    body_bottom_pad=0.030,
)
add_arrow(
    ax,
    (plant_x + 0.060, plant_y + plant_h),
    (source_x + 0.075, 0.340),
    color=C["arrow"],
    lw=0.95,
    ls=(0, (3.0, 2.4)),
    ms=8.2,
    text="feedback enables scheduling",
    text_xy=(0.245, 0.290),
    text_size=7.3,
    rad=-0.12,
)


chain_x = 0.720
chain_w = 0.245
chain_h = 0.115
chain = [
    (0.725, "Scheduling error", r"$e_{\theta,k}=\theta_k^{sch}-\theta_k^{true}$"),
    (0.565, "Model mismatch", "local model differs from\ntrue grade dynamics"),
    (0.405, "Inaccurate prediction", r"biased state prediction"),
    (0.245, "Closed-loop effect", "degraded tracking /\naggressive control"),
]
for y, title, line in chain:
    add_box(
        ax,
        chain_x,
        y,
        chain_w,
        chain_h,
        title,
        [line],
        fc=C["chain_fill"],
        ec="#B8822B",
        title_pad=0.024,
        body_top_pad=0.086,
        body_bottom_pad=0.024,
        title_size=7.5,
        body_size=6.8,
        body_linespacing=0.92,
    )

for idx in range(len(chain) - 1):
    y0 = chain[idx][0]
    y1 = chain[idx + 1][0]
    add_arrow(
        ax,
        (chain_x + chain_w / 2, y0),
        (chain_x + chain_w / 2, y1 + chain_h),
        color=C["arrow"],
        lw=1.05,
        ms=8.8,
    )

add_arrow(
    ax,
    (model_x + model_w, model_y + 0.135),
    (chain_x, 0.790),
    color="#665A8F",
    lw=1.0,
    ms=8.5,
    text=r"$\theta_k^{sch}$",
    text_xy=(0.675, 0.725),
    text_color="#665A8F",
    rad=0.10,
)
add_arrow(
    ax,
    (plant_x + plant_w, plant_y + 0.105),
    (chain_x, 0.758),
    color=C["stroke"],
    lw=1.0,
    ls=(0, (3.0, 2.2)),
    ms=8.5,
    text=r"$\theta_k^{true}$",
    text_xy=(0.684, 0.440),
    text_color=C["stroke"],
    rad=-0.18,
)


footer = mpatches.FancyBboxPatch(
    (0.035, 0.050),
    0.930,
    0.070,
    boxstyle="round,pad=0.006,rounding_size=0.012",
    transform=ax.transAxes,
    linewidth=0.75,
    edgecolor="#CBD5DF",
    facecolor=C["footer_fill"],
    zorder=1,
)
ax.add_patch(footer)
ax.text(
    0.500,
    0.085,
    r"Only the oracle uses $\theta_k^{true}$ directly; zero-slope, IMU-based, and learned schedulers supply compared $\theta_k^{sch}$ signals to the same LPV-MPC.",
    transform=ax.transAxes,
    ha="center",
    va="center",
    fontsize=7.4,
    color=C["muted"],
    zorder=2,
)


fig.savefig(OUT_DIR / f"{STEM}.pdf")
fig.savefig(OUT_DIR / f"{STEM}.svg")
fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
plt.close(fig)

print(f"Saved: {OUT_DIR / f'{STEM}.pdf'}")
print(f"Saved: {OUT_DIR / f'{STEM}.svg'}")
print(f"Saved: {OUT_DIR / f'{STEM}.png'}")
