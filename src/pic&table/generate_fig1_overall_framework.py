"""Generate Fig. 1: Overall framework of temporal-perception-enhanced LPV-MPC."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


PROJECT = Path(r"E:\Matlab\Simulink\S-Function_16")
OUT_DIR = PROJECT / "results" / "paper" / "pic"
OUT_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig01_overall_framework"

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
    }
)


C = {
    "meas": "#DCEAF6",
    "window": "#C6DDF0",
    "est": "#DDEFD8",
    "head": "#EEF8EA",
    "cond": "#FFF0D4",
    "sched": "#DDEBF8",
    "ctrl": "#E8E2F2",
    "plant": "#F0E2EF",
    "stroke": "#4A6FA5",
    "arrow": "#2F3F46",
    "text": "#1A1A1A",
    "muted": "#546E7A",
    "blue": "#1565C0",
}


def box(ax, x, y, w, h, title, lines, fc, title_size=8.8, body_size=8.0, body_ls=1.0):
    patch = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.018",
        transform=ax.transAxes,
        linewidth=1.15,
        edgecolor=C["stroke"],
        facecolor=fc,
        zorder=2,
    )
    ax.add_patch(patch)

    title_pad = 0.030 if h < 0.14 else 0.045
    title_y = y + h / 2 if not lines else y + h - title_pad
    title_va = "center" if not lines else "top"
    ax.text(
        x + w / 2,
        title_y,
        title,
        transform=ax.transAxes,
        ha="center",
        va=title_va,
        fontsize=title_size,
        fontweight="bold",
        color=C["text"],
        linespacing=1.02,
        zorder=3,
    )

    if lines:
        top = y + h - (0.090 if h < 0.15 else 0.112)
        bottom = y + (0.030 if h < 0.15 else 0.045)
        ys = [(top + bottom) / 2] if len(lines) == 1 else [
            top - i * (top - bottom) / (len(lines) - 1) for i in range(len(lines))
        ]
        for line, yy in zip(lines, ys):
            ax.text(
                x + w / 2,
                yy,
                line,
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=body_size,
                color=C["blue"] if "$" in line else C["muted"],
                linespacing=body_ls,
                zorder=3,
            )
    return patch


def arrow(ax, start, end, text=None, text_xy=None, dashed=False, lw=1.15, text_size=8.0):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        xycoords=ax.transAxes,
        textcoords=ax.transAxes,
        arrowprops=dict(
            arrowstyle="-|>",
            color=C["arrow"],
            lw=lw,
            linestyle="--" if dashed else "-",
            shrinkA=4,
            shrinkB=4,
            mutation_scale=10,
        ),
        zorder=5,
    )
    if text:
        x, y = text_xy if text_xy else (
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2,
        )
        ax.text(
            x,
            y,
            text,
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=text_size,
            color=C["muted"],
            fontstyle="italic",
            zorder=6,
        )


fig, ax = plt.subplots(figsize=(7.16, 3.45))
fig.subplots_adjust(left=0.014, right=0.988, bottom=0.055, top=0.965)
ax.set_axis_off()


# Perception chain.
box(
    ax,
    0.025,
    0.615,
    0.200,
    0.305,
    "AGV measurements",
    [
        "acceleration | yaw rate",
        "steering angles | wheel speeds",
        "current-related features",
        "velocity / pitch-related features",
    ],
    C["meas"],
    title_size=8.7,
    body_size=7.0,
)

box(
    ax,
    0.255,
    0.640,
    0.155,
    0.255,
    "Historical window",
    [
        r"$\mathbf{Z}_k \in \mathbb{R}^{128 \times 19}$",
        "128 steps, 19 features",
        r"$T_s = 0.01$ s",
    ],
    C["window"],
    title_size=9.0,
    body_size=8.0,
)

box(
    ax,
    0.445,
    0.585,
    0.220,
    0.350,
    "Temporal perception",
    [
        "ModernTCN-based estimator",
        "multi-task outputs",
    ],
    C["est"],
    title_size=8.4,
    body_size=7.8,
    body_ls=0.95,
)

head_x, head_w, head_h = 0.725, 0.240, 0.108
heads = [
    (0.790, "Main condition", "flat / stall / slope"),
    (0.655, "Steering direction", "right / straight / left"),
    (0.520, "Slope-related\nestimate", r"$\hat{\theta}_k$"),
]
for y, title, line in heads:
    box(
        ax,
        head_x,
        y,
        head_w,
        head_h,
        title,
        [line],
        C["head"],
        title_size=8.3,
        body_size=8.0,
    )

arrow(ax, (0.225, 0.768), (0.255, 0.768))
arrow(ax, (0.410, 0.768), (0.445, 0.768))

bus_x = 0.700
head_ys = [y + head_h / 2 for y, _, _ in heads]
ax.plot([0.665, bus_x], [0.760, 0.760], transform=ax.transAxes, color=C["arrow"], lw=1.05, zorder=4)
ax.plot([bus_x, bus_x], [head_ys[-1], head_ys[0]], transform=ax.transAxes, color=C["arrow"], lw=1.05, zorder=4)
for hy in head_ys:
    arrow(ax, (bus_x, hy), (head_x, hy), lw=1.05)


# Closed-loop LPV-MPC update.
box(
    ax,
    0.725,
    0.210,
    0.240,
    0.225,
    "Scheduling conditioning",
    ["magnitude/rate limits", "dead-zone"],
    C["cond"],
    title_size=8.1,
    body_size=8.0,
)

box(
    ax,
    0.480,
    0.230,
    0.198,
    0.188,
    "LPV-MPC\nscheduler",
    [r"$\boldsymbol{\rho}_k = [v_k,\, \omega_k,\, \theta_k^{sch}]^T$"],
    C["sched"],
    title_size=8.4,
    body_size=8.0,
)

box(
    ax,
    0.255,
    0.230,
    0.178,
    0.188,
    "LPV-MPC\ncontroller",
    ["constrained optimization"],
    C["ctrl"],
    title_size=8.4,
    body_size=8.0,
)

box(
    ax,
    0.025,
    0.230,
    0.190,
    0.188,
    "Nonlinear diagonal\n dual-steer AGV plant",
    [],
    C["plant"],
    title_size=8.3,
)

arrow(
    ax,
    (head_x + head_w / 2, 0.520),
    (0.845, 0.435),
    text=r"$\hat{\theta}_k$",
    text_xy=(0.890, 0.475),
    lw=1.15,
    text_size=8.0,
)
arrow(ax, (0.725, 0.324), (0.678, 0.324))
arrow(ax, (0.480, 0.324), (0.433, 0.324))
arrow(ax, (0.255, 0.324), (0.215, 0.324))
ax.text(
    0.236,
    0.382,
    r"$\mathbf{u}_k=[F_{\mathrm{cmd}},\,\omega_{\mathrm{cmd}}]^T$",
    transform=ax.transAxes,
    ha="center",
    va="bottom",
    fontsize=8.0,
    color=C["muted"],
    zorder=6,
    bbox=dict(facecolor="white", edgecolor="none", pad=0.5, alpha=0.92),
)

arrow(ax, (0.120, 0.418), (0.120, 0.615), dashed=True, lw=1.05)
ax.text(
    0.178,
    0.520,
    "proprioceptive\nfeedback",
    transform=ax.transAxes,
    ha="left",
    va="center",
    fontsize=8.0,
    color=C["muted"],
    fontstyle="italic",
)


fig.savefig(OUT_DIR / f"{STEM}.pdf")
fig.savefig(OUT_DIR / f"{STEM}.svg")
fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
plt.close(fig)

print(f"Saved: {OUT_DIR / f'{STEM}.pdf'}")
print(f"Saved: {OUT_DIR / f'{STEM}.svg'}")
print(f"Saved: {OUT_DIR / f'{STEM}.png'}")
