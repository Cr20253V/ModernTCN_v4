"""Generate Fig. 2: Diagonal dual-steer AGV model schematic."""

from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms


PROJECT = Path(r"E:\Matlab\Simulink\S-Function_16")
OUT_DIR = PROJECT / "results" / "paper" / "pic"
OUT_DIR.mkdir(parents=True, exist_ok=True)
STEM = "fig02_agv_model"

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
    "body": "#F7F8FA",
    "body_edge": "#2F3F46",
    "active": "#2F6DB3",
    "active_edge": "#163D73",
    "passive": "#CFD4DA",
    "passive_edge": "#6B737C",
    "force": "#1565C0",
    "dim": "#1F1F1F",
    "aux": "#5B6770",
    "slope": "#E5EDF6",
    "text": "#1A1A1A",
}


def add_arrow(ax, start, end, color=None, lw=1.0, ms=9, style="-|>", ls="-", z=5):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle=style,
            color=color or C["dim"],
            lw=lw,
            linestyle=ls,
            shrinkA=0,
            shrinkB=0,
            mutation_scale=ms,
        ),
        zorder=z,
    )


def rotated_rect(ax, center, width, height, angle_deg, fc, ec, lw=1.05, z=4):
    x, y = center
    rect = mpatches.Rectangle(
        (x - width / 2, y - height / 2),
        width,
        height,
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        zorder=z,
    )
    tr = mtransforms.Affine2D().rotate_deg_around(x, y, angle_deg) + ax.transData
    rect.set_transform(tr)
    ax.add_patch(rect)
    return rect


def add_angle_arc(ax, center, radius, theta1, theta2, label, label_xy, color=None, lw=0.95, fs=8.0):
    arc = mpatches.Arc(
        center,
        2 * radius,
        2 * radius,
        theta1=theta1,
        theta2=theta2,
        linewidth=lw,
        color=color or C["dim"],
        zorder=5,
    )
    ax.add_patch(arc)
    ax.text(*label_xy, label, ha="center", va="center", color=color or C["text"], fontsize=fs, zorder=6)


def wheel_heading(angle_deg):
    """Unit vector along the wheel rolling direction."""
    a = math.radians(angle_deg)
    return -math.sin(a), math.cos(a)


def world_heading_angle(steer_deg):
    """Convert body-axis steering angle to Matplotlib world angle."""
    return 90.0 + steer_deg


def draw_wheel(ax, xy, steer_deg, active, label, label_xy, label_ha):
    fc = C["active"] if active else C["passive"]
    ec = C["active_edge"] if active else C["passive_edge"]
    rotated_rect(ax, xy, 0.14, 0.38, steer_deg, fc, ec, lw=1.05, z=6)
    ax.text(
        *label_xy,
        label,
        ha=label_ha,
        va="center",
        fontsize=8.0,
        color=C["text"],
        linespacing=0.9,
        zorder=7,
    )


def force_arrow(ax, xy, steer_deg, name, offset=0.33):
    x, y = xy
    ux, uy = wheel_heading(steer_deg)
    start = (x + 0.035 * ux, y + 0.065 * uy)
    end = (x + offset * ux, y + offset * uy)
    add_arrow(ax, start, end, color=C["force"], lw=1.05, ms=9.5, z=7)
    ax.text(
        end[0] + 0.04 * ux,
        end[1] + 0.04 * uy,
        name,
        ha="center",
        va="center",
        fontsize=8.0,
        color=C["force"],
        zorder=8,
    )


fig, ax = plt.subplots(figsize=(3.5, 3.35))
fig.subplots_adjust(left=0.045, right=0.970, bottom=0.040, top=0.965)
ax.set_aspect("equal")
ax.set_xlim(-0.98, 1.20)
ax.set_ylim(-1.42, 1.35)
ax.axis("off")


# Vehicle parameters used by the simulation model: L = 2.0 m, W = 0.8 m.
L = 2.0
W = 0.8
cx, cy = 0.12, -0.02
half_l = L / 2
half_w = W / 2

lf = (cx - half_w, cy + half_l)
rf = (cx + half_w, cy + half_l)
lr = (cx - half_w, cy - half_l)
rr = (cx + half_w, cy - half_l)
cg = (cx, cy)


