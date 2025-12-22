import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

def draw_stack_colored(items, title="Stack - (Last In, First Out)"):
    # smaller figure + smaller cells
    w, h = 2.1, 0.6
    x0, y0 = 0.9, 0.6

    fig, ax = plt.subplots(figsize=(4.0, 2.5))

    # pastel-ish colors cycling
    colors = ["#CFE8FF", "#DFF7D9", "#FFF2CC", "#F8D7DA", "#E7D7FF", "#D1F2EB"]

    # Draw stack cells (bottom to top)
    for i, item in enumerate(items):
        y = y0 + i * h
        face = colors[i % len(colors)]
        rect = Rectangle((x0, y), w, h, linewidth=1.8, edgecolor="black", facecolor=face)
        ax.add_patch(rect)
        ax.text(x0 + w/2, y + h/2, str(item), ha="center", va="center", fontsize=12, weight="bold")

    # Frame around stack
    frame = Rectangle((x0, y0), w, max(len(items), 1)*h, fill=False, linewidth=1.8)
    ax.add_patch(frame)

    # Top pointer
    top_y = y0 + (len(items)-1)*h + h/2 if items else y0 + h/2
    arrow = FancyArrowPatch((x0 + w + 0.9, top_y), (x0 + w + 0.03, top_y),
                            arrowstyle='-|>', mutation_scale=14, linewidth=1.8, color="black")
    ax.add_patch(arrow)
    ax.text(x0 + w + 0.95, top_y, "top", ha="left", va="center", fontsize=10)

    # Optional push/pop mini labels
    ax.text(
        x0 + w + 0.85,
        top_y + 0.35,
        r"$\uparrow$ Push()",
        ha="center",
        va="center",
        fontsize=9,
    )
    ax.text(
        x0 + w + 0.85,
        top_y - 0.35,
        r"$\downarrow$ Pop()",
        ha="center",
        va="center",
        fontsize=9,
    )


    # Styling
    ax.set_xlim(0, x0 + w + 1.6)
    ax.set_ylim(0, y0 + max(len(items), 1)*h + 0.9)
    ax.axis("off")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(os.path.join(script_dir, "stack_graphic.png"), dpi=200, bbox_inches="tight")


draw_stack_colored(["14", "67", "43", "8"])
