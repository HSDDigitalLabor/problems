import os
import subprocess
import sys
from pathlib import Path

import check50
import check50.py

FILE_NAME = "fir_design.py"
CSV_FILE = "kaiser_koeffizienten.csv"
MASK_PLOT = "0-Frequenzmaske.png"
RECTANGULAR_PLOT = "1-Rechteck-Fenster.png"
KAISER_PLOT = "2-Kaiser-Fenster.png"
COMPARISON_PLOT = "3-Fenstervergleich.png"
OUTPUT_FILES = (
    MASK_PLOT,
    RECTANGULAR_PLOT,
    KAISER_PLOT,
    COMPARISON_PLOT,
    CSV_FILE,
)


def _require_output(filename: str) -> None:
    if not Path(filename).is_file():
        raise check50.Failure(f"{filename} was not created")


@check50.check()
def exists():
    """fir_design.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """fir_design.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def runs():
    """fir_design.py runs successfully"""
    for filename in OUTPUT_FILES:
        Path(filename).unlink(missing_ok=True)
    try:
        result = subprocess.run(
            [sys.executable, FILE_NAME],
            env={**os.environ, "MPLBACKEND": "Agg"},
            capture_output=True,
            text=True,
            errors="replace",
            timeout=45,
        )
    except subprocess.TimeoutExpired as exc:
        raise check50.Failure(
            f"{FILE_NAME} timed out after {exc.timeout} seconds"
        ) from exc
    if result.returncode:
        raise check50.Failure(
            f"{FILE_NAME} exited with status {result.returncode}",
            help=result.stderr.strip() or None,
        )


@check50.check(runs)
def creates_mask_plot():
    """creates 0-Frequenzmaske.png"""
    _require_output(MASK_PLOT)


@check50.check(runs)
def creates_rectangular_plot():
    """creates 1-Rechteck-Fenster.png"""
    _require_output(RECTANGULAR_PLOT)


@check50.check(runs)
def creates_kaiser_plot():
    """creates 2-Kaiser-Fenster.png"""
    _require_output(KAISER_PLOT)


@check50.check(runs)
def creates_comparison_plot():
    """creates 3-Fenstervergleich.png"""
    _require_output(COMPARISON_PLOT)


@check50.check(runs)
def creates_csv():
    """creates kaiser_koeffizienten.csv"""
    _require_output(CSV_FILE)
