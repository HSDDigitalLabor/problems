import check50
import check50.py
import tokenize
from pathlib import Path

FILE_NAME = "zeilen.py"


@check50.check()
def exists():
    """file exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """zeilen.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_functions():
    """rowMult and rowAdd functions defined"""
    module = check50.py.import_(FILE_NAME)

    missing = []
    if not hasattr(module, "rowMult"):
        missing.append("rowMult")
    if not hasattr(module, "rowAdd"):
        missing.append("rowAdd")

    if missing:
        msg = f"Function(s) {', '.join(f'`{m}`' for m in missing)} not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_functions)
def test_rowMult_example_1():
    """rowMult: multiply 2nd row by 8 (example-style test)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    module.rowMult(M, 1, 8)

    expected = [
        [1, 2, 3, 4],
        [40, 48, 56, 64],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    if M != expected:
        raise check50.Mismatch(str(expected), str(M))


@check50.check(has_functions)
def test_rowMult_k_zero_no_change():
    """rowMult: k = 0 does not change the matrix"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    original = [row[:] for row in M]

    module.rowMult(M, 2, 0)

    expected = original  # soll unverändert bleiben

    if M != expected:
        raise check50.Mismatch(str(expected), str(M))


@check50.check(has_functions)
def test_rowAdd_example():
    """rowAdd: add -3 times row 0 to row 2 (example from problem)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    module.rowAdd(M, 0, 2, -3)

    expected = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [6, 4, 2, 0],
        [13, 14, 15, 16],
    ]

    if M != expected:
        raise check50.Mismatch(str(expected), str(M))


@check50.check(has_functions)
def test_rowAdd_k_zero_no_change():
    """rowAdd with k = 0 does not change the matrix"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [2, 4, 6],
        [1, 3, 5],
        [0, 0, 1],
    ]

    original = [row[:] for row in M]

    module.rowAdd(M, 0, 2, 0)

    if M != original:
        raise check50.Mismatch(str(original), str(M))


@check50.check(has_functions)
def test_rowMult_only_target_row_changes():
    """rowMult changes only the target row (k != 0)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    module.rowMult(M, 1, -2)

    expected = [
        [1, 2, 3],
        [-8, -10, -12],
        [7, 8, 9],
    ]

    if M != expected:
        raise check50.Mismatch(str(expected), str(M))


@check50.check(has_functions)
def test_rowAdd_only_target_row_changes():
    """rowAdd changes only the destination row (for k != 0)"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 0, 0],
        [0, 1, 0],
        [2, 3, 4],
    ]

    module.rowAdd(M, 0, 2, 5)  # Zeile 2 := Zeile 2 + 5 * Zeile 0

    expected = [
        [1, 0, 0],
        [0, 1, 0],
        [7, 3, 4],
    ]

    if M != expected:
        raise check50.Mismatch(str(expected), str(M))


@check50.check(has_functions)
def test_invalid_indices_safe():
    """functions handle invalid row indices without crashing"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [1, 2],
        [3, 4],
    ]
    original = [row[:] for row in M]

    # Ungültiger Index sollte Matrix nicht verändern (oder zumindest nicht crashen)
    module.rowMult(M, 5, 3)
    module.rowAdd(M, -1, 1, 2)
    module.rowAdd(M, 0, 10, 2)

    if M != original:
        raise check50.Mismatch(str(original), str(M))
