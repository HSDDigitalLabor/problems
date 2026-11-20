import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

N = 256
M = N // 2
N_FFT = 8192

# TODO 1: Erzeugen Sie die vier Fensterfunktionen (M Koeffizienten).
# Verwenden Sie die methoden aus scipy.signal.windows. ...
# für das Kaiser-Fenster β = 8.6
windows = {
    "Rectangular": None,  # replace None with your Code
    "Hann": None,
    "Hamming": None,
    "Kaiser (8.6)": None,
}

# ========== ZEITBEREICH ==========
fig_time, ax_time = plt.subplots(figsize=(10, 5))

for name, window in windows.items():

    # Erzeuget einen Numpy-Vektor, Nullvektor mit der Gesamtlänge N.
    w = np.zeros(N)

    # TODO 2: Berechnen Sie den Startindex
    # und kopieren Sie das Fenster "window"
    # an die entsprechende Position in den Nullvektor "w".

    # Zeichnet das zentrierte Fenster mit Legende.
    ax_time.plot(w, label=name)


# TODO 4: Beschriften Sie die Achsen (x-Achse: "n", y-Achse: "w[n]").

# TODO 5: Aktivieren Sie Raster und Legende.

# Speichert den plot unter "plot_windows_time.png".
plt.savefig("plot_windows_time.png")

# ========== FREQUENZBEREICH ==========
fig_freq, ax_freq = plt.subplots(figsize=(10, 5))

for name, window in windows.items():

    # TODO 7: Berechnen Sie die FFT des Fenster "window" mit N_FFT Punkten.
    W = None  # replace None with your Code

    # Verschiebt Sie die Nullfrequenz in die Mitte mit fftshift.
    W = np.fft.fftshift(W)

    # TODO 8: Bilden Sie den Betrag, normieren Sie und konvertieren Sie zu dB.
    # Verhindern Sie log10(0) mit Clipping auf 1e-12 (use: np.clip(W, 1e-12, None)).

    # Berechnen die Frequenzachse (normierte Frequenz f/f_s).
    f = np.fft.fftshift(np.fft.fftfreq(N_FFT))

    # Zeichnet den Frequenzgang des Fensters mit Legende.
    ax_freq.plot(f, W, label=name)

# TODO 9: Achsenbeschriftungen (x: "Normierte Frequenz f / f_s", y: "Betrag (dB)").

# TODO 10: Setzen Sie xlim(0.0, 0.2) und ylim(-100, 5).

# TODO 11: Aktivieren Sie Raster und Legende.

# Speichert den plot unter "plot_windows_freq.png".
plt.savefig("plot_windows_freq.png")
