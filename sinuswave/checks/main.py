import os
import shutil
import check50
import check50.py

FILE_NAME = "sinuswave.py"
OUT_FILE = "sinus_lut.coe"
SUBMITTED_FILE = "sinus_lut_submitted.coe"
REFERENCE_FILE = "sinus_lut_ref.coe"


def read_file(fname):
    with open(fname, "r") as f:
        return [line.strip() for line in f.readlines()]


def parse_coe_values(lines):
    if len(lines) < 2:
        raise check50.Failure("COE-Datei enthält keinen gültigen Header")
    if lines[0] != "memory_initialization_radix=16;":
        raise check50.Failure("Header-Zeile 1 muss 'memory_initialization_radix=16;' sein")
    if lines[1] != "memory_initialization_vector=":
        raise check50.Failure("Header-Zeile 2 muss 'memory_initialization_vector=' sein")

    raw_values = lines[2:]
    parsed = []
    for i, line in enumerate(raw_values):
        expected_delimiter = ";" if i == len(raw_values) - 1 else ","
        if not line.endswith(expected_delimiter):
            raise check50.Failure(
                f"Zeile {i + 3} muss mit '{expected_delimiter}' enden, erhalten: '{line}'"
            )
        parsed.append(line[:-1])
    return parsed


def remove_output_file():
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)


def copy_output_file():
    if os.path.exists(OUT_FILE):
        shutil.copyfile(OUT_FILE, SUBMITTED_FILE)


@check50.check()
def exists():
    """Python-Datei existiert"""
    check50.exists(FILE_NAME)


@check50.check()
def exists_memoryfile():
    """COE-Datei existiert"""
    check50.exists(OUT_FILE)
    copy_output_file()


@check50.check(exists)
def compiles():
    """Python-Datei kompiliert fehlerfrei"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    """Funktion generateLUT ist definiert"""
    module = check50.py.import_(FILE_NAME)

    if not hasattr(module, "generateLUT"):
        raise check50.Failure(f"Funktion `generateLUT` wurde nicht in {FILE_NAME} gefunden")


@check50.check(has_function)
def creates_file():
    """generateLUT erstellt sinus_lut.coe"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(4, 15)

    check50.exists(OUT_FILE)


@check50.check(creates_file)
def four_points():
    """4-Punkte-LUT mit Amplitude 15 ist korrekt (Zweierkomplement)"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(4, 15)

    # sin(0)=0 -> 0000, sin(pi/2)=15 -> 000F, sin(pi)=0 -> 0000, sin(3pi/2)=-15 -> FFF1
    expected = ["0000", "000F", "0000", "FFF1"]

    lines = read_file(OUT_FILE)
    result = parse_coe_values(lines)

    if result != expected:
        raise check50.Failure(f"Erwartet: {expected}, erhalten: {result}")


@check50.check(creates_file)
def eight_points():
    """8-Punkte-LUT mit Amplitude 32767 ist korrekt (Zweierkomplement)"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(8, 32767)

    # 32767 * sin([0, 45, 90, 135, 180, 225, 270, 315] deg)
    # gerundet: [0, 23169, 32767, 23169, 0, -23169, -32767, -23169]
    expected = ["0000", "5A81", "7FFF", "5A81", "0000", "A57F", "8001", "A57F"]

    lines = read_file(OUT_FILE)
    result = parse_coe_values(lines)

    if result != expected:
        raise check50.Failure(f"Erwartet: {expected}, erhalten: {result}")


@check50.check(creates_file)
def correct_number_of_lines():
    """Anzahl an Datenwerten entspricht num_points"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(64, 1023)

    lines = read_file(OUT_FILE)
    result = parse_coe_values(lines)

    if len(result) != 64:
        raise check50.Failure(f"Erwartet: 64 Datenzeilen, erhalten: {len(result)}")


@check50.check(has_function)
def invalid_num_points():
    """Ungültiges num_points wirft ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT(0, 1023)
    except ValueError:
        return

    raise check50.Failure("ValueError für num_points = 0 erwartet")


@check50.check(has_function)
def invalid_max_amplitude():
    """Ungültige max_amplitude wirft ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT(8, 0)
    except ValueError:
        return

    raise check50.Failure("ValueError für max_amplitude = 0 erwartet")


@check50.check(has_function)
def invalid_types():
    """Ungültige Parametertypen werfen ValueError"""
    module = check50.py.import_(FILE_NAME)

    try:
        module.generateLUT("8", 255)
    except ValueError:
        return

    raise check50.Failure("ValueError für ungültige Argumenttypen erwartet")


@check50.check(creates_file)
def file_1024_samples():
    """COE-Datei enthält genau 1024 Samples"""
    module = check50.py.import_(FILE_NAME)

    remove_output_file()
    module.generateLUT(1024, 32767)

    lines = read_file(OUT_FILE)
    result = parse_coe_values(lines)

    if len(result) != 1024:
        raise check50.Failure(f"Erwartet: 1024 Samples, erhalten: {len(result)}")


@check50.check(file_1024_samples)
def valid_hex_format():
    """Alle Werte sind gültige 4-stellige Hex-Werte"""
    lines = read_file(OUT_FILE)
    values = parse_coe_values(lines)

    for i, val in enumerate(values):
        if len(val) != 4:
            raise check50.Failure(f"Wert in Zeile {i + 3} hat falsche Länge: '{val}'")

        try:
            int(val, 16)
        except ValueError:
            raise check50.Failure(f"Wert in Zeile {i + 3} ist kein gültiges Hex: '{val}'")


@check50.check(valid_hex_format)
def start_value_check():
    """Erster Wert sollte bei sin(0) = 0 liegen"""
    lines = read_file(OUT_FILE)
    values = parse_coe_values(lines)
    first = int(values[0], 16)

    if first != 0:
        raise check50.Failure(f"Erwarteter Startwert '0000', erhalten: '{values[0]}'")


@check50.check(exists_memoryfile)
def reference_exists():
    """Referenzdatei sinus_lut_ref.coe existiert"""
    check50.include(f"files/{REFERENCE_FILE}")
    check50.exists(REFERENCE_FILE)


@check50.check(exists_memoryfile)
def compare_with_reference():
    """Eingereichte Datei stimmt mit sinus_lut_ref.coe überein"""
    check50.include(f"files/{REFERENCE_FILE}")

    student = read_file(SUBMITTED_FILE)
    reference = read_file(REFERENCE_FILE)

    if len(student) != len(reference):
        raise check50.Failure(
            f"Zeilenanzahl stimmt nicht überein: erwartet {len(reference)}, erhalten {len(student)}"
        )

    for i, (s, r) in enumerate(zip(student, reference)):
        if s != r:
            raise check50.Failure(
                f"Zeile {i + 1} stimmt nicht überein:\nErwartet: {r}\nErhalten: {s}"
            )