# Chassis outline.
body = mpatches.FancyBboxPatch(
    (cx - half_w, cy - half_l),
    W,
    L,
    boxstyle="round,pad=0.012,rounding_size=0.025",
    linewidth=1.15,
    edgecolor=C["body_edge"],
    facecolor=C["body"],
    zorder=1,
)
ax.add_patch(body)
ax.plot([cx - half_w, cx + half_w], [cy, cy], color=C["aux"], lw=0.8, ls=(0, (4, 3)), zorder=2)
ax.plot([cx, cx], [cy - half_l, cy + half_l], color=C["aux"], lw=0.8, ls=(0, (4, 3)), zorder=2)


# Wheels. LF and RR are the active drive-steer wheels.
steer_lf = 28
steer_rr = -28
draw_wheel(ax, lf, steer_lf, True, "LF active\n drive-steer", (-0.46, 1.00), "right")
draw_wheel(ax, rf, 0, False, "RF passive\n support", (0.70, 1.00), "left")
draw_wheel(ax, lr, 0, False, "LR passive\n support", (-0.45, -1.03), "right")
draw_wheel(ax, rr, steer_rr, True, "RR active\n drive-steer", (0.72, -1.02), "left")


# Active wheel steering angles and longitudinal drive forces.
force_arrow(ax, lf, steer_lf, r"$F_{x,lf}$")
force_arrow(ax, rr, steer_rr, r"$F_{x,rr}$")
for wheel in (lf, rr):
    ax.plot(
        [wheel[0], wheel[0]],
        [wheel[1] - 0.28, wheel[1] + 0.28],
        color=C["active_edge"],
        lw=0.75,
        ls=(0, (2.5, 2.5)),
        zorder=5,
    )
add_angle_arc(
    ax,
    lf,
    0.28,
    90,
    world_heading_angle(steer_lf),
    r"$\delta_{lf}$",
    (lf[0] + 0.28, lf[1] + 0.25),
    color=C["active_edge"],
    lw=1.05,
    fs=9.0,
)
add_angle_arc(
    ax,
    rr,
    0.28,
    world_heading_angle(steer_rr),
    90,
    r"$\delta_{rr}$",
    (rr[0] - 0.27, rr[1] - 0.18),
    color=C["active_edge"],
    lw=1.05,
    fs=9.0,
)


# Body variables and body-fixed frame at the center of gravity.
ax.scatter([cg[0]], [cg[1]], s=22, color=C["dim"], zorder=8)
ax.text(cg[0] + 0.05, cg[1] - 0.055, "CG", ha="left", va="top", fontsize=8.0, color=C["text"], zorder=8)

add_arrow(ax, cg, (cg[0], cg[1] + 0.44), color=C["aux"], lw=0.9, ms=8.5, ls=(0, (3, 3)), z=4)
ax.text(cg[0] + 0.055, cg[1] + 0.39, r"$x_b$", ha="left", va="center", fontsize=8.0, color=C["aux"])
add_arrow(ax, cg, (cg[0] - 0.40, cg[1]), color=C["aux"], lw=0.9, ms=8.5, ls=(0, (3, 3)), z=4)
ax.text(cg[0] - 0.34, cg[1] - 0.065, r"$y_b$", ha="center", va="top", fontsize=8.0, color=C["aux"])

# Heading angle with respect to the global X-axis.
ax.plot([cg[0] - 0.44, cg[0] + 0.50], [cg[1], cg[1]], color=C["aux"], lw=0.75, ls=(0, (5, 4)), zorder=2)
ax.text(cg[0] + 0.43, cg[1] - 0.055, "global X", ha="left", va="top", fontsize=7.5, color=C["aux"])
add_angle_arc(ax, cg, 0.34, 0, 90, r"$\psi$", (cg[0] + 0.36, cg[1] + 0.25), color=C["dim"], fs=9.0)

# Velocity and sideslip angle.
v_tip = (cg[0] - 0.13, cg[1] + 0.50)
add_arrow(ax, cg, v_tip, color=C["dim"], lw=1.05, ms=9.5, z=7)
ax.text(v_tip[0] - 0.03, v_tip[1] + 0.050, r"$v$", ha="center", va="bottom", fontsize=9.0, color=C["text"])
v_world = math.degrees(math.atan2(v_tip[1] - cg[1], v_tip[0] - cg[0]))
add_angle_arc(ax, cg, 0.23, 90, v_world, r"$\beta$", (cg[0] - 0.055, cg[1] + 0.27), color=C["dim"], fs=8.8)

