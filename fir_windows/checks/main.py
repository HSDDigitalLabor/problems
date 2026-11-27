from pathlib import Path

import check50
import check50.py
import matplotlib
import numpy as np
from scipy import signal

matplotlib.use("Agg")
import matplotlib.pyplot as plt


FILE_NAME = "fir_windows.py"
TIME_PLOT_NAME = "plot_windows_time.png"
FREQ_PLOT_NAME = "plot_windows_freq.png"

N = 256
M = N // 2
N_FFT = 8192

WINDOW_FUNCTIONS = {
    "Rectangular": signal.windows.boxcar,
    "Hann": signal.windows.hann,
    "Hamming": signal.windows.hamming,
    "Kaiser (8.6)": lambda length: signal.windows.kaiser(length, beta=8.6),
}


def expected_window(name):
    values = WINDOW_FUNCTIONS[name](M)
    result = np.zeros(N)
    start = (N - M) // 2
    result[start : start + M] = values
    return result


def expected_spectrum(name):
    values = WINDOW_FUNCTIONS[name](M)
    spectrum = np.fft.fftshift(np.fft.fft(values, n=N_FFT))
    magnitude = np.abs(spectrum)
    magnitude /= np.max(magnitude)
    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-12))
    frequencies = np.fft.fftshift(np.fft.fftfreq(N_FFT))
    return frequencies, magnitude_db


def run_submission():
    plt.close("all")
    for filename in (TIME_PLOT_NAME, FREQ_PLOT_NAME):
        output = Path(filename)
        if output.exists():
            output.unlink()

    try:
        check50.py.import_(FILE_NAME)
    except Exception as exc:
        msg = f"Error executing {FILE_NAME}"
        explanation = f"{type(exc).__name__}: {exc}"
        raise check50.Failure(msg, help=explanation) from exc

    return [
        axis
        for figure_number in plt.get_fignums()
        for axis in plt.figure(figure_number).axes
    ]


def get_plot_axis(index):
    axes = run_submission()
    if len(axes) <= index:
        expected = "two plots: time domain and frequency domain"
        actual = f"{len(axes)} plot axes"
        raise check50.Mismatch(expected, actual)
    return axes[index]


def get_curves(axis, expected_length):
    lines = axis.get_lines()
    if len(lines) != len(WINDOW_FUNCTIONS):
        expected = f"{len(WINDOW_FUNCTIONS)} plotted curves"
        actual = f"{len(lines)} plotted curves"
        raise check50.Mismatch(expected, actual)

    result = {}
    for line in lines:
        name = line.get_label()
        if name in result:
            raise check50.Failure(f"Duplicate curve label: {name}")
        x = np.asarray(line.get_xdata(), dtype=float)
        y = np.asarray(line.get_ydata(), dtype=float)
        if len(x) != expected_length or len(y) != expected_length:
            expected = f"{expected_length} samples for {name}"
            actual = f"x: {len(x)}, y: {len(y)}"
            raise check50.Mismatch(expected, actual)
        result[name] = (x, y)

    expected_names = set(WINDOW_FUNCTIONS)
    if set(result) != expected_names:
        raise check50.Mismatch(str(sorted(expected_names)), str(sorted(result)))
    return result


def check_time_window(name):
    axis = get_plot_axis(0)
    curves = get_curves(axis, N)
    actual_x, actual_y = curves[name]

    if not np.allclose(actual_x, np.arange(N), rtol=0, atol=1e-10):
        raise check50.Failure(f"{name}: Incorrect coefficient indices.")

    expected_y = expected_window(name)
    if not np.allclose(actual_y, expected_y, rtol=1e-7, atol=1e-10):
        difference = np.max(np.abs(actual_y - expected_y))
        msg = f"{name}: Time-domain window is incorrect."
        explanation = f"Maximum absolute difference: {difference:.6g}"
        raise check50.Failure(msg, help=explanation)


