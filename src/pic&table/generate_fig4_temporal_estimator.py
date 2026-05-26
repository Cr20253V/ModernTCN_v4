"""Generate Fig. 4: ModernTCN-based multi-task temporal estimator."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


PROJECT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT / "results" / "paper" / "pic"
OUT_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig04_temporal_estimator"

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
    "stroke": "#4A6FA5",
    "arrow": "#2F3F46",
    "input": "#DCEAF6",
    "scale": "#FFF0D4",
    "encoder": "#DDEFD8",
    "shared": "#E8E2F2",
    "class": "#EEF8EA",
    "reg": "#EAF2FC",
    "cond": "#FFF0D4",
    "blue": "#1565C0",
    "green": "#2E7D72",
    "purple": "#665A8F",
    "orange": "#B8822B",
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
    title_size=8.3,
    body_size=7.3,
    lw=1.05,
    rounding=0.014,
    title_pad=0.027,
    body_top_pad=None,
    body_bottom_pad=0.024,
    title_linespacing=0.92,
    body_linespacing=1.02,
    z=2,
):
    patch = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.008,rounding_size={rounding}",
        transform=ax.transAxes,
        linewidth=lw,
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
        default_top = 0.102 if "\n" in title else 0.067
        top = y + h - (body_top_pad if body_top_pad is not None else default_top)
        bottom = y + body_bottom_pad
        if len(lines) == 1:
            ys = [(top + bottom) / 2]
        else:
            ys = [top - i * (top - bottom) / (len(lines) - 1) for i in range(len(lines))]
        for line, yy in zip(lines, ys):
            ax.text(
                x + w / 2,
                yy,
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
            linespacing=title_linespacing,
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
    rad=0.0,
    text=None,
    text_xy=None,
    text_size=7.1,
    text_color=None,
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
            bbox=dict(facecolor="white", edgecolor="none", pad=0.35, alpha=0.88),
        )


def add_group_label(ax, x, y, text):
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=8.2,
        fontweight="bold",
        color=C["muted"],
        zorder=6,
    )


def add_window_matrix(ax, x, y, w, h):
    """Draw a compact 128 x 19 historical feature window."""
    outer = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        transform=ax.transAxes,
        linewidth=1.05,
        edgecolor=C["stroke"],
        facecolor=C["input"],
        zorder=2,
    )
    ax.add_patch(outer)

    ax.text(
        x + w / 2,
        y + h - 0.028,
        "Historical window",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8.3,
        fontweight="bold",
        color=C["text"],
        zorder=4,
    )

    mx, my = x + 0.035, y + 0.170
    mw, mh = w - 0.070, h - 0.260
    matrix = mpatches.Rectangle(
        (mx, my),
        mw,
        mh,
        transform=ax.transAxes,
        facecolor="#F8FBFE",
        edgecolor="#9DB9D3",
        linewidth=0.85,
        zorder=3,
    )
    ax.add_patch(matrix)

    # Sparse grid: enough to signal a matrix without drawing 128 x 19 cells.
    for i in range(1, 8):
        xx = mx + mw * i / 8
        ax.plot([xx, xx], [my, my + mh], transform=ax.transAxes, color="#C9D9E8", lw=0.45, zorder=4)
    for j in range(1, 5):
        yy = my + mh * j / 5
        ax.plot([mx, mx + mw], [yy, yy], transform=ax.transAxes, color="#C9D9E8", lw=0.45, zorder=4)

    # A few feature traces make the window look temporal rather than tabular.
    rng = np.linspace(0, 1, 70)
    for idx, color in enumerate(["#1565C0", "#2E7D72", "#665A8F"]):
        yy = my + mh * (0.24 + 0.23 * idx) + mh * 0.035 * np.sin(2 * np.pi * (rng * (idx + 1.2) + 0.10 * idx))
        xx = mx + mw * rng
        ax.plot(xx, yy, transform=ax.transAxes, color=color, lw=0.75, alpha=0.85, zorder=5)

    ax.text(
        x + w / 2,
        y + 0.080,
        r"$\mathbf{Z}_k \in \mathbb{R}^{128 \times 19}$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=7.7,
        color=C["text"],
        zorder=4,
    )
    ax.text(
        x + w / 2,
        y + 0.040,
        r"128 steps | 19 proprioceptive/derived features | $T_s=0.01$ s",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.3,
        color=C["muted"],
        zorder=4,
    )

    # Axis hints for time and feature dimensions.
    add_arrow(ax, (mx, my - 0.022), (mx + mw, my - 0.022), color=C["muted"], lw=0.7, ms=6.5)
    ax.text(mx + mw / 2, my - 0.042, "time", transform=ax.transAxes, ha="center", va="top", fontsize=6.5, color=C["muted"])
    add_arrow(ax, (mx - 0.012, my), (mx - 0.012, my + mh), color=C["muted"], lw=0.7, ms=6.5)
    ax.text(mx - 0.026, my + mh / 2, "features", transform=ax.transAxes, ha="center", va="center", rotation=90, fontsize=6.6, color=C["muted"])


def add_feature_vector(ax, x, y, w, h):
    patch = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        transform=ax.transAxes,
        linewidth=1.05,
        edgecolor=C["purple"],
        facecolor=C["shared"],
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h - 0.030,
        "Shared temporal\nrepresentation",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=7.5,
        fontweight="bold",
        color=C["text"],
        linespacing=0.90,
        zorder=3,
    )
    vx0, vy = x + 0.035, y + 0.052
    bar_w = (w - 0.070) / 8
    heights = [0.030, 0.052, 0.040, 0.066, 0.046, 0.057, 0.034, 0.049]
    for i, bh in enumerate(heights):
        rect = mpatches.Rectangle(
            (vx0 + i * bar_w, vy),
            bar_w * 0.62,
            bh,
            transform=ax.transAxes,
            facecolor="#FFFFFF",
            edgecolor=C["purple"],
            linewidth=0.65,
            zorder=4,
        )
        ax.add_patch(rect)
    ax.text(
        x + w / 2,
        y + 0.024,
        "temporal readout",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=6.7,
        color=C["muted"],
        zorder=4,
    )
    return patch


def add_head_icon(ax, x, y, kind, color):
    if kind == "class":
        base = y + 0.018
        for i, height in enumerate([0.020, 0.034, 0.027]):
            ax.add_patch(
                mpatches.Rectangle(
                    (x + 0.007 + 0.012 * i, base),
                    0.007,
                    height,
                    transform=ax.transAxes,
                    facecolor=color,
                    edgecolor="none",
                    alpha=0.90,
                    zorder=5,
                )
            )
    else:
        xs = np.linspace(0, 1, 34)
        yy = y + 0.034 + 0.017 * np.sin(2 * np.pi * xs)
        xx = x + 0.006 + 0.045 * xs
        ax.plot(xx, yy, transform=ax.transAxes, color=color, lw=1.05, zorder=5)
        ax.scatter([x + 0.051], [y + 0.034], transform=ax.transAxes, s=10, color=color, zorder=6)


fig, ax = plt.subplots(figsize=(7.16, 3.65))
fig.subplots_adjust(left=0.014, right=0.986, bottom=0.060, top=0.955)
ax.set_axis_off()

add_group_label(ax, 0.155, 0.925, "Input window and preprocessing")
add_group_label(ax, 0.475, 0.925, "ModernTCN shared encoder")
add_group_label(ax, 0.820, 0.925, "Task-specific heads")


# Input and preprocessing.
add_window_matrix(ax, 0.030, 0.335, 0.195, 0.480)

add_box(
    ax,
    0.255,
    0.465,
    0.105,
    0.170,
    "Normalization",
    ["train-set scaler"],
    fc=C["scale"],
    ec=C["orange"],
    title_color=C["orange"],
    title_size=7.8,
    body_size=7.0,
    body_top_pad=0.078,
)
add_arrow(ax, (0.225, 0.575), (0.255, 0.550), lw=1.05)


# ModernTCN encoder as one module with internal building blocks.
enc_x, enc_y, enc_w, enc_h = 0.395, 0.330, 0.250, 0.490
encoder_patch = mpatches.FancyBboxPatch(
    (enc_x, enc_y),
    enc_w,
    enc_h,
    boxstyle="round,pad=0.008,rounding_size=0.014",
    transform=ax.transAxes,
    linewidth=1.05,
    edgecolor=C["green"],
    facecolor=C["encoder"],
    zorder=2,
)
ax.add_patch(encoder_patch)
ax.text(
    enc_x + enc_w / 2,
    enc_y + enc_h - 0.030,
    "ModernTCN encoder",
    transform=ax.transAxes,
    ha="center",
    va="top",
    fontsize=8.4,
    fontweight="bold",
    color=C["green"],
    zorder=4,
)

inner = [
    (0.675, "stem"),
    (0.565, "large-kernel\ntemporal convolution"),
    (0.455, "channel\nmixing"),
    (0.345, "residual\nblocks"),
]
inner_x, inner_w, inner_h = enc_x + 0.034, enc_w - 0.068, 0.075
for y, label in inner:
    add_box(
        ax,
        inner_x,
        y,
        inner_w,
        inner_h,
        label,
        [],
        fc="#F8FCF7",
        ec="#8AB58A",
        title_size=7.0,
        title_color=C["text"],
        lw=0.85,
        rounding=0.010,
        title_linespacing=0.88,
        z=4,
    )
for y0, y1 in zip([0.675, 0.565, 0.455], [0.565, 0.455, 0.345]):
    add_arrow(
        ax,
        (enc_x + enc_w / 2, y0),
        (enc_x + enc_w / 2, y1 + inner_h),
        color=C["green"],
        lw=0.85,
        ms=7.2,
        z=6,
    )

add_arrow(ax, (0.360, 0.550), (enc_x, 0.550), lw=1.05)


# Shared representation and branches.
shared_x, shared_y, shared_w, shared_h = 0.665, 0.468, 0.145, 0.180
add_feature_vector(ax, shared_x, shared_y, shared_w, shared_h)
add_arrow(ax, (enc_x + enc_w, 0.550), (shared_x, 0.550), lw=1.05)

head_x, head_w, head_h = 0.845, 0.135, 0.112
heads = [
    (0.735, "Main-condition\nclassification", "flat | stall | slope", "class", C["green"], C["class"]),
    (0.535, "Steering-direction\nclassification", "right | straight | left", "class", C["green"], C["class"]),
    (0.335, "Slope-related\nregression", r"$\hat{\theta}_k$", "reg", C["blue"], C["reg"]),
]
for y, title, line, kind, color, fill in heads:
    add_box(
        ax,
        head_x,
        y,
        head_w,
        head_h,
        title,
        [line],
        fc=fill,
        ec=color,
        title_color=color,
        title_size=7.1,
        body_size=6.6,
        title_pad=0.020,
        body_top_pad=0.076,
        body_bottom_pad=0.020,
        z=3,
    )
branch_start = (shared_x + shared_w, shared_y + shared_h / 2)
for y, _, _, kind, color, _ in heads:
    add_arrow(
        ax,
        branch_start,
        (head_x, y + head_h / 2),
        color=color,
        lw=1.0,
        ms=8.5,
        rad=0.08 if y > shared_y else (-0.08 if y < shared_y else 0),
    )

note_x, note_y, note_w, note_h = 0.650, 0.145, 0.330, 0.090
add_box(
    ax,
    note_x,
    note_y,
    note_w,
    note_h,
    "Scheduling link",
    [r"$\hat{\theta}_k$ is passed to scheduling conditioning in Fig. 1."],
    fc="#F8FBFE",
    ec="#CBD5DF",
    title_color=C["muted"],
    title_size=6.9,
    body_size=6.7,
    title_pad=0.020,
    body_top_pad=0.058,
    body_bottom_pad=0.018,
    z=3,
)
add_arrow(
    ax,
    (head_x + head_w * 0.50, 0.335),
    (note_x + note_w * 0.52, note_y + note_h),
    color=C["blue"],
    lw=0.90,
    ms=7.8,
    rad=-0.12,
)



fig.savefig(OUT_DIR / f"{STEM}.pdf")
fig.savefig(OUT_DIR / f"{STEM}.svg")
fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
plt.close(fig)

print(f"Saved: {OUT_DIR / f'{STEM}.pdf'}")
print(f"Saved: {OUT_DIR / f'{STEM}.svg'}")
print(f"Saved: {OUT_DIR / f'{STEM}.png'}")
