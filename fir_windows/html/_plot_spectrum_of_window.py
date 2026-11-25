from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


def main():
    length = 13
    omega = np.linspace(0, np.pi, 6000)
    spectrum = np.ones_like(omega)
    spectrum[1:] = np.abs(
        np.sin(length * omega[1:] / 2) / (length * np.sin(omega[1:] / 2))
    )

    first_zero = 2 * np.pi / length
    peaks, _ = find_peaks(spectrum)
    side_peak = peaks[omega[peaks] > first_zero][0]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(omega, spectrum, color="red", linewidth=3)
    ax.set_xlim(-0.12, np.pi * 1.10)
    ax.set_ylim(-0.18, 1.19)
    ax.axis("off")

    arrow_style = dict(arrowstyle="-|>", lw=2, color="black", mutation_scale=20)
    ax.annotate("", (np.pi * 1.07, 0), (0, 0), arrowprops=arrow_style)
    ax.annotate("", (0, 1.16), (0, -0.025), arrowprops=arrow_style)

    ax.text(-0.055, 1.105, r"$|W[k]|$", fontsize=20, rotation=90, ha="right", va="top")
    ax.text(np.pi * 1.075, -0.055, r"$\Omega$", fontsize=21, ha="left", va="top")
    ax.text(-0.035, -0.04, "0", fontsize=15, ha="right", va="top")
    ax.text(-0.035, 1, "1", fontsize=15, ha="right", va="center")
    ax.text(np.pi, -0.042, r"$\pi$", fontsize=17, ha="center", va="top")

    ax.annotate(
        "Hauptmaximum",
        xy=(0, 1),
        xytext=(0.66, 1.08),
        fontsize=17,
        ha="left",
        va="center",
        arrowprops=dict(
            arrowstyle="->", color="black", lw=1.5, connectionstyle="arc3,rad=0.15"
        ),
    )
    ax.annotate(
        "Seitenmaximum",
        xy=(omega[side_peak], spectrum[side_peak]),
        xytext=(1.40, 0.53),
        fontsize=17,
        ha="left",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
    )

    ax.plot([first_zero, first_zero], [-0.02, 0.04], color="black", lw=1)
    ax.text(first_zero, -0.055, "erste Nullstelle", ha="center", va="top", fontsize=13)
    ax.annotate(
        "",
        xy=(first_zero, -0.122),
        xytext=(0, -0.122),
        arrowprops=dict(arrowstyle="<->", lw=1.35, color="black"),
    )
    ax.text(
        first_zero / 2,
        -0.149,
        "Bereich des\nHauptmaximums",
        fontsize=12,
        ha="center",
        va="top",
    )

    fig.subplots_adjust(left=0.11, right=0.93, bottom=0.23, top=0.91)
    output = Path(__file__).resolve().parent / "spectrum_of_window.png"
    fig.savefig(output, dpi=250, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Gespeichert: {output}")


if __name__ == "__main__":
    main()
