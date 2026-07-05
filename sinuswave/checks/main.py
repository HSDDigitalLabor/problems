import os
import shutil
import check50
import check50.py

FILE_NAME = "sinuswave.py"
OUT_FILE = "sinus.mem"
SUBMITTED_FILE = "sinus_submitted.mem"
REFERENCE_FILE = "sinus_reference.mem"


def read_file(fname):
    with open(fname, "r") as f:
        return [line.strip() for line in f.readlines()]


def remove_output_file():
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)


def copy_output_file():
    if os.path.exists(OUT_FILE):
        shutil.copyfile(OUT_FILE, SUBMITTED_FILE)


@check50.check()
def exists():
    """sinuswave.py exists"""
    check50.exists(FILE_NAME)


@check50.check()
def exists_memoryfile():
    """sinus.mem exists"""
    check50.exists(OUT_FILE)
    copy_output_file()


@check50.check(exists)
def compiles():
    """sinuswave.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """generateLUT function defined"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "generateLUT"):
        raise check50.Failure(f"Function `generateLUT` not found in {FILE_NAME}")


@check50.check(has_function)
def creates_file():
    """generateLUT creates sinus.mem"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(4, 15)

    check50.exists(OUT_FILE)


@check50.check(creates_file)
def four_points():
    """4 point LUT with max amplitude 15 is correct"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(4, 15)

    expected = [
        "8",
        "f",
        "8",
        "0",
    ]

    result = read_file(OUT_FILE)

    if result != expected:
        raise check50.Failure(f"expected {expected}, got {result}")


@check50.check(creates_file)
def eight_points():
    """8 point LUT with max amplitude 255 is correct"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(8, 255)

    expected = [
        "80",
        "da",
        "ff",
        "da",
        "80",
        "25",
        "00",
        "25",
    ]

    result = read_file(OUT_FILE)

    if result != expected:
        raise check50.Failure(f"expected {expected}, got {result}")


@check50.check(creates_file)
def correct_number_of_lines():
    """number of lines matches num_points"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(64, 1023)

    result = read_file(OUT_FILE)

    if len(result) != 64:
        raise check50.Failure(f"expected 64 lines, got {len(result)}")


@check50.check(has_function)
def invalid_num_points():
    """invalid num_points raises ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT(0, 1023)
    except ValueError:
        return

    raise check50.Failure("expected ValueError for num_points = 0")


@check50.check(has_function)
def invalid_max_amplitude():
    """invalid max_amplitude raises ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT(8, 0)
    except ValueError:
        return

    raise check50.Failure("expected ValueError for max_amplitude = 0")


@check50.check(has_function)
def invalid_types():
    """invalid argument types raise ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT("8", 255)
    except ValueError:
        return

    raise check50.Failure("expected ValueError for invalid argument types")


@check50.check(creates_file)
def file_1024_samples():
    """sinus.mem contains exactly 1024 samples"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(1024, 65535)

    result = read_file(OUT_FILE)

    if len(result) != 1024:
        raise check50.Failure(f"expected 1024 samples, got {len(result)}")


@check50.check(file_1024_samples)
def valid_hex_format():
    """all lines are valid 4-digit hex values"""
    lines = read_file(OUT_FILE)

    for i, line in enumerate(lines):
        if len(line) != 4:
            raise check50.Failure(f"line {i + 1} has wrong length: '{line}'")

        try:
            int(line, 16)
        except ValueError:
            raise check50.Failure(f"line {i + 1} is not valid hex: '{line}'")


@check50.check(valid_hex_format)
def value_range():
    """values are within 0..65535"""
    lines = read_file(OUT_FILE)

    for i, line in enumerate(lines):
        value = int(line, 16)

        if value < 0 or value > 65535:
            raise check50.Failure(f"value out of range at line {i + 1}: {value}")


@check50.check(value_range)
def midpoint_check():
    """first value should be around midpoint"""
    lines = read_file(OUT_FILE)
    first = int(lines[0], 16)

    if not (32767 <= first <= 32768):
        raise check50.Failure(f"expected midpoint around 32768, got {first}")


@check50.check(exists_memoryfile)
def reference_exists():
    """reference file sinus_reference.mem exists"""
    check50.include(f"files/{REFERENCE_FILE}")
    check50.exists(REFERENCE_FILE)


@check50.check(exists_memoryfile)
def compare_with_reference():
    """sinus_submitted.mem matches sinus_reference.mem line by line"""

    check50.include(f"files/{REFERENCE_FILE}")

    student = read_file(SUBMITTED_FILE)
    reference = read_file(REFERENCE_FILE)

    if len(student) != len(reference):
        raise check50.Failure(
            f"line count mismatch: expected {len(reference)}, got {len(student)}"
        )

    for i, (s, r) in enumerate(zip(student, reference)):
        if s != r:
            raise check50.Failure(
                f"line {i + 1} incorrect\nexpected: {r}\nfound:    {s}"
            )
