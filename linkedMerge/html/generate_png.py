import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np
import os


def draw_node(ax, x, y, text, facecolor=None, radius=0.35):
    c = Circle(
        (x, y),
        radius=radius,
        linewidth=2,
        edgecolor="black",
        facecolor=facecolor if facecolor is not None else "white",
    )
    ax.add_patch(c)
    ax.text(x, y, str(text), ha="center", va="center", fontsize=14, weight="bold")
    return c


def draw_arrow(ax, x1, y1, x2, y2, radius=0.35):
    # Shorten arrow so it touches the circle boundaries
    v = np.array([x2 - x1, y2 - y1], dtype=float)
    d = np.linalg.norm(v)
    if d == 0:
        return
    u = v / d
    start = np.array([x1, y1]) + u * radius
    end = np.array([x2, y2]) - u * radius
    arrow = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=15, linewidth=2, color="black"
    )
    ax.add_patch(arrow)


# Colors (chosen to match the example)
RED = "#e53935"
PURPLE = "#7e57c2"

fig, ax = plt.subplots(figsize=(10, 4))

# --- Top list: 1 -> 2 -> 4 (red) ---
top_y = 2.3
top_xs = [1.5, 3.5, 5.5]
top_vals = [1, 2, 4]
for x, v in zip(top_xs, top_vals):
    draw_node(ax, x, top_y, v, facecolor=RED)
for x1, x2 in zip(top_xs[:-1], top_xs[1:]):
    draw_arrow(ax, x1, top_y, x2, top_y)

# --- Middle list: 1 -> 3 -> 4 (purple) ---
mid_y = 1.2
mid_xs = [1.5, 3.5, 5.5]
mid_vals = [1, 3, 4]
for x, v in zip(mid_xs, mid_vals):
    draw_node(ax, x, mid_y, v, facecolor=PURPLE)
for x1, x2 in zip(mid_xs[:-1], mid_xs[1:]):
    draw_arrow(ax, x1, mid_y, x2, mid_y)

# Separator line
ax.plot([0.5, 6.5], [0.55, 0.55], linewidth=2, color="black")

# --- Bottom merged list: 1(p) -> 1(r) -> 2(r) -> 3(p) -> 4(r) -> 4(p) ---
bot_y = -0.2
bot_xs = [0.8, 1.9, 3.0, 4.1, 5.2, 6.3]
bot_vals = [1, 1, 2, 3, 4, 4]
bot_colors = [PURPLE, RED, RED, PURPLE, RED, PURPLE]
for x, v, col in zip(bot_xs, bot_vals, bot_colors):
    draw_node(ax, x, bot_y, v, facecolor=col)
for x1, x2 in zip(bot_xs[:-1], bot_xs[1:]):
    draw_arrow(ax, x1, bot_y, x2, bot_y)

# Layout
ax.set_aspect("equal")
ax.set_xlim(0, 7.1)
ax.set_ylim(-1.0, 3.0)
ax.axis("off")

script_dir = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(script_dir, "linked_list_graphic.png"), dpi=200, bbox_inches="tight")
