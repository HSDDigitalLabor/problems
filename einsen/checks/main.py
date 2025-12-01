import check50
import check50.py
import tokenize
from pathlib import Path

FILE_NAME = "einsen.py"


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


def a(a, b, c, d):
    if not (0 <= b < len(a)) or not (0 <= c < len(a)) or d == 0:
        return
    a[c] = [x + d * y for x, y in zip(a[c], a[b])]


def m(a, b, c):
    if not (0 <= b < len(a)) or c == 0:
        return
    a[b] = [x * c if x != 0 else x for x in a[b]]


@check50.check()
def exists():
    """einsen.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """einsen.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_functions():
    """rowMult, rowAdd und reduzierteStufen functions defined"""
    module = check50.py.import_(FILE_NAME)

    missing = []
    if not hasattr(module, "rowMult"):
        missing.append("rowMult")
    if not hasattr(module, "rowAdd"):
        missing.append("rowAdd")
    if not hasattr(module, "reduzierteStufen"):
        missing.append("reduzierteStufen")

    if missing:
        msg = f"Function(s) {', '.join(f'`{m}`' for m in missing)} not found in {FILE_NAME}"
        raise check50.Failure(msg)


# ---------- Tests für reduzierteStufen (Reduzierte Zeilenstufenform) ----------


@check50.check(has_functions)
def test_reduzierteStufen_3x4():
    """reduzierteStufen: 3x4-Matrix (Pivot nicht 1) in reduzierte Zeilenstufenform"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [2, 4, -2, 2],
        [0, 1, 1, 2],
        [0, 0, 1, 2.5],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1.0, 0.0, 0.0, 4.5],
        [0.0, 1.0, 0.0, -0.5],
        [0.0, 0.0, 1.0, 2.5],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_4x5():
    """reduzierteStufen: 4x5-Matrix (Pivot nicht 1) in reduzierte Zeilenstufenform"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [2, 4, 2, 0, 6],
        [0, 1, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_2x3():
    """reduzierteStufen: 2x3-Matrix (Pivot nicht 1) in reduzierte Zeilenstufenform"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [4, 8, -4],
        [0, 1, 1],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1.0, 0.0, -3.0],
        [0.0, 1.0, 1.0],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_5x6():
    """reduzierteStufen: 5x6-Matrix (Pivot nicht 1) in reduzierte Zeilenstufenform"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [2, 4, 0, 0, 8, 10],
        [0, 3, 6, 0, 9, 12],
        [0, 0, 5, 10, 15, 20],
        [0, 0, 0, 7, 14, 21],
        [0, 0, 0, 0, 11, 22],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0, 1.0, 0.0, 0.0, 0.0, -2.0],
        [0, 0, 1.0, 0.0, 0.0, 0.0],
        [0, 0, 0, 1.0, 0.0, -1.0],
        [0, 0, 0, 0, 1.0, 2.0],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_7x8():
    """reduzierteStufen: 7x8-Matrix (Pivot nicht 1) in reduzierte Zeilenstufenform"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [2, 4, 6, 8, 10, 12, 14, 16],
        [0, 3, 6, 9, 12, 15, 18, 21],
        [0, 0, 4, 8, 12, 16, 20, 24],
        [0, 0, 0, 5, 10, 15, 20, 25],
        [0, 0, 0, 0, 6, 12, 18, 24],
        [0, 0, 0, 0, 0, 7, 14, 21],
        [0, 0, 0, 0, 0, 0, 8, 16],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, -1],
        [0, 0, 0, 0, 0, 0, 1, 2],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_4x4_with_zero_rows():
    """reduzierteStufen: 4x4-Matrix, erwartete Form mit Nullzeilen unten"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [1, 2, 0, 3],
        [0, 1, 1, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1, 0, -2, -1],
        [0, 1, 1, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_identity_matrix_preserved():
    """reduzierteStufen: 3x3-Matrix Einheitsmatrix bleibt unverändert"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    matrices_almost_equal(M, expected)


@check50.check(has_functions)
def test_reduzierteStufen_zero_matrix_remains_zero():
    """reduzierteStufen: 3x4-Matrix Nullmatrix bleibt unverändert"""
    module = check50.py.import_(FILE_NAME)

    # Matrix liegt bereits in Zeilenstufenform vor
    M = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    module.rowAdd = a
    module.rowMult = m
    module.reduzierteStufen(M)

    expected = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    matrices_almost_equal(M, expected)


# ---------- Stil-Check ----------
@check50.check(has_functions)
def no_forbidden_methods():
    """does not use forbidden built-ins"""
    forbidden = {"rref", "numpy", "sympy"}

    with Path(FILE_NAME).open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            if tok_string in forbidden:
                msg = f"Found forbidden function '{tok_string}'"
                raise check50.Failure(msg)
