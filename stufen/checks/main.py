import check50
import check50.py

FILE_NAME = "stufen.py"


def pretty_matrix_diff(actual, expected):
    """Return a pretty diff between two matrices as a string with aligned columns."""
    lines = ["expected values in ():"]

    num_cols = max(
        len(row) for row in expected + actual
    )  # calculate the number of columns

    # calculate the maximum width for each column
    col_widths = []
    for col in range(num_cols):
        max_width = 0
        for row in expected + actual:
            if col < len(row):
                max_width = max(max_width, len(str(row[col])))
        col_widths.append(max_width)

    # build diff lines
    for i, (exp_row, act_row) in enumerate(zip(expected, actual, strict=False)):
        row_diff = []
        for j in range(num_cols):
            e = exp_row[j] if j < len(exp_row) else ""
            a = act_row[j] if j < len(act_row) else ""
            cell = f"{a}" if a == e else f"{a} ({e})"
            row_diff.append(cell.ljust(col_widths[j] + 4))  # pad with spaces
        lines.append(f"Row {i}: " + " | ".join(row_diff))

    return "\n".join(lines)


def ensure_row_functions(module):
    """Ensure module has rowAdd and rowMult.
    If missing, provide default implementations."""

    # add rowAdd default implementation
    if not hasattr(module, "rowAdd"):
        check50.log("PATCHING rowAdd")

        def rowAdd(M, i, j, k):
            """Addiert das k-fache der i-ten Zeile zur j-ten Zeile der Matrix M."""
            for col in range(len(M[j])):
                M[j][col] += k * M[i][col]

        module.rowAdd = rowAdd

    # add rowMult default implementation
    if not hasattr(module, "rowMult"):

        def rowMult(M, i, k):
            """Multipliziert die i-te Zeile der Matrix M mit dem Faktor k."""
            for col in range(len(M[i])):
                M[i][col] *= k

        module.rowMult = rowMult


@check50.check()
def exists():
    """stufen.py exists"""
    check50.exists(FILE_NAME)


@check50.check(exists)
def compiles():
    """stufen.py compiles"""
    check50.py.compile(FILE_NAME)


@check50.check(compiles)
def has_function():
    module = check50.py.import_(FILE_NAME)
    FUNCTION_NAME = "zeilenStufen"

    if not hasattr(module, FUNCTION_NAME):
        msg = f"Function {FUNCTION_NAME} not found in {FILE_NAME}"
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_3x4():
    """zeilenStufen: 3x4-Beispielmatrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [2, 4, -2, 2],
        [4, 9, -3, 8],
        [-2, -7, 1, -9],
    ]

    module.zeilenStufen(input)

    # Erwartete Zeilenstufenform bei reinem Vorwärtsschritt + Pivot-Skalierung
    expected = [
        [1.0, 2.0, -1.0, 1.0],
        [0.0, 1.0, 1.0, 4.0],
        [0.0, 0.0, 1.0, 2.5],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_4x5():
    """zeilenStufen: 4x5-Beispielmatrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [2, 4, 2, 0, 6],
        [1, 3, 1, 2, 5],
        [0, 1, 0, 1, 1],
        [3, 10, 3, 5, 12],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 2.0, 1.0, 0.0, 3.0],
        [0.0, 1.0, 0.0, 2.0, 2.0],
        [0.0, 0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_2x3():
    """zeilenStufen: 2x3-Matrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [4, 8, -4],
        [2, 3, 1],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 2.0, -1.0],
        [0.0, 1.0, -3.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_5x6():
    """zeilenStufen: 5x6-Matrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [2, 4, 0, 0, 8, 10],
        [0, 3, 6, 0, 9, 12],
        [0, 0, 5, 10, 15, 20],
        [0, 0, 0, 7, 14, 21],
        [0, 0, 0, 0, 11, 22],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 2.0, 0.0, 0.0, 4.0, 5.0],
        [0.0, 1.0, 2.0, 0.0, 3.0, 4.0],
        [0.0, 0.0, 1.0, 2.0, 3.0, 4.0],
        [0.0, 0.0, 0.0, 1.0, 2.0, 3.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_7x8():
    """zeilenStufen: 7x8-Matrix in Zeilenstufenform bringen"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [2, 4, 6, 8, 10, 12, 14, 16],
        [0, 3, 6, 9, 12, 15, 18, 21],
        [0, 0, 4, 8, 12, 16, 20, 24],
        [0, 0, 0, 5, 10, 15, 20, 25],
        [0, 0, 0, 0, 6, 12, 18, 24],
        [0, 0, 0, 0, 0, 7, 14, 21],
        [0, 0, 0, 0, 0, 0, 8, 16],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
        [0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        [0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_4x4_with_zero_rows():
    """zeilenStufen: 4x4-Matrix, erwartete Form mit Nullzeilen unten"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [1, 2, 0, 3],
        [2, 5, 1, 8],
        [0, 1, 1, 2],
        [3, 8, 2, 13],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 2.0, 0.0, 3.0],
        [0.0, 1.0, 1.0, 2.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_identity_matrix_preserved():
    """zeilenStufen: 3x3-Matrix Einheitsmatrix bleibt unverändert"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

    module.zeilenStufen(input)

    expected = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(has_function)
def test_zeilenStufen_zero_matrix_remains_zero():
    """zeilenStufen: 3x4-Matrix Nullmatrix bleibt unverändert"""
    module = check50.py.import_(FILE_NAME)
    ensure_row_functions(module)

    input = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    module.zeilenStufen(input)

    expected = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
    ]

    if expected != input:
        msg = pretty_matrix_diff(expected, input)
        raise check50.Failure(msg)


@check50.check(compiles)
def no_forbidden_methods():
    """does not use libraries"""
    import tokenize
    from pathlib import Path

    # forbidden libraries / functions and common aliases AND the import keyword
    forbidden = {"rref", "numpy", "sympy", "np", "sp", "import"}

    path = Path(FILE_NAME)

    with path.open() as f:
        tokens = list(tokenize.generate_tokens(f.readline))

        for tok_type, tok_string, *_ in tokens:
            # Skip comments and string literals
            if tok_type in (tokenize.COMMENT, tokenize.STRING):
                continue

            # Normalize to lowercase for case-insensitive check
            tok_lower = tok_string.lower()
            if tok_lower in forbidden:
                msg = f"Found forbidden function or library '{tok_string}'"
                raise check50.Failure(msg)
