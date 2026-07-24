import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Ellipse
import numpy as np
import os

ORANGE = "#F9770B"
ORANGE_D = "#C85A00"
DARK = "#2E2E2E"
GREY = "#8A8A8A"
LIGHT = "#FBEAD9"
BLUE = "#2C6E8F"

os.makedirs("assets", exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"

def save(fig, name):
    fig.savefig(f"assets/{name}.png", dpi=200, transparent=True,
                bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("wrote", name)

# ---------------------------------------------------------------
# Diagram 1 - Slide 2: same parabola hiding in three scenes
# ---------------------------------------------------------------
def diagram_parabola():
    fig, ax = plt.subplots(figsize=(11, 3.3))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.2); ax.axis("off")
    titles = ["Cliff Diver", "Welding Sparks", "Fountain Arc"]
    # panel separators
    for xsep in (4, 8):
        ax.plot([xsep, xsep], [0.2, 4.0], color=GREY, lw=1, ls=(0,(2,3)))
    for i, t in enumerate(titles):
        ax.text(2 + 4*i, 3.95, t, ha="center", va="top", fontsize=13,
                color=DARK, fontweight="bold")
    # one continuous dashed parabola across the whole strip
    x = np.linspace(0.4, 11.6, 400)
    peak, x0 = 3.3, 6.0
    y = peak - 0.075*(x - x0)**2
    mask = y > 0.25
    ax.plot(x[mask], y[mask], color=ORANGE, lw=3, ls=(0,(6,4)), zorder=2)
    ax.text(x0, peak+0.05, "one parabola", ha="center", color=ORANGE_D,
            fontsize=11, fontstyle="italic", fontweight="bold")
    # markers per panel
    # panel1: diver figure near start
    dx, dy = 1.4, peak - 0.075*(1.4-x0)**2
    ax.add_patch(Circle((dx, dy+0.18), 0.12, color=DARK, zorder=4))
    ax.plot([dx, dx],[dy+0.06, dy-0.28], color=DARK, lw=2.2, zorder=4)
    ax.plot([dx-0.18, dx+0.18],[dy-0.05, dy-0.05], color=DARK, lw=2.2, zorder=4)
    # panel2: spark scatter along curve
    xs = np.linspace(4.6, 7.4, 9)
    ys = peak - 0.075*(xs-x0)**2
    ax.scatter(xs, ys, s=np.linspace(45,15,9), color=ORANGE_D, zorder=4)
    # panel3: fountain droplets
    xd = np.linspace(8.6, 11.2, 8)
    yd = peak - 0.075*(xd-x0)**2
    ax.scatter(xd, yd, s=40, color=BLUE, zorder=4, marker="o")
    ax.plot([8.5,8.5],[0.25,0.9], color=BLUE, lw=3, zorder=3)  # fountain base
    fig.tight_layout()
    save(fig, "parabola_scenes")

# ---------------------------------------------------------------
# Diagram 2 - Slide 5: independence of motion (two rows)
# ---------------------------------------------------------------
def diagram_independence():
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    xs = [1.2, 3.1, 5.0, 6.9, 8.8]           # equal spacing in x
    arrow_len = 1.1                           # identical horizontal arrows
    # TOP ROW: constant velocity, straight line
    ytop = 4.7
    ax.text(0.2, 5.55, "Before the puff  —  constant velocity in x",
            fontsize=12.5, color=DARK, fontweight="bold")
    ax.plot([0.6, 10.4], [ytop, ytop], color=GREY, lw=1, ls=(0,(2,3)))
    for x in xs:
        ax.add_patch(Circle((x, ytop), 0.20, color=DARK, zorder=4))
        ax.add_patch(FancyArrowPatch((x, ytop), (x+arrow_len, ytop),
                     arrowstyle="-|>", mutation_scale=16, color=ORANGE, lw=2.6, zorder=5))
    # BOTTOM ROW: diagonal drift, x-arrows identical, small y added
    ybot0 = 2.4
    ax.text(0.2, 3.25, "After a sideways puff  —  drifts diagonally, x-speed unchanged",
            fontsize=12.5, color=DARK, fontweight="bold")
    ys = [ybot0 - 0.42*i for i in range(len(xs))]
    ax.plot([xs[0], xs[-1]], [ys[0], ys[-1]], color=GREY, lw=1, ls=(0,(2,3)))
    for x, y in zip(xs, ys):
        ax.add_patch(Circle((x, y), 0.20, color=DARK, zorder=4))
        # identical horizontal arrow (same length as top)
        ax.add_patch(FancyArrowPatch((x, y), (x+arrow_len, y),
                     arrowstyle="-|>", mutation_scale=16, color=ORANGE, lw=2.6, zorder=5))
        # small downward y-velocity arrow
        ax.add_patch(FancyArrowPatch((x, y), (x, y-0.55),
                     arrowstyle="-|>", mutation_scale=12, color=BLUE, lw=2.0, zorder=5))
    # legend note
    ax.text(9.6, 4.7, "horizontal\narrows equal", color=ORANGE_D, fontsize=10.5,
            fontweight="bold", va="center")
    ax.text(9.6, 1.15, "added y-velocity", color=BLUE, fontsize=10.5,
            fontweight="bold", va="center")
    fig.tight_layout()
    save(fig, "independence")

# ---------------------------------------------------------------
# Diagram 3 - Slide 11: launch-angle trajectory fan
# ---------------------------------------------------------------
def diagram_trajectory_fan():
    fig, ax = plt.subplots(figsize=(10, 4.6))
    g, v = 9.8, 20.0
    angles = [30, 45, 60, 75]
    colors = [GREY, ORANGE, BLUE, "#7A4FB5"]
    for ang, c in zip(angles, colors):
        th = np.radians(ang)
        T = 2*v*np.sin(th)/g
        t = np.linspace(0, T, 200)
        x = v*np.cos(th)*t
        y = v*np.sin(th)*t - 0.5*g*t**2
        lw = 3.4 if ang == 45 else 2.2
        ax.plot(x, y, color=c, lw=lw, label=f"{ang}°",
                zorder=5 if ang==45 else 3)
    ax.axhline(0, color=DARK, lw=1.5)
    ax.scatter([0],[0], color=DARK, s=40, zorder=6)
    ax.set_xlabel("horizontal distance (range)", fontsize=11, color=DARK)
    ax.set_ylabel("height", fontsize=11, color=DARK)
    ax.tick_params(colors=GREY, labelsize=9)
    for s in ["top","right"]:
        ax.spines[s].set_visible(False)
    for s in ["left","bottom"]:
        ax.spines[s].set_color(GREY)
    leg = ax.legend(title="launch angle\n(same speed)", fontsize=10,
                    title_fontsize=10, loc="upper right", frameon=False)
    ax.set_ylim(bottom=0)
    ax.annotate("45° gives\nmax range", xy=(0.80, 0.20), xycoords="axes fraction",
                color=ORANGE_D, fontsize=11, fontweight="bold", ha="center")
    fig.tight_layout()
    save(fig, "trajectory_fan")

# ---------------------------------------------------------------
# Diagram 4 - Slide 17: constant speed, changing direction
# ---------------------------------------------------------------
def diagram_circle_vectors():
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.set_aspect("equal"); ax.axis("off")
    R = 1.0
    ax.add_patch(Circle((0,0), R, fill=False, color=DARK, lw=2.5))
    ax.add_patch(Circle((0,0), 0.045, color=DARK))
    L = 0.95  # identical arrow length
    for ang in [90, 0, 270, 180]:
        th = np.radians(ang)
        px, py = R*np.cos(th), R*np.sin(th)
        # tangent (velocity) direction, counter-clockwise
        tx, ty = -np.sin(th), np.cos(th)
        ax.add_patch(FancyArrowPatch((px, py), (px+L*tx, py+L*ty),
                     arrowstyle="-|>", mutation_scale=20, color=ORANGE, lw=3, zorder=6))
        # radius dashed
        ax.plot([0, px],[0, py], color=GREY, lw=1, ls=(0,(2,3)), zorder=2)
        ax.add_patch(Circle((px,py), 0.05, color=DARK, zorder=5))
    lim = 2.15
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.text(0, -1.95, "speed (arrow length) is constant\ndirection rotates continuously",
            ha="center", color=ORANGE_D, fontsize=12, fontweight="bold")
    fig.tight_layout()
    save(fig, "circle_vectors")

# ---------------------------------------------------------------
# Diagram 5 - Slide 26: stopper-tube-washer apparatus
# ---------------------------------------------------------------
def diagram_apparatus():
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-3.2, 3.2); ax.set_ylim(-3.6, 3.2)
    # horizontal circular path (top, perspective ellipse)
    path = Ellipse((0, 2.1), 4.4, 1.2, fill=False, color=DARK, lw=2, ls=(0,(4,3)))
    ax.add_patch(path)
    # stopper on the circle
    sx, sy = 2.2, 2.1
    ax.add_patch(Circle((sx, sy), 0.20, color=ORANGE, zorder=6))
    ax.text(sx+0.15, sy+0.35, "stopper", color=ORANGE_D, fontsize=11, fontweight="bold")
    # radius arrow
    ax.add_patch(FancyArrowPatch((0, 2.1), (sx, sy), arrowstyle="-|>",
                 mutation_scale=15, color=BLUE, lw=2, zorder=5))
    ax.text(1.0, 2.35, "radius  r", color=BLUE, fontsize=11, fontweight="bold")
    # swing direction
    ax.add_patch(FancyArrowPatch((-1.9, 2.35), (-1.4, 1.75), arrowstyle="-|>",
                 mutation_scale=14, color=DARK, lw=1.8,
                 connectionstyle="arc3,rad=0.5"))
    ax.text(-2.9, 2.5, "swing", color=DARK, fontsize=10, fontstyle="italic")
    # string from stopper to top of tube
    ax.plot([sx, 0.18], [sy, 1.0], color=DARK, lw=1.6, zorder=4)
    # hollow tube (vertical)
    ax.add_patch(Rectangle((-0.18, -1.4), 0.36, 2.4, fill=True,
                 facecolor="#DDDDDD", edgecolor=DARK, lw=1.6, zorder=3))
    ax.text(0.45, -0.2, "hollow tube\n(grip here)", color=DARK, fontsize=10)
    # string continues down through tube to washers
    ax.plot([0, 0], [-1.4, -2.5], color=DARK, lw=1.6, zorder=4)
    # washers stacked
    for i in range(4):
        ax.add_patch(Rectangle((-0.42, -2.9 + i*0.16), 0.84, 0.13,
                     facecolor=ORANGE, edgecolor=ORANGE_D, lw=1, zorder=5))
    ax.text(0.6, -2.7, "washers\n(known pulling force)", color=ORANGE_D,
            fontsize=11, fontweight="bold", va="center")
    fig.tight_layout()
    save(fig, "apparatus")

diagram_parabola()
diagram_independence()
diagram_trajectory_fan()
diagram_circle_vectors()
diagram_apparatus()
print("ALL DIAGRAMS DONE")