omega = mpatches.FancyArrowPatch(
    (cg[0] + 0.15, cg[1] - 0.03),
    (cg[0] + 0.02, cg[1] + 0.15),
    connectionstyle="arc3,rad=0.75",
    arrowstyle="-|>",
    mutation_scale=9,
    lw=1.0,
    color=C["dim"],
    zorder=7,
)
ax.add_patch(omega)
ax.text(cg[0] + 0.23, cg[1] + 0.07, r"$\omega$", ha="left", va="center", fontsize=9.0, color=C["text"])


# Vehicle dimensions.
dim_x = cx + half_w + 0.18
ax.plot([cx + half_w, dim_x], [cy + half_l, cy + half_l], color=C["dim"], lw=0.8)
ax.plot([cx + half_w, dim_x], [cy - half_l, cy - half_l], color=C["dim"], lw=0.8)
add_arrow(ax, (dim_x, cy - half_l), (dim_x, cy + half_l), color=C["dim"], lw=0.9, ms=8.0, style="<|-|>")
ax.text(dim_x + 0.07, cy, r"$L$", ha="center", va="center", fontsize=9.0, color=C["text"])

dim_y = cy - half_l - 0.18
ax.plot([cx - half_w, cx - half_w], [cy - half_l, dim_y], color=C["dim"], lw=0.8)
ax.plot([cx + half_w, cx + half_w], [cy - half_l, dim_y], color=C["dim"], lw=0.8)
add_arrow(ax, (cx - half_w, dim_y), (cx + half_w, dim_y), color=C["dim"], lw=0.9, ms=8.0, style="<|-|>")
ax.text(cx, dim_y - 0.08, r"$W$", ha="center", va="top", fontsize=9.0, color=C["text"])


# Global frame.
origin = (-0.82, -1.20)
add_arrow(ax, origin, (-0.48, -1.20), color=C["dim"], lw=1.0, ms=9)
add_arrow(ax, origin, (-0.82, -0.84), color=C["dim"], lw=1.0, ms=9)
ax.text(-0.45, -1.21, r"$X$", ha="left", va="top", fontsize=9.0)
ax.text(-0.84, -0.81, r"$Y$", ha="right", va="bottom", fontsize=9.0)
ax.text(-0.85, -1.23, r"$O$", ha="right", va="top", fontsize=8.5)


# Road-slope inset.
base_x, base_y = -0.88, 1.14
ramp_len = 0.46
ramp_h = 0.17
ax.plot([base_x, base_x + ramp_len], [base_y, base_y], color=C["dim"], lw=0.95)
ax.plot([base_x, base_x + ramp_len], [base_y, base_y + ramp_h], color=C["dim"], lw=1.15)
tri = mpatches.Polygon(
    [(base_x, base_y), (base_x + ramp_len, base_y), (base_x + ramp_len, base_y + ramp_h)],
    closed=True,
    facecolor=C["slope"],
    edgecolor="none",
    zorder=0,
)
ax.add_patch(tri)
theta_deg = math.degrees(math.atan2(ramp_h, ramp_len))
add_angle_arc(
    ax,
    (base_x + 0.02, base_y),
    0.19,
    0,
    theta_deg,
    r"$\theta$",
    (base_x + 0.23, base_y + 0.065),
    color=C["dim"],
    fs=8.8,
)
ax.text(base_x + 0.25, base_y + 0.22, "grade angle", ha="center", va="bottom", fontsize=8.0, color=C["aux"])


fig.savefig(OUT_DIR / f"{STEM}.pdf")
fig.savefig(OUT_DIR / f"{STEM}.svg")
fig.savefig(OUT_DIR / f"{STEM}.png", dpi=600)
plt.close(fig)

print(f"Saved: {OUT_DIR / f'{STEM}.pdf'}")
print(f"Saved: {OUT_DIR / f'{STEM}.svg'}")
print(f"Saved: {OUT_DIR / f'{STEM}.png'}")
