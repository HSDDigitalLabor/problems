import check50
import check50.py
import tokenize
from pathlib import Path

FILE_NAME = "stufen.py"


def matrices_almost_equal(actual, expected, eps=1e-6):
    """Vergleicht zwei Matrizen mit Toleranz eps."""
    if len(actual) != len(expected):
        raise check50.Mismatch(str(expected), str(actual))

    for row_a, row_e in zip(actual, expected):
        if len(row_a) != len(row_e):
            raise check50.Mismatch(str(expected), str(actual))
        for a, e in zip(row_a, row_e):
            if abs(a - e) > eps:
                raise check50.Mismatch(str(expected), str(actual))


@check50.check()
def exists():
    """stufen.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """stufen.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_functions():
    """rowMult, rowAdd und zeilenStufen functions defined"""
    module = check50.py.import_(FILE_NAME)

    missing = []
    if not hasattr(module, "rowMult"):
        missing.append("rowMult")
    if not hasattr(module, "rowAdd"):
        missing.append("rowAdd")
    if not hasattr(module, "zeilenStufen"):
        missing.append("zeilenStufen")

    if missing:
        msg = f"Function(s) {', '.join(f'`{m}`' for m in missing)} not found in {FILE_NAME}"
        raise check50.Failure(msg)


# ---------- Tests für rowMult ----------


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


# ---------- Tests für rowAdd ----------


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


# ---------- Tests für zeilenStufen (nur Vorwärtsschritt) ----------


@check50.check(has_functions)
def test_zeilenStufen_3x4():
    """zeilenStufen: 3x4-Beispielmatrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [2, 4, -2, 2],
        [4, 9, -3, 8],
        [-2, -7, 1, -9],
    ]

    module.zeilenStufen(M)

    # Erwartete Zeilenstufenform bei reinem Vorwärtsschritt + Pivot-Skalierung
    expected = [
        [1.0, 2.0, -1.0, 1.0],
        [0.0, 1.0, 1.0, 4.0],
        [0.0, 0.0, 1.0, 2.5],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_zeilenStufen_4x5():
    """zeilenStufen: 4x5-Beispielmatrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)

    M = [
        [2, 4, 2, 0, 6],
        [1, 3, 1, 2, 5],
        [0, 1, 0, 1, 1],
        [3, 10, 3, 5, 12],
    ]

    module.zeilenStufen(M)

    expected = [
        [1.0, 2.0, 1.0, 0.0, 3.0],
        [0.0, 1.0, 0.0, 2.0, 2.0],
        [0.0, 0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
    ]

    matrices_almost_equal(M, expected)


# ---------- Stil-Check ----------


@check50.check(has_functions)
def no_forbidden_methods():
    """does not use forbidden built-ins"""
    forbidden = {"index", "sort", "enumerate", "find", "count", "map", "filter"}

    with Path(FILE_NAME).open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden:
                msg = f"Found forbidden function '{tok_string}'"
                raise check50.Failure(msg)