def check_frequency_response(name):
    axis = get_plot_axis(1)
    curves = get_curves(axis, N_FFT)
    actual_x, actual_y = curves[name]
    expected_x, expected_y = expected_spectrum(name)

    if not np.all(np.isfinite(actual_y)):
        raise check50.Failure(f"{name}: Frequency response contains NaN or infinity.")

    if not np.allclose(actual_x, expected_x, rtol=0, atol=1e-12):
        raise check50.Failure(f"{name}: Frequency axis is incorrect.")

    if not np.allclose(actual_y, expected_y, rtol=1e-6, atol=1e-4):
        difference = np.max(np.abs(actual_y - expected_y))
        msg = f"{name}: Frequency response is incorrect."
        explanation = f"Maximum absolute difference: {difference:.6g} dB"
        raise check50.Failure(msg, help=explanation)


def check_grid(axis):
    gridlines = axis.get_xgridlines() + axis.get_ygridlines()
    if not any(line.get_visible() for line in gridlines):
        raise check50.Failure("Plot is missing a visible grid.")


def check_legend(axis):
    legend = axis.get_legend()
    if legend is None:
        raise check50.Failure("Plot is missing a legend.")

    labels = {text.get_text() for text in legend.get_texts()}
    if labels != set(WINDOW_FUNCTIONS):
        raise check50.Mismatch(str(sorted(WINDOW_FUNCTIONS)), str(sorted(labels)))


@check50.check()
def exists():
    """fir_windows.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """fir_windows.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def test_time_windows():
    """plots four centered time-domain windows"""
    axis = get_plot_axis(0)
    get_curves(axis, N)
    check_grid(axis)
    check_legend(axis)


@check50.check(compiles)
def test_frequency_responses():
    """plots four frequency responses"""
    axis = get_plot_axis(1)
    get_curves(axis, N_FFT)
    check_grid(axis)
    check_legend(axis)


@check50.check(test_time_windows)
def test_rectangular():
    """Rectangular window and spectrum are correct"""
    check_time_window("Rectangular")
    check_frequency_response("Rectangular")


@check50.check(test_time_windows)
def test_hann():
    """Hann window and spectrum are correct"""
    check_time_window("Hann")
    check_frequency_response("Hann")


@check50.check(test_time_windows)
def test_hamming():
    """Hamming window and spectrum are correct"""
    check_time_window("Hamming")
    check_frequency_response("Hamming")


@check50.check(test_time_windows)
def test_kaiser():
    """Kaiser window and spectrum are correct"""
    check_time_window("Kaiser (8.6)")
    check_frequency_response("Kaiser (8.6)")


@check50.check(compiles)
def test_plot_labels():
    """time and frequency plots have correct axis labels"""
    time_axis = get_plot_axis(0)
    freq_axis = get_plot_axis(1)

    if time_axis.get_xlabel() != "n" or time_axis.get_ylabel() != "w[n]":
        raise check50.Failure("Time-domain axis labels are incorrect.")

    if (
        freq_axis.get_xlabel() != "Normierte Frequenz f / f_s"
        or freq_axis.get_ylabel() != "Betrag (dB)"
    ):
        raise check50.Failure("Frequency-domain axis labels are incorrect.")


@check50.check(compiles)
def test_frequency_limits():
    """frequency plot uses the specified axis limits"""
    axis = get_plot_axis(1)
    if not np.allclose(axis.get_xlim(), (0, 0.2), rtol=0, atol=1e-12):
        raise check50.Failure("Frequency plot x limits should be 0 to 0.2.")
    if not np.allclose(axis.get_ylim(), (-100, 5), rtol=0, atol=1e-12):
        raise check50.Failure("Frequency plot y limits should be -100 to 5.")


@check50.check(compiles)
def test_plot_files():
    """saves both time- and frequency-domain plots"""
    run_submission()
    for filename in (TIME_PLOT_NAME, FREQ_PLOT_NAME):
        check50.exists(filename)
        if Path(filename).stat().st_size == 0:
            raise check50.Failure(f"{filename} is empty.")
