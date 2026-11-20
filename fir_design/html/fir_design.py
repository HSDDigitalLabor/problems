import csv

import numpy as np
from scipy import signal

from fir_tools import plot_frequenzgang, plot_vergleich

f_s = 8000
f_c = 1200
numtaps = 81

# TODO 1: Definieren Sie hier die Filter-Maske.
maske = {
    "f_pass": None,  # replace None with the Specs
    "f_stop": None,
    "f_max": None,
    "pass_min_db": None,
    "pass_max_db": None,
    "stop_max_db": None,
}


n = np.arange(numtaps) - numtaps // 2
f = np.linspace(0, maske["f_max"], 16001)

plot_frequenzgang(f, {}, maske, dateiname="0-Frequenzmaske.png")

# Teil Rechteckfenster
# TODO 2: Entwerfen Sie den Rechteck-Tiefpass mit signal.firwin.
h_rechteck = None  # replace None with the signal.firwin call
_, H_rechteck = signal.freqz(h_rechteck, worN=f, fs=f_s)
rechteck_db = 20 * np.log10(np.maximum(np.abs(H_rechteck), 1e-12))

plot_frequenzgang(f, {"Rechteck-Fenster": rechteck_db}, maske, dateiname="1-Rechteck-Fenster.png")

# Teil zulaessiges beta mit der staerksten Sperrbanddaempfung suchen
beta = 0.0  # TODO: Erhoehen Sie beta in 0,1-Schritten bis zur ersten gueltigen Maske.
# TODO 3: Entwerfen Sie den Kaiser-Tiefpass mit signal.firwin.
h_kaiser = None  # replace None with the signal.firwin call
_, H_kaiser = signal.freqz(h_kaiser, worN=f, fs=f_s)
kaiser_db = 20 * np.log10(np.maximum(np.abs(H_kaiser), 1e-12))

plot_frequenzgang(f, {f"Kaiser (β = {beta:g})": kaiser_db},
                  maske, dateiname="2-Kaiser-Fenster.png")

plot_vergleich(n, f, h_rechteck, H_rechteck, h_kaiser, H_kaiser, beta, maske)

# Teil Ausgabe der Filterkoeffizienten
# TODO 4: Speichern Sie n und h_kaiser mit csv.writer in einer CSV-Datei.
