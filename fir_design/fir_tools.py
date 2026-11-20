import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def plot_frequenzgang(f_hz, kurven, maske, dateiname="frequenzgang.png", *,
                      ax=None, linear=False):
    """Zeichnet Betragsgaenge mit Frequenzmaske und faerbt Verletzungen rot.

    Werte in dB oder bei linear=True als Betrag. Nur ohne uebergebene Achse
    wird eine eigene PNG-Datei mit Durchlassband-Zoom gespeichert.
    """
    grenzen = np.array([maske["pass_min_db"], maske["pass_max_db"], maske["stop_max_db"]])
    if linear:
        grenzen = 10 ** (grenzen / 20)
    pass_min, pass_max, stop_max = grenzen

    eigenes_bild = ax is None
    if eigenes_bild:
        fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    zoom = ax.inset_axes([0.43, 0.59, 0.24, 0.29]) if eigenes_bild and not linear else None
    achsen = [ax] if zoom is None else [ax, zoom]

    f_hz = np.asarray(f_hz)
    durchlass = f_hz <= maske["f_pass"]
    sperre = f_hz >= maske["f_stop"]
    label = "Maskenverletzungen"
    for name, pegel in kurven.items():
        pegel = np.asarray(pegel)
        linie, = ax.plot(f_hz, pegel, label=name)
        if zoom is not None:
            zoom.plot(f_hz[durchlass], pegel[durchlass], color=linie.get_color())
        for band, verletzt, grenze in (
            (durchlass, pegel > pass_max, pass_max),
            (durchlass, pegel < pass_min, pass_min),
            (sperre, pegel > stop_max, stop_max),
        ):
            if not verletzt[band].any():
                continue
            for ziel in achsen if band is durchlass else [ax]:
                ziel.fill_between(f_hz[band], pegel[band], grenze, where=verletzt[band],
                                  interpolate=True, color="tab:red", alpha=0.25,
                                  label=label if ziel is ax else None)
            label = "_nolegend_"

    einheit = "" if linear else " dB"
    baender = (
        (0, maske["f_pass"], f"Durchlassband\n{pass_min:g} bis {pass_max:g}{einheit}", "tab:green"),
        (maske["f_pass"], maske["f_stop"], "Übergangsband\nkeine Vorgabe", "tab:gray"),
        (maske["f_stop"], maske["f_max"], f"Sperrband\nhöchstens {stop_max:g}{einheit}", "tab:blue"),
    )
    for start, ende, text, farbe in baender:
        ax.axvspan(start, ende, color=farbe, alpha=0.1, zorder=0)
        if not kurven:
            ax.text((start + ende) / 2, 0.42, text, transform=ax.get_xaxis_transform(),
                    ha="center", va="center")
    for ziel in achsen:
        ziel.hlines([pass_min, pass_max], 0, maske["f_pass"], colors="tab:red",
                    linestyles="--", label="Frequenzmaske" if ziel is ax else None)
    ax.hlines(stop_max, maske["f_stop"], maske["f_max"], colors="tab:red", linestyles="--")

    if not kurven:
        ax.set_title("Toleranzbandschema")
        ax.set_xticks([0, maske["f_pass"], maske["f_stop"], maske["f_max"]])
    if zoom is not None:
        sichtbar = [pass_min, pass_max] + [np.asarray(p)[durchlass] for p in kurven.values()]
        rand = (pass_max - pass_min) / 2
        zoom.axhspan(pass_min, pass_max, color="tab:green", alpha=0.15)
        zoom.set(title="Durchlassband (Detail)", xlim=(0, maske["f_pass"]),
                 ylim=(np.min(np.hstack(sichtbar)) - rand, np.max(np.hstack(sichtbar)) + rand),
                 xticks=[0, maske["f_pass"]], yticks=[pass_min, pass_max])
        zoom.set_ylabel("dB", labelpad=1)

    ax.set(xlim=(0, maske["f_max"]), xlabel="Frequenz (Hz)",
           ylabel="|H(f)|" if linear else "Betrag (dB)")
    if not linear:
        ax.set_ylim(bottom=-70)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right" if zoom is not None or not kurven else "best")
    if eigenes_bild:
        fig.savefig(dateiname, dpi=150)
        plt.close(fig)


def plot_vergleich(n, f_hz, h_rechteck, H_rechteck, h_kaiser, H_kaiser, beta, maske):
    """Speichert Impulsantworten und lineare Betraege als 2x2-Diagramm."""
    entwuerfe = (
        ("Rechteck", h_rechteck, H_rechteck, signal.windows.boxcar(len(n))),
        (f"Kaiser (β = {beta:g})", h_kaiser, H_kaiser, signal.windows.kaiser(len(n), beta)),
    )
    fig, achsen = plt.subplots(2, 2, sharex="row", sharey="row", figsize=(11, 7),
                               layout="constrained")
    for spalte, (name, h, H, fenster) in enumerate(entwuerfe):
        ax = achsen[0, spalte]
        ax.stem(n, h, label="Impulsantwort")
        ax.plot(n, fenster / fenster.max() * h.max(), "--", label="Fensterform")
        ax.set(title=name, xlabel="Index n", ylabel="h[n]")
        ax.grid(True, alpha=0.3)
        ax.legend()
        plot_frequenzgang(f_hz, {name: np.abs(H)}, maske, ax=achsen[1, spalte], linear=True)
    fig.savefig("3-Fenstervergleich.png", dpi=150)
    plt.close(fig)
